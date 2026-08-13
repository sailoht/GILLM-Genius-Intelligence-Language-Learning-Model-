IRREGULAR_PAST_PARTICIPLE = {
    "went": ("go", {"tense": "PAST"}),
    "gone": ("go", {"tense": "PAST_PARTICIPLE"}),
    "saw": ("see", {"tense": "PAST"}),
    "seen": ("see", {"tense": "PAST_PARTICIPLE"}),
    "did": ("do", {"tense": "PAST"}),
    "done": ("do", {"tense": "PAST_PARTICIPLE"}),
    "was": ("be", {"tense": "PAST", "number": "SINGULAR", "person": "FIRST_OR_THIRD"}),
    "were": ("be", {"tense": "PAST", "number": "PLURAL"}),
    "had": ("have", {"tense": "PAST"}),
    "has": ("have", {"tense": "PRESENT", "number": "SINGULAR", "person": "THIRD"}),
    "ate": ("eat", {"tense": "PAST"}),
    "eaten": ("eat", {"tense": "PAST_PARTICIPLE"}),
}

IRREGULAR_PLURALS = {
    "men": "man",
    "women": "woman",
    "children": "child",
    "mice": "mouse",
    "feet": "foot",
    "teeth": "tooth",
}
