# Phase 3 — Multi-Model Idea Factory

## Goal

Replace the stub idea factory with a **real LLM-backed factory** that can run **multiple models against the same signal** and surface their premises side-by-side in the review UI. This is where the pipeline starts actually generating comedy premises from real news instead of hardcoded strings.

The factory must be **pluggable**: a `ModelAdapter` interface with one real implementation (Claude via the `claude -p` CLI, which is already installed and authenticated on this machine) and stub implementations for GPT-5 and Gemini that the user can swap in later by setting API keys.

A tiny **leaderboard** tracks approval rates per model so we can see which one the human actually likes best over time.

---

## Acceptance criteria

1. Running the pipeline promotes real Reddit/HN/news signals to the factory, and the factory calls **one or more models** per signal and writes their premises to `data/queues/premise-review/`. Each model's premises are stored in a separate file so the UI can show them side-by-side.

2. At least **one real model call works end-to-end** — Claude via `claude -p --output-format json`. The subagent must capture the output of at least one real Claude call on a real Reddit signal and include it in the phase report.

3. **Two stub model adapters** are in place for OpenAI (`gpt-5`) and Gemini (`gemini-2.5-pro`). They're wired into the same interface, live in the same `config/models.yaml`, and can be enabled by setting env vars (`OPENAI_API_KEY`, `GEMINI_API_KEY`) — but with no key set, they gracefully fall back to "stub mode" that returns 3 deterministic placeholder premises so the factory loop still runs.

4. The **premise-review page** in the web UI now shows premises grouped by sketch, and within each sketch, premises are **grouped by model side-by-side**. The user can approve any single premise variant (not all at once), and the approved one becomes the sketch's canonical premise.

5. The **leaderboard** is updated on every approve/reject action and is surfaced as a small top-right widget on the dashboard showing `{model_id}: {approved}/{total} ({rate}%)`.

6. The `config/models.yaml` file controls which models are enabled, their CLI/API invocation, cost hints, and routing policy (for Phase 3 the policy is just "run all enabled models on every signal" — smarter routing comes later).

