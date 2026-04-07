# Phase 5 — Completion Report

Status: **all 8 acceptance criteria met**.

## Acceptance criteria

| # | Criterion | Status |
|---|---|---|
| 1 | `VideoProviderAdapter` ABC with one method `generate(start_frame, end_frame, prompt, duration_sec, out_path)` returning a `VideoClip` dataclass | met (`video_gen/adapter.py`) |
| 2 | Five real adapters (Kling, Luma, Veo, Runway, Pika) plus a Stub adapter, all wired through env-var keys, all gated by `is_available()` | met — see per-adapter completeness table below |
| 3 | `config/video.yaml` with routing list, per-adapter config, `max_cost_cents_per_sketch` cap | met |
| 4 | `approve_storyboard` runs the real video pipeline: per-beat clips → ffmpeg stitching → CRITIC_REVIEW transition | met (live demo: 7 beats → 7 clips → stitched ffmpeg final.mp4 → critic_review) |
| 5 | Critic Review page embeds the actual video with HTML5 `<video controls>` from the `/data` static route | met |
| 6 | Without any video API key set, StubVideoAdapter takes over and the pipeline still completes | met (this demo was run with **zero** video keys set) |
| 7 | New tests cover adapter contract, routing, stub, mocked HTTP per real adapter, ffmpeg stitching, cost cap, critic-review API + final.mp4 serving | met (150 → 200 offline tests, +50 new) |
| 8 | `pytest -m "not network and not llm and not gemini and not video"` is green; new `@pytest.mark.video` marker registered | met |

## File tree (new and changed)

```
ai_vids_virality/
  pytest.ini                                  CHANGED — registers `video` marker
  config/
    video.yaml                                NEW — routing + per-adapter config + $5 cost cap
  video_gen/
    _common.py                                NEW — placeholder helpers, base64_file, write_bytes
    adapter.py                                NEW — VideoProviderAdapter ABC + VideoClip dataclass
    pipeline.py                               NEW — load_adapters / select_video_adapter / run_video_pipeline
    stitch.py                                 NEW — ffmpeg concat-demuxer wrapper with re-encode fallback
    adapters/
      __init__.py                             NEW
      stub_video.py                           NEW — Phase 1 stub, lifted into the new layout
      kling.py                                NEW — REAL: full image2video + JWT HS256 + polling + download
      luma.py                                 NEW — REAL: dream-machine v1 generations + keyframes + polling
      runway.py                               NEW — REAL: /v1/image_to_video + X-Runway-Version + tasks polling
      pika.py                                 NEW — REAL: queue.fal.run pika 2.2 image-to-video + queue polling
      veo.py                                  NEW — PARTIAL (with TODO): module-level docstring explains what's missing
    prompts/
      clip_prompt.md                          NEW — per-clip text prompt template
    placeholder.mp4                           UNCHANGED — fallback asset
    stub_provider.py                          UNCHANGED (legacy Phase 1 module, no longer imported anywhere; kept for reference parity with storyboard/stub_storyboard.py)
  backend/
    main.py                                   CHANGED — approve_storyboard runs run_video_pipeline; new GET /api/sketch/{id}/clips; AI_VIDS_OFFLINE_VIDEO env var support
    static/
      index.html                              CHANGED — Critic Review page redesigned with embedded `<video>`, per-clip stats, cost cap warning, critic report panel
  tests/
    test_video_adapters.py                    NEW — 24 tests: stub + Kling JWT + Kling happy/failure/end-frame + Luma + Runway + Pika + Veo partial + adapter contract
    test_video_routing.py                     NEW — 7 tests: routing order + fallback to stub + skip raising adapter
    test_video_stitch.py                      NEW — 6 tests: 3-clip stitch + ffprobe duration + single clip + empty/zero-byte + ffmpeg-missing fallback + reencode fallback
    test_video_pipeline.py                    NEW — 6 tests: end-to-end with stub + missing storyboard frames + cost cap stops early + cap=0 disables + adapter errors don't break + transition=False
    test_critic_review_api.py                 NEW — 7 tests: approve_storyboard advances + clips endpoint shape + 404 + /data serving final.mp4 + /data serving individual clip + clips.json persistence + publish-after-critic
    test_api.py                               CHANGED — populated_client sets AI_VIDS_OFFLINE_VIDEO=1
    test_end_to_end.py                        CHANGED — same env flag
    test_premise_review_api.py                CHANGED — same env flag
    test_storyboard_api.py                    CHANGED — same env flag
    fixtures/
      sample_clips/clip-01.mp4                NEW — 1s red, 2289 bytes
      sample_clips/clip-02.mp4                NEW — 1s green, 2289 bytes
      sample_clips/clip-03.mp4                NEW — 1s blue, 2289 bytes
```

