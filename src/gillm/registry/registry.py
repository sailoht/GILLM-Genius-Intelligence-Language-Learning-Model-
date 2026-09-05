from typing import List, Optional
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.space.coordinates import SpatialCoordinate

class InformationRegistry3D:
    """
    3D spatial registry for registering, searching, and filtering Data Molecules.
    """
    def __init__(self):
        self.molecules: List[DataMolecule] = []

    def register(self, molecule: DataMolecule):
        self.molecules.append(molecule)

    def insert(self, molecule: DataMolecule):
        self.register(molecule)

    def register_molecule(self, molecule: DataMolecule):
        self.register(molecule)

    def query_spatial(self, origin: Optional[SpatialCoordinate] = None, radius: float = 0.0, center: Optional[SpatialCoordinate] = None) -> List[DataMolecule]:
        pos = origin or center or SpatialCoordinate(0, 0, 0)
        results = []
        for mol in self.molecules:
            if mol.spatial_position is not None:
                if isinstance(mol.spatial_position, tuple):
                    mol_pos = SpatialCoordinate(*mol.spatial_position)
                else:
                    mol_pos = mol.spatial_position
                dist = mol_pos.distance_to(pos)
                if dist <= radius:
                    results.append(mol)
        return results

    def spatial_search(self, origin: Optional[SpatialCoordinate] = None, radius: float = 0.0, center: Optional[SpatialCoordinate] = None) -> List[DataMolecule]:
        return self.query_spatial(origin=origin, radius=radius, center=center)

    def query_radius(self, origin: Optional[SpatialCoordinate] = None, radius: float = 0.0, center: Optional[SpatialCoordinate] = None) -> List[DataMolecule]:
        return self.query_spatial(origin=origin, radius=radius, center=center)

    def query_type(self, molecule_type: str) -> List[DataMolecule]:
        return [m for m in self.molecules if m.type == molecule_type or m.molecule_type == molecule_type]
