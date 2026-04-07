# ai_vids_virality

End-to-end pipeline for turning real-world viral / pop-culture / political moments into AI-generated comedy sketch videos. Human review gates at every decision point, file-based state, no database, single-file kanban UI.

The system is organized as seven phases, each leaving a clean seam for the next:

| Phase | Ships |
|---|---|
| **1** | State machine, file store, stub pipeline skeleton, kanban UI |
| **2** | Real radar: Reddit / Hacker News / Google News / YouTube trending + comedy-lens analyzer + cron-ready bash wrapper |
| **3** | Multi-model idea factory with Claude CLI + OpenAI + Gemini adapters, side-by-side premise review, leaderboard |
| **4** | Storyboard pipeline with beat-sheet LLM call + nano-banana-2 character ref sheets and per-beat frames |
| **5** | Video generation with 5 pluggable providers (Kling / Luma / Runway / Pika / Veo) + ffmpeg stitching + cost cap |
| **6** | Two-layer AI critic (per-clip shot check with retry loop + full-sketch structured critique) |
| **7** | Publishing layer (local archive + YouTube Shorts + stubs), keyboard shortcuts, SSE auto-refresh, cost dashboard, insights, bulk reject |

The full operational guide — how to run the radar, deploy to the Hetzner box, add a new adapter, where logs go, every env var — lives in **[RUNBOOK.md](./RUNBOOK.md)**. The phase-by-phase build logs live in `phases/phase-N-report.md`.

## Quick start (laptop)

```bash
cd other_projects/ai_vids_virality
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Offline test suite (no network, no LLMs, no video APIs)
pytest -m "not network and not llm and not gemini and not video and not critic and not publish" -q

# Pull real signals + run the full pipeline. Without API keys set this
# exercises every stub fallback path end-to-end.
python -m pipelines.run_skeleton

# Launch the web UI
uvicorn backend.main:app --reload --port 8000
# open http://localhost:8000
```

Default UI starts on **Premise Review**. Use the top-nav tabs to switch pages, or the keyboard shortcuts below.

## Keyboard shortcuts (Phase 7)

| Key | Action |
|---|---|
| `j` / `↓` | next card on the current page |
| `k` / `↑` | previous card |
| `a` | approve the highlighted card |
| `r` | reject the highlighted card |
| `p` | publish (critic review only) |
| `/` | open the `+ new idea` modal |
| `cmd+enter` | submit the new-idea modal |
| `esc` | close any open modal / overlay |
| `?` | show / hide keyboard shortcut help |

## API keys (all optional, all graceful-fallback)

Every adapter checks its env var at runtime. Without the key, the adapter logs a warning and either uses a deterministic stub (Phase 3/6) or copies the placeholder asset (Phase 4/5/7 local archive). The pipeline always completes.

```bash
# Phase 3 idea factory
export OPENAI_API_KEY=sk-...
export GEMINI_API_KEY=AIza...
# Claude uses the `claude -p` CLI instead of an env var.

# Phase 4 storyboard
export GEMINI_API_KEY=AIza...

# Phase 5 video providers
export KLING_AK=...; export KLING_SK=...
export LUMA_API_KEY=...
export RUNWAY_API_KEY=...
export FAL_KEY=...                  # Pika via fal.ai
export GOOGLE_VERTEX_KEY=...        # Veo (partial)

# Phase 6 critic
# Uses GEMINI_API_KEY (for GeminiVideoCritic) and the claude CLI.

# Phase 7 publishing
export YT_REFRESH_TOKEN=...
export YT_CLIENT_ID=...
export YT_CLIENT_SECRET=...
```

See **[RUNBOOK.md](./RUNBOOK.md)** for how to get each one.

## Offline test groups

Tests are marker-gated so the default run never touches the network or burns tokens:

```bash
pytest -m "not network and not llm and not gemini and not video and not critic and not publish"
```

To opt into real-API tests:

```bash
pytest -m llm       # Phase 3 Claude CLI integration (~$0.01)
pytest -m gemini    # Phase 4 real nano-banana-2 (skipped without GEMINI_API_KEY)
pytest -m video     # Phase 5 real video providers (no tests ship, marker reserved)
pytest -m critic    # Phase 6 real critic APIs (no tests ship, marker reserved)
pytest -m publish   # Phase 7 real YouTube upload (skipped without YT_* env)
pytest -m network   # radar network integration (Hacker News)
```

## Layout

```
ai_vids_virality/
  config/             # comedy-lens.md + every adapter yaml (models / storyboard / video / critic / publishing)
  data/               # signals, queues, sketches, published, leaderboard.json (all JSON on disk)
  collectors/         # reddit / hacker_news / google_news / youtube_trending / reddit_stub (fixture)
  analyzers/          # score_signals (lens-driven keyword scorer)
  idea_factory/       # ModelAdapter ABC + claude_cli / openai_stub / gemini_stub + factory
  storyboard/         # StoryboardAdapter ABC + gemini_image / stub_storyboard + beats + pipeline
  video_gen/          # VideoProviderAdapter ABC + kling / luma / runway / pika / veo / stub_video + pipeline + stitch
  critic/             # CriticAdapter ABC + gemini_video / claude_frame / stub_critic + pipeline + frame_sampler
  publishing/         # Publisher ABC + local_archive / youtube_shorts / stub_publisher + pipeline
  state/              # machine.py (enum + transitions) + store.py (file-based store) + leaderboard.py
  pipelines/          # run_skeleton.py + run-radar.sh (cron wrapper)
  backend/            # FastAPI (main.py) + events.py (SSE pub/sub) + stats.py + static/index.html
  tests/              # pytest suite (~270 offline tests)
  logs/               # cron log sink (radar-YYYY-MM-DD.log)
  phases/             # phase-1-plan.md, phase-1-report.md, ... phase-7-report.md
  RUNBOOK.md          # the operational guide
  README.md           # this file
```

## What "works" right now

- Collectors pull real signals from four public sources every run and dedupe via `.seen-ids`
- Real Claude generates real comedy premises for every promoted signal
- OpenAI and Gemini fall back to deterministic stub premises when their keys aren't set, so the side-by-side UI still has three variants per sketch
- Storyboard pipeline generates a real beat sheet via Claude and real nano-banana-2 character/frame images when `GEMINI_API_KEY` is set (stub frames otherwise)
- Video pipeline routes to the first available provider (Kling/Luma/Runway/Pika) with cost cap enforcement, ffmpeg stitches the final cut
- Two-layer critic runs per-clip shot checks with up to 2 retries and a full-sketch critique with per-axis scoring
- Publishing writes to a local archive and uploads to YouTube Shorts as a `private` category-23 video when `YT_REFRESH_TOKEN` is set
- Web UI has keyboard shortcuts, SSE auto-refresh, cost dashboard, approval insights, bulk reject, help overlay
- Cron-ready `pipelines/run-radar.sh` for the Hetzner box

The full runbook for operating the system is in **[RUNBOOK.md](./RUNBOOK.md)**.
