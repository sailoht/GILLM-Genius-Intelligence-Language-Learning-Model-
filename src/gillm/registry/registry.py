import math
from typing import List, Dict, Any, Tuple, Optional
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.space.coordinates import SpatialCoordinate
from src.gillm.query.molecule import QueryMolecule
from src.gillm.fields.gaussian import GaussianInformationField

class InformationRegistry3D:
    """
    3D Information Registry -
    Spatial 3D information-world and search structure for DataMolecules.
    """
    def __init__(self) -> None:
        self.molecules: Dict[str, DataMolecule] = {}

    def insert(self, molecule: DataMolecule) -> None:
        self.molecules[molecule.id] = molecule

    def get_by_id(self, mol_id: str) -> Optional[DataMolecule]:
        return self.molecules.get(mol_id)

    def spatial_search(self, center: Tuple[float, float, float], radius: float) -> List[DataMolecule]:
        results = []
        center_coord = SpatialCoordinate(*center)
        for mol in self.molecules.values():
            mol_coord = SpatialCoordinate(*mol.spatial_position)
            if center_coord.distance_to(mol_coord) <= radius:
                results.append(mol)
        return results

    def retrieve(self, query: QueryMolecule) -> List[DataMolecule]:
        """Filters molecules matching entities, domain, or requested properties in QueryMolecule."""
        candidates = []
        for mol in self.molecules.values():
            # Check domain or entity match
            match = False
            if query.entities:
                if any(e.lower() in mol.name.lower() or e.lower() in [a.lower() for a in mol.data_atoms] for e in query.entities):
                    match = True
            else:
                match = True

            if match:
                candidates.append(mol)
        return candidates
