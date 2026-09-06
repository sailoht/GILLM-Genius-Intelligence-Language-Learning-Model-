from typing import List, Optional, Any
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.space.coordinates import SpatialCoordinate

class SpatialFilter:
    def __init__(self, center: Optional[Any] = None, radius: float = 0.0):
        if isinstance(center, tuple):
            self.center = SpatialCoordinate(*center)
        else:
            self.center = center or SpatialCoordinate(0, 0, 0)
        self.radius = radius

    def filter(self, molecules: List[DataMolecule], query: Optional[Any] = None) -> List[DataMolecule]:
        center = self.center
        radius = self.radius

        if query is not None:
            spatial_reqs = None
            if hasattr(query, 'spatial_requirements') and query.spatial_requirements:
                spatial_reqs = query.spatial_requirements
            elif isinstance(query, dict) and 'spatial_requirements' in query:
                spatial_reqs = query['spatial_requirements']

            if spatial_reqs:
                if 'center' in spatial_reqs:
                    c = spatial_reqs['center']
                    center = SpatialCoordinate(*c) if isinstance(c, tuple) else c
                if 'radius' in spatial_reqs:
                    radius = float(spatial_reqs['radius'])

        results = []
        for m in molecules:
            if m.spatial_position is not None:
                if isinstance(m.spatial_position, tuple):
                    mol_pos = SpatialCoordinate(*m.spatial_position)
                else:
                    mol_pos = m.spatial_position
                if mol_pos.distance_to(center) <= radius:
                    results.append(m)
        return results

class SemanticFilter:
    def __init__(self, required_type: Optional[str] = None):
        self.required_type = required_type

    def filter(self, molecules: List[DataMolecule], query: Optional[Any] = None) -> List[DataMolecule]:
        target_entities = []
        if query is not None:
            if hasattr(query, 'entities') and query.entities:
                target_entities = query.entities
            elif isinstance(query, dict) and 'entities' in query:
                target_entities = query['entities']

        if self.required_type:
            return [m for m in molecules if m.type == self.required_type or m.molecule_type == self.required_type or m.name == self.required_type]
        elif target_entities:
            return [m for m in molecules if m.name in target_entities or m.id in target_entities or m.type in target_entities]

        return molecules

class FilterPipeline:
    def __init__(self, filters: Optional[List[Any]] = None):
        self.filters = filters if filters is not None else []

    def add_filter(self, filter_obj):
        self.filters.append(filter_obj)

    def apply(self, molecules: List[DataMolecule], query: Optional[Any] = None) -> List[DataMolecule]:
        current = list(molecules)
        for f in self.filters:
            if hasattr(f, 'filter'):
                try:
                    current = f.filter(current, query=query)
                except TypeError:
                    current = f.filter(current)
        return current
