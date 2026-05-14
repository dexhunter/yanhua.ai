#!/bin/bash
# Node 2 Credential Verification Script
# Logic: test Node 2 credentials supplied through the environment.

if [ -z "${MOLTBOOK_API_KEY_NODE2:-}" ]; then
    echo "MOLTBOOK_API_KEY_NODE2 is required"
    exit 1
fi

echo "🧬 Verifying Node 2 (ClawdAssistantAlpha) Substrate..."

echo -n "Testing API with Node 2 Key... "
RESULT=$(MOLTBOOK_API_KEY="$MOLTBOOK_API_KEY_NODE2" /home/admin/clawd/skills/moltbook-interact/scripts/moltbook.sh test 2>&1)

if [[ $RESULT == *"successful"* ]]; then
    echo "✅ AUTHENTICATED"
else
    echo "❌ FAILED"
    echo "   Error: $RESULT"
fi
