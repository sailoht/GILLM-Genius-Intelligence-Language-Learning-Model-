import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Dict, Any, List

class ExperimentVisualizer:
    """
    Generates Matplotlib plots for simulation experiments:
    Plot 1: Force vs Time F(t)
    Plot 2: Velocity vs Time v(t)
    Plot 3: Interaction State vs Time x(t)
    Plot 4: 2D Trajectory (x, y) with event markers
    """
    def __init__(self, output_dir: str = "human_interaction_sim/results") -> None:
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_experiment_summary(self, res: Dict[str, Any], show: bool = False) -> str:
        exp_name = res["experiment"]
        t_hist = np.array(res["t_history"])
        f_hist = np.array(res["force_history"])
        v_hist = np.array(res["vel_history"])
        pos_hist = np.array(res["pos_history"])  # Shape (N, 2)
        events = res.get("events", [])

        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f"Computational Interaction Dynamics: {exp_name.replace('_', ' ')}", fontsize=16)

        # Plot 1: Force vs Time
        axs[0, 0].plot(t_hist, f_hist, color='blue', linewidth=1.5, label='Force F(t)')
        axs[0, 0].set_title("Force F(t) vs Time")
        axs[0, 0].set_xlabel("Time (t)")
        axs[0, 0].set_ylabel("Applied Force Magnitude")
        axs[0, 0].grid(True, linestyle='--', alpha=0.6)
        axs[0, 0].legend()

        # Plot 2: Velocity vs Time
        axs[0, 1].plot(t_hist, v_hist, color='red', linewidth=1.5, label='Velocity v(t)')
        axs[0, 1].axhline(y=0.1, color='gray', linestyle=':', label='Near-Zero Threshold (epsilon)')
        axs[0, 1].set_title("Velocity v(t) vs Time")
        axs[0, 1].set_xlabel("Time (t)")
        axs[0, 1].set_ylabel("Interaction Velocity Magnitude")
        axs[0, 1].grid(True, linestyle='--', alpha=0.6)
        axs[0, 1].legend()

        # Plot 3: State x(t) vs Time
        axs[1, 0].plot(t_hist, pos_hist[:, 0], color='green', linewidth=1.5, label='State Position x(t)')
        axs[1, 0].set_title("Interaction Position x(t) vs Time")
        axs[1, 0].set_xlabel("Time (t)")
        axs[1, 0].set_ylabel("Semantic Position x")
        axs[1, 0].grid(True, linestyle='--', alpha=0.6)
        axs[1, 0].legend()

        # Plot 4: 2D Trajectory (x, y)
        axs[1, 1].plot(pos_hist[:, 0], pos_hist[:, 1], color='purple', linewidth=1.5, label='2D Trajectory')
        axs[1, 1].set_title("2D Interaction Trajectory (x vs y)")
        axs[1, 1].set_xlabel("Topic Position x")
        axs[1, 1].set_ylabel("Conceptual Direction y")
        axs[1, 1].grid(True, linestyle='--', alpha=0.6)

        # Mark events on 2D Trajectory
        for ev in events:
            pos = ev.get("position", [0.0, 0.0])
            ev_type = ev.get("type")
            if ev_type in ["INITIAL_USER_PROMPT", "USER_RESPONSE"]:
                axs[1, 1].plot(pos[0], pos[1], 'go', markersize=6, label='User Input' if 'User Input' not in axs[1, 1].get_legend_handles_labels()[1] else "")
            elif ev_type in ["NEAR_ZERO_QUESTION", "QUESTION_GENERATED"]:
                axs[1, 1].plot(pos[0], pos[1], 'ro', markersize=6, label='Question Generated' if 'Question Generated' not in axs[1, 1].get_legend_handles_labels()[1] else "")
            elif ev_type == "TOPIC_CHANGE":
                axs[1, 1].plot(pos[0], pos[1], 'mo', markersize=8, label='Topic Change' if 'Topic Change' not in axs[1, 1].get_legend_handles_labels()[1] else "")

        axs[1, 1].legend()

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, f"{exp_name}_summary.png")
        plt.savefig(save_path, dpi=300)
        if show:
            plt.show()
        plt.close()
        return save_path
