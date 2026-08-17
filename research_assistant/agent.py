import json

from ollama import chat

from search import search_web
from prompts import SYSTEM_PROMPT

DECISION_SCHEMA = {
	"type": "object",
	"properties":{
		"action":{
			"type": "string",
			"enum": ["search", "final"]
		},
		"query":{
			"type": "string"
		},
		"answer":{
			"type": "string"
		}
	},
	"required": ["action"]
}

class ResearchAgent:

	def __init__(self, model="qwen:latest", max_steps=5):
		self.model = model
		self.max_steps = max_steps

	def research(self, question):

		conversation = [
			{
				"role": "system",
				"content": SYSTEM_PROMPT
			},
			{
				"role": "user",
				"content": question
			}
		]

		for step in range(self.max_steps):

			print(f"\n--- Agent Step {step + 1} ---")

			response = chat(
				model=self.model,
				messages=conversation,
				format=DECISION_SCHEMA
			)

			content = response["message"]["content"]

			print("LLM decision:")
			print(content)

			# Try to parse the LLM's JSON response
			try:

				decision = json.loads(content)

			except json.JSONDecodeError:

				print("The LLM returned invalid JSON.")
				continue

			action = decision.get("action")

			# --------------------------------
			# SEARCH
			# --------------------------------

			if action == "search":

				query = decision.get("query")

				print(f"\nSearching for: {query}")

				results = search_web(query)

				research_context = ""

				for i, result in enumerate(results, start= 1):
					research_context +=f"""
SOURCE {i}

Title:
{result["title"]}

URL:
{result["url"]}

Snippet:
{result["snippet"]}

----------------------------
"""
				# Give the search results back to the LLM

				conversation.append({
					"role": "assistant",
					"content": content
				})

				conversation.append({
					"role": "user",
					"content": f"""
Search results for:

{query}

{research_context}

Use these results to decide what to do next.

Remember:

- Search again if you need more information.
- Give a final answer if you have enough information.
"""
				})

			# --------------------------------
			# FINAL
			# --------------------------------

			elif action == "final":

				print("\nResearch complete.")

				return decision.get("answer")

			else:

				print(f"Unknown action: {action}")

		return "I was unable to complete the research within the allowed number of steps."