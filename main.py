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

    # Add the user's message to conversation history
    messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Send the full conversation to Ollama
    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    ai_reply = response["message"]["content"]

    # Save the assistant's response to conversation history
    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    print("\nAI:", ai_reply)
    print()