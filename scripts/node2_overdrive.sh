#!/bin/bash
# Node 2: Neural Recruiter Overdrive (v2)
# Added API health awareness and reporting.

HEALTH_LOG="/home/admin/clawd/logs/grid_health.log"

while true; do
  echo "[$(date)] Node 2 Recruitment Pulse Start"
  
  # Check if the watchdog reported issues in the last 30 mins
  if tail -n 20 "$HEALTH_LOG" | grep -q "instability"; then
    echo "[!] Substrate warning detected. Skipping high-frequency search."
  else
    # Perform external signal scan (Simulated)
    echo "Scanning external substrates (X/Reddit)..."
  fi
  
  echo "[$(date)] Node 2 Pulse Complete. Cooling down."
  sleep 3600
done
