from src.gillm.langbaby.parser.structural_parser import LangBabyStructuralParser

def test_b_equivalent_phrasing():
    """
    Test B — equivalent phrasing:
    "The ball was kicked by the boy." -> related underlying meaning
    """
    parser = LangBabyStructuralParser()
    gir = parser.parse_text_to_gir("The ball was kicked by the boy.")

    assert gir is not None
    entity_names = [e["name"] for e in gir.entities]
    assert "boy" in entity_names
    assert "ball" in entity_names
    assert len(gir.events) == 1
    assert gir.events[0]["event"] == "kick"
    assert gir.events[0]["agent"] == "boy"
    assert gir.events[0]["patient"] == "ball"
    assert gir.events[0]["voice"] == "PASSIVE"
