from typing import List
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.provenance.model import ProvenanceRecord
from src.gillm.core.enums import EpistemicStatus, ValidationStatus

class FusionEngine:
    """
    Constructs new scenario/molecule by fusing compatible scenario molecules.
    Preserves provenance and explicit constraints.
    """
    def fuse(self, molecule_a: DataMolecule, molecule_b: DataMolecule) -> DataMolecule:
        fused_id = f"fused_{molecule_a.molecule_id}_{molecule_b.molecule_id}"
        combined_atoms = {**molecule_a.atoms, **molecule_b.atoms}
        fused_state = {**molecule_a.state, **molecule_b.state}

        prov = ProvenanceRecord(
            source_id="SynthesisEngine.Fusion",
            transformation_type="FUSION",
            input_ids=[molecule_a.molecule_id, molecule_b.molecule_id]
        )

        return DataMolecule(
            molecule_id=fused_id,
            molecule_type="FUSED_SCENARIO",
            atoms=combined_atoms,
            state=fused_state,
            provenance=prov,
            epistemic_status=EpistemicStatus.SYNTHESIZED,
            validation_status=ValidationStatus.VALID
        )

class FissionEngine:
    """
    Decomposes a complex information structure / molecule into constituent molecules.
    Preserves provenance.
    """
    def fission(self, complex_molecule: DataMolecule) -> List[DataMolecule]:
        constituents = []
        for idx, (atom_id, atom) in enumerate(complex_molecule.atoms.items()):
            prov = ProvenanceRecord(
                source_id="SynthesisEngine.Fission",
                transformation_type="FISSION",
                input_ids=[complex_molecule.molecule_id]
            )
            sub_mol = DataMolecule(
                molecule_id=f"{complex_molecule.molecule_id}_constituent_{idx}",
                molecule_type="CONSTITUENT_MOLECULE",
                atoms={atom_id: atom},
                state={atom.atom_type: atom.value},
                provenance=prov,
                epistemic_status=EpistemicStatus.DERIVED,
                validation_status=ValidationStatus.VALID
            )
            constituents.append(sub_mol)
        return constituents
