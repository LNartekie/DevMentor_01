import ollama

from prompts import SYSTEM_PROMPT

user_prompt = input("You: ")

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": user_prompt
        }
    ]
)

print("AI:", response["message"]["content"])