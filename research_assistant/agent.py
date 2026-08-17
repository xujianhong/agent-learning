from ollama import chat

from search import search_web
from prompts import SYSTEM_PROMPT

class ResearchAgent:

	def __init__(self, model="qwen:latest"):
		self.model = model

	def research(self, question):

		print("\nSearching the web...\n")

		#Step 1: Search
		results = search_web(question)

		#Step 2: Format search results
		research_context = ""

		for i, result in enumerate(results, start=1):

			research_context += f"""
SOURCE {i}

Title:
{result["title"]}

URL:
{result["url"]}

Snippet:
{result["snippet"]}

-------------------------
"""

		#Step 3: Ask the LLM to synthesize the information 
		response = chat(
			model=self.model,
			messages=[
				{
					"role": "system",
					"content":SYSTEM_PROMPT
				},
				{
					"role": "user",
					"content": f"""
Research question:

{question}

Here are the web search results:

{research_context}

Using these sources, answer the research question.
"""
				}
			]
		)

		return response["message"]["content"]