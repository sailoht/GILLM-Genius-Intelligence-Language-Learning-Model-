import numpy as np
import time
from typing import Dict, Any, List, Optional, Tuple
from human_interaction_sim.force_model import DecayingForce
from human_interaction_sim.friction import FrictionModel
from human_interaction_sim.integrator import ExplicitEulerIntegrator
from human_interaction_sim.interaction_state import InteractionState

class SimulationEngine:
    """
    Simulates conversational interaction dynamics following a physics-inspired model:
    F_net(t) = F_applied(t) - F_friction(v)
    a(t) = F_net(t) / m
    """
    def __init__(
        self,
        mass: float = 1.0,
        f0: float = 10.0,
        lambda_decay: float = 0.5,
        c_friction: float = 0.5,
        epsilon: float = 0.1,
        persistence_steps: int = 5,
        dt: float = 0.1
    ) -> None:
        self.mass = mass
        self.f0 = f0
        self.lambda_decay = lambda_decay
        self.friction_model = FrictionModel(damping_coefficient=c_friction)
        self.integrator = ExplicitEulerIntegrator()
        self.epsilon = epsilon
        self.persistence_steps = persistence_steps
        self.dt = dt

        self.state = InteractionState(mass=mass)
        self.active_force: Optional[DecayingForce] = None
        self.status = "WAITING"  # WAITING, DYNAMIC_EVOLUTION, STALLED_ZERO_STATE
        self.zero_counter = 0

    def apply_user_prompt(self, prompt: str, direction: np.ndarray, t: float, custom_f0: Optional[float] = None) -> None:
        """
        Applies a one-time initial interaction force F0 produced by a user prompt at time t0.
        Direction is normalized.
        """
        norm_dir = direction / np.linalg.norm(direction) if np.linalg.norm(direction) > 0 else np.array([1.0, 0.0])
        mag = custom_f0 if custom_f0 is not None else self.f0
        self.active_force = DecayingForce(f0=mag, lambda_decay=self.lambda_decay, t0=t, direction=norm_dir)
        self.status = "FORCE_INITIALIZED"
        self.zero_counter = 0

    def compute_acceleration(self, pos: np.ndarray, vel: np.ndarray, t: float) -> np.ndarray:
        # Applied force
        f_applied = self.active_force.get_force(t) if self.active_force else np.zeros(2)
        # Friction force opposes velocity
        f_friction = self.friction_model.get_friction_force(vel)
        f_net = f_applied - f_friction
        return f_net / self.mass

    def step(self, t: float) -> Tuple[InteractionState, bool]:
        """
        Advances the simulation by dt.
        Returns (state, is_stalled_near_zero)
        """
        pos, vel = self.integrator.step(
            self.state.position,
            self.state.velocity,
            self.compute_acceleration,
            t,
            self.dt
        )
        accel = self.compute_acceleration(pos, vel, t)
        self.state.update(pos, vel, accel)

        # Check speed against epsilon threshold
        speed = self.state.speed()
        is_stalled = False

        if speed < self.epsilon:
            self.zero_counter += 1
            if self.zero_counter >= self.persistence_steps:
                is_stalled = True
                self.status = "STALLED_ZERO_STATE"
        else:
            self.zero_counter = 0
            self.status = "DYNAMIC_EVOLUTION"

        return self.state, is_stalled
