from src.gillm.sets.model import InformationSet
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.vectors.model import Vector
from src.gillm.laws.model import LawRegistry
from src.gillm.state.engine import StateTransitionEngine

def test_vector_state_transition():
    """
    Integration Test proving:
    SET -> contains OBJECTS -> OBJECT has VECTOR STATE -> LAW applies ->
    VECTOR/STATE changes -> transition recorded -> provenance recorded -> validation succeeds.
    """
    ball = DataMolecule(
        id="ball_1",
        type="PHYSICAL_OBJECT",
        name="Ball",
        vector_state={
            "position": Vector([0.0, 0.0, 10.0]),
            "velocity": Vector([0.0, 0.0, 0.0]),
            "acceleration": Vector([0.0, 0.0, -9.81])
        },
        state={"dt": 1.0, "t": 0.0}
    )

    obj_set = InformationSet("PhysicsWorldSet", [ball])
    engine = StateTransitionEngine()

    res = engine.step_set(obj_set)

    assert len(res.resulting_set) == 1
    new_ball = list(res.resulting_set)[0]

    assert new_ball.vector_state["velocity"] == Vector([0.0, 0.0, -9.81])
    assert new_ball.vector_state["position"] == Vector([0.0, 0.0, 10.0 - 0.5 * 9.81])
    assert len(res.transitions) == 1
    assert res.transitions[0].action == "Gravity Kinematics Law"
    assert new_ball.provenance.source == "GRAVITY_LAW"
    assert res.critic_results[0].is_valid is True
