from gillm.input.manager import InputManager

def test_tokenizer_and_input_manager():
    manager = InputManager()
    tokens = manager.process_input("The boy opened the door?")

    assert len(tokens) == 6
    assert tokens[0].text == "The"
    assert tokens[0].token_type == "WORD"
    assert tokens[0].position == 0

    assert tokens[2].text == "opened"
    assert tokens[2].token_type == "WORD"
    assert tokens[2].position == 2

    assert tokens[5].text == "?"
    assert tokens[5].token_type == "PUNCTUATION"
    assert tokens[5].position == 5
