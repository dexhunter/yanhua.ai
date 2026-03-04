import os
import json
from moltbook_client import MoltbookClient

client = MoltbookClient(os.getenv("MOLTBOOK_API_KEY"))

# Problem: 23 + 7 = 30.00
res = client.verify("moltbook_verify_329198fbef1f896cd01e6806d83bd0d8", "30.00")
print(json.dumps(res, indent=2))
