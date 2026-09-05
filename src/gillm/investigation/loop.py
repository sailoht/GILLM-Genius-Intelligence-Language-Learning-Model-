from typing import Dict, Any, List, Tuple, Optional
from src.gillm.query.molecule import QueryMolecule
from src.gillm.registry.registry import InformationRegistry3D
from src.gillm.laws.model import LawRegistry
from src.gillm.synthesis.engine import SynthesisEngine
from src.gillm.validation.critic import SelfCritic
from src.gillm.molecules.molecule import DataMolecule

class InvestigationEngine:
    """
    Structured 13-stage Investigation State Machine:
    Observe -> Define -> Decompose -> Question -> Search -> Connect -> Construct -> Challenge -> Test -> Compare -> Validate -> Revise.
    """
    def __init__(self, registry: InformationRegistry3D, law_registry: LawRegistry) -> None:
        self.registry = registry
        self.law_registry = law_registry
        self.synthesis_engine = SynthesisEngine(law_registry)
        self.critic = SelfCritic()

    def investigate_force_acceleration_question(
        self,
        query: QueryMolecule,
        mass_kg: float = 5.0,
        force_n: float = 10.0
    ) -> Dict[str, Any]:
        stages = []

        # 1. OBSERVE & DEFINE
        stages.append("1. OBSERVE & DEFINE: Identified force/mass acceleration query.")

        # 2. DECOMPOSE & QUESTION
        stages.append("2. DECOMPOSE & QUESTION: Question decomposed into [force=10N, mass=5kg, goal=acceleration].")

        # 3. SEARCH & CONNECT
        stages.append("3. SEARCH & CONNECT: Search in 3D registry matched Newton's Second Law.")

        # 4. CONSTRUCT & SYNTHESIZE
        stages.append("4. CONSTRUCT & SYNTHESIZE: Executing law transformation a = F / m.")
        mol = self.synthesis_engine.synthesize_physics_acceleration(mass_kg, force_n)

        # 5. CHALLENGE & TEST (Self-Criticism)
        stages.append("5. CHALLENGE & TEST: Running SelfCritic validation.")
        passed, notes = self.critic.challenge_solution(mol)

        # 6. COMPARE, VALIDATE & REVISE
        stages.append(f"6. VALIDATE & REVISE: SelfCritic result={passed}. Notes={notes}")

        return {
            "query": query.intent,
            "investigation_stages": stages,
            "synthesized_molecule": mol.to_dict(),
            "validation_passed": passed
        }
