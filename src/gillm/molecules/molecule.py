from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from src.gillm.core.enums import EpistemicStatus, ValidationStatus
from src.gillm.molecules.atom import DataAtom
from src.gillm.provenance.model import ProvenanceRecord

@dataclass
class DataMolecule:
    """
    Structured information object representing an entity, concept, event, state, or object:
    M = (data, state, vector, sets, relations, spatial_position, temporal_state, gaussian_field, laws, provenance)
    """
    id: str
    name: str
    data_atoms: Dict[str, DataAtom] = field(default_factory=dict)
    epistemic_status: EpistemicStatus = EpistemicStatus.OBSERVED
    validation_status: ValidationStatus = ValidationStatus.VALID
    vector: Optional[List[float]] = None
    sets: Dict[str, List[str]] = field(default_factory=dict)
    relations: List[Dict[str, Any]] = field(default_factory=list)
    spatial_position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    temporal_state: Dict[str, Any] = field(default_factory=dict)
    gaussian_field: Dict[str, Any] = field(default_factory=dict)
    laws: List[str] = field(default_factory=list)
    provenance: ProvenanceRecord = field(default_factory=ProvenanceRecord)

    def add_atom(self, atom: DataAtom) -> None:
        self.data_atoms[atom.id] = atom

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "data_atoms": {k: v.to_dict() for k, v in self.data_atoms.items()},
            "epistemic_status": self.epistemic_status.value,
            "validation_status": self.validation_status.value,
            "vector": self.vector,
            "sets": self.sets,
            "relations": self.relations,
            "spatial_position": list(self.spatial_position),
            "temporal_state": self.temporal_state,
            "gaussian_field": self.gaussian_field,
            "laws": self.laws,
            "provenance": self.provenance.to_dict()
        }
