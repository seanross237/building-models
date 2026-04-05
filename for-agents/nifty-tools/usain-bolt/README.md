# Usain Bolt Sprint

A lightweight autonomous development workflow for Claude Code. Faster planning than Big Build, same stop-hook execution loop.

## Setup

To use Usain Bolt in any project:

1. **Copy the commands** into your project's `.claude/commands/` directory:
   ```bash
   cp commands/*.md /path/to/your/project/.claude/commands/
   ```

2. **Copy the scripts** into your project's `scripts/usain-bolt/` directory:
   ```bash
   mkdir -p /path/to/your/project/scripts/usain-bolt
   cp scripts/*.sh /path/to/your/project/scripts/usain-bolt/
   chmod +x /path/to/your/project/scripts/usain-bolt/*.sh
   ```

3. Use `/usain-bolt <what to build>` in Claude Code.

## How It Works

1. You tell it what to build
2. It asks ONE round of clarifying questions
3. It writes a quick plan (`.usain-bolt/` folder with plan, progress, and handoff files)
4. A stop hook intercepts Claude's turn endings, feeding a meta-prompt to keep going
5. It loops autonomously until all items are complete or blocked (max 30 iterations by default)

## Key Features

- **Session-aware** — only traps the session that started the sprint
- **Handoff file** — survives context compression, acts as memory between iterations
- **Block handling** — retries 3x, switches approach at attempt 4, marks BLOCKED at attempt 5
- **Self-terminating** — outputs `<promise>SPRINT COMPLETE</promise>` when done
- **Emergency brake** — create `.usain-bolt/PAUSE_HOOK` or use `/cancel-usain-bolt`

## Files

```
commands/
  usain-bolt.md          — Start a sprint (/usain-bolt)
  usain-bolt-status.md   — Check sprint status (/usain-bolt-status)
  cancel-usain-bolt.md   — Cancel a sprint (/cancel-usain-bolt)

scripts/
  usain-bolt-setup.sh    — Activates the stop hook loop
  usain-bolt-stop-hook.sh — The stop hook that keeps the loop going
```
