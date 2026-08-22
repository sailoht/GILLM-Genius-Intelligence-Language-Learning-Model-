import numpy as np

class FrictionModel:
    """
    Models natural friction continuously opposing the interaction's velocity.
    F_friction = c * v
    Friction is independent of user typing state and always opposes motion.
    """
    def __init__(self, damping_coefficient: float = 0.5) -> None:
        self.c = damping_coefficient

    def get_friction_force(self, velocity: np.ndarray) -> np.ndarray:
        return self.c * velocity
