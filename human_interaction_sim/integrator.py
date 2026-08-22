import numpy as np
from typing import Tuple, Callable

class Integrator:
    """Base class for numerical integration methods."""
    def step(
        self,
        position: np.ndarray,
        velocity: np.ndarray,
        accel_fn: Callable[[np.ndarray, np.ndarray, float], np.ndarray],
        t: float,
        dt: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError

class ExplicitEulerIntegrator(Integrator):
    """
    Explicit Euler numerical integration method.
    v(t + dt) = v(t) + a(t) * dt
    x(t + dt) = x(t) + v(t) * dt
    """
    def step(
        self,
        position: np.ndarray,
        velocity: np.ndarray,
        accel_fn: Callable[[np.ndarray, np.ndarray, float], np.ndarray],
        t: float,
        dt: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        acceleration = accel_fn(position, velocity, t)
        new_velocity = velocity + acceleration * dt
        new_position = position + velocity * dt  # or new_velocity * dt
        return new_position, new_velocity
