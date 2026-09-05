from src.gillm.molecules.atom import DataAtom
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.laws.model import LawRegistry
from src.gillm.core.enums import EpistemicStatus, ValidationStatus

def test_newtons_second_law_execution():
    registry = LawRegistry()
    law = registry.get_law("NewtonsSecondLaw")
    assert law is not None

    # Input atoms: mass = 5 kg, force = 10 N
    mass_atom = DataAtom(id="m1", type="measurement", value=5.0, unit="kg")
    force_atom = DataAtom(id="f1", type="measurement", value=10.0, unit="N")

    atoms = {"mass": mass_atom, "force": force_atom}
    accel_atom, dim_valid = law.transformation_fn(atoms)

    # Assert values
    assert accel_atom.value == 2.0
    assert accel_atom.unit == "m/s^2"
    assert dim_valid is True

    # Assert provenance
    assert accel_atom.provenance.rule_used == "Newton's Second Law (F = m*a)"
    assert accel_atom.provenance.inputs_used == ["f1", "m1"]
