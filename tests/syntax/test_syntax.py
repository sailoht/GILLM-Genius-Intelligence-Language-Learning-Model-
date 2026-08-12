from gillm.input.tokenizer import Tokenizer
from gillm.gsl.candidates.ranker import CandidateGenerator
from gillm.gsl.candidates.scorer import LexicalScorer
from gillm.gsl.syntax.matcher import ChartParser

def test_chart_parser():
    tokenizer = Tokenizer()
    generator = CandidateGenerator()
    scorer = LexicalScorer()
    parser = ChartParser()

    tokens = tokenizer.tokenize("The boy opened the door.")
    # Exclude punctuation from tokens for simplified syntax matching if we want to match exact patterns,
    # or let the parser handle it. Wait, the tokenizer output has "." at the end.
    # In GSL 1.0, punctuation is optional for the syntax rules, so we can filter out "." before parsing.
    word_tokens = [t for t in tokens if t.token_type == "WORD"]

    candidates = generator.generate_candidates(word_tokens)
    scored_candidates = scorer.score_lexical_candidates(candidates)

    parses = parser.parse(scored_candidates)

    assert len(parses) > 0
    # At least one parse should be of category "S"
    assert any(p.label == "S" for p in parses)

    # Check that children form Det + Noun as NP, Verb + NP as VP
    s_parse = [p for p in parses if p.label == "S"][0]
    assert len(s_parse.children) == 2
    assert s_parse.children[0].label == "NP"
    assert s_parse.children[1].label == "VP"
