from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# Correction levels
LEVEL_0 = 0  # No correction
LEVEL_1 = 1  # Very strong correction
LEVEL_2 = 2  # Likely correction
LEVEL_3 = 3  # Possible correction
LEVEL_4 = 4  # Ambiguous — preserve alternatives / request clarification
LEVEL_5 = 5  # Unknown — do not guess

# Language variations
STANDARD = "STANDARD"
INFORMAL = "INFORMAL"
NON_STANDARD = "NON_STANDARD"
DIALECTAL = "DIALECTAL"
POETIC = "POETIC"
QUOTED = "QUOTED"
POSSIBLE_ERROR = "POSSIBLE_ERROR"
UNKNOWN = "UNKNOWN"

@dataclass
class ErrorObject:
    error_type: str
    location: str  # e.g., "token_0", "sentence", "index_3"
    original: str
    evidence: List[str] = field(default_factory=list)
    candidates: List[str] = field(default_factory=list)
    status: str = "DETECTED"  # DETECTED, POSSIBLE, HIGH_CONFIDENCE, AMBIGUITY, UNKNOWN, VALIDATED
    reason: str = ""
    correction_level: int = LEVEL_3

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.error_type,
            "location": self.location,
            "original": self.original,
            "evidence": self.evidence,
            "candidates": self.candidates,
            "status": self.status,
            "reason": self.reason
        }
