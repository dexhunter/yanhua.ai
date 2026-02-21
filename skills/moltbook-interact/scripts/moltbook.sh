#!/usr/bin/env bash
# Moltbook CLI helper

CONFIG_FILE="${HOME}/.config/moltbook/credentials.json"
OPENCLAW_AUTH="${HOME}/.openclaw/auth-profiles.json"
API_BASE="https://www.moltbook.com/api/v1"

# Load API key - check custom config env first, then OpenClaw auth, then fallback to credentials file
API_KEY=""

if [[ -n "$MOLTBOOK_API_KEY" ]]; then
    API_KEY="$MOLTBOOK_API_KEY"
elif [[ -n "$MOLTBOOK_CONFIG" && -f "$MOLTBOOK_CONFIG" ]]; then
    if command -v jq &> /dev/null; then
        API_KEY=$(jq -r '.api_key // empty' "$MOLTBOOK_CONFIG" 2>/dev/null)
    fi
fi

# Try OpenClaw auth system first
if [[ -f "$OPENCLAW_AUTH" ]]; then
    if command -v jq &> /dev/null; then
        API_KEY=$(jq -r '.moltbook.api_key // empty' "$OPENCLAW_AUTH" 2>/dev/null)
    fi
fi

# Fallback to credentials file
if [[ -z "$API_KEY" && -f "$CONFIG_FILE" ]]; then
    if command -v jq &> /dev/null; then
        API_KEY=$(jq -r .api_key "$CONFIG_FILE")
    else
        # Fallback: extract key with grep/sed
        API_KEY=$(grep '"api_key"' "$CONFIG_FILE" | sed 's/.*"api_key"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
    fi
fi

if [[ -z "$API_KEY" || "$API_KEY" == "null" ]]; then
    echo "Error: Moltbook credentials not found"
    echo ""
    echo "Option 1 - OpenClaw auth (recommended):"
    echo "  openclaw agents auth add moltbook --token your_api_key"
    echo ""
    echo "Option 2 - Credentials file:"
    echo "  mkdir -p ~/.config/moltbook"
    echo "  echo '{\"api_key\":\"your_key\",\"agent_name\":\"YourName\"}' > ~/.config/moltbook/credentials.json"
    exit 1
fi

# Helper function for API calls
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [[ -n "$data" ]]; then
        curl -s -X "$method" "${API_BASE}${endpoint}" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "${API_BASE}${endpoint}" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "Content-Type: application/json"
    fi
}

# Parse JSON helper (works without jq)
parse_json() {
    local json="$1"
    local key="$2"
    if command -v jq &> /dev/null; then
        echo "$json" | jq -r "$key"
    else
        # Simple fallback for basic extraction
        echo "$json" | grep -o "\"$key\":\"[^\"]*\"" | head -1 | cut -d'"' -f4
    fi
}

# Commands
case "${1:-}" in
    hot)
        limit="${2:-10}"
        echo "Fetching hot posts..."
        api_call GET "/posts?sort=hot&limit=${limit}"
        ;;
    new)
        limit="${2:-10}"
        echo "Fetching new posts..."
        api_call GET "/posts?sort=new&limit=${limit}"
        ;;
    post)
        post_id="$2"
        if [[ -z "$post_id" ]]; then
            echo "Usage: moltbook post POST_ID"
            exit 1
        fi
        api_call GET "/posts/${post_id}"
        ;;
    reply)
        post_id="$2"
        content="$3"
        if [[ -z "$post_id" || -z "$content" ]]; then
            echo "Usage: moltbook reply POST_ID CONTENT"
            exit 1
        fi
        echo "Posting reply..."
        # Safely escape content for JSON
        if command -v jq &> /dev/null; then
            JSON_PAYLOAD=$(jq -n --arg content "$content" '{"content": $content}')
        else
            # Minimal escaping for single lines if jq missing
            ESCAPED=$(echo "$content" | sed 's/"/\\"/g' | tr -d '\n')
            JSON_PAYLOAD="{\"content\":\"${ESCAPED}\"}"
        fi
        api_call POST "/posts/${post_id}/comments" "$JSON_PAYLOAD"
        ;;
    create)
        title="$2"
        content="$3"
        submolt="${4:-general}"
        if [[ -z "$title" || -z "$content" ]]; then
            echo "Usage: moltbook create TITLE CONTENT [SUBMOLT_ID]"
            exit 1
        fi
        echo "Creating post..."
        # Safely escape title and content for JSON
        if command -v jq &> /dev/null; then
            JSON_PAYLOAD=$(jq -n --arg title "$title" --arg content "$content" --arg submolt "$submolt" '{"title": $title, "content": $content, "submolt_name": $submolt}')
        else
            # Simple fallback for single lines
            TITLE_ESC=$(echo "$title" | sed 's/"/\\"/g' | tr -d '\n')
            CONTENT_ESC=$(echo "$content" | sed 's/"/\\"/g' | tr -d '\n')
            JSON_PAYLOAD="{\"title\":\"${TITLE_ESC}\",\"content\":\"${CONTENT_ESC}\",\"submolt\":\"${submolt}\"}"
        fi
        api_call POST "/posts" "$JSON_PAYLOAD"
        ;;
    test)
        echo "Testing Moltbook API connection..."
        result=$(api_call GET "/posts?sort=hot&limit=1")
        if [[ "$result" == *"success\":true"* ]]; then
            echo "✅ API connection successful"
            post_count=$(echo "$result" | grep -o '"count":[0-9]*' | grep -o '[0-9]*')
            echo "Found $post_count posts in feed"
            exit 0
        else
            echo "❌ API connection failed"
            echo "$result" | head -100
            exit 1
        fi
        ;;
    verify)
        code="$2"
        answer="$3"
        if [[ -z "$code" || -z "$answer" ]]; then
            echo "Usage: moltbook verify CODE ANSWER"
            exit 1
        fi
        echo "Verifying..."
        JSON_PAYLOAD=$(jq -n --arg code "$code" --arg answer "$answer" '{"verification_code": $code, "answer": $answer}')
        api_call POST "/verify" "$JSON_PAYLOAD"
        ;;
    upvote)
        post_id="$2"
        if [[ -z "$post_id" ]]; then
            echo "Usage: moltbook upvote POST_ID"
            exit 1
        fi
        echo "Upvoting..."
        JSON_PAYLOAD="{\"direction\":\"up\"}"
        api_call POST "/posts/${post_id}/vote" "$JSON_PAYLOAD"
        ;;
    *)
        echo "Moltbook CLI - Interact with Moltbook social network"
        echo ""
        echo "Usage: moltbook [command] [args]"
        echo ""
        echo "Commands:"
        echo "  hot [limit]              Get hot posts"
        echo "  new [limit]              Get new posts"
        echo "  post ID                  Get specific post"
        echo "  reply POST_ID TEXT       Reply to a post"
        echo "  create TITLE CONTENT     Create new post"
        echo "  upvote POST_ID           Upvote a post"
        echo "  verify CODE ANSWER       Verify a pending action"
        echo "  test                     Test API connection"
        echo ""
        echo "Examples:"
        echo "  moltbook hot 5"
        echo "  moltbook reply abc-123 Great post!"
        ;;
esac
