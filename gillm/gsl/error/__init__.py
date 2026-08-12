from gillm.gsl.error.correction import ErrorObject, LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, STANDARD, INFORMAL, NON_STANDARD, POSSIBLE_ERROR, UNKNOWN
from gillm.gsl.error.spelling import check_spelling
from gillm.gsl.error.missing_words import check_missing_words
from gillm.gsl.error.extra_words import check_extra_words
from gillm.gsl.error.word_order import check_word_order
from gillm.gsl.error.agreement import check_agreement
from gillm.gsl.error.tense import check_tense
from gillm.gsl.error.pronouns import check_pronouns
from gillm.gsl.error.determiners import check_determiners
from gillm.gsl.error.prepositions import check_prepositions
from gillm.gsl.error.auxiliaries import check_auxiliaries
from gillm.gsl.error.negation import check_negation
from gillm.gsl.error.punctuation import check_punctuation
from gillm.gsl.error.capitalization import check_capitalization
from gillm.gsl.error.sentence_boundary import check_sentence_boundaries
from gillm.gsl.error.semantic import check_semantics

def run_full_error_analysis(tokens, generator, scorer) -> list[ErrorObject]:
    """Runs all modular GSL 1.1 error checks and aggregates error results."""
    errors = []
    errors.extend(check_spelling(tokens, generator, scorer))
    errors.extend(check_missing_words(tokens))
    errors.extend(check_extra_words(tokens))
    errors.extend(check_word_order(tokens))
    errors.extend(check_agreement(tokens))
    errors.extend(check_tense(tokens))
    errors.extend(check_pronouns(tokens))
    errors.extend(check_determiners(tokens))
    errors.extend(check_prepositions(tokens))
    errors.extend(check_auxiliaries(tokens))
    errors.extend(check_negation(tokens))
    errors.extend(check_punctuation(tokens))
    errors.extend(check_capitalization(tokens))
    errors.extend(check_sentence_boundaries(tokens))
    errors.extend(check_semantics(tokens))
    return errors
