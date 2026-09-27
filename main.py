import json
import os
from datetime import datetime

import ollama

from config import APP_NAME, DEFAULT_MODEL, CONVERSATIONS_DIR
from prompts import SYSTEM_PROMPT


def build_initial_history():
    """Create a fresh conversation containing only the system prompt."""

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


def select_model():
    """Allow the user to select one of the Ollama models installed locally."""

    try:
        response = ollama.list()

        if isinstance(response, dict):
            installed_models = response.get("models", [])
        else:
            installed_models = getattr(response, "models", [])

        models = []

        for item in installed_models:

            if isinstance(item, dict):
                model_name = item.get("model") or item.get("name")

            else:
                model_name = (
                    getattr(item, "model", None)
                    or getattr(item, "name", None)
                )

            if model_name:
                models.append(model_name)

    except Exception as error:
        print(
            "\nCould not retrieve installed models."
            f"\nUsing default model: {DEFAULT_MODEL}"
            f"\nDetails: {error}\n"
        )

        return DEFAULT_MODEL

    if not models:
        print(
            "\nNo installed Ollama models were found."
            f"\nUsing default model: {DEFAULT_MODEL}\n"
        )

        return DEFAULT_MODEL

    print("\nAvailable models:")

    for number, model_name in enumerate(models, start=1):
        print(f"{number}. {model_name}")

    choice = input(
        f"\nSelect a model number "
        f"(press Enter for {DEFAULT_MODEL}): "
    ).strip()

    if not choice:
        return DEFAULT_MODEL

    if choice.isdigit():
        choice_number = int(choice)

        if 1 <= choice_number <= len(models):
            return models[choice_number - 1]

    print(
        "\nInvalid selection."
        f"\nUsing default model: {DEFAULT_MODEL}\n"
    )

    return DEFAULT_MODEL


def get_ai_response(messages, model):
    """Send the conversation to Ollama and return the AI response."""

    response = ollama.chat(
        model=model,
        messages=messages
    )

    return response["message"]["content"]


def reset_conversation():
    """Clear conversation history while keeping the system prompt."""

    print("Conversation reset.\n")

    return build_initial_history()


def display_history(messages):
    """Display user and assistant messages without the system prompt."""

    chat_history = [
        message
        for message in messages
        if message["role"] != "system"
    ]

    if not chat_history:
        print("No conversation history yet.\n")
        return

    for number, message in enumerate(chat_history, start=1):
        role = message["role"].upper()
        content = message["content"]

        print(f"{number}. {role}: {content}\n")


def save_conversation(messages):
    """Save the current conversation history to a JSON file."""

    os.makedirs(
        CONVERSATIONS_DIR,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y_%m_%d_%H%M%S"
    )

    filename = os.path.join(
        CONVERSATIONS_DIR,
        f"chat_{timestamp}.json"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            messages,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Conversation saved to: {filename}\n"
    )


def load_conversation(filename):
    """Load a previously saved conversation from a JSON file."""

    # If the user only gives the filename,
    # look inside the conversations folder.
    if not os.path.dirname(filename):
        filename = os.path.join(
            CONVERSATIONS_DIR,
            filename
        )

    if not os.path.exists(filename):
        print(
            f"Conversation file not found: {filename}\n"
        )

        return None

    try:
        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:
            messages = json.load(file)

    except (json.JSONDecodeError, OSError) as error:
        print(
            f"Could not load conversation: {error}\n"
        )

        return None

    print(
        f"Conversation loaded from: {filename}\n"
    )

    return messages


def chat_loop(model):
    """Run the main DevMentor conversation loop."""

    messages = build_initial_history()

    while True:
        user_prompt = input("You: ").strip()

        # Handle empty input
        if not user_prompt:
            print("Please enter a message.\n")
            continue

        # Exit the application
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

        # Save conversation
        if user_prompt == "/save":
            save_conversation(messages)
            continue

        # Load conversation
        if user_prompt.startswith("/load "):
            filename = user_prompt[6:].strip()

            loaded_messages = load_conversation(
                filename
            )

            if loaded_messages is not None:
                messages = loaded_messages

            continue

        # Handle /load without a filename
        if user_prompt == "/load":
            print(
                "Please provide a filename.\n"
                "Example: /load chat_2026_09_27_140000.json\n"
            )
            continue

        # Handle unknown commands
        if user_prompt.startswith("/"):
            print(
                f"Unknown command: {user_prompt}\n"
            )
            continue

        # Add the user's message to history
        messages.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )

        try:
            ai_reply = get_ai_response(
                messages,
                model
            )

        except ollama.ResponseError as error:
            print(f"\nModel error: {error}")
            print(
                "Check that the selected Ollama model "
                "is installed.\n"
            )

            messages.pop()
            continue

        except Exception as error:
            error_message = str(error).lower()

            if (
                "connection" in error_message
                or "refused" in error_message
            ):
                print(
                    "\nUnable to connect to Ollama. "
                    "Make sure Ollama is running "
                    "and try again.\n"
                )

            else:
                print(
                    f"\nUnexpected error: {error}\n"
                )

            messages.pop()
            continue

        # Save the assistant's response
        messages.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

        print("\nAI:", ai_reply)
        print()


def main():
    """Start DevMentor."""

    selected_model = select_model()

    print()
    print("=" * 50)
    print(APP_NAME)
    print(f"Model: {selected_model}")
    print("=" * 50)
    print(
        "Commands: "
        "/reset  "
        "/history  "
        "/save  "
        "/load <file>  "
        "/exit"
    )
    print()

    chat_loop(selected_model)


if __name__ == "__main__":
    main()