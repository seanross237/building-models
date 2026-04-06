# Phase 1 — Skeleton End-to-End

## Goal

Build a runnable end-to-end pipeline on the laptop using **stub data and stub generators**, with a working web kanban UI. The whole pipeline must run with `python -m pipelines.run_skeleton` followed by `uvicorn backend.main:app`, and a human must be able to walk a sketch from "signal" to "published" by clicking buttons in a browser.

**Zero external API calls.** No Claude, no Gemini, no Reddit, no money spent. This phase exists to lock the contracts (file layout, state machine, queue transitions, web UI) so later phases can plug real implementations into stable seams.

---

## Acceptance criteria — must all be true at the end

1. From a clean clone of `other_projects/ai_vids_virality/`, running:
   ```bash
   cd other_projects/ai_vids_virality
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python -m pipelines.run_skeleton
   uvicorn backend.main:app --reload --port 8000
   ```
   produces a live kanban at `http://localhost:8000` with at least 3 sketches sitting in the leftmost column.

2. A human can click "Approve" on a card and watch it move to the next column. By approving through every gate, a card reaches "Published" with a stub video file recorded against it.

3. `pytest` passes with all tests green. Test coverage includes: collector creates files, analyzer transitions queues, state machine transitions are valid, every API endpoint responds correctly, and there's at least one full integration test that runs the whole pipeline against an in-memory state directory and asserts a sketch reaches `published`.

4. All files live under `other_projects/ai_vids_virality/`. Nothing is written outside that directory.

5. The code is structured so that each stub module (collector, analyzer, idea factory, storyboard, video gen, critic) has a clear `generate()` / `run()` function with type hints — these are the seams that later phases will swap for real implementations.

---

## Directory layout to create

```
ai_vids_virality/
  PLAN.md                          # already exists
  README.md                        # NEW — how to run
  requirements.txt                 # NEW
  phases/
    phase-1-plan.md                # this file
  config/
    comedy-lens.md                 # NEW — placeholder rubric (1 paragraph is fine)
    sources.yaml                   # NEW — list of collectors to run (just reddit_stub for now)
    thresholds.yaml                # NEW — promotion thresholds
  data/                            # state lives here, gitignored except .gitkeep files
    signals/
      reddit_stub/
        items/.gitkeep
        .seen-ids                  # empty
    queues/
      idea-factory/.gitkeep
      premise-review/.gitkeep
      manual-ideas/.gitkeep
      scripted/.gitkeep
      storyboard-review/.gitkeep
      video-gen/.gitkeep
      final-review/.gitkeep
    sketches/.gitkeep
    published/.gitkeep
    leaderboard.json               # initialized as {}
  collectors/
    __init__.py
    reddit_stub/
      __init__.py
      fetch.py                     # emits 3 hardcoded signal files
  analyzers/
    __init__.py
    score_signals/
      __init__.py
      analyze.py                   # rule-based stub scorer
      prompt.md                    # NEW — placeholder, used in later phase
      schema.json                  # NEW — analyzer output schema
  idea_factory/
    __init__.py
    stub_factory.py                # generates 3 hardcoded premises per signal
  storyboard/
    __init__.py
    stub_storyboard.py             # creates placeholder PNG files
    placeholder.png                # one 512x512 solid color PNG checked in
  video_gen/
    __init__.py
    stub_provider.py               # creates a placeholder MP4 (ffmpeg-generated 2sec solid color, OR copies a checked-in placeholder)
    placeholder.mp4                # 2-second solid color clip checked in
  critic/
    __init__.py
    stub_critic.py                 # outputs hardcoded critic JSON
  state/
    __init__.py
    machine.py                     # the state machine — lifecycle, transitions
    store.py                       # file-based store: read/write sketches, queues
  pipelines/
    __init__.py
    run_skeleton.py                # runs collector → analyzer → factory in order, populates queues
  backend/
    __init__.py
    main.py                        # FastAPI app + static file serving
    static/
      index.html                   # single-file kanban UI (vanilla JS, no build step)
  scripts/
    .gitkeep                       # populated in later phases
  tests/
    __init__.py
    test_collector.py
    test_analyzer.py
    test_state_machine.py
    test_api.py
    test_end_to_end.py             # the integration test
  .gitignore                       # ignores .venv/, data/, *.pyc, __pycache__
```

---

## Component specifications

### `state/machine.py` — sketch lifecycle

A sketch is identified by `sketch_id` (string, e.g. `sk-2026-04-06-001`). It moves through these statuses:

```python
class Status(str, Enum):
    SIGNAL = "signal"                       # raw radar item, not yet a sketch
    IDEA_PENDING = "idea_pending"           # signal promoted to factory, no premises yet
    PREMISE_REVIEW = "premise_review"       # premises generated, waiting for human
    SCRIPTED = "scripted"                   # premise approved, beats generated
    STORYBOARD_REVIEW = "storyboard_review" # frames generated, waiting for human
    VIDEO_PENDING = "video_pending"         # storyboard approved, video gen pending
    CRITIC_REVIEW = "critic_review"         # video done, critic ran, waiting for human
    PUBLISHED = "published"
    REJECTED = "rejected"
```

