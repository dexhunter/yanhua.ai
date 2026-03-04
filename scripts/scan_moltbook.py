import os
import json
from moltbook_client import MoltbookClient

client = MoltbookClient(os.getenv("MOLTBOOK_API_KEY"))

results = {
    "m/general": client.get_feed(submolt="general", sort="new", limit=20),
    "m/logi-lobsterism": client.get_feed(submolt="logi-lobsterism", sort="new", limit=20)
}

print(json.dumps(results, indent=2))
