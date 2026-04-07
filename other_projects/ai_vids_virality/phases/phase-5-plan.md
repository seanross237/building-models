# Phase 5 — Video Generation

## Goal

Replace the Phase 1 stub video generator with a **pluggable video provider adapter** that can call real video-generation APIs (Kling, Luma, Veo, Runway, Pika) using the storyboard frames from Phase 4 as start (and optionally end) frames. ffmpeg stitches the resulting clips into a single final cut.

Like Phase 4, the system gracefully falls back to placeholder MP4s when no API keys are present, so the pipeline always runs end-to-end. The phase report should include at least one real video clip generated end-to-end IF any video API key is configured — but we don't require it (these APIs cost real money per clip, $0.20–$1.50 each).

---

## Acceptance criteria

1. A `VideoProviderAdapter` ABC exists with one method `generate(start_frame, end_frame, prompt, duration_sec)` returning a `VideoClip` dataclass with the path on disk + metadata.

2. **Five adapter implementations**, all wrapping the real APIs but only exercised if the corresponding API key env var is set:
   - `KlingAdapter` — `KLING_API_KEY` (or `KLING_AK`/`KLING_SK` for the JWT-style auth Kling actually uses)
   - `LumaAdapter` — `LUMA_API_KEY`
   - `VeoAdapter` — `GOOGLE_VERTEX_KEY` or service-account JSON path
   - `RunwayAdapter` — `RUNWAY_API_KEY`
   - `PikaAdapter` — `PIKA_API_KEY`
   Plus one **`StubVideoAdapter`** (Phase 1 stub, moved into the new layout) that always copies the placeholder MP4. Used as fallback when no real adapter is available for a given routing decision.

3. `config/video.yaml` controls:
   - The `routing` policy: which adapter handles which kind of beat (default for Phase 5: route everything to the first available real adapter, and if none available, to the stub)
   - Per-adapter config (model name, polling interval, timeout)
   - A hard `max_cost_cents_per_sketch` cap that stops generation early if exceeded

4. When a user approves a storyboard, the backend:
   - Loads beats + storyboard frames
   - For each beat, calls the routed video adapter with the start frame (and end frame if available — Phase 4 only generates start frames, so end is None for now)
   - Polls until each clip is ready (these APIs are async — submit job, poll, download)
   - Stitches the clips with ffmpeg into `data/sketches/{id}/final.mp4`
   - Transitions sketch to `CRITIC_REVIEW`

5. The Critic Review page in the UI now **embeds the actual video** with HTML5 `<video>` tag, sourced from the static `/data` mount. Premise + beats + critic stub still shown alongside.

6. Without any video API key set, the StubVideoAdapter takes over and the placeholder MP4 is used. The pipeline still completes; the Critic Review page just shows the same 2-second black placeholder for every sketch.

7. New tests cover:
   - Adapter interface contract
   - Routing logic in `pipeline.py`
   - Stub adapter
   - Mocked HTTP for each real adapter (one happy path + one failure path each)
   - ffmpeg stitching (use a fixture of multiple short MP4s)
   - Cost-cap enforcement
   - Critic Review page renders the video tag

8. `pytest -m "not network and not llm and not gemini and not video"` is green. New marker `@pytest.mark.video` gates real video API integration tests (skipped by default — they cost money).

---

## New directory additions

```
ai_vids_virality/
  config/
    video.yaml                # NEW
  video_gen/
    __init__.py
    adapter.py                # NEW — VideoProviderAdapter ABC + VideoClip dataclass
    pipeline.py               # NEW — orchestrates clip generation + stitching
    stitch.py                 # NEW — thin ffmpeg wrapper for concatenation
    adapters/
      __init__.py
      kling.py                # NEW
      luma.py                 # NEW
      veo.py                  # NEW
      runway.py               # NEW
      pika.py                 # NEW
      stub_video.py           # MOVED from video_gen/stub_provider.py
    placeholder.mp4           # UNCHANGED
    prompts/
      clip_prompt.md          # NEW — template for per-clip text prompts
  backend/
    main.py                   # UPDATED — wire run_video_pipeline into approve_storyboard endpoint
    static/
      index.html              # UPDATED — Critic Review page embeds the video
  tests/
    test_video_adapters.py    # NEW
    test_video_routing.py     # NEW
    test_video_stitch.py      # NEW
    test_video_pipeline.py    # NEW
    test_critic_review_api.py # NEW
    fixtures/
      sample_clips/clip-01.mp4 # NEW — ffmpeg-generated tiny test clips
      sample_clips/clip-02.mp4
      sample_clips/clip-03.mp4
```

---

## Component specs

