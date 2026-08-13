from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_1

def check_capitalization(tokens: List[Token]) -> List[ErrorObject]:
    errors = []

    if not tokens:
        return errors

    first_token = tokens[0]
    if first_token.token_type == "WORD" and first_token.text and not first_token.text[0].isupper():
        original_phrase = " ".join([t.text for t in tokens]).replace(" .", ".").replace(" ?", "?")
        corrected_tokens = [t.text for t in tokens]
        corrected_tokens[0] = corrected_tokens[0][0].upper() + corrected_tokens[0][1:]

        suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")

        errors.append(ErrorObject(
            error_type="MISSING_CAPITALIZATION",
            location="token_0",
            original=original_phrase,
            evidence=["Sentence-initial token is a word but does not start with a capitalized letter."],
            candidates=[suggestion],
            status="HIGH_CONFIDENCE",
            reason="Missing sentence capitalization",
            correction_level=LEVEL_1
        ))

    return errors
