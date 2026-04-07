# Phase 10 — Manual Editing + Collapsed Premise Review

## Goal

Make the system collaborative — at every gate, the human can not only approve or reject, but also **edit and add their own creative input** before the next stage runs. Plus a key UX fix: **Premise Review cards start collapsed**, showing only the topic headline, expanding only when clicked.

This phase is purely additive. No infrastructure changes, no new external services. Just new endpoints + UI that lets the human be a real co-author instead of a passive reviewer.

---

## Three editing affordances

### A. Signals page — guidance text on promote

When the user clicks **promote** on a signal, instead of immediately enqueueing it, open a **promote dialog** with:
- The signal title (read-only)
- A textarea labeled `"What angle / spin / setup are you thinking?"` (optional, can be left blank)
- A **"promote"** button and a **cancel** button

The text the user types becomes a `user_guidance` field on the signal's idea-factory queue manifest, and the **idea factory passes it to every model adapter as part of the prompt**. So when Claude/GPT-5/Gemini generate premises, they have the human's intuition baked in.

### B. Premise Review — edit + add premises

Each variant sub-card on the Premise Review page gains:
- An **edit** pencil icon on every individual premise that opens an inline edit modal: textareas for `logline`, `synopsis`, `tone`, `twist`, `target_length_sec`, `characters` (as a small repeating list)
- An **add new premise** button at the bottom of the variant column that creates a new blank premise inline (under a special model_id like `human` or `manual`)
- The **approve** button still works on edited / added premises identically — they get treated as the canonical premise downstream

In the leaderboard, human-authored / human-edited premises are tracked in their own row (`model_id: human`) with their own approval rate. Useful: if the human's hand-written premises outperform every model, that's a signal to retrain prompts.

### C. Storyboard Review — edit beat text before regen

Each beat cell on the Storyboard Review page gains an **edit** icon on the beat text. Click it → inline modal with editable `action`, `dialogue`, `camera`, `visual_note`, `location`, `duration_sec`. Save → updates the beat in `data/sketches/{id}/beats.json` → next regen for that frame uses the new text.

---

## The collapse change (Premise Review)

Cards on Premise Review currently show all variants expanded by default. With 13 sketches each having 3 variants × 3 premises, that's 117 premises rendered at once — overwhelming.

**New default state per sketch card:**
- Collapsed view: just the headline (signal title) + the sketch ID + the variant count summary (e.g. `3 models · 9 premises · click to expand`) + the reject button
- Click anywhere on the card to expand → reveals the full variant grid
- Click again (or the collapse arrow) to collapse
- **All sketches start collapsed on page load**
- A `expand all` / `collapse all` toggle at the top of the page for power use
- Keyboard shortcut: `Space` toggles the currently-focused card; `J/K` advances focus to the next/previous card

This is the same pattern as a Gmail-style conversation list.

---

## New API endpoints

- `POST /api/signals/{signal_id}/promote` — body now accepts `{"guidance": "optional user text"}`. Stored in the queue manifest at `data/queues/idea-factory/{signal_id}.json` under a new `user_guidance` field. If empty, the field is omitted (no behavior change).
- `PATCH /api/sketch/{sketch_id}/premise` — body `{"model_id": "...", "premise_index": N, "premise": {logline, synopsis, tone, twist, target_length_sec, characters}}`. Updates the variant in place. Marks the sketch's history with a `human_edit` event.
- `POST /api/sketch/{sketch_id}/premise` — body `{"premise": {...}}`. Adds a new premise as a `human` variant. Returns the updated sketch.
- `PATCH /api/sketch/{sketch_id}/beat/{beat_n}` — body `{"action": "...", "dialogue": "...", ...}`. Updates the beat in `beats.json`. Marks history.

All four endpoints use the existing Store layer — no new persistence work.

## Idea factory prompt update

`idea_factory/prompts/premise_generation.md` gets a new optional section:

```
{user_guidance_section}
```

The factory fills this with `## Human guidance\n\n{guidance_text}\n` if `user_guidance` is present in the queue manifest, or with empty string otherwise. Models that receive guidance treat it as creative direction from the producer.

## State machine + leaderboard

- New `model_id: "human"` slot in the leaderboard. Counted alongside the AI models.
- Sketch history events: `human_edit_premise`, `human_add_premise`, `human_edit_beat`, `human_promote_with_guidance`.

## Tests

- `test_signals_promote_with_guidance.py` — the guidance text gets stored in the queue manifest, omitted if empty
- `test_idea_factory_uses_guidance.py` — the prompt template includes the guidance section when present
- `test_premise_edit_endpoint.py` — PATCH updates the variant, adds history event
- `test_premise_add_endpoint.py` — POST adds a new human variant, leaderboard counts it
- `test_beat_edit_endpoint.py` — PATCH updates the beat
- `test_premise_review_collapse.py` — frontend smoke test of the collapse markup (assert the JS module exposes the expected expand/collapse state functions)

## UI updates (single-file, vanilla JS)

- Premise Review page: new collapsed-by-default rendering, click-to-expand, `Space`/`J`/`K` keyboard wiring, expand-all toggle, edit + add premise inline modals
- Signals page: promote button now opens a dialog with the guidance textarea
- Storyboard Review page: each beat cell gains an edit icon → inline beat editor

---

## Out of scope

- Multi-edit history / undo (just append to history, don't track diffs)
- Collaboration with multiple humans (single-user app)
- Drag-and-drop reordering of premises or beats

---

## Demo

Run `pytest -m "not network and not llm and not gemini and not video and not critic and not publish and not fal"`. Then:
- Promote a signal with guidance text via the UI, confirm the queue manifest contains `user_guidance`
- Edit a premise inline, confirm the sketch.json reflects the change with a history event
- Add a new human premise, confirm leaderboard increments
- Toggle a card collapsed → expanded → collapsed
- Edit a beat's action text, confirm beats.json reflects the change

---

## Reporting

`phases/phase-10-report.md` with file tree, pytest summary, before/after screenshots (or markdown sketches) of the collapsed Premise Review page.
