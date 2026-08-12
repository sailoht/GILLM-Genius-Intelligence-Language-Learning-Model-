import pytest
from gillm.gsl.phaser import GSLPhaser

@pytest.fixture
def phaser():
    return GSLPhaser()

def test_valid_scenarios(phaser):
    # Valid statements
    gcpr, _ = phaser.phase("The boy opened the door.")
    assert len(gcpr.to_dict().get("errors", [])) == 0

    gcpr, _ = phaser.phase("The dog eats food.")
    assert len(gcpr.to_dict().get("errors", [])) == 0

def test_question_scenarios(phaser):
    # WHO, expected answer PERSON
    gcpr, _ = phaser.phase("Who opened the door?")
    assert gcpr.conversation.expected_answer == "PERSON"
    assert gcpr.conversation.question_family == "WHO"

    # YES/NO, expected answer BOOLEAN
    gcpr, _ = phaser.phase("Did the dog eat food?")
    assert gcpr.conversation.expected_answer == "BOOLEAN"
    assert gcpr.conversation.question_family == "YES_NO"

def test_spelling_correction(phaser):
    # hte -> the
    gcpr, _ = phaser.phase("hte boy opened the door.")
    errors = gcpr.to_dict().get("errors", [])
    assert len(errors) > 0
    assert any(e["error_type"] == "SPELLING" for e in errors)
    assert errors[0]["candidates"][0] == "the"

