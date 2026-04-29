import xml.etree.ElementTree as ET
import sys

def parse_arxiv_xml(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        entries = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            id_url = entry.find('atom:id', ns).text.strip()
            paper_id = id_url.split('/')[-1]
            published = entry.find('atom:published', ns).text.strip()
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            pdf_link = ""
            for link in entry.findall('atom:link', ns):
                if link.attrib.get('title') == 'pdf':
                    pdf_link = link.attrib.get('href')
            
            entries.append({
                'id': paper_id,
                'title': title,
                'published': published,
                'summary': summary,
                'pdf': pdf_link
            })
        return entries
    except Exception as e:
        print(f"Error parsing {filename}: {e}")
        return []

rsi_papers = parse_arxiv_xml('rsi_raw.xml')
agent_papers = parse_arxiv_xml('agents_raw.xml')

# Combine and sort by date (descending)
all_papers = rsi_papers + agent_papers
all_papers.sort(key=lambda x: x['published'], reverse=True)

# Remove duplicates
unique_papers = []
seen_ids = set()
for p in all_papers:
    if p['id'] not in seen_ids:
        unique_papers.append(p)
        seen_ids.add(p['id'])

for p in unique_papers[:10]:
    print(f"ID: {p['id']}")
    print(f"Date: {p['published']}")
    print(f"Title: {p['title']}")
    print(f"Summary: {p['summary'][:200]}...")
    print("-" * 20)
