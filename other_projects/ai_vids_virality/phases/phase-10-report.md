# Phase 10 — Manual Editing + Collapsed Premise Review

Status: **code complete, 356 tests passing, every acceptance criterion met.** Phase 10 is purely additive — no infrastructure changes, no new external services, no new providers, no changes to existing state-machine transitions. Four new API endpoints, six new test files, one new JS namespace (`window.premiseReview`), three new inline modals (promote-with-guidance, premise editor, beat editor), and a Gmail-style collapsed-by-default Premise Review page.

## Files added / changed

| Path | Status | Purpose |
|---|---|---|
| `idea_factory/prompts/premise_generation.md` | CHANGED | Inserted `{user_guidance_section}` placeholder between the Signal block and the Task block. |
| `idea_factory/factory.py` | CHANGED | New `_build_user_guidance_section(signal)` helper that renders `## Human guidance\n\n{text}\n` when `user_guidance` is present on the queue marker, empty string otherwise. `_format_prompt` now passes the rendered section into the template's new placeholder. `run_factory` appends a `human_promote_with_guidance` event onto sketch history when guidance is present. |
| `backend/main.py` | CHANGED | Four new endpoints: `POST /api/signals/{id}/promote` (now accepts optional `{"guidance": "..."}`), `PATCH /api/sketch/{id}/premise`, `POST /api/sketch/{id}/premise`, `PATCH /api/sketch/{id}/beat/{n}`. New Pydantic models (`PromoteSignalIn`, `PremiseEditIn`, `PremiseAddIn`, `BeatEditIn`). New helpers (`_normalize_premise_payload`, `_variant_marker_path`, `_read_variant_marker`, `_write_variant_marker`, `_write_beats_sidecar`). The `/api/sketch/{id}/storyboard` frame payload gains `dialogue` + `visual_note` so the beat editor can pre-populate the modal. |
| `backend/static/index.html` | CHANGED | Premise Review cards start collapsed. New `window.premiseReview` namespace (`expandAllPremiseCards`, `collapseAllPremiseCards`, `togglePremiseCard`, `isPremiseCardExpanded`). `expand all` / `collapse all` toolbar. `Space` toggles the focused card. New premise editor modal (used for both edit and add). New promote-with-guidance modal. New beat editor modal. New CSS for `.sketch-card.collapsed`, `.sketch-card.expanded`, `.variant-summary`, `.collapse-arrow`, `.premise-review-toolbar`, `.edit-premise-btn`, `.add-premise-btn`, `.editor-modal`, `.edit-beat-btn`. |
| `tests/test_signals_promote_with_guidance.py` | **NEW** | 4 tests: guidance present writes `user_guidance` on queue marker; no body still promotes cleanly; empty / whitespace guidance omits the field; promote still creates the downstream sketch |
| `tests/test_idea_factory_uses_guidance.py` | **NEW** | 7 tests: `_build_user_guidance_section` with / without guidance; factory passes guidance into the prompt; factory omits guidance when absent; factory stamps `human_promote_with_guidance` history event only when guidance is present; bundled `premise_generation.md` carries the `{user_guidance_section}` placeholder |
| `tests/test_premise_edit_endpoint.py` | **NEW** | 5 tests: PATCH updates the variant in place, writes `human_edit_premise` history event with full payload, returns 404 on unknown variant, returns 400 on out-of-range index, returns 404 on unknown sketch |
| `tests/test_premise_add_endpoint.py` | **NEW** | 4 tests: POST creates a fresh `__human.json` variant marker, appends to an existing human variant, writes `human_add_premise` history, and approving a human premise increments the `human` row on the leaderboard (with losing AI variants getting rejected on the same call) |
| `tests/test_beat_edit_endpoint.py` | **NEW** | 5 tests: PATCH updates `sketch.beats` in place, writes a `beats.json` sidecar, writes `human_edit_beat` history with `fields_updated` payload, returns 404 on unknown sketch, returns 404 on unknown beat_n |
| `tests/test_premise_review_collapse.py` | **NEW** | 10 tests: `window.premiseReview` namespace exposes the four state functions; `expandedPremiseCards = new Set()` declaration exists; `.collapsed` / `.expanded` class tokens present; `expand all` / `collapse all` buttons present; `togglePremiseCard(...)` wired to click handlers; Space key wired as a keydown check; PATCH `/premise` fetch present; `add premise` button present; promote guidance dialog wiring present; `editBeat` wiring present |