def test_missing_word(phaser):
    # Missing auxiliary
    gcpr, _ = phaser.phase("The boy going to school.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "MISSING_WORD" for e in errors)
    assert "is" in errors[0]["candidates"][0]

    # Missing preposition
    gcpr, _ = phaser.phase("He went school.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "MISSING_WORD" for e in errors)
    assert "to school" in errors[0]["candidates"][0]

def test_extra_word(phaser):
    # Extra "is"
    gcpr, _ = phaser.phase("The boy is is going home.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "EXTRA_WORD" for e in errors)
    assert "is going" in errors[0]["candidates"][0]

def test_word_order(phaser):
    # Why you did -> Why did you
    gcpr, _ = phaser.phase("Why you did go there?")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "WORD_ORDER" for e in errors)
    assert "Why did you go" in errors[0]["candidates"][0]

def test_subject_verb_agreement(phaser):
    # He go -> He goes
    gcpr, _ = phaser.phase("He go to school.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "SUBJECT_VERB_AGREEMENT" for e in errors)
    assert "He goes to" in errors[0]["candidates"][0]

    # They goes -> They go
    gcpr, _ = phaser.phase("They goes to school.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "SUBJECT_VERB_AGREEMENT" for e in errors)
    assert "They go to" in errors[0]["candidates"][0]

def test_tense_inconsistency(phaser):
    # Yesterday I go -> Yesterday I went
    gcpr, _ = phaser.phase("Yesterday I go to school.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "TENSE_INCONSISTENCY" for e in errors)
    assert "Yesterday I went" in errors[0]["candidates"][0]

def test_pronoun_case(phaser):
    # Me went -> I went
    gcpr, _ = phaser.phase("Me went to school.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "PRONOUN_CASE" for e in errors)
    assert "I went to" in errors[0]["candidates"][0]

def test_determiners_missing_and_mismatch(phaser):
    # I saw dog -> I saw a dog
    gcpr, _ = phaser.phase("I saw dog.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "MISSING_DETERMINER" for e in errors)
    assert "I saw a dog." in errors[0]["candidates"][0]

    # a honest -> an honest
    gcpr, _ = phaser.phase("He is a honest man.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "PHONOLOGICAL_DETERMINER_MISMATCH" for e in errors)
    assert "an honest" in errors[0]["candidates"][0]

def test_preposition_collocation(phaser):
    # good in -> good at
    gcpr, _ = phaser.phase("He is good in mathematics.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "PREPOSITION_USAGE" for e in errors)
    assert "good at mathematics" in errors[0]["candidates"][0]
    assert errors[0]["status"] == "POSSIBLE" # Non-standard/possible vs strict error

def test_auxiliary_double_past(phaser):
    # Did he went -> Did he go
    gcpr, _ = phaser.phase("Did he went there?")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "AUXILIARY_DOUBLE_PAST" for e in errors)
    assert "Did he go there" in errors[0]["candidates"][0]

    # He didn't went -> He didn't go
    gcpr, _ = phaser.phase("He didn't went.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "AUXILIARY_DOUBLE_PAST" for e in errors)

def test_number_agreement(phaser):
    # two book -> two books
    gcpr, _ = phaser.phase("two book")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "NUMBER_AGREEMENT" for e in errors)
    assert "two books" in errors[0]["candidates"][0]

    # one books -> one book
    gcpr, _ = phaser.phase("one books")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "NUMBER_AGREEMENT" for e in errors)
    assert "one book" in errors[0]["candidates"][0]

def test_punctuation_capitalization(phaser):
    # Why did you go there -> Why did you go there?
    gcpr, _ = phaser.phase("Why did you go there")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "MISSING_PUNCTUATION" for e in errors)
    assert "there?" in errors[0]["candidates"][0]

    # the boy -> The boy
    gcpr, _ = phaser.phase("the boy opened the door.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "MISSING_CAPITALIZATION" for e in errors)
    assert "The boy" in errors[0]["candidates"][0]

def test_sentence_boundaries(phaser):
    # Run-on I went I ate -> sentence boundary
    gcpr, _ = phaser.phase("I went home I ate food I slept.")
    errors = gcpr.to_dict().get("errors", [])
    assert any(e["error_type"] == "SENTENCE_BOUNDARY_RUNON" for e in errors)
    assert "I went home. I ate food. I slept." in errors[0]["candidates"][0]

def test_semantics_and_figurative(phaser):
    # The stone ate the boy -> Semantically unusual
    gcpr, _ = phaser.phase("The stone ate the boy.")
    data = gcpr.to_dict()
    errors = data.get("errors", [])
    assert any(e["error_type"] == "SEMANTICALLY_UNUSUAL" for e in errors)
    assert len(errors[0]["candidates"]) == 0

    # The moon smiled at me -> Figurative language personification
    gcpr, _ = phaser.phase("The moon smiled at me.")
    data = gcpr.to_dict()
    errors = data.get("errors", [])
    assert any(e["error_type"] == "FIGURATIVE_POSSIBILITY" for e in errors)
    fig_lang = data.get("figurative_language", {})
    assert fig_lang["is_figurative"] is True
    assert fig_lang["type"] == "PERSONIFICATION"

def test_discourse_and_temporal(phaser):
    # Before John arrived, Mary left.
    gcpr, _ = phaser.phase("Before John arrived, Mary left.")
    data = gcpr.to_dict()
    temp_relations = data.get("temporal_relations", [])
    assert len(temp_relations) > 0
    assert temp_relations[0]["relation"] == "BEFORE"

    # It was raining. Therefore, we stayed home.
    gcpr, _ = phaser.phase("It was raining. Therefore, we stayed home.")
    data = gcpr.to_dict()
    disc_relations = data.get("discourse_relations", [])
    assert len(disc_relations) > 0
    assert disc_relations[0]["relation"] == "CAUSE"

def test_speech_act_and_exercises(phaser):
    # "Can you open the door?" -> speech act REQUEST
    gcpr, _ = phaser.phase("Can you open the door?")
    data = gcpr.to_dict()
    assert data.get("speech_act") == "REQUEST"

    exercises = data.get("exercises", {})
    assert "fill_in_blanks_candidates" in exercises
    assert len(exercises["fill_in_blanks_candidates"]) > 0

def test_entities_preservation(phaser):
    # "The boy bought a book." -> preserved boy, book
    gcpr, _ = phaser.phase("The boy bought a book.")
    data = gcpr.to_dict()
    entities = data.get("semantic", {}).get("entities", {})
    assert "boy" in entities
    assert "book" in entities
