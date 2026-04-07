# Section 1, Step 4 — Response Contracts (Builder D notes)

## What I wrote

Two new contract files in `eywa-system/contracts/`:

- `buddy-node-authored-response-contract.md` — schema Buddy must return on every host turn (`pick_subgraph` or `done`)
- `worker-node-authored-response-contract.md` — schema a worker must return after one assigned execution

These two replace super-eywa's single `node-authored-response-contract.md` and capture the strategic-vs-tactical split at the authoring protocol level.

## Judgment calls

- **`decision_notes` is optional on Buddy's schema, not required.** The spec said "strongly encouraged but optional" and I held to that. Making it required would punish trivial obvious turns. Documented its load-bearing status in Notes so the encouragement actually shows up at author time.
- **`final_answer_summary` kept as optional on `done`.** It doesn't appear directly in `03-buddy-loop.md`, but the spec asked for it and the learning-surface argument is real — the buddy-turn table needs a one-line column for `done` outcomes that mirrors `output_summary` for workers. Optional rather than required because `final_answer` itself can be short.
- **`pick_subgraph` and `done` are flat siblings of `turn_decision`, not nested under a discriminator object.** Matched super-eywa's flat shape so the JSON stays scannable. The validation rules section explicitly forbids the wrong-branch fields rather than using a JSON Schema `oneOf`.
- **`slot_fills` field names match `slots_resolved` field names exactly** (`instructions`, `variable_overrides`, `artifact_refs`). The acceptance criteria called this out and I kept it identical so the runtime can do a direct copy from the authored response into the materialized instance with no renaming.
- **`fail_fast` is an object with `triggered` + `reason`, not a top-level boolean + sibling string.** Keeps the escape hatch self-contained and visually distinct from normal output fields. Matches the shape shown in `04-workers-slots.md`. `triggered: false` is documented as equivalent to omitting the field, so the success example can either include it (as I did, for clarity) or skip it entirely.
- **Required-when-triggered: `reason` is required only when `triggered` is `true`.** The `04-workers-slots.md` example shows `reason: null` when `triggered: false`, so I left that as a valid form rather than forcing absence. Validation rule names the conditional cleanly.
- **`result_type` is loose free-form, not an enum.** The design doc lists examples (`summary | plan | code | data | finding | ...`) with explicit "..." — I treated that as deliberate looseness and did not pin a closed set. The slot-execution learning surface can do its own bucketing later.
- **`output` typed as "structured object or string" rather than locked to one.** Matches Buddy's `final_answer` decision and reflects that workers' tactical outputs vary wildly across task types.
- **No `Planned Buddy-Eywa Extensions` section on either contract.** Per the explicit "do not" in the spec, and consistent with Builder C's choice to omit it from buddy-eywa-native contracts.
- **Explicit anti-list of orchestration fields in worker validation rules.** I named every super-eywa decision field that's NOT allowed (delegate, transmute, execute_locally, helpers, synthesis_brief, message_for_next_agent, next_node_overrides, chosen_subgraph_type, slot_fills, turn_decision). It reads aggressive but the spec was clear that "no orchestration branching" should be loud, and the worker contract's whole point is what's missing. Also reinforces for any future builder skimming the file that the radical simplicity is intentional, not an oversight.
- **Worker `output_summary` is required.** The spec listed it under required top-level fields. It's strict because the buddy-turn accumulated-state view depends on it being present for every prior worker — making it optional would force the runtime to synthesize one when missing, and synthesized summaries are noisy.
- **Buddy example uses `delegate_fanout_synthesize` with the same Riemann hypothesis content as the `subgraph-instance-contract.md` example.** Lifted intentionally so a reader can see the same task flow through Buddy's authored response → into the materialized instance. Cross-document continuity helps the contracts read as a set.

## Cross-reference consistency

Verified each cross-reference against the actual contract files:

