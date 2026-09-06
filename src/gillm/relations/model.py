from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict, Any, Optional

class RelationType(Enum):
    IS_A = auto()
    PART_OF = auto()
    HAS_PROPERTY = auto()
    LOCATED_AT = auto()
    DEPENDS_ON = auto()
    ENABLES = auto()
    PREVENTS = auto()
    INTERACTS_WITH = auto()
    BEFORE = auto()
    AFTER = auto()

@dataclass
class ExplicitRelation:
    source_id: str
    target_id: str
    relation_type: RelationType
    bidirectional: bool = False

class RelationGraph:
    """
    Stores and queries first-class relations between objects for reasoning and state transition engines.
    """
    def __init__(self):
        self.relations: List[ExplicitRelation] = []

    def add_relation(self, relation: ExplicitRelation):
        self.relations.append(relation)

    def get_relations_for_source(self, source_id: str) -> List[ExplicitRelation]:
        return [r for r in self.relations if r.source_id == source_id]

    def get_relations_by_type(self, rel_type: RelationType) -> List[ExplicitRelation]:
        return [r for r in self.relations if r.relation_type == rel_type]
