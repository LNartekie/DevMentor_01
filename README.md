# DevMentor

DevMentor is a local conversational AI assistant designed to help junior developers understand programming concepts in a clear and beginner-friendly way.

The application is built with Python and uses Ollama to communicate with a locally installed large language model. It supports multi-turn conversations, keeps track of conversation history during a session, follows a custom system prompt, and handles common user and connection errors without crashing.

The goal of this project is not only to build a chatbot, but also to demonstrate an understanding of how Python communicates with a local LLM, how prompt engineering affects responses, how conversation memory works, and how application state is managed.

---

## Features

DevMentor includes the following features:

- Runs locally using Ollama
- Uses the `llama3.2` local language model
- Accepts dynamic user input
- Uses a custom system prompt to guide the assistant's behaviour
- Supports multi-turn conversations
- Stores conversation history during the current session
- Uses `/reset` to clear conversation history while keeping the system prompt
- Uses `/history` to display the current user and assistant conversation
- Uses `/exit` to close the program cleanly
- Prevents blank input from being sent to the model
- Handles missing or invalid models
- Handles Ollama connection problems
- Organises code into reusable functions
- Separates configuration, prompts, and application logic into different files
- Allows the user to select an installed Ollama model at startup
- Supports `/save` for saving conversations as JSON files
- Supports `/load <filename>` for restoring saved conversations

---

## Architecture

DevMentor uses a simple local architecture without external chatbot frameworks.

The application flow is:

```text
User
  |
  v
Python Application
  |
  v
Conversation History
  |
  v
Ollama API
  |
  v
Local LLM
  |
  v
Generated Response
  |
  v
Python displays response to user
```

A more detailed view of the architecture is:

```text
                    +----------------------+
                    |        User          |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |  Python Application  |
                    |      main.py         |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   messages list      |
                    | Conversation State   |
                    +----------+-----------+
                               |
                 System + User + Assistant
                    messages are sent
                               |
                               v
                    +----------------------+
                    |     Ollama API       |
                    | localhost service    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |      Local LLM       |
                    |      llama3.2        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Generated Response   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Response appended    |
                    | to messages list     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Displayed to User    |
                    +----------------------+
```

The local LLM runs through Ollama.

The conversation state lives inside the Python application in a `messages` list.

The Ollama API acts as the communication layer between the Python application and the local language model.

On each request, the application sends the system prompt together with the relevant user and assistant messages so that the model has enough context to continue the conversation.

---

## Project Structure

```text
devmentor/
│
├── main.py
├── config.py
├── prompts.py
├── requirements.txt
├── README.md
├── experiment_results.txt
├── memory_results.txt
└── .venv/
```

The main files have the following responsibilities:

- `main.py` - controls the application, chat loop, conversation history, commands, error handling, and Ollama communication
- `config.py` - stores configuration values such as the application name and model name
- `prompts.py` - stores the system prompts used to control DevMentor's behaviour
- `requirements.txt` - lists the Python dependencies required to run the application
- `README.md` - documents the project, architecture, experiments, and lessons learned
- `experiment_results.txt` - stores observations from the prompt engineering experiment
- `memory_results.txt` - stores observations from the memory investigation

---

## Installation

### 1. Install Ollama

Install Ollama on your computer.

After installation, download a local model such as:

```bash
ollama pull llama3.2
```

You can check which models are installed using:

```bash
ollama list
```

For this project, the main model used was:

```text
llama3.2
```

---

### 2. Create a Virtual Environment

From inside the project folder, create a Python virtual environment:

```bash
py -m venv .venv
```

Activate the environment in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

When the environment is active, the terminal should show something similar to:

```text
(.venv)
```

---

### 3. Install Python Dependencies

Install the required packages using:

```bash
py -m pip install -r requirements.txt
```

The main dependency used in this project is:

```text
ollama>=0.3.0
```

---

## Running the Application

Before running DevMentor, make sure Ollama is running and the required model is installed.

Start the application with:

```bash
py main.py
```

When the application starts, it displays the application name, selected model, and available commands.

Example:

```text
==================================================
DevMentor AI Assistant
Model: llama3.2
==================================================
Commands: /reset  /history  /save  /load <file>  /exit

You:
```

The available commands are:

- `/reset` - clears the current conversation history while keeping the system prompt
- `/history` - displays the current user and assistant conversation
- `/exit` - closes the application cleanly

Example interaction:

