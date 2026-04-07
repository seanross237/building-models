# Section 1 — Doc Update I: 03-buddy-loop.md notes

## What I changed

- "What Buddy decides" rewritten from four things to three things, collapsing "which type" + "context bindings" into one bullet, removing "fill slots", and adding an explicit `meta_prompt` pointer plus a paragraph on the minimal authoring surface.
- Pseudocode block: `slot_fills` -> `context_bindings` + `variable_overrides`; `prior_turns` records now capture `context_bindings` instead of `slot_fills`.
- "What Buddy's prompt looks like conceptually" updated: prior-turn recap mentions context_bindings instead of "instructions"; the JSON OUTPUT example now matches the buddy-node-authored-response contract (schema_name, schema_version, turn_decision, chosen_subgraph_type, context_bindings, variable_overrides, decision_notes); the LIBRARY listing line now mentions buddy_bound_variables; the closing prose changed from "what class of work" to "which bundle in the library is the right next move".
- "Recursion via nesting" got a single sentence clarifying that the nested host's task text is the slot's `rendered_prompt` (template-substituted `meta_prompt`).
- Lighter touches on "Pivots are free", "Fail-fast", and the "Buddy does not" bullet list to remove any Option 1 phrasing.

## Judgment calls

- **Three things, not four.** I collapsed "which type" + "context bindings" into one numbered item rather than keeping them as separate bullets. They are conceptually a single decision under Option 3 — picking a bundle and resolving its required variables together — and the contract treats them as a single `pick_subgraph` shape. Splitting them felt artificial.
- **Where to put the "minimal authoring surface" paragraph.** The brief said "in the 'What Buddy decides' section or near it". I put it in that section, immediately after the "Buddy never authors per-slot instructions" sentence, so the section flows: enumerated decisions -> what Buddy never authors -> why minimalism is load-bearing. This kept the section self-contained and meant the "Buddy does not:" bullet list at the end of the section still reads cleanly. ~5 sentences as the brief suggested.
- **"Buddy does not:" bullet list.** I added "Author per-slot instructions" as the second bullet (after "Invent new subgraph types") because that pairing felt natural — both are forms of authoring that belong to the Scientist or to the bundle. I also updated the last bullet from "beyond one of the four things above" to "beyond one of the three things above" to match the new count.
- **Pseudocode `prior_turns` payload.** I included `context_bindings` but not `variable_overrides` in the prior-turn record. The brief asked for chosen_type + context_bindings + terminal_output explicitly. Variable overrides are arguably worth preserving for replay too, but they live on the materialized instance and the response contract; not duplicating them in the pseudocode keeps the loop sketch tight. Flagging this as a possible future addition if the actual replay system wants it inline in accumulated_state.
- **Conceptual prompt — prior-turn recap wording.** I rewrote "with instructions 'implement step 1 of the plan'" to "with empty context_bindings" because the seed types both have empty buddy_bound_variables, and inventing a hypothetical bundle for the example would have introduced noise. This makes the example slightly less colorful but accurate to the seed library. Alternative was to invent a hypothetical `revise_plan_given_review`-style bundle inline, but I judged the consistency win was worth the loss of color.
- **JSON OUTPUT example schema completeness.** I matched the contract's required fields verbatim (schema_name, schema_version, turn_decision, chosen_subgraph_type, context_bindings, variable_overrides, decision_notes) rather than abbreviating. The original was a 4-line stub. The new version is ~10 lines but it gives the reader an actual contract preview without making them open the contract file. Within the 15% length budget.
- **Fail-fast section.** I left the section essentially as-is per the brief and only updated step 4 to "pick a different bundle, possibly with different context bindings, re-plan, give up". The old phrasing didn't have any Option 1 language to fix; I touched it just to make Option 3 vocabulary explicit.
- **Pivots section.** Original last sentence said "Buddy makes a different pick on the next turn based on what's in the accumulated state." I extended it with "— a different type, different bindings, or different overrides" to enumerate the actual axes of pivot under Option 3, per the brief.
- **Recursion section.** I added a single trailing clause to the first paragraph clarifying rendered_prompt -> nested host task. I considered making it a separate paragraph but a clause inline kept the section's length stable and the flow intact. Also added "binds context" to the second paragraph's "It picks subgraphs, composes turns, declares done" so the nested loop's decisions match the new "What Buddy decides" enumeration.
- **"Why multi-turn buddy does NOT create two control planes" section.** Left untouched. I scanned it for "fill" and Option 1 language; it doesn't reference Buddy's authoring surface at all. It only argues against multi-turn-inside-slots, which is unchanged under Option 3.
- **Budget controls + "What happens when Buddy runs out of turns" sections.** Left untouched per the brief; double-checked that neither references slot_fills or per-slot instructions.

