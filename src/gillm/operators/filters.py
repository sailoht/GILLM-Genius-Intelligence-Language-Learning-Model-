from typing import List, Dict, Any
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.query.molecule import QueryMolecule
from src.gillm.space.coordinates import SpatialCoordinate

class OperatorFilter:
    """Base class for filterization operators: S_n = O_n(S_n-1, Query)."""
    def filter(self, molecules: List[DataMolecule], query: QueryMolecule) -> List[DataMolecule]:
        raise NotImplementedError

class SpatialFilter(OperatorFilter):
    def filter(self, molecules: List[DataMolecule], query: QueryMolecule) -> List[DataMolecule]:
        if not query.spatial_requirements or "center" not in query.spatial_requirements:
            return molecules
        center = SpatialCoordinate(*query.spatial_requirements["center"])
        radius = query.spatial_requirements.get("radius", 10.0)
        return [m for m in molecules if center.distance_to(SpatialCoordinate(*m.spatial_position)) <= radius]

class SemanticFilter(OperatorFilter):
    def filter(self, molecules: List[DataMolecule], query: QueryMolecule) -> List[DataMolecule]:
        if not query.entities:
            return molecules
        results = []
        for m in molecules:
            name_lower = m.name.lower()
            if any(e.lower() in name_lower or any(e.lower() in atom_id.lower() for atom_id in m.data_atoms) for e in query.entities):
                results.append(m)
        return results

class FilterPipeline:
    """Applies a sequence of operator filters in order."""
    def __init__(self, operators: List[OperatorFilter]) -> None:
        self.operators = operators

    def apply(self, molecules: List[DataMolecule], query: QueryMolecule) -> List[DataMolecule]:
        curr = molecules
        for op in self.operators:
            curr = op.filter(curr, query)
        return curr
