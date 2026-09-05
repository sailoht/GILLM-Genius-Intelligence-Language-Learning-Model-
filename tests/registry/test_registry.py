from src.gillm.molecules.molecule import DataMolecule
from src.gillm.registry.registry import InformationRegistry3D
from src.gillm.query.molecule import QueryMolecule
from src.gillm.fields.gaussian import GaussianInformationField
from src.gillm.operators.filters import SpatialFilter, SemanticFilter, FilterPipeline

def test_3d_registry_and_spatial_search():
    registry = InformationRegistry3D()
    mol1 = DataMolecule(id="m1", name="Object_A", spatial_position=(0.0, 0.0, 0.0))
    mol2 = DataMolecule(id="m2", name="Object_B", spatial_position=(5.0, 0.0, 0.0))
    mol3 = DataMolecule(id="m3", name="Object_C", spatial_position=(50.0, 50.0, 50.0))

    registry.insert(mol1)
    registry.insert(mol2)
    registry.insert(mol3)

    results = registry.spatial_search(center=(0.0, 0.0, 0.0), radius=10.0)
    assert len(results) == 2
    assert set([m.id for m in results]) == {"m1", "m2"}

def test_gaussian_field_and_filter_pipeline():
    field1 = GaussianInformationField(center=(0.0, 0.0, 0.0), amplitude=1.0, sigma=2.0)
    val = field1.evaluate(0.0, 0.0, 0.0)
    assert val == 1.0

    query = QueryMolecule(entities=["Object_A"], spatial_requirements={"center": (0.0, 0.0, 0.0), "radius": 10.0})
    pipeline = FilterPipeline([SpatialFilter(), SemanticFilter()])

    mol1 = DataMolecule(id="m1", name="Object_A", spatial_position=(0.0, 0.0, 0.0))
    mol2 = DataMolecule(id="m2", name="Object_B", spatial_position=(0.0, 0.0, 0.0))

    filtered = pipeline.apply([mol1, mol2], query)
    assert len(filtered) == 1
    assert filtered[0].id == "m1"
