from dataclasses import dataclass
from enum import Enum, auto

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
