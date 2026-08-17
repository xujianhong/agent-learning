from ollama import chat


schema = {
	"type": "object",
	"properties": {
		"action": {
			"type": "string",
			"enum": ["search", "final"]
		},
		"query": {
			"type": "string"
		},
		"answer": {
			"type": "string"
		}
	},
	"required": ["action"]
}


response = chat(
	model="qwen:latest",
	messages=[
		{
			"role": "user",
			"content": """
Research this question:

What is retrieval augmented generation?

Decide whether you need to search the web.
"""
		}
	],
	format=schema
)

print(response["message"]["content"])