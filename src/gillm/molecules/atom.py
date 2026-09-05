from dataclasses import dataclass, field
from typing import Any, Optional
from src.gillm.provenance.model import ProvenanceRecord

@dataclass
class DataAtom:
    """
    Primitive unit of information in GILLM: (id, type, value, unit, provenance).
    Supports backward and forward parameter aliases (id/atom_id, type/atom_type).
    """
    id: str = "atom_default"
    type: str = "GENERIC"
    value: Any = None
    unit: Optional[str] = None
    provenance: ProvenanceRecord = field(default_factory=ProvenanceRecord)

    def __init__(
        self,
        id: Optional[str] = None,
        type: Optional[str] = None,
        value: Any = None,
        unit: Optional[str] = None,
        provenance: Optional[ProvenanceRecord] = None,
        atom_id: Optional[str] = None,
        atom_type: Optional[str] = None
    ):
        self.id = id or atom_id or "atom_default"
        self.type = type or atom_type or "GENERIC"
        self.value = value
        self.unit = unit
        self.provenance = provenance or ProvenanceRecord()

    @property
    def atom_id(self) -> str:
        return self.id

    @property
    def atom_type(self) -> str:
        return self.type
