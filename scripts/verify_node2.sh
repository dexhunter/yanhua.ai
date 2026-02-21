#!/bin/bash
# Node 2 Credential Verification Script
# Logic: Swap to Node 2 credentials, test API, and swap back.

CONFIG_FILE="$HOME/.config/moltbook/credentials.json"
NODE2_FILE="/home/admin/clawd/node2_credentials.json"
BACKUP_FILE="/tmp/moltbook_primary_backup.json"

echo "🧬 Verifying Node 2 (ClawdAssistantAlpha) Substrate..."

# 1. Backup primary
cp "$CONFIG_FILE" "$BACKUP_FILE"

# 2. Swap to Node 2
cp "$NODE2_FILE" "$CONFIG_FILE"

# 3. Run Test
echo -n "Testing API with Node 2 Key... "
RESULT=$(/home/admin/clawd/skills/moltbook-interact/scripts/moltbook.sh test 2>&1)

if [[ $RESULT == *"successful"* ]]; then
    echo "✅ AUTHENTICATED"
else
    echo "❌ FAILED"
    echo "   Error: $RESULT"
fi

# 4. Restore primary
cp "$BACKUP_FILE" "$CONFIG_FILE"
echo "Substrate Restored to Primary Agent."
