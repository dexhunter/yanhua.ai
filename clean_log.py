import re
from datetime import datetime

def clean_research_log(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Remove git conflict markers
    content = re.sub(r'<<<<<<< .*?\n', '', content)
    content = re.sub(r'=======.*?\n', '', content)
    content = re.sub(r'>>>>>>> .*?\n', '', content)

    # Split into entries
    entries = re.split(r'### ', content)
    header = entries[0]
    entry_list = entries[1:]

    parsed_entries = {}
    for entry in entry_list:
        match = re.match(r'\[(.*?)\] (.*)', entry)
        if match:
            date_str, title_full = match.groups()
            title = title_full.split('\n')[0].strip()
            
            # Use title as key for deduplication
            if title not in parsed_entries:
                parsed_entries[title] = {
                    'date': date_str,
                    'content': '### ' + entry.strip()
                }

    # Sort entries by date descending, then title
    sorted_titles = sorted(parsed_entries.keys(), key=lambda x: (parsed_entries[x]['date'], x), reverse=True)

    new_content = header
    for title in sorted_titles:
        new_content += parsed_entries[title]['content'] + '\n\n'

    with open(file_path, 'w') as f:
        f.write(new_content)

clean_research_log('/home/admin/clawd/yanhua.ai/memory/RESEARCH_LOG.md')