## Things left alone that might warrant reconsideration

- The "Recursion via nesting" diagram still shows generic slot names (worker_a, synthesizer, subworker_a). Under Option 3 these would have specific meta_prompt template variables, but the diagram's purpose is structural, not content-bearing. Left as-is.
- The "Pivots are free" section's bullet sequence is intentionally vague ("approach A", "different approach"). I considered making it concrete (e.g., "approach A = delegate_fanout_synthesize, different approach = just_execute") but the abstract version reads more cleanly and the section's job is to show the temporal pattern, not name specific bundles.
- The conceptual prompt's PRIOR TURNS recap shows two `delegate_fanout_synthesize` / `just_execute` turns with empty bindings. If a future seed library entry has buddy_bound_variables, this example would benefit from showing a non-empty bindings recap. Not adding now because the seed library doesn't have such a type. Flagging.

## Option 1 language I noticed in OTHER design docs (did not edit)

- I did not open `01-philosophy.md`, `05-host-vs-worker.md`, `06-learning-surfaces.md`, `07-cost-model.md`, `08-wins-and-tradeoffs.md`, or `09-build-plan.md`. Per the spec I was not to touch them. I cannot confirm they are clean.
- Builder H's notes (`section-1-doc-update-h-02-subgraph-types-notes.md`) likely covers anything they noticed in 02. I deferred to that and did not duplicate the sweep.
- The four ported contracts (`run-packet`, `node-packet`, `node-output`, `node-record`) and `worker-node-authored-response-contract.md` and `artifact-record-contract.md`: per Builder G's revision notes, these were checked and don't reference the old shape directly. I did not re-verify.

## Things I wasn't sure about

- Whether to include `variable_overrides` in the pseudocode's prior-turn record. I left it out for terseness; see judgment call above. If Builder J's `04-workers-slots.md` or any later doc shows `variable_overrides` flowing into accumulated_state for replay, this should be reconciled.
- Whether the JSON OUTPUT example in the conceptual prompt should show `final_answer` / `final_answer_summary` for the `done` branch as a second sub-example. I went with one example showing the `pick_subgraph` shape, since that's the more common path and the `done` shape is described in the buddy-response contract. A two-example version would be more complete but would push the section length up further.
- Whether to add a forward-pointer to `06-learning-surfaces.md` from the new "minimal authoring surface" paragraph, since that paragraph claims minimalism is load-bearing for the learning signal. I held off because the existing doc has minimal cross-doc links and adding one felt like scope creep.

## Files touched

- `/Users/seanross/kingdom_of_god/home-base/eywa/buddy-eywa/03-buddy-loop.md`
- this notes file

## Files NOT touched (per the spec)

- `eywa-system/contracts/*` (all contract files)
- `02-subgraph-types.md` (Builder H's territory)
- `04-workers-slots.md` (Builder J's territory)
- `01-philosophy.md`, `05-...`, `06-...`, `07-...`, `08-...`, `09-...`
- anything under `super-eywa/`

## Length check

- Original: 154 lines
- Updated: 164 lines (+6.5%)
- Within the 15% budget.
