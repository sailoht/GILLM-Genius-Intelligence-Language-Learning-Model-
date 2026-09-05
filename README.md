# GILLM — Genius Intelligence Language Learning Model

### Architecture Overview:
```text
Human
  ↕
LangBaby (Human Communication Subsystem)
  ↕
GIR (Genius Intelligence Representation)
  ↕
GILLM Intelligence Core
  ↕
World Model / 3D Registry / Executable Laws
```

---

## 1. PROJECT OVERVIEW

GILLM is an experimental research architecture for building an intelligence system around explicit representation, investigation, structured transformation, validation, and synthesis rather than conventional next-token prediction.

Rather than treating language intelligence as a statistical next-token prediction problem $P(\text{token}_t \mid \text{token}_{<t})$, GILLM decouples human communication (**LangBaby**) from core intelligence (**GILLM Core**), communicating through a structured, serializable contract called **GIR** (Genius Intelligence Representation).

---

## 2. KEY ARCHITECTURAL COMPONENTS

*   **LangBaby**: The human communication subsystem inside GILLM. Responsible for structural text parsing into GIR and hierarchical text realization from GIR without next-token autocomplete.
*   **GIR (Genius Intelligence Representation)**: The common internal serializable representation between LangBaby and GILLM.
*   **DataAtoms & DataMolecules**: Explicit information units ($A = \text{id, type, value, unit, provenance}$) and structured information objects ($M = \text{atoms, state, spatial\_position, laws, provenance}$).
*   **3D Information Registry**: Spatial 3D information-world and search structure where DataMolecules exist at coordinates $(x, y, z)$.
*   **Gaussian Information Fields**: Mathematical field $G(x,y,z)$ used as an information search and synthesis signal.
*   **Executable Laws & Physics Foundation**: Formal law registry (`LawRegistry`) executing physical transformations (e.g. Newton's 2nd Law $F = m \cdot a \implies a = F/m$) with dimensional unit validation.
*   **Proof-Carrying State & Provenance**: Every derived or synthesized conclusion carries complete derivation trace graphs (`ProvenanceRecord`).
*   **13-Stage Investigation Loop**: `Observe` $\rightarrow$ `Define` $\rightarrow$ `Decompose` $\rightarrow$ `Question` $\rightarrow$ `Search` $\rightarrow$ `Connect` $\rightarrow$ `Construct` $\rightarrow$ `Challenge` $\rightarrow$ `Test` $\rightarrow$ `Compare` $\rightarrow$ `Validate` $\rightarrow$ `Revise`.

---

## 3. CORE DESIGN PRINCIPLES

1.  **NO NEXT-TOKEN PREDICTION**: Language generation is built via explicit structural construction: `Word` $\rightarrow$ `Phrase` $\rightarrow$ `Proposition` $\rightarrow$ `Sentence` $\rightarrow$ `Paragraph` $\rightarrow$ `Document`.
2.  **NO-ILLUSION PRINCIPLE**: Nothing becomes an asserted fact without a valid state path and proof-carrying derivation provenance. Epistemic status (`OBSERVED`, `DERIVED`, `SYNTHESIZED`, `HYPOTHETICAL`) is strictly separated from Validation status (`VALID`, `INVALID`, `UNVERIFIED`).
3.  **UNKNOWN IS A FIRST-CLASS STATE**: `UNKNOWN != FAILURE`. If information is missing, GILLM explicitly represents it as `UNKNOWN` rather than fabricating proselike hallucinations.
4.  **DECOUPLED COMMUNICATION**: LangBaby handles language communication; GILLM Core handles world modeling, reasoning, and synthesis.

---

## 4. REPOSITORY STRUCTURE

```text
src/gillm/
├── core/            # Enums (EpistemicStatus, ValidationStatus)
├── gir/             # Genius Intelligence Representation (GIR)
├── molecules/       # DataAtoms and DataMolecules
├── provenance/      # ProvenanceGraph and Traceability
├── space/           # 3D Coordinates (x, y, z)
├── registry/        # 3D Information Registry
├── fields/          # Gaussian Information Fields
├── query/           # QueryMolecules
├── operators/       # Filterization operators
├── physics/         # Quantities and Units checking
├── laws/            # Executable LawRegistry (F = m*a)
├── synthesis/       # Data Synthesis Engine
├── validation/      # SelfCritic and Validation
├── investigation/   # 13-stage Investigation Loop
├── langbaby/        # LangBaby Structural Parser & Realizer
└── runtime/         # GILLM End-to-End Vertical Slice
```

---

## 5. QUICK START

### Installation:
```bash
pip install -e .
```

### Running Tests:
```bash
PYTHONPATH=. pytest
```

### Running End-to-End Vertical Slice Execution:
```python
from src.gillm.runtime.engine import GILLMRuntimeEngine

runtime = GILLMRuntimeEngine()
question = "Why does an object accelerate when a net force acts on it?"

res = runtime.execute_end_to_end(question, mass_kg=5.0, force_n=10.0)

print("User Question:", res["user_question"])
print("Final Answer:", res["final_answer"])
print("Validation Status:", res["validation_passed"])
```

---

## 6. LICENSE

Distributed under the MIT License. See `LICENSE` for more information.
