import json

from ollama import chat



MODEL = "qwen:latest"


MEMORY_SCHEMA = {
	"type": "object",
	"properties":{
		"memories":{
			"type": "array",
			"items": {
				"type": "string"
			}
		}
	},
	"required": ["memories"]
}

def extract_memories(user_message):
	prompt = f"""
You are a long-term memory extraction system.

Your ONlY job is to identify useful information about
the USER from the user's message.

Do not answer the user.

Do not explain your reasoning.

Do not create example memories.

Extract only information that the user actually stated
or clearly expressed.

Useful memories include:

- User facts
- User Preferences
- User goals
- User interests
- Ongoing projects
- Long-term habits
- Important constraints

Do NOT remember:

- Questions the user asks
- General knowledge
- Temporary requests
- Information from the assistant
- Information invented by you
- Information about other people
- One-time requests
- Greetings
- Casual conversation
- Information that is only relevant to this one question

IMPORTANT:

The strings inside "memories" must contain REAL information
from the user's message.

For example, if the user says:

I am learning Python because I want to build AI agents.

The correct output is:
{{
	"memories":[
		"User is learning Python",
		"User wants to build AI agents"
	]
}}

Do NOT output the words "memory 1", "memory 2", or any
other placeholder text.

If the user's message contains no useful long-term information,
return an empty memories array.

User message:
{user_message}
"""
	# print(f"\n{prompt}")
	response = chat(
		model = MODEL,
		messages =[
			{
				"role": "user",
				"content": prompt,
			}
		],
		format=MEMORY_SCHEMA,
	)

	result = response.message.content

	try:
		data = json.loads(result)

		memories = data.get("memories",[])

		return [
			memory.strip()
			for memory in memories
			if isinstance(memory,str)
			and memory.strip()
		]

	except json.JSONDecodeError:
		print("\n[Memory extraction failed]")
		return []