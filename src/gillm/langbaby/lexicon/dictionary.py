from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class LexicalEntry:
    word: str
    pos: str  # NOUN, VERB, ADJECTIVE, PREPOSITION, DET, AUX
    lemma: str
    definitions: List[str] = field(default_factory=list)
    semantic_category: Optional[str] = None

class Lexicon:
    """
    Lexicon abstraction storing candidate analyses and meanings.
    """
    def __init__(self):
        self._entries: Dict[str, List[LexicalEntry]] = {}
        self._populate_default_lexicon()

    def _populate_default_lexicon(self):
        defaults = [
            LexicalEntry("the", "DET", "the"),
            LexicalEntry("a", "DET", "a"),
            LexicalEntry("boy", "NOUN", "boy", semantic_category="PERSON"),
            LexicalEntry("man", "NOUN", "man", semantic_category="PERSON"),
            LexicalEntry("ball", "NOUN", "ball", semantic_category="OBJECT"),
            LexicalEntry("car", "NOUN", "car", semantic_category="VEHICLE"),
            LexicalEntry("telescope", "NOUN", "telescope", semantic_category="INSTRUMENT"),
            LexicalEntry("force", "NOUN", "force", semantic_category="PHYSICAL_QUANTITY"),
            LexicalEntry("kicked", "VERB", "kick", semantic_category="ACTION"),
            LexicalEntry("kick", "VERB", "kick", semantic_category="ACTION"),
            LexicalEntry("saw", "VERB", "see", semantic_category="PERCEPTION"),
            LexicalEntry("accelerates", "VERB", "accelerate", semantic_category="MOTION"),
            LexicalEntry("accelerate", "VERB", "accelerate", semantic_category="MOTION"),
            LexicalEntry("acts", "VERB", "act", semantic_category="ACTION"),
            LexicalEntry("was", "AUX", "be"),
            LexicalEntry("is", "AUX", "be"),
            LexicalEntry("with", "PREPOSITION", "with"),
            LexicalEntry("by", "PREPOSITION", "by"),
            LexicalEntry("on", "PREPOSITION", "on"),
            LexicalEntry("because", "CONJUNCTION", "because"),
            LexicalEntry("it", "PRONOUN", "it"),
        ]
        for entry in defaults:
            self.add_entry(entry)

    def add_entry(self, entry: LexicalEntry):
        key = entry.word.lower()
        if key not in self._entries:
            self._entries[key] = []
        self._entries[key].append(entry)

    def lookup(self, word: str) -> List[LexicalEntry]:
        return self._entries.get(word.lower(), [LexicalEntry(word, "UNKNOWN", word)])
