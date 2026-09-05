import time
from typing import Dict, Any, List, Tuple
from src.gillm.core.enums import EpistemicStatus, ValidationStatus
from src.gillm.molecules.atom import DataAtom
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.laws.model import LawRegistry
from src.gillm.provenance.model import ProvenanceRecord

class SynthesisEngine:
    """
    Data Synthesis Engine:
    Synthesizes new DataMolecules from inputs and executable laws,
    tagging the output as SYNTHESIZED or DERIVED with full derivation provenance.
    """
    def __init__(self, law_registry: LawRegistry) -> None:
        self.law_registry = law_registry

    def synthesize_physics_acceleration(self, mass_kg: float, force_n: float) -> DataMolecule:
        law = self.law_registry.get_law("NewtonsSecondLaw")
        if not law:
            raise ValueError("Newton's Second Law not registered.")

        m_atom = DataAtom(id="m_in", type="measurement", value=mass_kg, unit="kg")
        f_atom = DataAtom(id="f_in", type="measurement", value=force_n, unit="N")

        atoms = {"mass": m_atom, "force": f_atom}
        accel_atom, dim_valid = law.transformation_fn(atoms)

        prov = ProvenanceRecord(
            source="SYNTHESIS_ENGINE",
            transformation="a = F / m",
            rule_used=law.name,
            inputs_used=["m_in", "f_in"]
        )

        mol = DataMolecule(
            id=f"mol_synth_{int(time.time()*1000)}",
            name="DerivedAccelerationState",
            epistemic_status=EpistemicStatus.DERIVED if dim_valid else EpistemicStatus.INVALID,
            validation_status=ValidationStatus.VALID if dim_valid else ValidationStatus.INVALID,
            laws=[law.name],
            provenance=prov
        )
        mol.add_atom(accel_atom)
        return mol
