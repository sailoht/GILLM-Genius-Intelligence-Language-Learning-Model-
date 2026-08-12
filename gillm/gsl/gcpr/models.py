from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class SurfaceRepresentation:
    original_text: str
    tokens: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class LinguisticRepresentation:
    sentence_type: str = "statement"  # statement, question, exclamation
    morphology: Dict[str, Any] = field(default_factory=dict)
    grammar: Dict[str, Any] = field(default_factory=dict)
    syntax: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SemanticRepresentation:
    roles: Dict[str, Any] = field(default_factory=dict)
    entities: Dict[str, Any] = field(default_factory=dict)
    relations: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ConversationRepresentation:
    role: Optional[str] = None
    question_family: Optional[str] = None
    expected_answer: Optional[str] = None

@dataclass
class UncertaintyRepresentation:
    ambiguous: bool = False
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    confidence: Optional[float] = 1.0

@dataclass
class GCPR:
    surface: SurfaceRepresentation
    linguistic: LinguisticRepresentation = field(default_factory=LinguisticRepresentation)
    semantic: SemanticRepresentation = field(default_factory=SemanticRepresentation)
    conversation: ConversationRepresentation = field(default_factory=ConversationRepresentation)
    intent: Optional[str] = None
    uncertainty: UncertaintyRepresentation = field(default_factory=UncertaintyRepresentation)
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Converts GCPR dataclass to serializable nested dictionary structure."""
        base = {
            "surface": {
                "original_text": self.surface.original_text,
                "tokens": self.surface.tokens
            },
            "linguistic": {
                "sentence_type": self.linguistic.sentence_type,
                "morphology": self.linguistic.morphology,
                "grammar": self.linguistic.grammar,
                "syntax": self.linguistic.syntax
            },
            "semantic": {
                "roles": self.semantic.roles,
                "entities": self.semantic.entities,
                "relations": self.semantic.relations
            },
            "conversation": {
                "role": self.conversation.role,
                "question_family": self.conversation.question_family,
                "expected_answer": self.conversation.expected_answer
            },
            "intent": self.intent,
            "uncertainty": {
                "ambiguous": self.uncertainty.ambiguous,
                "alternatives": self.uncertainty.alternatives,
                "confidence": self.uncertainty.confidence
            }
        }
        if self.extra_fields:
            base.update(self.extra_fields)
        return base
