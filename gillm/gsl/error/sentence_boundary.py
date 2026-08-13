from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_2

def check_sentence_boundaries(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    pron_indices = [i for i, w in enumerate(text_words) if w == "i"]
    if len(pron_indices) >= 2:
        original_phrase = " ".join([t.text for t in tokens])
        corrected_tokens = [t.text for t in tokens]

        inserted_count = 0
        for idx in pron_indices[1:]:
            pos_to_insert = idx + inserted_count
            corrected_tokens.insert(pos_to_insert, ".")
            inserted_count += 1

        suggestion = " ".join(corrected_tokens).replace(" .", ".").replace(" ?", "?")
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