- **`subgraph-type-contract.md`** — referenced via `chosen_subgraph_type` (the `name` field) and the slot label set (`slots` keys). Both fields exist with those exact names in Builder C's file.
- **`subgraph-instance-contract.md`** — referenced via `slots_resolved` keys `instructions`, `variable_overrides`, `artifact_refs`. All three exist with those exact names in Builder C's file. The runtime-owned fields `node_id` and `buddy_policy` are correctly documented as runtime-added, not Buddy-authored.
- **`artifact-record-contract.md`** — referenced via `artifact_id` (for both `artifact_refs` and worker `supersedes`), the allowed `type` values, and the runtime-owned write fields (`artifact_id`, `created_by_node_id`, `version`, `content_ref`, `content_size_bytes`). All match Builder C's file.
- **`subgraph-instance-contract.md` status `failed_fail_fast`** — confirmed exact spelling in Builder C's status enum.
- **`node-record-contract.md`** — referenced as the preservation surface for both authored responses. Note: the existing `node-record-contract.md` is a Builder B port from super-eywa and still has super-eywa's `final_action_type` and `orchestration` field shapes. I did NOT update it; that's outside my scope and is presumably retired in a later section's update to that contract. Flagging here because the cross-reference is technically pointing at a soon-to-be-stale shape.
- **`slots_resolved` field-name mapping** — the spec was explicit: `instructions` → `instructions`, `variable_overrides` → `variable_overrides`, `artifact_refs` → `artifact_refs`. My contract uses identical names on both sides. Direct copy at runtime, no renaming.

One thing I had to interpret rather than read directly:

- The exact mechanism by which the runtime validates `chosen_subgraph_type` against the loaded library at turn time is not spelled out anywhere. I documented the rule ("must match the `name` of a subgraph type in the currently loaded library") and left "loaded library" as a runtime concept that lands in Section 6. Correct conceptually but the validator implementation will need to define what "loaded" means.

## Voice consistency with Builder B and C

Patterns kept:

- Same heading order: `Purpose` → `Required Fields` → field-shape sections → `Example Shape(s)` → `Validation Rules` → `Relationship to Other Contracts` → `Notes`
- Same terse, structural tone — no marketing words
- Same JSON code-fence style for examples
- Same flat `Required Fields` bullet list at the top, with shapes expanded in dedicated sections below
- Same lowercase-bullet style in `Notes` (e.g., "this is the only authoring surface...")
- Same convention of using cross-references via relative markdown links

Intentional divergences:

- **Both contracts have a `Validation Rules` section** following Builder C's precedent. Builder B's ports do not. The validation surface for these authored shapes is rich enough that prose-burying it would be worse.
- **Both contracts have a `Relationship to Other Contracts` section.** Builder C used a similar idea inline ("Relationship to subgraph_type"); I made it a top-level section because the response contracts touch four other contracts each and the relationships deserve their own heading.
- **No `Planned Buddy-Eywa Extensions` section** on either contract — buddy-eywa-native from day one, matching Builder C's choice for the structural contracts.
- **`schema_name` / `schema_version` instead of `contract_name` / `contract_version`.** This matches super-eywa's `node-authored-response-contract.md` (which uses `schema_name`) and reflects the conceptual difference: the response shapes are model-authored schemas that the runtime validates, while packets and records are runtime-authored contracts. Builder B's ports also preserve this distinction (run-packet/node-packet/node-record use `contract_name`, node-output uses `schema_name`/equivalent). I kept the convention rather than collapsing it.
- **Allowed-values sections (`Allowed turn_decision Values`)** match super-eywa's style (Builder B's source material) for response contracts specifically. Builder C's structural contracts didn't need them.

## Uncertainties / things to revisit

- **`output` and `final_answer` typing.** I left both as "structured object or string, task-appropriate." If later sections need a stricter type (e.g., always-string for benchmark grading), this becomes a v2 bump. Flagged.
- **`fail_fast` shape with `triggered: false, reason: null` versus omission.** I documented both as valid. If runtime validators want a single canonical shape, they should normalize on parse. Not a contract concern.
- **Whether `output` should be required to be a string when `result_type` is `"answer"`.** I did not couple them. If grading wants that coupling, it lands in Section 11's grading layer, not here.
- **`variable_overrides` validation surface.** I did not enumerate which variable names Buddy is allowed to override. The full variable set lives in `node-packet-contract.md` and isn't yet finalized for buddy-eywa. Left unconstrained for now; later sections may want a whitelist.
- **`artifact_refs` membership check timing.** "At turn time" is what I wrote, but the manifest can change between turns within a host's loop. The runtime needs to lock the manifest snapshot Buddy was shown when it built the prompt and validate against that snapshot, not whatever the manifest looks like when validation runs. Flagging for the runtime builder.
- **`final_answer` and `final_answer_summary` interaction.** Both fields exist on `done`. Nothing prevents `final_answer_summary` from being inconsistent with `final_answer`. I documented that the summary is "for the learning surfaces" but did not add a coherence rule. Probably fine — it's Buddy's own authored content and inconsistency would just hurt its own future self.