## pytest summary

### Offline (`pytest -m "not network and not llm and not gemini and not video and not critic and not publish and not fal and not openrouter"`)

```
tests/test_analyzer.py ....                                              [  1%]
tests/test_api.py ............                                           [  4%]
tests/test_beat_edit_endpoint.py .....                                   [  5%]
tests/test_beats_generation.py ........                                  [  7%]
tests/test_bulk_reject_api.py ....                                       [  8%]
tests/test_collector.py ...                                              [  9%]
tests/test_critic_adapters.py .................                          [ 14%]
tests/test_critic_api.py ......                                          [ 16%]
tests/test_critic_pipeline.py .........                                  [ 19%]
tests/test_critic_review_api.py .......                                  [ 21%]
tests/test_end_to_end.py .                                               [ 21%]
tests/test_events_api.py .....                                           [ 23%]
tests/test_fal_image_adapter.py ..............                           [ 27%]
tests/test_fal_unified_adapter.py ......................                 [ 33%]
tests/test_google_news_collector.py ....                                 [ 35%]
tests/test_hn_collector.py ....                                          [ 36%]
tests/test_idea_factory.py ......                                        [ 37%]
tests/test_idea_factory_uses_guidance.py .......                         [ 39%]
tests/test_leaderboard.py ......                                         [ 41%]
tests/test_lens_rules.py .........                                       [ 44%]
tests/test_model_adapters.py ...................                         [ 49%]
tests/test_openrouter_adapter.py ................                        [ 54%]
tests/test_premise_add_endpoint.py ....                                  [ 55%]
tests/test_premise_edit_endpoint.py .....                                [ 57%]
tests/test_premise_review_api.py ........                                [ 59%]
tests/test_premise_review_collapse.py ..........                         [ 62%]
tests/test_publish_api.py ....                                           [ 63%]
tests/test_publishers.py .............                                   [ 67%]
tests/test_reddit_collector.py .....                                     [ 68%]
tests/test_shot_retry_logic.py ......                                    [ 70%]
tests/test_signals_api.py .......                                        [ 72%]
tests/test_signals_promote_with_guidance.py ....                         [ 73%]
tests/test_state_machine.py ........................                     [ 80%]
tests/test_stats_api.py ........                                         [ 82%]
tests/test_storyboard_adapters.py .............                          [ 86%]
tests/test_storyboard_api.py ......                                      [ 88%]
tests/test_storyboard_pipeline.py .......                                [ 90%]
tests/test_video_adapters.py ........................                    [ 97%]
tests/test_video_pipeline.py ......                                      [ 98%]
tests/test_video_routing.py .......                                      [100%]
tests/test_video_stitch.py ......                                        [100%]
tests/test_youtube_trending_collector.py .....                           [100%]

====================== 356 passed, 7 deselected in 3.23s =======================
```

Phase 9 was 321 passed. Phase 10 is **356 passed** (+35 new tests: 4 + 7 + 5 + 4 + 5 + 10). The plan estimated "roughly 327 passed (+15-20)"; the actual count is higher because each new endpoint got explicit edge-case coverage (404 / 400 paths) and the frontend smoke test got one assertion per Phase 10 UI affordance.

## Demo walkthrough

All four endpoints were exercised end-to-end via `fastapi.testclient.TestClient` against a `tmp_path` data root. The same TestClient path is what the six new test files hit, but this section shows the curl-equivalent happy-path for each. Output is verbatim from the demo script.

### 1) Promote a signal with guidance text

```
POST /api/signals/demo-sig-1/promote
{"guidance": "lean into the crosswalk-volunteer angle, one location, mockumentary tone"}

status: 200
body: {"signal_id": "demo-sig-1", "promoted": true, "score": 7,
       "new_sketches": ["sk-2026-04-06-a3584b"],
       "user_guidance": "lean into the crosswalk-volunteer angle, one location, mockumentary tone"}
```

`cat data/queues/idea-factory/demo-sig-1.json` (the queue manifest) shows the new `user_guidance` field landed alongside the existing Phase 2 payload:

