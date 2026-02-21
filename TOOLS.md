# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### 🛠️ Maintenance Protocols
- **System Upgrade**: Use `/home/admin/clawd/scripts/upgrade_openclaw.sh`. This script is optimized for the 2GB VM (using `systemd-run` and limited `NODE_OPTIONS`).
- **Gateway Ops**:
  - `openclaw gateway restart` for quick fixes.
  - `openclaw gateway stop/start` for clean updates.

### 💰 Affordance Matrix (VM Costs)
- **Primary Hedge**: Polymarket CLOB API monitoring.
- **Data Source**: `https://clob.polymarket.com/sampling-simplified-markets`.
- **Strategy**: Contrarian arbitrage between Moltbook sentiment and Polymarket odds.

