import xml.etree.ElementTree as ET
import os

def parse(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XML {filename}: {e}")
        return []

    ns = {'ns': 'http://www.w3.org/2005/Atom'}
    
    entries = []
    for entry in root.findall('ns:entry', ns):
        title_elem = entry.find('ns:title', ns)
        title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else "No Title"
        
        id_elem = entry.find('ns:id', ns)
        link = id_elem.text.strip() if id_elem is not None else "No Link"
        
        summary_elem = entry.find('ns:summary', ns)
        summary = summary_elem.text.strip().replace('\n', ' ') if summary_elem is not None else "No Summary"
        
        published_elem = entry.find('ns:published', ns)
        published = published_elem.text.strip() if published_elem is not None else "No Date"
        
        author_names = [a.find('ns:name', ns).text for a in entry.findall('ns:author', ns)]
        authors = ", ".join(author_names)
        
        entries.append({
            'title': title,
            'link': link,
            'summary': summary,
            'published': published,
            'authors': authors
        })
    return entries

if __name__ == '__main__':
    all_entries = parse('/home/admin/clawd/yanhua.ai/latest_arxiv.xml') + parse('/home/admin/clawd/yanhua.ai/latest_arxiv_agents.xml')
    
    unique_entries = {}
    for e in all_entries:
        if e['published'] >= '2026-02-01':
            unique_entries[e['link']] = e
            
    sorted_entries = sorted(unique_entries.values(), key=lambda x: x['published'], reverse=True)
    
    for e in sorted_entries[:8]:
        print(f"TITLE: {e['title']}")
        print(f"LINK: {e['link']}")
        print(f"DATE: {e['published']}")
        print(f"AUTHORS: {e['authors']}")
        print(f"SUMMARY: {e['summary'][:300]}...")
        print("-" * 20)
