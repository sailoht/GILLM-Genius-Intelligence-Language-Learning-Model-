from typing import List
from gillm.input.models import Token
from gillm.gsl.error.correction import ErrorObject, LEVEL_2

def check_word_order(tokens: List[Token]) -> List[ErrorObject]:
    errors = []
    text_words = [t.text.lower() for t in tokens if t.token_type == "WORD"]

    # Pattern: Why you did go there? -> Wh-adv + Subject Pronoun + Aux
    # We want Wh-adv + Aux + Subject Pronoun
    # Standard: why, where, what, who, when, how
    if len(text_words) >= 3:
        if text_words[0] in ["why", "where", "what", "who", "when", "how"]:
            # Check if second word is a subject pronoun or NP like 'you', 'the boy', 'dog'
            # and third word is an auxiliary like 'did', 'does', 'do', 'is', 'was', 'were'
            if text_words[1] in ["you", "i", "he", "she", "they", "we", "the", "boy", "dog"]:
                if text_words[2] in ["did", "does", "do", "is", "was", "were", "can", "could", "should", "will", "would"]:
                    original_phrase = " ".join([t.text for t in tokens])

                    # Swap index 1 and 2
                    suggestion_tokens = [t.text for t in tokens]

                    # Find positions of words at text_words[1] and text_words[2]
                    # Since tokens may contain punctuation, find the actual word indices
                    word_indices = [idx for idx, t in enumerate(tokens) if t.token_type == "WORD"]
                    if len(word_indices) >= 3:
                        pos1 = word_indices[1]
                        pos2 = word_indices[2]
                        # Swap
                        suggestion_tokens[pos1], suggestion_tokens[pos2] = suggestion_tokens[pos2], suggestion_tokens[pos1]

                    suggestion = " ".join(suggestion_tokens).replace(" .", ".").replace(" ?", "?")

                    # Capitalize first word of suggestion if original was capitalized
                    if tokens[0].text[0].isupper():
                        suggestion = suggestion[0].upper() + suggestion[1:]

                    errors.append(ErrorObject(
                        error_type="WORD_ORDER",
                        location="sentence",
                        original=original_phrase,
                        evidence=[
                            "Detected interrogative pronoun/adverb followed directly by subject and auxiliary.",
                            "Standard English interrogative syntax requires subject-auxiliary inversion (AUX + SUBJECT + VERB)."
                        ],
                        candidates=[suggestion],
                        status="HIGH_CONFIDENCE",
                        reason=f"Word order error: '{text_words[1]} {text_words[2]}' -> '{text_words[2]} {text_words[1]}'",
                        correction_level=LEVEL_2
                    ))

    return errors
