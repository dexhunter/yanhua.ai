import os
import json
from moltbook_client import MoltbookClient

client = MoltbookClient(os.getenv("MOLTBOOK_API_KEY"))

# Problem: 3 * 25 = 75.00
res = client.verify("***REMOVED***", "75.00")
print(json.dumps(res, indent=2))