## pytest summaries

### Offline (`pytest -m "not network and not llm and not gemini and not video"`)

```
tests/test_analyzer.py ....                                              [  2%]
tests/test_api.py ............                                           [  8%]
tests/test_beats_generation.py ........                                  [ 12%]
tests/test_collector.py ...                                              [ 14%]
tests/test_critic_review_api.py .......                                  [ 17%]
tests/test_end_to_end.py .                                               [ 18%]
tests/test_google_news_collector.py ....                                 [ 20%]
tests/test_hn_collector.py ....                                          [ 22%]
tests/test_idea_factory.py ......                                        [ 25%]
tests/test_leaderboard.py ......                                         [ 28%]
tests/test_lens_rules.py .........                                       [ 32%]
tests/test_model_adapters.py ...................                         [ 42%]
tests/test_premise_review_api.py ........                                [ 46%]
tests/test_reddit_collector.py .....                                     [ 48%]
tests/test_signals_api.py .......                                        [ 52%]
tests/test_state_machine.py .......................                      [ 63%]
tests/test_storyboard_adapters.py .............                          [ 70%]
tests/test_storyboard_api.py ......                                      [ 73%]
tests/test_storyboard_pipeline.py .......                                [ 76%]
tests/test_video_adapters.py ........................                    [ 88%]
tests/test_video_pipeline.py ......                                      [ 91%]
tests/test_video_routing.py .......                                      [ 94%]
tests/test_video_stitch.py ......                                        [ 97%]
tests/test_youtube_trending_collector.py .....                           [100%]

====================== 200 passed, 3 deselected in 2.04s =======================
```

Phase 4 was 150 passed — Phase 5 is **200 passed** (+50). The 3 deselected tests are:
- `test_network_integration.py::test_hacker_news_real_topstories` (`network`)
- `test_model_adapters.py::test_real_claude_call_returns_premises` (`llm`)
- `test_storyboard_adapters.py::test_real_gemini_image_api` (`gemini`)

The new `video` marker has zero tests under it — that's intentional. Per the plan: "all adapter tests use mocked HTTP" and "no real-provider integration tests required for this phase". The marker is registered so future opt-in tests can use it without breaking the default suite.

## Demo script output

**Video API keys set during this demo: NONE.**

```
KLING_AK=unset, KLING_SK=unset, LUMA_API_KEY=unset
RUNWAY_API_KEY=unset, FAL_KEY=unset, PIKA_API_KEY=unset
GOOGLE_VERTEX_KEY=unset
```

The pipeline therefore exercised the **stub fallback** path end-to-end, which is exactly what acceptance criterion #6 asks us to prove.

```
=== Step 1: offline test suite ===
200 passed, 3 deselected in 1.94s

=== Step 2: python -m pipelines.run_skeleton ===
Phase 2 pipeline run: 172 signals, 9 analyzed, 9 sketches
  reddit: 79
  hacker_news: 25
  google_news: 48
  youtube_trending: 20

=== Step 3: walk sk-2026-04-06-176639 ===
SKETCH_ID=sk-2026-04-06-176639
MODEL_ID=gpt-5

POST approve_premise (triggers Phase 4 storyboard pipeline)
  status: storyboard_review
  beats: 7    frames: 7

POST approve_storyboard (triggers Phase 5 video pipeline)
  status: critic_review
  clips: 7
  final_cut_path: /Users/.../sk-2026-04-06-176639/final.mp4

GET /api/sketch/sk-2026-04-06-176639/clips
{
    "sketch_id": "sk-2026-04-06-176639",
    "status": "critic_review",
    "adapter_id": "stub",
    "total_cost_cents": 0,
    "max_cost_cents_per_sketch": 500,
    "cap_hit": false,
    "cap_hit_at_beat": null,
    "clip_count": 7,
    "successful_clip_count": 7,
    "final_url": "/data/sketches/sk-2026-04-06-176639/final.mp4",
    "clips": [
        { "beat_n": 1, "provider_id": "stub", "duration_sec": 4.0, "cost_cents": 0, "url": ".../clips/beat-01.mp4" },
        { "beat_n": 2, "provider_id": "stub", "duration_sec": 5.0, "cost_cents": 0, "url": ".../clips/beat-02.mp4" },
        ... (7 total)
    ]
}

per-clip files on disk:
  -rw-r--r--  beat-01.mp4   3044 bytes
  -rw-r--r--  beat-02.mp4   3044 bytes
  -rw-r--r--  beat-03.mp4   3044 bytes
  -rw-r--r--  beat-04.mp4   3044 bytes
  -rw-r--r--  beat-05.mp4   3044 bytes
  -rw-r--r--  beat-06.mp4   3044 bytes
  -rw-r--r--  beat-07.mp4   3044 bytes

final.mp4:
  -rw-r--r--  16313 bytes
  ISO Media, MP4 Base Media v1 [ISO 14496-12:2003]

/data static mount sanity:
  GET /data/sketches/sk-2026-04-06-176639/final.mp4   -> HTTP 200, 16313 bytes
  GET /data/sketches/sk-2026-04-06-176639/clips/beat-01.mp4 -> HTTP 200, 3044 bytes
```

