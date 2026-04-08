# Phase 2 — Real Radar

## Goal

Replace the stub Reddit collector with **real collectors** that pull actual viral/trending content from sources that require **no API keys and no money**, using only public endpoints. The Signals page in the UI starts showing real content from the outside world.

**Still no LLMs in this phase** (that's Phase 3). The analyzer stays rule-based but gets slightly smarter — it reads a real `comedy-lens.md` and does keyword-based scoring. The important thing is that Phase 2 proves we can ingest the real world into the pipeline we built in Phase 1.

---

## Acceptance criteria — must all be true at the end

1. Running `python -m pipelines.run_skeleton` (or a new `run_radar.py` — see below) calls **four real collectors** in sequence:
   - Reddit public JSON (no auth)
   - Hacker News public Firebase API (no auth)
   - Google News RSS (no auth)
   - YouTube trending via yt-dlp (no API key)
   And all four write signal files to `data/signals/{source}/items/`.

2. Running the pipeline twice does not duplicate signals (dedupe via `.seen-ids` still works).

3. The analyzer reads the new `config/comedy-lens.md` and the new `config/thresholds.yaml`, and promotes signals to the idea-factory queue based on a **rule-based keyword scorer** (no LLM). The stub idea factory then picks them up and creates sketches as before.

4. The Signals page in the web UI now shows the real collected signals, grouped by source, sorted by score descending, with a "promote to factory" button on signals that were NOT auto-promoted (so the user can manually bump a low-scored signal).

5. There's a `pipelines/run-radar.sh` bash script — **cron-ready** — that activates the venv, runs the full pipeline, logs to `logs/radar-YYYY-MM-DD.log`, and exits non-zero on failure. This is the script that will eventually run on the Hetzner box. Don't actually add it to cron — just make it runnable.

6. All new collectors have unit tests that **mock the HTTP layer** so tests don't hit the network. Test markers `@pytest.mark.network` gate any actual-network test (there's one, as an integration test, that can be skipped via `pytest -m "not network"`).

7. `pytest -m "not network"` is green. Total test count should grow from 43 to ~60+ (at least 4 new collector tests, plus tests for the real analyzer, plus signals-page API tests).

8. The Phase 1 stub Reddit collector (`collectors/reddit_stub/`) **stays** — it becomes a test fixture and is no longer run by default. Mark it clearly as a fixture in its module docstring.

---

## New directory additions

```
ai_vids_virality/
  config/
    comedy-lens.md            # EXPANDED — real rubric (2-3 paragraphs)
    sources.yaml              # EXPANDED — enables the 4 real collectors
    thresholds.yaml           # EXPANDED — promotion score + freshness windows
  collectors/
    reddit/                   # NEW
      __init__.py
      fetch.py
    hacker_news/              # NEW
      __init__.py
      fetch.py
    google_news/              # NEW
      __init__.py
      fetch.py
    youtube_trending/         # NEW
      __init__.py
      fetch.py
    reddit_stub/              # UNCHANGED, becomes test fixture
  analyzers/
    score_signals/
      analyze.py              # UPDATED — reads lens, does keyword scoring
      lens_rules.py           # NEW — rule-based scoring engine
  pipelines/
    run_skeleton.py           # UPDATED — now runs all enabled collectors from sources.yaml
    run_radar.sh              # NEW — bash wrapper for cron
  backend/
    main.py                   # UPDATED — new /api/signals endpoint, /api/signals/{id}/promote endpoint
    static/
      index.html              # UPDATED — Signals page shows real signal data
  logs/
    .gitkeep                  # log dir for cron output
  tests/
    test_reddit_collector.py  # NEW
    test_hn_collector.py      # NEW
    test_google_news_collector.py  # NEW
    test_youtube_trending_collector.py  # NEW (mocks subprocess)
    test_lens_rules.py        # NEW
    test_signals_api.py       # NEW
    fixtures/                 # NEW
      reddit_popular_sample.json
      hn_topstories_sample.json
      google_news_sample.xml
      yt_dlp_sample.json
```

---

## Component specs

### `config/comedy-lens.md`

