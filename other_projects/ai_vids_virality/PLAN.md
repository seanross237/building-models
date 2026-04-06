# ai_vids_virality — Plan

End-to-end automated pipeline for turning real-world viral / pop-culture / political moments into AI-generated comedy sketch videos, with human review gates at the key decision points.

A second variant of the pipeline targets **music videos** — see "Variant: Music Videos" at the bottom. Most infrastructure is shared.

---

## 1. Goals

- Steady stream of fresh sketch premises sourced from what's actually happening in the world.
- Minimize human time on bad ideas — review gates feel like Tinder, not a spreadsheet.
- Produce publish-ready short videos (15–60 sec) with consistent characters and coherent shots.
- AI critics catch obvious failures before a human sees them.
- A **manual idea queue** so I can drop in my own ideas at any time and they slot into the same pipeline.
- Multi-model A/B testing for the creative stages (different LLMs writing premises against the same signal).
- Track cost per sketch end-to-end.

---

## 2. Architectural decisions (grounded in what already exists)

We are not inventing this from scratch. Three existing systems in the repo give us the patterns:

### research-radar — radar/collector/analyzer pattern
`research_hub/research-radar/`

This is a working topic-driven content radar. We **clone its patterns** for the news-scanning layer:

- **Collectors** are small per-source scripts (Python or shell) that fetch items, dedupe via a `.seen-ids` file, and write each item as a markdown file with YAML frontmatter into `data/topics/{topic}/{source}/items/{id}.md`.
- **Analyzers** are Python scripts that find unanalyzed items, build a Claude prompt with `prompt.md` + `schema.json` + a "what we care about" lens markdown, spawn `claude -p --output-format json`, parse the JSON, write a summary file, and gate items into a queue if they score above a threshold.
- **Pipelines** are bash scripts (`nightly-radar.sh`) that orchestrate collectors → analyzers → queue gating → final output. Easy to debug, easy to schedule.
- **Storage is files in git.** No database. Inspectable, version-controlled, free.
- **The "lens"** is a single markdown file (`config/what-we-care-about-right-now.md`) that defines the scoring rubric. We swap the research lens for a **comedy lens**.

Key files to read for the pattern:
- `research_hub/research-radar/runner/agent-runner/lib/executor.js` (1–50) — how tasks shell out
- `research_hub/research-radar/runner/agent-runner/lib/claude.js` — `spawn('claude', args)` subprocess pattern
- `research_hub/research-radar/analyzers/summarize-and-score/analyze-items.py` (50–150) — analyzer loop
- `research_hub/research-radar/pipelines/nightly-radar.sh` — orchestration
- `research_hub/research-radar/config/topics-we-care-about.yaml` — topic config schema

What we keep: collector layout, dedupe, markdown-with-frontmatter items, JSON schema for analyzer outputs, queue manifests, lens-based scoring, bash pipelines.

What we change: sources (Reddit/X/TikTok/news instead of YouTube/papers), the lens (comedy potential instead of research relevance), the downstream output (sketch ideas instead of HTML presentations).

### colossus — controller-spawns-workers in tmux
`research_hub/big-thinkers/colossus/`

Colossus is an autonomous controller that runs every 5 min via `bootstrap.sh`, reads state files, decides what to do, and **spawns worker Claude sessions in tmux windows** of the same tmux session. We adapt this pattern for the **idea generation phase**:

- A single `idea-factory` tmux session on the Hetzner box
- Controller window reads the radar's "fresh signals" queue, decides which signals are worth ideating on, and spawns worker windows
- Each worker window runs `claude -p` (or `gemini`/`codex`) on one signal, generates premises, writes them to the idea queue, exits
- Concurrency cap: 3 workers at a time (same as colossus)

Key file: `research_hub/big-thinkers/colossus/CONTROLLER.md` — read it. The "How to Spawn Workers" section (lines 57–89) is exactly the pattern we want, just with our prompts.

### remote-dev-box-plan.md — Hetzner setup
`eywa/super-eywa/sticky-notes/daily-journals/2026-04-03/remote-dev-box-plan.md`

