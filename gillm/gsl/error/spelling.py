from typing import List
from gillm.input.models import Token
from gillm.gsl.candidates.ranker import CandidateGenerator
from gillm.gsl.candidates.scorer import LexicalScorer, get_spelling_corrections
from gillm.gsl.error.correction import ErrorObject, LEVEL_1
from gillm.gsl.lexicon.loader import LexiconLoader

def check_spelling(tokens: List[Token], generator: CandidateGenerator, scorer: LexicalScorer) -> List[ErrorObject]:
    errors = []
    lexicon = LexiconLoader.get_lexicon()

    candidates_raw = generator.generate_candidates(tokens)
    candidates_scored = scorer.score_lexical_candidates(candidates_raw)

    for i, token_cands in enumerate(candidates_scored):
        if not token_cands:
            continue

        token = tokens[i]
        top_cand = token_cands[0]
        if top_cand.normalized_correction and top_cand.normalized_correction != token.text.lower():
            # Get all spelling corrections for this token
            raw_corrections = get_spelling_corrections(token.text, max_distance=2)
            raw_corrections = [c for c in raw_corrections if c[0].lower() != token.text.lower()]

            # Apply contextual syntax boost
            boosted_corrections = []
            for word_cand, confidence in raw_corrections:
                score = confidence

                # Look up POS candidates of the spelling correction
                cand_entry = lexicon.lookup(word_cand)
                cand_pos_list = cand_entry.pos_candidates if cand_entry else []

                # Check surrounding context
                # If next word is NOUN, boost DET candidates
                if i < len(tokens) - 1:
                    next_token = tokens[i+1]
                    next_entry = lexicon.lookup(next_token.text)
                    next_pos_list = next_entry.pos_candidates if next_entry else []

                    if "NOUN" in next_pos_list:
                        if "DET" in cand_pos_list:
                            score += 0.5  # Strong boost for DET + NOUN compatibility
                        if "PRON" in cand_pos_list:
                            score -= 0.3  # Penalty for PRON + NOUN compatibility

                boosted_corrections.append((word_cand, score))

            # Re-sort spelling correction candidates
            boosted_corrections.sort(key=lambda x: x[1], reverse=True)
            sorted_candidates = [c[0] for c in boosted_corrections]

            evidence = [
                f"Word '{token.text}' is not found in the local lexicon.",
                f"Applied context syntax-prior check: DET followed by NOUN is supported, PRON is penalized.",
                f"Sorted spelling candidates based on syntax compatibility: {sorted_candidates}."
            ]
            errors.append(ErrorObject(
                error_type="SPELLING",
                location=f"token_{token.position}",
                original=token.text,
                evidence=evidence,
                candidates=sorted_candidates,
                status="HIGH_CONFIDENCE",
                reason=f"Spelling error: '{token.text}' -> '{sorted_candidates[0]}'",
                correction_level=LEVEL_1
            ))

    return errors
