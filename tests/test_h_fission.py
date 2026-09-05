from src.gillm.molecules.atom import DataAtom
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.synthesis.fusion_fission import FissionEngine

def test_h_fission():
    """
    Test H — fission:
    Decompose a complex scenario into constituent structures.
    """
    atom_a = DataAtom("a1", "MASS", 5.0, "kg")
    atom_b = DataAtom("b1", "FORCE", 10.0, "N")

    complex_mol = DataMolecule("complex_1", "COMPLEX_SCENARIO", atoms={"mass": atom_a, "force": atom_b})

    fission_engine = FissionEngine()
    constituents = fission_engine.fission(complex_mol)

    assert len(constituents) == 2
    assert constituents[0].provenance.transformation_type == "FISSION"
    assert constituents[0].provenance.input_ids == ["complex_1"]
