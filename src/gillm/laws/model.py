from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Optional, Tuple
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.molecules.atom import DataAtom
from src.gillm.physics.units import QuantityUnit
from src.gillm.provenance.model import ProvenanceRecord
from src.gillm.core.enums import EpistemicStatus, ValidationStatus

@dataclass
class ExecutableLaw:
    law_id: str
    name: str
    condition: Callable[[Any], bool]
    transformation: Callable[[Any], Any]

    @property
    def transformation_fn(self) -> Callable[[Any], Any]:
        return self.transformation

class LawRegistry:
    def __init__(self):
        self.laws: Dict[str, ExecutableLaw] = {}
        self.register_default_laws()

    def register_law(self, law: ExecutableLaw):
        self.laws[law.law_id] = law

    def get_law(self, law_id: str) -> Optional[ExecutableLaw]:
        return self.laws.get(law_id)

    def register_default_laws(self):
        def f_ma_cond(arg: Any) -> bool:
            if isinstance(arg, DataMolecule):
                return "mass" in arg.atoms and "force" in arg.atoms
            elif isinstance(arg, dict):
                return "mass" in arg and "force" in arg
            return False

        def f_ma_trans(arg: Any) -> Any:
            if isinstance(arg, dict):
                m_atom = arg["mass"]
                f_atom = arg["force"]
                m_val = m_atom.value
                f_val = f_atom.value
                a_val = f_val / m_val if m_val != 0 else 0.0

                m_unit = QuantityUnit.from_string(m_atom.unit or "kg")
                f_unit = QuantityUnit.from_string(f_atom.unit or "N")
                a_unit_derived = f_unit / m_unit
                expected_a_unit = QuantityUnit(0, 1, -2) # m/s^2
                dim_valid = (a_unit_derived == expected_a_unit)

                prov = ProvenanceRecord(
                    source="LAW_EXECUTION",
                    rule_used="Newton's Second Law (F = m*a)",
                    inputs_used=["m_in", "f_in"] if hasattr(m_atom, 'id') else ["mass", "force"]
                )

                accel_atom = DataAtom(
                    id="a_derived",
                    type="acceleration",
                    value=a_val,
                    unit=str(a_unit_derived),
                    provenance=prov
                )
                return accel_atom, dim_valid
            elif isinstance(arg, DataMolecule):
                m_val = arg.atoms["mass"].value
                f_val = arg.atoms["force"].value
                a_val = f_val / m_val if m_val != 0 else 0.0

                prov = ProvenanceRecord(
                    source="LAW_EXECUTION",
                    rule_used="Newton's Second Law (F = m*a)",
                    inputs_used=["mass", "force"]
                )

                acc_atom = DataAtom(id="acc_1", type="ACCELERATION", value=a_val, unit="m/s^2", provenance=prov)
                new_atoms = {**arg.atoms, "acceleration": acc_atom}

                return DataMolecule(
                    id=f"derived_{arg.id}",
                    type="DERIVED_PHYSICAL_STATE",
                    atoms=new_atoms,
                    state={**arg.state, "acceleration": a_val},
                    spatial_position=arg.spatial_position,
                    provenance=prov,
                    epistemic_status=EpistemicStatus.DERIVED,
                    validation_status=ValidationStatus.VALID
                )
            return None

        law_newton = ExecutableLaw(
            law_id="NewtonsSecondLaw",
            name="Newton's Second Law (F = m*a)",
            condition=f_ma_cond,
            transformation=f_ma_trans
        )
        self.register_law(law_newton)
        self.register_law(ExecutableLaw("LAW_NEWTON_2ND", "Newton's Second Law (F = m*a)", f_ma_cond, f_ma_trans))
        self.register_law(ExecutableLaw("LAW_F_MA", "Newton's Second Law (F = m*a)", f_ma_cond, f_ma_trans))

    def execute_applicable_laws(self, input_molecule: DataMolecule) -> DataMolecule:
        current = input_molecule
        for law in self.laws.values():
            if law.condition(current):
                res = law.transformation(current)
                if isinstance(res, DataMolecule):
                    current = res
        return current
