import time
from ollama import chat

from vector_memory import search_memory


conversation=[
	{
		"role": "system",
		"content": """
You are a Python programming tutor.

Your job is to help the user learn Python 
and AI agent development.

Explain concepts clearly and give examples
when useful.
"""
	}
]

while True:
	user_input = input("You: ")

	if user_input.lower() in {"exit","quit"}:
		break

	# Search long-term memory
	relevant_memories = search_memory(
		user_input,
		n_results = 3,
	)

	memory_context = "\n".join(
		f"- {memory}"
		for memory in relevant_memories
	)

	#Add memory to the current request
	user_message = f"""
Relevant memories about the user:

{memory_context}

Current user message:

{user_input}
"""
	print(f"\n{user_message}")
	conversation.append({
		"role": "user",
		"content": user_message,
	})

	# start = time.perf_counter()
	# print(f"[{time.perf_counter() - start:.2f}s] Starting qwen ")

	response = chat(
		model = "qwen:latest",
		messages = conversation,
	)

	# print(f"[{time.perf_counter() - start:.2f}s] Finished qwen")
	answer = response.message.content

	print(f"\nAssistant: {answer}")

	# print(f"[{time.perf_counter() - start:.2f}s] Finished printing answer")

	conversation.append({
		"role": "assistant",
		"content": answer,
	})