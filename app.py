import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from human_interaction_sim.dynamics import SimulationEngine
from human_interaction_sim.question_generator import ModularQuestionGenerator
from human_interaction_sim.simulated_user import SimulatedUser
from human_interaction_sim.hierarchical_generator import PhysicsControlledGenerator
from human_interaction_sim.comparator import ModeComparisonEngine

st.set_page_config(page_title="Human-AI Interaction Dynamics Simulation", layout="wide")

st.title("Human-AI Interaction Dynamics Simulation")
st.caption("A physics-inspired computational model controlling hierarchical language generation (GILLM 0.5.0 Research Baseline)")

# Sidebar Controls
st.sidebar.header("Physics Parameters")
m = st.sidebar.slider("Mass (m)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
f0 = st.sidebar.slider("Initial Force (F0)", min_value=1.0, max_value=50.0, value=15.0, step=1.0)
lambda_decay = st.sidebar.slider("Force Decay Coefficient (lambda)", min_value=0.05, max_value=2.0, value=0.5, step=0.05)
c_friction = st.sidebar.slider("Friction Coefficient (c)", min_value=0.05, max_value=3.0, value=0.5, step=0.05)
epsilon = st.sidebar.slider("Near-Zero Speed Threshold (epsilon)", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
persistence_steps = st.sidebar.slider("Persistence Steps for Zero State", min_value=1, max_value=20, value=5, step=1)
dt = st.sidebar.slider("Timestep (dt)", min_value=0.01, max_value=0.5, value=0.1, step=0.01)

st.sidebar.subheader("Language Generation Settings")
topic = st.sidebar.selectbox("Concept Topic", ["quantum mechanics", "machine learning", "physics", "general"])
gen_mode = st.sidebar.radio("Generation Format", ["PARAGRAPH", "SENTENCE"])

prompt = st.text_input("User Prompt:", value=f"Explain {topic}.")

if st.button("Run Simulation & Generate Language"):
    sim = SimulationEngine(
        mass=m,
        f0=f0,
        lambda_decay=lambda_decay,
        c_friction=c_friction,
        epsilon=epsilon,
        persistence_steps=persistence_steps,
        dt=dt
    )

    physics_gen = PhysicsControlledGenerator()
    comparator = ModeComparisonEngine()

    t_hist = []
    f_hist = []
    v_hist = []
    pos_hist = []

    # Apply prompt force
    sim.apply_user_prompt(prompt, direction=np.array([1.0, 0.4]), t=0.0)

    # Run physics steps
    for step in range(50):
        t = step * dt
        t_hist.append(t)
        f_val = sim.active_force.get_force(t) if sim.active_force else np.zeros(2)
        f_hist.append(np.linalg.norm(f_val))
        v_hist.append(sim.state.speed())
        pos_hist.append(sim.state.position.copy().tolist())
        sim.step(t)

    pos_arr = np.array(pos_hist)

    # Generate hierarchical output
    out = physics_gen.generate_from_sim_state(sim, topic=topic, mode=gen_mode)
    comp_res = comparator.compare_modes(prompt, topic=topic)

    # TABS FOR DUAL VIEW
    tab1, tab2, tab3 = st.tabs(["USER VIEW", "RESEARCH VIEW", "MODE A vs MODE B COMPARISON"])

    # 1. USER VIEW
    with tab1:
        st.subheader("Final Human-Readable Output")
        st.info(out["user_view"])

    # 2. RESEARCH VIEW
    with tab2:
        st.subheader("Internal Simulation & Hierarchical Generation Progression")

        # Subword -> Word -> Phrase -> Sentence Debug Box
        st.markdown("#### Hierarchical Language Progression")
        r_view = out["research_view"]

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("**1. Subword Candidates:**")
            st.code(", ".join(r_view["subword_candidates"]))
        with col_b:
            st.markdown("**2. Phrase Projections:**")
            st.code(", ".join(r_view["phrase_projections"]))
        with col_c:
            st.markdown("**3. Paragraph State:**")
            st.json(r_view["paragraph_state"])

        st.markdown("#### Physical Dynamics Plots")
        c1, c2 = st.columns(2)
        with c1:
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            ax1.plot(t_hist, f_hist, color='blue', label='Force F(t)')
            ax1.set_title("Force F(t) vs Time")
            ax1.set_xlabel("Time (t)")
            ax1.set_ylabel("Force Magnitude")
            ax1.grid(True)
            st.pyplot(fig1)

            fig2, ax2 = plt.subplots(figsize=(6, 4))
            ax2.plot(t_hist, pos_arr[:, 0], color='green', label='Position x(t)')
            ax2.set_title("Position x(t) vs Time")
            ax2.set_xlabel("Time (t)")
            ax2.set_ylabel("Semantic Position x")
            ax2.grid(True)
            st.pyplot(fig2)

        with c2:
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            ax3.plot(t_hist, v_hist, color='red', label='Velocity v(t)')
            ax3.axhline(y=epsilon, color='gray', linestyle=':', label='Threshold (epsilon)')
            ax3.set_title("Velocity v(t) vs Time")
            ax3.set_xlabel("Time (t)")
            ax3.set_ylabel("Velocity Magnitude")
            ax3.grid(True)
            st.pyplot(fig3)

            fig4, ax4 = plt.subplots(figsize=(6, 4))
            ax4.plot(pos_arr[:, 0], pos_arr[:, 1], color='purple', label='2D Trajectory')
            ax4.set_title("2D Trajectory (x vs y)")
            ax4.set_xlabel("Position x")
            ax4.set_ylabel("Direction y")
            ax4.grid(True)
            st.pyplot(fig4)

    # 3. MODE A vs MODE B
    with tab3:
        st.subheader("Mode A (Physics-Inspired) vs Mode B (Probabilistic Baseline)")

        ca, cb = st.columns(2)
        with ca:
            st.markdown("### Mode A: Physics-Inspired Generator")
            st.write(comp_res["mode_a_physics_inspired"]["text"])
            st.json(comp_res["mode_a_physics_inspired"])

        with cb:
            st.markdown("### Mode B: Baseline Generator")
            st.write(comp_res["mode_b_baseline"]["text"])
            st.json(comp_res["mode_b_baseline"])

        st.success(comp_res["comparison_summary"])
