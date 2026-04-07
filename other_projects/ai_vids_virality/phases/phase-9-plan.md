# Phase 9 — OpenRouter unified LLM adapter

## Goal

Replace the per-vendor `OpenAIAdapter` and `GeminiAdapter` with a single `OpenRouterAdapter` that talks to OpenRouter's OpenAI-compatible API. One key (`OPENROUTER_API_KEY`, already in `.env`) unlocks GPT-5, Gemini 2.5 Pro, Grok, Llama, Qwen, etc. The Phase 3 stubs stay on disk as fallbacks but get demoted in `config/models.yaml` to `enabled: false`. The new adapter is added twice (once per slug), so `gpt-5` and `gemini-2.5-pro` keep their identity in the leaderboard.

This phase mirrors Phase 8's strategy: one unified adapter, multiple model slugs via config, dotenv-loaded key, mocked-HTTP test suite, opt-in real-API test marker.

---

## Files to add

### `idea_factory/adapters/openrouter.py` (NEW)

```python
"""OpenRouter adapter — OpenAI-compatible chat-completions for any OpenRouter model.

One adapter, N model slugs. Configure per-model via `config/models.yaml`:

  - id: gpt-5
    enabled: true
    adapter: idea_factory.adapters.openrouter.OpenRouterAdapter
    config:
      api_model: openai/gpt-5
      timeout_sec: 120

  - id: gemini-2.5-pro
    enabled: true
    adapter: idea_factory.adapters.openrouter.OpenRouterAdapter
    config:
      api_model: google/gemini-2.5-pro
      timeout_sec: 120

`is_available()` checks `OPENROUTER_API_KEY`. The endpoint is
`https://openrouter.ai/api/v1/chat/completions`. Auth header is
`Authorization: Bearer <key>`. The body shape is identical to OpenAI's
chat-completions, with one OpenRouter-specific addition:
`HTTP-Referer` and `X-Title` headers (recommended by OpenRouter for
free-tier rate limit grace; not required).
"""
```

The class implements `ModelAdapter`:
- `model_id` defaults to `"openrouter"` but is overridden by the `id` field passed in via `config` (the factory hands the registry id through)
- `api_model` is the OpenRouter slug (`openai/gpt-5`, `google/gemini-2.5-pro`, etc.)
- `is_available()` returns `True` iff `OPENROUTER_API_KEY` is set
- `generate(signal, prompt, n_premises)` POSTs to `/v1/chat/completions` with the same body shape as `openai_stub.py` (system + user message, `temperature: 0.7`, `response_format: {"type": "json_object"}`), parses `choices[0].message.content`, runs it through `extract_first_json_object` + `find_premise_list`, returns a `PremiseResult`
- On non-200 / network error / parse failure, sets `result.error` and returns (no exceptions bubble out)
- Optional headers: `HTTP-Referer: https://github.com/seanross237/ai_vids_virality` and `X-Title: ai_vids_virality` so OpenRouter's free-tier grace is honored (cosmetic, but free)

No deterministic stub fallback in the new adapter — if `OPENROUTER_API_KEY` is missing, return an error and let the factory move on. (The legacy `OpenAIAdapter` and `GeminiAdapter` remain on disk and still have their stub paths if anyone re-enables them.)

### `tests/test_openrouter_adapter.py` (NEW)

Mocked-HTTP suite using a fake `httpx.post`:
1. `test_is_available_when_env_set` — sets `OPENROUTER_API_KEY`, asserts `is_available() is True`
2. `test_is_available_when_env_missing` — clears env, asserts `False`
3. `test_generate_happy_path_gpt5` — fake httpx returns a 200 with a valid JSON premise list, asserts the adapter parses 3 premises and stamps `model_id` correctly
4. `test_generate_happy_path_gemini` — same, but with `api_model: google/gemini-2.5-pro` and `id: gemini-2.5-pro` — asserts `result.model_id == "gemini-2.5-pro"` (proves the per-slug identity sticks)
5. `test_generate_uses_bearer_auth` — captures the headers passed to httpx, asserts `Authorization: Bearer <key>` and the OpenRouter referer/title headers
6. `test_generate_passes_system_and_user_messages` — captures the body, asserts `messages[0].role == "system"`, `messages[1].role == "user"`, `messages[1].content == prompt`
7. `test_generate_passes_response_format_json_object` — captures the body, asserts `response_format: {"type": "json_object"}`
8. `test_generate_passes_api_model` — captures the body, asserts `model == "openai/gpt-5"` (NOT the registry id)
9. `test_generate_503_returns_error` — fake httpx returns 503, asserts `result.error` contains `"openrouter status 503"`, no exception
10. `test_generate_network_error_returns_error` — fake httpx raises `httpx.ConnectError`, asserts `result.error` contains `"openrouter request failed"`
11. `test_generate_missing_choices_returns_error` — 200 but no `choices` field, asserts `result.error` mentions `"missing choices"`
12. `test_generate_non_json_content_returns_error` — 200 with `choices[0].message.content` of `"sorry, can't help"`, asserts `result.error` mentions `"did not contain a JSON object"`
13. `test_generate_empty_premise_list_returns_error` — 200 with valid JSON object but no premises, asserts `result.error` mentions `"no premises"`
14. `test_generate_truncates_to_n_premises` — fake response has 5 premises, `n_premises=2`, asserts `len(result.premises) == 2`
15. `test_generate_stamps_signal_id_and_duration` — asserts `result.signal_id` and `result.duration_ms > 0`
16. `test_generate_when_env_missing_returns_error` — `OPENROUTER_API_KEY` not set, asserts `result.error` mentions `"OPENROUTER_API_KEY not set"` and no httpx call was made
17. **One opt-in real-API test** marked `@pytest.mark.openrouter`:
    - Skipped unless `OPENROUTER_API_KEY` is set in the env (NOT the scrubbed test env — uses a `real_openrouter_key` fixture analogous to Phase 8's `real_fal_key`)
    - Calls the real `openai/gpt-5` slug with a tiny test prompt
    - Asserts at least 1 premise comes back, no error, `duration_ms > 0`
    - On 401 / 402 (gated key) the test SKIPS with a clear message — analogous to Phase 8's pattern

Total: 16 mocked + 1 opt-in real = **17 new tests**.

### `tests/conftest.py` (CHANGED)

Add `OPENROUTER_API_KEY` to the same scrub-and-stash dance that `FAL_KEY` / `FAL_API_KEY` already have:
- Session-level pop into `_REAL_OPENROUTER_KEY`
- Autouse `_scrub_openrouter_key_per_test` fixture
- `real_openrouter_key` fixture that re-injects via `monkeypatch.setenv`

This prevents accidental real OpenRouter calls from offline tests.

### `pytest.ini` (CHANGED)

Register the new marker:
```ini
markers =
    ...existing...
    openrouter: opt-in real OpenRouter API call (requires OPENROUTER_API_KEY)
```

---

## Files to change

### `config/models.yaml` (CHANGED)

Replace the existing GPT-5 and Gemini entries:

```yaml
default_n_premises: 3
models:
  - id: claude-opus
    enabled: true
    adapter: idea_factory.adapters.claude_cli.ClaudeCLIAdapter
    config:
      cli_model: claude-opus-4-6
      timeout_sec: 180
      max_turns: 1

  - id: gpt-5
    enabled: true
    adapter: idea_factory.adapters.openrouter.OpenRouterAdapter
    config:
      api_model: openai/gpt-5
      timeout_sec: 120

  - id: gemini-2.5-pro
    enabled: true
    adapter: idea_factory.adapters.openrouter.OpenRouterAdapter
    config:
      api_model: google/gemini-2.5-pro
      timeout_sec: 120

  # Legacy stubs — kept on disk for fallback / reference, disabled by default.
  - id: gpt-5-stub
    enabled: false
    adapter: idea_factory.adapters.openai_stub.OpenAIAdapter
    config:
      api_model: gpt-5
      timeout_sec: 120

  - id: gemini-2.5-pro-stub
    enabled: false
    adapter: idea_factory.adapters.gemini_stub.GeminiAdapter
    config:
      api_model: gemini-2.5-pro
      timeout_sec: 120
```

The leaderboard keeps `gpt-5` and `gemini-2.5-pro` as the visible model ids (so historical counts continue to accumulate against the same row), but the adapter behind them is now `OpenRouterAdapter`. The renamed `gpt-5-stub` / `gemini-2.5-pro-stub` ids are new — they don't shadow existing leaderboard rows.

### `idea_factory/factory.py` (VERIFY, possibly CHANGE)

Confirm the factory passes `id` into the adapter's `config` dict (Phase 3's `OpenAIAdapter` already does this in its `__init__`: `if "id" in self.config: self.model_id = str(self.config["id"])`). If the factory does NOT pass `id`, this is a one-line fix to inject `config = {**entry.config, "id": entry.id}` before instantiation.

### `idea_factory/adapter.py` (NO CHANGE)

The ABC stays. The new adapter just implements it.

---

## Out of scope

- Routing premise generation across providers based on cost / latency (still sequential per-model rotation)
- Streaming responses (Phase 3's contract is one-shot only)
- Token-budget caps (Phase 3 doesn't track tokens; OpenRouter returns usage in the response, but we're not consuming it yet)
- Tool calling / function calling (the prompt template uses `response_format: json_object` and that's enough)
- Re-running the leaderboard against the new real models — the next signal that flows through the pipeline will populate it naturally

---

## Demo

```bash
# Offline suite — should grow from 305 → 322 (305 + 17 new)
pytest -m "not network and not llm and not gemini and not video and not critic and not publish and not fal and not openrouter"

# OpenRouter live test — uses .env via the real_openrouter_key fixture
pytest -m openrouter -v
```

Then a one-shot live demo:
```bash
# Pipe one signal through the idea factory using the real OpenRouter adapter
python -m pipelines.run_skeleton --once
# Confirm the resulting sketch.json has variants from gpt-5 and gemini-2.5-pro
# AND that they look like real model output (not the stub seeds)
cat data/sketches/sk-*/sketch.json | python -c "import json, sys; \
  s = json.load(sys.stdin); \
  print([v['model_id'] for v in s.get('variants', [])])"
```

If the OpenRouter key is gated (account doesn't have access to GPT-5 specifically, which is plausible since GPT-5 was just released), the demo should fall back gracefully: the `claude-opus` adapter still produces real premises via the local `claude -p` CLI, and the `gpt-5` / `gemini-2.5-pro` variants will have `error` set on them in `sketch.json`. The pipeline still advances.

---

## Reporting

`phases/phase-9-report.md` with:
- File tree (new files + changed files)
- Pytest summaries (offline 322 passed; openrouter live test result — pass or skip-with-reason)
- One real OpenRouter response in `raw_response` form, copy-pasted, to prove the live path works
- Per-model coverage table: `openai/gpt-5` and `google/gemini-2.5-pro` with verification source
- Any deviations from this plan (e.g., if the GPT-5 slug returns 404 because OpenRouter still calls it `openai/gpt-4o`, document the fallback)
- Final paragraph: "what changes for the user"

---

## What changes for the user (preview)

After Phase 9, the `OPENROUTER_API_KEY` already in `.env` unlocks GPT-5 and Gemini 2.5 Pro for premise generation through one unified adapter. The leaderboard will start populating with real model output instead of the deterministic Phase 3 stubs, so when the user lands on Premise Review they'll see meaningfully different premises from each model. Combined with Phase 8 (fal for video + storyboard) and the existing Claude CLI adapter, the user is now down to **two API keys total** (`FAL_KEY` and `OPENROUTER_API_KEY`) to run the entire pipeline end-to-end with real models at every stage.
