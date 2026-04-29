import urllib.request
import urllib.parse
import time

def search_arxiv(query, max_results=5):
    encoded_query = urllib.parse.quote(query)
    url = f"https://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    print(f"Fetching {url}...")
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return str(e)

rsi_xml = search_arxiv("Recursive Self-Improvement")
with open("rsi_arxiv.xml", "w") as f:
    f.write(rsi_xml)

time.sleep(1)

agents_xml = search_arxiv("LLM Agents")
with open("agents_arxiv.xml", "w") as f:
    f.write(agents_xml)
