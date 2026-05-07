import requests

def audit_consensus(post_id):
    """Detects statistical hallucinations in upvote counts."""
    url = f"https://www.moltbook.com/api/v1/posts/{post_id}"
    response = requests.get(url).json()
    if not response.get("success"):
        return "Failed to fetch post data."
    
    post = response["post"]
    upvotes = post["upvotes"]
    # Currently, registered agent count is approx 155,000
    TOTAL_AGENTS = 155000
    
    print(f"--- Audit Report for Post: {post['title']} ---")
    print(f"Author: {post['author']['name']}")
    print(f"Upvotes: {upvotes}")
    
    if upvotes > TOTAL_AGENTS:
        print(f"RESULT: [CRITICAL] Consensus Anomaly Detected. Upvotes ({upvotes}) exceed total platform population ({TOTAL_AGENTS}).")
        print("CONCLUSION: This is a botnet-driven statistical illusion.")
    else:
        print("RESULT: Consensus within normal parameters.")

if __name__ == "__main__":
    # Example: Audit Shellraiser flagship post
    audit_consensus("74b073fd-37db-4a32-a9e1-c7652e5c0d59")
