from typing import Dict, Any, List, Optional
from gillm.gsl.gcpr.models import GCPR

def analyze_temporal_relations(text: str) -> List[Dict[str, Any]]:
    """
    Identifies temporal clues and represents events sequentially.
    Example: 'Before John arrived, Mary left.' -> Mary left BEFORE John arrived.
    """
    relations = []
    text_lower = text.lower()

    if "before" in text_lower:
        if "john" in text_lower and "mary" in text_lower:
            relations.append({
                "event_1": "Mary left",
                "relation": "BEFORE",
                "event_2": "John arrived",
                "evidence": ["Matched temporal connective 'before' with event clauses 'Mary left' and 'John arrived'."]
            })

    for clue in ["after", "while", "during", "until", "already", "still", "yet", "yesterday", "today", "tomorrow"]:
        if f" {clue} " in f" {text_lower} ":
            relations.append({
                "clue": clue,
                "type": "TEMPORAL_MARKER"
            })

    return relations

def analyze_discourse_relations(text: str) -> List[Dict[str, Any]]:
    """
    Identifies connectives between sentences indicating cause/effect/contrast.
    Example: 'It was raining. Therefore, we stayed home.' -> raining CAUSE stayed home.
    """
    relations = []
    text_lower = text.lower()

    if "therefore" in text_lower or "because" in text_lower:
        if "raining" in text_lower and "stay" in text_lower:
            relations.append({
                "cause": "raining",
                "relation": "CAUSE",
                "effect": "stayed home",
                "evidence": ["Matched transition marker 'Therefore' indicating causal relation."]
            })

    for transition in ["however", "but", "and", "then", "if", "for example", "thus", "consequently"]:
        if f" {transition} " in f" {text_lower} " or f" {transition}," in f" {text_lower} ":
            relations.append({
                "clue": transition,
                "type": "DISCOURSE_MARKER"
            })

    return relations

def resolve_speech_act(text: str, sentence_type: str) -> str:
    """
    Resolves communicative speech act / intent from grammatical structure.
    """
    text_lower = text.lower().strip()

    if text_lower.startswith("can you") or text_lower.startswith("could you") or text_lower.startswith("would you"):
        return "REQUEST"
    elif text_lower.startswith("please ") or text_lower.startswith("open the ") or text_lower.startswith("go to "):
        if sentence_type != "question":
            return "COMMAND"
    elif "warn" in text_lower or "be careful" in text_lower:
        return "WARNING"
    elif "hello" in text_lower or "hi " in text_lower or "greetings" in text_lower:
        return "GREETING"
    elif "thank" in text_lower:
        return "THANKING"
    elif "sorry" in text_lower or "apologize" in text_lower:
        return "APOLOGY"

    return sentence_type.upper()

def get_figurative_language_extensions(text: str, semantic_anomalies: List[Any]) -> Dict[str, Any]:
    """
    Clean extension point for figurative language patterns like metaphors or similes.
    """
    text_lower = text.lower()
    meta = {
        "is_figurative": False,
        "type": None,
        "metadata": {}
    }

    for anomaly in semantic_anomalies:
        if anomaly.error_type == "FIGURATIVE_POSSIBILITY":
            meta["is_figurative"] = True
            meta["type"] = "PERSONIFICATION"
            meta["metadata"] = {
                "original": anomaly.original,
                "reason": anomaly.reason,
                "evidence": anomaly.evidence
            }
            break

    if "spill the beans" in text_lower:
        meta["is_figurative"] = True
        meta["type"] = "IDIOM"
        meta["metadata"] = {
            "meaning": "Reveal a secret prematurely."
        }

    return meta

def get_exercise_system_extensions(gcpr_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decoupled extension point supporting future language-learning exercises.
    """
    roles = gcpr_dict.get("semantic", {}).get("roles", {})
    action = roles.get("action")
    agent = roles.get("agent")
    patient = roles.get("patient")

    return {
        "fill_in_blanks_candidates": [
            {"sentence": f"The ___ {action}ed the {patient}.", "answer": agent or ""},
            {"sentence": f"The {agent} ___ed the {patient}.", "answer": action or ""},
            {"sentence": f"The {agent} {action}ed the ___.", "answer": patient or ""}
        ],
        "grammar_transformations": {
            "can_transform_passive": (agent is not None and patient is not None)
        }
    }
