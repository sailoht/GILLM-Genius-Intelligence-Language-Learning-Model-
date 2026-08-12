from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class SearchKey:
    concept: str
    intent: str

def generate_search_key(gcpr_data: Dict[str, Any]) -> Optional[SearchKey]:
    """
    Generates a SearchKey from a GCPR dict.
    Example: SearchKey(concept="quantum tunneling", intent="definition")
    """
    linguistic = gcpr_data.get("linguistic", {})
    semantic = gcpr_data.get("semantic", {})
    conv = gcpr_data.get("conversation", {})

    sentence_type = linguistic.get("sentence_type")
    roles = semantic.get("roles", {})

    # Simple logic to determine main concept
    # Prioritize non-pronoun noun phrases from the roles (e.g. quantum tunneling, door, food)
    concept = "unknown"
    for role in ["identity", "patient", "subject", "agent"]:
        val = roles.get(role)
        if val and val not in ["unknown", "it", "who", "what", "why", "where"]:
            concept = val
            break

    # Resolve 'it' coreference if present
    entities = semantic.get("entities", {})
    if concept == "unknown" and "it" in entities:
        concept = entities["it"].get("coreference", "unknown")

    # Determine intent
    intent = "statement"
    if sentence_type == "question":
        q_family = conv.get("question_family")
        if q_family == "WHAT":
            intent = "definition"
        elif q_family == "WHY":
            intent = "cause"
        elif q_family == "WHERE":
            intent = "location"
        elif q_family == "WHO":
            intent = "person"
        elif q_family == "YES_NO":
            intent = "confirmation"

    return SearchKey(concept=concept, intent=intent)
