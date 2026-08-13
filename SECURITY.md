# J.A.R.V.I.S. Core Security Model

Safety, auditability, and local-first data privacy are the bedrock architectural principles of JARVIS.

---

## 1. CENTRAL SAFETY & AUTHORIZATION GATE

Every action formulated by the planning engine must be checked against a centralized safety controller before execution.

```
Plan Step → Security Controller → Check Risk Category → AUTO_APPROVE / ASK_USER / DENY
```

### Risk Classifications:
*   **`READ`**: Inspecting files, viewing system status, or indexing local notes. (Normally `AUTO_APPROVE`).
*   **`WRITE`**: Creating or modifying local files. (Requires `AUTO_APPROVE` inside designated directories; `ASK_USER` otherwise).
*   **`EXECUTE`**: Launching processes, running scripts, or terminal execution. (Requires `ASK_USER` or strict Docker sandboxing).
*   **`DELETE`**: Removing files or stopping system processes. (Always `ASK_USER` or `DENY`).
*   **`NETWORK`**: Making API calls or web browsing. (Requires explicit host whitelist).
*   **`FINANCIAL`**: Performing operations with commercial costs or payments. (Always requires `ASK_USER` manual confirmation).
*   **`CREDENTIAL`**: Extracting system secrets, keys, or passwords. (Always `DENY` or restrict to secure local vaults).

---

## 2. RECURSION SAFETY & EMERGENCY KILL SWITCH

To prevent runaway background agents, recursive code loops, or unresponsive automation tasks, JARVIS implements a hardware-level **Emergency Kill Switch**.

*   **Activation**: Direct user interruption (`JARVIS STOP`) or CLI keyboard trigger.
*   **Operation**: Immediately kills active sub-processes, closes browser automation instances, clears the Task Queue, and halts background thread schedulers.
*   **Non-AI Dependent**: The kill switch is registered as a low-level interrupt hook that executes immediately without passing through cognitive model parsing.
