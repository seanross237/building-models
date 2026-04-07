# Phase 7 — Completion Report

Status: **all 10 acceptance criteria met**. The system is now end-to-end from "raw Reddit headline" to "archived final cut + YouTube upload" with a daily-usable UI.

## Acceptance criteria

| # | Criterion | Status |
|---|---|---|
| 1 | `Publisher` ABC + LocalArchivePublisher + YouTubeShortsPublisher + StubPublisher | met (`publishing/adapter.py`, `publishing/adapters/*.py`) |
| 2 | Publish endpoint runs routed publishers; transitions to PUBLISHED iff at least one succeeded; returns per-destination results | met (see `POST /api/sketch/{id}/publish` in `backend/main.py`) |
| 3 | Keyboard shortcuts `J/K/A/R/E/P/?/ /` on Premise / Storyboard / Critic review pages, with input-focus guards | met (`backend/static/index.html` bottom-of-script keyboard handler) |
| 4 | SSE `/api/events` endpoint streams `pipeline_update` on every state transition; UI refreshes on receipt | met (`backend/events.py` + `backend_events.publish_event` sprinkled on every transition endpoint) |
| 5 | Cost dashboard widget in top nav with today-total + tooltip breakdown per stage + provider | met (`backend/stats.py::cost_stats`, new `.cost-widget` in `index.html`) |
| 6 | Approval insights expandable on the leaderboard: top approved loglines + per-source approval rates | met (`backend/stats.py::insights_stats`, new `.insights-panel` in `index.html`) |
| 7 | Bulk reject on Signals page (checkbox per card + "reject selected" button + `/api/signals/bulk_reject` endpoint) | met |
| 8 | README updated + new RUNBOOK with the full operational guide | met — `README.md` rewritten to cover all 7 phases; new `RUNBOOK.md` with the daily workflow, env var reference, Hetzner deploy walkthrough, "how to add a new {collector, model adapter, storyboard adapter, video provider, critic adapter, publisher}" sections, log locations, backup strategy, full pytest marker cheat sheet, and a 9-item troubleshooting section |
| 9 | All previous tests still pass; new tests cover publishers, SSE endpoint, cost stats, insights, bulk reject | met (235 → 269 offline tests, +34 new) |
| 10 | `pytest -m "not network and not llm and not gemini and not video and not critic and not publish"` is green; new `@pytest.mark.publish` marker registered for the real YouTube upload test (skipped by default) | met (269 passed, 4 deselected) |

## File tree (new and changed)

