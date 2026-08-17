import uuid
from datetime import datetime, timezone

import chromadb
from ollama import embed


EMBEDDING_MODEL = "nomic-embed-text"


client = chromadb.PersistentClient(
	path ="./chroma_db"
)

collection = client.get_or_create_collection(
	name ="user_memories",
	metadata={"hnsw:space": "cosine"},
)

def now():
	return datetime.now(timezone.utc).isoformat()

def create_embedding(text):
	response = embed(
		model = EMBEDDING_MODEL,
		input = text,
	)

	return response["embeddings"][0]

def add_memory(
	text,
	category="fact",
	confidence=1.0,
	source="user",
):
	memory_id = str(uuid.uuid4())

	timestamp = now()

	embedding = create_embedding(text)

	collection.add(
		ids =[memory_id],
		embeddings =[embedding],
		documents =[text],
		metadatas=[{
			"category": category,
			"created_at": timestamp,
			"updated_at": timestamp,
			"source":source,
			"confidence":confidence,

		}],
	)

	print(f"\n[Memory added] {text}")

	return memory_id


def search_memory(
	query,
	n_results=3,
	max_distance=0.7,
):

	if collection.count() == 0:
		return []

	
	embedding = create_embedding(query)

	results = collection.query(
		query_embeddings =[embedding],
		n_results = min(
			n_results,
			collection.count(),
		),
		include=[
			"documents",
			"metadatas",
			"distances",
		],
	)

	memories = []

	for memory_id, document, metadata, distance in zip(
		results["ids"][0],
		results["documents"][0],
		results["metadatas"][0],
		results["distances"][0],
	):

		if distance <= max_distance:

			memories.append({
				"id": memory_id,
				"text": document,
				"metadata": metadata,
				"distance": distance,
			})

	return memories


def update_memory(
	memory_id,
	new_text,
	category=None,
	confidence=None,
):
	existing = collection.get(
		ids=[memory_id],
		include=["metadatas"],
	)

	if not existing["ids"]:
		print(
			f"[Memory update failed] "
			f"{memory_id} not found"
		)
		return

	old_metadata = existing["metadatas"][0]

	metadata = {
		"category":(
			category
			if category is not None
			else old_metadata.get("category","fact")
		),
		"created_at": old_metadata.get(
			"created_at",
			now(),
		),
		"updated_at":now(),
		"source": old_metadata.get(
			"source",
			"user",
		),
		"confidence":(
			confidence
			if confidence is not None
			else old_metadata.get(
				"confidence",
				1.0,
			)
		),
	}

	embedding = create_embedding(new_text)

	collection.update(
		ids=[memory_id],
		embeddings=[embedding],
		documents=[new_text],
		metadatas=[metadata],
	)

	print(f"[Memory updated] {new_text}")


def delete_memory(memory_id):
	collection.delete(
		ids=[memory_id],
	)

	print(f"[Memory deleted] {memory_id}")