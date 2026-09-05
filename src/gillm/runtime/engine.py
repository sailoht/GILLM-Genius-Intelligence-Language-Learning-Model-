from typing import Dict, Any, Tuple
from src.gillm.gir.model import GIR
from src.gillm.query.molecule import QueryMolecule
from src.gillm.registry.registry import InformationRegistry3D
from src.gillm.laws.model import LawRegistry
from src.gillm.investigation.loop import InvestigationEngine
from src.gillm.langbaby.parser.structural_parser import LangBabyStructuralParser
from src.gillm.langbaby.realization.structural_realizer import LangBabyStructuralRealizer
from src.gillm.molecules.atom import DataAtom
from src.gillm.core.enums import EpistemicStatus, ValidationStatus

class GILLMRuntimeEngine:
    """
    The End-to-End GILLM Runtime Engine.
    Executes the complete vertical slice:
    Human Question -> LangBaby -> GIR -> Query Molecule -> Registry -> Investigation -> Synthesis -> Validation -> GIR -> LangBaby Realizer -> Answer.
    """
    def __init__(self) -> None:
        self.parser = LangBabyStructuralParser()
        self.realizer = LangBabyStructuralRealizer()
        self.registry = InformationRegistry3D()
        self.law_registry = LawRegistry()
        self.investigator = InvestigationEngine(self.registry, self.law_registry)

    def execute_end_to_end(self, user_question: str, mass_kg: float = 5.0, force_n: float = 10.0) -> Dict[str, Any]:
        # 1. Human -> LangBaby Structural Parser -> GIR
        gir_in = self.parser.parse_text_to_gir(user_question)

        # 2. GIR -> Query Molecule
        query_mol = QueryMolecule(
            intent=gir_in.intent,
            entities=[e["name"] for e in gir_in.entities],
            domain="physics"
        )

        # 3. Query Molecule -> 3D Registry Search & Investigation Loop
        inv_result = self.investigator.investigate_force_acceleration_question(
            query=query_mol,
            mass_kg=mass_kg,
            force_n=force_n
        )

        # 4. Synthesized Result -> GIR Out
        synth_mol = inv_result["synthesized_molecule"]
        accel_atom = list(synth_mol["data_atoms"].values())[0]

        gir_out = GIR(
            id=f"gir_resp_{gir_in.id}",
            intent="ANSWER",
            observations=[{
                "quantity": "acceleration",
                "value": accel_atom["value"],
                "unit": accel_atom["unit"]
            }],
            epistemic_status=EpistemicStatus.DERIVED,
            validation_status=ValidationStatus.VALID if inv_result["validation_passed"] else ValidationStatus.INVALID
        )

        # 5. GIR Out -> LangBaby Realizer -> Human Answer
        final_answer = self.realizer.realize_gir_to_text(gir_out)

        return {
            "user_question": user_question,
            "input_gir": gir_in.to_dict(),
            "query_molecule": {
                "intent": query_mol.intent,
                "entities": query_mol.entities,
                "domain": query_mol.domain
            },
            "investigation_stages": inv_result["investigation_stages"],
            "validation_passed": inv_result["validation_passed"],
            "output_gir": gir_out.to_dict(),
            "final_answer": final_answer
        }
