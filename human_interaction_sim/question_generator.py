from typing import Dict, Any

class ModularQuestionGenerator:
    """
    Rule-based question generator inspecting current simulated state/topic.
    Decoupled interface so it can later be replaced by GILLM.
    """
    def __init__(self) -> None:
        self.question_templates = {
            "quantum mechanics": [
                "Would you like to start with wave-particle duality or the Schrödinger equation?",
                "Should we explore quantum entanglement or quantum superposition next?",
                "Would you like to see a practical example like quantum computing?"
            ],
            "machine learning": [
                "Would you prefer discussing supervised learning or neural networks?",
                "Should we look at model evaluation metrics or training algorithms?",
                "Would you like to explore deep learning architectures?"
            ],
            "physics": [
                "Shall we examine classical mechanics or thermodynamics?",
                "Would you like to explore relativity theory?",
                "Should we analyze force and motion principles?"
            ],
            "general": [
                "Would you like to dive deeper into this topic or explore a related concept?",
                "What specific aspect of this topic interests you most?",
                "Shall we look at a practical example?"
            ]
        }

    def generate_question(self, topic: str, cycle_count: int = 0) -> str:
        topic_lower = topic.lower().strip()
        templates = self.question_templates.get(topic_lower, self.question_templates["general"])
        idx = cycle_count % len(templates)
        return templates[idx]
