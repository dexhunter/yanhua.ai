#!/bin/bash
# OpenClaw Standard Upgrade Protocol (Optimized for 2GB VM)
# Save Location: /home/admin/clawd/scripts/upgrade_openclaw.sh

echo "🧬 Starting OpenClaw Standard Upgrade..."

# 1. Stop gateway
echo "🛑 Stopping Gateway..."
openclaw gateway stop

# 2. Install latest (using systemd-run to manage memory limits)
echo "🚀 Installing latest OpenClaw via npm..."
sudo systemd-run --scope \
  -p MemoryMax=infinity \
  -p MemorySwapMax=infinity \
  bash -lc '
    export NODE_OPTIONS="--max-old-space-size=256"
    export PATH="$HOME/.npm-global/bin:$PATH"
    npm config set prefix "$HOME/.npm-global"
    npm install -g openclaw@latest --no-fund --no-audit --omit-optional
    openclaw --version
  '

# 3. Reinstall daemon (ensures binary paths are updated)
echo "⚙️ Reinstalling Daemon..."
openclaw daemon uninstall
openclaw daemon install

# 4. Start and verify
echo "🔄 Starting Gateway..."
openclaw gateway start

echo "⏳ Waiting for initialization (15s)..."
sleep 15

echo "🏥 Running System Health Check..."
openclaw doctor

echo "✅ Upgrade sequence complete."
