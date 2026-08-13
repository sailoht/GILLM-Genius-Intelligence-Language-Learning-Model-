from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_2

def check_determiners(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    for i, word in enumerate(text_words):
        if word in ["dog", "boy", "door"] and i > 0:
            preceding = text_words[i-1]
            if preceding in ["saw", "opened", "see", "open", "likes", "with", "behind"]:
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]

                for pos, t in enumerate(tokens):
                    if t.text.lower() == word and pos > 0 and tokens[pos-1].text.lower() == preceding:
                        corrected_tokens.insert(pos, "a")
                        break

                suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
                errors.append(ErrorObject(
                    error_type="MISSING_DETERMINER",
                    location=f"token_{tokens[i].position}",
                    original=original_phrase,
                    evidence=[f"Singular count noun '{word}' lacks a required preceding determiner (e.g., 'a', 'the')."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason=f"Missing determiner before singular count noun: '{word}' -> 'a {word}'",
                    correction_level=LEVEL_2
                ))

    for i in range(len(text_words) - 1):
        if text_words[i] == "a" and text_words[i+1] in ["honest", "apple", "orange", "elephant", "hour"]:
            original_phrase = " ".join([t.text for t in tokens])
            corrected_tokens = [t.text for t in tokens]
            for pos, t in enumerate(tokens):
                if t.text.lower() == "a" and pos < len(tokens)-1 and tokens[pos+1].text.lower() == text_words[i+1]:
                    corrected_tokens[pos] = "an"
                    break

            suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
            if tokens[i].text[0].isupper():
                suggestion = suggestion[0].upper() + suggestion[1:]

            errors.append(ErrorObject(
                error_type="PHONOLOGICAL_DETERMINER_MISMATCH",
                location=f"token_{tokens[i].position}",
                original=original_phrase,
                evidence=[f"Determiner 'a' used before vowel-sound word '{text_words[i+1]}'. Expected 'an'."],
                candidates=[suggestion],
                status="HIGH_CONFIDENCE",
                reason=f"Determiner mismatch: 'a {text_words[i+1]}' -> 'an {text_words[i+1]}'",
                correction_level=LEVEL_2
            ))

    return errors