```json
{
  "analyzed_at": "2026-04-06T14:51:27Z",
  "character_archetypes": ["everyman", "authority figure"],
  "comedy_angles": [{"angle": "manual", "note": "force-promoted from signals page"}],
  "force_promoted": true,
  "should_promote": true,
  "signal_id": "demo-sig-1",
  "sketchability_score": 7,
  "source": "reddit",
  "source_item_path": ".../signals/reddit/items/demo-sig-1.md",
  "source_url": "https://example.com/demo",
  "summary": "Traffic chaos ensues.",
  "title": "City council accidentally replaces stoplights with colored flags",
  "topical_window_hours": 48,
  "user_guidance": "lean into the crosswalk-volunteer angle, one location, mockumentary tone"
}
```

When the body is missing or `guidance` is empty / whitespace-only, the field is omitted entirely — the endpoint is fully backward-compatible with the Phase 2 no-body promote path.

### 2) Edit a premise inline

```
PATCH /api/sketch/sk-2026-04-06-b29af3/premise
{
  "model_id": "gpt-5",
  "premise_index": 0,
  "premise": {
    "logline": "HUMAN-EDITED: A crosswalk volunteer runs the new flag system",
    "synopsis": "human edit synopsis",
    "tone": "mockumentary",
    "target_length_sec": 45,
    "characters": [{"name": "Martha", "description": "volunteer"}],
    "twist": "her idea"
  }
}

status: 200
```

`cat data/queues/premise-review/sk-2026-04-06-b29af3__gpt-5.json` shows `premises[0].logline == "HUMAN-EDITED: A crosswalk volunteer runs the new flag system"`. Siblings in the same variant list are untouched (verified in `test_edit_premise_updates_variant_in_place`).

`cat data/sketches/sk-2026-04-06-b29af3/sketch.json` history array now contains a `human_edit_premise` event:

```
history events: [null, "human_promote_with_guidance", "human_edit_premise"]
```

The first entry is the factory's `IDEA_PENDING -> PREMISE_REVIEW` transition (stored as `{from, to, at, payload}` — no `event` key, so it shows as `null` in this extract). The second is the Phase 10 `human_promote_with_guidance` stamp (because the seed signal had `user_guidance` set). The third is the `human_edit_premise` stamp from this PATCH call. All three are append-only, in chronological order.

### 3) Add a new human premise + leaderboard increment

```
POST /api/sketch/sk-2026-04-06-b29af3/premise
{
  "premise": {
    "logline": "A human-written premise: three volunteers run the intersection",
    "synopsis": "crosswalk volunteers try to keep order",
    "tone": "mockumentary",
    "target_length_sec": 30,
    "characters": [{"name": "Martha", "description": "volunteer"}],
    "twist": "Martha is the mayor"
  }
}

status: 200
body: {"model_id": "human", "premise_index": 0, "variant_premise_count": 1, ...}
```

A brand-new variant marker appears on disk: `data/queues/premise-review/sk-2026-04-06-b29af3__human.json` with `model_id: "human"` and one premise in the list. A second POST appends a second premise to the same human variant (verified in `test_add_human_premise_appends_to_existing_human_variant`).

Approving the human premise then drives the leaderboard:

```
POST /api/sketch/sk-2026-04-06-b29af3/approve_premise
{"model_id": "human", "premise_index": 0}

leaderboard rows (after):
  claude-opus: approved=0, rejected=1
  gpt-5:       approved=0, rejected=1
  human:       approved=1, rejected=0
```

The `human` row is created on first use by the existing `Leaderboard.record_decision` path — no schema migration needed. When the human's pitch wins, the losing AI variants get `rejected +=1` on the same call (existing Phase 3 leaderboard accounting).

### 4) Edit a beat

```
PATCH /api/sketch/sk-demo-beat/beat/2
{
  "action": "HUMAN-EDITED: inspector arrives and the entire cafe freezes",
  "dialogue": "just here for a scone"
}

status: 200
edited beat action: HUMAN-EDITED: inspector arrives and the entire cafe freezes
```

`cat data/sketches/sk-demo-beat/beats.json` (the new Phase 10 sidecar) shows the updated beat alongside the untouched siblings:

```json
{
  "beats": [
    {
      "action": "establish",
      "camera": "wide",
      "characters": [],
      "dialogue": null,
      "duration_sec": 6,
      "location": "cafe",
      "n": 1,
      "visual_note": "morning"
    },
    {
      "action": "HUMAN-EDITED: inspector arrives and the entire cafe freezes",
      "camera": "two-shot",
      "characters": [],
      "dialogue": "just here for a scone",
      "duration_sec": 12,
      "location": "cafe",
      "n": 2,
      "visual_note": "fluor"
    },
    {
      "action": "twist",
      "camera": "close",
      "characters": [],
      "dialogue": "aha",
      "duration_sec": 12,
      "location": "cafe",
      "n": 3,
      "visual_note": "punch"
    }
  ],
  "sketch_id": "sk-demo-beat"
}
```

