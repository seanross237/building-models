# Remote Dev Box — Detailed Plan

## Goal

A persistent cloud VM that replaces both the laptop-bound workflow AND the Railway runner. One box for everything: interactive Claude Code / Codex sessions, long-running agent tasks that survive laptop close, and scheduled jobs (nightly radar, future automations).

---

## 1. Provider & Machine

**Recommended: Hetzner Cloud (CPX31)**
- 4 vCPU, 8 GB RAM, 160 GB disk — $15/mo
- US East (Ashburn) or US West datacenter for low latency
- Why Hetzner: cheapest for the specs, simple, no surprises on billing
- Alternative: Fly.io Machine (more DevOps-y) or DigitalOcean Droplet ($24/mo for same specs)

**Why not Railway:** No SSH access, containers restart unpredictably, not designed for interactive sessions. Railway gets retired — its scheduled jobs move here too (see section 11).

## 2. Initial Server Setup

```bash
# On the VM after first SSH in as root

# --- System ---
apt update && apt upgrade -y
apt install -y git curl wget tmux zsh htop jq python3 python3-pip \
  build-essential unzip ripgrep fd-find yt-dlp

# --- Non-root user ---
adduser sean --disabled-password
usermod -aG sudo sean
echo "sean ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/sean

# --- SSH hardening ---
# Copy your public key
mkdir -p /home/sean/.ssh
cp /root/.ssh/authorized_keys /home/sean/.ssh/
chown -R sean:sean /home/sean/.ssh
chmod 600 /home/sean/.ssh/authorized_keys

# Disable password auth
sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart sshd
```

## 3. Tool Installation

```bash
# As sean

# --- Node (via nvm) ---
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc
nvm install 20
npm install -g npm

# --- Claude Code ---
npm install -g @anthropic-ai/claude-code

# --- Codex (if using OpenAI Codex CLI) ---
npm install -g @openai/codex

# --- GitHub CLI ---
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install -y gh

# --- Python tools ---
pip3 install --user yt-dlp arxiv requests
```

## 4. Auth & Credentials

```bash
# --- Claude Code auth ---
# Option A: OAuth (interactive, one-time)
claude login

# Option B: API key (headless, set in env)
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc

# --- GitHub ---
gh auth login   # interactive one-time setup
git config --global user.name "seanross237"
git config --global user.email "your@email.com"

# --- OpenAI (for Codex) ---
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
```

## 5. Repo Setup

```bash
# Clone the repo
cd ~
gh repo clone seanross237/building-models
# or whatever the repo is called — adjust path

# Symlink or structure to match local layout if needed
mkdir -p ~/kingdom_of_god
ln -s ~/building-models ~/kingdom_of_god/home-base
```

## 6. tmux — Session Persistence

This is the key piece. tmux keeps your session alive when you disconnect.

```bash
# ~/.tmux.conf
cat << 'EOF' > ~/.tmux.conf
# Sensible defaults
set -g mouse on
set -g history-limit 50000
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:Tc"

# Start windows and panes at 1, not 0
set -g base-index 1
setw -g pane-base-index 1

# Easy split panes
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# Status bar
set -g status-right '#H | %Y-%m-%d %H:%M'
EOF
```

**Daily workflow:**
```bash
# From your laptop
ssh dev

# First time each boot:
tmux new -s work

# Returning after disconnect:
tmux attach -t work
# or just: tmux a
```

## 7. SSH Config (on your Mac)

```bash
# ~/.ssh/config (on your laptop)

Host dev
    HostName <VM_IP_ADDRESS>
    User sean
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountDown 3
    ForwardAgent yes
```

Then from any terminal: `ssh dev` and you're in.

## 8. VS Code Remote (optional)

If you want a GUI editor pointing at remote files:
1. Install "Remote - SSH" extension in VS Code
2. Cmd+Shift+P > "Remote-SSH: Connect to Host" > `dev`
3. Opens a full VS Code window with the remote filesystem
4. Terminal panel runs on the remote — can run Claude Code there

## 9. Keeping Things in Sync

The repo lives on the remote. Your workflow:

```
[Remote VM]                        [GitHub]                    [Laptop]
   |                                  |                           |
   |-- git push ----->                |                           |
   |                                  |  <---- git pull ----------|
   |                                  |                           |
```

- **Primary work happens on the remote.** Push when ready.
- If you also want to browse files locally, `git pull` on your laptop.
- Don't edit the same files in both places — pick one as primary.

## 10. Long-Running Agent Tasks

The whole point. Examples:

```bash
# SSH in, start tmux, then:

# Run a multi-hour Atlas mission
cd ~/kingdom_of_god/home-base
claude "Run Atlas mission exploring X. Take your time."

# Close your laptop. Come back hours later:
ssh dev
tmux a
# Claude Code is still running, output is all there
```

