from typing import List, Dict, Any, Tuple
from gillm.gsl.candidates.candidate import Candidate
from gillm.gsl.syntax.chunks import ParseNode
from gillm.gsl.syntax.patterns import STANDARD_RULES, GrammarRule
from gillm.gsl.lexicon.loader import LexiconLoader

def map_pos_to_syntax_label(pos: str, lemma: str) -> str:
    pos_upper = pos.upper()
    lemma_lower = lemma.lower()
    if pos_upper == "DET":
        return "Det"
    elif pos_upper == "NOUN":
        return "Noun"
    elif pos_upper == "VERB":
        return "Verb"
    elif pos_upper == "AUX":
        return "Aux"
    elif pos_upper == "ADP":
        return "Adp"
    elif pos_upper == "PRON":
        if lemma_lower in ["who", "what", "which", "whose"]:
            return "Pron_Wh"
        return "Pron"
    elif pos_upper == "ADV":
        if lemma_lower in ["why", "where", "how", "when"]:
            return "Adv_Wh"
        return "Adv"
    return pos

def get_node_key(node: ParseNode) -> Tuple[str, Tuple[Tuple[int, str, str], ...]]:
    leaves = node.get_leaves()
    leaf_keys = tuple((l.token.position, l.lemma, l.pos) for l in leaves)
    return (node.label, leaf_keys)

def apply_unary_rules(cell: List[ParseNode], rules: List[GrammarRule]) -> None:
    """
    Repeatedly applies rules of length 1 to the given cell until no new categories can be derived.
    """
    added = True
    while added:
        added = False
        new_nodes = []
        existing_keys = {get_node_key(node) for node in cell}

        for rule in rules:
            if len(rule.pattern) == 1:
                for node in cell:
                    if rule.matches([node]):
                        combined = rule.combine([node])
                        key = get_node_key(combined)
                        if key not in existing_keys:
                            new_nodes.append(combined)
                            existing_keys.add(key)
                            added = True
        cell.extend(new_nodes)

class ChartParser:
    def __init__(self, rules: List[GrammarRule] = STANDARD_RULES) -> None:
        self.rules = rules
        self.lexicon = LexiconLoader.get_lexicon()

    def parse(self, candidates_grid: List[List[Candidate]]) -> List[ParseNode]:
        """
        Runs a general chart parser on the given grid of lexical candidates.
        Returns all valid sentence-level candidate trees (spanning the entire input).
        """
        n = len(candidates_grid)
        if n == 0:
            return []

        # chart[i][j] will store all ParseNodes spanning index i to j inclusive
        chart: List[List[List[ParseNode]]] = [[[] for _ in range(n)] for _ in range(n)]

        # 1. Base case: spans of length 1
        for i in range(n):
            for cand in candidates_grid[i]:
                syntax_label = map_pos_to_syntax_label(cand.pos, cand.lemma)

                lex_entry = self.lexicon.lookup(cand.lemma)
                sem_cats = lex_entry.semantic_categories if lex_entry else []

                feats = dict(cand.features)
                feats["semantic_categories"] = sem_cats
                if cand.normalized_correction:
                    feats["original_text"] = cand.token.text
                    feats["correction"] = cand.normalized_correction
                    feats["correction_confidence"] = cand.correction_confidence

                node = ParseNode(
                    label=syntax_label,
                    children=[],
                    candidate=cand,
                    features=feats,
                    score=cand.score,
                    evidence=[f"Leaf: {cand.token.text} -> {syntax_label} ({cand.lemma})"]
                )
                chart[i][i].append(node)

            # Apply unary rules on length 1 spans
            apply_unary_rules(chart[i][i], self.rules)

        # 2. Iterate over span widths
        for width in range(2, n + 1):
            for i in range(n - width + 1):
                j = i + width - 1

                for rule in self.rules:
                    rule_len = len(rule.pattern)

                    if rule_len == 2:
                        for k1 in range(i, j):
                            for left in chart[i][k1]:
                                for right in chart[k1 + 1][j]:
                                    if rule.matches([left, right]):
                                        combined = rule.combine([left, right])
                                        chart[i][j].append(combined)

                    elif rule_len == 3 and width >= 3:
                        for k1 in range(i, j - 1):
                            for k2 in range(k1 + 1, j):
                                for part1 in chart[i][k1]:
                                    for part2 in chart[k1 + 1][k2]:
                                        for part3 in chart[k2 + 1][j]:
                                            if rule.matches([part1, part2, part3]):
                                                combined = rule.combine([part1, part2, part3])
                                                chart[i][j].append(combined)

                    elif rule_len == 4 and width >= 4:
                        for k1 in range(i, j - 2):
                            for k2 in range(k1 + 1, j - 1):
                                for k3 in range(k2 + 1, j):
                                    for part1 in chart[i][k1]:
                                        for part2 in chart[k1 + 1][k2]:
                                            for part3 in chart[k2 + 1][k3]:
                                                for part4 in chart[k3 + 1][j]:
                                                    if rule.matches([part1, part2, part3, part4]):
                                                        combined = rule.combine([part1, part2, part3, part4])
                                                        chart[i][j].append(combined)

                # Apply unary rules on derived spans
                apply_unary_rules(chart[i][j], self.rules)

        full_parses = chart[0][n - 1]
        sentence_parses = [node for node in full_parses if node.label in ["S", "S_Q"]]

        if not sentence_parses:
            return full_parses
        return sentence_parses
