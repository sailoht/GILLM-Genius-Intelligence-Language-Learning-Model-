import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional, Tuple
from src.gillm.core.enums import EpistemicStatus, ValidationStatus
from src.gillm.molecules.atom import DataAtom
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.provenance.model import ProvenanceRecord
from src.gillm.physics.units import UNIT_MASS, UNIT_FORCE, UNIT_ACCELERATION

@dataclass
class ExecutableLaw:
    """
    Formal representation of a law as an executable object:
    Law = (Conditions, Inputs, Transformation, Outputs, Validation, ValidityDomain)
    """
    name: str
    conditions: List[str]
    inputs: List[str]   # e.g., ["force", "mass"]
    outputs: List[str]  # e.g., ["acceleration"]
    transformation_fn: Callable[[Dict[str, DataAtom]], Tuple[DataAtom, bool]]
    validity_domain: Dict[str, Any] = field(default_factory=dict)

class LawRegistry:
    """Registry for formal physical/domain laws allowing registration, execution, and validation."""
    def __init__(self) -> None:
        self.laws: Dict[str, ExecutableLaw] = {}
        self._register_default_laws()

    def register(self, law: ExecutableLaw) -> None:
        self.laws[law.name] = law

    def get_law(self, name: str) -> Optional[ExecutableLaw]:
        return self.laws.get(name)

    def _register_default_laws(self) -> None:
        # Newton's Second Law: F = m * a  =>  a = F / m
        def newton_second_law_fn(atoms: Dict[str, DataAtom]) -> Tuple[DataAtom, bool]:
            f_atom = atoms.get("force")
            m_atom = atoms.get("mass")
            if not f_atom or not m_atom or m_atom.value == 0:
                raise ValueError("Newton's second law requires non-zero mass and force atoms.")

            accel_val = f_atom.value / m_atom.value

            # Dimensional validation check: N / kg = m/s^2
            dim_valid = (f_atom.unit in ["N", "kg*m/s^2"] and m_atom.unit == "kg")

            prov = ProvenanceRecord(
                source="LAW_EXECUTION",
                transformation="a = F / m",
                rule_used="Newton's Second Law (F = m*a)",
                inputs_used=[f_atom.id, m_atom.id]
            )

            output_atom = DataAtom(
                id=f"atom_accel_{int(time.time()*1000)}",
                type="measurement",
                value=accel_val,
                unit="m/s^2",
                provenance=prov
            )
            return output_atom, dim_valid

        newton_law = ExecutableLaw(
            name="NewtonsSecondLaw",
            conditions=["classical_mechanics_domain", "non_relativistic"],
            inputs=["force", "mass"],
            outputs=["acceleration"],
            transformation_fn=newton_second_law_fn,
            validity_domain={"max_velocity": 3e7}  # v < 0.1c
        )
        self.register(newton_law)
