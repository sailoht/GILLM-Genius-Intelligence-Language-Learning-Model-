import os
import json
import numpy as np
from human_interaction_sim.dynamics import SimulationEngine
from human_interaction_sim.experiments import ExperimentRunner
from human_interaction_sim.visualization import ExperimentVisualizer
from human_interaction_sim.hierarchical_generator import PhysicsControlledGenerator
from human_interaction_sim.comparator import ModeComparisonEngine

def main():
    print("==================================================")
    print("HUMAN-AI INTERACTION DYNAMICS SIMULATION ENGINE")
    print("Hierarchical Language Generation Controlled by Dynamics")
    print("==================================================")

    runner = ExperimentRunner()
    visualizer = ExperimentVisualizer()
    generator = PhysicsControlledGenerator()
    comparator = ModeComparisonEngine()

    # 1. Run Experiments A through F
    print("\n[1/6] Running Experiment A (Strong Initial Force)...")
    exp_a = runner.run_single_force_experiment("Experiment_A_Strong_Force", f0=25.0, c_friction=0.2)
    visualizer.plot_experiment_summary(exp_a)

    print("[2/6] Running Experiment B (Weak Initial Force)...")
    exp_b = runner.run_single_force_experiment("Experiment_B_Weak_Force", f0=3.0, c_friction=0.5)
    visualizer.plot_experiment_summary(exp_b)

    print("[3/6] Running Experiment C (High Friction)...")
    exp_c = runner.run_single_force_experiment("Experiment_C_High_Friction", f0=10.0, c_friction=1.5)
    visualizer.plot_experiment_summary(exp_c)

    print("[4/6] Running Experiment D (Low Friction)...")
    exp_d = runner.run_single_force_experiment("Experiment_D_Low_Friction", f0=10.0, c_friction=0.1)
    visualizer.plot_experiment_summary(exp_d)

    print("[5/6] Running Experiment E (Repeated Interaction Loop - 10 cycles)...")
    exp_e = runner.run_repeated_loop_experiment("Experiment_E_Repeated_Loop", num_cycles=10)
    visualizer.plot_experiment_summary(exp_e)

    print("[6/6] Running Experiment F (Topic Change)...")
    exp_f = runner.run_topic_change_experiment("Experiment_F_Topic_Change")
    visualizer.plot_experiment_summary(exp_f)

    # 2. Run Hierarchical Text Generation Demonstration
    print("\n==================================================")
    print("HIERARCHICAL LANGUAGE GENERATION DEMONSTRATION:")
    print("==================================================")
    print("Input Prompt: 'Explain quantum tunneling.'")
    sim_demo = SimulationEngine(f0=20.0, c_friction=0.5)
    sim_demo.apply_user_prompt("Explain quantum tunneling.", direction=np.array([1.0, 0.4]), t=0.0)
    sim_demo.step(1.0)

    demo_out = generator.generate_from_sim_state(sim_demo, topic="quantum mechanics", mode="PARAGRAPH")

    print("\n[USER VIEW - FINAL HUMAN-READABLE OUTPUT]:")
    print(demo_out["user_view"])

    print("\n[RESEARCH VIEW - HIERARCHICAL PROGRESSION]:")
    r_view = demo_out["research_view"]
    print(f"* Concept: {r_view['concept']}")
    print(f"* Subword Candidates ('quant'): {r_view['subword_candidates']}")
    print(f"* Phrase Projections ('quantum'): {r_view['phrase_projections']}")
    print(f"* Paragraph State: {r_view['paragraph_state']}")

    # 3. Mode A vs Mode B Comparison
    print("\n==================================================")
    print("MODE A (Physics-Inspired) vs MODE B (Baseline) COMPARISON:")
    print("==================================================")
    comp_res = comparator.compare_modes("Explain quantum tunneling.", topic="quantum mechanics")
    print(f"* Mode A (Physics-Inspired Output):\n  '{comp_res['mode_a_physics_inspired']['text']}'")
    print(f"* Mode B (Baseline Output):\n  '{comp_res['mode_b_baseline']['text']}'")
    print(f"\nConclusion: {comp_res['comparison_summary']}")

    # 4. Save aggregate metrics
    metrics_path = os.path.join(runner.results_dir, "simulation_summary_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump({
            "exp_a_time_to_zero": exp_a["time_to_near_zero"],
            "exp_b_time_to_zero": exp_b["time_to_near_zero"],
            "exp_e_cycles": exp_e["num_cycles_completed"],
            "comparison": comp_res
        }, f, indent=2)

    print(f"\nAll experiments and language generation runs completed successfully! Metrics saved to '{metrics_path}'.")

if __name__ == "__main__":
    main()