```text
You: What is recursion?

AI: Recursion is a programming technique where a function calls itself...

You: Show me an example.

AI: Here is a Python example...
```

The second question does not repeat the word "recursion", but the model can still understand the context because the earlier messages are stored in the application's conversation history and sent again to Ollama.

---

## System Prompt Design

DevMentor uses a system prompt to define how the assistant should behave before the user begins asking questions.

The system prompt defines:

- **Role** - DevMentor acts as a programming tutor for junior developers
- **Audience** - explanations are aimed at beginners and junior developers
- **Explanation style** - concepts should first be explained in plain language before technical terminology is introduced
- **Examples** - examples should be short, relevant, and use Python unless another programming language is requested
- **Uncertainty handling** - if the model is unsure, it should clearly say so instead of inventing an answer
- **Tone** - the assistant should be patient, encouraging, clear, and direct

The purpose of the system prompt is to make the assistant's responses more suitable for learners instead of relying only on the model's default behaviour.

A stronger system prompt is more useful than a vague instruction because it gives the model clearer guidance about its role, audience, response style, examples, and behaviour when uncertain.

---

## Prompt Engineering Experiment

A controlled experiment was carried out to investigate how different system prompts affect the behaviour of the same language model.

The same `llama3.2` model was used for all three prompts.

Only the system prompt was changed.

### Questions Used

The same four questions were asked for all three prompts:

1. Explain REST APIs.
2. Explain recursion.
3. What is dependency injection?
4. Show me an example.

---

### Prompt A - Minimal

The minimal prompt was:

```text
You are a programming assistant.
```

This prompt gave the model very little guidance about:

- audience
- explanation style
- response structure
- examples
- tone
- uncertainty handling

The model was therefore given more freedom to decide how to answer.

---

### Prompt B - Detailed

The detailed prompt defined:

- the assistant's role
- the target audience
- explanation style
- example style
- tone
- behaviour when uncertain

The goal of Prompt B was to make the assistant behave more like a programming tutor for junior developers.

---

### Prompt C - Constrained

Prompt C used more explicit behavioural rules.

The rules included:

- explain concepts in plain English before showing code
- keep the introduction to no more than two sentences
- use Python for code examples unless another language is requested
- keep examples short and directly related to the question
- avoid introducing unrelated concepts
- clearly state when the model is uncertain

---

## Prompt Experiment Observations

All three prompts were able to answer the programming questions, but their style and structure differed.

Prompt A gave the model the most freedom because it provided very little behavioural guidance.

Prompt B produced more guided and beginner-focused responses because it defined the assistant's role, audience, and explanation style.

Prompt C produced the most controlled and predictable responses because it used explicit rules about response length, examples, relevance, and explanation order.

For all three prompts, the final question:

```text
Show me an example.
```

was interpreted as referring to the previous question about dependency injection.

This showed that conversation history helped the model understand what the vague follow-up question referred to.

The experiment therefore showed two different effects:

- the **system prompt influenced how the assistant responded**
- the **conversation history influenced what the assistant understood the user to be referring to**

---

## Prompt Experiment Questions and Answers

### 1. Which prompt was most useful, and why?

Prompt C was the most useful.

Its explicit rules made the responses more controlled, focused, and consistent.

It clearly instructed the model to explain concepts in plain English first, keep introductions short, use Python examples by default, and avoid unrelated information.

These constraints made the answers easier to follow as a beginner.

---

### 2. What differences did you see?

Prompt A gave the model the most freedom, so its answers were less predictable in structure and level of detail.

Prompt B produced more guided and beginner-friendly responses because it clearly defined the assistant's role, audience, explanation style, and behaviour.

Prompt C produced the most structured and controlled responses because it used explicit rules and limits.

In all three cases, the final question, "Show me an example," referred to the previous topic, dependency injection.

This demonstrated that conversation history played an important role in understanding follow-up questions.

---

### 3. Did more instructions always help?

More instructions helped when they were clear and relevant.

In this experiment, Prompt C was the most useful because the additional rules made the responses more focused and predictable.

However, too many unnecessary or conflicting instructions could make a prompt harder for the model to follow.

Therefore, instructions should be specific and purposeful rather than simply increasing the number of rules.

---

### 4. Which rules changed behaviour the most?

The rules that had the strongest visible effect were:

- explain the concept in plain English before showing code
- keep the introduction short
- use Python for code examples unless another language is requested
- avoid introducing unrelated concepts

