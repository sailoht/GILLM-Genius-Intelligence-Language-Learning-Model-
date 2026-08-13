from typing import Dict, Any, Optional
from gillm.gsl.phaser import GSLPhaser
from gillm.gsl.gcpr.models import GCPR

class CognitiveEngine:
    """Abstract interface defining the cognitive capabilities of JARVIS."""
    def understand(self, text: str, context: Optional[Any] = None) -> Dict[str, Any]:
        raise NotImplementedError

class GILLMEngine(CognitiveEngine):
    """GILLM-only cognitive engine utilizing the deterministic GSL 1.1 phrasing library."""
    def __init__(self) -> None:
        self.phaser = GSLPhaser()

    def understand(self, text: str, context: Optional[Any] = None) -> Dict[str, Any]:
        gcpr, trace = self.phaser.phase(text, context)
        # Returns the rich, trace-documented GCPR 0.5 representation
        return gcpr.to_dict()

class LLMEngine(CognitiveEngine):
    """Conventional LLM-centered cognitive engine (Mock interface representing Ollama/Cloud models)."""
    def understand(self, text: str, context: Optional[Any] = None) -> Dict[str, Any]:
        # Represents an LLM response parsed into standard intents
        text_lower = text.lower().strip()
        intent = "STATEMENT"
        if "?" in text or any(text_lower.startswith(w) for w in ["who", "what", "where", "why", "did", "is"]):
            intent = "QUESTION"

        return {
            "surface": {
                "original_text": text,
                "tokens": []
            },
            "linguistic": {
                "sentence_type": "question" if intent == "QUESTION" else "statement",
                "morphology": {},
                "grammar": {},
                "syntax": {}
            },
            "semantic": {
                "roles": {"action": "open" if "open" in text_lower else "unknown"},
                "entities": {},
                "relations": []
            },
            "conversation": {
                "role": None,
                "question_family": "WHAT" if "what" in text_lower else "YES_NO",
                "expected_answer": "BOOLEAN" if "did" in text_lower else "ENTITY"
            },
            "intent": intent,
            "uncertainty": {
                "ambiguous": False,
                "alternatives": [],
                "confidence": 0.95
            },
            "gsl_version": "1.1",
            "gcpr_version": "0.5",
            "gillm_version": "0.5.0",
            "engine": "LLM_MOCK"
        }

class HybridEngine(CognitiveEngine):
    """
    Hybrid cognitive engine:
    Uses GILLM for precise structural, grammatical, and syntactic validation,
    and delegates open-ended, complex generative reasoning to LLM.
    """
    def __init__(self) -> None:
        self.gillm = GILLMEngine()
        self.llm = LLMEngine()

    def understand(self, text: str, context: Optional[Any] = None) -> Dict[str, Any]:
        gillm_gcpr = self.gillm.understand(text, context)

        # Route to LLM if GILLM cannot safely resolve the sentence (confidence 0.0)
        # or if the intent requires deep generative reasoning
        if gillm_gcpr.get("uncertainty", {}).get("confidence", 1.0) == 0.0:
            llm_gcpr = self.llm.understand(text, context)
            llm_gcpr["engine_route"] = "DELEGATED_TO_LLM_DUE_TO_GILLM_UNKNOWN"
            return llm_gcpr

        gillm_gcpr["engine_route"] = "GILLM_DETERMINISTIC_PATH"
        return gillm_gcpr
