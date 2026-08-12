from gillm.conversation.context import ConversationContext

def test_conversation_context_and_coreference():
    context = ConversationContext()

    # Turn 1: "What is quantum tunneling?"
    # Represent as parsed GCPR
    gcpr_data_1 = {
        "surface": {
            "original_text": "What is quantum tunneling?",
            "tokens": []
        },
        "linguistic": {
            "sentence_type": "question"
        },
        "semantic": {
            "roles": {
                "action": "be",
                "identity": "quantum tunneling"
            },
            "entities": {}
        }
    }

    context.add_turn("What is quantum tunneling?", gcpr_data_1)
    assert context.active_topic == "quantum tunneling"

    # Turn 2: "Why does it happen?"
    gcpr_data_2 = {
        "surface": {
            "original_text": "Why does it happen?",
            "tokens": []
        },
        "linguistic": {
            "sentence_type": "question"
        },
        "semantic": {
            "roles": {
                "action": "happen",
                "patient": "it",
                "cause": "unknown"
            },
            "entities": {}
        }
    }

    resolved_gcpr = context.resolve_coreferences(gcpr_data_2)
    entities = resolved_gcpr["semantic"]["entities"]

    assert "it" in entities
    assert entities["it"]["coreference"] == "quantum tunneling"