There is already a detailed plan for a Hetzner CPX31 box (4 vCPU, 8 GB, $15/mo) replacing Railway as the home for nightly cron jobs and persistent agent sessions. Our pipeline **piggybacks on this same VM** — we don't spin up a separate one.

What we use from it:
- The VM itself + its `~/.tmux.conf`, ssh config, claude/gh/git auth
- The cron pattern for nightly jobs
- The Telegram failure-notification hook (`notify-failure.sh`)
- The "commit + push after job" pattern (`radar-commit.sh`)

We add a new top-level directory on the VM at `~/kingdom_of_god/home-base/other_projects/ai_vids_virality/` and a new set of cron lines + tmux session.

### serenade — nano banana 2 integration
`other_projects/the_old_ways/serenade-your-story/`

A subagent investigated this and found that **serenade calls nano banana 2 via an external n8n webhook**, not from code. The integration lives at `pomypom237.app.n8n.cloud`, and serenade only POSTs `{order_id, form_data, ...}` and waits for a callback.

**Implication:** for ai_vids_virality we have two options:

1. **Direct API**: call Google AI Studio's Gemini image model (`gemini-2.5-flash-image` / nano banana 2) from Python ourselves. Simpler, no external dependency, full control over prompts, retries, and seeds.
2. **Reuse the same n8n instance**: build a new n8n workflow that wraps the image call and POST to it from our pipeline. Decoupled but adds an external dependency we can't easily debug.

**Recommendation:** go direct (option 1) for the storyboard layer. Use n8n only if we end up wanting the same image gen pattern shared with other projects. We do borrow the **batch_number / sequence_number metadata pattern** from serenade's database schema for ordering frames within a sketch.

---

## 3. Infrastructure: where things run

### The Hetzner box

The radar, idea factory, storyboard generation, video generation, and AI critic all run on the same Hetzner VM described in `remote-dev-box-plan.md`. The web UI is the only piece that runs locally on the laptop (or also on the VM behind a tunnel — see Phase 5).

### tmux session layout on the VM

```
ai-vids (tmux session)
  ├─ window 1: monitor          — htop, tail -F log files
  ├─ window 2: radar-runner     — manual radar runs / debugging
  ├─ window 3: idea-controller  — controller loop watching the signal queue
  ├─ window 4: idea-w-001       — spawned worker (one per active signal)
  ├─ window 5: idea-w-002       — spawned worker
  ├─ window 6: storyboard       — storyboard worker pool
  ├─ window 7: video            — video gen worker pool
  └─ window 8: critic           — AI critic worker
```

