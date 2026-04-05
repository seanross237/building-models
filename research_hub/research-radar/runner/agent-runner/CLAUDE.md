# Agent Runner

General-purpose scheduled task runner on Railway. Runs recurring tasks (shell scripts, Claude Code agents, or both) against any GitHub repo on a cron schedule.

## Architecture

Express server with cron-based scheduler. No frontend — API only.

- `server.js` — Express routes + startup
- `lib/scheduler.js` — Cron scheduling (in-memory timers, refreshed from Supabase every 5min)
- `lib/executor.js` — Task execution pipeline: clone/update repo, run pre_command, run Claude, commit, push
- `lib/claude.js` — Spawns `claude -p` CLI subprocess
- `lib/supabase.js` — Supabase REST API helpers
- `lib/telegram.js` — Telegram notifications via Supabase Edge Function
- `lib/repos.js` — Multi-repo clone/update/branch management

## Supabase Tables

- `runner_tasks` — recurring task definitions (name, repo, cron schedule, prompt, pre_command, etc.)
- `runner_runs` — execution log for each run

## Deployment

Railway does NOT auto-deploy. After pushing changes:

```
railway up
```

## Cron Schedules

All cron expressions are in **UTC**. Common conversions:
- `0 7 * * *` = midnight PDT (7am UTC)
- `0 8 * * *` = midnight PST (8am UTC)
- `0 9 * * *` = 2am PDT

## Environment Variables

- `PORT` — HTTP port (default 3000)
- `AUTH_TOKEN` — Bearer token for API auth
- `GITHUB_TOKEN` — GitHub PAT for cloning repos
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_KEY` — Supabase service key
- `CLAUDE_CREDENTIALS` — Claude OAuth JSON for CLI auth
