import urllib.request
import time
import sys

queries = [
    "all:\"recursive self-improvement\"",
    "all:\"autonomous agents\"",
    "all:\"self-evolving\""
]

for query in queries:
    url = f"https://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&max_results=3&sortBy=submittedDate&sortOrder=descending"
    print(f"Querying: {query}")
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            if "Rate exceeded" in data:
                print("Rate limited.")
            else:
                print(data)
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
