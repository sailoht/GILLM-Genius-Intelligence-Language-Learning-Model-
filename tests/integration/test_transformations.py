from gillm.gsl.gcpr.models import GCPR, SurfaceRepresentation, LinguisticRepresentation, SemanticRepresentation
from gillm.gsl.grammar.transformations import active_to_passive_transformation, statement_to_question_transformation, positive_to_negative_transformation
from gillm.response.realization import LanguageRealizer

def test_transformations_and_realization():
    # Construct base GCPR: "The boy opened the door."
    surface = SurfaceRepresentation(original_text="The boy opened the door.")
    linguistic = LinguisticRepresentation(sentence_type="statement")
    linguistic.syntax["voice"] = "ACTIVE"
    linguistic.syntax["tense"] = "PAST"

    semantic = SemanticRepresentation(roles={
        "action": "open",
        "agent": "boy",
        "patient": "door"
    })

    gcpr = GCPR(surface=surface, linguistic=linguistic, semantic=semantic)

    realizer = LanguageRealizer()

    # Verify base realization
    assert realizer.realize(gcpr) == "The boy opened the door."

    # 1. Active to Passive
    passive_gcpr = active_to_passive_transformation(gcpr)
    assert realizer.realize(passive_gcpr) == "The door was opened by the boy."

    # 2. Statement to Question
    q_gcpr = statement_to_question_transformation(gcpr)
    assert realizer.realize(q_gcpr) == "Did the boy open the door?"

    # 3. Positive to Negative
    neg_gcpr = positive_to_negative_transformation(gcpr)
    assert realizer.realize(neg_gcpr) == "The boy did not open the door."