The session is named `ai-vids` (parallel to colossus's `colossus` session). Workers are spawned with `tmux new-window -t ai-vids -n "w-NNN"` followed by `tmux send-keys` to launch the appropriate `claude -p` / `gemini` / Python script.

### Cron jobs

Added to the same crontab as the research-radar nightly job:

```cron
# News scan — every 30 min during waking hours (PT)
*/30 13-06 * * * cd ~/kingdom_of_god/home-base/other_projects/ai_vids_virality && bash pipelines/scan-news.sh >> /var/log/ai-vids/news-$(date +\%Y-\%m-\%d).log 2>&1

# Heavy nightly digest + idea generation kickoff — 7:00 UTC (midnight PT)
0 7 * * * cd ~/kingdom_of_god/home-base/other_projects/ai_vids_virality && bash pipelines/nightly-digest.sh >> /var/log/ai-vids/digest-$(date +\%Y-\%m-\%d).log 2>&1

# Commit + push of any new signals/ideas — 15 min after digest
15 7 * * * bash ~/scripts/ai-vids-commit.sh >> /var/log/ai-vids/commit-$(date +\%Y-\%m-\%d).log 2>&1
```

The lighter every-30-min scan catches breaking news. The nightly digest does heavier work — full analysis, premise generation, deduping the day's signals — when the human is asleep so the morning queue is fresh.

Failure notifications go through the existing `notify-failure.sh` Telegram hook.

---

## 4. Pipeline stages

```
Radar → Idea Factory → [Review 1] → Script/Beats → Storyboard → [Review 2] → Video Gen → AI Critic → [Review 3] → Publish
                  ↑
       Manual Idea Queue feeds in here
```

### Stage 1 — Radar (collectors)

Modeled on `research-radar/collectors/`. One subdirectory per source, each with its own dedupe file and item-writing script.

**Sources (build in this order):**
1. Reddit (PRAW or pushshift) — easiest, no auth headaches: r/popular, r/all, plus a curated list (r/politics, r/celebritynews, r/entertainment, niche sub for the comedy tone we want)
2. X / Twitter — via xAI's API, twscrape, or a paid scraper. Trending + curated lists.
3. Google Trends — `pytrends`, rising queries
4. NewsAPI / GDELT — pop culture (NewsAPI) + political (GDELT)
5. YouTube trending — yt-dlp (already installed on the VM for research-radar)
6. TikTok trending — last because it's the hardest. 3rd party scraper or TikTok Research API.

**Item file format** (`data/signals/{source}/items/{id}.md`):
```markdown
---
id: reddit-abc123
source: reddit
source_url: https://reddit.com/r/...
title: ...
captured_at: 2026-04-06T13:42:00Z
heat_score_raw: 0.87        # source-native popularity
freshness_hours: 4
tags: [political, scandal]
---

## Summary
2-3 sentences of what happened.

## Why this matters
Optional collector-side hint.

## Source content
Original post text, top comments, headline excerpt, etc.
```

**Dedupe:** `.seen-ids` file per collector, same as research-radar.

### Stage 2 — Analyzer (comedy lens)

Modeled on `research-radar/analyzers/summarize-and-score/`. The lens is at `config/comedy-lens.md` and defines what makes a signal sketchable.

**Analyzer prompt outputs:**
```json
{
  "signal_id": "...",
  "summary": "1-paragraph plain-language summary",
  "sketchability_score": 1-10,
  "comedy_angles": [
    {"angle": "absurdist", "note": "..."},
    {"angle": "satire", "note": "..."}
  ],
  "character_archetypes": ["politician", "out-of-touch CEO"],
  "topical_window_hours": 48,
  "should_promote": true
}
```

If `should_promote` is true and `sketchability_score >= 7`, the signal moves to the **idea factory queue** at `data/queues/idea-factory/{id}.json`.

### Stage 3 — Idea Factory (controller + workers in tmux)

**Two parts:**

**a) Manual idea queue (`data/queues/manual-ideas/`):** a directory I can drop markdown files into at any time. Each file is just:

```markdown
---
id: manual-2026-04-06-001
created_at: 2026-04-06T15:00:00Z
source: manual
priority: high
---

quick brain dump of an idea I had in the shower
```

The web UI has a "+ New Idea" button that creates these files. They flow into the same downstream pipeline as auto-generated ideas — they just skip Stage 2 (no analyzer, no scoring).

**b) Auto idea factory (controller pattern from colossus):**

A controller loop running in `ai-vids:idea-controller` window:

```bash
while true; do
  # 1. Read data/queues/idea-factory/ for unprocessed signals
  # 2. Pick top N (by sketchability_score), respecting concurrency cap
  # 3. For each, choose which model(s) to use (multi-model A/B — see Section 5)
  # 4. Spawn a worker tmux window per (signal × model) combo
  # 5. Sleep 60s, loop
  sleep 60
done
```

Each worker runs one of:
- `claude -p "$prompt" --output-format json`
- `codex exec "$prompt" --json` (or whatever the codex CLI flags are)
- `gemini -p "$prompt"` (Google CLI) or a curl to Gemini API
- A small Python wrapper around the OpenAI API for GPT-5.x

Each worker writes its premises into `data/queues/premise-review/{signal_id}__{model}.json`:

```json
{
  "signal_id": "...",
  "model": "claude-opus-4-6",
  "premises": [
    {
      "logline": "...",
      "synopsis": "...",
      "tone": "absurdist",
      "target_length_sec": 30,
      "characters": [...],
      "twist": "..."
    },
    ...
  ],
  "generated_at": "...",
  "cost_cents": 12
}
```

**The model choice is part of the experiment.** Section 5 covers the comparison harness.

### Stage 4 — Review Gate 1 (Premise review)

Web UI swipe-style. Loads premise files from `data/queues/premise-review/`.