Valid transitions are explicit in `VALID_TRANSITIONS: dict[Status, set[Status]]`. Any invalid transition raises `InvalidTransition`.

### `state/store.py` — file-based store

```python
class Store:
    def __init__(self, root: Path): ...
    def list_sketches(self) -> list[Sketch]: ...
    def get_sketch(self, sketch_id: str) -> Sketch: ...
    def save_sketch(self, sketch: Sketch) -> None: ...
    def transition(self, sketch_id: str, new_status: Status, payload: dict) -> Sketch: ...
        # validates transition, updates status, appends to history.json
```

`Sketch` is a dataclass / Pydantic model with: `id`, `status`, `signal_id`, `premise`, `beats`, `storyboard_frames`, `video_clips`, `final_cut_path`, `critic_report`, `cost_cents_total`, `history`.

Each sketch lives at `data/sketches/{sketch_id}/sketch.json`. Helper paths:
- `data/sketches/{sketch_id}/refs/`
- `data/sketches/{sketch_id}/storyboard/`
- `data/sketches/{sketch_id}/clips/`
- `data/sketches/{sketch_id}/final.mp4`

### `collectors/reddit_stub/fetch.py`

Function `fetch(store: Store) -> list[str]` that returns the list of new signal IDs it created. Writes 3 hardcoded markdown files (with YAML frontmatter) to `data/signals/reddit_stub/items/`, dedupes via `.seen-ids`. The 3 hardcoded signals should be funny and concrete — example titles:
- "Senator caught using spoon as wifi antenna in committee hearing"
- "Tech CEO announces 4-day work week, then 5-day, then 6-day in same press conference"
- "Local man discovers he's been pronouncing his own name wrong for 40 years"

If the collector is run twice, it should not duplicate (idempotent via `.seen-ids`).

### `analyzers/score_signals/analyze.py`

Function `analyze_pending(store: Store) -> list[str]` that finds unanalyzed signal files in `data/signals/`, applies a stub rule-based scorer (e.g. `len(title) % 10 + 5`), writes summary metadata, and promotes signals with score ≥ 7 to `data/queues/idea-factory/{signal_id}.json`.

### `idea_factory/stub_factory.py`

Function `run_factory(store: Store) -> list[str]` that reads `data/queues/idea-factory/`, for each signal creates a new sketch with status `PREMISE_REVIEW`, generates 3 hardcoded premises (vary the loglines based on signal title for verisimilitude), saves the sketch, and writes a marker in `data/queues/premise-review/`.

### `pipelines/run_skeleton.py`

Top-level orchestrator. Imports the three above and runs them in order. Idempotent — running twice should not duplicate sketches.

```python
def main():
    store = Store(root=Path("data"))
    new_signals = reddit_stub.fetch(store)
    analyzed = score_signals.analyze_pending(store)
    new_sketches = stub_factory.run_factory(store)
    print(f"Phase 1 pipeline run: {len(new_signals)} signals, {len(analyzed)} analyzed, {len(new_sketches)} sketches")

if __name__ == "__main__":
    main()
```

### `backend/main.py` — FastAPI app

Endpoints:

- `GET /` → serves `backend/static/index.html`
- `GET /api/kanban` → returns all sketches grouped by status:
  ```json
  {
    "premise_review": [{...sketch summary...}],
    "scripted": [...],
    ...
  }
  ```
- `GET /api/sketch/{sketch_id}` → full sketch detail
- `POST /api/sketch/{sketch_id}/approve_premise` → transitions to `SCRIPTED`, fills in stub beats, then immediately runs stub storyboard generation, transitions to `STORYBOARD_REVIEW`
- `POST /api/sketch/{sketch_id}/approve_storyboard` → transitions to `VIDEO_PENDING`, runs stub video gen, runs stub critic, transitions to `CRITIC_REVIEW`
- `POST /api/sketch/{sketch_id}/publish` → transitions to `PUBLISHED`
- `POST /api/sketch/{sketch_id}/reject` → transitions to `REJECTED` from any status
- `POST /api/manual_idea` → body `{"text": "..."}` creates a new sketch directly in `PREMISE_REVIEW` with the text as the only premise

For Phase 1, the storyboard/video/critic stages are inlined (synchronous) inside the approve endpoints — no background workers yet. They're cheap stubs.

CORS is enabled for localhost. Static files served from `backend/static/`.

### `backend/static/index.html` — single-file kanban

One HTML file. No build step. Vanilla JS (or Alpine.js loaded from CDN if it makes the code shorter).

Layout: a row of columns, one per status, each containing cards. Each card shows the sketch ID, the first premise logline, and stage-appropriate action buttons:

| Column | Buttons |
|---|---|
| Premise Review | Approve, Reject |
| Storyboard Review | Approve, Reject |
| Critic Review | Publish, Reject |
| Published | (none) |
| Rejected | (none) |

Click a card to open a side panel with the full sketch JSON pretty-printed (read-only is fine).

A `+ New Idea` button at the top opens a textarea modal that POSTs to `/api/manual_idea`.

After any action, the UI refreshes its state by re-fetching `/api/kanban`. SSE / websockets are out of scope for Phase 1 — polling on action is fine.

Style minimally with inline CSS or one `<style>` block. Dark background, columns with light borders. Doesn't have to be pretty, has to be usable.

### `requirements.txt`

```
fastapi>=0.110
uvicorn[standard]>=0.27
pydantic>=2.5
pyyaml>=6.0
pytest>=8.0
httpx>=0.27        # for FastAPI test client
```

### `tests/`

- `test_collector.py` — assert `fetch` creates exactly 3 files on first run, 0 on second run
- `test_analyzer.py` — assert analyze_pending promotes high-scoring signals to the idea-factory queue
- `test_state_machine.py` — exhaustively test valid transitions and that invalid ones raise
- `test_api.py` — use `TestClient`, hit every endpoint, assert status codes and response shapes
- `test_end_to_end.py` — the headline test:
  1. Spin up Store in a tmp dir
  2. Run the skeleton pipeline
  3. Assert 3 sketches exist in `PREMISE_REVIEW`
  4. Use TestClient to approve_premise → assert `STORYBOARD_REVIEW`
  5. approve_storyboard → assert `CRITIC_REVIEW`
  6. publish → assert `PUBLISHED`
  7. Assert the published sketch has a `final.mp4` file on disk (even if it's the placeholder)

### Stub assets

- `storyboard/placeholder.png` — a 512x512 solid color PNG. Generate it with PIL during the build, or save a tiny valid PNG byte string. Don't ship a downloaded image.
- `video_gen/placeholder.mp4` — a 2-second 320x240 black video. Generate it with `ffmpeg -f lavfi -i color=c=black:s=320x240:d=2 -y placeholder.mp4` during the build, OR if ffmpeg is not available, write a stub that creates a tiny valid MP4 byte sequence. Acceptable to require ffmpeg for the build (it's already on the Hetzner box per the remote-dev-box-plan, and the user has it locally too).

---

## Out of scope for Phase 1

- Real LLM calls
- Real video / image generation
- Multi-model A/B
- Storyboard frame regeneration UI
- Background workers / tmux controller
- Hetzner deployment
- Authentication
- Tailwind / Next.js / any frontend build step
- Database (everything is files)

---

## Demo script (the subagent must run this and confirm it works)

```bash
cd other_projects/ai_vids_virality
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Generate stub assets if needed
python -c "from PIL import Image; Image.new('RGB',(512,512),'#444').save('storyboard/placeholder.png')" || true
ffmpeg -f lavfi -i color=c=black:s=320x240:d=2 -y video_gen/placeholder.mp4

# Run the pipeline
python -m pipelines.run_skeleton

# Run the tests
pytest -v

# Start the server in background, hit the API, kill it
uvicorn backend.main:app --port 8765 &
SERVER_PID=$!
sleep 2
curl -s http://localhost:8765/api/kanban | python -m json.tool | head -40
# Approve the first sketch all the way to published
SKETCH_ID=$(curl -s http://localhost:8765/api/kanban | python -c "import sys,json;d=json.load(sys.stdin);print(d['premise_review'][0]['id'])")
curl -s -X POST http://localhost:8765/api/sketch/$SKETCH_ID/approve_premise
curl -s -X POST http://localhost:8765/api/sketch/$SKETCH_ID/approve_storyboard
curl -s -X POST http://localhost:8765/api/sketch/$SKETCH_ID/publish
curl -s http://localhost:8765/api/sketch/$SKETCH_ID | python -m json.tool
kill $SERVER_PID
```

The subagent must include the actual output of these commands in its report so we can verify.

---

## Notes for the executing subagent

- Read `PLAN.md` first for the broader architecture context
- Read `research_hub/research-radar/analyzers/summarize-and-score/analyze-items.py` and `research_hub/research-radar/collectors/youtube/` for the conventions you're modeling on
- Don't add Tailwind, React, Next.js, or any frontend build step. Single HTML file. This is a contract — don't deviate.
- Don't add databases, docker, alembic, or any persistence beyond JSON files
- All paths should use `pathlib.Path`, not string concatenation
- All file I/O should be UTF-8 explicit
- Add type hints throughout — these are the contracts later phases will rely on
- Pin requirements with `>=` not `==` (this is a fast-moving project, not a release)
- Don't write markdown comments that just narrate what code does. Comment only non-obvious decisions
- If you hit an unexpected blocker (e.g. a tool isn't installed), document it and continue with a workaround rather than stopping
- When done, write a `phases/phase-1-report.md` summarizing: what was built, test results, demo command output, any deviations from this plan and why