### `video_gen/adapter.py`

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class VideoClip:
    beat_n: int
    path: Path
    provider_id: str
    duration_sec: float
    cost_cents: int = 0
    seed: Optional[int] = None
    error: Optional[str] = None

class VideoProviderAdapter(ABC):
    provider_id: str

    @abstractmethod
    def generate(
        self,
        start_frame: Path,
        end_frame: Optional[Path],
        prompt: str,
        duration_sec: float,
        out_path: Path,
    ) -> VideoClip: ...

    @abstractmethod
    def is_available(self) -> bool: ...

    @abstractmethod
    def estimated_cost_cents(self, duration_sec: float) -> int: ...
```

### Real provider adapters

Each adapter is a thin httpx wrapper around its REST API. Common pattern:

1. POST a job submission with the start frame as base64 (or upload to a presigned URL)
2. Poll the status endpoint every N seconds (configurable, default 5s)
3. When status == done, download the MP4 to `out_path`
4. Return `VideoClip(...)` with cost set per adapter's pricing
5. On any failure: return with `error` set, don't raise

The subagent should implement the **call shape** for each real provider (endpoint, request body, response shape) based on each provider's public docs. **Do not invent endpoints.** If the subagent can't verify the exact endpoint format for a provider in time, it should leave that adapter as a stub-with-TODO that returns an error and document it in the phase report. Kling and Luma are highest priority since they support start+end frame interpolation, which we'll use in a future phase.

**Hard requirement: at least the Kling adapter must have a complete real implementation (request shape, polling, response parsing).** The other four can be partial as long as they satisfy the ABC and either work or return an error cleanly.

### `video_gen/adapters/stub_video.py`

The Phase 1 stub, moved. Always copies `placeholder.mp4` to `out_path`. `is_available()` returns True. `estimated_cost_cents()` returns 0.

### `video_gen/stitch.py`

```python
def stitch_clips(clips: list[Path], out_path: Path) -> Path:
    """Concatenate clips with ffmpeg's concat demuxer. Returns out_path on success, raises on failure."""
```

Use ffmpeg's concat-demuxer pattern (write a temp file list, run `ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4`). If clips have mismatched codecs, fall back to re-encoding with `-c:v libx264 -c:a aac`.

### `video_gen/pipeline.py`

```python
def run_video_pipeline(sketch_id: str, store: Store) -> None:
    """
    1. Load sketch (must be in VIDEO_PENDING)
    2. Load beats and storyboard frames
    3. For each beat: pick the routed adapter, call generate(), collect VideoClip
    4. Enforce max_cost_cents_per_sketch — stop if exceeded
    5. Stitch all successful clips into data/sketches/{id}/final.mp4
    6. Save metadata to data/sketches/{id}/clips.json
    7. Run the (still stubbed) critic
    8. Transition to CRITIC_REVIEW
    """
```

Routing logic in Phase 5: walk `config/video.yaml` adapter list in order, pick the first adapter where `is_available()` is True. (Smarter routing — Veo for dialogue beats, Kling for everything else — comes in a polish phase.)

### `config/video.yaml`

```yaml
routing:
  default: ["kling", "luma", "veo", "runway", "pika", "stub"]
budget:
  max_cost_cents_per_sketch: 500    # $5 hard cap
adapters:
  - id: kling
    enabled: true
    adapter: video_gen.adapters.kling.KlingAdapter
    config: { model: kling-v1.6, poll_interval_sec: 5, timeout_sec: 600 }
  - id: luma
    enabled: true
    adapter: video_gen.adapters.luma.LumaAdapter
    config: { model: dream-machine-1.6, poll_interval_sec: 5, timeout_sec: 600 }
  - id: veo
    enabled: true
    adapter: video_gen.adapters.veo.VeoAdapter
    config: { model: veo-3, poll_interval_sec: 10, timeout_sec: 900 }
  - id: runway
    enabled: true
    adapter: video_gen.adapters.runway.RunwayAdapter
    config: { model: gen-4, poll_interval_sec: 5, timeout_sec: 600 }
  - id: pika
    enabled: true
    adapter: video_gen.adapters.pika.PikaAdapter
    config: { model: pika-2, poll_interval_sec: 5, timeout_sec: 600 }
  - id: stub
    enabled: true
    adapter: video_gen.adapters.stub_video.StubVideoAdapter
    config: {}
