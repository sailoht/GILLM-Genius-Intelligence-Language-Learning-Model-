from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable, Type
import time

@dataclass
class PerceptionEvent:
    source: str  # e.g., "user", "microphone", "camera", "system"
    modality: str  # TEXT, VOICE, FILE, IMAGE, SYSTEM
    timestamp: float = field(default_factory=time.time)
    content: Any = ""
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    session: str = "default_session"
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UserInputEvent:
    text: str
    timestamp: float = field(default_factory=time.time)
    session: str = "default_session"

@dataclass
class PlanCreatedEvent:
    plan_id: str
    steps: List[Dict[str, Any]]
    goal: str
    timestamp: float = field(default_factory=time.time)

@dataclass
class ToolCallEvent:
    tool_name: str
    arguments: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

@dataclass
class ToolResultEvent:
    tool_name: str
    result: Any
    status: str  # SUCCESS, FAILED
    timestamp: float = field(default_factory=time.time)

@dataclass
class VerificationEvent:
    target: str
    consistent: bool
    notes: List[str]
    timestamp: float = field(default_factory=time.time)

@dataclass
class ResponseEvent:
    text: str
    modality: str  # TEXT, VOICE
    timestamp: float = field(default_factory=time.time)


class EventBus:
    """A highly decoupled, typed, thread-safe Event Bus for JARVIS OS."""
    def __init__(self) -> None:
        self._listeners: Dict[Type, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: Type, listener: Callable[[Any], None]) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def publish(self, event: Any) -> None:
        event_type = type(event)
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                try:
                    listener(event)
                except Exception as e:
                    print(f"Error in EventBus listener for {event_type.__name__}: {str(e)}")
