from memory import extract_memories


test_messages = [
	"I'm learning Python because I want to build AI agents.",

	"I prefer learning by building projects instead of watching tutorials.",

	"What is a Python dictionary?",

	"I am currently building a weather application.",

	"The capital of France is Paris.",
]

for message in test_messages:

	print("\nUser:")
	print(message)

	memories = extract_memories(message)

	print("Extracted memories:")

	for memory in memories:
		print("-", memory)