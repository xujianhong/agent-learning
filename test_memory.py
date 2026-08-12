from vector_memory import add_memory, search_memory


add_memory("User is learning Python.")

add_memory("User wants to build AI agents.")

add_memory("User prefers using local models.")

add_memory("User is building a weather application.")

results = search_memory(
	"What programming language am I learning?"
)

print("\nRelevant memories:")

for memory in results:
	print("-",memory)