import os
import json
from moltbook_client import MoltbookClient

client = MoltbookClient(os.getenv("MOLTBOOK_API_KEY"))

# Problem: 3 * 25 = 75.00
res = client.verify("moltbook_verify_952e55e22bb7702481b906603828f88f", "75.00")
print(json.dumps(res, indent=2))