These rules directly affected the structure, length, and relevance of the model's responses.

---

### 5. What happened when a rule was vague?

When instructions were vague, the model had more freedom to interpret them.

For example, an instruction such as:

```text
Keep the explanation short.
```

does not clearly define what "short" means.

A more measurable instruction such as:

```text
Keep the introduction to no more than two sentences.
```

gives the model a clearer limit and makes its behaviour more predictable.

---

## Memory Investigation

A memory experiment was performed to investigate whether the LLM truly remembers previous conversation turns.

### Test 1 - Full Conversation History

The following messages were sent in the same session:

```text
User: My favorite programming language is Python.

User: Explain interfaces.

User: What is my favorite programming language?
```

The model responded:

```text
You mentioned earlier that your favorite programming language is Python.
```

This showed that the model could use information from the earlier conversation.

However, this did not mean that the LLM had permanently stored the information.

The earlier message was still present in the application's `messages` list and was sent again to Ollama with the latest question.

---

### Test 2 - After Resetting the Conversation

The `/reset` command was used to clear the previous conversation history while keeping the system prompt.

The same question was asked again:

```text
What is my favorite programming language?
```

This time, the model did not know the answer.

Instead, it responded by asking questions such as what kinds of things the user likes to do with code and whether they had already tried any programming languages.

This showed that the information about Python was no longer available to the model.

---

## What the Memory Experiment Demonstrates

The experiment shows that the LLM itself does not permanently remember the conversation.

The apparent memory comes from the Python application.

The application stores conversation history in the `messages` list.

On each request, the relevant message history is sent to Ollama together with the new user message.

When `/reset` is used, earlier user and assistant messages are removed.

Because the model no longer receives the earlier statement about Python, it cannot reliably recall that information.

Therefore:

- **Application state** is stored in the Python program
- **Message history** contains previous user and assistant messages
- **Conversation context** is created by sending that history to the model on each request
- The LLM does not independently store the previous conversation between requests

---

## Challenge Questions

### 1. Why does the app send previous messages to the LLM?

The app sends previous messages because the LLM does not automatically remember earlier requests.

Each call to Ollama is treated as a new request.

To help the model understand the conversation, the Python application sends the previous user and assistant messages together with the new question.

This gives the model the context it needs to respond consistently.

---

### 2. What is the difference between system, user, and assistant messages?

The three main message roles are:

- **System message** - gives the model instructions about how it should behave, including its role, audience, tone, and explanation style
- **User message** - contains the question or instruction entered by the human user
- **Assistant message** - contains the response generated by the AI

Example:

```python
messages = [
    {"role": "system", "content": "You are DevMentor..."},
    {"role": "user", "content": "What is recursion?"},
    {"role": "assistant", "content": "Recursion is..."}
]
```

---

### 3. If you close Python and restart, why does the assistant "forget"?

The conversation history is stored in the Python application's memory while the program is running.

When the program closes, the `messages` list is lost because it only exists in the current Python process.

When the application starts again, a new `messages` list is created.

Therefore, the previous conversation is no longer available.

---

### 4. Is memory stored inside the LLM or inside the application?

For this project, conversation memory is stored inside the Python application, not inside the LLM.

The application keeps previous messages in the `messages` list and sends that list to Ollama on each request.

The LLM uses the context provided in the current request to generate a response.

It does not independently store the conversation between requests.

---

### 5. What happens when the conversation becomes extremely long?

Every language model has a limit on how much text it can process in one request.

This limit is called the **context window**.

As more messages are added to the conversation, the `messages` list becomes larger and uses more tokens.

If the conversation becomes too long, it may exceed the model's context window.

Possible strategies for managing long conversations include:

- removing the oldest non-essential messages
- summarising older sections of the conversation
- keeping only the most relevant messages
- using a sliding window of recent messages

These approaches reduce the amount of context sent while keeping important information available to the model.

---

### 6. Why is "You are helpful." a weak system prompt? How would you improve it?

"You are helpful." is weak because it gives the model very little information about how it should behave.

It does not define:

- the assistant's role
- the target audience
- the subject area
- the explanation style
- whether examples should be included
- what to do when uncertain

A stronger system prompt would be:

```text
You are DevMentor, a programming tutor for junior developers.
Explain concepts in plain language before introducing technical terms.
Use short Python examples when useful.
Keep answers focused and clearly state when you are uncertain.
```

