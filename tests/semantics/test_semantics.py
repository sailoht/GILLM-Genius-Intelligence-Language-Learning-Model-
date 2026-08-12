from gillm.input.tokenizer import Tokenizer
from gillm.gsl.candidates.ranker import CandidateGenerator
from gillm.gsl.candidates.scorer import LexicalScorer
from gillm.gsl.syntax.matcher import ChartParser
from gillm.gsl.semantics.roles import SemanticRoleResolver

def test_semantic_role_resolver():
    tokenizer = Tokenizer()
    generator = CandidateGenerator()
    scorer = LexicalScorer()
    parser = ChartParser()
    resolver = SemanticRoleResolver()

    # Test "The boy opened the door."
    tokens = [t for t in tokenizer.tokenize("The boy opened the door.") if t.token_type == "WORD"]
    candidates = scorer.score_lexical_candidates(generator.generate_candidates(tokens))
    tree = parser.parse(candidates)[0]

    roles = resolver.resolve(tree)
    assert roles["action"] == "open"
    assert roles["agent"] == "boy"
    assert roles["patient"] == "door"