Real rubric, 2-3 paragraphs. Cover:
- What makes a story sketchable (absurdity, relatable frustration, clear characters, visual comedy, topical punch)
- What kills sketchability (too niche, already a meme everyone's done, legally dangerous, tragic without a comedy angle)
- Tonal preferences (we like dry workplace, absurdist, satire — avoid mean-spirited, low-hanging-fruit political hate)

This file is **read by the rule-based scorer to extract its keyword list** in Phase 2, and **passed to the LLM as context** in Phase 3. Write it once, it serves both phases.

### `config/sources.yaml`

```yaml
collectors:
  - id: reddit
    enabled: true
    module: collectors.reddit.fetch
    config:
      subreddits: [popular, news, nottheonion, politics, funny]
      limit_per_sub: 25
      max_age_hours: 24
  - id: hacker_news
    enabled: true
    module: collectors.hacker_news.fetch
    config:
      limit: 30
      max_age_hours: 24
  - id: google_news
    enabled: true
    module: collectors.google_news.fetch
    config:
      feeds:
        - "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"                        # top stories
        - "https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=en-US&gl=US&ceid=US:en"
        - "https://news.google.com/rss/headlines/section/topic/NATION?hl=en-US&gl=US&ceid=US:en"
      limit_per_feed: 20
  - id: youtube_trending
    enabled: true
    module: collectors.youtube_trending.fetch
    config:
      limit: 20
  - id: reddit_stub
    enabled: false               # kept as fixture only
    module: collectors.reddit_stub.fetch
```

### `config/thresholds.yaml`

```yaml
scoring:
  promote_to_factory: 7           # min sketchability score
  signal_freshness_max_hours: 48  # drop signals older than this
  max_signals_per_run: 100        # safety cap across all collectors
```

### `collectors/reddit/fetch.py`

- Hit `https://www.reddit.com/r/{sub}.json?limit={limit}` with a custom `User-Agent` header (Reddit requires one; use `ai-vids-virality/0.1`)
- For each post, build a signal record with: `id` = `reddit-{post.id}`, source URL, title, selftext (truncated), subreddit, ups, num_comments, created_utc
- Write markdown files with YAML frontmatter to `data/signals/reddit/items/{id}.md`
- Dedupe via `.seen-ids`
- Idempotent

### `collectors/hacker_news/fetch.py`

- Hit `https://hacker-news.firebaseio.com/v0/topstories.json`
- For each ID in the first `limit`, hit `https://hacker-news.firebaseio.com/v0/item/{id}.json`
- Build signal records, write files, dedupe

### `collectors/google_news/fetch.py`

- Parse each feed URL via `feedparser` (add to requirements)
- For each entry, build a signal record (title, summary, link, published)
- Skip entries older than `max_age_hours`
- Write files, dedupe

### `collectors/youtube_trending/fetch.py`

- Run `yt-dlp --flat-playlist --dump-json "https://www.youtube.com/feed/trending"` as a subprocess
- Parse each JSON line for `id`, `title`, `uploader`, `view_count`, `duration`
- Write files, dedupe
- If `yt-dlp` is not on `$PATH`, log a warning and return 0 signals (don't crash the pipeline — the other collectors should still run)

### `analyzers/score_signals/lens_rules.py`

A small keyword-based scorer. Read `config/comedy-lens.md`, extract keywords (a simple approach: find lines starting with `- ` in a "Keywords that boost" section and a "Keywords that penalize" section). Then scoring is:

```python
def score(signal_title: str, signal_body: str, lens: Lens) -> int:
    text = (signal_title + " " + signal_body).lower()
    score = 5  # baseline
    for kw in lens.boost_keywords:
        if kw in text:
            score += 1
    for kw in lens.penalty_keywords:
        if kw in text:
            score -= 2
    # Length heuristics
    if 20 <= len(signal_title) <= 120:
        score += 1
    if "died" in text or "killed" in text:
        score -= 3  # tragedy is not sketch material by default
    return max(1, min(10, score))
```

Keep it simple — it's getting replaced in Phase 3.

The comedy-lens.md should include sections:
```markdown
## Keywords that boost sketchability
- caught
- absurd
- announces
- ban
- senator
- ceo
- scandal
- ...

## Keywords that penalize
- dies
- killed
- shooting
- ...
```

The scorer imports those from the markdown file.

### `analyzers/score_signals/analyze.py` (updated)

Instead of the Phase 1 `len(title) % 10 + 5`, call `lens_rules.score(...)` for each unanalyzed signal. Everything else (promoting to queue, writing summary file) stays the same.

### `pipelines/run_skeleton.py` (updated)

Reads `config/sources.yaml`, for each enabled collector, dynamically imports `module` and calls its `fetch(store, config=...)`. Collects new signal IDs across all collectors. Then runs the analyzer + factory as before.

Rename is OK — can stay `run_skeleton.py` for continuity, or rename to `run_pipeline.py` and leave a deprecated shim. I'll leave the call on the subagent — either way, `pipelines/run-radar.sh` calls it.

### `pipelines/run-radar.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate

mkdir -p logs
LOGFILE="logs/radar-$(date +%Y-%m-%d).log"

{
  echo "=== Radar run at $(date -Iseconds) ==="
  python -m pipelines.run_skeleton
  echo "=== OK at $(date -Iseconds) ==="
} >> "$LOGFILE" 2>&1
```

Make it executable (`chmod +x`).

### `backend/main.py` (updated)

New endpoints:

- `GET /api/signals` — returns signals from `data/signals/` across all sources, from the last 24h, sorted by score desc. Shape:
  ```json
  {
    "signals": [
      {
        "id": "...",
        "source": "reddit",
        "title": "...",
        "url": "...",
        "score": 7,
        "promoted": true,
        "captured_at": "..."
      },
      ...
    ]
  }
  ```
- `POST /api/signals/{signal_id}/promote` — force-promote a signal to the idea-factory queue (even if its score is below threshold). Triggers the stub idea factory to run on it immediately.
- `POST /api/signals/{signal_id}/reject` — mark a signal as "user-rejected" so the UI can hide it (add a `rejected_signal_ids` set stored at `data/rejected-signals.json`).

### `backend/static/index.html` (updated)

The **Signals** page is the only page that changes. Now it shows a feed of real signals:

- Grouped by source (tabs or sections: Reddit / Hacker News / Google News / YouTube)
- Each signal card: source badge, title (click to open source URL in new tab), score, captured time, action buttons: **promote** (if not already promoted), **reject**, **view source** (opens URL)
- Promoted signals are visually distinguished (e.g. border color)
- Empty state if no signals
- Count badge in the top nav reflects non-rejected signals from the last 24h

All other pages stay the same.

### Tests

Each new collector gets a test that uses a fixture file from `tests/fixtures/` and monkeypatches the HTTP client (use `pytest-httpx` or just `unittest.mock.patch` — either is fine). The test asserts:
- First run creates N signal files
- Second run creates 0 (dedupe)
- Signal file has expected frontmatter keys
- Signals older than `max_age_hours` are skipped

`test_lens_rules.py` — unit-test the scorer with known inputs and expected outputs, including edge cases (empty text, all penalty keywords, all boost keywords).

`test_signals_api.py` — TestClient hits `/api/signals`, `/api/signals/{id}/promote`, `/api/signals/{id}/reject` with a tmp data dir prepopulated with fixture signal files.

### Requirements additions

Add to `requirements.txt`:
```
requests>=2.31
feedparser>=6.0
```

(httpx is already there from Phase 1 for the test client — can reuse for collectors if the subagent prefers.)

---

## Out of scope for Phase 2

- Real LLM in the analyzer (Phase 3)
- Multi-model premise generation (Phase 3)
- Twitter/X, TikTok (both require auth or paid scrapers — later)
- NewsAPI, GDELT (later)
- Actually deploying to Hetzner / adding to cron
- Storyboard / video / critic upgrades (Phases 4–6)

---

## Demo script the subagent must run

```bash
cd /Users/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality
source .venv/bin/activate
pip install -r requirements.txt

# Run offline tests (no network)
pytest -m "not network" -v 2>&1 | tail -20

# Run the real radar pipeline (this WILL hit the network — it's the demo)
python -m pipelines.run_skeleton

# Count signals collected from each source
echo "--- Signal counts by source ---"
for src in reddit hacker_news google_news youtube_trending; do
  count=$(ls data/signals/$src/items/*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "$src: $count"
done

# Start the server and hit the new signals endpoint
uvicorn backend.main:app --port 8767 &
SERVER_PID=$!
sleep 2
curl -s http://localhost:8767/api/signals | python -c "import sys,json; d=json.load(sys.stdin); print(f'Total signals in API response: {len(d[\"signals\"])}'); print('First 3:'); [print(f'  {s[\"source\"]}/{s[\"id\"]} score={s[\"score\"]} title={s[\"title\"][:60]}') for s in d['signals'][:3]]"
kill $SERVER_PID
```

The subagent must include the actual output in the phase 2 report.

---

## Reporting

Write `phases/phase-2-report.md` with:
- File tree of new/changed files
- `pytest -m "not network"` summary
- Output of the demo script (the actual signal counts — showing that real data was ingested)
- Any sources that returned 0 signals (e.g. if yt-dlp is missing) and why
- Any deviations from the plan and why
- One-paragraph note on what the Signals page now looks like

---

## Notes for the executing subagent

- **All test code must avoid network calls by default.** Use fixture files + mocks. One optional network-integration test per collector is fine but must be marked `@pytest.mark.network`.
- The four sources will return different numbers of signals. That's fine. As long as **at least one source returns ≥1 signal** in the demo run, you're good. If all four return zero, investigate — something is broken.
- If yt-dlp isn't installed, `brew install yt-dlp` or `pip install yt-dlp` — try pip first since it works inside the venv and doesn't need sudo.
- Don't break any existing Phase 1 tests. `pytest -m "not network"` should include all 43 Phase 1 tests plus the new ones.
- Don't touch the premise review / storyboard / critic / publish flow. Phase 2 is strictly about the ingestion layer and the Signals page.
- Keep signal file format consistent across collectors (same YAML frontmatter keys) so the analyzer doesn't need source-specific logic.
- Preserve the multi-page top-nav UI design from the recent Phase 1 revision — only the Signals page content changes.
