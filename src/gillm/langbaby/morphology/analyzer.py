from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MorphologicalAnalysis:
    raw_word: str
    lemma: str
    pos: str
    tense: Optional[str] = None
    number: Optional[str] = None
    person: Optional[str] = None
    voice: Optional[str] = None

class MorphologicalAnalyzer:
    """
    Deterministic morphological analyzer supporting affixes and irregular forms.
    Generates candidate analyses without premature guessing.
    """
    def __init__(self):
        self.irregular_past = {
            "kicked": "kick",
            "saw": "see",
            "went": "go",
            "opened": "open",
            "was": "be",
            "were": "be",
        }

    def analyze(self, word: str) -> List[MorphologicalAnalysis]:
        analyses: List[MorphologicalAnalysis] = []
        w_lower = word.lower()

        # Irregular checks
        if w_lower in self.irregular_past:
            lemma = self.irregular_past[w_lower]
            analyses.append(MorphologicalAnalysis(
                raw_word=word, lemma=lemma, pos="VERB", tense="PAST"
            ))

        # Regular suffixes
        if w_lower.endswith("ed"):
            lemma = w_lower[:-2]
            analyses.append(MorphologicalAnalysis(
                raw_word=word, lemma=lemma, pos="VERB", tense="PAST"
            ))
        elif w_lower.endswith("s") and not w_lower.endswith("ss"):
            lemma = w_lower[:-1]
            analyses.append(MorphologicalAnalysis(
                raw_word=word, lemma=lemma, pos="VERB", tense="PRESENT", person="3SG"
            ))
            analyses.append(MorphologicalAnalysis(
                raw_word=word, lemma=lemma, pos="NOUN", number="PLURAL"
            ))
        elif w_lower.endswith("ing"):
            lemma = w_lower[:-3]
            analyses.append(MorphologicalAnalysis(
                raw_word=word, lemma=lemma, pos="VERB", tense="PARTICIPLE"
            ))

        # Default fallback
        if not analyses:
            analyses.append(MorphologicalAnalysis(raw_word=word, lemma=w_lower, pos="UNKNOWN"))

        return analyses
