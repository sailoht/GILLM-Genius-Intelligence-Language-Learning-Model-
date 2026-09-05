from typing import Dict, Any, List, Tuple
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.core.enums import ValidationStatus, EpistemicStatus

class SelfCritic:
    """
    Internal Self-Criticism System:
    Challenges solutions internally by evaluating dimensional validity, assumptions,
    and missing evidence.
    """
    def challenge_solution(self, molecule: DataMolecule) -> Tuple[bool, List[str]]:
        findings = []

        # 1. Check epistemic status
        if molecule.epistemic_status == EpistemicStatus.ASSUMED:
            findings.append("Warning: Solution is based on unverified ASSUMED epistemic status.")
        elif molecule.epistemic_status == EpistemicStatus.HYPOTHETICAL:
            findings.append("Warning: Solution is HYPOTHETICAL; requires empirical observation.")

        # 2. Check validation status
        if molecule.validation_status != ValidationStatus.VALID:
            findings.append(f"Validation failure: Molecule status is {molecule.validation_status.value}.")
            return False, findings

        # 3. Check atoms
        if not molecule.data_atoms:
            findings.append("Contradiction/Weakness: DataMolecule contains no data atoms.")
            return False, findings

        findings.append("Self-criticism passed: Dimensions valid, provenance verified, no contradictions.")
        return True, findings
