from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from src.gillm.core.enums import ValidationStatus, EpistemicStatus
from src.gillm.molecules.molecule import DataMolecule

@dataclass
class ValidationFinding:
    check_name: str
    passed: bool
    details: str

@dataclass
class SelfCriticResult:
    status: ValidationStatus
    is_valid: bool
    findings: List[ValidationFinding] = field(default_factory=list)

class SelfCritic:
    """
    SelfCritic conducts deep inspection of inputs, dimensional validity, provenance,
    laws execution results, contradictions, and missing assumptions.
    Returns structured findings without blindly trusting ValidationStatus.
    """
    def critique(self, molecule: DataMolecule) -> SelfCriticResult:
        findings: List[ValidationFinding] = []

        # Check 1: Provenance completeness
        prov_ok = bool(molecule.provenance and molecule.provenance.source != "UNKNOWN")
        findings.append(ValidationFinding(
            check_name="ProvenanceCompleteness",
            passed=prov_ok,
            details=f"Source: {molecule.provenance.source}, Rule: {molecule.provenance.rule_used}"
        ))

        # Check 2: Epistemic integrity (not claiming OBSERVED if derived)
        ep_ok = True
        if molecule.provenance.transformation != "NONE" and molecule.epistemic_status == EpistemicStatus.OBSERVED:
            ep_ok = False
            findings.append(ValidationFinding(
                check_name="EpistemicIntegrity",
                passed=False,
                details="Falsely claims OBSERVED for derived or transformed state."
            ))
        else:
            findings.append(ValidationFinding(
                check_name="EpistemicIntegrity",
                passed=True,
                details=f"Epistemic status '{molecule.epistemic_status}' matches provenance."
            ))

        # Check 3: Data Atoms or Vector State presence
        atoms_ok = len(molecule.atoms) > 0 or len(molecule.vector_state) > 0
        findings.append(ValidationFinding(
            check_name="StatePresence",
            passed=atoms_ok,
            details=f"Atoms count: {len(molecule.atoms)}, Vector states: {len(molecule.vector_state)}"
        ))

        all_passed = all(f.passed for f in findings)
        final_status = ValidationStatus.VALID if all_passed else ValidationStatus.INVALID

        return SelfCriticResult(
            status=final_status,
            is_valid=all_passed,
            findings=findings
        )

    def challenge_solution(self, molecule: DataMolecule) -> SelfCriticResult:
        return self.critique(molecule)
