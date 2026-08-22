import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class InteractionState:
    """
    Represents the simulated interaction/semantic state in 2D space:
    x = topic position
    y = conceptual direction
    """
    position: np.ndarray = field(default_factory=lambda: np.zeros(2))
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(2))
    acceleration: np.ndarray = field(default_factory=lambda: np.zeros(2))
    mass: float = 1.0
    current_topic: str = "general"
    history: List[Dict[str, Any]] = field(default_factory=list)

    def update(self, pos: np.ndarray, vel: np.ndarray, accel: np.ndarray) -> None:
        self.position = pos
        self.velocity = vel
        self.acceleration = accel

    def speed(self) -> float:
        return float(np.linalg.norm(self.velocity))