When multiple models generated premises for the same signal, the UI shows them side-by-side so I can pick the best (or take the best from each).

Actions: **approve / reject / edit / regenerate / "more from this model" / "more from a different model"**.

Approved premises move to `data/queues/scripted/{premise_id}.json` and trigger Stage 5. The model that produced an approved premise gets a +1 in the model leaderboard (Section 5).

### Stage 5 — Script / Beat Sheet

LLM expands an approved premise into a structured shot list. Lives at `data/sketches/{sketch_id}/beats.json`:

```json
{
  "sketch_id": "sk-2026-04-06-001",
  "premise_id": "...",
  "beats": [
    {
      "n": 1,
      "duration_sec": 4,
      "location": "office",
      "characters": ["politician_A", "intern_B"],
      "action": "politician slams door",
      "dialogue": null,
      "camera": "wide",
      "visual_note": "morning light, cluttered desk"
    },
    ...
  ]
}
```

### Stage 6 — Storyboard (nano banana 2, called directly)

For each sketch:

1. **Character reference sheet** — generate front + side views of every character in the cast. Save to `data/sketches/{sketch_id}/refs/{character}.png`. These become the visual anchor for every later frame.
2. **Per-beat key frames** — for each beat, generate a start frame (and optionally end frame), passing the relevant character ref images as additional inputs. Save to `data/sketches/{sketch_id}/storyboard/beat-{n}-start.png` etc.
3. **Metadata file** — `data/sketches/{sketch_id}/storyboard.json` with prompt, seed, model version, cost per frame.

**API:** Google AI Studio's `gemini-2.5-flash-image` (nano banana 2) endpoint. Auth via `GEMINI_API_KEY` env var on the VM. Python client (`google-generativeai` package).

We use the same `sequence_number` ordering pattern as serenade's database (`batch_number=0` for ref sheet, `batch_number=N` for beat N frames). Borrowed from serenade's schema, not its code.

### Stage 7 — Review Gate 2 (Storyboard review)

Grid view in the web UI. Catches visual disasters before burning video-gen budget. Actions: approve / regen frame / regen all frames for a beat / reject sketch entirely.

**This is the most important cost-saver in the pipeline** — image gen is cents per frame, video gen is dollars per clip.

### Stage 8 — Video Generation

For each beat, call a video API with the storyboard frame(s) as anchors.

**Adapter layer** at `backend/video_gen/providers/`:
- `kling.py` — Kling 1.6 / 2.0, supports start+end frames
- `luma.py` — Luma Dream Machine, supports start+end frames
- `veo.py` — Google Veo 3 via Vertex, native audio
- `runway.py` — Runway Gen-4
- `pika.py` — fallback

Each provider exposes the same interface: `generate(start_frame, end_frame, prompt, duration_sec) -> clip_path`.

Default routing: Kling for anchored shots, Veo 3 for any beat with dialogue (it gives us audio for free).

After all beats render, ffmpeg stitches the clips into the final cut at `data/sketches/{sketch_id}/final.mp4`.

### Stage 9 — AI Critic

**Two layers:**

1. **Shot-level check** — runs per clip. Multimodal model verifies: matches the storyboard frame? artifacts? character consistent with ref sheet? If fail, auto-regenerate (max 2 retries) before bothering the human.
2. **Full-sketch critic** — runs on the assembled cut. Scores comedic timing, pacing, punchline landing, audio clarity, "is it actually funny." Outputs structured JSON + concrete fix suggestions.

**Models we'll try for the critic:** Gemini 2.5 Pro (native video input), Claude with sampled frames, GPT-5.x with sampled frames + audio transcript. Same multi-model A/B pattern as the idea factory.

### Stage 10 — Review Gate 3 (Final review)

Web UI shows the final cut + critic report side-by-side. Actions: publish / regen / reject. Published sketches get the entire history (signal → premise → beats → storyboard → clips → critic → final) archived in `data/published/{sketch_id}/`.

---

## 5. Multi-model A/B testing

For every creative stage that uses an LLM (idea factory, beat-sheet generation, AI critic), we run **multiple models on the same input** and track which one I end up approving.

### Model roster (initial)

