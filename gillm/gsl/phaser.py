import json
from typing import List, Dict, Any, Tuple, Optional
from gillm.input.manager import InputManager
from gillm.gsl.candidates.ranker import CandidateGenerator
from gillm.gsl.candidates.scorer import LexicalScorer
from gillm.gsl.syntax.matcher import ChartParser
from gillm.gsl.semantics.roles import SemanticRoleResolver
from gillm.gsl.questions.answer_slots import QuestionPhaser
from gillm.intent.classifier import IntentClassifier
from gillm.gsl.trace.phase_trace import PhaseTrace
from gillm.gsl.gcpr.models import (
    GCPR, SurfaceRepresentation, LinguisticRepresentation,
    SemanticRepresentation, ConversationRepresentation, UncertaintyRepresentation
)

# GSL 1.1 Error System Imports
from gillm.gsl.error import run_full_error_analysis
from gillm.gsl.error.validator import BidirectionalValidator
from gillm.gsl.grammar.rules import (
    analyze_temporal_relations, analyze_discourse_relations,
    resolve_speech_act, get_figurative_language_extensions,
    get_exercise_system_extensions
)

def score_complete_parse(tree, resolved_roles: Dict[str, Any]) -> float:
    """
    Linguistically scores a complete parse tree structure based on syntax and semantic coherence.
    """
    score = tree.score

    # 1. Auxiliary penalty: Prefer auxiliary verbs like "do", "be", "have" to act as Aux
    # rather than main lexical verbs when another action verb is present in the sentence.
    main_verb = resolved_roles.get("action")
    if main_verb in ["do", "be", "have"]:
        leaves = tree.get_leaves()
        other_verbs = [l for l in leaves if l.pos == "VERB" and l.lemma not in ["do", "be", "have"]]
        if other_verbs:
            score -= 0.3  # Penalize treating auxiliary as main verb

    # 2. Structural Question preference
    if tree.label == "S_Q":
        score += 0.05

    return score

