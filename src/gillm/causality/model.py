from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class CausalRelation:
    cause_id: str
    effect_id: str
    relation_type: str = "DIRECT_CAUSE"  # DIRECT_CAUSE, ENABLING_CONDITION, PREVENTING_CONDITION
    counterfactual_state: Optional[Dict[str, Any]] = None
    confidence: float = 1.0

class CausalEngine:
    """
    Manages explicit causality separate from spatial proximity or vector similarity.
    Supports counterfactual state analysis.
    """
    def __init__(self):
        self.relations: List[CausalRelation] = []

    def add_causal_relation(self, relation: CausalRelation):
        self.relations.append(relation)

    def evaluate_counterfactual(self, cause_id: str, removed: bool) -> str:
        if removed:
            return f"If cause '{cause_id}' did not occur, effect would not manifest."
        return "Cause present; effect manifests."
