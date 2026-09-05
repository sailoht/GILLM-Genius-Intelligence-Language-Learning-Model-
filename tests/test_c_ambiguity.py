from src.gillm.langbaby.parser.structural_parser import LangBabyStructuralParser

def test_c_ambiguity():
    """
    Test C — ambiguity:
    "I saw the man with the telescope." -> multiple explicit interpretations
    """
    parser = LangBabyStructuralParser()
    gir = parser.parse_text_to_gir("I saw the man with the telescope.")

    assert gir is not None
    assert gir.ambiguity_flag is True
    assert len(gir.interpretations) >= 2
    # Interpretation 1: PP attached to NOUN
    # Interpretation 2: PP attached to VERB (instrument)
    assert any("patient_modifier" in interp for interp in gir.interpretations)
    assert any("instrument" in interp for interp in gir.interpretations)
