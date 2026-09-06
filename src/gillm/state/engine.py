from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from src.gillm.sets.model import InformationSet
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.laws.model import LawRegistry, ExecutableLaw
from src.gillm.time.model import TemporalState, StateTransition
from src.gillm.provenance.model import ProvenanceRecord
from src.gillm.validation.critic import SelfCritic, SelfCriticResult

@dataclass
class StateTransitionResult:
    initial_set: InformationSet
    resulting_set: InformationSet
    transitions: List[StateTransition]
    critic_results: List[SelfCriticResult]

class StateTransitionEngine:
    """
    General state-transition engine implementing the target abstraction:
    S_(t+1) = T(S_t, Law, Context)

    Operates over sets of objects with vector/atom states, applies matching laws,
    records state transitions and provenance, and validates resulting states.
    """
    def __init__(self, law_registry: Optional[LawRegistry] = None):
        self.law_registry = law_registry or LawRegistry()
        self.critic = SelfCritic()

    def step_set(self, object_set: InformationSet, context: Optional[Dict[str, Any]] = None) -> StateTransitionResult:
        new_set = InformationSet(name=f"{object_set.name}_t+1")
        transitions: List[StateTransition] = []
        critic_results: List[SelfCriticResult] = []

        for obj in object_set:
            if isinstance(obj, DataMolecule):
                applicable_laws = self.law_registry.find_applicable_laws(obj)
                current_mol = obj

                for law in applicable_laws:
                    transformed = law.transformation(current_mol)
                    if isinstance(transformed, DataMolecule):
                        # Record state transition history
                        t0 = TemporalState(timestamp=obj.state.get("t", 0.0), state_id=obj.id, properties=obj.to_dict())
                        t1 = TemporalState(timestamp=transformed.state.get("t", 1.0), state_id=transformed.id, properties=transformed.to_dict())

                        trans = StateTransition(from_state=t0, action=law.name, to_state=t1)
                        transitions.append(trans)
                        current_mol = transformed

                critic_res = self.critic.critique(current_mol)
                critic_results.append(critic_res)
                new_set.add(current_mol)
            else:
                new_set.add(obj)

        return StateTransitionResult(
            initial_set=object_set,
            resulting_set=new_set,
            transitions=transitions,
            critic_results=critic_results
        )
