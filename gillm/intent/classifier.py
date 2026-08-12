from typing import Dict, Any

class IntentClassifier:
    """Classifies the main intent of a GCPR structure."""

    @staticmethod
    def classify(gcpr_data: Dict[str, Any]) -> str:
        linguistic = gcpr_data.get("linguistic", {})
        conv = gcpr_data.get("conversation", {})

        sentence_type = linguistic.get("sentence_type")
        if sentence_type == "question":
            q_family = conv.get("question_family")
            if q_family == "WHAT":
                return "DEFINITION"
            elif q_family == "WHY":
                return "CAUSE"
            elif q_family == "WHERE":
                return "LOCATION"
            elif q_family == "WHO":
                return "PERSON"
            elif q_family == "YES_NO":
                return "CONFIRMATION"
            return "QUESTION"

        return "STATEMENT"
