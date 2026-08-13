from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_1

def check_punctuation(tokens: List[Token]) -> List[ErrorObject]:
    errors = []

    if not tokens:
        return errors

    last_token = tokens[-1]
    if last_token.token_type != "PUNCTUATION":
        original_phrase = " ".join([t.text for t in tokens])
        text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]
        is_question = False
        if text_words:
            if text_words[0] in ["who", "what", "where", "why", "did", "was", "were", "is", "does"]:
                is_question = True

        punc = "?" if is_question else "."
        suggestion = original_phrase + punc

        errors.append(ErrorObject(
            error_type="MISSING_PUNCTUATION",
            location=f"token_{last_token.position}",
            original=original_phrase,
            evidence=[f"Sentence lacks terminal punctuation. Sentence structure indicates a {'question' if is_question else 'statement'}."],
            candidates=[suggestion],
            status="HIGH_CONFIDENCE",
            reason=f"Missing terminal punctuation: expected '{punc}'",
            correction_level=LEVEL_1
        ))

    return errors
