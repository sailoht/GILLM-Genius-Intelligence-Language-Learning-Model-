from gillm.gsl.lexicon.loader import LexiconLoader

def test_lexicon_lookup():
    lexicon = LexiconLoader.get_lexicon()
    entry = lexicon.lookup("boy")
    assert entry is not None
    assert entry.lemma == "boy"
    assert "NOUN" in entry.pos_candidates
    assert entry.semantic_categories == ["PERSON"]

    entry_null = lexicon.lookup("nonexistentwordxyz")
    assert entry_null is None
