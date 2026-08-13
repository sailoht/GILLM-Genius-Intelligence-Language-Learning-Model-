from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_2

def check_negation(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    for i in range(len(text_words) - 2):
        if text_words[i] in ["didn't", "don't", "doesn't"] and text_words[i+1] in ["have", "see", "want"] and text_words[i+2] in ["no", "nothing"]:
            original_phrase = " ".join([t.text for t in tokens])
            corrected_tokens = [t.text for t in tokens]

            for pos, t in enumerate(tokens):
                if t.text.lower() == "no" and pos == i+2:
                    corrected_tokens[pos] = "any"
                elif t.text.lower() == "nothing" and pos == i+2:
                    corrected_tokens[pos] = "anything"

            suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
            errors.append(ErrorObject(
                error_type="DOUBLE_NEGATION",
                location=f"token_{tokens[i+2].position}",
                original=original_phrase,
                evidence=["Detected double negation structure ('didn't' + 'no'/'nothing'). Standard English prefers single negation."],
                candidates=[suggestion],
                status="POSSIBLE",
                reason="Double negation: 'no' -> 'any'",
                correction_level=LEVEL_2
            ))

    return errors
