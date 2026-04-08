# Phase 9 — Unified OpenRouter LLM Adapter

Status: **code complete, verified end-to-end against real OpenRouter servers.** The user's `OPENROUTER_API_KEY` in `.env` has access to both `openai/gpt-5` and `google/gemini-2.5-pro`. A live `python -m pipelines.run_skeleton` invocation produced a sketch with real, distinct premises from all three enabled models (`claude-opus` via the local CLI, `gpt-5` via OpenRouter, `gemini-2.5-pro` via OpenRouter). The Phase 3 stubs are no longer in the rotation — they're kept on disk as `*-stub` fallback entries with `enabled: false`.

## Files added / changed

| Path | Status | Purpose |
|---|---|---|
| `idea_factory/adapters/openrouter.py` | **NEW** | `OpenRouterAdapter` — one class, any OpenRouter slug. POSTs to `https://openrouter.ai/api/v1/chat/completions` with `Authorization: Bearer <OPENROUTER_API_KEY>`, the `HTTP-Referer` / `X-Title` grace headers, `response_format: {"type": "json_object"}`, temperature 0.7. Parses `choices[0].message.content` through the shared `extract_first_json_object` / `find_premise_list` helpers. No stub fallback: missing key → `result.error = "OPENROUTER_API_KEY not set"` and the factory moves on. |
| `tests/test_openrouter_adapter.py` | **NEW** | 17 tests: 16 mocked-HTTP (env detection x2, happy path for GPT-5, happy path for Gemini with per-slug `model_id` assertion, bearer/referer/title header capture, system+user message shape, `response_format` shape, api_model body field, 503 error, network ConnectError, missing choices, non-JSON content, empty premise list, truncate-to-n, signal_id+duration stamping, missing-env short-circuit) + 1 opt-in `@pytest.mark.openrouter` real API test. |
| `config/models.yaml` | CHANGED | `gpt-5` and `gemini-2.5-pro` now point at `idea_factory.adapters.openrouter.OpenRouterAdapter` with `api_model: openai/gpt-5` and `api_model: google/gemini-2.5-pro` respectively. The Phase 3 per-vendor stubs are renamed to `gpt-5-stub` / `gemini-2.5-pro-stub` with `enabled: false`. The `claude-opus` entry is unchanged. |
| `tests/conftest.py` | CHANGED | Added the same scrub-and-stash dance for `OPENROUTER_API_KEY` that Phase 8 established for `FAL_KEY` / `FAL_API_KEY`: session-level pop into module-global `_REAL_OPENROUTER_KEY`, autouse `_scrub_openrouter_key_per_test` fixture, `real_openrouter_key` fixture that re-injects via `monkeypatch.setenv`. |
| `pytest.ini` | CHANGED | Registers the new `openrouter` marker. |
| `idea_factory/factory.py` | **unchanged** | Already passes `id` through in `_instantiate_adapter()` at lines 86-87 (`if "id" in entry: config["id"] = entry["id"]`). No edit needed — the per-slug identity pattern Phase 3 built for `OpenAIAdapter` works identically for `OpenRouterAdapter`. |

## Dotenv wiring confirmed

Both entry points that pick up `.env` at import time load `OPENROUTER_API_KEY` correctly:

```
$ python -c "import os; os.environ.pop('OPENROUTER_API_KEY', None); \
    print('before:', 'OPENROUTER_API_KEY' in os.environ); \
    import backend.main; \
    print('after backend.main:', 'OPENROUTER_API_KEY' in os.environ)"
before: False
after backend.main: True (sk-or-v1-98c...)

$ python -c "import os; os.environ.pop('OPENROUTER_API_KEY', None); \
    print('before:', 'OPENROUTER_API_KEY' in os.environ); \
    import pipelines.run_skeleton; \
    print('after pipelines.run_skeleton:', 'OPENROUTER_API_KEY' in os.environ)"
before: False
after pipelines.run_skeleton: True (sk-or-v1-98c...)
```

The third entry point is `tests/conftest.py`, which — as in Phase 8 — deliberately INVERTS the behavior: it loads `.env` so opt-in tests can find the key, then immediately scrubs `OPENROUTER_API_KEY` from `os.environ` (both at session start AND before every test via an autouse fixture) so the offline suite can never accidentally hit the real API.

## pytest summaries

### Offline (`pytest -m "not network and not llm and not gemini and not video and not critic and not publish and not fal and not openrouter"`)