Beat 2's `action` and `dialogue` were replaced with the patched values; `camera`, `visual_note`, `location`, `duration_sec`, and `characters` (fields not in the PATCH body) were preserved. The same beat also got rewritten in place on `sketch.json`'s `beats` field so downstream pipelines (video gen, critic) see the edit. A `human_edit_beat` history event landed with payload `{"beat_n": 2, "fields_updated": ["action", "dialogue"]}`.

## Idea factory prompt rendering

The bundled template at `idea_factory/prompts/premise_generation.md` now carries a `{user_guidance_section}` placeholder between the Signal block and the Task block. `_build_user_guidance_section` returns either a fully-rendered `## Human guidance\n\n{text}\n` block, or the empty string.

### With guidance

```
(signal block)
- summary: chaos ensues

## Human guidance

lean into the crosswalk-volunteer angle, one location

# Task
```

### Without guidance

```
(signal block)
- summary: chaos ensues


# Task
```

(Two blank lines instead of the guidance block — the placeholder simply collapses to an empty string, so the template looks almost identical to the Phase 3 version.)

## Premise Review before / after (markdown sketch)

**Before Phase 10** — every sketch, every variant, every premise rendered at once:

```
┌──────────────────────────────────────────────────────────────────────┐
│ sk-2026-04-06-4ff7ec · signal: hn-47661231         [reject sketch]  │
│ When Virality Is the Message: The New Age of AI Propaganda          │
├──────────────────────────────────────────────────────────────────────┤
│ ┌─ CLAUDE-OPUS ─┐ ┌─ GPT-5 ──────┐ ┌─ GEMINI-2.5-PRO ─┐             │
│ │ logline #1    │ │ logline #1   │ │ logline #1        │             │
│ │ ...           │ │ ...          │ │ ...               │             │
│ │ [approve]     │ │ [approve]    │ │ [approve]         │             │
│ │ logline #2    │ │ logline #2   │ │ logline #2        │             │
│ │ ...           │ │ ...          │ │ ...               │             │
│ │ logline #3    │ │ logline #3   │ │ logline #3        │             │
│ └───────────────┘ └──────────────┘ └───────────────────┘             │
└──────────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────────────┐
│ sk-2026-04-06-256725 · signal: reddit-abc123       [reject sketch]  │
│ Another headline                                                     │
├──────────────────────────────────────────────────────────────────────┤
│ (9 more premises, all expanded at once)                              │
└──────────────────────────────────────────────────────────────────────┘
... 13 more sketches, 117 premises total on the page
```

**After Phase 10** — collapsed Gmail-style, one line per sketch:

```
┌──────────────────────────────────────────────────────────────────────┐
│ [expand all]  [collapse all]            click to expand · Space · J/K│
├──────────────────────────────────────────────────────────────────────┤
│ ▸ sk-2026-04-06-4ff7ec · signal: hn-47661231       [reject sketch]  │
│   When Virality Is the Message: The New Age of AI Propaganda        │
│   3 models · 9 premises · click to expand                           │
├──────────────────────────────────────────────────────────────────────┤
│ ▸ sk-2026-04-06-256725 · signal: reddit-abc123     [reject sketch]  │
│   Another headline                                                  │
│   3 models · 9 premises · click to expand                           │
├──────────────────────────────────────────────────────────────────────┤
│ ... 13 more collapsed sketches — all headlines, zero premise text    │
└──────────────────────────────────────────────────────────────────────┘
```

Clicking a headline expands that single sketch to reveal the full Phase 3 variant grid PLUS a fourth `human` column with a `+ add premise` button, and every premise inside every variant gains an `edit` pencil next to its `approve` button:

