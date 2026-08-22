# Human Interaction Dynamics Simulation

## A Physics-Inspired Computational Model of Conversational Interaction Dynamics

This project implements a research-grade computational simulation of human-AI interaction dynamics modeled as a physics-inspired dynamic system.

> **CRITICAL DISCLAIMER**: This simulation is **NOT** an attempt to claim that human cognition literally follows Newtonian mechanics or physical laws. It is an experimental computational hypothesis designed to evaluate whether physics-inspired dynamic forces (one-time decaying force, continuous friction, and zero-velocity state detection) can generate more proactive, sustained, and continuous conversational interactions.

---

## 1. MODEL ASSUMPTIONS & EQUATIONS

### 1.1 One-Time Initial Interaction Force
When a user provides a prompt at time $t_0$, it applies a one-time initial force $F_0$ that decays exponentially over time:
$$F(t) = F_0 \cdot e^{-\lambda (t - t_0)}$$
*   $F_0$: Initial force magnitude (representing prompt energy/salience).
*   $\lambda$: Exponential decay coefficient.
*   $t_0$: Timestamp of user prompt arrival.
*   **Key Assumption**: The user force is initialized once upon prompt arrival and is **NOT** re-added at every numerical simulation step.

### 1.2 Natural Friction / Damping Model
Friction is modeled as a continuous opposing force proportional to velocity:
$$F_{\text{friction}}(v) = c \cdot v$$
*   $c$: Damping coefficient.
*   **Key Assumption**: Friction continuously opposes motion regardless of whether the user is typing, simulating natural conversational inertia and topic decay.

### 1.3 State Equations & Integration
$$F_{\text{net}}(t) = F(t) - F_{\text{friction}}(v)$$
$$a(t) = \frac{F_{\text{net}}(t)}{m}$$
$$\frac{dv}{dt} = a(t), \quad \frac{dx}{dt} = v(t)$$
*   Numerical integration is performed via explicit Euler integration ($x, y$ 2D state space).

---

## 2. STATE MACHINE & ZERO-VELOCITY DETECTION

The interaction cycle progresses through the following state machine:

```
WAITING → USER_INPUT → FORCE_INITIALIZED → DYNAMIC_EVOLUTION → FORCE_DECAYS → MOTION_DECAYS → CHECK_ZERO_STATE → QUESTION_GENERATION → WAIT_FOR_USER → USER_RESPONSE → NEW_FORCE_INITIALIZED → ...
```

### Stalled / Near-Zero State Criteria:
To prevent numerical noise from triggering false questions on isolated low-velocity readings, the system classifies the interaction as stalled only when:
$$\|v(t)\| < \epsilon$$
persistently for a minimum of $N$ consecutive simulation timesteps (`persistence_steps`).

Once stalled, the system generates a relevant follow-up question, prompting a simulated user response that injects a new directional force $F_0$.

---

## 3. WHAT THE MODEL DOES NOT PROVE

1.  **Does NOT prove human brain physics**: Human thought is non-Newtonian, non-linear, and deeply biological.
2.  **Does NOT prove LLM replacement**: This simulation evaluates interaction dynamics, not open-ended reasoning capabilities.
3.  **Arbitrary Parameters**: Mass ($m$), initial force ($F_0$), decay ($\lambda$), and friction ($c$) are configurable computational scaling parameters, not physical constants.

---

## 4. SCIENTIFIC HYPOTHESES & OBSERVATIONS

*   **Supporting Observations**: If increasing $F_0$ extends trajectory length and higher friction $c$ shortens time-to-near-zero, the computational mechanics behave consistently with dynamic system predictions.
*   **Rejecting Observations**: If near-zero detection oscillates erratically or fails to produce sustained multi-cycle interactions under reasonable damping, the dynamic force model is unviable for conversational control.

---

## 5. RUNNING THE SIMULATION

### Run Automated Experiments A-F:
```bash
python main.py
```
This runs Experiments A through F, generates Matplotlib 4-panel summary plots in `results/`, and outputs JSON/CSV logs.

### Run Interactive Streamlit UI:
```bash
streamlit run app.py
```
Allows real-time adjustment of $m$, $F_0$, $\lambda$, $c$, $\epsilon$, and persistence steps with live trajectory plots.
