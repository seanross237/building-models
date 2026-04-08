# Phase 4 — Storyboard (nano banana 2)

## Goal

Replace the Phase 1 stub storyboard generator with a **real image-generation pipeline** using **nano banana 2** (Google's `gemini-2.5-flash-image` model). For each approved premise, the system:

1. Generates a **character reference sheet** so faces/outfits stay consistent across frames
2. Generates a **beat sheet** (LLM call to expand the premise into 4–8 shot beats)
3. Generates a **start frame** for each beat, anchored to the character ref sheet
4. Surfaces the storyboard grid in the web UI for human review with **regenerate-this-frame** controls

The user has nano banana 2 access via Google AI Studio (`GEMINI_API_KEY` env var). If the key is missing, the storyboard generator falls back to the Phase 1 placeholder PNG so the pipeline still runs end-to-end.

---

## Acceptance criteria

1. When a user approves a premise on the Premise Review page, the backend **generates a real beat sheet** using the same model adapter from Phase 3 (Claude CLI by default), and writes it to `data/sketches/{sketch_id}/beats.json` with 4–8 beats matching the schema in `PLAN.md` Section 4 / Stage 5.

2. The backend then **generates a character reference sheet**: one PNG per character (front view), saved to `data/sketches/{sketch_id}/refs/{character_slug}.png`. These calls go through the new `StoryboardAdapter`.

3. The backend then **generates a start frame for each beat**, passing the relevant character ref images as additional input to nano banana 2 so faces stay consistent. Frames saved to `data/sketches/{sketch_id}/storyboard/beat-{n:02d}-start.png`.

4. The sketch transitions to `STORYBOARD_REVIEW` and a **storyboard grid** appears on the Storyboard Review page in the web UI: a wide card per sketch with the premise logline, then a grid of frame thumbnails (one per beat) with each frame labeled "Beat N: action description". Each frame has a **regenerate** button that calls a new `/api/sketch/{id}/storyboard/regenerate` endpoint with `{"beat": N}`.

5. **Without `GEMINI_API_KEY`** set, the storyboard generator transparently uses the Phase 1 placeholder PNG for every frame and the pipeline still completes — it just shows the same placeholder for every beat. The fallback path is logged.

6. **With `GEMINI_API_KEY`** set, real frames are generated. The phase-4 demo must include at least one real generated frame (the subagent should base64 the bytes or copy the file path into the report so we can verify a real image landed on disk).

7. New tests cover:
   - StoryboardAdapter contract (real and stub)
   - Beat sheet generation (mocked LLM call)
   - Storyboard generation pipeline end-to-end with stub adapter
   - Regenerate endpoint
   - Character ref sheet generation
   All Phase 1 / 2 / 3 tests still pass.

8. `pytest -m "not network and not llm and not gemini"` is green. Two new markers:
   - `@pytest.mark.gemini` — gates real Gemini image API calls (one integration test)
   - `@pytest.mark.llm` — already exists for Claude calls

---

## New directory additions

```
ai_vids_virality/
  config/
    storyboard.yaml             # NEW — image model config + frame size + style guide
  storyboard/
    __init__.py
    adapter.py                  # NEW — StoryboardAdapter ABC + Frame dataclass
    adapters/
      __init__.py
      gemini_image.py           # NEW — real nano banana 2 caller
      stub_storyboard.py        # MOVED from storyboard/stub_storyboard.py — unchanged behavior
    beats.py                    # NEW — beat sheet generation using Phase 3 model adapter
    pipeline.py                 # NEW — end-to-end storyboard generation orchestration
    placeholder.png             # UNCHANGED — fallback asset
    prompts/
      beat_sheet.md             # NEW — prompt template for beat sheet generation
      character_ref.md          # NEW — prompt template for character ref images
      frame.md                  # NEW — prompt template for per-beat frames
  backend/
    main.py                     # UPDATED — wire the real storyboard pipeline + regenerate endpoint
    static/
      index.html                # UPDATED — Storyboard Review page renders the grid + regen button
  tests/
    test_storyboard_adapters.py # NEW
    test_beats_generation.py    # NEW
    test_storyboard_pipeline.py # NEW
    test_storyboard_api.py      # NEW
    fixtures/
      sample_premise.json       # NEW
```

---

## Component specs

### `storyboard/adapter.py`

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class Frame:
    beat_n: int
    path: Path                # where it was saved on disk
    prompt: str               # the exact prompt used
    seed: Optional[int] = None
    cost_cents: int = 0
    error: Optional[str] = None

@dataclass
class CharacterRef:
    name: str
    slug: str
    path: Path
    prompt: str
    error: Optional[str] = None

class StoryboardAdapter(ABC):
    adapter_id: str           # e.g. "gemini-2.5-flash-image"

    @abstractmethod
    def generate_character_ref(self, character: dict, style_guide: str, out_path: Path) -> CharacterRef: ...

    @abstractmethod
    def generate_frame(self, beat: dict, character_refs: list[CharacterRef], style_guide: str, out_path: Path) -> Frame: ...

    @abstractmethod
    def is_available(self) -> bool: ...
```

### `storyboard/adapters/gemini_image.py`

- `adapter_id = "gemini-2.5-flash-image"`
- `is_available()` returns True iff `GEMINI_API_KEY` is set
- Uses `httpx` directly (no SDK dependency) to call Google AI Studio:
  - Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}`
  - Body: `{"contents": [{"parts": [{"text": prompt}, {"inline_data": {"mime_type": "image/png", "data": "<base64>"}}]}]}`
  - For the character ref call, only a text prompt is sent
  - For the per-beat frame call, character ref images are included as `inline_data` parts so the model conditions on them
- Response handling: Gemini returns either text (skip) or an image part with base64-encoded PNG bytes — decode and write to `out_path`. Returns a `Frame` / `CharacterRef` with the path.
- On any failure (HTTP error, no image in response, JSON parse error), return with `error` set and a placeholder PNG copied to `out_path` so the downstream stages don't choke. Never raise.

### `storyboard/adapters/stub_storyboard.py`

The Phase 1 stub, moved into `adapters/`. Always copies `storyboard/placeholder.png` to `out_path`. `is_available()` returns True. Used when no real adapter is available.

### `storyboard/beats.py`

```python
def generate_beats(sketch: Sketch, model_adapter: ModelAdapter) -> list[dict]:
    """
    Use the Phase 3 model adapter to expand the approved premise into a list of beats.
    Returns a list of dicts matching the beat schema in PLAN.md Stage 5.
    """
```

Reads the prompt template at `storyboard/prompts/beat_sheet.md`, formats with the premise, calls `model_adapter.generate(...)` with a custom prompt, parses the JSON response (`{"beats": [...]}`), returns the beats. Adapter failure → log + return a single fallback beat so the pipeline keeps moving.

### `storyboard/pipeline.py`

```python
def run_storyboard(sketch_id: str, store: Store) -> None:
    """
    Full storyboard generation:
    1. Load the sketch (must be in SCRIPTED status)
    2. Generate beats (LLM)
    3. For each unique character across beats, generate a character ref (image)
    4. For each beat, generate a start frame (image)
    5. Save all metadata to data/sketches/{id}/storyboard.json
    6. Transition the sketch to STORYBOARD_REVIEW
    """
```

Uses `select_storyboard_adapter()` which picks the first available adapter from `config/storyboard.yaml` (real Gemini if key set, else stub).

### `config/storyboard.yaml`

```yaml
adapters:
  - id: gemini-image
    enabled: true
    adapter: storyboard.adapters.gemini_image.GeminiImageAdapter
    config:
      model: gemini-2.5-flash-image
      timeout_sec: 60
  - id: stub
    enabled: true
    adapter: storyboard.adapters.stub_storyboard.StubStoryboardAdapter
    config: {}

default_style_guide: |
  Bright, slightly stylized 3D animation. Cinematic lighting. Consistent character
  faces and outfits. Clean composition. Sketch-comedy energy.

frame_size: 1024x1024
character_ref_size: 512x512
```

The pipeline iterates the `adapters` list and uses the first one whose `is_available()` returns True.

### Backend updates

- `POST /api/sketch/{sketch_id}/approve_premise` — now calls `storyboard.pipeline.run_storyboard(sketch_id, store)` instead of the inline stub. The function blocks during generation (Phase 4 doesn't add async workers — that's later polish).
- `POST /api/sketch/{sketch_id}/storyboard/regenerate` — body `{"beat": N}`. Re-runs frame generation for that beat only. Returns the new frame metadata.
- `GET /api/sketch/{sketch_id}/storyboard` — returns the storyboard JSON + a list of frame URLs the UI can render (e.g. `/static/sketches/{id}/storyboard/beat-01-start.png` — see "Static file serving" below).

### Static file serving

The web UI needs to render generated PNGs. Add a FastAPI mount:

```python
app.mount("/data", StaticFiles(directory=DATA_ROOT), name="data")
```

So `data/sketches/{id}/storyboard/beat-01-start.png` is reachable at `http://localhost:8000/data/sketches/{id}/storyboard/beat-01-start.png`.

### UI updates — Storyboard Review page

- Each sketch is a wide card
- Top: premise logline + tone
- Below: a **grid of frames** (CSS grid, 4 columns or auto-fit). Each cell:
  - The frame image (lazy loaded)
  - Beat number + first sentence of action description
  - A small "regen" button under the frame
- Below the grid: approve / reject buttons for the whole storyboard (existing endpoints)
- The regen button POSTs and on response, swaps the image src (cache-bust with `?t={timestamp}`)

### Tests

- `test_storyboard_adapters.py`:
  - Stub adapter always copies the placeholder
  - Gemini adapter `is_available()` is False without env var
  - Gemini adapter mocked HTTP returns parses image bytes correctly
  - Gemini adapter handles malformed responses → returns with error + placeholder
- `test_beats_generation.py`:
  - Mocked model adapter returns valid JSON → beats parsed
  - Malformed JSON → fallback single beat
  - Empty response → fallback
- `test_storyboard_pipeline.py`:
  - Full pipeline runs with stub adapter against a SCRIPTED sketch → ends in STORYBOARD_REVIEW with frame files on disk
  - Frames count matches beats count
- `test_storyboard_api.py`:
  - GET /api/sketch/{id}/storyboard returns expected shape
  - POST regenerate updates the frame on disk
  - approve_premise transitions through scripted → storyboard_review properly with the new pipeline
- One `@pytest.mark.gemini` integration test that hits the real API if `GEMINI_API_KEY` is set (skipped otherwise)

---

## Demo script

```bash
cd /Users/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality
source .venv/bin/activate
pip install -r requirements.txt

# Offline tests
pytest -m "not network and not llm and not gemini" -q 2>&1 | tail -5

# Pipeline run (Phase 2 collectors + Phase 3 factory + Phase 4 storyboard)
python -m pipelines.run_skeleton 2>&1 | tail -20

# Pick an approvable sketch and walk it forward
SKETCH_ID=$(ls data/queues/premise-review/ | head -1 | cut -d'.' -f1 | cut -d'_' -f1)
echo "--- Walking sketch $SKETCH_ID through approve_premise ---"

uvicorn backend.main:app --port 8769 &
SERVER_PID=$!
sleep 2

# Approve premise (this triggers beat sheet + storyboard generation)
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"model_id":"claude-opus","premise_index":0}' \
  http://localhost:8769/api/sketch/$SKETCH_ID/approve_premise | python -m json.tool | head -20

# Inspect the storyboard
curl -s http://localhost:8769/api/sketch/$SKETCH_ID/storyboard | python -m json.tool | head -40

# List the generated frame files
ls -la data/sketches/$SKETCH_ID/storyboard/
ls -la data/sketches/$SKETCH_ID/refs/ 2>/dev/null

kill $SERVER_PID
```

The subagent must include in `phases/phase-4-report.md`:
- Whether `GEMINI_API_KEY` was set during the demo
- File listing of the generated frames
- If real frames were generated: the file size of one of them (should be > 50KB for a real PNG, ~few hundred bytes for the placeholder)

---

## Out of scope for Phase 4

- Real video generation (Phase 5)
- Real AI critic (Phase 6)
- Async / background frame generation (still synchronous in the approve handler)
- End-frame generation for video interpolation (Phase 5 needs this — defer)
- Style transfer / multiple style guides
- Hetzner deployment

---

## Reporting

Write `phases/phase-4-report.md` with:
- File tree diff
- pytest summary (offline + gemini if key set)
- Demo script output
- Whether real Gemini was used and a file listing showing real PNG sizes (or stub placeholder sizes)
- Any deviations
- One paragraph on the new Storyboard Review page

---

## Notes for the executing subagent

- nano banana 2 = `gemini-2.5-flash-image` on Google AI Studio. The endpoint is the standard generateContent path.
- The Gemini API supports passing **multiple images as input** — that's how character refs become anchors. Each ref goes in as an `inline_data` part alongside the text prompt.
- The model returns image bytes inline (base64 in the JSON response, mime_type `image/png`). Decode and write directly to disk.
- DO NOT use the `google-generativeai` Python SDK — call the REST API directly with httpx. Cleaner, no version conflicts.
- The Phase 1 placeholder PNG must remain in place — both the stub adapter and the error fallback in the real adapter use it.
- Don't break the Phase 1+2+3 test suites. Total count should grow from ~92 to ~110+.
- Preserve the multi-page UI shell from earlier phases. Only the Storyboard Review page content changes.
- If you can't acquire a real `GEMINI_API_KEY` during this run, the demo still has to work end-to-end via stub. Document it and move on.
- The static file mount `/data` is the simple way to serve generated images to the browser. Make sure it doesn't shadow `/api`. Mount it last.
