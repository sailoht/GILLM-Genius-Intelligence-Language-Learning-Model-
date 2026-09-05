from src.gillm.langbaby.parser.structural_parser import LangBabyStructuralParser
from src.gillm.langbaby.realization.structural_realizer import LangBabyStructuralRealizer

def test_langbaby_structural_parsing():
    parser = LangBabyStructuralParser()
    text = "The car accelerates because a net force acts on it."

    gir = parser.parse_text_to_gir(text)

    assert gir is not None
    assert gir.intent == "STATEMENT"
    assert len(gir.entities) >= 1
    assert gir.entities[0]["name"] == "car"
    assert len(gir.causality) == 1
    assert gir.causality[0]["relation"] == "CAUSED_BY"

def test_langbaby_realization():
    parser = LangBabyStructuralParser()
    realizer = LangBabyStructuralRealizer()

    text = "The car accelerates because a net force acts on it."
    gir = parser.parse_text_to_gir(text)
    out_text = realizer.realize_gir_to_text(gir)

    assert "car accelerates" in out_text
    assert "net force acts on it" in out_text