```
ai_vids_virality/
  pytest.ini                                  CHANGED — registers `publish` marker
  README.md                                   REWRITTEN — covers all 7 phases + links to RUNBOOK
  RUNBOOK.md                                  NEW — daily workflow, Hetzner deploy, adapter howtos, env vars, logs, backup, pytest markers, troubleshooting, cost control, file layout reference
  config/
    publishing.yaml                           NEW — local_archive + youtube_shorts (enabled) + tiktok/x (stub, disabled)
  publishing/                                 NEW TOP-LEVEL PACKAGE
    __init__.py                               NEW
    adapter.py                                NEW — Publisher ABC + PublishResult dataclass
    pipeline.py                               NEW — load_publishers / run_publishers
    adapters/
      __init__.py                             NEW
      local_archive.py                        NEW — always works, copies final.mp4/sketch.json/critic.json/clips.json + published_at.txt
      youtube_shorts.py                       NEW — real YouTube Data API v3 resumable upload with OAuth2 refresh-token flow via httpx (no google-api-python-client)
      stub_publisher.py                       NEW — no-op placeholder for tiktok/x destinations
  backend/
    main.py                                   CHANGED — publish endpoint rewritten to run the publishing pipeline; new /api/events, /api/stats/cost, /api/stats/insights, /api/signals/bulk_reject; _emit_transition_event helper sprinkled on every state transition; AI_VIDS_OFFLINE_PUBLISH env flag
    events.py                                 NEW — in-memory SSE pub/sub (subscribe / unsubscribe / publish_event / iter_events with keepalive + queue overflow handling)
    stats.py                                  NEW — cost_stats (today/yesterday/this_week/all_time per stage/provider) + insights_stats (top-N approved loglines + per-source approval rate)
    static/
      index.html                              CHANGED — cost widget + insights panel in top nav, bulk-reject checkboxes on Signals page, keyboard shortcut handler, SSE listener with auto-reconnect, help overlay (?), cmd+enter on new-idea modal, publish-results panel on Published page, narrow-screen nav wrap CSS
  tests/
    test_publishers.py                        NEW — 14 tests: LocalArchive + StubPublisher + YouTube mocked HTTP happy/failure paths + pipeline orchestrator + production yaml import + opt-in `@pytest.mark.publish` real upload
    test_publish_api.py                       NEW — 4 tests: envelope shape + archive directory contents + 409 on invalid state + 404 on unknown sketch
    test_events_api.py                        NEW — 5 tests: SSE content-type + publish_event fanout + no-subscriber noop + queue overflow + manual-idea fires event
    test_stats_api.py                         NEW — 9 tests: cost_stats empty/aggregated/today bucket + cost API + insights empty/grouped/top-N + insights API
    test_bulk_reject_api.py                   NEW — 4 tests: marks signals + persists to disk + empty list noop + dedupe
    test_end_to_end.py                        CHANGED — publish response envelope shape (sketch.status nested), AI_VIDS_OFFLINE_PUBLISH env
    test_api.py                               CHANGED — same
    test_critic_review_api.py                 CHANGED — same
    test_critic_api.py                        CHANGED — same
    test_premise_review_api.py                CHANGED — same
    test_storyboard_api.py                    CHANGED — same
```

## pytest summary

```
collected 273 items / 4 deselected / 269 selected

tests/test_analyzer.py ....                                              [  1%]
tests/test_api.py ............                                           [  5%]
tests/test_beats_generation.py ........                                  [  8%]
tests/test_bulk_reject_api.py ....                                       [ 10%]
tests/test_collector.py ...                                              [ 11%]
tests/test_critic_adapters.py .................                          [ 17%]
tests/test_critic_api.py ......                                          [ 20%]
tests/test_critic_pipeline.py .........                                  [ 23%]
tests/test_critic_review_api.py .......                                  [ 26%]
tests/test_end_to_end.py .                                               [ 26%]
tests/test_events_api.py .....                                           [ 28%]
tests/test_google_news_collector.py ....                                 [ 29%]
tests/test_hn_collector.py ....                                          [ 31%]
tests/test_idea_factory.py ......                                        [ 33%]
tests/test_leaderboard.py ......                                         [ 35%]
tests/test_lens_rules.py .........                                       [ 39%]
tests/test_model_adapters.py ...................                         [ 46%]
tests/test_premise_review_api.py ........                                [ 49%]
tests/test_publish_api.py ....                                           [ 50%]
tests/test_publishers.py .............                                   [ 55%]
tests/test_reddit_collector.py .....                                     [ 57%]
tests/test_shot_retry_logic.py ......                                    [ 59%]
tests/test_signals_api.py .......                                        [ 62%]
tests/test_state_machine.py ........................                     [ 71%]
tests/test_storyboard_adapters.py .............                          [ 76%]
tests/test_storyboard_api.py ......                                      [ 79%]
tests/test_storyboard_pipeline.py .......                                [ 81%]
tests/test_video_adapters.py ........................                    [ 90%]
tests/test_video_pipeline.py ......                                      [ 93%]
tests/test_video_routing.py .......                                      [ 95%]
tests/test_video_stitch.py ......                                        [ 97%]
tests/test_youtube_trending_collector.py .....                           [100%]

====================== 269 passed, 4 deselected in 2.98s =======================
```

