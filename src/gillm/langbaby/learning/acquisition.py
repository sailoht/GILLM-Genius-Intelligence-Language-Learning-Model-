from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class StructuralHypothesis:
    pattern: str
    frequency: int = 1
    validated: bool = False

class LanguageLearner:
    """
    LangBaby language acquisition subsystem.
    Progressively extracts patterns from observed language without hardcoded memorization.
    Path: Observed Language -> Segmentation -> Pattern Extraction -> Structural Hypothesis -> Validation.
    """
    def __init__(self):
        self.hypotheses: Dict[str, StructuralHypothesis] = {}

    def observe(self, tokens: List[str]):
        # Simple pattern extraction e.g., DET NOUN VERB DET NOUN
        pattern_str = " ".join(tokens)
        if pattern_str in self.hypotheses:
            self.hypotheses[pattern_str].frequency += 1
            if self.hypotheses[pattern_str].frequency >= 3:
                self.hypotheses[pattern_str].validated = True
        else:
            self.hypotheses[pattern_str] = StructuralHypothesis(pattern=pattern_str)
