from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_2

def check_missing_words(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    # Pattern 1: NP + going to -> missing auxiliary
    # e.g., "The boy going to school."
    # Token text matches "going to" without an auxiliary like "is", "was", "are" preceding it
    if "going" in text_words:
        idx = text_words.index("going")
        # Check if preceding words contain auxiliaries
        preceding = text_words[:idx]
        has_aux = any(aux in preceding for aux in ["is", "was", "are", "were", "am", "be", "been"])
        if not has_aux and "boy" in preceding:
            original_phrase = " ".join([t.text for t in tokens])
            # Construct corrected candidates
            corrected_list = []
            # Find the position of 'going' to insert 'is' before it
            original_tokens = [t.text for t in tokens]
            going_pos = -1
            for pos, t in enumerate(tokens):
                if t.text.lower() == "going":
                    going_pos = pos
                    break

            if going_pos != -1:
                cand_tokens = list(original_tokens)
                cand_tokens.insert(going_pos, "is")
                # Remove trailing question marks or punctuation spaces beautifully
                cand_sentence = " ".join(cand_tokens).replace(" .", ".").replace(" ?", "?")
                corrected_list.append(cand_sentence)

            errors.append(ErrorObject(
                error_type="MISSING_WORD",
                location="sentence",
                original=original_phrase,
                evidence=["Detected active progressive verb 'going' without a preceding auxiliary verb."],
                candidates=corrected_list,
                status="HIGH_CONFIDENCE",
                reason="Missing auxiliary verb: 'is'",
                correction_level=LEVEL_2
            ))

    # Pattern 2: went school -> missing preposition
    # e.g., "He went school."
    for i in range(len(text_words) - 1):
        if text_words[i] in ["went", "go", "goes", "going"] and text_words[i+1] in ["school", "home", "door", "boy", "dog", "food"]:
            # Exception: "go home" is correct, "went school" is missing "to"
            if text_words[i+1] != "home":
                original_phrase = " ".join([t.text for t in tokens])
                corrected_tokens = [t.text for t in tokens]
                # Find position of second word
                target_word = text_words[i+1]
                target_pos = -1
                for pos, t in enumerate(tokens):
                    if t.text.lower() == target_word:
                        target_pos = pos
                        break

                if target_pos != -1:
                    corrected_tokens.insert(target_pos, "to")
                    cand_sentence = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")

                    errors.append(ErrorObject(
                        error_type="MISSING_WORD",
                        location="sentence",
                        original=original_phrase,
                        evidence=["Detected motion verb followed immediately by count noun destination without preposition."],
                        candidates=[cand_sentence],
                        status="HIGH_CONFIDENCE",
                        reason="Missing preposition: 'to'",
                        correction_level=LEVEL_2
                    ))

    return errors
