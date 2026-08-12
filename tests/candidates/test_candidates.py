from gillm.input.tokenizer import Tokenizer
from gillm.gsl.candidates.ranker import CandidateGenerator

def test_candidate_generation_with_typo():
    tokenizer = Tokenizer()
    generator = CandidateGenerator()

    tokens = tokenizer.tokenize("hte boy")
    assert len(tokens) == 2

    candidates_list = generator.generate_candidates(tokens)
    hte_candidates = candidates_list[0]

    the_cand = [c for c in hte_candidates if c.lemma == "the"]
    assert len(the_cand) > 0
    assert the_cand[0].normalized_correction == "the"
    assert the_cand[0].pos == "DET"
    assert the_cand[0].score >= 0.4
