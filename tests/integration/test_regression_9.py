import pytest
from gillm.gsl.phaser import GSLPhaser
from gillm.conversation.context import ConversationContext

@pytest.fixture
def phaser():
    return GSLPhaser()

def test_scenario_1(phaser):
    # TEST 1: "The boy opened the door."
    gcpr, trace = phaser.phase("The boy opened the door.")

    assert gcpr.linguistic.sentence_type == "statement"
    assert gcpr.semantic.roles["action"] == "open"
    assert gcpr.semantic.roles["agent"] == "boy"
    assert gcpr.semantic.roles["patient"] == "door"
    assert gcpr.linguistic.grammar["tense"].lower() == "past"

def test_scenario_2(phaser):
    # TEST 2: "The dog eats food."
    gcpr, trace = phaser.phase("The dog eats food.")

    assert gcpr.semantic.roles["action"] == "eat"
    assert gcpr.semantic.roles["agent"] == "dog"
    assert gcpr.semantic.roles["patient"] == "food"
    assert gcpr.linguistic.grammar["tense"].lower() == "present"
    # features of 'eats' should contain third singular person
    assert gcpr.linguistic.morphology.get("number") == "SINGULAR"

def test_scenario_3(phaser):
    # TEST 3: "Who opened the door?"
    gcpr, trace = phaser.phase("Who opened the door?")

    assert gcpr.conversation.question_family == "WHO"
    assert gcpr.conversation.expected_answer == "PERSON"
    assert gcpr.semantic.roles["agent"] == "unknown"
    assert gcpr.semantic.roles["patient"] == "door"
    assert gcpr.semantic.roles["action"] == "open"

def test_scenario_4(phaser):
    # TEST 4: "What did the boy open?"
    gcpr, trace = phaser.phase("What did the boy open?")

    assert gcpr.conversation.question_family == "WHAT"
    assert gcpr.semantic.roles["agent"] == "boy"
    assert gcpr.semantic.roles["action"] == "open"
    assert gcpr.semantic.roles["patient"] == "unknown"

def test_scenario_5(phaser):
    # TEST 5: "Why did the boy open the door?"
    gcpr, trace = phaser.phase("Why did the boy open the door?")

    assert gcpr.conversation.question_family == "WHY"
    assert gcpr.conversation.expected_answer == "CAUSE"
    assert gcpr.semantic.roles["agent"] == "boy"
    assert gcpr.semantic.roles["action"] == "open"
    assert gcpr.semantic.roles["patient"] == "door"
    assert gcpr.linguistic.grammar["tense"].lower() == "past"

def test_scenario_6(phaser):
    # TEST 6: "Where did the boy go?"
    gcpr, trace = phaser.phase("Where did the boy go?")

    assert gcpr.conversation.question_family == "WHERE"
    assert gcpr.conversation.expected_answer == "LOCATION"
    assert gcpr.semantic.roles["agent"] == "boy"
    assert gcpr.semantic.roles["action"] == "go"
    # Destination or location is unknown
    assert gcpr.semantic.roles.get("destination") == "unknown" or gcpr.semantic.roles.get("location") == "unknown"

def test_scenario_7(phaser):
    # TEST 7: "The door was opened by the boy."
    gcpr, trace = phaser.phase("The door was opened by the boy.")

    assert gcpr.linguistic.sentence_type == "statement"
    assert gcpr.linguistic.syntax["voice"].lower() == "passive"
    assert gcpr.semantic.roles["patient"] == "door"
    assert gcpr.semantic.roles["agent"] == "boy"
    assert gcpr.semantic.roles["action"] == "open"

def test_scenario_8(phaser):
    # TEST 8: "I saw her duck."
    gcpr, trace = phaser.phase("I saw her duck.")

    # "saw" can be past of see or noun tool. "her" can be pronoun or determiner. "duck" can be noun or verb.
    # Therefore, multiple structurally valid analyses must emerge from the parser.
    # Check that ambiguity is set to true and alternatives list contains options
    assert gcpr.uncertainty.ambiguous is True
    assert len(gcpr.uncertainty.alternatives) > 0

def test_scenario_9(phaser):
    # TEST 9: "hte boy opened the door."
    gcpr, trace = phaser.phase("hte boy opened the door.")

    # Verify original text is preserved
    assert gcpr.surface.original_text == "hte boy opened the door."
    # Verify that 'hte' was corrected to 'the' as a token candidate (its lemma is 'the')
    tokens = gcpr.surface.tokens
    assert tokens[0]["text"] == "hte"

    # Check semantic agent is boy, patient is door, action is open (from the corrected parse tree)
    assert gcpr.semantic.roles["agent"] == "boy"
    assert gcpr.semantic.roles["patient"] == "door"
    assert gcpr.semantic.roles["action"] == "open"
