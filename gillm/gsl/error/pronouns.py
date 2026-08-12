from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_2

def check_pronouns(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    # 1. Me went -> should be I went
    # If first word is 'me' and is followed by a verb
    if len(text_words) > 1 and text_words[0] == "me":
        if text_words[1] in ["went", "go", "goes", "opened", "saw", "eat", "eats", "ate"]:
            original_phrase = " ".join([t.text for t in tokens])
            corrected_tokens = [t.text for t in tokens]

            # Find and replace "me" at start
            for pos, t in enumerate(tokens):
                if t.text.lower() == "me" and pos == 0:
                    corrected_tokens[pos] = "I"
                    break

            suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
            errors.append(ErrorObject(
                error_type="PRONOUN_CASE",
                location="token_0",
                original=original_phrase,
                evidence=["Objective case pronoun 'me' located in subjective position as sentence subject."],
                candidates=[suggestion],
                status="HIGH_CONFIDENCE",
                reason="Pronoun case error: 'Me' -> 'I'",
                correction_level=LEVEL_2
            ))

    return errors
