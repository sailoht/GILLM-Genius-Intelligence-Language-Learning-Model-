from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Optional, Tuple
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.molecules.atom import DataAtom
from src.gillm.vectors.model import Vector
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
    """
    LawRegistry manages law discovery, applicability analysis, and deterministic execution.
    Target contract: State_{t+1} = T(State_t, Law, Context)
    """
    def __init__(self):
        self.laws: Dict[str, ExecutableLaw] = {}
        self.register_default_laws()

    def register_law(self, law: ExecutableLaw):
        self.laws[law.law_id] = law

    def get_law(self, law_id: str) -> Optional[ExecutableLaw]:
        return self.laws.get(law_id)

    def find_applicable_laws(self, input_obj: Any) -> List[ExecutableLaw]:
        applicable = []
        for law in self.laws.values():
            try:
                if law.condition(input_obj):
                    applicable.append(law)
            except Exception:
                continue
        return applicable

    def register_default_laws(self):
        # 1. Newton's 2nd Law (F = ma => a = F/m)
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

                f_id = getattr(f_atom, 'id', 'f1')
                m_id = getattr(m_atom, 'id', 'm1')

                prov = ProvenanceRecord(
                    source="LAW_EXECUTION",
                    rule_used="Newton's Second Law (F = m*a)",
                    inputs_used=[f_id, m_id]
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
                    transformation="LAW_EXECUTION",
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

        # 2. Universal Gravity Kinematics State Transition Law
        def gravity_cond(arg: Any) -> bool:
            if isinstance(arg, DataMolecule):
                return "position" in arg.vector_state or "velocity" in arg.vector_state
            return False

        def gravity_trans(arg: Any) -> Any:
            if isinstance(arg, DataMolecule):
                pos = arg.vector_state.get("position", Vector([0.0, 0.0, 0.0]))
                vel = arg.vector_state.get("velocity", Vector([0.0, 0.0, 0.0]))
                acc = arg.vector_state.get("acceleration", Vector([0.0, 0.0, -9.81]))
                dt = arg.state.get("dt", 1.0)

                new_vel = vel + acc * dt
                new_pos = pos + vel * dt + 0.5 * acc * (dt ** 2)

                prov = ProvenanceRecord(
                    source="GRAVITY_LAW",
                    transformation="LAW_EXECUTION",
                    rule_used="Kinematics State Transition",
                    inputs_used=[arg.id]
                )

                new_mol = DataMolecule(
                    id=f"{arg.id}_t1",
                    type=arg.type,
                    name=arg.name,
                    data_atoms=dict(arg.data_atoms),
                    state={**arg.state, "t": arg.state.get("t", 0.0) + dt},
                    vector_state={
                        "position": new_pos,
                        "velocity": new_vel,
                        "acceleration": acc
                    },
                    spatial_position=new_pos.to_tuple(),
                    provenance=prov,
                    epistemic_status=EpistemicStatus.DERIVED,
                    validation_status=ValidationStatus.VALID,
                    laws=arg.laws + ["KinematicsStateTransition"]
                )
                return new_mol
            return None

        self.register_law(ExecutableLaw("NewtonsSecondLaw", "Newton's Second Law (F = m*a)", f_ma_cond, f_ma_trans))
        self.register_law(ExecutableLaw("LAW_NEWTON_2ND", "Newton's Second Law (F = m*a)", f_ma_cond, f_ma_trans))
        self.register_law(ExecutableLaw("LAW_F_MA", "Newton's Second Law (F = m*a)", f_ma_cond, f_ma_trans))
        self.register_law(ExecutableLaw("GravityKinematicsLaw", "Gravity Kinematics Law", gravity_cond, gravity_trans))

    def execute_applicable_laws(self, input_molecule: DataMolecule) -> DataMolecule:
        current = input_molecule
        for law in self.find_applicable_laws(current):
            res = law.transformation(current)
            if isinstance(res, DataMolecule):
                current = res
        return current
