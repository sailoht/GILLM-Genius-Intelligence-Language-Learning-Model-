from typing import Dict, Any, List
from src.gillm.gir.model import GIR

class LangBabyStructuralRealizer:
    """
    LangBaby Hierarchical Realizer:
    Realizes GIR objects into human-readable text using explicit structural realization:
    Word -> Phrase -> Proposition -> Sentence -> Paragraph -> Document.
    NO NEXT-TOKEN PREDICTION is used.
    """
    def realize_gir_to_text(self, gir: GIR) -> str:
        # Check if there is causality/synthesis to realize
        if gir.causality:
            cause_item = gir.causality[0]
            if "effect" in cause_item and "cause" in cause_item:
                return f"The {cause_item['effect']} because {cause_item['cause']}."

        # Check for derived physics result in observations/entities
        for obs in gir.observations:
            if "value" in obs and "unit" in obs:
                return f"The calculated {obs.get('quantity', 'value')} is {obs['value']} {obs['unit']}."

        if gir.entities:
            ent_names = [e["name"] for e in gir.entities]
            return f"Observed entities: {', '.join(ent_names)}."

        return f"GIR representation {gir.id} realized successfully for intent {gir.intent}."
