from src.gillm.core.enums import EpistemicStatus, ValidationStatus
from src.gillm.molecules.atom import DataAtom
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.gir.model import GIR

def test_data_atom_and_molecule():
    atom1 = DataAtom(id="atom_m", type="measurement", value=5.0, unit="kg")
    atom2 = DataAtom(id="atom_f", type="measurement", value=10.0, unit="N")

    mol = DataMolecule(id="mol_system", name="MechanicalSystem")
    mol.add_atom(atom1)
    mol.add_atom(atom2)

    assert len(mol.data_atoms) == 2
    assert mol.data_atoms["atom_m"].value == 5.0
    assert mol.data_atoms["atom_m"].unit == "kg"
    assert mol.epistemic_status == EpistemicStatus.OBSERVED

def test_gir_serialization():
    gir = GIR(id="gir_01", intent="QUESTION")
    gir.entities.append({"name": "Earth", "category": "PLANET"})

    json_str = gir.to_json()
    re_gir = GIR.from_json(json_str)

    assert re_gir.id == "gir_01"
    assert re_gir.intent == "QUESTION"
    assert re_gir.entities[0]["name"] == "Earth"
