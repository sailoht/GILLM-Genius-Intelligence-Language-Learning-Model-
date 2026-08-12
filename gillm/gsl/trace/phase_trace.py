from typing import List, Dict, Any

class PhaseTrace:
    def __init__(self) -> None:
        self.steps: Dict[str, Any] = {}

    def log_input(self, original_text: str) -> None:
        self.steps["INPUT"] = original_text

    def log_tokenization(self, tokens_str: str) -> None:
        self.steps["TOKENIZATION"] = tokens_str

    def log_morphology(self, morphology_log: str) -> None:
        self.steps["MORPHOLOGY"] = morphology_log

    def log_lexicon(self, lexicon_log: str) -> None:
        self.steps["LEXICON"] = lexicon_log

    def log_syntax(self, syntax_log: str) -> None:
        self.steps["SYNTAX"] = syntax_log

    def log_verb_frame(self, verb_frame_log: str) -> None:
        self.steps["VERB FRAME"] = verb_frame_log

    def log_semantics(self, semantics_log: str) -> None:
        self.steps["SEMANTICS"] = semantics_log

    def log_gcpr(self, gcpr_log: str) -> None:
        self.steps["GCPR"] = gcpr_log

    def format_trace(self) -> str:
        lines = []
        ordered_steps = ["INPUT", "TOKENIZATION", "MORPHOLOGY", "LEXICON", "SYNTAX", "VERB FRAME", "SEMANTICS", "GCPR"]

        for step in ordered_steps:
            if step in self.steps:
                lines.append(f"=== {step} ===")
                lines.append(self.steps[step].strip())
                lines.append("")

        return "\n".join(lines)
