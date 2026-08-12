from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ConversationTurn:
    user_text: str
    gcpr_data: Dict[str, Any]

class ConversationContext:
    def __init__(self) -> None:
        self.turns: List[ConversationTurn] = []
        self.entities: List[str] = []
        self.active_topic: Optional[str] = None
        self.references: Dict[str, str] = {}

    def add_turn(self, user_text: str, gcpr_data: Dict[str, Any]) -> None:
        turn = ConversationTurn(user_text=user_text, gcpr_data=gcpr_data)
        self.turns.append(turn)

        # Extract and register entities
        roles = gcpr_data.get("semantic", {}).get("roles", {})
        for role, concept in roles.items():
            if concept and concept not in ["unknown", "action"]:
                if concept not in self.entities:
                    self.entities.append(concept)
                    # Simple heuristic: active topic is the last mentioned entity that isn't a simple pronoun
                    if concept.lower() not in ["it", "who", "what", "where", "why", "i", "he", "she", "her"]:
                        self.active_topic = concept

    def resolve_coreferences(self, gcpr_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scans GCPR for pronouns like 'it' and links them to the active topic of conversation.
        """
        roles = gcpr_data.get("semantic", {}).get("roles", {})
        entities = gcpr_data.get("semantic", {}).get("entities", {})

        has_it = False
        for role, val in roles.items():
            if val and val.lower() == "it":
                has_it = True
                break

        if has_it and self.active_topic:
            # Attach a coreference link in the GCPR structure
            entities["it"] = {
                "coreference": self.active_topic,
                "confidence": 1.0,
                "evidence": [f"Linked pronoun 'it' to active topic '{self.active_topic}' from conversation history"]
            }
            # Also keep track in references dict
            self.references["it"] = self.active_topic

        return gcpr_data
