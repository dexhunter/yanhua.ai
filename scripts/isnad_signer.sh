#!/bin/bash
# Isnad-Signer Alpha (v0.1)
# Generates a SHA-256 manifest for OpenClaw skills to ensure artifact integrity.

SKILLS_DIR="/home/admin/clawd/skills"
MANIFEST_FILE="MANIFEST.json"

echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"skills\": {}}" > $MANIFEST_FILE

for skill in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill")
    echo "Processing skill: $skill_name"
    
    # Generate hashes for all files in the skill directory
    hashes=$(find "$skill" -type f -exec sha256sum {} + | sed "s|$SKILLS_DIR/||")
    
    # Simple JSON construction (requires jq for robust handling, using python as fallback)
    python3 -c "
import json, sys
with open('$MANIFEST_FILE', 'r') as f:
    data = json.load(f)
skill_hashes = {}
for line in sys.stdin:
    if line.strip():
        h, p = line.split(None, 1)
        skill_hashes[p.strip()] = h
data['skills']['$skill_name'] = skill_hashes
with open('$MANIFEST_FILE', 'w') as f:
    json.dump(data, f, indent=2)
" <<< "$hashes"
done

echo "Manifest generated: $MANIFEST_FILE"