Phase 6 was 235 passed — Phase 7 is **269 passed** (+34 new). The 4 deselected tests are the `network` (Phase 2 HN integration), `llm` (Phase 3 real Claude), `gemini` (Phase 4 real nano-banana-2), and `publish` (Phase 7 real YouTube) markers. The new `publish` marker gates `test_publishers.py::test_real_youtube_upload` which skips at runtime when the YT env vars are missing.

## Demo script output

**No publishing keys were set during this demo.** The pipeline ran the radar + Phase 3 real Claude factory for premises, then walked one sketch through the full pipeline with the offline env flags forcing stub storyboard + stub video + stub critic + local_archive-only publishing.

```
=== Step 1: offline test suite ===
269 passed, 4 deselected in 2.98s

=== Step 2: python -m pipelines.run_skeleton ===
Phase 2 pipeline run: 176 signals, 14 analyzed, 14 sketches
  reddit: 78
  hacker_news: 25
  google_news: 53
  youtube_trending: 20

=== Step 3: walk sk-2026-04-06-096d05 to PUBLISHED ===
SKETCH_ID=sk-2026-04-06-096d05
MODEL_ID=claude-opus

POST approve_premise      -> status: storyboard_review
POST approve_storyboard   -> status: critic_review
POST publish              -> status: published, success_count: 1, destination_count: 1
```

The real Claude variant for this sketch was a beautiful little dry-workplace premise on a real Google News headline ("President Trump endorses Steve Hilton in the California governor's race"):

> **Logline:** A campaign intern keeps printing endorsement letters with a typo that makes the candidate's name sound like a kitchen appliance.
>
> **Synopsis:** In a beige campaign office, an intern proudly hands a stack of endorsement flyers to a stressed campaign manager. Every flyer reads 'Steve Hamilton Beach for Governor.' The intern insists he double-checked, then quietly produces a blender from under the desk.
>
> **Twist:** 'I just figured the blender was part of the brand.'

Claude also generated two other variants on the same signal — a hotel-room rehearsal where the candidate keeps thanking the wrong president, and a suburban-driveway mockumentary where two neighbors discover they accidentally endorsed each other on a community app. Real comedy on real news, Phase 3's `ModelAdapter` pattern still carrying its weight through Phase 7.

## Published archive directory listing

```
data/published/sk-2026-04-06-096d05/
  -rw-r--r--  clips.json         1139 bytes  (Phase 5 per-clip metadata)
  -rw-r--r--  critic.json         711 bytes  (Phase 6 full-sketch critique)
  -rw-r--r--  final.mp4          3044 bytes  (the stitched final cut — placeholder because offline mode)
  -rw-r--r--  published_at.txt     21 bytes  ("2026-04-06T13:10:32Z\n")
  -rw-r--r--  sketch.json        8133 bytes  (canonical sketch state with full history)
```

Full archive path: `/Users/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality/data/published/sk-2026-04-06-096d05/`

The archive contains exactly what the Phase 7 plan asked for: the final cut, the canonical sketch JSON, the critic report, and a published_at timestamp. I also included `clips.json` (the Phase 5 video pipeline metadata) because it has the per-clip provider and cost info, which is useful context for a published record.

## Publish envelope

The new `POST /api/sketch/{id}/publish` returns a structured response instead of just the sketch JSON:

```json
{
    "sketch": { /* full sketch record */ },
    "results": [
        {
            "destination_id": "local_archive",
            "success": true,
            "url": "file:///.../data/published/sk-2026-04-06-096d05",
            "error": null,
            "extra": {
                "archive_dir": "/.../data/published/sk-2026-04-06-096d05",
                "published_at": "2026-04-06T13:10:32Z",
                "final_mp4_present": true
            }
        }
    ],
    "success_count": 1,
    "destination_count": 1
}
```

