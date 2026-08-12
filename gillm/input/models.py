from dataclasses import dataclass

@dataclass(frozen=True)
class Token:
    text: str
    normalized: str
    token_type: str  # WORD, NUMBER, PUNCTUATION, SYMBOL
    position: int
