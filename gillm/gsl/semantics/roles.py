from typing import Dict, Any, List, Optional
from gillm.gsl.syntax.chunks import ParseNode
from gillm.gsl.semantics.verb_frames import VerbFrameRegistry, VerbFrame

class SemanticRoleResolver:
    def __init__(self) -> None:
        self.vf_registry = VerbFrameRegistry()

    def find_node_by_label(self, node: ParseNode, label: str) -> Optional[ParseNode]:
        if node.label == label:
            return node
        for child in node.children:
            found = self.find_node_by_label(child, label)
            if found:
                return found
        return None

    def find_all_nodes_by_label(self, node: ParseNode, label: str) -> List[ParseNode]:
        results = []
        if node.label == label:
            results.append(node)
        for child in node.children:
            results.extend(self.find_all_nodes_by_label(child, label))
        return results

    def extract_np_concept(self, np_node: ParseNode) -> str:
        """Extracts the head noun or pronoun of an NP."""
        leaves = np_node.get_leaves()
        # 1. Look for NOUN or PRON
        for leaf in leaves:
            if leaf.pos in ["NOUN", "PRON"]:
                return leaf.normalized_correction or leaf.token.text
        # 2. Look for DET or others
        for leaf in leaves:
            if leaf.pos in ["DET", "ADP", "AUX", "PUNCT"]:
                # skip punctuation unless needed
                if leaf.pos == "PUNCT":
                    continue
                return leaf.normalized_correction or leaf.token.text
        # 3. Absolute fallback
        if leaves:
            return leaves[-1].normalized_correction or leaves[-1].token.text
        return "unknown"

    def resolve(self, tree: ParseNode) -> Dict[str, Any]:
        """
        Resolves semantic roles for a given parse tree using the syntax and verb frame.
        """
        roles: Dict[str, Any] = {}

        verb_node = self.find_node_by_label(tree, "Verb")
        if not verb_node or not verb_node.candidate:
            vp_node = self.find_node_by_label(tree, "VP")
            if vp_node:
                verb_node = self.find_node_by_label(vp_node, "Verb")

        if not verb_node or not verb_node.candidate:
            return roles

        verb_lemma = verb_node.candidate.lemma.lower()
        frame = self.vf_registry.get_frame(verb_lemma)
        if not frame:
            frame = VerbFrame(verb_lemma, ["AGENT", "PATIENT"], "transitive")

        roles["action"] = verb_lemma

        # Determine voice
        voice = "ACTIVE"
        aux_node = self.find_node_by_label(tree, "Aux")
        is_past_verb = verb_node.features.get("tense") == "PAST"
        by_pp = None

        pps = self.find_all_nodes_by_label(tree, "PP")
        for pp in pps:
            pp_leaves = pp.get_leaves()
            if pp_leaves and pp_leaves[0].lemma.lower() == "by":
                by_pp = pp
                break

        if aux_node and aux_node.candidate and aux_node.candidate.lemma.lower() in ["be", "was", "were"]:
            if is_past_verb or by_pp:
                voice = "PASSIVE"

        # Find NP nodes
        nps = self.find_all_nodes_by_label(tree, "NP")

        if tree.label == "S":
            if voice == "PASSIVE":
                if len(nps) > 0:
                    roles["patient"] = self.extract_np_concept(nps[0])
                if by_pp:
                    pp_nps = self.find_all_nodes_by_label(by_pp, "NP")
                    if pp_nps:
                        roles["agent"] = self.extract_np_concept(pp_nps[0])
            else:
                if len(nps) >= 2:
                    subj_role = frame.roles[0].lower()
                    obj_role = frame.roles[1].lower() if len(frame.roles) > 1 else "patient"
                    roles[subj_role] = self.extract_np_concept(nps[0])
                    roles[obj_role] = self.extract_np_concept(nps[1])
                elif len(nps) == 1:
                    subj_role = frame.roles[0].lower()
                    roles[subj_role] = self.extract_np_concept(nps[0])

        elif tree.label == "S_Q":
            wh_pron = self.find_node_by_label(tree, "Pron_Wh")
            wh_adv = self.find_node_by_label(tree, "Adv_Wh")

            is_yes_no = (not wh_pron and not wh_adv and aux_node is not None)

            if is_yes_no:
                if len(nps) >= 2:
                    subj_role = frame.roles[0].lower()
                    obj_role = frame.roles[1].lower() if len(frame.roles) > 1 else "patient"
                    roles[subj_role] = self.extract_np_concept(nps[0])
                    roles[obj_role] = self.extract_np_concept(nps[1])
                elif len(nps) == 1:
                    subj_role = frame.roles[0].lower()
                    roles[subj_role] = self.extract_np_concept(nps[0])

            elif wh_pron:
                wh_lemma = wh_pron.candidate.lemma.lower()
                if len(tree.children) == 2 and tree.children[0].label == "Pron_Wh":
                    subj_role = frame.roles[0].lower()
                    roles[subj_role] = "unknown"
                    if len(nps) > 0:
                        obj_role = frame.roles[1].lower() if len(frame.roles) > 1 else "patient"
                        roles[obj_role] = self.extract_np_concept(nps[0])
                else:
                    if len(nps) > 0:
                        subj_role = frame.roles[0].lower()
                        roles[subj_role] = self.extract_np_concept(nps[0])
                    obj_role = frame.roles[1].lower() if len(frame.roles) > 1 else "patient"
                    roles[obj_role] = "unknown"

            elif wh_adv:
                wh_lemma = wh_adv.candidate.lemma.lower()
                if len(nps) > 0:
                    subj_role = frame.roles[0].lower()
                    roles[subj_role] = self.extract_np_concept(nps[0])
                if len(nps) >= 2:
                    obj_role = frame.roles[1].lower() if len(frame.roles) > 1 else "patient"
                    roles[obj_role] = self.extract_np_concept(nps[1])

                if wh_lemma == "where":
                    loc_role = "destination" if "DESTINATION" in frame.roles else "location"
                    roles[loc_role] = "unknown"
                elif wh_lemma == "why":
                    roles["cause"] = "unknown"

        return roles
