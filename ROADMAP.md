# J.A.R.V.I.S. Engineering Roadmap

This document outlines the planned incremental development roadmap for the JARVIS Personal AI Operating System.

---

## DEVELOPMENT PHASES

### **Phase 1: Core Lifecycle & GILLM Integration [CURRENT]**
*   [x] Establish complete modular package directory tree.
*   [x] Design and build the typed `EventBus`.
*   [x] Define unified multi-modal `PerceptionEvent` schemas.
*   [x] Implement `CognitiveEngine` abstraction (`GILLMEngine`, `LLMEngine`, `HybridEngine`).
*   [x] Implement 11-step `JarvisAgent` core loop event lifecycle.
*   [x] Verify with 100% green unit and integration tests.

### **Phase 2: Memory & Tool Registry [PLANNED]**
*   [ ] Implement structured User Profile and preferences config.
*   [ ] Build decoupled Working, Episodic, and Procedural memory classes.
*   [ ] Implement a typed, schema-validated Tool Registry.
*   [ ] Build base local filesystem and system monitoring tools.

### **Phase 3: Planner & Verification [PLANNED]**
*   [ ] Implement sequential dependent-task plan generation.
*   [ ] Design action verification hooks querying the OS process table and window systems.
*   [ ] Implement retry, fallback planning, and rollback policies.

### **Phase 4: OS Control & Sandboxing [PLANNED]**
*   [ ] Implement OS-level semantic API bindings for windows, keyboard, and mouse control.
*   [ ] Set up dockerized terminal sandboxing for safe code execution.
*   [ ] Build basic browser automation adapter.

### **Phase 5: Sensory Voice & Vision [PLANNED]**
*   [ ] Integrate local Wake Word detection, Whisper speech-to-text, and TTS voice output.
*   [ ] Implement conversation activity detection (VAD) and barge-in interruption.
*   [ ] Integrate local vision models for document parsing and screenshot OCR.

### **Phase 6: Proactive Systems & Learning [PLANNED]**
*   [ ] Implement background task schedulers and system event listeners.
*   [ ] Build shadow-mode learning systems tracking user workflow corrections.
*   [ ] Implement proactive notification priorities.
