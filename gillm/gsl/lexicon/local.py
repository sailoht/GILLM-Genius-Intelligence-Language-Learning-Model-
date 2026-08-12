import json
import os
from typing import Dict, Optional, List
from gillm.gsl.lexicon.models import LexicalEntry

class LocalLexicon:
    def __init__(self, data_path: Optional[str] = None) -> None:
        if data_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, "data.json")

        self.data_path = data_path
        self.entries: Dict[str, LexicalEntry] = {}
        self.load_lexicon()

    def load_lexicon(self) -> None:
        if not os.path.exists(self.data_path):
            return

        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for surface, entry_data in data.items():
            self.entries[surface.lower()] = LexicalEntry(
                surface=surface,
                lemma=entry_data.get("lemma", surface),
                pos_candidates=entry_data.get("pos_candidates", []),
                definition=entry_data.get("definition", ""),
                morphological_features=entry_data.get("morphological_features", {}),
                frequency=entry_data.get("frequency", 1.0),
                semantic_categories=entry_data.get("semantic_categories", []),
                verb_frames=entry_data.get("verb_frames", []),
                transitivity=entry_data.get("transitivity")
            )

    def lookup(self, word: str) -> Optional[LexicalEntry]:
        return self.entries.get(word.lower())

    def get_all_entries(self) -> List[LexicalEntry]:
        return list(self.entries.values())
