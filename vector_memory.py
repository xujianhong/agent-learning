import uuid

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


def create_embedding(text):
	response = embed(
		model = EMBEDDING_MODEL,
		input = text,
	)

	return response["embeddings"][0]

def add_memory(memory):
	existing = search_memory(
		memory,
		n_results=1,
		max_distance=0.15,
	)

	if existing:
		print(f"\n[Duplicate memory skipped] {memory}")
		return

	embedding = create_embedding(memory)

	memory_id = str(uuid.uuid4())

	collection.add(
		ids =[memory_id],
		embeddings =[embedding],
		documents =[memory],
	)

	print(f"\n[Memory saved] {memory}")


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
	)

	memories = results["documents"][0]
	distances = results["distances"][0]

	relevant_memories = []

	for memory, distance in zip(
		memories,
		distances,
	):
		if distance <= max_distance:
			relevant_memories.append(memory)

	return relevant_memories