## 11. Replacing Railway — Scheduled Jobs on the VM

Railway gets retired. Everything moves here. The entire `runner/agent-runner/` Express + Supabase setup is replaced by system cron.

### Nightly Research Radar

```bash
# Add to crontab: crontab -e
# Runs at midnight PDT (7:00 UTC)
0 7 * * * cd ~/kingdom_of_god/home-base/research-radar && bash pipelines/nightly-radar.sh >> /var/log/radar/$(date +\%Y-\%m-\%d).log 2>&1
```

### Commit & Push After Radar

```bash
# radar-commit.sh — called at end of nightly-radar.sh or as a separate cron 15 min later
#!/bin/bash
cd ~/kingdom_of_god/home-base
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "chore(research-radar): nightly radar refresh $(date +%Y-%m-%d)"
  git push origin main
fi
```

```bash
# crontab entry — 15 min after radar
15 7 * * * bash ~/scripts/radar-commit.sh >> /var/log/radar/commit-$(date +\%Y-\%m-\%d).log 2>&1
```

### Failure Notifications

Simple Telegram ping on failure (replaces the Express/Supabase notification system):

```bash
# notify-failure.sh
#!/bin/bash
TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID"
MESSAGE="$1"
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d chat_id="$TELEGRAM_CHAT_ID" \
  -d text="[radar] $MESSAGE" > /dev/null
```

Then in your cron wrapper:
```bash
0 7 * * * cd ~/kingdom_of_god/home-base/research-radar && bash pipelines/nightly-radar.sh >> /var/log/radar/$(date +\%Y-\%m-\%d).log 2>&1 || bash ~/scripts/notify-failure.sh "Nightly radar failed — check logs"
```

### Future Scheduled Agents

Any new scheduled task is just another crontab line. No Express server, no Supabase tables, no Docker container. Examples:

```bash
# Run an Atlas mission every Monday at 9am UTC
0 9 * * 1 cd ~/kingdom_of_god/home-base && claude -p "Run Atlas exploration on topic X" >> /var/log/atlas/$(date +\%Y-\%m-\%d).log 2>&1

# Weekly repo health check
0 12 * * 0 cd ~/kingdom_of_god/home-base && claude -p "Review open issues and summarize status" >> /var/log/weekly-review.log 2>&1
```

### Railway Decommission Checklist

- [ ] Confirm VM cron runs nightly radar successfully for 3+ days
- [ ] Verify commits land on GitHub from the VM
- [ ] Verify Telegram notifications fire on failure
- [ ] Tear down Railway service
- [ ] Remove Supabase runner_tasks / runner_runs tables (or keep as archive)
- [ ] Optionally archive `runner/agent-runner/` directory in the repo

## 12. Cost Estimate

| Item | Monthly Cost |
|---|---|
| Hetzner CPX31 (4 vCPU, 8GB) | ~$15 |
| Railway | $0 (retired) |
| Supabase (runner tables) | $0 (retired) |
| Claude API usage | varies (existing spend) |
| Bandwidth | included |
| **Total infrastructure** | **~$15/mo** |

Net savings vs current: Railway costs go away. Could go cheaper with CPX21 (3 vCPU, 4GB, $9/mo) — Claude Code doesn't need much RAM since the model runs remotely.

## 13. Setup Checklist

**Phase 1 — Get the box working (day 1)**
- [ ] Create Hetzner account, spin up CPX31 in US East
- [ ] SSH in as root, run system setup (section 2)
- [ ] Install tools (section 3)
- [ ] Configure auth — Claude, GitHub, OpenAI (section 4)
- [ ] Clone repo (section 5)
- [ ] Set up tmux config (section 6)
- [ ] Add SSH config on laptop (section 7)
- [ ] Test: `ssh dev`, `tmux new`, `claude`, run a command, disconnect, reattach
- [ ] (Optional) VS Code Remote SSH

**Phase 2 — Migrate Railway (days 2-5)**
- [ ] Set up cron for nightly radar (section 11)
- [ ] Set up commit + push script
- [ ] Set up Telegram failure notifications
- [ ] Run nightly radar manually once, verify it works end-to-end
- [ ] Let cron run for 3 nights, confirm commits land on GitHub
- [ ] Decommission Railway service
- [ ] Archive or remove `runner/agent-runner/` from repo

## 14. Hardening (do after basics work)

- [ ] Set up UFW firewall: allow 22, deny everything else
- [ ] Fail2ban for SSH brute force protection
- [ ] Automatic security updates: `apt install unattended-upgrades`
- [ ] Backups: Hetzner snapshots ($0.01/GB/mo) or just rely on git