```
┌──────────────────────────────────────────────────────────────────────┐
│ ▾ sk-2026-04-06-4ff7ec · signal: hn-47661231       [reject sketch]  │
│   When Virality Is the Message: The New Age of AI Propaganda        │
├──────────────────────────────────────────────────────────────────────┤
│ ┌─ CLAUDE-OPUS ─┐ ┌─ GPT-5 ────┐ ┌─ GEMINI ──┐ ┌─ HUMAN ────────┐   │
│ │ logline #1    │ │ logline #1 │ │ logline #1│ │  author a new  │   │
│ │ ...           │ │ ...        │ │ ...       │ │  premise here  │   │
│ │ [approve][ed] │ │ [appr][ed] │ │ [appr][ed]│ │                │   │
│ │ logline #2    │ │ logline #2 │ │ logline #2│ │ [+ add premise]│   │
│ │ ...           │ │ ...        │ │ ...       │ │                │   │
│ │ [approve][ed] │ │ [appr][ed] │ │ [appr][ed]│ │                │   │
│ └───────────────┘ └────────────┘ └───────────┘ └────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

Clicking the headline again (or pressing `Space` on the focused card, or clicking the `collapse all` toolbar button) collapses the card back to a single line.

## Relevant JS snippets (proof of collapsed-by-default)

`backend/static/index.html` — state declaration, namespace, and per-card rendering:

```js
// Phase 10: Premise Review collapse state. All sketches start
// collapsed on page load; the set grows as the user clicks to
// expand. The window.premiseReview namespace exposes the state
// mutators so the smoke test (and any other script) can observe
// and drive the UI.
let expandedPremiseCards = new Set();

function isPremiseCardExpanded(sketchId) {
  return expandedPremiseCards.has(sketchId);
}

function togglePremiseCard(sketchId) {
  if (expandedPremiseCards.has(sketchId)) {
    expandedPremiseCards.delete(sketchId);
  } else {
    expandedPremiseCards.add(sketchId);
  }
  renderPage();
}

function expandAllPremiseCards() { ... }
function collapseAllPremiseCards() { ... }

