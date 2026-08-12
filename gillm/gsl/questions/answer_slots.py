from typing import Dict, Any, Optional
from gillm.gsl.syntax.chunks import ParseNode
from gillm.gsl.semantics.roles import SemanticRoleResolver

class QuestionPhaser:
    def __init__(self) -> None:
        self.role_resolver = SemanticRoleResolver()

    def phase_question(self, tree: ParseNode, resolved_roles: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Phases a question parse tree to determine its family, expected answer type, and missing slot.
        """
        if tree.label != "S_Q":
            return None

        question_family = None
        expected_answer = None
        missing_role = None

        # 1. Identify Wh-word or Yes/No structure
        wh_pron = self.role_resolver.find_node_by_label(tree, "Pron_Wh")
        wh_adv = self.role_resolver.find_node_by_label(tree, "Adv_Wh")
        aux_node = self.role_resolver.find_node_by_label(tree, "Aux")

        if wh_pron:
            lemma = wh_pron.candidate.lemma.lower() if wh_pron.candidate else ""
            if lemma == "who":
                question_family = "WHO"
                expected_answer = "PERSON"
            elif lemma == "what":
                question_family = "WHAT"
                expected_answer = "ENTITY"
            elif lemma == "which":
                question_family = "WHICH"
                expected_answer = "ENTITY"
            elif lemma == "whose":
                question_family = "WHOSE"
                expected_answer = "PERSON"
        elif wh_adv:
            lemma = wh_adv.candidate.lemma.lower() if wh_adv.candidate else ""
            if lemma == "where":
                question_family = "WHERE"
                expected_answer = "LOCATION"
            elif lemma == "why":
                question_family = "WHY"
                expected_answer = "CAUSE"
            elif lemma == "when":
                question_family = "WHEN"
                expected_answer = "TIME"
            elif lemma == "how":
                question_family = "HOW"
                expected_answer = "MANNER"
        else:
            # Yes/No Question
            question_family = "YES_NO"
            expected_answer = "BOOLEAN"

        # 2. Determine missing semantic role
        for role, val in resolved_roles.items():
            if val == "unknown":
                missing_role = role
                break

        return {
            "question_family": question_family,
            "expected_answer": expected_answer,
            "missing_role": missing_role
        }
