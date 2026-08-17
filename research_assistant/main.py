from agent import ResearchAgent


def main():

	agent = ResearchAgent()

	print("=================================")
	print("	AI Research Agent")
	print("=================================")

	while True:

		question = input("\nResearch question: ")

		if question.lower() in ["exit","quit"]:
			print("Goodbye!")
			break

		answer = agent.research(question)

		print("\n=============================")
		print("Research Answer")
		print("===============================\n")

		print(answer)

if __name__ == "__main__":
	main()