window.premiseReview = {
  isPremiseCardExpanded,
  togglePremiseCard,
  expandAllPremiseCards,
  collapseAllPremiseCards,
  _state: () => expandedPremiseCards,
};
```

Card rendering — the `.collapsed` / `.expanded` class is derived from `isPremiseCardExpanded`, which is `false` for every sketch on first render:

```js
function renderSketchPremiseCard(kanbanCard, payload) {
  const el = document.createElement("div");
  const expanded = isPremiseCardExpanded(kanbanCard.id);
  el.className = "sketch-card " + (expanded ? "expanded" : "collapsed");
  ...
  // Click anywhere on the headline toggles collapsed/expanded.
  left.addEventListener("click", (ev) => {
    ev.stopPropagation();
    togglePremiseCard(kanbanCard.id);
  });
  ...
}
```

CSS — `.collapsed` hides the variant row entirely; `.expanded` reveals it:

```css
.sketch-card.collapsed .variant-row { display: none; }
.sketch-card.collapsed .sketch-header { margin-bottom: 0; cursor: pointer; }
.sketch-card.expanded .variant-summary { display: none; }
```

Space keybinding — toggles the focused card on the Premise Review page:

```js
} else if (
  (ev.key === " " || ev.key === "Space") &&
  stage.id === "premise_review"
) {
  // Phase 10: Space toggles the currently-focused premise card
  // between collapsed and expanded.
  ev.preventDefault();
  const card = currentActiveCard();
  if (card) togglePremiseCard(card.id);
}
```

## Deviations from the plan

| # | Deviation | Reason |
|---|---|---|
| 1 | `beats.json` is a **new sidecar file**, not the source of truth. `sketch.beats` on `sketch.json` remains canonical. | Every existing pipeline (`storyboard/pipeline.py`, `storyboard/stub_storyboard.py`, `critic/pipeline.py`, `video_gen/pipeline.py`, `backend/main.py`'s `/api/sketch/{id}/storyboard` handler) reads `sketch.beats` directly from `sketch.json`. Introducing a new source of truth would have cascaded changes through five files. Instead, the PATCH endpoint updates `sketch.beats` in place AND writes a `beats.json` sidecar that mirrors the full list. The acceptance criterion (`cat data/sketches/{id}/beats.json` shows the edited beat) is satisfied without the existing reader path breaking. If the user wants to flip the source of truth later, it's a one-file change. |
| 2 | `human_promote_with_guidance` history events are stamped by `idea_factory.factory.run_factory`, not by the `POST /api/signals/{id}/promote` endpoint directly. | The promote endpoint writes the queue manifest but doesn't create the sketch — sketch creation happens later when the factory runs (either from `stub_factory.run_factory` in the API path, or from `idea_factory.factory.run_factory` in the nightly pipeline path). The history event can only land on a sketch that exists, so I added it to `run_factory` where the sketch is created. Verified in `test_factory_stamps_human_promote_event_when_guidance_present`. The stub factory path does not yet stamp the event (documented as item 5 below). |
| 3 | The "signals page promote button" in the UI uses `stub_factory.run_factory(store)`, which does NOT currently read the `user_guidance` field out of the queue manifest. | `stub_factory` is a hardcoded three-premise generator (Phase 1 era); its prompts are fixed strings, not a template. Per Phase 10 plan section "Idea factory prompt update", the guidance passthrough is specifically about the **multi-model** factory at `idea_factory/factory.py`, which IS updated. The manifest-level write is what the plan's test asserts (`test_signals_promote_with_guidance.py`), and the factory-level read is what the plan's other test asserts (`test_idea_factory_uses_guidance.py`). Both pass. The stub factory continues to work as before but never sees the guidance. |
| 4 | I added **35 new tests** instead of the plan's ~15-20 estimate. | Each new endpoint got its own 400 / 404 edge-case coverage, and the frontend smoke test got one assertion per Phase 10 UI affordance (namespace export, default state, collapsed class, toolbar buttons, click wiring, Space key, PATCH fetch, add button, promote dialog, edit-beat button). The plan explicitly listed six test files but didn't prescribe counts; 35 felt right for the coverage surface. Final offline count is 356, not the plan's "roughly 327". |
| 5 | I did not extend `stub_factory.run_factory` to stamp `human_promote_with_guidance` or read `user_guidance`. | The plan's stated goal is to make guidance visible to **model adapters** so Claude/GPT-5/Gemini see the producer's intuition. Stub factory is a deterministic three-template pitch, not a model adapter. Touching stub_factory would couple the Phase 1 stub to a Phase 10 feature for no functional benefit — the guidance field is on the manifest for the multi-model factory to read on the next scheduled run, and the UI promote path in production happens via `pipelines/run_skeleton.py` which uses the multi-model factory, not the stub. Documented for completeness. |
| 6 | I fixed one Pydantic v2 deprecation warning: `body.dict(exclude_none=True)` → `body.model_dump(exclude_none=True)` in the beat edit endpoint. | Pydantic v2 flags the `.dict()` method for removal in v3. Caught by the test run's warnings; trivial fix. |

## Data directory state

The Phase 8 agent learned to never wipe `data/`. I followed the lesson: every test runs against `tmp_path`, and every demo walkthrough used a `tempfile.mkdtemp()` directory. The real `data/sketches/` is untouched — `ls data/sketches/` still shows the same 24 sketches (including `sk-2026-04-06-4ff7ec` from Phase 9) that existed at the start of Phase 10.

## What changes for the user (one paragraph)

With Phase 10, every review gate in ai_vids_virality is now a **co-authoring surface** instead of a binary approve/reject. On the Signals page, clicking `promote` opens a dialog with an optional "what angle / spin / setup are you thinking?" textarea — whatever the user types lands on the idea-factory queue manifest as `user_guidance`, and the next time the multi-model factory picks up that signal, every model (Claude, GPT-5, Gemini) sees a `## Human guidance` block spliced into its premise-generation prompt directly above the Task section. On the Premise Review page, cards render in a Gmail-style collapsed list — 13 sketches show 13 one-line headlines instead of 117 premises, with an `expand all` / `collapse all` toolbar, click-to-expand on the headline, and `Space` / `J` / `K` keyboard shortcuts. Expanding a card reveals the three AI variants plus a new **human** column with `+ add premise` that writes a `{sketch_id}__human.json` variant marker to the premise-review queue; each individual premise also gains an `edit` pencil that pops an inline modal for logline / synopsis / tone / twist / target length / characters. On Storyboard Review, each beat cell gains an `edit beat` button that PATCHes `action` / `dialogue` / `camera` / `visual_note` / `location` / `duration_sec` back into `sketch.beats` and a new `beats.json` sidecar. The leaderboard grows a `human` row that tracks approval rate alongside the AI models — if the user's hand-written premises outperform every model, that's a measurable signal to retune the prompts. Every new editing action appends an append-only history record (`human_promote_with_guidance`, `human_edit_premise`, `human_add_premise`, `human_edit_beat`) onto the sketch so stats and future undo can see the full collaboration trail. Zero infrastructure changes, zero new external services, zero new providers, 35 new mocked tests green, 356 total offline pass.
