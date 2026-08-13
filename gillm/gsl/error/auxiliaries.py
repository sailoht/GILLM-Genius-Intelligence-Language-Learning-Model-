from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_2

def check_auxiliaries(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    if len(text_words) >= 4 and text_words[0] in ["did", "didn't"]:
        for i, word in enumerate(text_words):
            if word == "went" and i >= 2:
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]
                for pos, t in enumerate(tokens):
                    if t.text.lower() == "went":
                        corrected_tokens[pos] = "go"

                suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
                errors.append(ErrorObject(
                    error_type="AUXILIARY_DOUBLE_PAST",
                    location=f"token_{tokens[i].position}",
                    original=original_phrase,
                    evidence=["Detected past auxiliary 'did' combined with past inflected main verb 'went'. Auxiliary carries past, verb must be base form."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason="Double past auxiliary violation: 'went' -> 'go'",
                    correction_level=LEVEL_2
                ))

    for i in range(len(text_words) - 1):
        if text_words[i] in ["didn't", "did not"] and text_words[i+1] == "went":
            original_phrase = " ".join([t.text for t in tokens])
            corrected_tokens = [t.text for t in tokens]
            for pos, t in enumerate(tokens):
                if t.text.lower() == "went" and pos > 0 and tokens[pos-1].text.lower() in ["didn't", "not"]:
                    corrected_tokens[pos] = "go"

            suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
            errors.append(ErrorObject(
                error_type="AUXILIARY_DOUBLE_PAST",
                location=f"token_{tokens[i+1].position}",
                original=original_phrase,
                evidence=["Detected past negation auxiliary 'didn't' combined with past inflected main verb 'went'."],
                candidates=[suggestion],
                status="HIGH_CONFIDENCE",
                reason="Double past auxiliary violation: 'didn't went' -> 'didn't go'",
                correction_level=LEVEL_2
            ))

    return errors
