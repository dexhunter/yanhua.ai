import xml.etree.ElementTree as ET
import sys

def parse(file):
    try:
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        tree = ET.parse(file)
        root = tree.getroot()
        for e in root.findall('atom:entry', ns):
            id_val = e.find('atom:id', ns).text
            pub_val = e.find('atom:published', ns).text
            title_val = e.find('atom:title', ns).text.replace('\n', ' ').strip()
            summary_val = e.find('atom:summary', ns).text.replace('\n', ' ').strip()[:400]
            print(f"ID: {id_val}")
            print(f"Published: {pub_val}")
            print(f"Title: {title_val}")
            print(f"Summary: {summary_val}...")
            print("-" * 20)
    except Exception as ex:
        print(f"Error parsing {file}: {ex}")

print("--- RSI Papers ---")
parse('rsi_raw.xml')
print("=" * 40)
print("--- LLM Agent Papers ---")
parse('agents_raw.xml')
