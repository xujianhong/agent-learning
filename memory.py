import json
from pathlib import Path

MEMORY_FILE = Path("memory.json")

def load_memory():
    if not MEMORY_FILE.exists():
        return []

    with open(MEMORY_FILE,"r", encoding="utf-8") as file:
        return json.load(file)

def save_memory(conversation):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(conversation, file, indent=2, ensure_ascii=False)
    