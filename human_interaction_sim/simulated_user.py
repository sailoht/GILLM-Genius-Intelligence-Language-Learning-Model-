import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict, Any, Optional

@dataclass
class UserResponse:
    text: str
    response_type: str  # CONTINUE, DEEPEN, PARTIAL_CHANGE, COMPLETE_CHANGE, SHORT_ANSWER, NO_CONTINUATION
    force_magnitude: float
    direction: np.ndarray  # 2D direction vector
    topic: str

class SimulatedUser:
    """
    Simulates a human user producing one of several response types:
    1. CONTINUE (same direction, medium force)
    2. DEEPEN (same direction, strong force)
    3. PARTIAL_CHANGE (shifted direction vector)
    4. COMPLETE_CHANGE (abrupt direction vector, e.g. orthogonal)
    5. SHORT_ANSWER (same direction, small force)
    6. NO_CONTINUATION (zero force)
    """
    def __init__(self, base_f0: float = 10.0, seed: Optional[int] = 42) -> None:
        self.base_f0 = base_f0
        self.rng = np.random.default_rng(seed)

    def respond(
        self,
        question: str,
        current_topic: str,
        current_direction: np.ndarray,
        response_type: str = "CONTINUE",
        override_topic: Optional[str] = None
    ) -> UserResponse:
        current_direction = current_direction / np.linalg.norm(current_direction) if np.linalg.norm(current_direction) > 0 else np.array([1.0, 0.0])

        topic = override_topic or current_topic

        if response_type == "CONTINUE":
            text = f"Yes, let's continue discussing {topic}."
            mag = self.base_f0
            dir_vec = current_direction

        elif response_type == "DEEPEN":
            text = f"Let's dive deeper into the mathematics of {topic}."
            mag = self.base_f0 * 1.5
            dir_vec = current_direction

        elif response_type == "PARTIAL_CHANGE":
            text = f"How does {topic} relate to computer science?"
            mag = self.base_f0 * 0.9
            # Rotate direction by 45 degrees
            angle = np.pi / 4
            rot_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
            dir_vec = rot_matrix @ current_direction

        elif response_type == "COMPLETE_CHANGE":
            topic = override_topic or "machine learning"
            text = f"Let me change the topic completely to {topic}."
            mag = self.base_f0 * 1.2
            # Rotate direction by 120 degrees to redirect trajectory
            angle = 2 * np.pi / 3
            rot_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
            dir_vec = rot_matrix @ current_direction

        elif response_type == "SHORT_ANSWER":
            text = "Sure."
            mag = self.base_f0 * 0.3
            dir_vec = current_direction

        elif response_type == "NO_CONTINUATION":
            text = "I have no more questions."
            mag = 0.0
            dir_vec = current_direction

        else:
            text = "Okay."
            mag = self.base_f0
            dir_vec = current_direction

        dir_vec = dir_vec / np.linalg.norm(dir_vec) if np.linalg.norm(dir_vec) > 0 else np.array([1.0, 0.0])

        return UserResponse(
            text=text,
            response_type=response_type,
            force_magnitude=mag,
            direction=dir_vec,
            topic=topic
        )
