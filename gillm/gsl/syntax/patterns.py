from typing import List, Optional, Dict, Any
from gillm.gsl.syntax.chunks import ParseNode

class GrammarRule:
    def __init__(self, name: str, pattern: List[str], output_label: str) -> None:
        self.name = name
        self.pattern = pattern
        self.output_label = output_label

    def matches(self, nodes: List[ParseNode]) -> bool:
        if len(nodes) != len(self.pattern):
            return False
        for node, pat in zip(nodes, self.pattern):
            if node.label != pat:
                return False
        return True

    def combine(self, nodes: List[ParseNode]) -> ParseNode:
        merged_features: Dict[str, Any] = {}
        total_score = 1.0
        evidence = [f"Applied rule: {self.name}"]

        for node in nodes:
            merged_features.update(node.features)
            total_score *= node.score
            if node.evidence:
                evidence.extend(node.evidence)

        # Special feature propagation rules:
        if self.output_label == "NP":
            for node in nodes:
                if node.label == "Noun":
                    merged_features["number"] = node.features.get("number", "SINGULAR")
                if node.label in ["Noun", "Pron", "Det"]:
                    if "semantic_categories" in node.features:
                        merged_features["semantic_categories"] = node.features["semantic_categories"]

        elif self.output_label == "PP":
            for node in nodes:
                if node.label == "Adp" and node.candidate and node.candidate.lemma.lower() == "by":
                    merged_features["role"] = "AGENT_BY"

        elif self.output_label == "VP":
            has_aux = any(node.label == "Aux" for node in nodes)
            for node in nodes:
                if node.label == "Verb":
                    if not has_aux:
                        merged_features["tense"] = node.features.get("tense", "PRESENT")
                    merged_features["aspect"] = node.features.get("aspect")
                    merged_features["number"] = node.features.get("number")
                    merged_features["person"] = node.features.get("person")
                elif node.label == "Aux":
                    merged_features["tense"] = node.features.get("tense", "PRESENT")

                # Propagate passive voice or role from PP
                if node.label == "PP" and node.features.get("role") == "AGENT_BY":
                    merged_features["voice"] = "PASSIVE"

        elif self.output_label == "S" or self.output_label == "S_Q":
            has_aux = any(node.label == "Aux" for node in nodes)
            for node in nodes:
                if node.label == "Aux":
                    merged_features["tense"] = node.features.get("tense", "PRESENT")
                elif node.label == "VP" and not has_aux:
                    merged_features["tense"] = node.features.get("tense")
                    merged_features["aspect"] = node.features.get("aspect")

                if node.label == "VP":
                    merged_features["voice"] = node.features.get("voice", "ACTIVE")
                if node.label == "PP" and node.features.get("role") == "AGENT_BY":
                    merged_features["voice"] = "PASSIVE"

        return ParseNode(
            label=self.output_label,
            children=nodes,
            features=merged_features,
            score=total_score,
            evidence=evidence
        )


STANDARD_RULES = [
    # 1. NP rules
    GrammarRule("Det + Noun -> NP", ["Det", "Noun"], "NP"),
    GrammarRule("Noun -> NP", ["Noun"], "NP"),
    GrammarRule("Pron -> NP", ["Pron"], "NP"),
    GrammarRule("NP + PP -> NP", ["NP", "PP"], "NP"),

    # 2. PP rule
    GrammarRule("Adp + NP -> PP", ["Adp", "NP"], "PP"),

    # 3. VP rules
    GrammarRule("Verb + NP -> VP", ["Verb", "NP"], "VP"),
    GrammarRule("Verb -> VP", ["Verb"], "VP"),
    GrammarRule("Aux + VP -> VP", ["Aux", "VP"], "VP"),
    GrammarRule("VP + PP -> VP", ["VP", "PP"], "VP"),
    GrammarRule("Verb + NP + VP -> VP", ["Verb", "NP", "VP"], "VP"),  # Perception verb bare infinitive clause

    # 4. Sentence rules (Declarative)
    GrammarRule("NP + VP -> S", ["NP", "VP"], "S"),

    # 5. Question rules (Interrogative)
    # Wh-Questions
    GrammarRule("Pron(Wh) + VP -> S_Q", ["Pron_Wh", "VP"], "S_Q"),
    GrammarRule("Pron(Wh) + Aux + NP + VP -> S_Q", ["Pron_Wh", "Aux", "NP", "VP"], "S_Q"),
    GrammarRule("Adv(Wh) + Aux + NP + VP -> S_Q", ["Adv_Wh", "Aux", "NP", "VP"], "S_Q"),

    # Yes/No Questions
    GrammarRule("Aux + NP + VP -> S_Q", ["Aux", "NP", "VP"], "S_Q"),
]
