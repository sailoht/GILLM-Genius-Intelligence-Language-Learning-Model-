# Genius Intelligence Representation (GIR) Specification

`GIR` is the common internal contract representation between LangBaby and GILLM.

```text
Language
   ↕
 GIR
   ↕
GILLM
```

## Structure Fields:
*   `id`: Stable unique identifier
*   `intent`: Query/Statement intent classification
*   `entities`: List of tracked entities
*   `concepts`: List of domain concepts
*   `properties`: Key-value property map
*   `relations`: Typed structural relations
*   `events`: Event sequences
*   `observations`: Physical measurements and observations
*   `actions`: Executable action plans
*   `goals`: Targeted goals
*   `spatial_info`: 3D coordinates and spatial configuration
*   `temporal_info`: Time markers and sequence history
*   `causality`: Causal relationships
*   `epistemic_status`: Current epistemic classification
*   `validation_status`: Validation state
*   `provenance`: Derivation trace graph
