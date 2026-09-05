from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class TemporalState:
    timestamp: float
    state_id: str
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StateTransition:
    from_state: TemporalState
    action: str
    to_state: TemporalState
    duration: float = 0.0

class TemporalEngine:
    """
    Manages time-varying state transitions: Action(State_t) -> State_{t+1}
    """
    def __init__(self):
        self.history: List[TemporalState] = []
        self.transitions: List[StateTransition] = []

    def record_transition(self, from_state: TemporalState, action: str, to_state: TemporalState) -> StateTransition:
        trans = StateTransition(from_state=from_state, action=action, to_state=to_state)
        self.transitions.append(trans)
        self.history.append(to_state)
        return trans
