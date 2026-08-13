from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_2

def check_tense(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    if "yesterday" in text_words:
        for i, word in enumerate(text_words):
            if word == "go":
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]
                for pos, t in enumerate(tokens):
                    if t.text.lower() == "go":
                        corrected_tokens[pos] = "went"

                suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
                errors.append(ErrorObject(
                    error_type="TENSE_INCONSISTENCY",
                    location=f"token_{tokens[i].position}",
                    original=original_phrase,
                    evidence=["Detected past temporal modifier 'Yesterday' paired with present tense verb 'go'."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason="Tense inconsistency: 'go' -> 'went'",
                    correction_level=LEVEL_2
                ))
            elif word == "eat":
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]
                for pos, t in enumerate(tokens):
                    if t.text.lower() == "eat":
                        corrected_tokens[pos] = "ate"

                suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
                errors.append(ErrorObject(
                    error_type="TENSE_INCONSISTENCY",
                    location=f"token_{tokens[i].position}",
                    original=original_phrase,
                    evidence=["Detected past temporal modifier 'Yesterday' paired with present tense verb 'eat'."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason="Tense inconsistency: 'eat' -> 'ate'",
                    correction_level=LEVEL_2
                ))

    return errors
