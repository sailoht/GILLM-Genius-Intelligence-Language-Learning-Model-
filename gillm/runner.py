import sys
from gillm.gsl.phaser import GSLPhaser
from gillm.conversation.context import ConversationContext
from gillm.intent.search_key import generate_search_key

def main():
    print("==================================================")
    print("GILLM 1.0 — Genius Intelligence Language Learning Model")
    print("GSL — GILLM Structure Library Interactive Shell")
    print("==================================================")
    print("Type your message and press Enter.")
    print("Use command '/debug on' or '/debug off' to toggle PhaseTrace.")
    print("Type 'exit' or 'quit' to exit.")
    print("==================================================")

    phaser = GSLPhaser()
    context = ConversationContext()
    debug_mode = False

    while True:
        try:
            user_input = input("You > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting shell...")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if user_input.lower() == "/debug on":
            debug_mode = True
            print("System > PhaseTrace debug is now ENABLED.")
            continue
        elif user_input.lower() == "/debug off":
            debug_mode = False
            print("System > PhaseTrace debug is now DISABLED.")
            continue

        gcpr, trace = phaser.phase(user_input, context)
        context.add_turn(user_input, gcpr.to_dict())

        print("GILLM > ")
        if gcpr.linguistic.sentence_type == "question":
            print("Question detected.")
            print(f"Expected answer: {gcpr.conversation.expected_answer}.")
        else:
            print("Statement processed.")

        s_key = generate_search_key(gcpr.to_dict())
        if s_key and s_key.concept != "unknown":
            print(f"Generated SearchKey: (concept='{s_key.concept}', intent='{s_key.intent}')")

        if debug_mode:
            print("\n" + "=" * 40)
            print("DEBUG PHASING TRACE:")
            print("=" * 40)
            print(trace.format_trace())
            print("=" * 40 + "\n")

if __name__ == "__main__":
    main()
