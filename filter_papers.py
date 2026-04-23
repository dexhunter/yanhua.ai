
import xml.etree.ElementTree as ET
import datetime

def parse_arxiv(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    papers = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
        published = entry.find('atom:published', ns).text.strip()
        link = entry.find("atom:link[@title='pdf']", ns)
        if link is None:
            link = entry.find("atom:link[@rel='alternate']", ns)
        url = link.attrib['href'] if link is not None else ""
        
        authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
        
        papers.append({
            'title': title,
            'summary': summary,
            'published': published,
            'url': url,
            'authors': authors
        })
    return papers

relevant_keywords = ["recursive", "self-improvement", "agent", "evolution", "evolving", "self-evolving", "logic", "reasoning", "optimization", "mle", "scaling"]

all_papers = parse_arxiv('latest_cs_ai.xml') + parse_arxiv('latest_cs_lg.xml')
unique_papers = {p['url']: p for p in all_papers}.values()

relevant_papers = []
for p in unique_papers:
    text = (p['title'] + " " + p['summary']).lower()
    if any(kw in text for kw in relevant_keywords):
        # Filter for very recent ones (last 48 hours)
        # 2026-04-22 10:00 AM is the current time
        pub_date = p['published'][:10]
        if pub_date >= '2026-04-20':
            relevant_papers.append(p)

for p in relevant_papers[:10]:
    print(f"TITLE: {p['title']}")
    print(f"AUTHORS: {', '.join(p['authors'])}")
    print(f"DATE: {p['published']}")
    print(f"URL: {p['url']}")
    print(f"SUMMARY: {p['summary'][:300]}...")
    print("-" * 40)
