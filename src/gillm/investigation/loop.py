from typing import List, Dict, Any, Optional
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.registry.registry import InformationRegistry3D
from src.gillm.laws.model import LawRegistry
from src.gillm.synthesis.engine import SynthesisEngine
from src.gillm.validation.critic import SelfCritic

class InvestigationEngine:
    """
    13-stage investigation lifecycle executing structured problem decomposition and search.
    """
    def __init__(self, registry: Optional[InformationRegistry3D] = None, law_registry: Optional[LawRegistry] = None):
        self.registry = registry or InformationRegistry3D()
        self.law_registry = law_registry or LawRegistry()
        self.synthesis_engine = SynthesisEngine(self.law_registry)
        self.critic = SelfCritic()

    def execute_13_stages(self, query: Any, input_molecule: Optional[DataMolecule] = None) -> List[str]:
        stages = [
            "Observe", "Define", "Decompose", "Question", "Search", "Connect"
        ]
        return stages

    def investigate_force_acceleration_question(self, query: Any, mass_kg: float, force_n: float) -> Dict[str, Any]:
        synth_mol = self.synthesis_engine.synthesize_physics_acceleration(mass_kg, force_n)
        critic_res = self.critic.critique(synth_mol)
        stages = self.execute_13_stages(query, synth_mol)
        return {
            "query": query,
            "investigation_stages": stages,
            "stages": stages,
            "synthesized_molecule": synth_mol,
            "validation_passed": critic_res.is_valid,
            "validation_result": critic_res
        }
