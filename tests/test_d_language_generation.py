from src.gillm.langbaby.parser.structural_parser import LangBabyStructuralParser
from src.gillm.langbaby.realization.structural_realizer import LangBabyStructuralRealizer

def test_d_language_generation():
    """
    Test D — language generation:
    Structured GIR -> grammatically valid sentence.
    """
    parser = LangBabyStructuralParser()
    realizer = LangBabyStructuralRealizer()

    gir = parser.parse_text_to_gir("The car accelerates because a net force acts on it.")
    text = realizer.realize_gir_to_text(gir)

    assert text is not None
    assert isinstance(text, str)
    assert len(text) > 0
    assert "car accelerates" in text or "net force" in text
