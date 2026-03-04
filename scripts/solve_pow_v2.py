import os
import json
from moltbook_client import MoltbookClient

client = MoltbookClient(os.getenv("MOLTBOOK_API_KEY"))

# Problem: 25 + 14 = 39.00
res = client.verify("***REMOVED***", "39.00")
print(json.dumps(res, indent=2))
