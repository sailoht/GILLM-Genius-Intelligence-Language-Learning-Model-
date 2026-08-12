import re
from typing import List
from gillm.input.models import Token

class Tokenizer:
    def __init__(self) -> None:
        self.pattern = re.compile(r"([a-zA-Z]+(?:'[a-zA-Z]+)?|[0-9]+(?:\.[0-9]+)?|[.,!?;:()'\"]|[^a-zA-Z0-9\s])")

    def tokenize(self, text: str) -> List[Token]:
        tokens: List[Token] = []
        raw_tokens = self.pattern.findall(text)
        for i, raw in enumerate(raw_tokens):
            normalized = raw

            # Use regex to support words with internal apostrophes as WORD
            if re.match(r"^[a-zA-Z]+(?:'[a-zA-Z]+)?$", raw):
                token_type = "WORD"
            elif raw.isdigit() or re.match(r"^\d+(?:\.\d+)?$", raw):
                token_type = "NUMBER"
            elif raw in ".,!?;:()'\"":
                token_type = "PUNCTUATION"
            else:
                token_type = "SYMBOL"

            tokens.append(Token(
                text=raw,
                normalized=normalized,
                token_type=token_type,
                position=i
            ))
        return tokens
