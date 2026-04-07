# ai_vids_virality — RUNBOOK

This is the operational guide. It's written for a future self who has forgotten everything. Read it top to bottom the first time, then use the table of contents as a jump menu.

- [1. Morning review workflow (what you'll actually do daily)](#1-morning-review-workflow-what-youll-actually-do-daily)
- [2. Running the radar manually](#2-running-the-radar-manually)
- [3. Environment variables (every API key)](#3-environment-variables-every-api-key)
- [4. Deploying to the Hetzner box](#4-deploying-to-the-hetzner-box)
- [5. Adding a new collector](#5-adding-a-new-collector)
- [6. Adding a new model adapter (idea factory)](#6-adding-a-new-model-adapter-idea-factory)
- [7. Adding a new storyboard adapter](#7-adding-a-new-storyboard-adapter)
- [8. Adding a new video provider](#8-adding-a-new-video-provider)
- [9. Adding a new critic adapter](#9-adding-a-new-critic-adapter)
- [10. Adding a new publisher](#10-adding-a-new-publisher)
- [11. Where logs live](#11-where-logs-live)
- [12. Backing up data](#12-backing-up-data)
- [13. pytest marker cheat sheet](#13-pytest-marker-cheat-sheet)
- [14. Troubleshooting](#14-troubleshooting)
- [15. Cost control](#15-cost-control)
- [16. File system layout reference](#16-file-system-layout-reference)

---

## 1. Morning review workflow (what you'll actually do daily)

Assumes the Hetzner box has been running the radar + factory overnight.

1. **Open the UI** at `http://localhost:8000` (or the Tailscale URL of the Hetzner box).
2. **Check the cost widget** in the top nav. If today's spend is already more than expected, open the tooltip to see which stage burned the budget.
3. **Signals page** (`signal` tab): scan for signals worth promoting. Use `j`/`k` to navigate, the checkbox column to batch-select, and the bulk `reject selected` button to clear out noise fast. Click `promote` on anything sharp — it bounces to premise review.
4. **Premise Review page**: every sketch has 1–3 model variants side by side. Use `j`/`k` to move through sketches and `a` to approve the first good variant (or click a specific premise). The leaderboard widget in the top nav shows which model is currently winning approvals. Click `insights` next to it for the top approved loglines from the last 30 days.
5. **Storyboard Review**: check each sketch's beat grid for obvious artifacts (face morphs, wrong location). Use the per-frame `regen this frame` button for anything off. `a` approves the whole storyboard.
6. **Critic Review**: watch the embedded final cut. The structured panel below the video shows the `is_funny` verdict, per-axis scores, issues, and fix suggestions. If the critic flagged something fixable, hit `send back for regen` to bounce the sketch back to video pending. Otherwise `p` publishes.
7. **Published page** lists every sketch that made it out, with per-destination results (`local_archive` is always there, plus `youtube_shorts` when the YouTube env vars are set).

The UI auto-refreshes on state transitions thanks to the SSE stream — you don't need to reload between clicks. If the SSE connection drops, the page falls back to refreshing on every action.

---

## 2. Running the radar manually

### From your laptop (one-shot)

```bash
cd other_projects/ai_vids_virality
source .venv/bin/activate
python -m pipelines.run_skeleton
```

This walks the whole pipeline for any signals that aren't already consumed:

1. Runs every enabled collector in `config/sources.yaml`.
2. Runs the keyword scorer against any new signal markdown files.
3. Promotes high-scoring signals to the idea-factory queue.
4. Runs the multi-model factory to generate premises.

### From the Hetzner cron (production)

The cron-ready wrapper is `pipelines/run-radar.sh`. It activates the venv, runs the pipeline, and writes a dated log to `logs/radar-YYYY-MM-DD.log`. Failures exit non-zero so cron / Telegram notification hooks can pick them up.

```bash
bash pipelines/run-radar.sh
tail -f logs/radar-$(date +%Y-%m-%d).log
```

### Offline mode (for testing changes without burning tokens)

Set any of these env vars before running the backend or pipeline:

```bash
AI_VIDS_OFFLINE_STORYBOARD=1    # force stub storyboard adapter + null LLM for beats
AI_VIDS_OFFLINE_VIDEO=1         # force stub video adapter
AI_VIDS_OFFLINE_CRITIC=1        # force stub critic (always passes, hardcoded report)
AI_VIDS_OFFLINE_PUBLISH=1       # force local_archive-only publish (no YouTube)
```

All four are respected by the backend endpoints the UI calls; none of them change the radar layer (which is already network-by-design).

---

## 3. Environment variables (every API key)

All keys are optional. Every adapter gracefully falls back to a stub or placeholder when its key isn't set. The full list:

| Variable | Used by | What it unlocks | Where to get it |
|---|---|---|---|
| `OPENAI_API_KEY` | `idea_factory/adapters/openai_stub.py` | Real GPT-5 premise generation instead of the deterministic OpenAI stub | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `GEMINI_API_KEY` | `idea_factory/adapters/gemini_stub.py`, `storyboard/adapters/gemini_image.py`, `critic/adapters/gemini_video.py` | Real Gemini 2.5 Pro premises, nano-banana-2 images, and Gemini 2.5 Pro video critic | [aistudio.google.com](https://aistudio.google.com) → "Get API key" |
| `KLING_AK` + `KLING_SK` | `video_gen/adapters/kling.py` | Real Kling 1.6 video generation (the priority provider for Phase 5) | [app.klingai.com](https://app.klingai.com) → developer console → AccessKey/SecretKey pair |
| `LUMA_API_KEY` | `video_gen/adapters/luma.py` | Real Luma Dream Machine Ray 2 with start+end frame interpolation | [lumalabs.ai](https://lumalabs.ai) → API access |
| `RUNWAY_API_KEY` | `video_gen/adapters/runway.py` | Real Runway gen4_turbo image-to-video | [dev.runwayml.com](https://dev.runwayml.com) |
| `FAL_KEY` (or `PIKA_API_KEY`) | `video_gen/adapters/pika.py` | Real Pika 2.2 via fal.ai (Pika's official public API lives on fal.ai in 2026) | [fal.ai/dashboard](https://fal.ai/dashboard) |
| `GOOGLE_VERTEX_KEY` or `GOOGLE_APPLICATION_CREDENTIALS` | `video_gen/adapters/veo.py` | Veo 3 (partial — adapter is a TODO placeholder, see phase-5-report.md) | Google Cloud service account |
| `GOOGLE_CLOUD_PROJECT` | `video_gen/adapters/veo.py` | GCP project id for Veo | GCP console |
| `YT_REFRESH_TOKEN` + `YT_CLIENT_ID` + `YT_CLIENT_SECRET` | `publishing/adapters/youtube_shorts.py` | Real YouTube Shorts upload as category-23 (Comedy), default `private`, `#shorts` in description | 1. Create an OAuth client at [console.cloud.google.com](https://console.cloud.google.com) → APIs → Credentials → OAuth client ID (type "Desktop"). 2. Enable YouTube Data API v3. 3. Use the OAuth playground with scope `https://www.googleapis.com/auth/youtube.upload` to mint a refresh token. |

**Shell-wise**, the recommended place to stash these on the Hetzner box is `/etc/ai-vids-virality.env` with `chmod 600`, then `EnvironmentFile=/etc/ai-vids-virality.env` in the systemd unit (or `source` it from the cron wrapper).

### Test-only toggles

| Variable | Effect |
|---|---|
| `AI_VIDS_DATA_ROOT` | Point the backend at a different data root (tests set this to `tmp_path`) |
| `AI_VIDS_OFFLINE_STORYBOARD` | Force stub model + stub storyboard adapter from the backend |
| `AI_VIDS_OFFLINE_VIDEO` | Force stub video adapter from the backend |
| `AI_VIDS_OFFLINE_CRITIC` | Force stub critic from the backend |
| `AI_VIDS_OFFLINE_PUBLISH` | Force local_archive-only publishing |

---

## 4. Deploying to the Hetzner box

The Hetzner box is documented in `eywa/super-eywa/sticky-notes/daily-journals/2026-04-03/remote-dev-box-plan.md` — read that first if you're standing it up fresh. This section assumes the box exists, has a working venv with all requirements, and the `claude` CLI is already authenticated.

### 4.1 First-time setup

```bash
# On the Hetzner box
cd ~/kingdom_of_god/home-base
git clone ... ai_vids_virality  # (if not already part of the monorepo)
cd other_projects/ai_vids_virality

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Generate placeholder assets
python -c "from PIL import Image; Image.new('RGB',(512,512),'#444').save('storyboard/placeholder.png')"
ffmpeg -f lavfi -i color=c=black:s=320x240:d=2 -y video_gen/placeholder.mp4

# Drop env vars in /etc/ai-vids-virality.env (or similar)
sudo install -m 600 /dev/null /etc/ai-vids-virality.env
sudo ${EDITOR} /etc/ai-vids-virality.env
# Paste the GEMINI_API_KEY / KLING_* / YT_* / etc. as KEY=VALUE lines.

# Smoke test
source /etc/ai-vids-virality.env
bash pipelines/run-radar.sh
tail -20 logs/radar-$(date +%Y-%m-%d).log
```

### 4.2 Cron wrapper

Add this to the Hetzner crontab (every 30 minutes during waking hours PT):

```cron
*/30 13-06 * * * cd ~/kingdom_of_god/home-base/other_projects/ai_vids_virality && source /etc/ai-vids-virality.env && bash pipelines/run-radar.sh >> /var/log/ai-vids/cron.log 2>&1
```

The wrapper already writes its own detailed log into `logs/radar-YYYY-MM-DD.log` inside the project — the `>>` redirect is just a belt-and-suspenders trail for cron itself.

### 4.3 Web UI on the box (behind Tailscale or Cloudflare Access)

Run `uvicorn` under `systemd` so it comes back after a reboot. Example unit file at `/etc/systemd/system/ai-vids-virality.service`:

```ini
[Unit]
Description=ai_vids_virality web UI
After=network.target

[Service]
Type=simple
User=seanross
WorkingDirectory=/home/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality
EnvironmentFile=/etc/ai-vids-virality.env
ExecStart=/home/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality/.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ai-vids-virality
sudo systemctl status ai-vids-virality
journalctl -u ai-vids-virality -f
```

Front it with Tailscale (`tailscale up` + MagicDNS) or a Cloudflare tunnel; the app has no auth layer of its own, so the access gate is the network.

### 4.4 Telegram failure notifications

The radar-radar wrapper already writes to `logs/` and exits non-zero on failure. Wire the existing `~/scripts/notify-failure.sh` hook (from the remote-dev-box-plan) into the cron line:

```cron
*/30 13-06 * * * cd ~/.../ai_vids_virality && source /etc/ai-vids-virality.env && (bash pipelines/run-radar.sh || ~/scripts/notify-failure.sh "ai-vids-virality radar failed")
```

---

## 5. Adding a new collector

Collectors live at `collectors/<source>/fetch.py`. Each exposes a single function:

```python
def fetch(store: Store, config: Optional[Dict[str, Any]] = None) -> List[str]: ...
```

Returns the list of signal IDs newly written. The function must be **idempotent** (second call with no new upstream data returns `[]`) and **dedupe via `.seen-ids`**. Use `collectors/_common.py::render_signal_markdown` + `write_signal_file` to keep the YAML frontmatter shape consistent across collectors.

### Steps

1. Create `collectors/<new_source>/__init__.py` and `collectors/<new_source>/fetch.py`.
2. Implement `fetch(store, config)` following the pattern in `collectors/hacker_news/fetch.py` (the simplest real collector).
3. Add an entry to `config/sources.yaml`:
   ```yaml
   - id: your_source
     enabled: true
     module: collectors.your_source.fetch
     config: { ... }
   ```
4. Add a test file at `tests/test_your_source_collector.py` with a fixture JSON/XML/NDJSON in `tests/fixtures/` and mocked HTTP calls. The test must cover: first-run-creates-N-files, dedupe-returns-zero, max-age filter, error path.
5. Run `pytest tests/test_your_source_collector.py` until green.

No changes to the pipeline or UI required — `pipelines/run_skeleton.py` picks up new entries from `config/sources.yaml` dynamically.

---

## 6. Adding a new model adapter (idea factory)

Model adapters live at `idea_factory/adapters/<model>.py` and implement `idea_factory.adapter.ModelAdapter`. The contract is two methods: `is_available()` and `generate(signal, prompt, n_premises)`. Adapters must never raise — on failure they return a `PremiseResult` with `error` set and empty `premises`.

### Steps

1. Copy `idea_factory/adapters/openai_stub.py` as a template — it has both the real-API path and the deterministic stub fallback in one file.
2. Implement `generate()` using `httpx` for the real call. Parse the model's response with `idea_factory.adapters._json_parsing.extract_first_json_object` (handles markdown fences defensively) + `find_premise_list`.
3. Add an entry to `config/models.yaml`:
   ```yaml
   - id: your-model
     enabled: true
     adapter: idea_factory.adapters.your_model.YourAdapter
     config: { api_model: your-model, timeout_sec: 120 }
   ```
4. Add tests to `tests/test_model_adapters.py`:
   - `is_available()` is False without the env var
   - Happy path with mocked httpx returns the parsed premises
   - Malformed inner JSON → `error` set, `premises=[]`
   - Stub fallback returns three deterministic premises when the env var is missing
5. (Optional) Add an opt-in `@pytest.mark.llm` integration test that spends real tokens.

The factory (`idea_factory/factory.py`) iterates over every enabled entry in `models.yaml`, so your new adapter is picked up automatically.

---

## 7. Adding a new storyboard adapter

Same pattern as above, one layer down. Adapter class lives at `storyboard/adapters/<name>.py` and implements `storyboard.adapter.StoryboardAdapter`, which has `is_available()`, `generate_character_ref()`, and `generate_frame()`. On failure the adapter MUST copy the placeholder PNG to `out_path` so downstream stages always have a file — use `storyboard._common.copy_placeholder`.

Config lives at `config/storyboard.yaml`. The pipeline picks the first adapter whose `is_available()` is True.

---

## 8. Adding a new video provider

Video adapters live at `video_gen/adapters/<provider>.py` and implement `video_gen.adapter.VideoProviderAdapter` with three methods: `is_available()`, `estimated_cost_cents(duration_sec)`, and `generate(start_frame, end_frame, prompt, duration_sec, out_path, beat_n)`.

Critical rules:

1. **Do not invent endpoints or parameters.** Verify the provider's public docs before writing the request body. If anything can't be confirmed, leave the adapter as a partial with a module-level `# TODO` comment and ship it (see `video_gen/adapters/veo.py` for the template).
2. **Adapters never raise from `generate()`.** On any failure path return `VideoClip(error=...)` and copy the placeholder MP4 to `out_path` via `video_gen._common.copy_placeholder`.
3. **Report cost in integer cents.** The pipeline's cost-cap check depends on it.

### Steps

1. Copy `video_gen/adapters/kling.py` as a template — it has the full submit / poll / download cycle with HTTP error handling.
2. Add the adapter to `config/video.yaml` in both `adapters:` and `routing.default:`. Order matters — put cheaper providers earlier if you want cost-first routing.
3. Add mocked-HTTP tests to `tests/test_video_adapters.py` covering: unavailable without env, happy path submit/poll/download, HTTP failure fallback, missing clip, malformed response.
4. Run `pytest tests/test_video_adapters.py`.

---

## 9. Adding a new critic adapter

Critic adapters live at `critic/adapters/<name>.py` and implement `critic.adapter.CriticAdapter`:

```python
def check_shot(self, clip_path, expected_frame, character_refs, beat_metadata) -> ShotReport: ...
def critique_sketch(self, final_cut_path, sketch_metadata) -> SketchCritique: ...
```

**Critical invariant**: on infrastructure errors, `check_shot()` must return `passed=True` so the video pipeline's retry loop doesn't loop forever on our problems. `critique_sketch()` returns with `error` set.

Config at `config/critic.yaml`. Add mocked-HTTP tests to `tests/test_critic_adapters.py`.

---

## 10. Adding a new publisher

Publishers live at `publishing/adapters/<name>.py` and implement `publishing.adapter.Publisher`:

```python
def publish(self, sketch: Sketch, store: Store) -> PublishResult: ...
def is_available(self) -> bool: ...
```

Template: `publishing/adapters/youtube_shorts.py` (the most complete real adapter). Returns a `PublishResult` with `success: bool`, `url: Optional[str]`, `error: Optional[str]`, and an `extra: dict` for any provider-specific metadata.

### Steps

1. Copy the YouTube adapter as a template.
2. Handle the auth flow (refresh token, bearer header, whatever the provider uses). Use `httpx` directly — we avoid the heavy Google/Twitter SDKs on principle.
3. Add to `config/publishing.yaml` in the `destinations:` list.
4. Add tests to `tests/test_publishers.py` covering: unavailable without env, missing final.mp4, happy path with mocked httpx, failure paths.
5. Add an opt-in `@pytest.mark.publish` integration test.

The `POST /api/sketch/{id}/publish` endpoint runs every enabled destination sequentially and transitions the sketch to PUBLISHED if **at least one** succeeded. If every destination fails, the endpoint returns 502 and the sketch stays in CRITIC_REVIEW.

---

## 11. Where logs live

| Where | What |
|---|---|
| `logs/radar-YYYY-MM-DD.log` | Cron-wrapper output from `pipelines/run-radar.sh` — one file per day |
| `journalctl -u ai-vids-virality` | Web UI stdout/stderr when running under systemd on the Hetzner box |
| `/var/log/ai-vids/cron.log` | Cron's own log of the wrapper invocation (optional, belt-and-suspenders) |
| `data/sketches/{id}/clips.json` | Per-beat video generation metadata with `shot_reports` trail (Phase 6 retries) |
| `data/sketches/{id}/critic.json` | Full-sketch critique JSON from the Phase 6 critic |
| `data/sketches/{id}/storyboard.json` | Beat sheet + character ref metadata from Phase 4 |
| `data/published/{id}/published_at.txt` | Local archive publish timestamp |
| `data/leaderboard.json` | Per-model approval counts (Phase 3) |

For live debugging:

```bash
tail -F logs/radar-$(date +%Y-%m-%d).log
journalctl -u ai-vids-virality -f
uvicorn backend.main:app --reload --log-level debug
```

---

## 12. Backing up data

Everything that matters lives under `data/`. It's just JSON + PNG + MP4, no database.

### Daily automatic backup

The existing `radar-commit.sh` pattern from the research-radar project is the right template. Example:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd ~/kingdom_of_god/home-base/other_projects/ai_vids_virality

git add data/signals/ data/queues/ data/sketches/ data/published/ data/leaderboard.json
if ! git diff --cached --quiet; then
  git commit -m "ai-vids data snapshot $(date -Iseconds)" --quiet
  git push origin main --quiet
fi
```

Schedule it 15 minutes after the radar cron so you capture the day's signals, sketches, and published archive into git.

### Manual one-shot backup

```bash
tar -czf ~/backup-ai-vids-$(date +%Y-%m-%d).tar.gz -C ~/kingdom_of_god/home-base/other_projects/ai_vids_virality data
scp ~/backup-ai-vids-$(date +%Y-%m-%d).tar.gz backup-host:ai-vids/
```

### What to NOT back up

- `data/signals/*/items/*.md` — large-ish, regeneratable from the collectors. Backing up `.seen-ids` alone is enough to preserve dedupe state.
- `data/sketches/*/storyboard/*.png`, `clips/*.mp4`, `refs/*.png` — expensive to regenerate but not strictly necessary; skip them on tight backup budgets and rely on `data/published/` which has the final cut.

---

## 13. pytest marker cheat sheet

Every test is tagged so the default run never touches the network or burns tokens.

| Marker | Opt-in command | What it runs | Cost |
|---|---|---|---|
| (default) | `pytest -m "not network and not llm and not gemini and not video and not critic and not publish"` | All offline unit + mock tests | free |
| `network` | `pytest -m network -v` | Real Hacker News Firebase API hit | free |
| `llm` | `pytest -m llm -v` | Real Claude CLI call with a tiny prompt | ~$0.01 |
| `gemini` | `pytest -m gemini -v` | Real nano-banana-2 image generation — skipped without `GEMINI_API_KEY` | ~$0.05 |
| `video` | `pytest -m video -v` | Reserved for real video provider integration tests (no tests ship — marker only exists so future opt-in tests don't need a pytest.ini update) | varies |
| `critic` | `pytest -m critic -v` | Reserved for real critic API integration tests (none ship) | varies |
| `publish` | `pytest -m publish -v` | Real YouTube Shorts upload — skipped without `YT_REFRESH_TOKEN`/`YT_CLIENT_ID`/`YT_CLIENT_SECRET` | quota-only |

The total offline suite should run in under ~3 seconds. If a single test suddenly takes 10+ seconds, it probably snuck into a real network / CLI call — check for a missing `monkeypatch.setenv("AI_VIDS_OFFLINE_*", "1")` in the fixture.

---

## 14. Troubleshooting

### "pytest hangs for 2 minutes on one test"

Almost always an `AI_VIDS_OFFLINE_*` env var missing from a test fixture, causing the backend to shell out to the real Claude CLI or hit the real Gemini API. Check the fixture for the test file in question — it should set every offline env var that applies.

### "the backend returns 500 on approve_storyboard"

The video pipeline probably couldn't find storyboard frames on disk. Check `data/sketches/{id}/storyboard/` — if it's empty, the storyboard pipeline never ran (likely because `approve_premise` skipped the beat-sheet step when no LLM was available). Run `approve_premise` again with a different `model_id` variant.

### "nothing happens when I click publish"

Open the browser devtools network tab. If the `POST /api/sketch/{id}/publish` returns 502, every enabled destination failed. Check the response body — it contains the `results` array with per-destination errors.

### "the cost widget shows $0.00 even though I've been clicking for an hour"

The cost widget reads from `data/sketches/{id}/storyboard.json`, `clips.json`, and `critic.json` — it only sees adapters that reported non-zero `cost_cents`. Stub adapters report 0, which is correct. When you wire real Gemini + Kling + Gemini-critic keys, the widget will light up.

### "SSE keeps reconnecting every 3 seconds"

The frontend reconnects on `onerror`. Check `journalctl -u ai-vids-virality` — the uvicorn process may be dying on a streaming-response bug. If the backend logs look fine, confirm no proxy is buffering the `text/event-stream` response (nginx needs `proxy_buffering off;` for SSE).

### "yt-dlp keeps failing with 'trending playlist not found'"

YouTube has been quietly disabling `/feed/trending`. The collector falls back to the official "Popular Right Now" auto-playlist (`PLrEnWoR732-BHrPp_Pm8_VleD68f9s14-`), which should still work. If both fail, bump yt-dlp to a fresh release (`pip install --upgrade yt-dlp`) and check their issue tracker.

### "Kling returns 1001 'Authorization header empty'"

The JWT minted by `video_gen/adapters/kling.py::make_jwt` is rejected. Double-check `KLING_AK` and `KLING_SK` — they must be the raw AK/SK strings from the Kling dev console, not the base64-encoded versions some dashboards export.

### "the UI loads but the nav is empty"

Open devtools → Console. Usually an uncaught exception in `renderNav()` after a config change. Clear the state with `localStorage.clear()` and reload — the app doesn't use localStorage, but browser caching of the old `index.html` sometimes does.

### "publish succeeded locally but YouTube says 'video not found'"

YouTube defaults to `private` in `config/publishing.yaml`. You won't see it in public search. Open the YouTube Studio directly and filter by "private" to find it. Flip `default_privacy: unlisted` or `public` in the yaml if you want different behavior.

---

## 15. Cost control

The hard cap is in `config/video.yaml`:

```yaml
budget:
  max_cost_cents_per_sketch: 500    # $5 hard cap per sketch
```

The video pipeline checks the running cost BEFORE each clip generation and stops early if the next estimated clip would exceed the cap. It still stitches whatever clips were generated so the sketch can still reach the critic. The UI shows a red "cost cap reached at beat N" banner on the Critic Review page when this fires.

To stop a sketch from costing real money entirely, set `AI_VIDS_OFFLINE_VIDEO=1` (or disable every real video provider in `video.yaml` and leave only `stub` enabled).

The cost dashboard widget in the top nav shows today's total at a glance. Click for a per-stage / per-provider breakdown. The data is computed on every request from `data/sketches/{id}/clips.json`, `storyboard.json`, and `critic.json` — no pre-aggregation.

---

## 16. File system layout reference

```
ai_vids_virality/
  config/
    comedy-lens.md          # comedy scoring rubric + boost/penalty keywords
    sources.yaml            # which collectors to run
    thresholds.yaml         # promotion + freshness knobs
    models.yaml             # Phase 3 model roster
    storyboard.yaml         # Phase 4 storyboard adapter roster + style guide
    video.yaml              # Phase 5 video provider roster + cost cap
    critic.yaml             # Phase 6 critic adapter roster + shot_check.max_retries
    publishing.yaml         # Phase 7 publishing destinations
  data/                     # all runtime state, JSON on disk, no database
    signals/{source}/items/ # radar output, markdown with YAML frontmatter
    queues/                 # idea-factory / premise-review / storyboard-review / etc.
    sketches/{id}/
      sketch.json           # canonical sketch state
      beats.json            # (removed — beats live inside sketch.json now)
      storyboard.json       # Phase 4 output
      refs/                 # character reference PNGs
      storyboard/           # per-beat start-frame PNGs
      clips.json            # Phase 5 output (incl. shot_reports from Phase 6 retries)
      clips/                # per-beat MP4 clips
      final.mp4             # the stitched final cut
      critic.json           # Phase 6 output
    published/{id}/         # Phase 7 archive: final.mp4 + sketch.json + critic.json + published_at.txt
    leaderboard.json        # Phase 3 per-model approval counts
    rejected-signals.json   # Phase 2/7 user-rejected signal ids
  collectors/
    _common.py              # shared signal markdown helpers
    reddit/                 # Phase 2 real collector (reddit.com public JSON)
    hacker_news/            # Phase 2 (Firebase topstories)
    google_news/            # Phase 2 (RSS via feedparser)
    youtube_trending/       # Phase 2 (yt-dlp subprocess)
    reddit_stub/            # Phase 1 deterministic stub, still used by tests
  analyzers/
    score_signals/
      analyze.py            # analyzer loop over every source
      lens_rules.py         # lens-driven keyword scorer
      prompt.md             # (unused, placeholder for a future LLM analyzer)
  idea_factory/
    adapter.py              # ModelAdapter ABC + PremiseResult dataclass
    adapters/
      claude_cli.py         # Phase 3 real Claude via subprocess
      openai_stub.py        # Phase 3 real OpenAI or deterministic stub
      gemini_stub.py        # Phase 3 real Gemini or deterministic stub
      _json_parsing.py      # shared helpers for parsing LLM JSON output
    factory.py              # multi-model orchestrator
    prompts/
      premise_generation.md # the Phase 3 prompt template
  storyboard/
    adapter.py              # StoryboardAdapter ABC
    adapters/
      gemini_image.py       # Phase 4 real nano-banana-2
      stub_storyboard.py    # Phase 1/4 placeholder
    beats.py                # LLM call for the beat sheet
    pipeline.py             # run_storyboard + regenerate_frame
    prompts/
      beat_sheet.md
      character_ref.md
      frame.md
    placeholder.png         # fallback asset (1879 bytes)
  video_gen/
    adapter.py              # VideoProviderAdapter ABC + VideoClip dataclass
    adapters/
      kling.py              # Phase 5 real (complete)
      luma.py               # Phase 5 real (complete, needs image_url_resolver)
      runway.py             # Phase 5 real (complete)
      pika.py               # Phase 5 real (via fal.ai)
      veo.py                # Phase 5 partial (OAuth TODO)
      stub_video.py         # Phase 5 always-available fallback
    pipeline.py             # run_video_pipeline with shot-check retry loop (Phase 6)
    stitch.py               # ffmpeg concat-demuxer wrapper with re-encode fallback
    prompts/
      clip_prompt.md
    placeholder.mp4         # fallback asset (~3KB)
  critic/
    adapter.py              # CriticAdapter ABC + ShotReport + SketchCritique
    adapters/
      gemini_video.py       # Phase 6 real Gemini 2.5 Pro with video input
      claude_frame.py       # Phase 6 real Claude CLI with sampled frame metadata
      stub_critic.py        # Phase 6 deterministic hardcoded report
    pipeline.py             # select_critic_adapter + run_full_critique
    frame_sampler.py        # ffmpeg frame sampling + optional whisper hook
    prompts/
      shot_check.md
      full_sketch.md
  publishing/
    adapter.py              # Publisher ABC + PublishResult dataclass
    adapters/
      local_archive.py      # Phase 7 always-works archive
      youtube_shorts.py     # Phase 7 real YouTube Data API v3 resumable upload
      stub_publisher.py     # Phase 7 no-op for TikTok/X placeholders
    pipeline.py              # run_publishers
  state/
    machine.py              # Status enum + VALID_TRANSITIONS + InvalidTransition
    store.py                # file-based Store + Sketch dataclass
    leaderboard.py          # Phase 3 per-model approval counts
  pipelines/
    run_skeleton.py         # top-level orchestrator (collector -> analyzer -> factory)
    run-radar.sh            # cron-ready bash wrapper
  backend/
    main.py                 # FastAPI app, all route handlers
    events.py               # Phase 7 SSE pub/sub
    stats.py                # Phase 7 cost + insights aggregators
    static/
      index.html            # single-file multi-page UI (vanilla JS)
  tests/                    # ~270 offline tests + marker-gated integration tests
  logs/
    radar-YYYY-MM-DD.log    # daily cron output
  phases/
    phase-1-plan.md
    phase-1-report.md
    ...
    phase-7-report.md
  README.md
  RUNBOOK.md                # this file
  requirements.txt
  pytest.ini
```

If you're ever lost, start at `backend/main.py` — it has the full API surface in ~1,000 lines and imports from every other module, so following the imports is a fast way to reconstruct the mental model.
