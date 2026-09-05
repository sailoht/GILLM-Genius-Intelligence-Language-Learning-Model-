import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from src.gillm.core.enums import EpistemicStatus, ValidationStatus
from src.gillm.provenance.model import ProvenanceRecord

@dataclass
class GIR:
    """
    Genius Intelligence Representation (GIR) -
    The common internal contract representation between LangBaby and GILLM Core.
    Fully serializable to/from JSON.
    """
    id: str = "gir_default"
    intent: str = "STATEMENT"
    entities: List[Dict[str, Any]] = field(default_factory=list)
    concepts: List[Dict[str, Any]] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    relations: List[Dict[str, Any]] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)
    observations: List[Dict[str, Any]] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    goals: List[Dict[str, Any]] = field(default_factory=list)
    spatial_info: Dict[str, Any] = field(default_factory=dict)
    temporal_info: Dict[str, Any] = field(default_factory=dict)
    causality: List[Dict[str, Any]] = field(default_factory=list)
    epistemic_status: EpistemicStatus = EpistemicStatus.OBSERVED
    validation_status: ValidationStatus = ValidationStatus.VALID
    provenance: ProvenanceRecord = field(default_factory=ProvenanceRecord)
    version: str = "0.1.0"
    ambiguity_flag: bool = False
    interpretations: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def gir_id(self) -> str:
        return self.id

    @gir_id.setter
    def gir_id(self, val: str):
        self.id = val

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "intent": self.intent,
            "entities": self.entities,
            "concepts": self.concepts,
            "properties": self.properties,
            "relations": self.relations,
            "events": self.events,
            "observations": self.observations,
            "actions": self.actions,
            "goals": self.goals,
            "spatial_info": self.spatial_info,
            "temporal_info": self.temporal_info,
            "causality": self.causality,
            "epistemic_status": self.epistemic_status.value if isinstance(self.epistemic_status, EpistemicStatus) else str(self.epistemic_status),
            "validation_status": self.validation_status.value if isinstance(self.validation_status, ValidationStatus) else str(self.validation_status),
            "provenance": self.provenance.to_dict() if hasattr(self.provenance, 'to_dict') else {},
            "ambiguity_flag": self.ambiguity_flag,
            "interpretations": self.interpretations
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GIR':
        prov_dict = data.get("provenance", {})
        prov = ProvenanceRecord(
            source=prov_dict.get("source", "UNKNOWN"),
            transformation=prov_dict.get("transformation", "NONE"),
            rule_used=prov_dict.get("rule_used", "NONE"),
            inputs_used=prov_dict.get("inputs_used", []),
            assumptions=prov_dict.get("assumptions", [])
        )
        return cls(
            id=data.get("id", data.get("gir_id", "gir_default")),
            version=data.get("version", "0.1.0"),
            intent=data.get("intent", "STATEMENT"),
            entities=data.get("entities", []),
            concepts=data.get("concepts", []),
            properties=data.get("properties", {}),
            relations=data.get("relations", []),
            events=data.get("events", []),
            observations=data.get("observations", []),
            actions=data.get("actions", []),
            goals=data.get("goals", []),
            spatial_info=data.get("spatial_info", {}),
            temporal_info=data.get("temporal_info", {}),
            causality=data.get("causality", []),
            epistemic_status=EpistemicStatus(data.get("epistemic_status", "OBSERVED")),
            validation_status=ValidationStatus(data.get("validation_status", "VALID")),
            provenance=prov,
            ambiguity_flag=data.get("ambiguity_flag", False),
            interpretations=data.get("interpretations", [])
        )

    @classmethod
    def from_json(cls, json_str: str) -> 'GIR':
        return cls.from_dict(json.loads(json_str))