| Stage | Models to test |
|---|---|
| Idea factory (premises) | Claude Opus 4.6, GPT-5.x, Gemini 2.5 Pro, Claude Sonnet 4.6 (cheap baseline) |
| Beat sheet | Same set |
| Critic | Gemini 2.5 Pro, Claude Opus 4.6, GPT-5.x |

### Config

`config/models.yaml`:
```yaml
idea_factory:
  - id: claude-opus
    cli: claude
    args: ["-p", "--model", "claude-opus-4-6", "--output-format", "json"]
    cost_per_1k_tokens: ...
  - id: gpt5
    cli: python
    args: ["scripts/openai_premise.py", "--model", "gpt-5"]
    cost_per_1k_tokens: ...
  - id: gemini25
    cli: gemini
    args: ["-p"]
    cost_per_1k_tokens: ...
```

### Routing

Per signal, the controller decides which models to spawn. Options:
- **All models**, every signal — most data, most expensive
- **Tournament**: cheap models run first, top-N premises advance, expensive models only run on signals where the cheap models found something promising
- **Budget-aware**: respect `BUDGET.md`-style daily caps

Start with "all models on a small N per night," then move to tournament once we have enough data to know which models to favor.

### Leaderboard

`data/leaderboard.json` is updated whenever I approve/reject a premise:

```json
{
  "claude-opus": {"premises": 142, "approved": 38, "approval_rate": 0.27, "avg_cost_per_approved_cents": 47},
  "gpt5":        {"premises": 142, "approved": 41, "approval_rate": 0.29, "avg_cost_per_approved_cents": 52},
  "gemini25":    {"premises": 142, "approved": 22, "approval_rate": 0.15, "avg_cost_per_approved_cents": 12}
}
```

The web UI surfaces this on the dashboard so I can see, at a glance, which model is winning by approval rate, cost per approved premise, and time-to-publish.

---

## 6. Data model (file-based, like research-radar)

```
ai_vids_virality/
  config/
    comedy-lens.md          # the scoring rubric for the analyzer
    sources.yaml            # which collectors to run, on what cadence
    models.yaml             # the multi-model roster
    thresholds.yaml         # promotion thresholds per stage
  data/
    signals/
      reddit/items/{id}.md
      reddit/.seen-ids
      twitter/items/{id}.md
      ...
    queues/
      idea-factory/{id}.json       # signals ready for premises
      premise-review/{id}.json     # premises waiting for human
      manual-ideas/{id}.md         # user-dropped ideas
      scripted/{id}.json           # premises approved, awaiting beats
      storyboard-review/{id}.json
      video-gen/{id}.json
      final-review/{id}.json
    sketches/{sketch_id}/
      premise.json
      beats.json
      refs/{character}.png         # character reference sheet
      storyboard/beat-{n}-start.png
      storyboard.json
      clips/beat-{n}.mp4
      final.mp4
      critic.json
      history.json                 # full state machine log
    published/{sketch_id}/         # archive after publish
    leaderboard.json
  pipelines/
    scan-news.sh                   # half-hour radar
    nightly-digest.sh              # midnight heavy run
    idea-controller.sh             # the colossus-style controller loop
  collectors/
    reddit/
    twitter/
    google_trends/
    news_api/
    youtube_trending/
    tiktok/
  analyzers/
    score-signals/
      prompt.md
      schema.json
      analyze-signals.py
  idea_factory/
    workers/
      claude_premise.sh
      openai_premise.py
      gemini_premise.sh
  storyboard/
    gen_refs.py
    gen_frames.py
  video_gen/
    providers/
      kling.py
      luma.py
      veo.py
      runway.py
      pika.py
    stitch.py
  critic/
    shot_check.py
    full_sketch.py
  backend/                         # FastAPI for the web UI
    api/
    state/
  frontend/                        # Next.js kanban UI
  scripts/
    notify-failure.sh              # symlink to existing
    ai-vids-commit.sh              # commit + push the day's data
  PLAN.md                          # this file
  README.md
```

---

## 7. Visual interface

**Kanban dashboard** — one column per pipeline stage, cards flow left to right.

```
[Signals] [Ideas] [Approved] [Storyboard] [Video] [Critic] [Publish]
```

