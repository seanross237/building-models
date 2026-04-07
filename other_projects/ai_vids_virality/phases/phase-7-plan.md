# Phase 7 — Publish + Polish

## Goal

Two things:

1. **Publishing layer** — when a user clicks "Publish," the system actually pushes the final cut somewhere. For Phase 7 we implement **two destinations**: a local "published archive" (always works, no API) and a **YouTube Shorts uploader** (real if `YT_REFRESH_TOKEN` etc. are set, stub otherwise). TikTok and X are stubbed with TODOs for later.

2. **Polish** — the rough edges from earlier phases get cleaned up so the system is genuinely usable for daily review:
   - **Keyboard shortcuts** (J/K to navigate, A to approve, R to reject, E to edit)
   - **SSE refresh** so cards update without manual page reload
   - **Cost dashboard** showing today's spend per stage (LLM / image / video / critic) and per provider
   - **Approval-rate insights** — the leaderboard widget gets a "best premise hooks" view: top-N approved loglines from the last 30 days, broken down by signal source
   - **Bulk reject** on the Signals page so the user can clear out a batch of bad signals fast
   - **Manual idea quick-add** keyboard shortcut from anywhere (`/` to focus, `cmd+enter` to submit)

This is the phase that turns the system from "demoable" into "I'd actually use this every morning."

---

## Acceptance criteria

1. A `Publisher` ABC + three implementations:
   - `LocalArchivePublisher` — always works, copies the final.mp4 + sketch.json + critic.json to `data/published/{sketch_id}/`
   - `YouTubeShortsPublisher` — real upload via YouTube Data API v3 if `YT_REFRESH_TOKEN`/`YT_CLIENT_ID`/`YT_CLIENT_SECRET` are set; stub otherwise
   - `StubPublisher` — fallback no-op that just logs

2. The publish endpoint runs the routed publishers in order. Returns a list of `PublishResult` records (one per destination). The sketch transitions to `PUBLISHED` only if at least one publisher succeeded.

3. Web UI keyboard shortcuts work on Premise Review, Storyboard Review, and Critic Review pages:
   - `J` / `K` — next / previous card
   - `A` — approve current card (uses the first variant on Premise Review)
   - `R` — reject
   - `E` — open edit modal (Premise Review only)
   - `/` — focus the New Idea quick-add
   - `?` — show shortcut help overlay

4. **SSE auto-refresh**: a `GET /api/events` endpoint streams server-sent events (`pipeline_update`) whenever a sketch transitions. The UI listens and re-fetches the current page's data when an event arrives.

5. **Cost dashboard**: a new top-bar widget (next to the leaderboard) shows today's spend grand total + a tooltip breakdown by stage and provider, fed by `GET /api/stats/cost`.

6. **Approval insights**: the leaderboard widget gains a "top approved loglines" expandable section, fed by `GET /api/stats/insights`.

7. **Bulk reject**: the Signals page gains a checkbox per signal + a "reject selected" button.

8. **README + RUNBOOK**: `README.md` updated with the full quick-start. New `RUNBOOK.md` with: how to run the radar manually, how to deploy to the Hetzner box, how to add a new model adapter, how to add a new collector, where logs go, how to back up data, how to set every API key.

9. All previous tests still pass. New tests cover publishers, SSE endpoint (just assert content-type and that one event fires after a transition), cost stats endpoint, insights endpoint, bulk reject endpoint, and the keyboard shortcut DOM wiring (Selenium-free; just assert the JS module exports the expected key map).

10. `pytest -m "not network and not llm and not gemini and not video and not critic and not publish"` is green. New marker `@pytest.mark.publish` for the real YouTube upload integration test (skipped by default).

---

## Component highlights

### `publishing/adapter.py`

```python
@dataclass
class PublishResult:
    destination_id: str
    success: bool
    url: Optional[str]            # public URL if applicable
    error: Optional[str] = None

class Publisher(ABC):
    destination_id: str

    @abstractmethod
    def publish(self, sketch: Sketch, store: Store) -> PublishResult: ...

    @abstractmethod
    def is_available(self) -> bool: ...
```

### `publishing/adapters/youtube_shorts.py`

- Uses the YouTube Data API v3 (`videos.insert`) with resumable upload
- Auth: OAuth2 refresh token stored in env vars (`YT_REFRESH_TOKEN`, `YT_CLIENT_ID`, `YT_CLIENT_SECRET`)
- Sets `snippet.title` from the premise logline, `snippet.description` from synopsis, `snippet.tags`, `status.privacyStatus` (default `private`), and `snippet.categoryId="23"` (Comedy)
- Adds `#shorts` to the description so YouTube treats it as a Short
- Returns the watch URL

