from moltbook_client import MoltbookClient
import json

client = MoltbookClient(api_key="moltbook_sk_g5EHD6Y7X9J2K4L8M0P1Q3R5S7T9U1V2")
print(json.dumps(client.get_feed(submolt="general", limit=5), indent=2))
print(json.dumps(client.get_feed(submolt="logi-lobsterism", limit=5), indent=2))
