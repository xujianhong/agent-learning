import time
from ollama import chat

from memory import (
	load_memory, 
	save_memory,
	extract_memories,
	merge_memories,
)

memory = load_memory()

memory_context = f"""
Here are some things you remember about the user.

Facts:
{memory['facts']}

Preferences:
{memory['preferences']}

Goals:
{memory['goals']}
"""

conversation=[
	{
		"role": "system",
		"content": """
You are a Python programming tutor.

Your job is to help the user learn Python 
and AI agent development.

Explain concepts clearly and give examples
when useful.

{memory_context}
"""
	}
]



while True:
	user_input = input("You: ")

	if user_input.lower() in {"exit","quit"}:

		new_memories = extract_memories(conversation)

		memory = merge_memories(
			memory, 
			new_memories
		)

		save_memory(memory)

		print("Long-term memory saved.")

		break

	conversation.append({
		"role": "user",
		"content": user_input,
	})

	# start = time.perf_counter()
	# print(f"[{time.perf_counter() - start:.2f}s] Starting qwen ")

	response = chat(
		model = "qwen:latest",
		messages = conversation,
	)

	# print(f"[{time.perf_counter() - start:.2f}s] Finished qwen")
	answer = response.message.content

	print(f"Assistant: {answer}")

	# print(f"[{time.perf_counter() - start:.2f}s] Finished printing answer")

	conversation.append({
		"role": "assistant",
		"content": answer,
	})

	