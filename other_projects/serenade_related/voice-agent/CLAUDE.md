# Voice Agent Code

This is the **voice agent code** — the Express server that runs on Railway and provides voice/text access to Claude Code, plus scheduled build jobs.

## Naming

| Name | What it is | Location |
|------|-----------|----------|
| **Voice agent code** | This repo — the Express server, scheduler, API | Local: `~/kingdom_of_god/serenade/voice-agent/` · Railway: `/app/` |
| **Serenade remote copy** | A clone of the main serve_boldly repo that Claude works against | Railway: `/data/serenade-remote-copy/` |
| **serve_boldly** | The main Serenade codebase | Local: `~/kingdom_of_god/serenade/serve_boldly/` · GitHub: `seanross237/serve_boldly` |

## Deployment

Railway does NOT auto-deploy from git pushes. **Always deploy after pushing.** Run:

```
railway up
```

On every deploy, the container restarts and the entrypoint script pulls the latest serve_boldly main into the remote copy.

The project is linked to the `lovely-nurturing` Railway project, service `voice-agent`. If you get "no linked project" or "no service" errors, re-link:

```
railway link --project lovely-nurturing
railway service 733c998e-17db-4422-a81f-4007b864dcb7
railway up
```

## Architecture

Express server with a single-page frontend (public/index.html).

Pipeline: Browser → STT (AssemblyAI) → Claude CLI (`claude -p`) → TTS (OpenAI) → Browser

- `server.js` — Express routes, scheduled jobs API
- `lib/claude.js` — Spawns `claude -p` CLI subprocess against the serve boldly remote copy
- `lib/scheduler.js` — Scheduled build job runner (checks every 30s, reads specs, runs Claude, commits/pushes)
- `lib/stt.js` — AssemblyAI speech-to-text
- `lib/tts.js` — OpenAI gpt-4o-mini-tts text-to-speech
- `lib/logger.js` — Fire-and-forget logging to Supabase `agent_logs`
- `lib/notes.js` — Voice note capture to Supabase `voice_agent_notes`
- `public/index.html` — Full frontend (HTML/CSS/JS in one file)

## Scheduled Builds

The scheduler polls `agent_scheduled_jobs` (Supabase) every 30 seconds. Jobs have:
- `spec_file` — path to a build spec in serve_boldly (e.g., `build-specs/remove-admin-prefix.md`)
- `run_at` — optional scheduled time
- `depends_on` — optional job ID that must complete first (for chaining)
- `branch` — git branch to create and push to

API endpoints:
- `GET /api/jobs` — list jobs
- `POST /api/jobs` — create a job (`{ title, spec_file, branch, run_at, depends_on }`)
- `POST /api/jobs/:id/cancel` — cancel a queued job
- `POST /api/jobs/:id/retry` — retry a failed job

Create specs locally with `/schedule-build` in Claude Code, push to main, then queue via API.

## Sessions

Sessions are Claude CLI conversation sessions. The session ID is stored in the browser's localStorage and passed via `--resume` flag to continue conversations. "New Session" clears it.

## Auth

- Claude CLI authenticates via `CLAUDE_CODE_OAUTH_TOKEN` env var (Claude Max plan, no API key)
- App auth uses `AUTH_TOKEN` env var (Bearer token in headers)
- All API keys are Railway environment variables