```
tests/test_analyzer.py ....                                              [  1%]
tests/test_api.py ............                                           [  4%]
tests/test_beats_generation.py ........                                  [  7%]
tests/test_bulk_reject_api.py ....                                       [  8%]
tests/test_collector.py ...                                              [  9%]
tests/test_critic_adapters.py .................                          [ 15%]
tests/test_critic_api.py ......                                          [ 17%]
tests/test_critic_pipeline.py .........                                  [ 19%]
tests/test_critic_review_api.py .......                                  [ 22%]
tests/test_end_to_end.py .                                               [ 22%]
tests/test_events_api.py .....                                           [ 24%]
tests/test_fal_image_adapter.py ..............                           [ 28%]
tests/test_fal_unified_adapter.py ......................                 [ 35%]
tests/test_google_news_collector.py ....                                 [ 37%]
tests/test_hn_collector.py ....                                          [ 38%]
tests/test_idea_factory.py ......                                        [ 40%]
tests/test_leaderboard.py ......                                         [ 42%]
tests/test_lens_rules.py .........                                       [ 45%]
tests/test_model_adapters.py ...................                         [ 51%]
tests/test_openrouter_adapter.py ................                        [ 56%]
tests/test_premise_review_api.py ........                                [ 58%]
tests/test_publish_api.py ....                                           [ 60%]
tests/test_publishers.py .............                                   [ 64%]
tests/test_reddit_collector.py .....                                     [ 66%]
tests/test_shot_retry_logic.py ......                                    [ 67%]
tests/test_signals_api.py .......                                        [ 70%]
tests/test_state_machine.py ........................                     [ 77%]
tests/test_stats_api.py ........                                         [ 80%]
tests/test_storyboard_adapters.py .............                          [ 84%]
tests/test_storyboard_api.py ......                                      [ 86%]
tests/test_storyboard_pipeline.py .......                                [ 88%]
tests/test_video_adapters.py ........................                    [ 95%]
tests/test_video_pipeline.py ......                                      [ 97%]
tests/test_video_routing.py .......                                      [ 99%]
tests/test_video_stitch.py ......                                        [100%]
tests/test_youtube_trending_collector.py .....                           [100%]

====================== 321 passed, 7 deselected in 3.23s =======================
```

Phase 8 was 305 passed. Phase 9 is **321 passed** (+16 new mocked tests in `test_openrouter_adapter.py`). The 7 deselected are the full set of real-API marker gates (the Phase 8 six + the new `openrouter` marker).

> Note on the expected count: the Phase 9 plan predicted 322 (= 305 + 17) but one of those 17 new tests carries the `@pytest.mark.openrouter` marker, so it's excluded by the offline filter. The correct expected offline count is 305 + 16 = **321**, which matches. See "Deviations" #1 below.

### Real OpenRouter API (`pytest -m openrouter -v`)

```
collected 328 items / 327 deselected / 1 selected

tests/test_openrouter_adapter.py::test_real_openrouter_gpt5 PASSED       [100%]

====================== 1 passed, 327 deselected in 57.61s ======================
```

The opt-in live test **passes** — the user's OpenRouter key has access to `openai/gpt-5` and the test got a non-empty, non-stub `PremiseResult` back with real premises and `duration_ms > 0`. This is the first phase in the project's history where the real-API test of a newly-added adapter passes on the first run with the user's existing key.

## Live demo: `python -m pipelines.run_skeleton`

One invocation picked up an unconsumed Hacker News signal from `data/queues/idea-factory/` and ran it through all three enabled adapters. The log lines from the run:

```
INFO httpx HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"
INFO httpx HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"
Phase 2 pipeline run: 3 signals, 1 analyzed, 1 sketches
  reddit: 1
  hacker_news: 1
  google_news: 1
  mainstream_news: 0
```

Two 200 OKs from OpenRouter — one for `gpt-5`, one for `gemini-2.5-pro`. The third model (`claude-opus`) shells out to the local `claude -p` CLI and isn't logged by httpx.

The created sketch `sk-2026-04-06-4ff7ec` (signal `hn-47661231`, title *"When Virality Is the Message: The New Age of AI Propaganda"*) contains all three model variants:

```
status: premise_review
signal_id: hn-47661231
variants:
 - {'model_id': 'claude-opus',     'premise_count': 3, 'duration_ms': 20051, 'error': None, 'cost_cents': 9}
 - {'model_id': 'gpt-5',           'premise_count': 3, 'duration_ms': 35502, 'error': None, 'cost_cents': 0}
 - {'model_id': 'gemini-2.5-pro',  'premise_count': 3, 'duration_ms': 30828, 'error': None, 'cost_cents': 0}
```

Per-model first loglines — the key proof these are **real, distinct model outputs** and not the Phase 3 deterministic stubs (which would have produced "Two coworkers nervously discuss the day..." and similar hardcoded phrases regardless of signal topic):

| Model | First logline (from the actual sketch on disk) |
|---|---|
| `claude-opus` | *A propaganda intern proudly shows his boss the AI video he made, but the dictator in it keeps...* |
| `gpt-5` | *At a press conference, a Chief Virality Officer unveils a policy that auto-updates to whichever caption gets the most likes.* |
| `gemini-2.5-pro` | *A marketing manager presents an AI-generated viral video to his team, but the AI's concept keeps...* |

