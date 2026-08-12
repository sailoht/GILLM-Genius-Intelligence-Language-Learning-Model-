from typing import Dict, Any, List, Tuple

class GCPRValidator:
    """Validates that a given dictionary complies with the GSL GCPR contract."""

    @staticmethod
    def validate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        required_top_keys = ["surface", "linguistic", "semantic", "conversation", "intent", "uncertainty"]
        for key in required_top_keys:
            if key not in data:
                errors.append(f"Missing top-level key: '{key}'")

        if "surface" in data:
            surf = data["surface"]
            if not isinstance(surf, dict):
                errors.append("surface must be a dictionary")
            else:
                if "original_text" not in surf:
                    errors.append("surface must contain 'original_text'")
                if "tokens" not in surf:
                    errors.append("surface must contain 'tokens'")

        if "linguistic" in data:
            ling = data["linguistic"]
            if not isinstance(ling, dict):
                errors.append("linguistic must be a dictionary")
            else:
                for k in ["sentence_type", "morphology", "grammar", "syntax"]:
                    if k not in ling:
                        errors.append(f"linguistic must contain '{k}'")

        if "semantic" in data:
            sem = data["semantic"]
            if not isinstance(sem, dict):
                errors.append("semantic must be a dictionary")
            else:
                for k in ["roles", "entities", "relations"]:
                    if k not in sem:
                        errors.append(f"semantic must contain '{k}'")

        if "conversation" in data:
            conv = data["conversation"]
            if not isinstance(conv, dict):
                errors.append("conversation must be a dictionary")
            else:
                for k in ["role", "question_family", "expected_answer"]:
                    if k not in conv:
                        errors.append(f"conversation must contain '{k}'")

        if "uncertainty" in data:
            unc = data["uncertainty"]
            if not isinstance(unc, dict):
                errors.append("uncertainty must be a dictionary")
            else:
                for k in ["ambiguous", "alternatives", "confidence"]:
                    if k not in unc:
                        errors.append(f"uncertainty must contain '{k}'")

        return (len(errors) == 0, errors)
