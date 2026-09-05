# Core Design Principles of GILLM & LangBaby

## 1. NO NEXT-TOKEN PREDICTION
The core intelligence and language generation in GILLM are **NOT** built around $P(\text{token}_t \mid \text{token}_1 \dots \text{token}_{t-1})$ autoregressive neural generation.

Language generation is based on explicit structural construction:
```
Word → Phrase → Proposition → Sentence → Paragraph → Section → Document
```

## 2. NO-ILLUSION PRINCIPLE
Nothing becomes an asserted fact without a valid state path and proof-carrying derivation provenance.

### Epistemic Status:
*   `OBSERVED`: Directly witnessed facts.
*   `DEFINED`: Axiomatically defined.
*   `IMPORTED`: Loaded from external data sources.
*   `DERIVED`: Mathematically/algebraically derived from laws.
*   `SYNTHESIZED`: Constructed via multi-source synthesis.
*   `HYPOTHETICAL`: Assumed for scenario evaluation.
*   `ASSUMED`: Unverified assumption.
*   `UNKNOWN`: Insufficient information.
*   `INVALID`: Contradicted or mathematically failed.
*   `CONTRADICTED`: Falsified by counter-evidence.

### Validation Status:
*   `VALID`, `INVALID`, `UNVERIFIED`, `CONTRADICTED`.

## 3. UNKNOWN IS A FIRST-CLASS STATE
`UNKNOWN != FAILURE`. If the system cannot establish something from available information, it represents that explicitly rather than fabricating proselike hallucinations.
