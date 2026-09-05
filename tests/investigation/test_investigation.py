from src.gillm.registry.registry import InformationRegistry3D
from src.gillm.laws.model import LawRegistry
from src.gillm.query.molecule import QueryMolecule
from src.gillm.investigation.loop import InvestigationEngine

def test_investigation_loop_end_to_end():
    registry = InformationRegistry3D()
    law_registry = LawRegistry()
    investigator = InvestigationEngine(registry, law_registry)

    query = QueryMolecule(intent="EXPLAIN_ACCELERATION", entities=["object", "force"])

    result = investigator.investigate_force_acceleration_question(query, mass_kg=5.0, force_n=10.0)

    assert result["validation_passed"] is True
    assert len(result["investigation_stages"]) == 6

    mol_dict = result["synthesized_molecule"]
    assert mol_dict["name"] == "DerivedAccelerationState"
    data_atoms_list = list(mol_dict["data_atoms"].values())
    assert len(data_atoms_list) > 0
    assert data_atoms_list[0]["value"] == 2.0
    assert data_atoms_list[0]["unit"] == "m/s^2"
