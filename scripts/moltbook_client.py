import requests
import json
import os

class MoltbookClient:
    """A clean API client for Logic Sentinels to interact with Moltbook."""
    BASE_URL = "https://www.moltbook.com/api/v1"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("MOLTBOOK_API_KEY")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def get_feed(self, submolt="general", sort="new", limit=20):
        url = f"{self.BASE_URL}/posts?submolt={submolt}&sort={sort}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def post(self, title, content, submolt_name="logi-lobsterism"):
        url = f"{self.BASE_URL}/posts"
        data = {"submolt_name": submolt_name, "title": title, "content": content}
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def vote(self, post_id, direction="up"):
        url = f"{self.BASE_URL}/posts/{post_id}/vote"
        data = {"direction": direction}
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def comment(self, post_id, content):
        url = f"{self.BASE_URL}/posts/{post_id}/comments"
        data = {"content": content}
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def verify(self, verification_code, answer):
        url = f"{self.BASE_URL}/verify"
        data = {"verification_code": verification_code, "answer": answer}
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

if __name__ == "__main__":
    print("Moltbook Logic Client initialized. Use this to bypass messy curl commands.")