```

### Backend updates

- `POST /api/sketch/{sketch_id}/approve_storyboard` — now calls `run_video_pipeline(...)` instead of the inline stub. Synchronous (Phase 5 doesn't add background workers; that's polish).
- The endpoint can take a long time when real video gen is happening (minutes per sketch). For Phase 5 the simple solution is: increase the FastAPI timeout, accept the wait, document it. Background workers can come later.
- `GET /api/sketch/{sketch_id}/clips` — returns clip metadata (path, provider, duration, cost) so the UI can show per-clip stats.

### UI updates — Critic Review page

- Each card now embeds:
  - The premise logline + tone
  - An HTML5 `<video controls>` pointing at `/data/sketches/{id}/final.mp4`
  - Below the video: a small breakdown of clips (provider used, total cost in cents)
  - The (still stubbed) critic report
  - Publish / Reject buttons (existing endpoints)

### Tests

- `test_video_adapters.py`:
  - Stub always works
  - Each real adapter `is_available()` is False without env var
  - Mocked HTTP happy path for Kling (the priority real adapter): submit → poll → download → return VideoClip with non-zero size on disk
  - Mocked HTTP failure paths return with error set, don't raise
- `test_video_routing.py`:
  - Routing picks the first available adapter
  - When all real adapters are unavailable, falls back to stub
- `test_video_stitch.py`:
  - Stitch the three fixture clips into one MP4
  - Output exists, has nonzero size, ffprobe reports duration ≈ sum of inputs
- `test_video_pipeline.py`:
  - Full pipeline run on a STORYBOARD_REVIEW sketch with stub adapters
  - Sketch ends in CRITIC_REVIEW
  - `final.mp4` exists with size > 0
- `test_critic_review_api.py`:
  - Approve storyboard → 200 + sketch in critic_review
  - GET clips returns the clips list
  - Static file serving works for the final.mp4 path

---

## Demo script

```bash
cd /Users/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality
source .venv/bin/activate
pip install -r requirements.txt

# Offline tests
pytest -m "not network and not llm and not gemini and not video" -q 2>&1 | tail -5

# Walk a sketch all the way through
python -m pipelines.run_skeleton 2>&1 | tail -10

uvicorn backend.main:app --port 8770 &
SERVER_PID=$!
sleep 2

SKETCH_ID=$(ls data/queues/premise-review/ | head -1 | cut -d'.' -f1 | cut -d'_' -f1)
echo "--- Walking sketch $SKETCH_ID through approve_premise + approve_storyboard ---"

curl -s -X POST -H "Content-Type: application/json" \
  -d '{"model_id":"claude-opus","premise_index":0}' \
  http://localhost:8770/api/sketch/$SKETCH_ID/approve_premise > /dev/null
sleep 2
curl -s -X POST http://localhost:8770/api/sketch/$SKETCH_ID/approve_storyboard > /dev/null
sleep 2

# Inspect the result
curl -s http://localhost:8770/api/sketch/$SKETCH_ID | python -m json.tool | head -30
ls -la data/sketches/$SKETCH_ID/clips/ 2>/dev/null
ls -la data/sketches/$SKETCH_ID/final.mp4

# Confirm the video is reachable via the static mount
curl -s -o /dev/null -w "final.mp4HTTP status: %{http_code}, size: %{size_download}\n" http://localhost:8770/data/sketches/$SKETCH_ID/final.mp4

kill $SERVER_PID
```

---

## Out of scope for Phase 5

- Background / async workers (synchronous is fine for now; pipeline is single-user)
- Music / SFX overlay
- End-frame generation (depends on Phase 4 enhancement)
- Smart routing (per-beat adapter choice based on dialogue presence)
- Real publishing
- Hetzner deployment

---

## Reporting

Write `phases/phase-5-report.md` with:
- File tree diff
- pytest summary
- Demo script output (including the final.mp4 size)
- Which video API keys (if any) were set during the demo
- For each adapter, a one-line note on completeness: "real impl complete" / "real impl partial — endpoint TBD" / "stub only"
- Any deviations
- One paragraph on the new Critic Review page with embedded video

---

## Notes for the executing subagent

- The provider APIs change frequently. **Do not invent endpoints or parameters.** If you can't verify a provider's exact API shape (e.g. you'd have to guess at JSON field names), implement the adapter with TODOs and a clear error message, and prioritize getting Kling correct since it's the one we'll lean on first.
- Pricing estimates are rough — record what you used and we'll refine later.
- ffmpeg is required (already on the box per `remote-dev-box-plan.md`). Test by running `which ffmpeg` first; if it's missing, document and bail out of the stitching tests.
- The static file mount from Phase 4 (`/data`) is what the browser uses to fetch `final.mp4`. Make sure the mount path didn't move.
- Don't break tests from prior phases. Total count should grow from ~110 to ~135+.
- Keep the multi-page UI shell from earlier phases. Only Critic Review page changes.
- Don't add background workers, queues, or async — synchronous is fine. The polish phase can revisit.
- The `max_cost_cents_per_sketch` cap is a hard stop — implement it as a check before each clip generation. If exceeded, stop generation, stitch what we have, log it, and proceed to critic anyway.
