from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Union
from src.gillm.molecules.atom import DataAtom
from src.gillm.space.coordinates import SpatialCoordinate
from src.gillm.vectors.model import Vector
from src.gillm.provenance.model import ProvenanceRecord
from src.gillm.core.enums import EpistemicStatus, ValidationStatus

@dataclass(unsafe_hash=True)
class DataMolecule:
    """
    3D Information Object representing an individual object, concept, event, or scenario.
    Capable of representing state, vectors (position, velocity, acceleration), relations, and time history.
    """
    id: str = "mol_default"
    type: str = "GENERIC_MOLECULE"
    name: str = "GenericMolecule"
    data_atoms: Dict[str, DataAtom] = field(default_factory=dict, hash=False)
    state: Dict[str, Any] = field(default_factory=dict, hash=False)
    vector_state: Dict[str, Vector] = field(default_factory=dict, hash=False)
    relations: List[Dict[str, Any]] = field(default_factory=list, hash=False)
    spatial_position: Optional[SpatialCoordinate] = field(default=None, hash=False)
    provenance: ProvenanceRecord = field(default_factory=ProvenanceRecord, hash=False)
    epistemic_status: EpistemicStatus = field(default=EpistemicStatus.OBSERVED, hash=False)
    validation_status: ValidationStatus = field(default=ValidationStatus.VALID, hash=False)
    laws: list = field(default_factory=list, hash=False)

    def __init__(
        self,
        id: Optional[str] = None,
        type: Optional[str] = None,
        name: Optional[str] = None,
        data_atoms: Optional[Dict[str, DataAtom]] = None,
        atoms: Optional[Dict[str, DataAtom]] = None,
        state: Optional[Dict[str, Any]] = None,
        vector_state: Optional[Dict[str, Vector]] = None,
        relations: Optional[List[Dict[str, Any]]] = None,
        spatial_position: Optional[Union[SpatialCoordinate, tuple]] = None,
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
        self.vector_state = vector_state if vector_state is not None else {}
        self.relations = relations if relations is not None else []

        if isinstance(spatial_position, tuple):
            self.spatial_position = SpatialCoordinate(*spatial_position)
        else:
            self.spatial_position = spatial_position

        self.provenance = provenance or ProvenanceRecord()
        self.epistemic_status = epistemic_status or EpistemicStatus.OBSERVED
        self.validation_status = validation_status or ValidationStatus.VALID
        self.laws = laws if laws is not None else []

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataMolecule):
            return False
        return self.id == other.id

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

    def add_relation(self, target_id: str, relation_type: str):
        self.relations.append({"target_id": target_id, "relation_type": relation_type})

    def __getitem__(self, key: str) -> Any:
        d = self.to_dict()
        if key in d:
            return d[key]
        raise KeyError(key)

    def to_dict(self) -> Dict[str, Any]:
        atoms_dict = {}
        for k, atom in self.data_atoms.items():
            if hasattr(atom, 'value'):
                atoms_dict[k] = {
                    "id": getattr(atom, 'id', k),
                    "type": getattr(atom, 'type', 'GENERIC'),
                    "value": atom.value,
                    "unit": getattr(atom, 'unit', None)
                }
            else:
                atoms_dict[k] = atom

        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "data_atoms": atoms_dict,
            "atoms": atoms_dict,
            "state": self.state,
            "vector_state": {k: v.to_list() for k, v in self.vector_state.items()},
            "relations": self.relations,
            "epistemic_status": self.epistemic_status.value if isinstance(self.epistemic_status, EpistemicStatus) else str(self.epistemic_status),
            "validation_status": self.validation_status.value if isinstance(self.validation_status, ValidationStatus) else str(self.validation_status),
            "laws": self.laws,
            "provenance": self.provenance.to_dict() if hasattr(self.provenance, 'to_dict') else {}
        }
