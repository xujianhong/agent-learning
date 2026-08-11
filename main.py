import time
from ollama import chat

from memory import load_memory, save_memory

conversation = load_memory()

if not conversation:
    conversation.append({
            "role": "system",
            "content": """
You are a Python programming tutor.

Your job is to help the user learn Python and AI agent development.

Rules:
- Explain concepts clearly.
- Assume the user understands basic programming.
- Give examples when useful.
- Don't just give the answer; explain why it works.
"""
})

while True:
	user_input = input("You: ")

	if user_input.lower() in {"exit","quit"}:
		save_memory(conversation)
		print("Memory saved.")
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

	save_memory(conversation)
	