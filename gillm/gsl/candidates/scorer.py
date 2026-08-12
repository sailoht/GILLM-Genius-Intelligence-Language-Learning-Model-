from typing import List, Tuple
from gillm.gsl.lexicon.loader import LexiconLoader
from gillm.gsl.candidates.candidate import Candidate

def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def get_spelling_corrections(word: str, max_distance: int = 1) -> List[Tuple[str, float]]:
    word_lower = word.lower()
    lexicon = LexiconLoader.get_lexicon()
    local_lex = getattr(lexicon, "local_lexicon", None)
    if not local_lex:
        return []

    candidates: List[Tuple[str, float]] = []
    for entry in local_lex.get_all_entries():
        dist = levenshtein_distance(word_lower, entry.surface.lower())
        if dist <= max_distance:
            confidence = 1.0 - (dist / max_distance) * 0.5 if max_distance > 0 else 1.0
            candidates.append((entry.surface, confidence))

    return sorted(candidates, key=lambda x: x[1], reverse=True)


class LexicalScorer:
    def __init__(self) -> None:
        self.lexicon = LexiconLoader.get_lexicon()

    def score_lexical_candidates(self, candidates_grid: List[List[Candidate]]) -> List[List[Candidate]]:
        """
        Refines candidate scores based on:
        - Lexicon frequency
        - Part of speech priors (e.g. auxiliary, pronouns, determiners have high prior)
        """
        scored_grid: List[List[Candidate]] = []

        for token_candidates in candidates_grid:
            scored_token_candidates: List[Candidate] = []
            for cand in token_candidates:
                score = cand.score
                evidence = list(cand.evidence)

                # Prioritize based on lexicon frequency
                lex_entry = self.lexicon.lookup(cand.lemma)
                if lex_entry:
                    freq = lex_entry.frequency
                    # Add small boost proportional to frequency
                    freq_boost = (freq / 10.0) * 0.1  # Max frequency is 10
                    score += freq_boost
                    evidence.append(f"Lexical frequency boost: +{freq_boost:.2f}")

                # Minor boost for standard function words/PRON to help resolve ambiguous sentences
                if cand.pos in ["DET", "PRON", "AUX", "ADP"]:
                    score += 0.05
                    evidence.append("Function word prior boost: +0.05")

                # Normalize score to be between 0.0 and 1.0
                clamped_score = max(0.0, min(1.0, score))

                # Update candidate in place or return new
                scored_token_candidates.append(Candidate(
                    token=cand.token,
                    lemma=cand.lemma,
                    pos=cand.pos,
                    features=cand.features,
                    meaning=cand.meaning,
                    score=clamped_score,
                    evidence=evidence,
                    normalized_correction=cand.normalized_correction,
                    correction_confidence=cand.correction_confidence
                ))

            # Sort candidate analyses for this token in descending order of score
            scored_token_candidates.sort(key=lambda x: x.score, reverse=True)
            scored_grid.append(scored_token_candidates)

        return scored_grid
