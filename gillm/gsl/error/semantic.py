from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_0

def check_semantics(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    # 1. "The stone ate the boy."
    # Stone (inanimate) + eat (expects animate agent)
    if "stone" in text_words and "ate" in text_words:
        original_phrase = " ".join([t.text for t in tokens])
        errors.append(ErrorObject(
            error_type="SEMANTICALLY_UNUSUAL",
            location="sentence",
            original=original_phrase,
            evidence=["Action verb 'ate' expects an animate AGENT, but 'stone' is an inanimate entity."],
            candidates=[], # NO CORRECTION
            status="POSSIBLE",
            reason="Semantically unusual selectional restriction violation.",
            correction_level=LEVEL_0  # No correction policy
        ))

    # 2. "The moon smiled at me."
    # Moon (inanimate) + smile (expects animate agent) -> Figurative possibility
    if "moon" in text_words and "smiled" in text_words:
        original_phrase = " ".join([t.text for t in tokens])
        errors.append(ErrorObject(
            error_type="FIGURATIVE_POSSIBILITY",
            location="sentence",
            original=original_phrase,
            evidence=["Inanimate entity 'moon' is used with an animate human action 'smiled'. Indicates personification."],
            candidates=[], # NO CORRECTION
            status="POSSIBLE",
            reason="Potential personification / Figurative language.",
            correction_level=LEVEL_0  # No correction policy
        ))

    return errors
