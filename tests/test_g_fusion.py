from src.gillm.molecules.atom import DataAtom
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.synthesis.fusion_fission import FusionEngine
from src.gillm.core.enums import EpistemicStatus

def test_g_fusion():
    """
    Test G — fusion:
    Construct a valid new scenario from two compatible scenarios.
    """
    atom_a = DataAtom("a1", "MASS", 5.0, "kg")
    atom_b = DataAtom("b1", "FORCE", 10.0, "N")

    scen_a = DataMolecule("scen_a", "SCENARIO_A", atoms={"mass": atom_a})
    scen_b = DataMolecule("scen_b", "SCENARIO_B", atoms={"force": atom_b})

    fusion_engine = FusionEngine()
    fused_molecule = fusion_engine.fuse(scen_a, scen_b)

    assert fused_molecule.molecule_type == "FUSED_SCENARIO"
    assert "mass" in fused_molecule.atoms
    assert "force" in fused_molecule.atoms
    assert fused_molecule.epistemic_status == EpistemicStatus.SYNTHESIZED