### `publishing/adapters/local_archive.py`

Always works. Copies `data/sketches/{id}/final.mp4`, `sketch.json`, `critic.json` into `data/published/{sketch_id}/`. Writes a `published_at.txt` timestamp.

### `config/publishing.yaml`

```yaml
destinations:
  - id: local_archive
    enabled: true
    adapter: publishing.adapters.local_archive.LocalArchivePublisher
    config: {}
  - id: youtube_shorts
    enabled: true
    adapter: publishing.adapters.youtube_shorts.YouTubeShortsPublisher
    config: { default_privacy: private, category_id: "23" }
  - id: tiktok
    enabled: false
    adapter: publishing.adapters.stub_publisher.StubPublisher
    config: {}
  - id: x
    enabled: false
    adapter: publishing.adapters.stub_publisher.StubPublisher
    config: {}
```

### Backend updates

- `POST /api/sketch/{id}/publish` — runs all enabled publishers, returns the list of results, transitions the sketch to PUBLISHED if any succeeded
- `GET /api/events` — SSE stream
- `GET /api/stats/cost` — daily/weekly/monthly cost rollups, broken down by stage and provider
- `GET /api/stats/insights` — top approved loglines, approval rate by source, etc.
- `POST /api/signals/bulk_reject` — body `{"signal_ids": [...]}`

### UI updates

- Top bar additions: cost widget + insights expand on the leaderboard
- Keyboard shortcut module loaded on every page
- SSE listener attached at app boot, re-fetches current page on relevant events
- Bulk reject checkboxes on Signals page
- Help overlay (`?` shortcut) listing all shortcuts

### Tests

- Each publisher's `is_available()` and `publish()` happy path with mocked HTTP
- SSE endpoint returns `text/event-stream`, sends one event after a sketch transition
- Cost stats endpoint returns expected shape with no data → all zeros, with seeded data → correct totals
- Insights endpoint returns expected shape
- Bulk reject endpoint marks all signals as rejected

---

## Demo script

```bash
cd /Users/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality
source .venv/bin/activate

pytest -m "not network and not llm and not gemini and not video and not critic and not publish" -q 2>&1 | tail -5

# Walk a sketch all the way to publish
python -m pipelines.run_skeleton 2>&1 | tail -5

uvicorn backend.main:app --port 8772 &
SERVER_PID=$!
sleep 2

SKETCH_ID=$(ls data/queues/premise-review/ | head -1 | cut -d'.' -f1 | cut -d'_' -f1)
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"model_id":"claude-opus","premise_index":0}' \
  http://localhost:8772/api/sketch/$SKETCH_ID/approve_premise > /dev/null
curl -s -X POST http://localhost:8772/api/sketch/$SKETCH_ID/approve_storyboard > /dev/null
sleep 2
curl -s -X POST http://localhost:8772/api/sketch/$SKETCH_ID/publish | python -m json.tool

# Confirm local archive
ls -la data/published/$SKETCH_ID/

# Cost stats
curl -s http://localhost:8772/api/stats/cost | python -m json.tool

# Insights
curl -s http://localhost:8772/api/stats/insights | python -m json.tool | head -20

kill $SERVER_PID
```

---

## Out of scope for Phase 7

- TikTok / X uploaders (stub only)
- Real Hetzner cron deployment (covered in handoff phase)
- Mobile UI
- User accounts / multi-user

---

## Reporting

`phases/phase-7-report.md` with file tree, test summary, demo output, README + RUNBOOK paths, and a one-paragraph "what changed in the UI" note covering the new shortcuts and widgets.

---

## Notes for the executing subagent

- Keyboard shortcuts: implement in vanilla JS, no library. Listen on `document` with proper input-focus guards (don't trigger when typing in a textarea).
- SSE: FastAPI's `StreamingResponse` with `media_type="text/event-stream"` and a generator that yields `f"event: pipeline_update\\ndata: {json}\\n\\n"`. Use a tiny in-memory pub/sub (set/get on a `defaultdict(asyncio.Queue)` keyed by client id).
- Cost stats: read all sketches, sum the costs from premise generation, storyboard frames, video clips, and critic calls. Group by today/yesterday/this-week. Don't pre-aggregate; the data is small enough.
- The RUNBOOK should be the most useful doc in the project. Pretend you're handing this to a future self who has forgotten everything.
- Don't break tests from prior phases. Total count should reach ~180+.
- Preserve the multi-page UI shell.
