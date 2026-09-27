import ollama

from config import APP_NAME, DEFAULT_MODEL
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

        # Different versions of the Ollama Python package may return
        # the model information slightly differently.
        if isinstance(response, dict):
            installed_models = response.get("models", [])
        else:
            installed_models = getattr(response, "models", [])

        models = []

        for item in installed_models:

            # Handle dictionary-style responses
            if isinstance(item, dict):
                model_name = item.get("model") or item.get("name")

            # Handle object-style responses
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

    # If Ollama returns no installed models
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

    # Pressing Enter selects the default model
    if not choice:
        return DEFAULT_MODEL

    # Check that the selection is a valid number
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

        # Add the user's message to conversation history
        messages.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )

        try:
            # Send conversation history to the selected model
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

            # Remove the failed user message
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
                print(f"\nUnexpected error: {error}\n")

            # Remove the failed user message
            messages.pop()
            continue

        # Save the assistant's successful response
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

    # Ask the user which installed model they want to use
    selected_model = select_model()

    print()
    print("=" * 50)
    print(APP_NAME)
    print(f"Model: {selected_model}")
    print("=" * 50)
    print("Commands: /reset  /history  /exit")
    print()

    # Start the chatbot using the selected model
    chat_loop(selected_model)


if __name__ == "__main__":
    main()