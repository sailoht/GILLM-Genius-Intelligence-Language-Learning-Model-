from typing import List, Tuple, Dict, Any

def apply_suffix_rules(word: str) -> List[Tuple[str, str, Dict[str, Any]]]:
    results = []

    if len(word) > 3 and word.endswith("ing"):
        base = word[:-3]
        if len(base) > 2 and base[-1] == base[-2] and base[-1] not in "aeiouy":
            results.append((base[:-1], "VERB", {"tense": "PRESENT_PARTICIPLE", "aspect": "PROGRESSIVE"}))
        results.append((base + "e", "VERB", {"tense": "PRESENT_PARTICIPLE", "aspect": "PROGRESSIVE"}))
        results.append((base, "VERB", {"tense": "PRESENT_PARTICIPLE", "aspect": "PROGRESSIVE"}))

    if len(word) > 2 and word.endswith("ed"):
        base = word[:-2]
        if len(base) > 2 and base[-1] == base[-2] and base[-1] not in "aeiouy":
            results.append((base[:-1], "VERB", {"tense": "PAST"}))
        if word.endswith("ied") and len(word) > 3:
            results.append((word[:-3] + "y", "VERB", {"tense": "PAST"}))
        if base.endswith("e"):
            results.append((base, "VERB", {"tense": "PAST"}))
        else:
            results.append((base + "e", "VERB", {"tense": "PAST"}))
            results.append((base, "VERB", {"tense": "PAST"}))

    if len(word) > 1 and word.endswith("s") and not word.endswith("ss"):
        if word.endswith("es"):
            if word.endswith("ies") and len(word) > 3:
                base = word[:-3] + "y"
                results.append((base, "NOUN", {"number": "PLURAL"}))
                results.append((base, "VERB", {"tense": "PRESENT", "number": "SINGULAR", "person": "THIRD"}))
            else:
                base = word[:-2]
                results.append((base, "NOUN", {"number": "PLURAL"}))
                results.append((base, "VERB", {"tense": "PRESENT", "number": "SINGULAR", "person": "THIRD"}))
        else:
            base = word[:-1]
            results.append((base, "NOUN", {"number": "PLURAL"}))
            results.append((base, "VERB", {"tense": "PRESENT", "number": "SINGULAR", "person": "THIRD"}))

    return results
