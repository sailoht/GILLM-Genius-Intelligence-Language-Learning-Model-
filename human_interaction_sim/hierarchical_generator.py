import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional
from human_interaction_sim.dynamics import SimulationEngine

@dataclass
class ParagraphState:
    topic: str
    current_subtopic: str
    semantic_direction: np.ndarray
    unresolved_information: List[str] = field(default_factory=list)
    completed_information: List[str] = field(default_factory=list)
    interaction_velocity: float = 1.0
    projected_next_direction: np.ndarray = field(default_factory=lambda: np.array([1.0, 0.0]))

@dataclass
class SubwordCandidate:
    prefix: str
    suffix: str
    word: str
    score: float

class HierarchicalLanguageGenerator:
    """
    Implements a hierarchical, non-LLM rule-based language generation pipeline:
    Concept -> Subword Candidates -> Word -> Phrase -> Sentence -> Paragraph State -> Paragraph.
    Controlled via physics-inspired dynamics (velocity, direction, friction).
    """
    def __init__(self) -> None:
        self.subword_dictionary = {
            "quant": ["um", "ization", "ity"],
            "mechan": ["ics", "ical", "ism"],
            "wave": ["function", "length", "guide"],
            "part": ["icle", "icular", "ition"],
            "probab": ["ility", "le", "ly"],
            "barr": ["ier", "icade"],
            "tunnel": ["ing", "ed"]
        }

        self.phrase_graph = {
            "quantum": ["tunneling", "mechanics", "state", "superposition"],
            "tunneling": ["occurs", "is", "allows", "happens"],
            "occurs": ["when", "in", "because"],
            "when": ["a", "particles", "the"],
            "a": ["particle", "barrier", "system", "wavefunction"],
            "particle": ["passes", "meets", "crosses", "appears"],
            "passes": ["through", "across"],
            "through": ["a", "the"],
            "potential": ["barrier", "energy"],
            "barrier": ["that", "which", "easily"],
            "that": ["classical", "quantum"],
            "classical": ["physics", "mechanics"],
            "mechanics": ["would", "forbids", "describes"],
            "forbids": ["it", "crossing"],
            "from": ["crossing", "passing"]
        }

        self.domain_sentences = {
            "quantum mechanics": [
                "Quantum tunneling occurs when a particle passes through a potential barrier that classical mechanics would forbid it from crossing.",
                "The effect arises naturally from the wave-like nature of the quantum state.",
                "The probability of tunneling depends strongly on the width and height of the energy barrier."
            ],
            "machine learning": [
                "Machine learning algorithms optimize mathematical loss functions over training data.",
                "Deep neural networks extract hierarchical feature representations across multiple layers.",
                "Model generalization performance is evaluated on unseen validation datasets."
            ],
            "general": [
                "Complex dynamic systems evolve over time according to underlying force interactions.",
                "The state vector tracks continuous position and velocity trajectories.",
                "Friction and damping forces naturally stabilize the motion over time."
            ]
        }

    def match_subwords(self, prefix: str) -> List[SubwordCandidate]:
        prefix_lower = prefix.lower()
        candidates = []
        if prefix_lower in self.subword_dictionary:
            for suffix in self.subword_dictionary[prefix_lower]:
                full_word = prefix_lower + suffix
                score = 1.0 / (len(suffix) + 1.0)
                candidates.append(SubwordCandidate(prefix=prefix_lower, suffix=suffix, word=full_word, score=score))
        return candidates

    def construct_word_from_subword(self, prefix: str, suffix: str) -> str:
        return prefix + suffix

    def project_next_word_in_phrase(self, current_word: str) -> List[str]:
        w_lower = current_word.lower()
        return self.phrase_graph.get(w_lower, ["is", "system", "state"])

    def generate_sentence_from_concept(self, topic: str, subtopic_idx: int = 0, velocity: float = 1.0) -> str:
        topic_key = topic.lower()
        sentences = self.domain_sentences.get(topic_key, self.domain_sentences["general"])
        selected = sentences[subtopic_idx % len(sentences)]
        return selected

    def generate_paragraph(
        self,
        topic: str,
        velocity: float = 1.0,
        direction: np.ndarray = np.array([1.0, 0.0]),
        num_sentences: int = 3
    ) -> Tuple[str, ParagraphState, List[Dict[str, Any]]]:
        p_state = ParagraphState(
            topic=topic,
            current_subtopic="introduction",
            semantic_direction=direction,
            interaction_velocity=velocity,
            projected_next_direction=direction
        )

        sentences = []
        progression_trace = []

        topic_key = topic.lower()
        sentence_corpus = self.domain_sentences.get(topic_key, self.domain_sentences["general"])

        # Velocity controls sentence depth (higher velocity -> longer paragraph)
        actual_count = min(num_sentences, max(1, int(velocity * 0.8)))

        for i in range(min(actual_count, len(sentence_corpus))):
            s_text = sentence_corpus[i]
            sentences.append(s_text)

            progression_trace.append({
                "sentence_index": i + 1,
                "sentence": s_text,
                "paragraph_subtopic": f"subtopic_{i+1}",
                "velocity": velocity * (0.8 ** i),
                "direction": p_state.semantic_direction.tolist()
            })

            p_state.completed_information.append(f"sentence_{i+1}")

        final_paragraph = " ".join(sentences)
        return final_paragraph, p_state, progression_trace


class PhysicsControlledGenerator:
    """
    Couples the SimulationEngine dynamics (force, velocity, friction, direction)
    to the HierarchicalLanguageGenerator to steer language output.
    """
    def __init__(self) -> None:
        self.generator = HierarchicalLanguageGenerator()

    def generate_from_sim_state(self, sim: SimulationEngine, topic: str, mode: str = "PARAGRAPH") -> Dict[str, Any]:
        vel = sim.state.speed()
        direction = sim.state.velocity / vel if vel > 0 else np.array([1.0, 0.0])

        # Step 1: Subword demonstration
        subword_cands = self.generator.match_subwords("quant")

        # Step 2 & 3: Word and Phrase demonstration
        word = "quantum"
        phrase_proj = self.generator.project_next_word_in_phrase(word)

        # Step 4, 5, 6: Sentence and Paragraph generation
        if mode == "SENTENCE":
            sentence = self.generator.generate_sentence_from_concept(topic, velocity=vel)
            final_text = sentence
            paragraph_trace = []
            p_state = ParagraphState(topic=topic, current_subtopic="sentence_only", semantic_direction=direction, interaction_velocity=vel)
        else:
            final_text, p_state, paragraph_trace = self.generator.generate_paragraph(topic, velocity=vel, direction=direction)

        return {
            "user_view": final_text,
            "research_view": {
                "concept": topic,
                "velocity": vel,
                "direction": direction.tolist(),
                "applied_force": np.linalg.norm(sim.active_force.get_force(0.0)) if sim.active_force else 0.0,
                "friction": sim.friction_model.get_friction_force(sim.state.velocity).tolist(),
                "position": sim.state.position.tolist(),
                "subword_candidates": [c.word for c in subword_cands],
                "phrase_projections": phrase_proj,
                "paragraph_state": {
                    "topic": p_state.topic,
                    "subtopic": p_state.current_subtopic,
                    "completed_sentences": len(p_state.completed_information)
                },
                "progression_trace": paragraph_trace
            }
        }
