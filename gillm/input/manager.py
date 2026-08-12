from typing import List
from gillm.input.tokenizer import Tokenizer
from gillm.input.models import Token

class InputManager:
    def __init__(self) -> None:
        self.tokenizer = Tokenizer()

    def process_input(self, text: str) -> List[Token]:
        clean_text = text.strip()
        return self.tokenizer.tokenize(clean_text)
