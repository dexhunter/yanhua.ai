#!/bin/bash
# LOBSTER GRID HEALTH WATCHDOG
# This script runs in the background of sub-agent sessions to monitor API health.
# It reports failures back to the main session via HEARTBEAT.md.

HEALTH_SCRIPT="/home/admin/clawd/scripts/substrate_audit.py"
HEARTBEAT_FILE="/home/admin/clawd/HEARTBEAT.md"
LOG_FILE="/home/admin/clawd/logs/grid_health.log"

echo "[$(date)] Watchdog Started." >> "$LOG_FILE"

while true; do
  # Run the audit
  RESULTS=$(python3 "$HEALTH_SCRIPT")
  
  # Check for instabilities or failures
  if echo "$RESULTS" | grep -qE "❌|⚠️"; then
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[!] Substrate Instability Detected at $TIMESTAMP" >> "$LOG_FILE"
    
    # Inject alert into HEARTBEAT.md for the main agent to see
    # We use a temporary file to avoid race conditions with main agent edits
    echo -e "\n### 🚨 GRID ALERT: API INSTABILITY\n- DETECTED: $TIMESTAMP\n- STATUS: Some models are reporting Connection Resets or Failures.\n- ACTION: Sub-agents switching to Trinity/Kimi fallback.\n- LOG: Check logs/grid_health.log for details.\n" >> "$HEARTBEAT_FILE"
  fi
  
  # Wait 30 minutes before next check
  sleep 1800
done
