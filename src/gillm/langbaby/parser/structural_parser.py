import re
from typing import Dict, Any, List
from src.gillm.gir.model import GIR
from src.gillm.core.enums import EpistemicStatus, ValidationStatus
from src.gillm.provenance.model import ProvenanceRecord

class LangBabyStructuralParser:
    """
    LangBaby Structural Parser:
    Converts human language text into a structured GIR representation.
    NO NEXT-TOKEN PREDICTION or LLM autocomplete is used.
    """
    def parse_text_to_gir(self, text: str) -> GIR:
        text_clean = text.strip()
        text_lower = text_clean.lower()

        gir_id = f"gir_{abs(hash(text_clean))}"
        intent = "STATEMENT"
        if text_clean.endswith("?") or any(text_lower.startswith(w) for w in ["who", "what", "where", "why", "how", "did", "is"]):
            intent = "QUESTION"

        entities = []
        concepts = []
        actions = []
        causality = []

        # Extract entities / nouns
        words = re.findall(r"\b[a-zA-Z]+\b", text_lower)
        known_entities = ["car", "boy", "dog", "door", "ball", "earth", "particle", "stone", "moon"]
        for w in words:
            if w in known_entities:
                entities.append({"name": w, "category": "ENTITY"})

        # Extract cause and effect structure (e.g. 'car accelerates because a net force acts on it')
        if "because" in text_lower or "due to" in text_lower or "acts on" in text_lower:
            parts = re.split(r"\bbecause\b|\bdue to\b", text_lower)
            if len(parts) == 2:
                causality.append({
                    "effect": parts[0].strip(),
                    "relation": "CAUSED_BY",
                    "cause": parts[1].strip()
                })
            else:
                causality.append({
                    "relation": "CAUSAL_ACTION",
                    "text": text_clean
                })

        prov = ProvenanceRecord(
            source="LANGBABY_PARSER",
            transformation="TEXT_TO_GIR",
            rule_used="LangBabyStructuralParserRules",
            inputs_used=[text_clean]
        )

        return GIR(
            id=gir_id,
            intent=intent,
            entities=entities,
            concepts=concepts,
            causality=causality,
            epistemic_status=EpistemicStatus.OBSERVED,
            validation_status=ValidationStatus.VALID,
            provenance=prov
        )