**Side panels:**
- **Live signal feed** — incoming signals from collectors with a "promote to idea factory" button so I can manually inject a signal I spotted myself
- **Manual idea entry** — `+ New Idea` button writes a markdown file into `data/queues/manual-ideas/` and the card appears in the "Approved" column (or "Ideas" if I want it to go through the factory for variations)
- **Model leaderboard** — live approval rates and cost-per-approved by model
- **Spend today** — running total

**Card detail pane:** click any card to expand. Shows everything: source signal, all premises (grouped by model), approved premise, beat sheet, storyboard grid, video preview, critic report, full history log, cost breakdown.

**Review modes** — dedicated swipe screens for each gate:
- **Premise review:** `J/K` next-prev, `A` approve, `R` reject, `E` edit, `G` regenerate, `M` swap to next model's variant
- **Storyboard review:** grid of frames, click any frame to regen just that one
- **Final review:** video player + critic report side-by-side

**Stack:**
- Backend: Python FastAPI on the Hetzner VM (same ecosystem as collectors / analyzers)
- Frontend: Next.js + Tailwind, also served from the VM behind a Cloudflare tunnel or Tailscale
- Realtime: SSE stream from the FastAPI backend so cards move between columns without refresh
- Auth: Tailscale or Cloudflare Access — single-user, no need to build login

---

## 8. Build order

Build the smallest end-to-end loop first using stub media, then enrich each stage. Phases roughly mirror the structure I'll commit one-per-PR.

### Phase 1 — Skeleton end-to-end (proof of life)
- One collector (Reddit r/all)
- One analyzer with a stub comedy lens
- Minimal idea factory using just Claude (single model, no controller loop yet — just a script)
- Manual idea queue (drop-a-markdown-file workflow, no UI yet)
- Minimal kanban UI (list views, no styling)
- Premise review gate working (approve/reject)
- Stub storyboard + video (placeholder PNG/MP4)
- File-based data model and per-sketch directory layout

**Goal:** can approve a premise and watch a card move through every column to "published" with stub media. Runs locally first, deployed to the Hetzner box once it's stable.

