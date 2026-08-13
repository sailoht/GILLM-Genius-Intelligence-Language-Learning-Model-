from jarvis.events import PerceptionEvent, ResponseEvent
from jarvis.agent import JarvisAgent
from jarvis.cognition import GILLMEngine

def test_jarvis_agent_core_loop():
    # Instantiate with GILLM engine
    agent = JarvisAgent(cognitive_engine=GILLMEngine())

    # Send a PerceptionEvent: "The boy opened the door."
    event = PerceptionEvent(
        source="user",
        modality="TEXT",
        content="The boy opened the door."
    )

    # Execute loop
    resp = agent.process_perception(event)

    assert resp is not None
    assert isinstance(resp, ResponseEvent)
    assert "opened" in resp.text or "open" in resp.text
    assert agent.state == "COMPLETED"
    assert agent.memory_state["last_action"] == "open"
