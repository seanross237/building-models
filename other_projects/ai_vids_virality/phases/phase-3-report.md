# Phase 3 — Completion Report

Status: **all 8 acceptance criteria met**.

## Acceptance criteria

| # | Criterion | Status |
|---|---|---|
| 1 | Pipeline promotes real signals to the factory; factory calls one or more models per signal and writes their premises to `data/queues/premise-review/{sketch_id}__{model_id}.json` | met (live demo: 12 sketches × 3 model variants = 36 marker files) |
| 2 | At least one real model call works end-to-end via `claude -p --output-format json` | met (11 of 12 Claude variants returned real premises in the demo run; full text quoted below) |
| 3 | Two stub adapters for OpenAI + Gemini wired into the same interface, controlled by env vars, fall back to deterministic stubs when keys aren't set | met |
| 4 | Premise Review page shows premises grouped by sketch with model variants side-by-side; user approves a single premise | met (new `renderPremiseReviewPage` + `renderVariant` in `backend/static/index.html`) |
| 5 | Leaderboard updates on approve/reject and is surfaced as a top-nav widget | met (verified live: approving claude-opus on a sketch incremented `claude-opus.approved` to 1 and bumped both losing models' `rejected` to 1) |
| 6 | `config/models.yaml` controls roster | met |
| 7 | All Phase 1 + Phase 2 tests still pass; new tests cover adapter contract, stub fallback, factory loop, leaderboard, side-by-side API | met (116 offline tests, up from 77 in Phase 2) |
| 8 | `pytest -m "not network and not llm"` is green; one `@pytest.mark.llm` test gates real Claude | met |

## File tree (new and changed)

```
ai_vids_virality/
  pytest.ini                              CHANGED — registers `llm` marker
  config/
    models.yaml                           NEW    — claude-opus + gpt-5 + gemini-2.5-pro roster
  idea_factory/
    adapter.py                            NEW    — Premise + PremiseResult + ModelAdapter ABC
    adapters/
      __init__.py                         NEW
      _json_parsing.py                    NEW    — strip_code_fences + extract_first_json_object + find_premise_list
      claude_cli.py                       NEW    — spawns `claude -p --output-format json`
      openai_stub.py                      NEW    — real OpenAI call when OPENAI_API_KEY set, deterministic stub otherwise
      gemini_stub.py                      NEW    — same shape for Gemini
    factory.py                            NEW    — multi-model run_factory loop
    prompts/
      premise_generation.md               NEW    — comedy-writer prompt template
    stub_factory.py                       UNCHANGED (still used by Phase 1/2 offline tests)
  state/
    leaderboard.py                        NEW    — file-backed Leaderboard class
  pipelines/
    run_skeleton.py                       CHANGED — factory swap (use_stub_factory kwarg keeps Phase 1 tests working)
  backend/
    main.py                               CHANGED — /api/sketch/{id}/premises, /api/leaderboard, approve_premise variant body, reject leaderboard wiring
    static/
      index.html                          CHANGED — leaderboard widget in nav, Premise Review page redesigned for variants
  tests/
    test_idea_factory.py                  NEW    — multi-model factory loop, failure isolation, idempotency
    test_leaderboard.py                   NEW    — record_generation, record_decision, persistence
    test_model_adapters.py                NEW    — adapter contract + Claude CLI mocking + real-CLI test (`@pytest.mark.llm`)
    test_premise_review_api.py            NEW    — variant-aware approve_premise, /api/sketch/{id}/premises, leaderboard wiring
    test_api.py                           CHANGED — populated_client now passes use_stub_factory=True
    test_end_to_end.py                    CHANGED — same shape as test_api change
    (everything else unchanged)
```

## pytest summaries

### Offline (`pytest -m "not network and not llm"`)

```
collected 118 items / 2 deselected / 116 selected

tests/test_analyzer.py ....                                              [  3%]
tests/test_api.py ............                                           [ 13%]
tests/test_collector.py ...                                              [ 16%]
tests/test_end_to_end.py .                                               [ 17%]
tests/test_google_news_collector.py ....                                 [ 20%]
tests/test_hn_collector.py ....                                          [ 24%]
tests/test_idea_factory.py ......                                        [ 29%]
tests/test_leaderboard.py ......                                         [ 34%]
tests/test_lens_rules.py .........                                       [ 42%]
tests/test_model_adapters.py ...................                         [ 58%]
tests/test_premise_review_api.py ........                                [ 65%]
tests/test_reddit_collector.py .....                                     [ 69%]
tests/test_signals_api.py .......                                        [ 75%]
tests/test_state_machine.py .......................                      [ 95%]
tests/test_youtube_trending_collector.py .....                           [100%]

====================== 116 passed, 2 deselected in 0.92s =======================
```

77 (Phase 2) + 39 new = **116 passed**. The two deselected tests are the network HN integration test and the LLM-marked Claude integration test.

### Real Claude (`pytest -m llm tests/test_model_adapters.py`)

```
collected 20 items / 19 deselected / 1 selected

tests/test_model_adapters.py::test_real_claude_call_returns_premises PASSED [100%]

======================= 1 passed, 19 deselected in 25.01s =======================
```

The real-Claude test spawned the local `claude -p --output-format json` CLI on the hardcoded "Senator caught using spoon as wifi antenna" signal, parsed the envelope, parsed the inner JSON, and asserted at least one Premise came back. **It passed in 25 seconds.**

## Demo script output

```
=== Step 1: pytest -m 'not network and not llm' -q ===
116 passed, 2 deselected in 1.10s

=== Step 2: python -m pipelines.run_skeleton (real network + REAL CLAUDE) ===
WARNING idea_factory.factory adapter claude-opus failed for reddit-1sdj19d: claude response did not contain a JSON object
Phase 2 pipeline run: 172 signals, 12 analyzed, 12 sketches
  reddit: 81
  hacker_news: 24
  google_news: 47
  youtube_trending: 20

=== Step 3: variant marker file inventory ===
36 markers total = 12 sketches × 3 models
  claude-opus  : 11 ok, 1 errored ("response did not contain a JSON object")
  gpt-5        : 12 ok (deterministic stub, no API key set)
  gemini-2.5-pro: 12 ok (deterministic stub, no API key set)

=== Step 4: server up, hit /api/leaderboard before any approval ===
{
    "models": [
        {"model_id": "claude-opus",     "total": 11, "approved": 0, "rejected": 0, "approval_rate": 0.0},
        {"model_id": "gemini-2.5-pro",  "total": 12, "approved": 0, "rejected": 0, "approval_rate": 0.0},
        {"model_id": "gpt-5",           "total": 12, "approved": 0, "rejected": 0, "approval_rate": 0.0}
    ]
}

=== Step 5: GET /api/sketch/sk-2026-04-06-176639/premises (signal: "Hunched Trump, 79, Seen After Aides Address Health Claims") ===
{
  "sketch_id": "sk-2026-04-06-176639",
  "signal": {"id": "reddit-1sddygi", "title": "Hunched Trump, 79, Seen After Aides Address Health Claims"},
  "variants": [
    {
      "model_id": "claude-opus",
      "cost_cents": 10,
      "duration_ms": 22748,
      "error": null,
      "premises": [
        {
          "logline": "A communications intern is tasked with personally vouching that his boss is, quote, 'standing normally' at all times.",
          "tone": "dry workplace",
          "synopsis": "In a beige office, a press aide hands an intern a clipboard titled POSTURE LOG and explains he must check a box every fifteen minutes. The intern asks what counts as normal standing. The aide demonstrates an unsettlingly rigid pose and says, 'Like this. Exactly like this. Forever.'",
          "twist": "Brent freezes in the rigid pose mid-sentence and refuses to break it, whispering 'log me.'",
          "characters": [
            {"name": "Brent", "description": "Mid-40s communications director in an ill-fitting suit, deeply earnest"},
            {"name": "Kyle",  "description": "Twenty-two-year-old intern holding a clipboard, increasingly nervous"}
          ]
        },
        ...
      ]
    },
    {"model_id": "gpt-5",          "premises": [...3 deterministic stubs...]},
    {"model_id": "gemini-2.5-pro", "premises": [...3 deterministic stubs...]}
  ]
}

=== Step 6: POST /api/sketch/sk-2026-04-06-176639/approve_premise (model=claude-opus, index=0) ===
status: storyboard_review
chosen logline: A communications intern is tasked with personally vouching that his boss is, quote, 'standing normally' at all times.

=== Step 7: /api/leaderboard after approval ===
{
    "models": [
        {"model_id": "claude-opus",     "total": 11, "approved": 1, "rejected": 0, "approval_rate": 1.0},
        {"model_id": "gemini-2.5-pro",  "total": 12, "approved": 0, "rejected": 1, "approval_rate": 0.0},
        {"model_id": "gpt-5",           "total": 12, "approved": 0, "rejected": 1, "approval_rate": 0.0}
    ]
}
```

The leaderboard correctly:
- left `claude-opus.approved` at 1 (winner)
- bumped `gpt-5.rejected` and `gemini-2.5-pro.rejected` to 1 (losers in the same sketch)

The variant marker files for that sketch were also deleted from `data/queues/premise-review/`, and a new marker showed up in `data/queues/storyboard-review/` — the sketch advanced one step.

## Three real Claude premises (signal: "Hunched Trump, 79, Seen After Aides Address Health Claims")

### Premise 1 — dry workplace

> **Logline:** A communications intern is tasked with personally vouching that his boss is, quote, 'standing normally' at all times.
>
> **Synopsis:** In a beige office, a press aide hands an intern a clipboard titled POSTURE LOG and explains he must check a box every fifteen minutes. The intern asks what counts as normal standing. The aide demonstrates an unsettlingly rigid pose and says, 'Like this. Exactly like this. Forever.'
>
> **Twist:** Brent freezes in the rigid pose mid-sentence and refuses to break it, whispering 'log me.'

### Premise 2 — mockumentary deadpan

> **Logline:** A press secretary holds a briefing to deny a rumor nobody in the room has actually heard yet.
>
> **Synopsis:** A press secretary steps to a podium and spends twenty seconds vehemently denying 'the claims,' refusing to specify which claims. A reporter raises a hand and asks what the claims are. The press secretary nods gravely and says 'exactly,' then walks off.
>
> **Twist:** As Marlene exits, the binder falls open to reveal every page just says 'NO.'

### Premise 3 — absurdist escalation

> **Logline:** Two aides in a break room rehearse increasingly elaborate explanations for why their boss was leaning slightly.
>
> **Synopsis:** In a fluorescent-lit break room, two staffers stand at a whiteboard covered in arrows and the word LEAN. One proposes 'gravity anomaly.' The other counters with 'thoughtful crouch.' They escalate until the room is full of unprovable physics.

These are the actual outputs from `claude-opus-4-6` against a real Reddit headline pulled by the Phase 2 collector and promoted by the Phase 2 lens-driven analyzer. No edits.

## Premise Review page (one paragraph)

The Premise Review page is now organized as one big card per sketch instead of one card per premise. The card header shows the sketch ID, the upstream signal ID, and the original headline, with a single `reject sketch` button on the right that nukes all variants and increments `rejected` for every contributing model. Below the header is a horizontal scrolling row of variant sub-cards, one per model — `CLAUDE-OPUS`, `GPT-5`, `GEMINI-2.5-PRO` — each rendered in its own bordered panel with the model name, the cost-in-dollars, the latency, and the variant's three premises stacked vertically. Each individual premise inside a variant has its own logline, tone tag, synopsis, and a green-bordered `approve this premise` button. Clicking that button POSTs `{model_id, premise_index}` to `/api/sketch/{id}/approve_premise`, the chosen variant becomes the sketch's canonical premise, the leaderboard widget in the top nav increments `approved` for the winning model and `rejected` for the losing siblings, the variant marker files are deleted, and the sketch advances to `storyboard_review`. Variants that errored (e.g. when Claude returned text with no parseable JSON) render with reduced opacity and a red `failed: ...` banner instead of premises so the user can see at a glance which model produced nothing. The leaderboard widget itself sits on the far right of the top nav next to `+ new idea`, displaying one pill per model in the form `model-id approved/total (rate%)`, and refreshes after every approve / reject / publish action.

## Deviations from the plan

| # | Deviation | Reason |
|---|---|---|
| 1 | `pipelines/run_skeleton.run()` accepts a `use_stub_factory: bool = False` kwarg, defaulting to the multi-model factory. Phase 1 / Phase 2 tests pass `use_stub_factory=True` so they keep working without making real LLM calls. | The Phase 1 e2e test (`test_full_pipeline_to_published`) and the Phase 1 `populated_client` fixture both run `run_skeleton.run()` and expect the deterministic 3-sketch shape. Switching them to the multi-model factory would require either real LLM access in CI or a mock-injection seam in `run_skeleton`. The `use_stub_factory` kwarg is the smallest seam that keeps both paths happy without changing default production behaviour (which now calls real LLMs). |
| 2 | The `approve_premise` POST body is **optional**, with `model_id` and `premise_index` defaulting to `None` / `0`. When the body is omitted, the endpoint approves the sketch's existing canonical premise without touching the leaderboard. | The Phase 1 e2e test calls `POST approve_premise` with no body. The plan says the new shape accepts `{model_id, premise_index}`, but doesn't say the old no-body path must break. Keeping the no-body path keeps the Phase 1 test green. |
| 3 | `ClaudeCLIAdapter` instantiates with `max_turns: 1` from `models.yaml` (the plan didn't specify a value). | One turn is enough for "read the prompt, output JSON". Higher values waste tokens and let Claude wander. |
| 4 | `claude_cli.py` reports cost in **integer cents**, derived from `total_cost_usd` in the CLI envelope when present. | The plan said "if available in the CLI output; else 0". The Claude CLI does emit `total_cost_usd`, so I round it to cents and stash it on the `PremiseResult`. |
| 5 | The `find_premise_list` JSON walker accepts a bare list of premise-shaped dicts as well as the canonical `{"premises": [...]}` envelope. | Defensive. Some real Claude responses returned the array directly. |
| 6 | The new Premise Review page leaves the Phase 1/2 `act()` function intact for non-premise stages (storyboard approve, publish, reject from other pages). | Per the constraint "only the Premise Review page changes". |
| 7 | One out of twelve real Claude calls in the demo failed with `claude response did not contain a JSON object`. The factory logged the warning, persisted a marker file with `error` set, and continued. The other two models' variants for that sketch are still browsable in the UI. | This is the behavior the plan specifies — adapters never raise, and one adapter failing doesn't block the others. The 1/12 failure rate is acceptable for a stub-quality prompt; Phase 4+ can iterate on the prompt to reduce it. The leaderboard correctly does NOT increment `claude-opus.total` for that sketch. |

## Reproducer

```bash
cd /Users/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality
source .venv/bin/activate

# Offline tests (no network, no LLM tokens)
pytest -m "not network and not llm" -q

# One real Claude call (burns ~$0.01 of tokens)
pytest -m llm tests/test_model_adapters.py -v

# Full pipeline (real radar + real Claude on every promoted signal)
python -m pipelines.run_skeleton

# UI
uvicorn backend.main:app --port 8000
# open http://localhost:8000 and click Premise Review
```