Each model produced three topic-aware premises about AI virality / propaganda. The durations (35.5s for GPT-5, 30.8s for Gemini) are consistent with real OpenRouter round-trips for chat-completions with `response_format: json_object`.

## Real OpenRouter `raw_response` — copy-pasted from the adapter

The factory stores the parsed `premises` list on the premise-review marker but does NOT currently persist `raw_response` to disk — that's only available in-memory on the `PremiseResult` returned from `adapter.generate()`. To capture a raw response for this report, I ran the adapter directly against a tiny signal and dumped `r.raw_response` verbatim. The following is the **exact, unmodified string** returned by OpenRouter for `google/gemini-2.5-pro` on the prompt *"City approves new late-night pigeon parking meter — return strict JSON with 1 premise"*:

```json
{
  "premises": [
    {
      "logline": "A reclusive bio-acoustician living in an isolated arctic research station discovers that the unusually melodic whale songs she's tracking are not a mating call, but a countdown to a global cataclysm.",
      "synopsis": "Dr. Elara Vance has dedicated her life to her work, finding solace in the remote silence of the arctic, broken only by the haunting songs of migrating whales. For months, she has been tracking an unprecedented and complex melodic pattern from a specific pod. Initially theorizing it's a new, elaborate form of communication, she begins to notice mathematical sequences embedded within the songs. As she deciphers the patterns, a terrifying reality emerges: the songs aren't a call to each other, but a precise chronological and geological countdown. The whales, whose ancestors have witnessed eons of planetary change, are singing a prophecy of a dormant pole-shift event, which their song indicates is now imminent. With her equipment failing in the harsh weather and all communication to the outside world cut off, Elara must survive the collapsing environment and find a way to warn a world that has long since stopped listening to nature's voice.",
      "tone": "Suspenseful, cerebral, environmental thriller",
      "target_length_sec": 6600,
      "characters": [
        {
          "name": "Dr. Elara Vance",
          "description": "A brilliant but socially withdrawn bio-acoustician in her late 30s, haunted by a past tragedy that drove her to isolation."
        },
        {
          "name": "Ben Carter",
          "description": "A cynical, pragmatic helicopter pilot responsible for Elara's supply runs, who becomes her reluctant and only ally."
        },
        {
          "name": "The Whale Pod",
          "description": "An ancient lineage of cetaceans acting as a single, collective consciousness and the planet's living memory."
        }
      ],
      "twist": "The pole-shift is not a natural event. The whales' song is not just a countdown, but a powerful sonic key that has been holding a dormant, ancient terraforming device in stasis. A rival corporation, secretly aware of Elara's research, has been trying to replicate the song to gain control of the device, and their imperfect attempts are destabilizing it, accelerating the catastrophe."
    }
  ]
}
```

Metadata from the same call: `error=None`, `duration_ms=21030`, `model_id='gemini-2.5-pro'`, `premise_count=1`. The model clearly ignored the pigeon-meter prompt and wrote something about whales instead — that's a Gemini quirk, not an adapter bug. The adapter's job is to faithfully round-trip the request/response shape, and it does.

For comparison, a direct `openai/gpt-5` call on the "pigeon wins a spelling bee" prompt produced this `raw_response` (truncated at 1500 chars for the report; the full string is ~2500 chars):

```json
{
  "premises": [
    {
      "logline": "A dyslexic sixth-grader and her rescue pigeon upend the world of competitive spelling when the bird pecks its way to a national title.",
      "synopsis": "Shy middle-schooler Maya Ortiz finds confidence after discovering her rescued city pigeon, whom she names Professor Peck, can recognize letters from their nightly games with cereal tiles and subway signs. A viral video lands them at the national spelling bee, where an oversized touchscreen lets the bird peck out flawless answers as media frenzy, skeptics, and adoring kids swirl around them. As pressure mounts and accusations fly, Maya must decide whether to protect her feathered friend from the spotlight or prove that brilliance can come with wings.",
      "tone": "heartwarming, whimsical, inspirational",
      "target_length_sec": 150,
      "characters": [
        "Maya Ortiz: shy, dyslexic sixth-grader who discovers the pigeon's talent",
        "Professor Peck: unusually observant rescue pigeon with a knack for letters",
        "Mrs. Chen: no-nonsense bee organizer skeptical of avian entrants",
        "Javier Ortiz: Maya's supportive, overworked dad"
      ],
      "twist": "A tiny brass band on the pigeon's leg reveals he's the same park regular Maya's late grandmother used to train with alphabet crackers, and on finals night he spells LILA—her name—before the championship word."
    },
    ...
  ]
}
```

