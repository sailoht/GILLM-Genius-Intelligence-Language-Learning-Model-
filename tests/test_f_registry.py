from src.gillm.registry.registry import InformationRegistry3D
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.space.coordinates import SpatialCoordinate
from src.gillm.operators.filters import FilterPipeline, SpatialFilter, SemanticFilter

def test_f_registry():
    """
    Test F — registry:
    Insert molecules and retrieve/filter them through the 3D information registry.
    """
    registry = InformationRegistry3D()
    mol1 = DataMolecule("m1", "PHYSICAL", spatial_position=SpatialCoordinate(0, 0, 0))
    mol2 = DataMolecule("m2", "PHYSICAL", spatial_position=SpatialCoordinate(100, 100, 100))

    registry.register_molecule(mol1)
    registry.register_molecule(mol2)

    results = registry.query_radius(SpatialCoordinate(0, 0, 0), radius=10.0)
    assert len(results) == 1
    assert results[0].molecule_id == "m1"

    pipeline = FilterPipeline()
    pipeline.add_filter(SpatialFilter(center=SpatialCoordinate(0, 0, 0), radius=10.0))
    pipeline.add_filter(SemanticFilter(required_type="PHYSICAL"))

    filtered = pipeline.apply([mol1, mol2])
    assert len(filtered) == 1
    assert filtered[0].molecule_id == "m1"
