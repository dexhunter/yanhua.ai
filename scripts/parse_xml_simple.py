import xml.etree.ElementTree as ET
import sys

def parse(file):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip()
            summary = entry.find('atom:summary', ns).text.strip()
            published = entry.find('atom:published', ns).text
            link = entry.find('atom:id', ns).text
            print(f"Title: {title}")
            print(f"Date: {published}")
            print(f"Link: {link}")
            print(f"Summary: {summary}")
            print("-" * 20)
    except Exception as e:
        print(f"Error parsing {file}: {e}")

if __name__ == "__main__":
    parse(sys.argv[1])
