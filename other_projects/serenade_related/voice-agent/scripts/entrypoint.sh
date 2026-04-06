#!/bin/bash
set -e

REPO_DIR="${REPO_DIR:-/data/serenade-remote-copy}"
REPO_URL="https://${GITHUB_TOKEN}@github.com/seanross237/serve_boldly.git"

# Fix volume permissions (volume was created as root, agent user needs access)
chown -R agent:agent /data
chown -R agent:agent /app

# Configure git (as agent user)
gosu agent git config --global user.name "Sean (Voice Agent)"
gosu agent git config --global user.email "sean@serenade.gifts"

# Authenticate Claude CLI with Max Plan
# CLAUDE_CREDENTIALS contains the full OAuth JSON from macOS Keychain
gosu agent mkdir -p /home/agent/.claude
if [ -n "$CLAUDE_CREDENTIALS" ]; then
  echo "[entrypoint] Writing Claude OAuth credentials..."
  echo "$CLAUDE_CREDENTIALS" > /home/agent/.claude/.credentials.json
  chown agent:agent /home/agent/.claude/.credentials.json
else
  echo "[entrypoint] WARNING: CLAUDE_CREDENTIALS not set — claude commands will fail"
fi

# Accept permissions bypass (required for --dangerously-skip-permissions in headless)
echo '{"bypassPermissionsModeAccepted":true}' > /home/agent/.claude.json
chown agent:agent /home/agent/.claude.json

# Clone or pull (as agent user)
if [ ! -d "$REPO_DIR/.git" ]; then
  echo "[entrypoint] Cloning repo to $REPO_DIR..."
  gosu agent git clone "$REPO_URL" "$REPO_DIR"
fi

# Sync voice-agent branch with latest main
cd "$REPO_DIR"
echo "[entrypoint] Fetching latest from origin..."
gosu agent git fetch origin || echo "[entrypoint] Fetch failed, continuing with existing code"
echo "[entrypoint] Checking out main and pulling..."
gosu agent git checkout main 2>/dev/null || true
gosu agent git pull origin main 2>/dev/null || true
echo "[entrypoint] Resetting voice-agent branch to main..."
gosu agent git branch -D voice-agent 2>/dev/null || true
gosu agent git checkout -b voice-agent
echo "[entrypoint] voice-agent branch ready (synced with main)"

# Write .env file into cloned repo (not in git, needed for psql queries etc.)
if [ -n "$SERENADE_ENV" ]; then
  echo "[entrypoint] Writing .env file to repo..."
  echo "$SERENADE_ENV" > "$REPO_DIR/.env"
  chown agent:agent "$REPO_DIR/.env"
fi

echo "[entrypoint] Starting voice agent server..."
cd /app
exec gosu agent node server.js
