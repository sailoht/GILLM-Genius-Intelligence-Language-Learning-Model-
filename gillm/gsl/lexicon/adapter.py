from typing import Optional, List
from gillm.gsl.lexicon.models import LexicalEntry
from gillm.gsl.lexicon.local import LocalLexicon

class LexiconAdapter:
    def lookup(self, word: str) -> Optional[LexicalEntry]:
        raise NotImplementedError

class LocalLexiconAdapter(LexiconAdapter):
    def __init__(self, local_lexicon: LocalLexicon) -> None:
        self.local_lexicon = local_lexicon

    def lookup(self, word: str) -> Optional[LexicalEntry]:
        return self.local_lexicon.lookup(word)
