from typing import List, Optional, Any
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.space.coordinates import SpatialCoordinate

class SpatialFilter:
    def __init__(self, center: Optional[SpatialCoordinate] = None, radius: float = 0.0):
        self.center = center or SpatialCoordinate(0, 0, 0)
        self.radius = radius

    def filter(self, molecules: List[DataMolecule]) -> List[DataMolecule]:
        results = []
        for m in molecules:
            if m.spatial_position is not None:
                if m.spatial_position.distance_to(self.center) <= self.radius:
                    results.append(m)
        return results

class SemanticFilter:
    def __init__(self, required_type: Optional[str] = None):
        self.required_type = required_type or "GENERIC_MOLECULE"

    def filter(self, molecules: List[DataMolecule]) -> List[DataMolecule]:
        return [m for m in molecules if m.type == self.required_type or m.molecule_type == self.required_type]

class FilterPipeline:
    def __init__(self, filters: Optional[List[Any]] = None):
        self.filters = filters if filters is not None else []

    def add_filter(self, filter_obj):
        self.filters.append(filter_obj)

    def apply(self, molecules: List[DataMolecule], query: Optional[Any] = None) -> List[DataMolecule]:
        current = list(molecules)
        for f in self.filters:
            current = f.filter(current)
        return current