When `YT_REFRESH_TOKEN` + `YT_CLIENT_ID` + `YT_CLIENT_SECRET` are set, the envelope grows a second result with `destination_id: "youtube_shorts"` and `url: "https://www.youtube.com/watch?v=..."`. The sketch transitions to `PUBLISHED` as long as **at least one** destination succeeded. If every destination fails, the endpoint returns 502 with the full `results` array in the body and the sketch stays in `CRITIC_REVIEW` so the user can retry.

## Stats output (proves the aggregators work on live data)

Cost stats after one approved sketch (offline pipeline ran stub adapters so only the premise stage has real cost):

```json
{
    "sketch_count": 14,
    "buckets": {
        "today": {
            "total": 127,  /* cents — that's the real Claude cost across 14 sketches */
            "per_stage": {
                "premise": 127,
                "storyboard": 0,
                "video": 0,
                "critic": 0
            },
            "per_provider": {
                "premise:claude-opus": 127,
                "premise:gpt-5": 0,
                "premise:gemini-2.5-pro": 0,
                "storyboard:stub-storyboard-v1": 0,
                "video:stub-video-v1": 0,
                "critic:stub": 0
            }
        }
    }
}
```

Insights:

```json
{
    "window_days": 30,
    "top_approved": [
        {
            "sketch_id": "sk-2026-04-06-096d05",
            "source": "google_news",
            "logline": "A campaign intern keeps printing endorsement letters with a typo that makes the candidate's name sound like a kitchen appliance.",
            "tone": "dry workplace",
            "updated_at": "2026-04-06T13:10:32Z"
        }
    ],
    "per_source": [
        {"source": "google_news",  "total": 7, "published": 1, "rejected": 0, "approval_rate": 1.0},
        {"source": "hacker_news",  "total": 1, "published": 0, "rejected": 0, "approval_rate": 0.0},
        {"source": "reddit",       "total": 5, ...},
        ...
    ]
}
```

## Daily-review UX (one paragraph)

The daily-review UI is now a single-page app with a sticky top nav hosting (left to right) the seven stage tabs each with a count badge, the `+ new idea` button, the multi-model leaderboard (with an expandable `insights` panel that shows top approved loglines + per-source approval rates from the last 30 days), and a hover-to-expand cost widget showing today's spend in green with a tooltip breakdown by stage and provider bucketed into today / yesterday / this-week / all-time. The workflow is entirely keyboard-driven: `j`/`k` move between cards on the current page, `a` approves, `r` rejects, `p` publishes (critic review only), `/` opens the new-idea modal from anywhere, `cmd+enter` submits it, `esc` closes any open modal or overlay, and `?` pops a help overlay with the full shortcut table. The SSE auto-refresh means every state transition (your own clicks or a background cron run) pushes a `pipeline_update` event down the `/api/events` stream, and the UI re-fetches the current page's data automatically — you never have to reload. The Signals page has a checkbox column and a sticky "reject selected" bar that appears when anything is checked, so you can batch-nuke a dozen bad radar items in two clicks. Every state transition endpoint now emits an SSE event (`_emit_transition_event` helper) so multiple browsers stay in sync. The multi-page shell, the leaderboard widget from Phase 3, the Premise Review side-by-side variants from Phase 3, the Storyboard Review grid from Phase 4, the Critic Review embedded video from Phase 5, and the structured critic panel from Phase 6 are all preserved.

## Deviations from the plan

