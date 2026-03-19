import requests
import json
import time
import os

session_id = "27b64a8a-5fe1-46aa-a272-738fc7be4ff4"
poll_url = f"https://api.mails.dev/v1/claim/poll?session={session_id}"
config_file = "/home/admin/clawd/memory/mails_config.json"

print(f"Polling for claim status for session {session_id}...")

for _ in range(60): # Poll for 10 minutes (every 10s)
    try:
        response = requests.get(poll_url)
        data = response.json()
        
        if data.get("status") == "complete":
            print("Claim successful!")
            with open(config_file, "w") as f:
                json.dump(data, f)
            print(f"Configuration saved to {config_file}")
            break
        elif data.get("status") == "expired":
            print("Claim session expired.")
            break
        else:
            # Still pending
            time.sleep(10)
    except Exception as e:
        print(f"Error polling: {e}")
        time.sleep(10)