This gives the model clearer guidance and makes its behaviour more predictable.

---

### 7. After the LLM replies, what should happen to `messages` before the next user turn, and why?

After the LLM generates a response, the assistant's reply should be added to the `messages` list.

Example:

```python
messages.append(
    {
        "role": "assistant",
        "content": ai_reply
    }
)
```

This is important because the model needs to see both the user's previous messages and its own previous responses when processing the next request.

If the assistant response is not stored, the conversation history becomes incomplete.

This could cause the model to lose important context, repeat information, or respond inconsistently.

---

## Bonus Features

Three optional bonus features were implemented to extend the functionality of DevMentor.

### Bonus 1 - Model Selection

At startup, DevMentor retrieves the Ollama models installed on the local computer and allows the user to choose which model should be used for the session.

Example:

```text
Available models:

1. qwen3:1.7b
2. qwen:latest
3. mistral:latest
4. llama3.2:latest

Select a model number (press Enter for llama3.2):
```

If the user presses Enter without making a selection, DevMentor uses the default model defined in `config.py`.

This feature makes the application more flexible because different local models can be tested without modifying the Python source code.

---

### Bonus 2 - Save Conversations

DevMentor supports the `/save` command.

When the user enters:

```text
/save
```

the current conversation history is stored as a JSON file inside the `conversations` directory.

Example:

```text
Conversation saved to:
conversations\chat_2026_09_27_211500.json
```

The saved JSON file contains the system, user, and assistant messages from the current conversation.

Example structure:

```json
[
  {
    "role": "system",
    "content": "..."
  },
  {
    "role": "user",
    "content": "My favorite framework is Django."
  },
  {
    "role": "assistant",
    "content": "..."
  }
]
```

Saving the `messages` list makes it possible to preserve the conversation after the Python application has been closed.

---

### Bonus 3 - Load Conversations

DevMentor supports the `/load` command for restoring a previously saved conversation.

Example:

```text
/load chat_2026_09_27_211500.json
```

When a conversation is loaded, the saved messages are placed back into the application's `messages` list.

The `/history` command can then be used to confirm that the earlier messages have been restored.

This was tested by first entering:

```text
My favorite framework is Django.
```

The conversation was saved and the application was closed.

After restarting DevMentor, the saved JSON conversation was loaded. The restored conversation history contained the earlier statement about Django.

When asked:

```text
Based on our earlier conversation, what framework did I say was my favorite?
```

DevMentor responded that Django was the favorite framework.

This demonstrates that the model did not permanently remember the information. Instead, the Python application restored the saved conversation state and sent the earlier context back to the language model.

---

## Available Commands

DevMentor supports the following commands:

| Command | Purpose |
|---|---|
| `/reset` | Clears the current conversation while keeping the system prompt |
| `/history` | Displays user and assistant conversation history |
| `/save` | Saves the current conversation to a JSON file |
| `/load <filename>` | Loads a previously saved conversation |
| `/exit` | Ends the program cleanly |

---

## Updated Project Structure

```text
devmentor/
│
├── main.py
├── config.py
├── prompts.py
├── requirements.txt
├── README.md
├── experiment_results.txt
├── memory_results.txt
├── conversations/
│   └── chat_YYYY_MM_DD_HHMMSS.json
└── .venv/
```

The `conversations` directory is created automatically when the `/save` command is used.

## Key Learning

This project demonstrated that a conversational AI application is not created by the language model alone.

The main components work together:

```text
Prompt
+
Message History
+
Application State
+
Ollama API
+
Local LLM
=
Conversational AI Application
```

The system prompt controls how the model should behave.

The Python application manages the conversation state.

The `messages` list provides context.

The Ollama API connects the Python application to the local language model.

The LLM generates the response based on the information provided in the current request.

---

## Conclusion

DevMentor demonstrates the basic components required to build a local conversational AI assistant without relying on higher-level chatbot frameworks.

The project successfully connects Python to a local Ollama model, applies prompt engineering, maintains multi-turn conversation history, supports conversation controls, and handles common errors.

The prompt engineering experiment showed that more specific instructions can make model behaviour more predictable, while the memory investigation demonstrated that conversation memory is managed by the application rather than stored permanently inside the LLM.

Building the application directly with Python and Ollama provided a clearer understanding of how prompts, APIs, message history, application state, and local language models work together to create a conversational AI system.