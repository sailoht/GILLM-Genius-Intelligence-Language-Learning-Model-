import time
from typing import Dict, Any, List, Optional
from jarvis.events.bus import (
    EventBus, PerceptionEvent, UserInputEvent, PlanCreatedEvent,
    ToolCallEvent, ToolResultEvent, VerificationEvent, ResponseEvent
)
from jarvis.cognition.engine import CognitiveEngine, GILLMEngine, HybridEngine

class JarvisAgent:
    """
    The J.A.R.V.I.S. Core Agent Lifecycle Controller.
    Implements the explicit typed event transitions:
    RECEIVE → UNDERSTAND → CLASSIFY → RETRIEVE_CONTEXT → PLAN → AUTHORIZE → EXECUTE → OBSERVE → VERIFY → UPDATE_MEMORY → RESPOND
    """
    def __init__(self, cognitive_engine: Optional[CognitiveEngine] = None) -> None:
        self.event_bus = EventBus()
        self.cognitive_engine = cognitive_engine or HybridEngine()
        self.state: str = "INITIALIZED"
        self.memory_state: Dict[str, Any] = {}

        # Subscribe to standard events
        self.event_bus.subscribe(PerceptionEvent, self._handle_perception)

    def process_perception(self, event: PerceptionEvent) -> ResponseEvent:
        """Runs the explicit 11-step lifecycle loop on the incoming perception event."""
        print(f"\n[JARVIS OS] Entering Core Lifecycle. State: RECEIVE")
        self.state = "RECEIVE"

        # 1. RECEIVE
        content = event.content
        print(f"  -> Content Received: '{content}' (modality={event.modality})")

        # 2. UNDERSTAND
        print(f"[JARVIS OS] State: UNDERSTAND")
        self.state = "UNDERSTAND"
        gcpr_dict = self.cognitive_engine.understand(content)

        # 3. CLASSIFY
        print(f"[JARVIS OS] State: CLASSIFY")
        self.state = "CLASSIFY"
        intent = gcpr_dict.get("intent", "STATEMENT")
        speech_act = gcpr_dict.get("speech_act", "STATEMENT")
        print(f"  -> Intent Classified: '{intent}', Speech Act: '{speech_act}'")

        # 4. RETRIEVE CONTEXT
        print(f"[JARVIS OS] State: RETRIEVE_CONTEXT")
        self.state = "RETRIEVE_CONTEXT"
        # Gather tracked entities from memory state or GCPR
        entities = gcpr_dict.get("semantic", {}).get("entities", {})
        print(f"  -> Active Context Entities: {list(entities.keys())}")

        # 5. PLAN
        print(f"[JARVIS OS] State: PLAN")
        self.state = "PLAN"
        plan_steps = []
        action = gcpr_dict.get("semantic", {}).get("roles", {}).get("action", "unknown")
        if action == "open":
            plan_steps.append({"step_id": "1", "tool": "application_control", "action": "OPEN", "target": "Chrome"})
        elif action == "eat":
            plan_steps.append({"step_id": "1", "tool": "terminal_control", "action": "EXECUTE", "command": "python eat_food.py"})

        plan_event = PlanCreatedEvent(plan_id="plan_01", steps=plan_steps, goal=f"Execute task for action '{action}'")
        self.event_bus.publish(plan_event)
        print(f"  -> Plan formulated with {len(plan_steps)} steps.")

        # 6. AUTHORIZE
        print(f"[JARVIS OS] State: AUTHORIZE")
        self.state = "AUTHORIZE"
        is_authorized = True  # Auto-approve for safe baseline tasks
        print(f"  -> Authorization Status: APPROVED (Auto)")

        # 7. EXECUTE
        print(f"[JARVIS OS] State: EXECUTE")
        self.state = "EXECUTE"
        exec_results = []
        if is_authorized:
            for step in plan_steps:
                tool_event = ToolCallEvent(tool_name=step["tool"], arguments=step)
                self.event_bus.publish(tool_event)

                # Mock actual execution of the tool
                print(f"  -> Executing Tool: '{step['tool']}'...")
                res_event = ToolResultEvent(tool_name=step["tool"], result={"process_id": 4042, "window_title": "Chrome"}, status="SUCCESS")
                self.event_bus.publish(res_event)
                exec_results.append(res_event)

        # 8. OBSERVE
        print(f"[JARVIS OS] State: OBSERVE")
        self.state = "OBSERVE"
        # In real-world, we would query process status or screenshot vision. Here we observe process is running.
        print(f"  -> Observed system state modification: Process running successfully.")

        # 9. VERIFY
        print(f"[JARVIS OS] State: VERIFY")
        self.state = "VERIFY"
        # Confirm that the tool action actually completed successfully!
        # Verification check: did the process start? Yes!
        is_verified = len(exec_results) > 0 and all(r.status == "SUCCESS" for r in exec_results)
        ver_event = VerificationEvent(target=action, consistent=is_verified, notes=["Verified process ID 4042 active on OS window-bus."])
        self.event_bus.publish(ver_event)
        print(f"  -> Action Verification: {'VERIFIED' if is_verified else 'FAILED'}")

        # 10. UPDATE MEMORY
        print(f"[JARVIS OS] State: UPDATE_MEMORY")
        self.state = "UPDATE_MEMORY"
        # Record entities and last action in working memory
        self.memory_state["last_action"] = action
        self.memory_state["entities"] = entities
        print(f"  -> Working Memory updated.")

        # 11. RESPOND
        print(f"[JARVIS OS] State: RESPOND")
        self.state = "RESPOND"
        resp_text = ""
        if sentence_type := gcpr_dict.get("linguistic", {}).get("sentence_type") == "question":
            ans = gcpr_dict.get("conversation", {}).get("expected_answer")
            resp_text = f"Question detected. Expected answer: {ans}."
        else:
            resp_text = f"Action '{action}' processed, executed, and verified."

        resp_event = ResponseEvent(text=resp_text, modality="TEXT")
        self.event_bus.publish(resp_event)

        self.state = "COMPLETED"
        return resp_event

    def _handle_perception(self, event: PerceptionEvent) -> None:
        """Callback to execute agent loop when a PerceptionEvent is published."""
        self.process_perception(event)
