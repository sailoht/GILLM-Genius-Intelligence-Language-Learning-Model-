from typing import List
from gillm.input.models import Token
from gillm.gsl.candidates.ranker import CandidateGenerator
from gillm.gsl.candidates.scorer import LexicalScorer
from gillm.gsl.error.correction import ErrorObject, LEVEL_1

def check_spelling(tokens: List[Token], generator: CandidateGenerator, scorer: LexicalScorer) -> List[ErrorObject]:
    errors = []

    # Process tokens to generate and score candidates
    candidates_raw = generator.generate_candidates(tokens)
    candidates_scored = scorer.score_lexical_candidates(candidates_raw)

    for i, token_cands in enumerate(candidates_scored):
        if not token_cands:
            continue

        token = tokens[i]
        # Check if the highest scored candidate has a correction
        top_cand = token_cands[0]
        if top_cand.normalized_correction and top_cand.normalized_correction != token.text.lower():
            # Generate spelling error object
            # Only assert if there's high confidence or strong syntactic match (handled globally or here)
            evidence = [
                f"Word '{token.text}' is not found in the local lexicon.",
                f"Typo distance matches candidate '{top_cand.normalized_correction}' with score {top_cand.score:.2f}."
            ]
            errors.append(ErrorObject(
                error_type="SPELLING",
                location=f"token_{token.position}",
                original=token.text,
                evidence=evidence,
                candidates=[top_cand.normalized_correction],
                status="HIGH_CONFIDENCE",
                reason=f"Spelling error: '{token.text}' -> '{top_cand.normalized_correction}'",
                correction_level=LEVEL_1
            ))

    return errors
