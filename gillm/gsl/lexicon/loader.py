from typing import Optional, List
from gillm.gsl.lexicon.local import LocalLexicon
from gillm.gsl.lexicon.adapter import LocalLexiconAdapter, LexiconAdapter

class LexiconLoader:
    _instance: Optional[LexiconAdapter] = None

    @classmethod
    def get_lexicon(cls) -> LexiconAdapter:
        if cls._instance is None:
            local_lex = LocalLexicon()
            cls._instance = LocalLexiconAdapter(local_lex)
        return cls._instance
