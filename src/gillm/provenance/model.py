import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ProvenanceRecord:
    source: str = "SYSTEM_INITIAL"
    transformation: str = "DIRECT_ASSIGNMENT"
    rule_used: str = "NONE"
    inputs_used: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "transformation": self.transformation,
            "rule_used": self.rule_used,
            "inputs_used": self.inputs_used,
            "assumptions": self.assumptions,
            "timestamp": self.timestamp
        }

class ProvenanceGraph:
    """Tracks full derivation chains and input dependency trees for proof-carrying states."""
    def __init__(self) -> None:
        self.nodes: Dict[str, ProvenanceRecord] = {}

    def add_record(self, item_id: str, record: ProvenanceRecord) -> None:
        self.nodes[item_id] = record

    def get_derivation_chain(self, item_id: str) -> List[Dict[str, Any]]:
        chain = []
        visited = set()
        curr = item_id

        while curr and curr in self.nodes and curr not in visited:
            visited.add(curr)
            rec = self.nodes[curr]
            chain.append({"item_id": curr, "provenance": rec.to_dict()})
            if rec.inputs_used:
                curr = rec.inputs_used[0]
            else:
                break
        return chain
