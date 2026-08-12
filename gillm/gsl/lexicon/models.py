from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class LexicalEntry:
    surface: str
    lemma: str
    pos_candidates: List[str]  # e.g. ["NOUN", "VERB"]
    definition: str = ""
    morphological_features: Dict[str, Any] = field(default_factory=dict)
    frequency: float = 1.0
    semantic_categories: List[str] = field(default_factory=list)  # e.g. ["PERSON", "ENTITY"]
    verb_frames: List[str] = field(default_factory=list)  # e.g. ["AGENT_PATIENT", "AGENT_GOAL", "AGENT"]
    transitivity: Optional[str] = None  # e.g. "transitive", "intransitive", "ditransitive"
