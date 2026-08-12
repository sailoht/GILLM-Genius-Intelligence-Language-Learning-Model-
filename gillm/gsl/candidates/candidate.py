from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from gillm.input.models import Token

@dataclass
class Candidate:
    token: Token
    lemma: str
    pos: str
    features: Dict[str, Any] = field(default_factory=dict)
    meaning: str = ""
    score: float = 1.0
    evidence: List[str] = field(default_factory=list)
    normalized_correction: Optional[str] = None
    correction_confidence: Optional[float] = None