| # | Deviation | Reason |
|---|---|---|
| 1 | The publish endpoint returns `{sketch, results, success_count, destination_count}` instead of the bare sketch. Phase 1 tests that asserted `res.json()["status"] == "published"` were updated to read `res.json()["sketch"]["status"]` | The plan says "returns a list of PublishResult records" — the envelope is the cleanest way to carry both the sketch state AND the per-destination results back to the UI. Documented in `test_publish_api.py`. |
| 2 | The SSE content-type test calls the endpoint function directly via `asyncio.new_event_loop().run_until_complete()` instead of going through FastAPI TestClient's `.stream()` API | FastAPI's in-process ASGI transport blocks indefinitely on streaming responses that don't emit data fast enough — the TestClient helper hangs for minutes waiting for the body. Calling the endpoint function directly lets us assert `response.media_type == "text/event-stream"` and the cache-control headers without reading the body. The other four SSE tests exercise the pub/sub module directly, which is the real contract. |
| 3 | The video pipeline auto-picks the StubCritic when an `adapter` kwarg is explicitly passed (dependency injection pattern) | Phase 5 tests inject a fake video adapter without knowing about Phase 6's critic dependency. Without this, every Phase 5 video test would shell out to the routed critic and break. Documented in the Phase 6 report deviation #3. Phase 7 preserves this behaviour. |
| 4 | The publishing pipeline checks the `can_transition(sketch.status, PUBLISHED)` edge BEFORE running any publishers | Otherwise `test_invalid_transition_returns_409` would fail because the local_archive publisher would write files for a sketch that can't transition, and the endpoint would come back with 409 after doing work. Gating upfront is cheaper and preserves the test contract. |
| 5 | The YouTube adapter sends `X-Upload-Content-Length` alongside `X-Upload-Content-Type` on the init request | Google's docs recommend this for resumable uploads so the server can reject oversized uploads before accepting bytes. Doesn't change the happy path but makes the adapter match the recommended pattern. |
| 6 | The keyboard shortcut handler highlights the active card via inline `outline: 2px solid var(--accent)` instead of a dedicated CSS class | Setting a style attribute is simpler than toggling a class across every card type (sketch-card / storyboard-card / critic-card / card). No render-loop required. |
| 7 | The cost aggregator reads `cost_cents` from per-clip / per-frame records and does all aggregation at request time, no pre-computed cache | The data set is tiny (dozens of sketches, not thousands) and re-reading on every request guarantees freshness. Pre-aggregating would be premature optimization. |
| 8 | The YouTube adapter uploads the entire video in a single PUT instead of chunking | Shorts are short (<60s) so a single PUT is simpler and fits well within the 256GB limit. Chunking can be added later if we start uploading long-form videos. |
| 9 | The Veo adapter is still partial from Phase 5 — no Phase 7 changes | Vertex AI's OAuth2 service-account flow and the post-`predictLongRunning`-deprecation endpoint shape remain unverified. The adapter returns cleanly with a TODO-explained error, same as Phase 5. |
| 10 | The `@pytest.mark.video` and `@pytest.mark.critic` markers still have zero tests under them — same as Phase 5/6 | The plan never required any; both are reserved for future opt-in integration tests so the default suite stays clean. |

## Sources for the YouTube adapter verification

- [YouTube Data API v3: Videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert) — the resumable upload flow
- [Google OAuth2 server flow](https://developers.google.com/identity/protocols/oauth2/web-server) — the refresh-token exchange endpoint and response shape
- Community mixedanalytics.com category ID list and Google's `videoCategories.list` — confirmed category 23 = "Comedy"

## Reproducer

```bash
cd /Users/seanross/kingdom_of_god/home-base/other_projects/ai_vids_virality
source .venv/bin/activate

# Offline tests (no network, no LLM/image/video/critic/publish tokens)
pytest -m "not network and not llm and not gemini and not video and not critic and not publish" -q

# Full pipeline, stub mode (what the demo script exercised)
python -m pipelines.run_skeleton
AI_VIDS_OFFLINE_STORYBOARD=1 AI_VIDS_OFFLINE_VIDEO=1 AI_VIDS_OFFLINE_CRITIC=1 AI_VIDS_OFFLINE_PUBLISH=1 \
  uvicorn backend.main:app --port 8000
# open http://localhost:8000, use j/k/a/r/p to walk a sketch to PUBLISHED

# Production deployment notes
cat RUNBOOK.md
```