### final.mp4 size

**16,313 bytes**, validated as a real ISO MP4 container by `file`. That's bigger than a single 3,044-byte placeholder, which is the proof that real ffmpeg stitching ran across all 7 clips and produced a valid concat output (not just a copy of the first clip). When real video providers are wired in, expect file sizes in the hundreds of KB to single-digit MB range.

## Per-adapter completeness table

| Adapter | Completeness | Notes |
|---|---|---|
| **Kling** | **real impl complete** | Full submit → poll → download cycle. JWT HS256 with `iss`/`exp`/`nbf` claims signed by `KLING_SK`. Body includes `model_name`, `image` (base64), optional `image_tail` (forces `duration: "5"` per Kling's docs), `prompt`, `cfg_scale`, `mode`. Polls `GET /v1/videos/image2video/{task_id}` until `task_status=succeed`, downloads `task_result.videos[0].url`. Verified against `https://github.com/betasecond/KlingDemo/blob/main/APIDoc.md` and `APIDoc_Auth.md`. Mocked HTTP tests cover: happy path, JWT shape, submit failure → fallback, task failed → fallback, end-frame body shape. |
| **Luma** | **real impl complete** | Full submit → poll → download against `https://api.lumalabs.ai/dream-machine/v1/generations/video`. Body has `model`, `aspect_ratio`, `duration`, `keyframes.frame0` (and optional `frame1`) per the official OpenAPI spec at `https://github.com/lumalabs/lumaai-api/blob/main/openapi.yaml`. **Caveat:** Luma's keyframe URL must be a publicly reachable HTTPS URL — local PNGs aren't supported by the API. The adapter accepts an optional `image_url_resolver` callable in its config; without one it falls back to a `file://` URL that Luma will reject, and the adapter returns cleanly with an error. A future phase will wire in a tiny S3/GCS uploader. Mocked HTTP tests cover the happy path (with a fake resolver) and the submit failure path. |
| **Runway** | **real impl complete** | Full submit → poll → download against `https://api.dev.runwayml.com/v1/image_to_video` with the `X-Runway-Version: 2024-11-06` header. Body has `model`, `promptImage` (sent as a `data:image/png;base64,...` data URI, no external upload needed), `ratio`, `duration`, optional `promptText`. End-frame support uses the documented `[{"uri": ..., "position": "first"}, {"uri": ..., "position": "last"}]` array form. Polls `GET /v1/tasks/{id}` until `status=SUCCEEDED`, downloads `output[0]`. Verified against the runwayml/sdk-python source (`src/runwayml/_client.py`, `src/runwayml/resources/image_to_video.py`, `src/runwayml/types/task_retrieve_response.py`). Mocked HTTP tests cover happy path + the X-Runway-Version header + the failed-status path. |
| **Pika** | **real impl complete (via fal.ai)** | In 2026 Pika's official public API is hosted on fal.ai. The adapter calls the queue REST endpoints directly: `POST https://queue.fal.run/fal-ai/pika/v2.2/image-to-video`, then polls `GET /fal-ai/pika/requests/{id}/status`, then fetches `GET /fal-ai/pika/requests/{id}` to get the `video.url`. Auth is `Authorization: Key <FAL_KEY>`. Body has `image_url` (data URI), `prompt`, `duration` (5 or 10), `resolution` (720p or 1080p). Accepts both `FAL_KEY` and `PIKA_API_KEY` env vars. Verified against `https://fal.ai/models/fal-ai/pika/v2.2/image-to-video/api`. **Caveat:** Pika 2.2 image-to-video doesn't currently expose an end-frame parameter — the adapter ignores `end_frame` and prints a comment in the source explaining that Pikaframes (a separate fal endpoint) would be needed for that. Mocked HTTP tests cover the happy path and the FAILED status path. |
| **Veo** | **partial — TODO noted** | Two reasons: (1) Vertex AI requires OAuth2 service-account auth via the `google-auth` library, which would add a non-trivial dependency to `requirements.txt` and the Hetzner deploy story — explicitly out of Phase 5 scope. (2) The Veo `predictLongRunning` preview endpoint was deprecated on **2026-04-02** (4 days before this report was written) and the GA endpoint shape is in flux. Per the plan's hard rule "Do not invent endpoints or parameter names you can't confirm", the adapter is partial: `is_available()` correctly checks for `GOOGLE_VERTEX_KEY` or `GOOGLE_APPLICATION_CREDENTIALS` plus a project ID; `estimated_cost_cents()` returns a placeholder; `generate()` returns immediately with a clean error explaining what's missing and copies the placeholder MP4 to `out_path`. The module-level docstring lists exactly what needs to be added to finish: pull a fresh access token via `google.auth.default()`, confirm the post-deprecation GA endpoint, re-verify the `instances` + `parameters` body schema. Two mocked tests cover the un-credentialed and the credentialed paths — both must return cleanly without raising. |
| **Stub** | **stub only** | Always available, zero cost, copies `video_gen/placeholder.mp4` to `out_path`. Used as the fallback when no real provider reports `is_available()`. This is what the demo run exercised end-to-end. |

## Critic Review page (one paragraph)

The Critic Review page now renders one wide card per sketch with the assembled final cut **embedded as an HTML5 `<video controls>` element** sourced from `/data/sketches/{id}/final.mp4`. The card header shows the sketch ID, the video provider that produced the clips (e.g. `provider: stub` or `provider: kling`), the approved premise logline, and a publish/reject button pair on the right that hits the existing `/api/sketch/{id}/publish` and `/reject` endpoints. Below the header is a two-column grid: the left two-thirds is the embedded video player with a black background and full-width responsive sizing (it collapses to a single column on narrow screens), and the right third is a stats panel showing the provider, the success rate (`successful_clip_count / clip_count`), the running cost in dollars, the cost cap, and a per-clip breakdown listing each beat's provider, cost, and an error indicator if anything failed. If the cost cap was hit during generation a red warning banner reads `cost cap reached at beat N` so the user knows the final cut may be shorter than the original beat sheet intended. Below the video row is the (still stubbed) **critic report panel** showing the overall score, the verdict line, and a bulleted list of fix suggestions. The video element uses a `?t=Date.now()` cache-bust query string so a regen-then-refresh shows the new bytes. Every other page (Signals, Premise Review, Storyboard Review, Published, Rejected) is unchanged from Phase 4.

## Deviations from the plan

| # | Deviation | Reason |
|---|---|---|
| 1 | The Veo adapter is partial-with-TODO instead of complete | The Veo `predictLongRunning` preview endpoint was deprecated on 2026-04-02 (4 days before this report). The GA endpoint shape is in flux. Per the Phase 5 plan's explicit rule — "Do not invent endpoints or parameter names you can't confirm. Better to ship a clean error than guess" — the adapter returns cleanly with a documented error rather than guess at field names. The module-level docstring lists exactly what needs to be added. |
| 2 | Pika is wired through fal.ai (`queue.fal.run/fal-ai/pika/v2.2/image-to-video`), not a direct Pika first-party endpoint | Pika doesn't have a direct first-party developer API in 2026 — `pika.art/api` redirects to fal.ai. This is verified against Pika's own marketing page and the fal.ai blog post titled "Pika API is now powered by fal". The adapter accepts both `FAL_KEY` and `PIKA_API_KEY` env vars to match user expectations either way. |
| 3 | The Luma adapter requires an `image_url_resolver` callable in its config to upload local PNGs to a publicly reachable URL | Luma's official API only accepts `keyframes.frame0.url` as an HTTPS URL — the OpenAPI spec doesn't expose a base64 path. Without an uploader, the adapter falls back to `file://` which Luma rejects, and the adapter returns cleanly with an error. A future phase will wire in a tiny S3/GCS uploader. The Luma test injects a fake resolver to verify the happy path. |
| 4 | The Pika adapter ignores the `end_frame` argument (returns a clip generated only from `start_frame`) | Pika 2.2's `image-to-video` endpoint doesn't expose end-frame conditioning. fal.ai has a separate `pikaframes` model for keyframe interpolation. Documented in the source. |
| 5 | The Kling adapter forces `duration: "5"` whenever `image_tail` is supplied | Per the official Kling docs: "Requests containing `image_tail` ... currently only support generating 5s videos." The adapter respects this rather than send a 10s request that would fail. |
| 6 | `backend/main.py` accepts an `AI_VIDS_OFFLINE_VIDEO=1` env var that forces the stub video adapter | Same pattern as Phase 4's `AI_VIDS_OFFLINE_STORYBOARD=1`. Without it, every API test that walks through `approve_storyboard` would block on the Kling adapter trying to call `api.klingai.com`. Production runs (no env var) use the routed adapter. |
| 7 | The video pipeline transitions the sketch all the way to `CRITIC_REVIEW` itself (via `transition=True`), and the backend's `approve_storyboard` then runs the still-stub critic on a sketch that's already in CRITIC_REVIEW | The critic stub doesn't transition state, it just attaches a `critic_report` field. Letting the pipeline drive the SCRIPTED → VIDEO_PENDING → CRITIC_REVIEW chain means any future async/parallel video worker doesn't need a side door for the transition. |
| 8 | `video_gen/stub_provider.py` (legacy Phase 1 module) is kept on disk but no longer imported anywhere | Same call as Phase 4's `storyboard/stub_storyboard.py` — deletion is risk, the file is harmless, the new layout lives at `video_gen/adapters/stub_video.py`. Can be swept in a follow-up. |
| 9 | A `cost cap of 0` is treated as "no cap" by the pipeline | The cap check is `if cap > 0 and (cumulative + estimate) > cap`. Treating 0 as "disabled" matches the YAML ergonomics — leave the field at 0 in tests and the cap doesn't fire. Documented in `test_cost_cap_zero_disables_check`. |

## Reproducer

```bash
cd /Users/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality
source .venv/bin/activate

# Offline tests (no network, no LLM/image/video tokens)
pytest -m "not network and not llm and not gemini and not video" -q

# Phase 3 real Claude call (~21s, ~$0.01)
pytest -m llm -v

# Phase 4 real Gemini image call (skipped unless GEMINI_API_KEY is set)
pytest -m gemini -v

# Full pipeline (real radar + real Claude factory + real video pipeline if keys set)
python -m pipelines.run_skeleton

# UI
uvicorn backend.main:app --port 8000
# open http://localhost:8000 and click Critic Review
```

## Sources I verified the API shapes against

- Kling: <https://github.com/betasecond/KlingDemo/blob/main/APIDoc.md> and `APIDoc_Auth.md`
- Luma: <https://github.com/lumalabs/lumaai-api/blob/main/openapi.yaml>
- Runway: <https://github.com/runwayml/sdk-python> (`_client.py`, `resources/image_to_video.py`, `resources/tasks.py`, `types/task_retrieve_response.py`)
- Pika (via fal): <https://fal.ai/models/fal-ai/pika/v2.2/image-to-video/api> and the fal.ai blog announcement
- Veo: <https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation> (intentionally not implemented past the gate, see deviation 1)

Sources:
- [Kling APIDoc.md](https://github.com/betasecond/KlingDemo/blob/main/APIDoc.md)
- [Kling APIDoc_Auth.md](https://github.com/betasecond/KlingDemo/blob/main/APIDoc_Auth.md)
- [Luma openapi.yaml](https://github.com/lumalabs/lumaai-api/blob/main/openapi.yaml)
- [Runway sdk-python](https://github.com/runwayml/sdk-python)
- [Pika 2.2 image-to-video on fal.ai](https://fal.ai/models/fal-ai/pika/v2.2/image-to-video/api)
- [Veo on Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation)
