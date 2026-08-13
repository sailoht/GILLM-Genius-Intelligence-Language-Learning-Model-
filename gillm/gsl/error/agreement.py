from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_2

def check_agreement(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    for i in range(len(text_words) - 1):
        subj = text_words[i]
        verb = text_words[i+1]

        if subj in ["he", "she", "it", "boy", "dog"]:
            if verb == "go":
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]
                for pos, t in enumerate(tokens):
                    if t.text.lower() == "go" and pos > 0 and tokens[pos-1].text.lower() == subj:
                        corrected_tokens[pos] = "goes"

                suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
                errors.append(ErrorObject(
                    error_type="SUBJECT_VERB_AGREEMENT",
                    location=f"token_{tokens[i+1].position}",
                    original=original_phrase,
                    evidence=[f"Subject '{subj}' is Third-Person Singular, but verb '{verb}' is in base/plural form."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason="Subject-verb agreement error: 'go' -> 'goes'",
                    correction_level=LEVEL_2
                ))
            elif verb == "eat":
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]
                for pos, t in enumerate(tokens):
                    if t.text.lower() == "eat" and pos > 0 and tokens[pos-1].text.lower() == subj:
                        corrected_tokens[pos] = "eats"
                suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
                errors.append(ErrorObject(
                    error_type="SUBJECT_VERB_AGREEMENT",
                    location=f"token_{tokens[i+1].position}",
                    original=original_phrase,
                    evidence=[f"Subject '{subj}' is Third-Person Singular, but verb '{verb}' is in base/plural form."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason="Subject-verb agreement error: 'eat' -> 'eats'",
                    correction_level=LEVEL_2
                ))

        elif subj in ["they", "we", "you", "i"]:
            if verb == "goes":
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]
                for pos, t in enumerate(tokens):
                    if t.text.lower() == "goes" and pos > 0 and tokens[pos-1].text.lower() == subj:
                        corrected_tokens[pos] = "go"
                suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
                errors.append(ErrorObject(
                    error_type="SUBJECT_VERB_AGREEMENT",
                    location=f"token_{tokens[i+1].position}",
                    original=original_phrase,
                    evidence=[f"Subject '{subj}' is plural/non-3SG, but verb '{verb}' is in Third-Person Singular form."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason="Subject-verb agreement error: 'goes' -> 'go'",
                    correction_level=LEVEL_2
                ))
            elif verb == "eats":
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]
                for pos, t in enumerate(tokens):
                    if t.text.lower() == "eats" and pos > 0 and tokens[pos-1].text.lower() == subj:
                        corrected_tokens[pos] = "eat"
                suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
                errors.append(ErrorObject(
                    error_type="SUBJECT_VERB_AGREEMENT",
                    location=f"token_{tokens[i+1].position}",
                    original=original_phrase,
                    evidence=[f"Subject '{subj}' is plural/non-3SG, but verb '{verb}' is in Third-Person Singular form."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason="Subject-verb agreement error: 'eats' -> 'eat'",
                    correction_level=LEVEL_2
                ))

    # 2. Number / Plural Agreement checks
    for i in range(len(text_words) - 1):
        determiner = text_words[i]
        noun = text_words[i+1]

        if determiner in ["two", "three", "many", "these", "those"]:
            if noun in ["book", "boy", "dog", "door"]:
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]
                for pos, t in enumerate(tokens):
                    if t.text.lower() == noun and pos > 0 and tokens[pos-1].text.lower() == determiner:
                        corrected_tokens[pos] = noun + "s"

                suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
                errors.append(ErrorObject(
                    error_type="NUMBER_AGREEMENT",
                    location=f"token_{tokens[i+1].position}",
                    original=original_phrase,
                    evidence=[f"Plural determiner/quantifier '{determiner}' paired with singular count noun '{noun}'."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason=f"Number agreement error: '{noun}' -> '{noun}s'",
                    correction_level=LEVEL_2
                ))

        elif determiner in ["one", "a", "an", "this", "that"]:
            if noun in ["books", "boys", "dogs", "doors"]:
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]
                for pos, t in enumerate(tokens):
                    if t.text.lower() == noun and pos > 0 and tokens[pos-1].text.lower() == determiner:
                        corrected_tokens[pos] = noun[:-1]

                suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
                errors.append(ErrorObject(
                    error_type="NUMBER_AGREEMENT",
                    location=f"token_{tokens[i+1].position}",
                    original=original_phrase,
                    evidence=[f"Singular determiner/quantifier '{determiner}' paired with plural count noun '{noun}'."],
                    candidates=[suggestion],
                    status="HIGH_CONFIDENCE",
                    reason=f"Number agreement error: '{noun}' -> '{noun[:-1]}'",
                    correction_level=LEVEL_2
                ))

    return errors
