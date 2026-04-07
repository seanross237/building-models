# Phase 6 — AI Critic

## Goal

Replace the Phase 1 stub critic with a **real two-layer AI critic**:

1. **Shot-level check** — runs after each clip is generated. A multimodal model verifies the clip matches the storyboard frame, has no obvious artifacts, and the character is consistent. If the check fails, the system **automatically regenerates** the clip up to N retries before flagging the sketch for human review.

2. **Full-sketch critic** — runs on the assembled cut. A multimodal model watches/scores the whole sketch on comedic timing, pacing, punchline landing, audio clarity, and "is this actually funny." Outputs structured JSON with scores + concrete fix suggestions.

Both layers are pluggable via a `CriticAdapter` ABC and gracefully fall back to deterministic stubs when no API keys are set.

---

## Acceptance criteria

1. A `CriticAdapter` ABC exists with two methods: `check_shot(clip, expected_frame, character_refs) -> ShotReport` and `critique_sketch(final_cut_path, sketch_metadata) -> SketchCritique`.

2. **Two real adapters** + one stub:
   - `GeminiVideoCritic` — uses Gemini 2.5 Pro's native video input via `gemini-2.5-pro` (real if `GEMINI_API_KEY` set; stub otherwise)
   - `ClaudeFrameCritic` — samples N frames from each clip with ffmpeg, sends them to Claude with the audio transcript (whisper if available, else skipped), gets a critique back. Real if Claude CLI is available.
   - `StubCritic` — Phase 1 stub, moved into the new layout, returns deterministic hardcoded reports

3. The Phase 5 video pipeline now invokes shot-level check after each clip generation. If `ShotReport.passed == False` and we haven't hit the retry cap, regenerate the clip. Log every retry.

4. After stitching, the full-sketch critic runs and stores its report at `data/sketches/{id}/critic.json`.

5. The Critic Review page in the UI now shows the **real critic report** alongside the embedded video: scores per axis, the list of issues, and the fix suggestions.

6. New tests cover the adapter contract, mocked happy paths for each real adapter, retry logic on shot check failures, and the critic API endpoint.

7. `pytest -m "not network and not llm and not gemini and not video and not critic"` is green. New marker `@pytest.mark.critic` for the real-API integration tests.

---

## New directory additions

```
ai_vids_virality/
  config/
    critic.yaml                 # NEW
  critic/
    __init__.py
    adapter.py                  # NEW — ABC + ShotReport, SketchCritique dataclasses
    pipeline.py                 # NEW — shot-check + full-sketch orchestration
    adapters/
      __init__.py
      gemini_video.py           # NEW
      claude_frame.py           # NEW
      stub_critic.py            # MOVED from critic/stub_critic.py
    frame_sampler.py            # NEW — ffmpeg-based frame sampling for Claude path
    prompts/
      shot_check.md
      full_sketch.md
  video_gen/
    pipeline.py                 # UPDATED — wire shot-level check + retry into the loop
  backend/
    main.py                     # UPDATED — real critic in the approve_storyboard handler
    static/
      index.html                # UPDATED — Critic Review page renders the structured report
  tests/
    test_critic_adapters.py
    test_critic_pipeline.py
    test_shot_retry_logic.py
    test_critic_api.py
```

---

## Component specs

### `critic/adapter.py`

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

@dataclass
class ShotReport:
    beat_n: int
    passed: bool
    score: int                  # 0-10
    issues: list[str]           # ["face morphs at 1.2s", "background flickers"]
    suggestions: list[str]      # ["regenerate with stricter character ref"]
    raw_response: Optional[str] = None
    error: Optional[str] = None

@dataclass
class SketchCritique:
    sketch_id: str
    overall_score: int          # 0-10
    axes: dict                  # {"comedic_timing": 7, "pacing": 6, "punchline": 8, "audio": 5}
    issues: list[str]
    fix_suggestions: list[str]
    is_funny: bool              # the headline judgment
    raw_response: Optional[str] = None
    error: Optional[str] = None

class CriticAdapter(ABC):
    adapter_id: str

    @abstractmethod
    def check_shot(self, clip_path: Path, expected_frame: Path, character_refs: list[Path], beat_metadata: dict) -> ShotReport: ...

    @abstractmethod
    def critique_sketch(self, final_cut_path: Path, sketch_metadata: dict) -> SketchCritique: ...

    @abstractmethod
    def is_available(self) -> bool: ...
```

### `critic/adapters/gemini_video.py`

- Uses Gemini 2.5 Pro via the same REST endpoint as Phase 4 storyboard, but with a `gemini-2.5-pro` model and video as input
- Video input: Gemini supports inline video bytes for short clips (under N MB) or a `file_data` URI from the Files API for longer ones — for the per-clip shot check (a few seconds), inline is fine
- Build a prompt that asks for structured JSON matching `ShotReport` / `SketchCritique`
- Parse the JSON, return the dataclass
- On failure: return with `error` set, `passed=True` (don't block retries on infrastructure errors), `score=0`

### `critic/adapters/claude_frame.py`

- Samples 4 frames from each clip using `frame_sampler.sample_frames(clip_path, n=4)` — ffmpeg-based, returns list of PNG paths
- Reads the storyboard frame + the sampled frames + character refs
- Builds a prompt asking Claude to compare the sampled frames against the storyboard frame and report on consistency
- Spawns `claude -p` (same pattern as Phase 3 ClaudeCLIAdapter) with the prompt
- Parses the JSON response
- For full-sketch critique: samples a denser set of frames across the full cut, optionally extracts audio with `ffmpeg -i in.mp4 -vn -ar 16000 audio.wav`, transcribes with whisper if available, and includes the transcript in the prompt

### `critic/frame_sampler.py`

```python
def sample_frames(clip_path: Path, n: int, out_dir: Path) -> list[Path]:
    """Sample n frames evenly across the clip using ffmpeg. Returns list of frame paths."""
