from gillm.gsl.morphology.analyzer import MorphologicalAnalyzer

def test_morphological_analyzer():
    analyzer = MorphologicalAnalyzer()

    eats_analyses = analyzer.analyze("eats")
    assert any(a.lemma == "eat" and a.pos == "VERB" and a.features.get("tense") == "PRESENT" and a.features.get("number") == "SINGULAR" for a in eats_analyses)

    opened_analyses = analyzer.analyze("opened")
    assert any(a.lemma == "open" and a.pos == "VERB" and a.features.get("tense") == "PAST" for a in opened_analyses)

    went_analyses = analyzer.analyze("went")
    assert any(a.lemma == "go" and a.pos == "VERB" and a.features.get("tense") == "PAST" for a in went_analyses)

    duck_analyses = analyzer.analyze("duck")
    duck_pos = [a.pos for a in duck_analyses]
    assert "NOUN" in duck_pos
    assert "VERB" in duck_pos
