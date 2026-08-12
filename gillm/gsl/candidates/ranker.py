from typing import List, Optional
from gillm.input.models import Token
from gillm.gsl.candidates.candidate import Candidate
from gillm.gsl.morphology.analyzer import MorphologicalAnalyzer
from gillm.gsl.lexicon.loader import LexiconLoader
from gillm.gsl.candidates.scorer import get_spelling_corrections

class CandidateGenerator:
    def __init__(self) -> None:
        self.morphology_analyzer = MorphologicalAnalyzer()
        self.lexicon = LexiconLoader.get_lexicon()

    def generate_candidates(self, tokens: List[Token]) -> List[List[Candidate]]:
        all_token_candidates: List[List[Candidate]] = []

        for token in tokens:
            token_candidates: List[Candidate] = []
            word = token.text

            # For punctuation/numbers/symbols, return direct candidates without spelling correction
            if token.token_type != "WORD":
                lex_entry = self.lexicon.lookup(word)
                pos = "PUNCT" if token.token_type == "PUNCTUATION" else token.token_type
                meaning = lex_entry.definition if lex_entry else "Punctuation or symbol"
                token_candidates.append(Candidate(
                    token=token,
                    lemma=word,
                    pos=pos,
                    features={},
                    meaning=meaning,
                    score=1.0,
                    evidence=["Direct match for non-word token"]
                ))
                all_token_candidates.append(token_candidates)
                continue

            analyses = self.morphology_analyzer.analyze(word)
            is_known = any(not a.features.get("unknown", False) for a in analyses)

            if is_known:
                for analysis in analyses:
                    lex_entry = self.lexicon.lookup(analysis.lemma)
                    meaning = lex_entry.definition if lex_entry else ""

                    token_candidates.append(Candidate(
                        token=token,
                        lemma=analysis.lemma,
                        pos=analysis.pos,
                        features=analysis.features,
                        meaning=meaning,
                        score=1.0,
                        evidence=["Exact morphological match"]
                    ))
            else:
                corrections = get_spelling_corrections(word, max_distance=2)
                corrections = [c for c in corrections if c[0].lower() != word.lower()]

                if corrections:
                    for corrected_word, confidence in corrections:
                        corrected_analyses = self.morphology_analyzer.analyze(corrected_word)
                        for analysis in corrected_analyses:
                            lex_entry = self.lexicon.lookup(analysis.lemma)
                            meaning = lex_entry.definition if lex_entry else ""

                            token_candidates.append(Candidate(
                                token=token,
                                lemma=analysis.lemma,
                                pos=analysis.pos,
                                features=analysis.features,
                                meaning=meaning,
                                score=0.8 * confidence,
                                evidence=[f"Typo correction candidate '{corrected_word}' with confidence {confidence:.2f}"],
                                normalized_correction=corrected_word,
                                correction_confidence=confidence
                            ))

                for analysis in analyses:
                    token_candidates.append(Candidate(
                        token=token,
                        lemma=analysis.lemma,
                        pos=analysis.pos,
                        features=analysis.features,
                        meaning="Unknown word fallback",
                        score=0.2,
                        evidence=["Unknown word fallback"]
                    ))

            all_token_candidates.append(token_candidates)

        return all_token_candidates

class CandidateRanker:
    """Combines lexical, morphological, syntax and semantic scoring for complete structures."""
    pass