7. All Phase 1 and Phase 2 tests still pass. New tests cover:
   - Model adapter interface contract (all adapters return the same shape)
   - Stub adapters work without API keys set
   - Factory loop handles adapter failures gracefully (one model failing doesn't block the others)
   - Leaderboard updates on approve/reject
   - The new side-by-side premise-review API endpoint returns the expected shape

8. `pytest -m "not network and not llm"` must be green. A new `@pytest.mark.llm` marker gates the one real-Claude-call integration test so tests remain free by default.

---

## New directory additions

```
ai_vids_virality/
  config/
    models.yaml                  # NEW — model roster + enabled flags + invocation config
  idea_factory/
    __init__.py
    adapter.py                   # NEW — ModelAdapter ABC + PremiseResult dataclass
    adapters/
      __init__.py
      claude_cli.py              # NEW — spawns `claude -p` subprocess, parses JSON
      openai_stub.py             # NEW — real call if OPENAI_API_KEY set, else stub
      gemini_stub.py             # NEW — real call if GEMINI_API_KEY set, else stub
    factory.py                   # NEW — loads enabled adapters, runs each on each signal
    prompts/
      premise_generation.md      # NEW — the prompt template all models use
    stub_factory.py              # UNCHANGED (kept as fallback for offline tests)
  state/
    leaderboard.py               # NEW — read/write data/leaderboard.json
  backend/
    main.py                      # UPDATED — new endpoints for side-by-side premises + leaderboard
    static/
      index.html                 # UPDATED — premise-review page redesign, leaderboard widget
  tests/
    test_model_adapters.py       # NEW
    test_idea_factory.py         # NEW
    test_leaderboard.py          # NEW
    test_premise_review_api.py   # NEW
```

---

## Component specs

### `idea_factory/adapter.py`

The contract every model adapter implements:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Premise:
    logline: str
    synopsis: str
    tone: str
    target_length_sec: int
    characters: list[dict]
    twist: str

@dataclass
class PremiseResult:
    model_id: str                   # e.g. "claude-opus-4-6"
    signal_id: str
    premises: list[Premise]         # the N premises generated
    cost_cents: int = 0
    duration_ms: int = 0
    raw_response: Optional[str] = None
    error: Optional[str] = None     # set if the call failed — premises is then empty

class ModelAdapter(ABC):
    model_id: str                   # class attribute — must be set by subclass

    @abstractmethod
    def generate(self, signal: dict, prompt: str, n_premises: int = 3) -> PremiseResult:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the adapter can actually call a real model right now."""
        ...
```

### `idea_factory/adapters/claude_cli.py`

- `model_id = "claude-opus-4-6"` (or whatever the user's default Claude model is — read from the adapter config)
- `is_available()` returns True if `which claude` succeeds
- `generate()`:
  1. Loads the prompt template from `idea_factory/prompts/premise_generation.md`
  2. Formats it with the signal data (title, source, summary, source URL)
  3. Builds command: `["claude", "-p", "--model", self.model, "--output-format", "json", formatted_prompt]`
  4. `subprocess.run(...)` with a timeout (120s)
  5. Parses stdout as JSON; the Claude CLI with `--output-format json` returns a JSON object with the assistant's text in a field like `result` or `response` — the adapter needs to handle whatever shape the CLI actually returns (read `research_hub/research-radar/runner/agent-runner/lib/claude.js` as a reference for the shape)
  6. Inside the assistant's response, expect JSON matching the `Premise` schema — wrapped in a `{"premises": [...]}` object. The prompt explicitly asks for JSON output.
  7. Returns a `PremiseResult` with the parsed premises and the cost (if available in the CLI output; else 0)
- On any failure (timeout, non-zero exit, JSON parse error), return a `PremiseResult` with `error` set and empty `premises`. Never raise.

### `idea_factory/adapters/openai_stub.py` and `gemini_stub.py`

Same interface. `is_available()` returns True if the API key env var is set. If not, `generate()` returns three **deterministic stub premises** derived from the signal title (so tests can assert exact output).

If the key IS set, these should make a real API call — but in Phase 3, the user probably doesn't have keys yet, so we won't exercise that path. The code still needs to be there for completeness. Use `httpx` to call:
- OpenAI: `POST https://api.openai.com/v1/chat/completions` with `model: "gpt-5"` (or `"gpt-5-turbo"` — read from adapter config)
- Gemini: `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent`

Don't hand-roll the auth — just bearer token / API key query param as documented.

Wrap the real-API code path in `if not self.is_available(): return self._stub_result(signal)` so the stub always works.

### `idea_factory/factory.py`

```python
def run_factory(store: Store, models_config_path: Path = Path("config/models.yaml")) -> list[str]:
    """
    Read data/queues/idea-factory/, for each signal run all enabled ModelAdapters,
    write each adapter's PremiseResult to data/queues/premise-review/{sketch_id}__{model_id}.json,
    and create a Sketch in PREMISE_REVIEW status. Returns list of new sketch IDs.
    """
```

Key behaviors:
- If multiple adapters run on the same signal, they produce **one sketch** with **multiple premise variants** — the sketch's status is `PREMISE_REVIEW` and the store knows which premises came from which model.
- Adapters run sequentially within a signal (not parallel — keep Phase 3 simple). Parallelism can come in a later phase via the colossus-style controller.
- If an adapter fails (returns with `error`), the factory logs it and moves on — the other adapters' premises still count.
- If ALL adapters fail for a signal, the factory marks the signal as processed (skip `.seen-ids` style) but creates no sketch, and logs the failure.

### `idea_factory/prompts/premise_generation.md`

The prompt template. Placeholder vars: `{signal_title}`, `{signal_source}`, `{signal_url}`, `{signal_summary}`, `{n_premises}`, `{comedy_lens}`.

The prompt should:
1. Give the model a comedy writer persona
2. Paste the signal data
3. Paste the relevant sections of `config/comedy-lens.md` as context
4. Instruct the model to output strict JSON matching the schema:
   ```json
   {
     "premises": [
       {
         "logline": "...",
         "synopsis": "...",
         "tone": "...",
         "target_length_sec": 30,
         "characters": [{"name": "...", "description": "..."}],
         "twist": "..."
       }
     ]
   }
   ```
5. Explicitly say "Output only JSON, no prose, no markdown fences."

### `config/models.yaml`

```yaml
default_n_premises: 3
models:
  - id: claude-opus
    enabled: true
    adapter: idea_factory.adapters.claude_cli.ClaudeCLIAdapter
    config:
      cli_model: claude-opus-4-6
      timeout_sec: 120
  - id: gpt-5
    enabled: true
    adapter: idea_factory.adapters.openai_stub.OpenAIAdapter
    config:
      api_model: gpt-5
      timeout_sec: 120
  - id: gemini-2.5-pro
    enabled: true
    adapter: idea_factory.adapters.gemini_stub.GeminiAdapter
    config:
      api_model: gemini-2.5-pro
      timeout_sec: 120
```

### `state/leaderboard.py`

Simple file-backed leaderboard:

```python
# data/leaderboard.json
{
  "claude-opus": {"total": 12, "approved": 5, "rejected": 7},
  "gpt-5":      {"total": 12, "approved": 3, "rejected": 9},
  "gemini-2.5-pro": {"total": 12, "approved": 4, "rejected": 8}
}
```

Functions:
- `record_generation(model_id: str) -> None` — increment total when a premise is generated
- `record_decision(model_id: str, approved: bool) -> None` — increment approved or rejected when the human acts
- `get_leaderboard() -> dict` — return the full leaderboard for the API

### Backend updates (`backend/main.py`)

New/updated endpoints:
- `GET /api/sketch/{sketch_id}/premises` — returns:
  ```json
  {
    "sketch_id": "...",
    "signal": {...},
    "variants": [
      {
        "model_id": "claude-opus",
        "premises": [...],
        "generated_at": "...",
        "cost_cents": 0,
        "error": null
      },
      ...
    ]
  }
  ```
- `POST /api/sketch/{sketch_id}/approve_premise` — now accepts a body: `{"model_id": "claude-opus", "premise_index": 0}`. The chosen premise becomes the sketch's canonical premise and drives the downstream stub stages (storyboard → video → critic). The leaderboard increments approved for the chosen model; it increments rejected for the other models (since they lost).
- `POST /api/sketch/{sketch_id}/reject` — unchanged, but also increments rejected for every model that contributed to the sketch.
- `GET /api/leaderboard` — returns the full leaderboard.

### UI updates (`backend/static/index.html`)

**Premise Review page — redesign:**

- Each sketch is a wide card
- Inside the card:
  - Top: signal info (title, source, URL, captured_at)
  - Below: a horizontal row of **variant sub-cards**, one per model that generated premises
  - Each variant sub-card shows: model_id label, the 3 premises (each with its own logline + tone + approve button), and a "failed" state if the adapter errored
  - Approving a single premise submits `{model_id, premise_index}` and the whole sketch moves to the next stage
- A single reject button on the parent card rejects the whole sketch

**Leaderboard widget:**

- Top-right of the nav bar (next to `+ new idea`), a small collapsible widget
- Shows: `{model_id}: {approved}/{total} ({rate}%)` per model
- Updates on action

### Tests

- `test_model_adapters.py`:
  - Each adapter's `generate()` returns a `PremiseResult` with the correct shape for stub mode
  - `is_available()` logic is correct (Claude CLI, env vars)
  - Adapters handle malformed JSON responses gracefully (return with `error` set, don't raise)
- `test_idea_factory.py`:
  - Factory runs multiple adapters on a signal
  - One failing adapter doesn't block the others
  - All adapters failing for a signal is logged and handled
  - Sketches are created with variants from every successful adapter
- `test_leaderboard.py`:
  - record_generation increments total
  - record_decision (approved=True) increments approved
  - record_decision (approved=False) increments rejected
  - get_leaderboard returns the correct shape
- `test_premise_review_api.py`:
  - GET /api/sketch/{id}/premises returns variants
  - POST approve_premise with model_id + index works, moves sketch forward
  - Leaderboard is updated by the approve call
- **One real Claude CLI integration test**, marked `@pytest.mark.llm`, that spawns `claude -p` on a tiny hardcoded signal and asserts the PremiseResult has ≥1 premise and no error. This is the only test that actually calls Claude.

### Requirements additions

- `httpx` (already there for TestClient)
- No new dependencies — OpenAI and Gemini stubs can use httpx directly without the official SDKs

---

## Demo script the subagent must run

```bash
cd /Users/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality
source .venv/bin/activate
pip install -r requirements.txt

# Quick offline tests
pytest -m "not network and not llm" -q 2>&1 | tail -5

# Run the pipeline — this will fetch real signals AND call Claude (real money, small)
python -m pipelines.run_skeleton 2>&1 | tail -20

# Inspect one of the generated sketches
SKETCH_ID=$(ls data/queues/premise-review/ | head -1 | cut -d'.' -f1 | cut -d'_' -f1)
echo "--- Sample sketch: $SKETCH_ID ---"
cat data/sketches/$SKETCH_ID/sketch.json | python -m json.tool | head -30
ls data/queues/premise-review/ | head -5

# The real Claude call integration test
pytest -m llm -v tests/test_model_adapters.py 2>&1 | tail -10

# Start the server and hit the leaderboard endpoint
uvicorn backend.main:app --port 8768 &
SERVER_PID=$!
sleep 2
echo "--- Leaderboard ---"
curl -s http://localhost:8768/api/leaderboard | python -m json.tool
echo "--- One sketch's premises ---"
curl -s http://localhost:8768/api/sketch/$SKETCH_ID/premises | python -m json.tool | head -40
kill $SERVER_PID
```

The subagent must include the actual output of this script in `phases/phase-3-report.md` — specifically the real Claude-generated premise text so we can see it worked.

---

## Out of scope for Phase 3

- Real OpenAI / Gemini API calls (stubs only; code path exists but untested by default)
- Parallel adapter execution
- Controller loop in tmux (Phase 7 polish)
- Smarter routing (tournament, budget-aware)
- Real storyboard / video / critic (Phases 4–6)
- Hetzner deployment
- Hiding model identity from the reviewer (anti-bias)

---

## Reporting

Write `phases/phase-3-report.md` with:
- File tree diff (new/changed files)
- `pytest -m "not network and not llm"` summary
- `pytest -m llm` summary (the one real Claude call)
- Demo script output — **include the actual premise text Claude generated**, we want to see real comedy
- Any deviations and why
- One paragraph on what the Premise Review page now looks like

---

## Notes for the executing subagent

- `claude -p --output-format json` is the contract — don't try to call the Anthropic SDK directly. Use the CLI subprocess pattern. `research_hub/research-radar/runner/agent-runner/lib/claude.js` is the reference for how to shell out and what the output shape looks like (lines 1–80 are the key parts).
- When the Claude CLI returns, its JSON output has the assistant's text in a field. The actual JSON payload from the model (the premises) will be **inside that text** — you'll need to parse twice: once for the CLI output envelope, once for the inner JSON.
- If the inner JSON is wrapped in markdown code fences, strip them defensively (the prompt says no fences, but models sometimes add them anyway).
- Keep the real Claude call bounded: `n_premises=3`, timeout 120s. Don't burn tokens needlessly.
- If the Claude CLI isn't available in this environment, the Phase 3 demo can't fully run — in that case, still implement everything, make the stub fallback work perfectly, and document that the real-call integration test is skipped pending CLI availability.
- Preserve the Phase 1 + Phase 2 UI. Only the Premise Review page changes, plus the leaderboard widget in the nav.
- Don't touch storyboard/video/critic — they stay as Phase 1 stubs.
- Don't break any existing tests. Total count should grow from 77 to ~95+.
