from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from src.gillm.molecules.atom import DataAtom
from src.gillm.space.coordinates import SpatialCoordinate
from src.gillm.provenance.model import ProvenanceRecord
from src.gillm.core.enums import EpistemicStatus, ValidationStatus

@dataclass
class DataMolecule:
    """
    3D Information Object representing a structured piece of data in GILLM.
    Supports backward and forward attribute aliases, serialization, and helper methods.
    """
    id: str = "mol_default"
    type: str = "GENERIC_MOLECULE"
    name: str = "GenericMolecule"
    data_atoms: Dict[str, DataAtom] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)
    spatial_position: Optional[SpatialCoordinate] = None
    provenance: ProvenanceRecord = field(default_factory=ProvenanceRecord)
    epistemic_status: EpistemicStatus = EpistemicStatus.OBSERVED
    validation_status: ValidationStatus = ValidationStatus.VALID
    laws: list = field(default_factory=list)

    def __init__(
        self,
        id: Optional[str] = None,
        type: Optional[str] = None,
        name: Optional[str] = None,
        data_atoms: Optional[Dict[str, DataAtom]] = None,
        atoms: Optional[Dict[str, DataAtom]] = None,
        state: Optional[Dict[str, Any]] = None,
        spatial_position: Optional[SpatialCoordinate] = None,
        provenance: Optional[ProvenanceRecord] = None,
        epistemic_status: Optional[EpistemicStatus] = None,
        validation_status: Optional[ValidationStatus] = None,
        molecule_id: Optional[str] = None,
        molecule_type: Optional[str] = None,
        laws: Optional[list] = None
    ):
        self.id = id or molecule_id or "mol_default"
        self.type = type or molecule_type or "GENERIC_MOLECULE"
        self.name = name or self.type
        self.data_atoms = data_atoms if data_atoms is not None else (atoms if atoms is not None else {})
        self.state = state if state is not None else {}
        self.spatial_position = spatial_position
        self.provenance = provenance or ProvenanceRecord()
        self.epistemic_status = epistemic_status or EpistemicStatus.OBSERVED
        self.validation_status = validation_status or ValidationStatus.VALID
        self.laws = laws if laws is not None else []

    @property
    def molecule_id(self) -> str:
        return self.id

    @property
    def molecule_type(self) -> str:
        return self.type

    @property
    def atoms(self) -> Dict[str, DataAtom]:
        return self.data_atoms

    @atoms.setter
    def atoms(self, val: Dict[str, DataAtom]):
        self.data_atoms = val

    def add_atom(self, key_or_atom: Any, atom_obj: Optional[DataAtom] = None):
        if isinstance(key_or_atom, DataAtom):
            atom = key_or_atom
            key = atom.id or atom.type.lower()
        else:
            key = str(key_or_atom)
            atom = atom_obj
        if atom is not None:
            self.data_atoms[key] = atom
            if hasattr(atom, 'value') and hasattr(atom, 'type'):
                self.state[atom.type] = atom.value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "state": self.state,
            "epistemic_status": self.epistemic_status.value if isinstance(self.epistemic_status, EpistemicStatus) else str(self.epistemic_status),
            "validation_status": self.validation_status.value if isinstance(self.validation_status, ValidationStatus) else str(self.validation_status),
            "laws": self.laws,
            "provenance": self.provenance.to_dict() if hasattr(self.provenance, 'to_dict') else {}
        }
