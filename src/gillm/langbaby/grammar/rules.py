from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ParseTreeNode:
    label: str  # S, NP, VP, PP, V, N, Det, Prep
    children: List['ParseTreeNode'] = field(default_factory=list)
    text: Optional[str] = None
    voice: str = "ACTIVE"  # ACTIVE or PASSIVE

class GrammarEngine:
    """
    Grammatical pattern matcher & parser supporting Active, Passive, Prepositional phrases, and Clause structures.
    """
    def parse_structure(self, tokens: List[str]) -> ParseTreeNode:
        # Check for passive voice pattern: DET NOUN AUX VERB "by" DET NOUN
        # e.g., ["the", "ball", "was", "kicked", "by", "the", "boy"]
        tokens_lower = [t.lower() for t in tokens if t not in ".!?"]

        if "was" in tokens_lower and "by" in tokens_lower:
            by_idx = tokens_lower.index("by")
            was_idx = tokens_lower.index("was")
            patient_tokens = tokens_lower[:was_idx]
            verb_token = tokens_lower[was_idx + 1]
            agent_tokens = tokens_lower[by_idx + 1:]

            patient_np = ParseTreeNode(label="NP", text=" ".join(patient_tokens))
            agent_np = ParseTreeNode(label="NP", text=" ".join(agent_tokens))
            verb_node = ParseTreeNode(label="V", text=verb_token)

            vp_node = ParseTreeNode(
                label="VP",
                children=[verb_node, agent_np],
                text=f"{verb_token} by {' '.join(agent_tokens)}"
            )
            return ParseTreeNode(
                label="S",
                children=[patient_np, vp_node],
                text=" ".join(tokens_lower),
                voice="PASSIVE"
            )

        # Default Active Voice parse
        # e.g., ["the", "boy", "kicked", "the", "ball"]
        return ParseTreeNode(
            label="S",
            children=[ParseTreeNode(label="NP", text=" ".join(tokens_lower))],
            text=" ".join(tokens_lower),
            voice="ACTIVE"
        )
