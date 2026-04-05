#!/bin/bash
set -e

# Fix volume permissions
chown -R agent:agent /data
chown -R agent:agent /app

# Configure git
gosu agent git config --global user.name "Agent Runner"
gosu agent git config --global user.email "sean@serenade.gifts"

# Authenticate Claude CLI with Max Plan
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

echo "[entrypoint] Starting agent runner..."
cd /app
exec gosu agent node server.js
