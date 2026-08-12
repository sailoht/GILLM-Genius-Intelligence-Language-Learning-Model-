from gillm.input.tokenizer import Tokenizer
from gillm.gsl.candidates.ranker import CandidateGenerator
from gillm.gsl.candidates.scorer import LexicalScorer
from gillm.gsl.syntax.matcher import ChartParser
from gillm.gsl.semantics.roles import SemanticRoleResolver
from gillm.gsl.questions.answer_slots import QuestionPhaser

def test_question_phaser_who():
    tokenizer = Tokenizer()
    generator = CandidateGenerator()
    scorer = LexicalScorer()
    parser = ChartParser()
    resolver = SemanticRoleResolver()
    phaser = QuestionPhaser()

    # "Who opened the door?"
    # Note: punctuation like "?" at the end is stripped for the core syntactic phrase, but let's test how tokenizer handles it.
    tokens = [t for t in tokenizer.tokenize("Who opened the door?") if t.token_type == "WORD"]
    candidates = scorer.score_lexical_candidates(generator.generate_candidates(tokens))
    tree = parser.parse(candidates)[0]

    roles = resolver.resolve(tree)
    q_info = phaser.phase_question(tree, roles)

    assert q_info is not None
    assert q_info["question_family"] == "WHO"
    assert q_info["expected_answer"] == "PERSON"
    assert q_info["missing_role"] == "agent"

def test_question_phaser_yes_no():
    tokenizer = Tokenizer()
    generator = CandidateGenerator()
    scorer = LexicalScorer()
    parser = ChartParser()
    resolver = SemanticRoleResolver()
    phaser = QuestionPhaser()

    # "Did the dog eat food?"
    tokens = [t for t in tokenizer.tokenize("Did the dog eat food?") if t.token_type == "WORD"]
    candidates = scorer.score_lexical_candidates(generator.generate_candidates(tokens))
    tree = parser.parse(candidates)[0]

    roles = resolver.resolve(tree)
    q_info = phaser.phase_question(tree, roles)

    assert q_info is not None
    assert q_info["question_family"] == "YES_NO"
    assert q_info["expected_answer"] == "BOOLEAN"
    assert q_info["missing_role"] is None
