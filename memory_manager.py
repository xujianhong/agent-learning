import json

from ollama import chat

from vector_memory import (
	add_memory,
	update_memory,
	delete_memory,
	search_memory,
)


MODEL = "qwen:latest"

DECISION_SCHEMA= {
	"type": "object",
	"properties":{
		"action": {
			"type": "string",
			"enum": [
				"ADD",
				"UPDATE",
				"DELETE",
				"IGNORE",
			],
		},
		"reason": {
			"type": "string"
		},
		"new_text": {
			"type": "string"
		},
		"category": {
			"type": "string"
		},
	},
	"required":[
		"action",
		"reason",
		"new_text",
		"category",
	],
}


def decide_memory_action(
	candidate,
	existing_memories,
):

	existing_text = ""

	for memory in existing_memories:

		existing_text += f"""
ID: {memory['id']}
Memory: {memory['text']}
Category: {memory['metadata'].get('category')}
Distance: {memory['distance']}
"""
	prompt = f"""
You are a memory management system.

A new piece of information was extracted
from the user.

NEW INFORMATION:

{candidate['text']}

Category:
{candidate['category']}

Existing potentially related memories:

{existing_text}

Decide what should happen.

Rules:

ADD:
Use ADD when the information is new and does
not conntradict or duplicate an existing memory.

UPDATE:
Use UPDATE when the new information replaces,
corrects, or changes an existing memory.

DELETE:
Use DELETE when the use clearly says that an
existing memory is no longer true and these is
no replacement.

IGNORE:
Use IGNORE when the information is not useful
or is already represented by an existing memory.

Example:

Existing:
"User now prefers JavaScript"

New:
"User now prefers Python"

Correct:
UPDATE

New memory:
"User prefers Python"

Another example:

Existing:
"User is buildig a weather app"

New:
"I stopped working on my weather app"

Correct:
DELETE

Return ONLY the JSON structure.
"""

	print(f"\n{prompt}")
	response = chat(
		model=MODEL,
		messages=[
			{
				"role": "user",
				"content": prompt,
			}
		],
		format=DECISION_SCHEMA,
	)

	try:
		return json.loads(
			response.message.content
		)

	except json.JSONDecodeError:

		print("[Memory decision failed]")

		return {
			"action": "IGNORE",
			"reason": "Invalid JSON",
			"new_text": "",
			"category": "fact",
		}

def process_memory(candidate):

	#Search for semantically related memories.
	existing_memories = search_memory(
		candidate["text"],
		n_results=3,
		max_distance=0.7,
	)

	decision = decide_memory_action(
		candidate,
		existing_memories,
	)

	action = decision["action"]

	print(f"[Memory decision] {action}")

	print(f"[Reason] {decision['reason']}")

	# -----------------------------------------
	# ADD
	# -----------------------------------------

	if action == "ADD":

		add_memory(
			text=candidate["text"],
			category=candidate["category"],
			confidence=candidate["confidence"],
		)

	# -----------------------------------------
	# UPDATE
	# -----------------------------------------

	elif action == "UPDATE":

		if existing_memories:

			target = existing_memories[0]

			update_memory(
				memory_id=target["id"],
				new_text=decision["new_text"],
				category=candidate["category"],
				confidence=candidate["confidence"],
			)

	# -----------------------------------------
	# DELETE
	# -----------------------------------------

	elif action == "DELETE":

		if existing_memories:

			target = existing_memories[0]

			delete_memory(
				target["id"]
			)

	# -----------------------------------------
	# IGNORE
	# -----------------------------------------

	elif action == "IGNORE":

		print("[Memory ignored]")