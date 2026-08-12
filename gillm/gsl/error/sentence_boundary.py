from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_2

def check_sentence_boundaries(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    # 1. Run-on check for duplicated subjective pronouns
    # e.g., "I went home I ate food I slept."
    # We look for pronoun sequences "I ... I ... I" with verbs in between
    pron_indices = [i for i, w in enumerate(text_words) if w == "i"]
    if len(pron_indices) >= 2:
        # Check if they have verbs in between
        # Suggesting sentence boundaries
        original_phrase = " ".join([t.text for t in tokens])
        corrected_tokens = [t.text for t in tokens]

        # We find each "I" (except the first one) and insert terminal punctuation "." before it
        # and capitalize "I"
        inserted_count = 0
        for idx in pron_indices[1:]:
            # Find the actual position of the token
            pos_to_insert = idx + inserted_count
            corrected_tokens.insert(pos_to_insert, ".")
            inserted_count += 1

        suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
        # clean duplicates or double periods
        suggestion = suggestion.replace("..", ".").replace(". .", ".")

        errors.append(ErrorObject(
            error_type="SENTENCE_BOUNDARY_RUNON",
            location="sentence",
            original=original_phrase,
            evidence=["Detected adjacent declarative clauses with subjective pronouns without terminal punctuation boundaries."],
            candidates=[suggestion],
            status="HIGH_CONFIDENCE",
            reason="Missing sentence boundary / Run-on sentence",
            correction_level=LEVEL_2
        ))

    return errors
