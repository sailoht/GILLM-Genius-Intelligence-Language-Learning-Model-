import numpy as np
import json
import csv
import os
from typing import Dict, Any, List
from human_interaction_sim.dynamics import SimulationEngine
from human_interaction_sim.question_generator import ModularQuestionGenerator
from human_interaction_sim.simulated_user import SimulatedUser

class ExperimentRunner:
    def __init__(self, results_dir: str = "human_interaction_sim/results") -> None:
        self.results_dir = results_dir
        os.makedirs(self.results_dir, exist_ok=True)
        self.q_gen = ModularQuestionGenerator()
        self.user = SimulatedUser()

    def run_single_force_experiment(
        self,
        exp_name: str,
        f0: float,
        c_friction: float,
        lambda_decay: float = 0.5,
        max_time: float = 20.0,
        dt: float = 0.1
    ) -> Dict[str, Any]:
        sim = SimulationEngine(f0=f0, c_friction=c_friction, lambda_decay=lambda_decay, dt=dt)

        # Apply initial prompt
        sim.apply_user_prompt("I want to learn quantum mechanics.", direction=np.array([1.0, 0.5]), t=0.0)

        t_history = []
        force_history = []
        vel_history = []
        pos_history = []
        events = []

        time_to_zero = None
        t = 0.0

        while t <= max_time:
            t_history.append(t)
            # Record current force
            f_val = sim.active_force.get_force(t) if sim.active_force else np.zeros(2)
            force_history.append(np.linalg.norm(f_val))
            vel_history.append(sim.state.speed())
            pos_history.append(sim.state.position.copy().tolist())

            state, is_stalled = sim.step(t)

            if is_stalled and time_to_zero is None:
                time_to_zero = t
                q = self.q_gen.generate_question("quantum mechanics")
                events.append({"time": t, "type": "NEAR_ZERO_QUESTION", "question": q, "position": state.position.copy().tolist()})

            t += dt

        logs = [{
            "cycle_id": 1,
            "user_input": "I want to learn quantum mechanics.",
            "initial_force": f0,
            "force_decay_rate": lambda_decay,
            "friction": c_friction,
            "initial_velocity": vel_history[0] if vel_history else 0.0,
            "time_to_near_zero": time_to_zero or max_time,
            "question_generated": events[0]["question"] if events else "None",
            "user_response": "N/A",
            "new_force": 0.0,
            "trajectory_direction": [1.0, 0.5]
        }]

        res = {
            "experiment": exp_name,
            "f0": f0,
            "c_friction": c_friction,
            "lambda_decay": lambda_decay,
            "t_history": t_history,
            "force_history": force_history,
            "vel_history": vel_history,
            "pos_history": pos_history,
            "events": events,
            "time_to_near_zero": time_to_zero or max_time,
            "logs": logs
        }

        # Save JSON & CSV
        self._save_logs(exp_name, logs, res)
        return res

    def run_repeated_loop_experiment(
        self,
        exp_name: str = "Experiment_E_Repeated_Loop",
        num_cycles: int = 10,
        dt: float = 0.1
    ) -> Dict[str, Any]:
        sim = SimulationEngine(f0=10.0, c_friction=0.5, lambda_decay=0.5, dt=dt)

        t_history = []
        force_history = []
        vel_history = []
        pos_history = []
        events = []
        logs = []

        t = 0.0
        current_topic = "quantum mechanics"
        current_dir = np.array([1.0, 0.2])

        sim.apply_user_prompt(f"I want to learn {current_topic}.", direction=current_dir, t=t)
        events.append({"time": t, "type": "INITIAL_USER_PROMPT", "text": f"I want to learn {current_topic}.", "position": sim.state.position.copy().tolist()})

        cycle_count = 0
        cycle_start_time = t

        while cycle_count < num_cycles and t <= 150.0:
            t_history.append(t)
            f_val = sim.active_force.get_force(t) if sim.active_force else np.zeros(2)
            force_history.append(np.linalg.norm(f_val))
            vel_history.append(sim.state.speed())
            pos_history.append(sim.state.position.copy().tolist())

            state, is_stalled = sim.step(t)

            if is_stalled:
                cycle_count += 1
                time_to_zero = t - cycle_start_time
                q = self.q_gen.generate_question(current_topic, cycle_count)
                events.append({"time": t, "type": "QUESTION_GENERATED", "question": q, "position": state.position.copy().tolist()})

                # Simulate user response
                # Alternate between continue, deepen, and short answer
                resp_types = ["CONTINUE", "DEEPEN", "SHORT_ANSWER"]
                resp_type = resp_types[cycle_count % len(resp_types)]
                user_resp = self.user.respond(q, current_topic, current_dir, response_type=resp_type)

                events.append({"time": t + dt, "type": "USER_RESPONSE", "response": user_resp.text, "position": state.position.copy().tolist()})

                # Log cycle data
                logs.append({
                    "cycle_id": cycle_count,
                    "user_input": f"User response: {user_resp.text}",
                    "initial_force": user_resp.force_magnitude,
                    "force_decay_rate": sim.lambda_decay,
                    "friction": sim.friction_model.c,
                    "initial_velocity": state.speed(),
                    "time_to_near_zero": time_to_zero,
                    "question_generated": q,
                    "user_response": user_resp.text,
                    "new_force": user_resp.force_magnitude,
                    "trajectory_direction": user_resp.direction.tolist()
                })

                # Re-initialize force from user response
                current_dir = user_resp.direction
                sim.apply_user_prompt(user_resp.text, direction=current_dir, t=t + dt, custom_f0=user_resp.force_magnitude)
                cycle_start_time = t + dt

            t += dt

        res = {
            "experiment": exp_name,
            "num_cycles_completed": cycle_count,
            "t_history": t_history,
            "force_history": force_history,
            "vel_history": vel_history,
            "pos_history": pos_history,
            "events": events,
            "logs": logs
        }
        self._save_logs(exp_name, logs, res)
        return res

    def run_topic_change_experiment(
        self,
        exp_name: str = "Experiment_F_Topic_Change",
        dt: float = 0.1
    ) -> Dict[str, Any]:
        sim = SimulationEngine(f0=10.0, c_friction=0.5, lambda_decay=0.5, dt=dt)

        t_history = []
        force_history = []
        vel_history = []
        pos_history = []
        events = []
        logs = []

        t = 0.0
        current_topic = "quantum mechanics"
        current_dir = np.array([1.0, 0.0])

        sim.apply_user_prompt("I want to learn quantum mechanics.", direction=current_dir, t=t)
        events.append({"time": t, "type": "INITIAL_USER_PROMPT", "text": "I want to learn quantum mechanics.", "position": sim.state.position.copy().tolist()})

        cycle = 0
        cycle_start_time = t

        while cycle < 3 and t <= 50.0:
            t_history.append(t)
            f_val = sim.active_force.get_force(t) if sim.active_force else np.zeros(2)
            force_history.append(np.linalg.norm(f_val))
            vel_history.append(sim.state.speed())
            pos_history.append(sim.state.position.copy().tolist())

            state, is_stalled = sim.step(t)

            if is_stalled:
                cycle += 1
                time_to_zero = t - cycle_start_time
                q = self.q_gen.generate_question(current_topic, cycle)
                events.append({"time": t, "type": "QUESTION_GENERATED", "question": q, "position": state.position.copy().tolist()})

                if cycle == 1:
                    # Abrupt topic change!
                    user_resp = self.user.respond(q, current_topic, current_dir, response_type="COMPLETE_CHANGE", override_topic="machine learning")
                    events.append({"time": t + dt, "type": "TOPIC_CHANGE", "text": user_resp.text, "position": state.position.copy().tolist()})
                else:
                    user_resp = self.user.respond(q, current_topic, current_dir, response_type="CONTINUE")
                    events.append({"time": t + dt, "type": "USER_RESPONSE", "text": user_resp.text, "position": state.position.copy().tolist()})

                logs.append({
                    "cycle_id": cycle,
                    "user_input": user_resp.text,
                    "initial_force": user_resp.force_magnitude,
                    "force_decay_rate": sim.lambda_decay,
                    "friction": sim.friction_model.c,
                    "initial_velocity": state.speed(),
                    "time_to_near_zero": time_to_zero,
                    "question_generated": q,
                    "user_response": user_resp.text,
                    "new_force": user_resp.force_magnitude,
                    "trajectory_direction": user_resp.direction.tolist()
                })

                current_topic = user_resp.topic
                current_dir = user_resp.direction
                sim.apply_user_prompt(user_resp.text, direction=current_dir, t=t + dt, custom_f0=user_resp.force_magnitude)
                cycle_start_time = t + dt

            t += dt

        res = {
            "experiment": exp_name,
            "num_cycles_completed": cycle,
            "t_history": t_history,
            "force_history": force_history,
            "vel_history": vel_history,
            "pos_history": pos_history,
            "events": events,
            "logs": logs
        }
        self._save_logs(exp_name, logs, res)
        return res

    def _save_logs(self, name: str, logs: List[Dict[str, Any]], res: Dict[str, Any]) -> None:
        json_path = os.path.join(self.results_dir, f"{name}.json")
        csv_path = os.path.join(self.results_dir, f"{name}.csv")

        # Save JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2)

        # Save CSV
        if logs:
            fieldnames = list(logs[0].keys())
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(logs)
