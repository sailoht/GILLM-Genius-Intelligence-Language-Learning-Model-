# GILLM 0.5.0 Architecture & Principles

## Principles
1. **No Next-Token Prediction**: Language understanding and state synthesis are structural and compositional.
2. **Language is Not Intelligence**: LangBaby handles human communication while GILLM Core models the world, laws, space, and time.
3. **DataMolecule Identity Invariant**: DataMolecule identity is stable and independent from its mutable state. InformationSet membership is identity-based and must not depend on hashing the mutable DataMolecule object.
4. **Epistemic vs Validation Status**:
   - Epistemic: `OBSERVED`, `DERIVED`, `SYNTHESIZED`, `HYPOTHETICAL`, `ASSUMED`, `UNKNOWN`.
   - Validation: `VALID`, `INVALID`, `UNVERIFIED`, `CONTRADICTED`.
5. **State Transition Engine**: $S_{t+1} = T(S_t, \text{Law}, \text{Context})$ operates over `InformationSet` collections and `Vector` state representations with proof-carrying provenance.
