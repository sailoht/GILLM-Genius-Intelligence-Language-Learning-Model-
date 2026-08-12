from typing import List, Optional
from gillm.gsl.morphology.models import MorphologicalAnalysis
from gillm.gsl.morphology.irregular import IRREGULAR_PAST_PARTICIPLE, IRREGULAR_PLURALS
from gillm.gsl.morphology.rules import apply_suffix_rules
from gillm.gsl.lexicon.loader import LexiconLoader

class MorphologicalAnalyzer:
    def __init__(self) -> None:
        self.lexicon = LexiconLoader.get_lexicon()

    def analyze(self, word: str) -> List[MorphologicalAnalysis]:
        word_lower = word.lower()
        analyses: List[MorphologicalAnalysis] = []
        seen = set()

        def add_analysis(lemma: str, pos: str, features: dict):
            key = (lemma, pos, tuple(sorted(features.items())))
            if key not in seen:
                seen.add(key)
                analyses.append(MorphologicalAnalysis(lemma=lemma, pos=pos, features=features))

        # 1. Direct Lookup in Lexicon
        lex_entry = self.lexicon.lookup(word_lower)
        if lex_entry:
            for pos in lex_entry.pos_candidates:
                features = dict(lex_entry.morphological_features)
                if pos == "NOUN" and "number" not in features:
                    features["number"] = "SINGULAR"
                elif pos == "VERB" and "tense" not in features:
                    features["tense"] = "PRESENT"
                add_analysis(lex_entry.lemma, pos, features)

        # 2. Check Irregular Past/Participles
        if word_lower in IRREGULAR_PAST_PARTICIPLE:
            lemma, feats = IRREGULAR_PAST_PARTICIPLE[word_lower]
            lex_entry = self.lexicon.lookup(lemma)
            pos_list = lex_entry.pos_candidates if lex_entry else ["VERB"]
            for pos in pos_list:
                add_analysis(lemma, pos, feats.copy())

        # 3. Check Irregular Plurals
        if word_lower in IRREGULAR_PLURALS:
            lemma = IRREGULAR_PLURALS[word_lower]
            lex_entry = self.lexicon.lookup(lemma)
            pos_list = lex_entry.pos_candidates if lex_entry else ["NOUN"]
            for pos in pos_list:
                add_analysis(lemma, pos, {"number": "PLURAL"})

        # 4. Apply Suffix Rules (Lexicon-verified first)
        rule_candidates = apply_suffix_rules(word_lower)
        for lemma, suggested_pos, features in rule_candidates:
            lex_entry = self.lexicon.lookup(lemma)
            if lex_entry:
                for pos in lex_entry.pos_candidates:
                    if pos == suggested_pos:
                        feats = features.copy()
                        add_analysis(lex_entry.lemma, pos, feats)

        # 5. Fallback for out-of-lexicon words:
        if not analyses:
            for lemma, suggested_pos, features in rule_candidates:
                add_analysis(lemma, suggested_pos, features)

        # 6. Absolute default fallback
        if not analyses:
            add_analysis(word_lower, "NOUN", {"number": "SINGULAR", "unknown": True})
            add_analysis(word_lower, "VERB", {"tense": "PRESENT", "unknown": True})

        return analyses