### Phase 2 — Real radar
- More collectors: Twitter, Google Trends, NewsAPI, YouTube trending
- Real comedy lens
- Cron jobs on the Hetzner VM (every 30 min + nightly digest)
- Telegram failure notification hook
- TikTok last (it's painful)

### Phase 3 — Multi-model idea factory
- Add codex / GPT-5 worker
- Add Gemini worker
- Build the colossus-style controller loop in `ai-vids:idea-controller` tmux window
- `models.yaml` config
- Side-by-side premise comparison in the review UI
- Leaderboard tracking

### Phase 4 — Storyboard
- nano banana 2 direct integration (Google AI Studio, `gemini-2.5-flash-image`)
- Character reference sheet generation
- Beat sheet generation from premise
- Per-beat key frame generation referencing character sheets
- Storyboard review gate with regen-per-frame
- Grid view in the UI

### Phase 5 — Video generation
- Pluggable provider adapter
- Kling (start+end) as primary
- Veo 3 as second provider for dialogue shots
- ffmpeg stitching
- Cost tracking per clip

### Phase 6 — AI critic
- Shot-level check with auto-regen (bounded retries)
- Full-sketch critic with structured scoring + fix suggestions
- Critic-model A/B testing (same as idea factory)
- Surface critic report in the final review UI

### Phase 7 — Polish + publishing
- Few-shot the idea factory with past approved/rejected premises (learning from the queue)
- Publishing integrations: YouTube Shorts API first, then TikTok and X
- Better analytics: which signal sources → which approval rates → which sketches → which views
- Web UI polish, keyboard shortcuts, tighter swipe flows

### Phase 8 — Music videos variant (see Section 11)

---

## 9. Open questions

- Which publishing platforms first? YouTube Shorts is easiest API-wise; TikTok is harder.
- Recurring cast across sketches, or fresh cast every time? Affects whether the character reference sheets are per-sketch or per-channel.
- Music + SFX — library, or generate with Suno / ElevenLabs / Stable Audio?
- Branding / channel identity — one show or multiple channels by tone?
- Hard budget cap per sketch (auto-reject if storyboard regens exceed N)?
- Does the radar's comedy lens need different sub-lenses for political vs. pop-culture vs. absurdist tones?
- For multi-model A/B: do we hide model identity from the human reviewer to avoid bias? (Probably yes.)

---

## 10. Variant: Music Videos

A second pipeline that reuses most of the infrastructure but specializes a few stages.

**What changes:**
- **Radar:** optional. Music videos can be triggered from a song input rather than a trending topic. (Could also have a radar for trending songs on Spotify / TikTok sounds.)
- **Idea Factory → Concept Factory:** takes a song (or song + reference track) and generates 3–5 visual concept treatments. Each describes aesthetic, narrative arc, recurring motifs, key imagery. Same multi-model A/B harness.
- **Script → Shot list timed to the track:** instead of beats with dialogue, we produce a shot list timed to musical sections (intro, verse, chorus, bridge). Needs tempo + structure analysis of the audio first. Each shot has start/end timestamps anchored to the waveform.
- **Storyboard:** same — nano banana 2 generates key frames per shot. Aesthetic consistency matters even more here than for sketches, so the character/style reference sheet is critical.
- **Video Gen:** same provider adapter, optimized for longer form (3–5 min). Probably favors Kling/Luma for visual continuity. No dialogue audio needed from the video model — the track is the audio.
- **Assembly:** ffmpeg stitches clips *to the beat*, using the timestamped shot list. This is the new tricky piece — handle tempo-sync and transitions.
- **AI Critic:** scores on visual aesthetic, rhythm/sync with the music, narrative coherence, attention-holding for the full song. Different rubric, same scaffolding.

**Shared with sketch pipeline:**
- Hetzner box, tmux session layout, cron infrastructure
- Kanban UI, review gates, file-based data model
- Character/style reference sheet system
- Video provider adapter
- Cost + leaderboard tracking
- AI critic framework

**Build order:** sketch pipeline first end-to-end. The music video variant becomes Phase 8 — a specialization of an already-working system, not a parallel build.

---

## 11. References — files I read while writing this plan

- `research_hub/research-radar/runner/agent-runner/lib/executor.js` — task → claude subprocess pipeline
- `research_hub/research-radar/runner/agent-runner/lib/claude.js` — `spawn('claude')` pattern
- `research_hub/research-radar/runner/agent-runner/lib/scheduler.js` — cron loop (we replace with system cron)
- `research_hub/research-radar/analyzers/summarize-and-score/` — analyzer prompt + schema pattern
- `research_hub/research-radar/pipelines/nightly-radar.sh` — bash orchestration
- `research_hub/research-radar/config/topics-we-care-about.yaml` — topic config schema
- `research_hub/big-thinkers/colossus/CONTROLLER.md` — controller loop + tmux worker spawning (lines 57–89 are the key worker-spawn pattern)
- `research_hub/big-thinkers/colossus/CLAUDE.md` — file-based state conventions
- `eywa/super-eywa/sticky-notes/daily-journals/2026-04-03/remote-dev-box-plan.md` — Hetzner setup, tmux config, cron pattern, Telegram failure notification
- `other_projects/the_old_ways/serenade-your-story/` — nano banana 2 is integrated via n8n webhook (we go direct instead); borrow `batch_number` ordering pattern only

---

## 12. Next step

Start Phase 1 on the laptop, then move to the Hetzner box once the skeleton is stable.

First code to write:
1. `config/comedy-lens.md` — the scoring rubric (2-3 paragraphs is enough to start)
2. `collectors/reddit/fetch.py` — the simplest collector, modeled on `research-radar/collectors/youtube/fetch-topic-videos.py`
3. `analyzers/score-signals/{prompt.md, schema.json, analyze-signals.py}` — modeled on `research-radar/analyzers/summarize-and-score/`
4. `idea_factory/workers/claude_premise.sh` — wraps `claude -p` for one signal
5. `pipelines/scan-news.sh` — bash orchestration of the above
6. Minimal FastAPI + Next.js kanban with stubbed video columns

That's the smallest loop that produces a real premise from a real Reddit post and lets me click "approve" in a UI.
