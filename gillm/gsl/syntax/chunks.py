from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from gillm.gsl.candidates.candidate import Candidate

@dataclass
class ParseNode:
    label: str  # e.g., "S", "NP", "VP", "PP", "Det", "Noun", "Verb", etc.
    children: List['ParseNode'] = field(default_factory=list)
    candidate: Optional[Candidate] = None  # Only set on leaf nodes
    features: Dict[str, Any] = field(default_factory=dict)
    score: float = 1.0
    evidence: List[str] = field(default_factory=list)

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def get_leaves(self) -> List[Candidate]:
        if self.is_leaf():
            return [self.candidate] if self.candidate else []
        leaves = []
        for child in self.children:
            leaves.extend(child.get_leaves())
        return leaves

    def pretty_format(self, indent: int = 0) -> str:
        space = "  " * indent
        details = ""
        if self.candidate:
            details = f" ({self.candidate.token.text} -> lemma={self.candidate.lemma}, pos={self.candidate.pos})"
        elif self.features:
            details = f" feats={self.features}"

        res = f"{space}[{self.label}]{details}\n"
        for child in self.children:
            res += child.pretty_format(indent + 1)
        return res
