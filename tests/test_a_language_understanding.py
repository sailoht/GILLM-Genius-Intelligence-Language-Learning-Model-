from src.gillm.langbaby.parser.structural_parser import LangBabyStructuralParser

def test_a_language_understanding():
    """
    Test A — language understanding:
    "The boy kicked the ball." -> structural interpretation (ENTITY boy, ENTITY ball, EVENT kick)
    """
    parser = LangBabyStructuralParser()
    gir = parser.parse_text_to_gir("The boy kicked the ball.")

    assert gir is not None
    assert gir.intent == "STATEMENT"
    entity_names = [e["name"] for e in gir.entities]
    assert "boy" in entity_names
    assert "ball" in entity_names
    assert len(gir.events) == 1
    assert gir.events[0]["event"] == "kick"
    assert gir.events[0]["agent"] == "boy"
    assert gir.events[0]["patient"] == "ball"