## Departures from super-eywa's `node-authored-response-contract.md`

The whole point of Step 4 is to replace super-eywa's mixed-role response. The notable departures, listed because the divergence IS the design:

- **Two contracts, not one.** Super-eywa's single contract branched on `orchestration_decision`. Buddy-eywa has two distinct authoring surfaces (`buddy_node_authored_response`, `worker_node_authored_response`) with no shared schema name.
- **`turn_decision` has exactly two values** (`pick_subgraph`, `done`). Super-eywa's `orchestration_decision` had four (`execute_locally`, `transmute`, `delegate`, `report_problem`).
- **Workers have NO orchestration decision values at all.** No `delegate`, no `transmute`, no `execute_locally`, no `report_problem`. The closest analog is `fail_fast`, which is a signal not a decision and explicitly cannot propose alternatives.
- **`helpers` is gone.** Super-eywa let any node author a helper list inline. Buddy-eywa moves this entirely into `chosen_subgraph_type` + `slot_fills` — Buddy picks a type whose slots define the helper structure, then fills their instructions.
- **`message_for_next_agent` and `next_node_overrides` are gone.** Super-eywa's `transmute` shape was a way to reframe a task and pass it down. In buddy-eywa, that pattern is just "Buddy picks a single-slot type with the reframed instructions on the next turn." No special schema.
- **`synthesis_brief` is gone.** Super-eywa attached it to delegation. In buddy-eywa, synthesis is a slot in the chosen subgraph type, with its own instructions filled like any other slot.
- **`response` (super-eywa's `execute_locally` field) is split into worker `output` and Buddy `final_answer`.** Super-eywa used the same field name for both "the worker did the work itself" and "the agent is reporting an answer." Buddy-eywa separates them because the authoring roles are different.
- **`report_problem` is gone.** Super-eywa let any node escalate by switching its decision verb. Buddy-eywa has `fail_fast` for workers (a signal, not a strategic move) and nothing equivalent for Buddy — if Buddy thinks the host is unsolvable, Buddy declares `done` with a `final_answer` that explains the problem. The escalation is content, not a schema branch.
- **Workers cannot author follow-up structure of any kind.** Super-eywa's authoring surface mixed "what I did" with "what should happen next." Buddy-eywa's worker schema only has "what I did" plus the fail-fast escape hatch. Strategy is exclusively Buddy's.
- **`schema_name` values are role-specific** (`buddy_node_authored_response` vs `worker_node_authored_response`) instead of a single shared `eywa_node_response`. Makes the role visible at the protocol level so a parser can route on the schema name alone.

## What the next reviewer should pay extra attention to

- **Slot-fill field-name parity with `subgraph-instance-contract.md`.** Verified, but re-check that `instructions` / `variable_overrides` / `artifact_refs` are spelled identically on both sides — the runtime depends on direct copy.
- **`failed_fail_fast` status spelling** matches Builder C's `subgraph-instance-contract.md` exactly. Cross-checked.
- **The "no orchestration branching" anti-list in worker validation rules** is intentionally aggressive. If the voice feels too loud, it can be softened, but the explicitness is the point.
- **The pointer to `node-record-contract.md`** is technically pointing at Builder B's port which still has super-eywa's `final_action_type` / `orchestration` shape. That contract presumably gets its `final_action_type` enum revisited in a later section; the response contracts here will read cleaner once that catches up.
- **`schema_name` vs `contract_name` distinction** — kept it on purpose to match super-eywa's response-vs-record convention. If buddy-eywa wants to collapse these into one envelope name, it's a sweep across all contracts and not just these two.
