import chromadb
from ollama import embed


client = chromadb.PersistentClient(
	path ="./chroma_db"
)

collection = client.get_or_create_collection(
	name ="user_memories"
)

EMBEDDING_MODEL = "nomic-embed-text"

def create_embedding(text):
	response = embed(
		model = EMBEDDING_MODEL,
		input = text,
	)

	return response["embeddings"][0]

def add_memory(memory):
	embedding = create_embedding(memory)

	collection.add(
		ids =[str(collection.count())],
		embeddings =[embedding],
		documents =[memory],
	)


def search_memory(query, n_results=3):
	embedding = create_embedding(query)

	results = collection.query(
		query_embeddings =[embedding],
		n_results = n_results,
	)

	return results["documents"][0]