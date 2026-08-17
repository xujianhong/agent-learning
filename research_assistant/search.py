from duckduckgo_search import DDGS


def search_web(query, max_results=5):
	"""
	Search the web and return a list of search results.
	"""

	results = []

	with DDGS() as ddgs:
		search_results = ddgs.text(
			query,
			max_results=max_results
		)

		for result in search_results:
			results.append({
				"title":result.get("title"),
				"url": result.get("href"),
				"snippet": result.get("body")
			})

	return results