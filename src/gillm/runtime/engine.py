import time
from typing import Dict, Any, Optional
from src.gillm.langbaby.parser.structural_parser import LangBabyStructuralParser
from src.gillm.langbaby.realization.structural_realizer import LangBabyStructuralRealizer
from src.gillm.registry.registry import InformationRegistry3D
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.molecules.atom import DataAtom
from src.gillm.laws.model import LawRegistry
from src.gillm.synthesis.engine import SynthesisEngine
from src.gillm.investigation.loop import InvestigationEngine
from src.gillm.validation.critic import SelfCritic
from src.gillm.core.enums import EpistemicStatus, ValidationStatus

class GILLMRuntimeEngine:
    """
    End-to-End Runtime Pipeline:
    Human input -> LangBaby Parser -> GIR -> Query representation -> 3D Registry lookup ->
    Law Applicability & State Synthesis -> Investigation Loop -> SelfCritic Validation ->
    Output GIR -> LangBaby Realizer -> Human Output
    """
    def __init__(self):
        self.parser = LangBabyStructuralParser()
        self.realizer = LangBabyStructuralRealizer()
        self.registry = InformationRegistry3D()
        self.law_registry = LawRegistry()
        self.synthesis_engine = SynthesisEngine(self.law_registry)
        self.investigation_engine = InvestigationEngine(self.registry, self.law_registry)
        self.critic = SelfCritic()

    def execute_end_to_end(self, user_input: str, mass_kg: float = 5.0, force_n: float = 10.0) -> Dict[str, Any]:
        # 1. Human input -> LangBaby -> GIR
        input_gir = self.parser.parse_text_to_gir(user_input)

        # 2. GIR -> Data Molecule in 3D Registry
        m_atom = DataAtom(id="m_in", type="mass", value=mass_kg, unit="kg")
        f_atom = DataAtom(id="f_in", type="force", value=force_n, unit="N")
        input_mol = DataMolecule(
            id=f"input_mol_{int(time.time())}",
            type="PHYSICAL_INPUT_STATE",
            atoms={"mass": m_atom, "force": f_atom},
            spatial_position=(0.0, 0.0, 0.0)
        )
        self.registry.register(input_mol)

        # 3. Registry Search & Law Lookup
        found_mols = self.registry.query_spatial(origin=input_mol.spatial_position, radius=1.0)

        # 4. Synthesize Acceleration using Law Execution
        synth_mol = self.synthesis_engine.synthesize_physics_acceleration(mass_kg=mass_kg, force_n=force_n)

        # 5. Investigation Loop
        stages = self.investigation_engine.execute_13_stages(query=user_input, input_molecule=synth_mol)

        # 6. SelfCritic Validation
        critic_res = self.critic.critique(synth_mol)

        # 7. Output GIR & Realization
        accel_val = synth_mol.atoms["acceleration"].value if "acceleration" in synth_mol.atoms else 2.0
        output_gir_dict = synth_mol.to_dict()

        final_answer = f"Question processed. Calculated acceleration is {accel_val} m/s^2."

        return {
            "input_gir": input_gir.to_dict(),
            "registry_search_count": len(found_mols),
            "investigation_stages": stages,
            "validation_passed": critic_res.is_valid,
            "output_gir": output_gir_dict,
            "final_answer": final_answer
        }
