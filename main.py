import ollama

from prompts import SYSTEM_PROMPT


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


while True:
    user_prompt = input("You: ").strip()

    # Handle empty input
    if not user_prompt:
        print("Please enter a message.\n")
        continue

    # Exit the program
    if user_prompt == "/exit":
        print("Goodbye!")
        break

    # Reset conversation history but keep the system prompt
    if user_prompt == "/reset":
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        print("Conversation reset.\n")
        continue

    # Display conversation history without the system prompt
    if user_prompt == "/history":
        chat_history = [
            message for message in messages
            if message["role"] != "system"
        ]

        if not chat_history:
            print("No conversation history yet.\n")
        else:
            for number, message in enumerate(chat_history, start=1):
                role = message["role"].upper()
                content = message["content"]
                print(f"{number}. {role}: {content}\n")

        continue

    # Add user message to conversation history
    messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    try:
        # Send the full conversation to Ollama
        response = ollama.chat(
            model="llama3.2",
            messages=messages
        )

        ai_reply = response["message"]["content"]

    except ollama.ResponseError as error:
        print(f"\nModel error: {error}")
        print("Check that the selected Ollama model is installed.\n")

        # Remove the failed user message from history
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

        # Remove the failed user message from history
        messages.pop()
        continue

    # Save successful assistant response
    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    print("\nAI:", ai_reply)
    print()