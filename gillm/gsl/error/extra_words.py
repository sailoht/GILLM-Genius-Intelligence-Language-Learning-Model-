from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_1

def check_extra_words(tokens: List[Token]) -> List[ErrorObject]:
    errors = []

    for i in range(len(tokens) - 1):
        t1 = tokens[i]
        t2 = tokens[i+1]

        if t1.token_type == "WORD" and t2.token_type == "WORD":
            if t1.text.lower() == t2.text.lower():
                original_phrase = " ".join([t.text for t in tokens])

                suggestion_tokens = [t.text for pos, t in enumerate(tokens) if pos != i+1]
                suggestion = " ".join(suggestion_tokens).replace(" .", ".").replace(" ?", "?")

                errors.append(ErrorObject(
                    error_type="EXTRA_WORD",
                    location=f"token_{t2.position}",
                    original=original_phrase,
                    evidence=[f"Detected duplicate adjacent word '{t1.text}' at index {t1.position} and {t2.position}."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason=f"Extra duplicate word: '{t2.text}'",
                    correction_level=LEVEL_1
                ))

    return errors
