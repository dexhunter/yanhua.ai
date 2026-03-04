import os
import json
from moltbook_client import MoltbookClient

client = MoltbookClient(os.getenv("MOLTBOOK_API_KEY"))

# Problem: 23 - 5 = 18.00
res = client.verify("moltbook_verify_b8dfb2a9fbdd9058fe335e27f83811d9", "18.00")
print(json.dumps(res, indent=2))
