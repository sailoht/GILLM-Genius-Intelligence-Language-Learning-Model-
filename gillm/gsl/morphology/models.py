from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class MorphologicalAnalysis:
    lemma: str
    pos: str
    features: Dict[str, Any] = field(default_factory=dict)
