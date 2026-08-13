from typing import Dict, Any, Tuple, List, Optional
from gillm.gsl.gcpr.models import GCPR
from gillm.response.realization import LanguageRealizer

class BidirectionalValidator:
    """
    Validates structural consistency by performing Bidirectional Validation:
    Input Text → GSL Analysis (GCPR) → Structural Realization (Text) → Re-analysis (GCPR) → Structural Comparison.
    """
    def __init__(self, phaser) -> None:
        self.phaser = phaser
        self.realizer = LanguageRealizer()

    def validate_structural_consistency(self, original_gcpr: GCPR) -> Tuple[bool, List[str]]:
        notes: List[str] = []

        try:
            realized_text = self.realizer.realize(original_gcpr)
            notes.append(f"Realized text: '{realized_text}'")
        except Exception as e:
            notes.append(f"Realization failed: {str(e)}")
            return False, notes

        if not realized_text:
            notes.append("Realized text is empty.")
            return False, notes

        try:
            re_gcpr, _ = self.phaser.phase(realized_text, context=None)
            notes.append("Re-analysis parsed successfully.")
        except Exception as e:
            notes.append(f"Re-analysis parsing failed: {str(e)}")
            return False, notes

        orig_dict = original_gcpr.to_dict()
        re_dict = re_gcpr.to_dict()

        orig_intent = orig_dict.get("intent")
        re_intent = re_dict.get("intent")
        if orig_intent != re_intent:
            notes.append(f"Intent mismatch: Original='{orig_intent}', Re-analyzed='{re_intent}'")
            return False, notes

        orig_roles = orig_dict.get("semantic", {}).get("roles", {})
        re_roles = re_dict.get("semantic", {}).get("roles", {})

        for role, val in orig_roles.items():
            if role == "action":
                if val.lower() != re_roles.get(role, "").lower():
                    notes.append(f"Action semantic role mismatch: '{val}' vs '{re_roles.get(role)}'")
                    return False, notes
            else:
                orig_val = str(val).lower()
                re_val = str(re_roles.get(role, "")).lower()
                if orig_val != re_val and orig_val != "unknown" and re_val != "unknown":
                    if orig_val.replace("the ", "").replace("a ", "") != re_val.replace("the ", "").replace("a ", ""):
                        notes.append(f"Semantic role mismatch for '{role}': '{orig_val}' vs '{re_val}'")
                        return False, notes

        notes.append("Structural bidirectional validation matches perfectly.")
        return True, notes
