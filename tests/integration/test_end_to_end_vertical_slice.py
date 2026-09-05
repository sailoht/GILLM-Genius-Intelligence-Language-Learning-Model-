from src.gillm.runtime.engine import GILLMRuntimeEngine

def test_end_to_end_vertical_slice():
    runtime = GILLMRuntimeEngine()
    question = "Why does an object accelerate when a net force acts on it?"

    # Run end-to-end execution slice
    res = runtime.execute_end_to_end(question, mass_kg=5.0, force_n=10.0)

    assert res is not None
    assert res["validation_passed"] is True
    assert res["input_gir"]["intent"] in ["QUESTION", "STATEMENT"]
    assert len(res["investigation_stages"]) == 6
    assert res["output_gir"]["epistemic_status"] == "DERIVED"
    assert res["output_gir"]["validation_status"] == "VALID"
    assert "calculated acceleration is 2.0 m/s^2" in res["final_answer"]
