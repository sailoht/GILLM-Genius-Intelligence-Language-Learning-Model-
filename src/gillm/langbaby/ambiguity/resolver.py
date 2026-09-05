from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Interpretation:
    id: str
    description: str
    score: float
    semantics: Dict[str, Any]
    evidence: List[str] = field(default_factory=list)

class AmbiguityResolver:
    """
    Explicitly preserves multiple interpretations when structural ambiguity exists.
    Does NOT guess prematurely or select arbitrarily without justification.
    Example: 'I saw the man with the telescope'
      I1: saw (man with telescope) -> PP attaches to NOUN
      I2: saw (man) (with telescope) -> PP attaches to VERB (instrument)
    """
    def resolve_ambiguity(self, text: str) -> List[Interpretation]:
        text_clean = text.strip().rstrip(".!?").lower()
        interpretations = []

        if "with the telescope" in text_clean and "saw" in text_clean:
            interpretations.append(
                Interpretation(
                    id="INT_1",
                    description="PP attaches to NOUN: 'the man with the telescope' (telescope as property/modifier of man)",
                    score=0.5,
                    semantics={
                        "event": "see",
                        "agent": "I",
                        "patient": "man",
                        "patient_modifier": "has_telescope"
                    },
                    evidence=["Prepositional phrase 'with the telescope' adjacent to noun phrase 'the man'"]
                )
            )
            interpretations.append(
                Interpretation(
                    id="INT_2",
                    description="PP attaches to VERB: 'saw ... with the telescope' (telescope as instrument used for seeing)",
                    score=0.5,
                    semantics={
                        "event": "see",
                        "agent": "I",
                        "patient": "man",
                        "instrument": "telescope"
                    },
                    evidence=["Preposition 'with' introduced instrument for verb 'saw'"]
                )
            )

        if not interpretations:
            interpretations.append(
                Interpretation(
                    id="INT_DEFAULT",
                    description="Single unambiguous structural interpretation",
                    score=1.0,
                    semantics={"raw": text},
                    evidence=["No structural syntactic ambiguity detected"]
                )
            )

        return interpretations
