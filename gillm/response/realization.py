from gillm.gsl.gcpr.models import GCPR

def get_verb_form(lemma: str, tense: str, person: str = "third", number: str = "singular") -> str:
    lemma = lemma.lower()
    tense = tense.upper() if tense else "PRESENT"
    person = person.lower() if person else "third"
    number = number.lower() if number else "singular"

    past_irregular = {
        "go": "went",
        "see": "saw",
        "do": "did",
        "be": "was",
        "eat": "ate",
        "open": "opened",
        "happen": "happened",
    }

    present_3sg = {
        "go": "goes",
        "see": "sees",
        "do": "does",
        "be": "is",
        "eat": "eats",
        "open": "opens",
        "happen": "happens",
    }

    if tense == "PAST":
        return past_irregular.get(lemma, lemma + "ed")

    if person == "third" and number == "singular":
        return present_3sg.get(lemma, lemma + "s")

    return lemma

def format_np(noun: str) -> str:
    if not noun:
        return ""
    noun_lower = noun.lower()
    if noun_lower in ["food", "quantum tunneling", "it", "who", "what"]:
        return noun
    # If already starts with "the" or "a", return as is
    if noun_lower.startswith("the ") or noun_lower.startswith("a ") or noun_lower.startswith("an "):
        return noun
    return f"the {noun}"

class LanguageRealizer:
    def realize(self, gcpr: GCPR) -> str:
        roles = gcpr.semantic.roles
        action = roles.get("action")
        if not action:
            return ""

        tense = gcpr.linguistic.grammar.get("tense") or gcpr.linguistic.syntax.get("tense") or "PRESENT"
        voice = gcpr.linguistic.syntax.get("voice", "ACTIVE")
        polarity = gcpr.linguistic.grammar.get("polarity", "POSITIVE")

        sentence_type = gcpr.linguistic.sentence_type

        # 1. QUESTION realization
        if sentence_type == "question":
            q_family = gcpr.conversation.question_family

            if q_family == "YES_NO":
                aux = "did" if tense.upper() == "PAST" else "does"
                agent = format_np(roles.get("agent") or roles.get("experiencer") or "")
                patient = format_np(roles.get("patient") or "")

                neg = " not" if polarity == "NEGATIVE" else ""
                pat_part = f" {patient}" if patient else ""
                return f"{aux.capitalize()} {agent}{neg} {action}{pat_part}?".replace("  ", " ")

            elif q_family == "WHO":
                if roles.get("agent") == "unknown":
                    verb = get_verb_form(action, tense)
                    patient = format_np(roles.get("patient", ""))
                    pat_part = f" {patient}" if patient else ""
                    return f"Who {verb}{pat_part}?"
                else:
                    aux = "did" if tense.upper() == "PAST" else "does"
                    agent = format_np(roles.get("agent") or roles.get("experiencer") or "")
                    return f"Who {aux} {agent} {action}?"

            elif q_family == "WHAT":
                aux = "did" if tense.upper() == "PAST" else "does"
                agent = format_np(roles.get("agent") or roles.get("experiencer") or "")
                return f"What {aux} {agent} {action}?"

            elif q_family == "WHERE":
                aux = "did" if tense.upper() == "PAST" else "does"
                agent = format_np(roles.get("agent") or roles.get("experiencer") or "")
                return f"Where {aux} {agent} {action}?"

            elif q_family == "WHY":
                aux = "did" if tense.upper() == "PAST" else "does"
                agent = format_np(roles.get("agent") or roles.get("experiencer") or "")
                patient = format_np(roles.get("patient") or "")
                pat_part = f" {patient}" if patient else ""
                return f"Why {aux} {agent} {action}{pat_part}?"

        # 2. STATEMENT realization
        else:
            agent = format_np(roles.get("agent") or roles.get("experiencer") or "")
            patient = format_np(roles.get("patient") or "")

            if voice.upper() == "PASSIVE":
                aux = "was" if tense.upper() == "PAST" else "is"
                action_part = get_verb_form(action, "PAST")
                by_agent = f" by {agent}" if agent else ""
                neg = " not" if polarity == "NEGATIVE" else ""
                # Capitalize first letter of patient
                pat_str = patient.capitalize()
                return f"{pat_str} {aux}{neg} {action_part}{by_agent}."

            else:
                verb = get_verb_form(action, tense)
                pat_part = f" {patient}" if patient else ""
                neg = ""
                # Capitalize first letter of agent
                agent_str = agent.capitalize()
                if polarity == "NEGATIVE":
                    aux = "did not" if tense.upper() == "PAST" else "does not"
                    verb = action
                    return f"{agent_str} {aux} {verb}{pat_part}."

                return f"{agent_str} {verb}{pat_part}."

        return ""
