import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ProvenanceRecord:
    source: str = "UNKNOWN"
    transformation: str = "NONE"
    rule_used: str = "NONE"
    inputs_used: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def __init__(
        self,
        source: Optional[str] = None,
        transformation: Optional[str] = None,
        rule_used: Optional[str] = None,
        inputs_used: Optional[List[str]] = None,
        assumptions: Optional[List[str]] = None,
        timestamp: Optional[float] = None,
        source_id: Optional[str] = None,
        transformation_type: Optional[str] = None,
        input_ids: Optional[List[str]] = None
    ):
        self.source = source or source_id or "UNKNOWN"
        self.transformation = transformation or transformation_type or "NONE"
        self.rule_used = rule_used or "NONE"
        self.inputs_used = inputs_used if inputs_used is not None else (input_ids if input_ids is not None else [])
        self.assumptions = assumptions if assumptions is not None else []
        self.timestamp = timestamp or time.time()

    @property
    def source_id(self) -> str:
        return self.source

    @property
    def transformation_type(self) -> str:
        return self.transformation

    @property
    def input_ids(self) -> List[str]:
        return self.inputs_used

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "transformation": self.transformation,
            "rule_used": self.rule_used,
            "inputs_used": self.inputs_used,
            "assumptions": self.assumptions,
            "timestamp": self.timestamp
        }
