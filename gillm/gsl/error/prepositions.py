from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_3

def check_prepositions(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    for i in range(len(text_words) - 2):
        if text_words[i] == "good" and text_words[i+1] == "in" and text_words[i+2] in ["mathematics", "math", "sports", "english"]:
            original_phrase = " ".join([t.text for t in tokens])
            corrected_tokens = [t.text for t in tokens]

            for pos, t in enumerate(tokens):
                if t.text.lower() == "in" and pos > 0 and tokens[pos-1].text.lower() == "good" and pos < len(tokens)-1 and tokens[pos+1].text.lower() in ["mathematics", "math", "sports", "english"]:
                    corrected_tokens[pos] = "at"
                    break

            suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
            errors.append(ErrorObject(
                error_type="PREPOSITION_USAGE",
                location=f"token_{tokens[i+1].position}",
                original=original_phrase,
                evidence=["Detected collocation 'good in' before academic discipline or subject. Standard dialect prefers 'good at'."],
                candidates=[suggestion],
                status="POSSIBLE",
                reason="Preposition collocation warning: 'good in' -> 'good at'",
                correction_level=LEVEL_3
            ))

    return errors
