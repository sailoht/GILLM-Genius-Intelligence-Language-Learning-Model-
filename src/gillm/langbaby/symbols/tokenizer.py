from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional

class TokenType(Enum):
    WORD = auto()
    NUMBER = auto()
    PUNCTUATION = auto()
    SYMBOL = auto()

@dataclass
class Token:
    text: str
    normalized: str
    token_type: TokenType
    position: int
    metadata: dict = field(default_factory=dict)

class Tokenizer:
    """
    Deterministic Tokenizer for LangBaby.
    Does NOT determine meaning or guess prematurely.
    Preserves original text, punctuation, and character indices.
    """
    def tokenize(self, text: str) -> List[Token]:
        tokens: List[Token] = []
        i = 0
        n = len(text)
        pos = 0

        while i < n:
            char = text[i]
            if char.isspace():
                i += 1
                continue

            if char.isalpha():
                start = i
                while i < n and (text[i].isalpha() or text[i] in "'-"):
                    i += 1
                word = text[start:i]
                tokens.append(Token(text=word, normalized=word.lower(), token_type=TokenType.WORD, position=pos))
                pos += 1
            elif char.isdigit():
                start = i
                while i < n and (text[i].isdigit() or text[i] == '.'):
                    i += 1
                num = text[start:i]
                tokens.append(Token(text=num, normalized=num, token_type=TokenType.NUMBER, position=pos))
                pos += 1
            else:
                tokens.append(Token(text=char, normalized=char, token_type=TokenType.PUNCTUATION if char in ".!?,;:\"'()-[]" else TokenType.SYMBOL, position=pos))
                i += 1
                pos += 1

        return tokens