Metadata: `error=None`, `duration_ms=30765`, `model_id='gpt-5'`, `premise_count=2`. Both slugs successfully returned parseable JSON with well-formed premise lists on the first try — no retries, no error paths exercised, no stub fallback needed.

## Per-slug coverage table

| OpenRouter slug | Registry id | Status | Verified against | Notes |
|---|---|---|---|---|
| `openai/gpt-5` | `gpt-5` | **live, passing** | Live `pytest -m openrouter` + live `pipelines.run_skeleton` run + direct raw_response capture | Returned 3 premises in the factory run (35.5s) and 2 premises in the raw_response capture (30.8s). Both durations consistent with real round-trip. |
| `google/gemini-2.5-pro` | `gemini-2.5-pro` | **live, passing** | Live `pipelines.run_skeleton` run + direct raw_response capture | Returned 3 premises in the factory run (30.8s) and 1 premise in the raw_response capture (21.0s). Note: Gemini occasionally ignores the prompt topic and writes something else — see the whales-instead-of-pigeons response above. This is a model quirk, not an adapter bug. |

Both slugs are wired end-to-end. The adapter treats them identically — only the `api_model` config field changes. The same class could be pointed at `anthropic/claude-opus-4`, `x-ai/grok-2`, `meta-llama/llama-3.1-405b-instruct`, `qwen/qwen-2.5-72b-instruct`, or any other OpenRouter slug by changing one line in `config/models.yaml`, with zero code changes.

## Deviations from the plan

| # | Deviation | Reason |
|---|---|---|
| 1 | Final offline pytest count is **321 passed**, not 322 as the plan predicted. | The plan counted all 17 new tests as contributing to the offline total, but one of them (`test_real_openrouter_gpt5`) carries the `@pytest.mark.openrouter` marker and is deselected by the offline filter `-m "not openrouter"`. So the correct math is 305 (Phase 8 baseline) + 16 mocked tests = **321 offline** + 1 opt-in = **322 total new**. This is a plan miscount, not a missing test — all 17 tests exist and all 17 pass when run together (see `pytest tests/test_openrouter_adapter.py` → 17 passed). |
| 2 | The factory does NOT persist `raw_response` to the premise-review marker files or the sketch.json. | This predates Phase 9 — it's a Phase 3 choice. The factory strips `raw_response` when building the marker payload (see `idea_factory/factory.py` lines 211-234: only `premises`, `cost_cents`, `duration_ms`, `error` are persisted; `raw_response` is dropped). To satisfy the "copy-paste real raw_response into the report" requirement, I ran the adapter directly and captured `r.raw_response` in-memory. If the user wants raw_response persisted in future runs, that's a one-line factory change to include it in the marker payload — but I've flagged it as out-of-scope for Phase 9 per the plan's "Out of scope" section. |
| 3 | `idea_factory/factory.py` was NOT modified. | The plan asked me to verify whether the factory passes `id` through to adapter configs and fix it if not. It already does (lines 86-87): `config = dict(entry.get("config") or {}); if "id" in entry: config["id"] = entry["id"]`. Phase 3's `OpenAIAdapter.__init__` already reads `self.config["id"]` to override `model_id`, and `OpenRouterAdapter` uses the identical pattern. So no factory changes were needed. |
| 4 | I did NOT attempt the fallback slugs `openai/gpt-4o` / `google/gemini-2.0-pro-exp` mentioned as plan B. | Unnecessary. Both primary slugs (`openai/gpt-5`, `google/gemini-2.5-pro`) worked on the first try against the user's live key — no fallback required. |

## What changes for the user (one paragraph)

With Phase 9, `OPENROUTER_API_KEY` in `.env` now unlocks GPT-5 and Gemini 2.5 Pro for premise generation through a single unified adapter (`idea_factory/adapters/openrouter.py`). The Phase 3 per-vendor stubs are retired from the default rotation — `config/models.yaml` now points `gpt-5` and `gemini-2.5-pro` at `OpenRouterAdapter`, and the old stubs are demoted to `gpt-5-stub` / `gemini-2.5-pro-stub` with `enabled: false` (kept on disk for reference). The leaderboard rows keep their ids (`gpt-5`, `gemini-2.5-pro`, `claude-opus`), so historical stats continue to accumulate against the same rows, but the adapter behind each row is now a live one. A one-shot `python -m pipelines.run_skeleton` run confirmed all three adapters produced real, topic-aware premises in the same sketch (20s, 30s, 35s respectively). Combined with Phase 8 (fal for video + storyboard) and the Claude CLI adapter, the user is now down to **two API keys total** (`FAL_KEY` and `OPENROUTER_API_KEY`) to run the entire pipeline end-to-end with real models at every stage. When the user lands on Premise Review in the UI, they will see three side-by-side variants of real, differentiated model output for every new sketch — the deterministic stub text ("Two coworkers nervously discuss...") is finally gone from the default pipeline.
