# J.A.R.V.I.S. Engineering Design Document

## 1. VISION
The long-term objective of **J.A.R.V.I.S.** is to construct a persistent, multi-modal, local-first personal AI operating system.

It is designed to feel like an operating intelligence—capable of perceiving, remembering, planning, and executing verifiably—rather than a passive text box wrapped around a cloud API.

---

## 2. GILLM RESEARCH GOALS
Within JARVIS, **GILLM (Genius Intelligence Language Learning Model)** serves as our primary experimental linguistic and pre-processing engine.

GILLM's core purpose is to investigate whether a deterministic, compositional, rule-based approach can provide useful structural understanding, strict error detection, and intent validation with minimal computational cost.

Rather than assuming GILLM will completely replace deep neural networks, JARVIS provides a decoupled, model-agnostic abstraction (`CognitiveEngine`). This allows researchers to measure and compare:
1.  **GILLM-only mode**: Fully local, highly deterministic, zero statistical hallucinations, operates in under 200 KB RAM.
2.  **LLM-only mode**: Standard generative reasoning via local Ollama or cloud models.
3.  **Hybrid mode**: Combining GILLM's strict grammatical and semantic role parsing with the LLM's open-ended reasoning capabilities.

---

## 3. CORE DESIGN RULES

*   **Rule 1: OS Control must be Semantic**. Keyboard/mouse clicks based on screenshot coordinate predictions must be a last-resort fallback. Vision-based UI detection must supplement structured OS API calls (such as D-Bus, Win32, or AppleEvents), not replace them.
*   **Rule 2: Separating Personality from Cognition**. Personality layers, speech patterns, and custom response templates must reside in a decoupled presentation view layer. Factorial logic, factual reasoning, permission validation, and memory recall must remain objective and uninfluenced by communication style.
*   **Rule 3: Decoupled Modularity**. If any single AI model or external API disappears, the JARVIS agent lifecycle remains fully operational. The system degradates gracefully to local fallback models.
*   **Rule 4: Zero Silent Errors**. If the system is uncertain, has insufficient evidence, or detects an error, it must explicitly represent that uncertainty and request human clarification, rather than guessing or fabricating certainty.
