import json
from ollama import chat
from pathlib import Path

# MEMORY_FILE = Path("memory.json")
MEMORY_FILE = Path("long_term_memory.json") 

def load_memory():
	if not MEMORY_FILE.exists():
		return {
			"facts":[],
			"preferences":[],
			"goals":[],
		}
	
	with open(MEMORY_FILE,"r", encoding="utf-8") as file:
		return json.load(file)

def save_memory(conversation):
	with open(MEMORY_FILE, "w", encoding="utf-8") as file:
		json.dump(conversation, file, indent=2, ensure_ascii=False)


def extract_memories(conversation):
	prompt ="""
Analyze the conversation below.

Identify information about the user that would be useful
to remember in future conversations.

Only extract information that is:

- Personal facts about the user
- User preferences
- User goals
- Long-term interests
- Important ongoing projects

Do NOT extract:

- Temporary questions
- General knowledge
- Information about other people
- Things that are only relevant to this conversation

Return ONLY valid JSON in this format:

{
	"facts": [],
	"preferences": [],
	"goals": []
}

Conversation:

"""
	for message in conversation:
		role = message.get("role")
		if role in "user":
			prompt += f"{message['role']}: {message['content']}\n"

	print(prompt)
	response = chat(
		model = "qwen:latest",
		messages = [
			{
				"role": "user", 
				"content": prompt,
			}
		],
	) 
	result = response.message.content
	print(result)
	try:
		return json.loads(result)
	except json.JSONDecodeError:
		print("Error decoding JSON from model response:")
		
		return {
			"facts":[],
			"preferences":[],
			"goals":[],
		}



def merge_memories(existing, new):
	for category in existing:
		for item in new.get(category, []):
			if item not in existing[category]:
				existing[category].append(item)
	return existing
