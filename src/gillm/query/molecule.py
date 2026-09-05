from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class QueryMolecule:
    """
    Structured query representation derived from human inputs via LangBaby.
    """
    intent: str = "SEARCH"
    entities: List[str] = field(default_factory=list)
    requested_relations: List[str] = field(default_factory=list)
    requested_properties: List[str] = field(default_factory=list)
    time_requirements: Dict[str, Any] = field(default_factory=dict)
    spatial_requirements: Dict[str, Any] = field(default_factory=dict)
    domain: str = "general"
    known_context: Dict[str, Any] = field(default_factory=dict)
