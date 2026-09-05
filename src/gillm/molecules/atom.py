from dataclasses import dataclass, field
from typing import Any, Optional, Dict
from src.gillm.provenance.model import ProvenanceRecord

@dataclass
class DataAtom:
    """
    Fundamental explicit information item.
    Examples: mass = 5 kg, velocity = 20 m/s, name = "Earth"
    """
    id: str
    type: str  # numeric, symbol, string, categorical, measurement
    value: Any
    unit: Optional[str] = None
    provenance: ProvenanceRecord = field(default_factory=ProvenanceRecord)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "value": self.value,
            "unit": self.unit,
            "provenance": self.provenance.to_dict()
        }
