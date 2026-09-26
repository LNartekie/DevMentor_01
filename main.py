import ollama

from prompts import SYSTEM_PROMPT


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


while True:
    user_prompt = input("You: ")

    messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    ai_reply = response["message"]["content"]

    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    print("\nAI:", ai_reply)
    print()