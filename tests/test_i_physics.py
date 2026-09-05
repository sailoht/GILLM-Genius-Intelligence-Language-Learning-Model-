from src.gillm.laws.model import LawRegistry, ExecutableLaw
from src.gillm.molecules.atom import DataAtom
from src.gillm.molecules.molecule import DataMolecule

def test_i_physics():
    """
    Test I — physics:
    Perform the transparent F = ma derivation with units and provenance.
    """
    registry = LawRegistry()
    registry.register_default_laws()

    mass_atom = DataAtom("m1", "MASS", 5.0, "kg")
    force_atom = DataAtom("f1", "FORCE", 10.0, "N")

    input_mol = DataMolecule("obj_1", "PHYSICAL_STATE", atoms={"mass": mass_atom, "force": force_atom})

    derived_mol = registry.execute_applicable_laws(input_mol)

    assert derived_mol is not None
    assert "acceleration" in derived_mol.atoms
    acc_atom = derived_mol.atoms["acceleration"]
    assert acc_atom.value == 2.0
    assert acc_atom.unit == "m/s^2"
    assert derived_mol.provenance.transformation_type == "LAW_EXECUTION"
