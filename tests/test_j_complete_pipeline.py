from src.gillm.runtime.engine import GILLMRuntimeEngine

def test_j_complete_pipeline():
    """
    Test J — complete pipeline:
    Language -> LangBaby -> GIR -> Query Molecule -> 3D Registry ->
    transformation/information retrieval -> validation -> GIR -> LangBaby -> Language
    """
    runtime = GILLMRuntimeEngine()
    question = "Why does a car accelerate when a net force acts on it?"

    result = runtime.execute_end_to_end(question, mass_kg=5.0, force_n=10.0)

    assert result is not None
    assert result["validation_passed"] is True
    assert result["input_gir"]["intent"] == "QUESTION"
    assert len(result["investigation_stages"]) == 6
    assert result["output_gir"]["epistemic_status"] == "DERIVED"
    assert result["output_gir"]["validation_status"] == "VALID"
    assert "calculated acceleration is 2.0 m/s^2" in result["final_answer"]
