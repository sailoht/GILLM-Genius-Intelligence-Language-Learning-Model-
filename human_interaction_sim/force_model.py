import numpy as np
from dataclasses import dataclass
from typing import Tuple

@dataclass
class DecayingForce:
    """
    Represents a one-time initial interaction force produced by a user prompt.
    F(t) = F0 * exp(-lambda * (t - t0))
    This force naturally decays over time and is initialized once per prompt.
    """
    f0: float  # Initial force magnitude
    lambda_decay: float  # Decay coefficient
    t0: float  # Start time of force application
    direction: np.ndarray  # 2D direction unit vector

    def get_force(self, t: float) -> np.ndarray:
        if t < self.t0:
            return np.zeros(2)
        dt = t - self.t0
        magnitude = self.f0 * np.exp(-self.lambda_decay * dt)
        return magnitude * self.direction
