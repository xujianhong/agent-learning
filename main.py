from ollama import chat

from memory import extract_memories
from vector_memory import(
	add_memory,
	search_memory,
)

from memory_manager import process_memory

MODEL = "qwen:latest"


conversation=[
	{
		"role": "system",
		"content": """
You are a Python programming tutor.

Your job is to help the user learn Python 
and AI agent development.

Explain concepts clearly.

Give examples when useful.

Use relevant memories about the user
when they help answer the question.
"""
	}
]

while True:
	user_input = input("\nYou: ")

	if user_input.lower() in {"exit","quit"}:
		break

	# ------------------------------------------------
	# 1. Retrieve relevant long-term memories
	# ------------------------------------------------
	relevant_memories = search_memory(
		user_input,
		n_results = 3,
	)

	memory_context = ""

	if relevant_memories:

		memory_context = (
			"\nRelevant memories about the user:\n"
		)

		for memory in relevant_memories:
			memory_context += f"- {memory}\n"

	# ------------------------------------------------
	# 2. Add user message
	# ------------------------------------------------
	user_message = f"""
{memory_context}

Current user message:

{user_input}
"""

	print(f"\n{user_message}")
	conversation.append({
		"role": "user",
		"content": user_message,
	})

	# ------------------------------------------------
	# 3. Generate response
	# ------------------------------------------------

	response = chat(
		model = MODEL,
		messages = conversation,
	)

	answer = response.message.content

	print(f"\nAssistant: {answer}")

	conversation.append({
		"role": "assistant",
		"content": answer,
	})

	# ------------------------------------------------
	# 4. Extract possible memories
	# ------------------------------------------------

	new_memories = extract_memories(
		user_input
	)

	# ------------------------------------------------
	# 5. Store new memories
	# ------------------------------------------------

	for memory in new_memories:
		process_memory(memory)