class GSLPhaser:
    def __init__(self) -> None:
        self.input_manager = InputManager()
        self.candidate_generator = CandidateGenerator()
        self.lexical_scorer = LexicalScorer()
        self.parser = ChartParser()
        self.role_resolver = SemanticRoleResolver()
        self.question_phaser = QuestionPhaser()
        self.bidirectional_validator = BidirectionalValidator(self)
        self._in_validation = False

    def phase(self, text: str, context: Optional[Any] = None) -> Tuple[GCPR, PhaseTrace]:
        trace = PhaseTrace()
        trace.log_input(text)

        tokens = self.input_manager.process_input(text)
        tokens_str = " | ".join([t.text for t in tokens])
        trace.log_tokenization(tokens_str)

        word_tokens = [t for t in tokens if t.token_type == "WORD"]

        candidates_raw = self.candidate_generator.generate_candidates(word_tokens)
        candidates_scored = self.lexical_scorer.score_lexical_candidates(candidates_raw)

        morph_log_lines = []
        lex_log_lines = []
        for i, token_cands in enumerate(candidates_scored):
            word_text = word_tokens[i].text
            morph_log_lines.append(f"{word_text}:")
            for c in token_cands:
                feats_str = ", ".join([f"{k}={v}" for k, v in c.features.items()])
                morph_log_lines.append(f"  -> lemma='{c.lemma}', pos={c.pos}, features={{{feats_str}}}")
                lex_log_lines.append(f"Word: '{word_text}' matched lemma '{c.lemma}' with POS candidate {c.pos}. Meaning: {c.meaning}")
        trace.log_morphology("\n".join(morph_log_lines))
        trace.log_lexicon("\n".join(lex_log_lines))

        parses = self.parser.parse(candidates_scored)

        syntax_log_lines = []
        for p in parses:
            syntax_log_lines.append(p.pretty_format())
        trace.log_syntax("\n".join(syntax_log_lines) if syntax_log_lines else "No valid parses found!")

        errors_found = run_full_error_analysis(tokens, self.candidate_generator, self.lexical_scorer)

        tracked_entities = {}
        for token_cands in candidates_scored:
            for c in token_cands:
                if c.pos == "NOUN" and c.lemma not in ["unknown", "duck", "stone"]:
                    tracked_entities[c.lemma.lower()] = {
                        "lemma": c.lemma,
                        "status": "PRESERVED_FOR_FUTURE_COREFERENCE",
                        "pos": "NOUN"
                    }

        if not parses:
            surface = SurfaceRepresentation(original_text=text, tokens=[{"text": t.text, "type": t.token_type} for t in tokens])
            empty_gcpr = GCPR(surface=surface)
            empty_gcpr.uncertainty.confidence = 0.0

            gcpr_dict = empty_gcpr.to_dict()
            gcpr_dict["gsl_version"] = "1.1"
            gcpr_dict["gcpr_version"] = "0.5"
            gcpr_dict["gillm_version"] = "0.5.0"
            gcpr_dict["errors"] = [e.to_dict() for e in errors_found]
            gcpr_dict["semantic"]["entities"] = tracked_entities

            # GSL 1.1 extra fields on fallback:
            gcpr_dict["temporal_relations"] = analyze_temporal_relations(text)
            gcpr_dict["discourse_relations"] = analyze_discourse_relations(text)
            gcpr_dict["speech_act"] = resolve_speech_act(text, "statement")
            gcpr_dict["figurative_language"] = get_figurative_language_extensions(text, errors_found)
            gcpr_dict["exercises"] = get_exercise_system_extensions(gcpr_dict)

            trace.log_semantics("No valid parse found. UNKNOWN output.")
            trace.log_gcpr(json.dumps(gcpr_dict, indent=2))

            empty_gcpr.extra_fields = gcpr_dict
            return empty_gcpr, trace

        interpretations: List[Dict[str, Any]] = []
        for idx, tree in enumerate(parses):
            resolved_roles = self.role_resolver.resolve(tree)

            sentence_type = "statement"
            if tree.label == "S_Q":
                sentence_type = "question"
            elif tree.label == "S_E":
                sentence_type = "exclamation"

            action = resolved_roles.get("action", "")
            trace.log_verb_frame(f"Action: {action} -> expectation frame role slots resolved from tree.")

            q_family = None
            expected_answer = None
            if sentence_type == "question":
                q_info = self.question_phaser.phase_question(tree, resolved_roles)
                if q_info:
                    q_family = q_info["question_family"]
                    expected_answer = q_info["expected_answer"]

            surface_data = SurfaceRepresentation(
                original_text=text,
                tokens=[{"text": t.text, "type": t.token_type} for t in tokens]
            )

            polarity = "POSITIVE"
            if "did not" in text.lower() or "does not" in text.lower() or "is not" in text.lower():
                polarity = "NEGATIVE"

            tense = tree.features.get("tense", "PRESENT")
            voice = tree.features.get("voice", "ACTIVE")

            linguistic_data = LinguisticRepresentation(
                sentence_type=sentence_type,
                morphology=tree.features,
                grammar={"tense": tense, "polarity": polarity},
                syntax={"voice": voice, "labels": tree.label}
            )

            semantic_data = SemanticRepresentation(
                roles=resolved_roles,
                entities=dict(tracked_entities),
                relations=[]
            )

            conv_data = ConversationRepresentation(
                role=None,
                question_family=q_family,
                expected_answer=expected_answer
            )

            gcpr_candidate = GCPR(
                surface=surface_data,
                linguistic=linguistic_data,
                semantic=semantic_data,
                conversation=conv_data,
                intent=None,
                uncertainty=UncertaintyRepresentation(confidence=tree.score)
            )

            intent_val = IntentClassifier.classify(gcpr_candidate.to_dict())
            gcpr_candidate.intent = intent_val

            final_score = score_complete_parse(tree, resolved_roles)

            interpretations.append({
                "gcpr": gcpr_candidate,
                "score": final_score
            })

        interpretations.sort(key=lambda x: x["score"], reverse=True)

        best_gcpr = interpretations[0]["gcpr"]
        best_score = interpretations[0]["score"]

        threshold = 0.15
        alternatives: List[Dict[str, Any]] = []
        is_ambiguous = False

        for item in interpretations[1:]:
            if abs(best_score - item["score"]) <= threshold:
                is_ambiguous = True
                alternatives.append(item["gcpr"].to_dict())

        best_gcpr.uncertainty.ambiguous = is_ambiguous
        best_gcpr.uncertainty.alternatives = alternatives

        if context:
            gcpr_dict = best_gcpr.to_dict()
            resolved_dict = context.resolve_coreferences(gcpr_dict)
            best_gcpr.semantic.entities.update(resolved_dict["semantic"]["entities"])

        temporal_rel = analyze_temporal_relations(text)
        discourse_rel = analyze_discourse_relations(text)

        speech_act = resolve_speech_act(text, best_gcpr.linguistic.sentence_type)

        fig_lang = get_figurative_language_extensions(text, errors_found)

        exercise_data = get_exercise_system_extensions(best_gcpr.to_dict())

        final_dict = best_gcpr.to_dict()
        final_dict["gsl_version"] = "1.1"
        final_dict["gcpr_version"] = "0.5"
        final_dict["gillm_version"] = "0.5.0"

        final_dict["speech_act"] = speech_act
        final_dict["temporal_relations"] = temporal_rel
        final_dict["discourse_relations"] = discourse_rel
        final_dict["errors"] = [e.to_dict() for e in errors_found]
        final_dict["figurative_language"] = fig_lang
        final_dict["exercises"] = exercise_data

        # 7. Run Bidirectional Validation with Recursion Guard
        if not self._in_validation:
            self._in_validation = True
            try:
                is_consistent, val_notes = self.bidirectional_validator.validate_structural_consistency(best_gcpr)
            finally:
                self._in_validation = False
        else:
            is_consistent = True
            val_notes = ["Skipped nested validation to prevent infinite recursion."]

        final_dict["bidirectional_validation"] = {
            "consistent": is_consistent,
            "notes": val_notes
        }

        best_gcpr.extra_fields = final_dict

        roles_str = ", ".join([f"{k} = {v}" for k, v in best_gcpr.semantic.roles.items()])
        trace.log_semantics(roles_str)
        trace.log_gcpr(json.dumps(final_dict, indent=2))

        return best_gcpr, trace
