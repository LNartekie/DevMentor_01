import ollama

from config import APP_NAME, DEFAULT_MODEL
from prompts import SYSTEM_PROMPT


def build_initial_history():
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


def get_ai_response(messages):
    response = ollama.chat(
        model=DEFAULT_MODEL,
        messages=messages
    )

    return response["message"]["content"]


def reset_conversation():
    print("Conversation reset.\n")
    return build_initial_history()


def display_history(messages):
    chat_history = [
        message for message in messages
        if message["role"] != "system"
    ]

    if not chat_history:
        print("No conversation history yet.\n")
        return

    for number, message in enumerate(chat_history, start=1):
        role = message["role"].upper()
        content = message["content"]

        print(f"{number}. {role}: {content}\n")


def chat_loop():
    messages = build_initial_history()

    while True:
        user_prompt = input("You: ").strip()

        # Handle empty input
        if not user_prompt:
            print("Please enter a message.\n")
            continue

        # Exit
        if user_prompt == "/exit":
            print("Goodbye!")
            break

        # Reset conversation
        if user_prompt == "/reset":
            messages = reset_conversation()
            continue

        # Show conversation history
        if user_prompt == "/history":
            display_history(messages)
            continue

        # Add user message
        messages.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )

        try:
            ai_reply = get_ai_response(messages)

        except ollama.ResponseError as error:
            print(f"\nModel error: {error}")
            print("Check that the selected Ollama model is installed.\n")

            messages.pop()
            continue

        except Exception as error:
            error_message = str(error).lower()

            if "connection" in error_message or "refused" in error_message:
                print(
                    "\nUnable to connect to Ollama. "
                    "Make sure Ollama is running and try again.\n"
                )
            else:
                print(f"\nUnexpected error: {error}\n")

            messages.pop()
            continue

        # Save assistant reply
        messages.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

        print("\nAI:", ai_reply)
        print()


def main():
    print("=" * 50)
    print(APP_NAME)
    print(f"Model: {DEFAULT_MODEL}")
    print("=" * 50)
    print("Commands: /reset  /history  /exit")
    print()

    chat_loop()


if __name__ == "__main__":
    main()