```

Use `ffmpeg -i in.mp4 -vf "select='eq(n\,0)+eq(n\,N/4)+..." -vsync vfr out_%02d.png` or simpler: `-vf fps=N/duration` with a target frame count.

### `critic/pipeline.py`

```python
def run_shot_checks(sketch: Sketch, store: Store) -> list[ShotReport]:
    """For each clip, run the routed critic adapter's shot check. Return list of reports."""

def run_full_critique(sketch: Sketch, store: Store) -> SketchCritique:
    """Run the full-sketch critique on data/sketches/{id}/final.mp4. Return the critique."""
```

### Video pipeline integration (`video_gen/pipeline.py` updated)

Modify `run_video_pipeline` to:

```python
for beat in beats:
    for attempt in range(max_retries := 3):
        clip = adapter.generate(...)
        if clip.error:
            break  # provider error, log and move on
        report = critic.check_shot(clip.path, expected_frame, character_refs, beat_metadata)
        if report.passed or attempt == max_retries - 1:
            break
        # otherwise regenerate
```

Cap retries via `config/critic.yaml`. Default 2 retries.

### `config/critic.yaml`

```yaml
shot_check:
  max_retries: 2
  enabled: true
full_sketch:
  enabled: true
adapters:
  - id: gemini-video
    enabled: true
    adapter: critic.adapters.gemini_video.GeminiVideoCritic
    config: { model: gemini-2.5-pro, timeout_sec: 120 }
  - id: claude-frame
    enabled: true
    adapter: critic.adapters.claude_frame.ClaudeFrameCritic
    config: { cli_model: claude-opus-4-6, timeout_sec: 120, n_frames_per_clip: 4 }
  - id: stub
    enabled: true
    adapter: critic.adapters.stub_critic.StubCritic
    config: {}
```

The pipeline picks the first available adapter from the list. Stub is the catch-all.

### Backend updates

- The `approve_storyboard` handler chain now includes the real critic invocation (it was already there from Phase 1, just with the stub). Replace the stub call with `critic.pipeline.run_full_critique(...)` after stitching.
- `GET /api/sketch/{id}/critic` — returns the SketchCritique JSON

### UI updates — Critic Review page

- Below the embedded video (added in Phase 5), render a structured critic panel:
  - Headline: `is_funny` (yes/no with color)
  - Overall score with a colored bar
  - Per-axis bars
  - Issues list (red bullets)
  - Fix suggestions (blue bullets)
- A "send back for regen" button that resets the sketch to STORYBOARD_REVIEW (or VIDEO_PENDING — depends what the user wants to redo). For Phase 6, send-back goes to VIDEO_PENDING. The state machine needs a new transition added.
- Existing publish / reject buttons stay

### State machine update

Add a transition: `CRITIC_REVIEW → VIDEO_PENDING` (send back for video regen).

### Tests

- `test_critic_adapters.py` — stub always works; real adapters not available without keys; mocked HTTP happy + failure paths
- `test_critic_pipeline.py` — full-sketch critique runs against a fixture MP4 with stub adapter; returns expected dataclass shape
- `test_shot_retry_logic.py` — mock a video adapter that always succeeds, mock a critic that fails twice then passes, assert the pipeline regenerates twice and stops
- `test_critic_api.py` — GET /api/sketch/{id}/critic returns the report; the new send-back transition works

---

## Demo script

```bash
cd /Users/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality
source .venv/bin/activate

pytest -m "not network and not llm and not gemini and not video and not critic" -q 2>&1 | tail -5

python -m pipelines.run_skeleton 2>&1 | tail -10

uvicorn backend.main:app --port 8771 &
SERVER_PID=$!
sleep 2

SKETCH_ID=$(ls data/queues/premise-review/ | head -1 | cut -d'.' -f1 | cut -d'_' -f1)

curl -s -X POST -H "Content-Type: application/json" \
  -d '{"model_id":"claude-opus","premise_index":0}' \
  http://localhost:8771/api/sketch/$SKETCH_ID/approve_premise > /dev/null
curl -s -X POST http://localhost:8771/api/sketch/$SKETCH_ID/approve_storyboard > /dev/null
sleep 2

curl -s http://localhost:8771/api/sketch/$SKETCH_ID/critic | python -m json.tool

kill $SERVER_PID
```

---

## Out of scope for Phase 6

- Multi-model critic A/B (could come later — for Phase 6 just one critic per sketch)
- Whisper integration (optional — if it's installed great, otherwise skip audio transcript)
- Background async — still synchronous
- Hetzner deployment

---

## Reporting

`phases/phase-6-report.md` with file tree, pytest summary, demo output (the actual critic JSON for one sketch), and a one-paragraph description of the Critic Review panel.

---

## Notes for the executing subagent

- The shot-check retry loop is the heart of this phase. Get it right: video gen → critic check → retry if fail → stop on success or retry exhaustion.
- Don't break Phase 5 video pipeline tests — extend them, don't rewrite.
- Whisper is optional. If `whisper` isn't installed, skip the transcript and document it. Don't add it to requirements.
- Total test count should reach ~150+ after this phase.
- Keep the multi-page UI shell. Only Critic Review changes.
- If Gemini and Claude are both unavailable, the stub takes over and the pipeline still completes — just with a hardcoded "is_funny=true, score=7" critique. Document this.
