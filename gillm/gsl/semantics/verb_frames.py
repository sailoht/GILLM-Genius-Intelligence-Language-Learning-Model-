from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from gillm.gsl.lexicon.loader import LexiconLoader

@dataclass
class VerbFrame:
    lemma: str
    roles: List[str]  # e.g. ["AGENT", "PATIENT"]
    transitivity: str  # "transitive", "intransitive", "ditransitive"
    features: Dict[str, Any] = field(default_factory=dict)

class VerbFrameRegistry:
    def __init__(self) -> None:
        self.lexicon = LexiconLoader.get_lexicon()
        self._default_frames: Dict[str, VerbFrame] = {
            "open": VerbFrame("open", ["AGENT", "PATIENT"], "transitive"),
            "eat": VerbFrame("eat", ["AGENT", "PATIENT"], "transitive"),
            "sleep": VerbFrame("sleep", ["AGENT"], "intransitive"),
            "see": VerbFrame("see", ["EXPERIENCER", "PATIENT"], "transitive"),
            "go": VerbFrame("go", ["AGENT", "DESTINATION"], "intransitive"),
            "give": VerbFrame("give", ["AGENT", "THEME", "RECIPIENT"], "ditransitive"),
            "happen": VerbFrame("happen", ["PATIENT"], "intransitive"),
            "be": VerbFrame("be", ["IDENTITY"], "intransitive")
        }

    def get_frame(self, lemma: str) -> Optional[VerbFrame]:
        lemma_lower = lemma.lower()

        if lemma_lower in self._default_frames:
            return self._default_frames[lemma_lower]

        entry = self.lexicon.lookup(lemma_lower)
        if entry and entry.verb_frames:
            roles = []
            for frame_str in entry.verb_frames:
                roles = frame_str.split("_")
            trans = entry.transitivity or ("transitive" if len(roles) > 1 else "intransitive")
            return VerbFrame(lemma_lower, roles, trans)

        return None
