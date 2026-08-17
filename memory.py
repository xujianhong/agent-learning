import json

from ollama import chat



MODEL = "qwen:latest"


MEMORY_SCHEMA = {
	"type": "object",
	"properties":{
		"memories":{
			"type": "array",
			"items": {
				"type": "object",
				"properties":{
					"text":{
						"type": "string"
					},
					"category":{
						"type": "string",
						"enum":[
							"fact",
							"preference",
							"goal",
							"interest",
							"project",
							"constraint",
						],
					},
					"confidence":{
						"type": "number"
					},
				},
				"required": [
					"text",
					"category",
					"confidence",
				],
			},
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

Examples:

User:
"I am learning Python."

Memory:
"User is learning Python"

User:
"I prefer Python over JavaScript."

Memory:
"User prefers Python over JavaScript"

User:
"I am building an AI agent."

Memory:
"User is building an AI agent"

If there is nothing worth remembering,
return an empty memories array.

User message:
{user_message}
"""
	print(f"\n{prompt}")
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
	print(f"\n{result}")
	try:
		data = json.loads(result)

		return data.get("memories",[])

	except json.JSONDecodeError:
		print("\n[Memory extraction failed]")
		return []