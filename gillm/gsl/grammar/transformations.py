import copy
from gillm.gsl.gcpr.models import GCPR

def active_to_passive_transformation(gcpr: GCPR) -> GCPR:
    """
    Transforms an Active Statement GCPR into a Passive Statement GCPR.
    Preconditions:
      - sentence_type == "statement"
      - voice == "ACTIVE" or not specified as "PASSIVE"
      - agent, patient, and action exist in semantic roles
    """
    roles = gcpr.semantic.roles
    if gcpr.linguistic.sentence_type != "statement":
        raise ValueError("Transformation precondition failed: Sentence type must be statement")

    voice = gcpr.linguistic.syntax.get("voice", "ACTIVE")
    if voice == "PASSIVE":
        raise ValueError("Transformation precondition failed: Voice is already passive")

    if not ("agent" in roles and "patient" in roles and "action" in roles):
        raise ValueError("Transformation precondition failed: Must have agent, patient, and action")

    # Perform structural transformation
    new_gcpr = copy.deepcopy(gcpr)
    new_gcpr.linguistic.syntax["voice"] = "PASSIVE"
    # Swap syntax roles if present
    # In GCPR, the semantic roles remain the same (agent=boy, patient=door, action=open),
    # but linguistic syntax voice becomes passive, which changes how realization generates the sentence.
    return new_gcpr

def statement_to_question_transformation(gcpr: GCPR) -> GCPR:
    """
    Transforms a Statement GCPR into a Yes/No Question GCPR.
    """
    if gcpr.linguistic.sentence_type != "statement":
        raise ValueError("Transformation precondition failed: Must be a statement")

    new_gcpr = copy.deepcopy(gcpr)
    new_gcpr.linguistic.sentence_type = "question"
    new_gcpr.conversation.question_family = "YES_NO"
    new_gcpr.conversation.expected_answer = "BOOLEAN"
    return new_gcpr

def positive_to_negative_transformation(gcpr: GCPR) -> GCPR:
    """
    Transforms a positive sentence to a negative sentence in GCPR.
    """
    new_gcpr = copy.deepcopy(gcpr)
    new_gcpr.linguistic.grammar["polarity"] = "NEGATIVE"
    return new_gcpr
