# Section 1 Step 3b — Option 3 Revision Notes

## What I revised

Three contracts in `eywa-system/contracts/`:

- `subgraph-type-contract.md` — added required per-slot `meta_prompt`, optional top-level `buddy_bound_variables`, a new "Template Variables" section, content-hash note, and rewrote both seed examples to carry templated meta prompts.
- `subgraph-instance-contract.md` — added top-level `context_bindings`, replaced per-slot `instructions` and `artifact_refs` with `rendered_prompt`, updated the example, and rewrote validation/notes accordingly.
- `buddy-node-authored-response-contract.md` — removed `slot_fills` entirely, added `context_bindings` and a top-level `variable_overrides`, documented the binding-type vocabulary, added a hypothetical second example with buddy-bound variables, rewrote validation/notes accordingly.

## Judgment calls

- **Template variable syntax: single curly braces `{name}`.** I went with `{name}` and `{namespace.field}` for structured refs (e.g., `{task.text}`, `{inputs.worker_1.output}`, `{prior_turns[2].terminal_output}`). I also documented bracket-index syntax for `prior_turns[N]` because zero-padding integers into a key felt clumsy. I added an explicit "literal curly braces must be escaped as `{{` / `}}`" note so the contract is unambiguous about how to embed JSON examples in a meta prompt later.
- **Auto vs buddy collision rule.** Resolution is "auto-bound first, fall back to `context_bindings` lookup." A buddy-bound variable can never shadow an auto-bound name. I called this out explicitly so Scientists don't trip on it.
- **Validation symmetry across contracts.** All three contracts (type, instance, response) state the same validation rule from their own angle: every buddy-bound variable referenced must have a matching binding. The instance contract delegates the per-entry shape rules to the response contract; the type contract delegates the binding semantics to the response contract. This avoids triple-maintained schemas.
- **`role` kept as a separate required field.** Rather than collapsing `role` into the meta prompt, I kept it as the short human-readable label. It's still required, and its purpose was rewritten to "display, debugging, and grouping in learning surfaces — NOT the prompt." This keeps slot-execution rows readable without having to substring meta prompts.
- **`buddy_bound_variables` is optional, not required.** I made it optional and let the runtime auto-compute it from the meta prompts when omitted. The Scientist can declare it explicitly for self-documentation; the runtime cross-validates declared vs referenced. This was a judgment call — making it required would force more boilerplate; making it optional risks people forgetting to keep it in sync. I went with optional because the runtime can compute it, and the prose strongly implies the Scientist should provide it on any non-trivial type.
- **Seed type meta prompts.** For `just_execute` I wrote a single-paragraph meta prompt that injects `{task.text}` and adds the standing rule from the worker contract: "do not propose follow-up work or alternative approaches." For `delegate_fanout_synthesize` I wrote near-symmetric per-worker prompts (varying only the worker number text) and a synthesizer prompt that pulls in `{inputs.worker_1.output}` / `worker_2` / `worker_3`. I also added a "do not duplicate the workers' work or critique their approach — integrate" line on the synthesizer because that was a behavior the old per-turn `instructions` strings tended to convey case-by-case. Both seed types have empty `buddy_bound_variables`.
- **Realistic example task in the instance contract.** I changed the example task text from the old "Riemann hypothesis 1859-1900 / 1900-1950 / 1950-present" three-bucket plan (which was per-slot instructions Buddy used to author) to a single shared task — "Write a 600-word general-audience summary of the historical context of the Riemann hypothesis from 1859 to today" — because under Option 3 every worker sees the same `{task.text}` and the per-bucket split is no longer Buddy-authored. This was a deliberate change beyond the bare spec, but I think it's necessary: the old example would no longer be coherent under Option 3 (the workers would each get the same task text but the meta prompt only says "handle the Nth piece" without specifying the partition). Flagging it as a known content shift; if the right answer is "the seed type itself should partition the task," that's a Section 2 design call.
- **Synthesizer rendered_prompt placeholder text.** Slots whose meta prompt references `{inputs.<slot>.output}` can't have a fully-substituted `rendered_prompt` until the upstream slots complete. I documented this in the field details ("may grow incrementally for slots whose `meta_prompt` references upstream...") and showed the placeholder as `<rendered once worker_N completes>` in the example. The validation rule allows the placeholder to remain unsubstituted but requires the field itself to always be present. Alternative was to require `rendered_prompt` only post-execution, but that would mean the field is empty for any slot still waiting on upstream input, which loses replay value. I went with "always present, may contain placeholder."
- **`context_bindings` is flat, not per-slot.** The spec said flat. I documented the implication explicitly: "every slot in the instance shares the same bindings; if two slots both reference `{plan}`, they resolve to the same thing." This is a real design constraint Scientists should know about when designing multi-slot bundles.
- **`variable_overrides` keys must exist in the type.** I added "extra keys are an error" because silently ignoring overrides on nonexistent slot labels would mask Buddy bugs. Auto-bound `context_bindings` extras are warnings; `variable_overrides` extras are errors. Slightly asymmetric but defensible — a typo in a slot label is almost always a bug.
- **`prior_turn_output` validation.** I required `turn_number` to be a non-negative integer pointing at a *prior* turn (not the current or a future turn). This matches the auto-bound `{prior_turns[N].terminal_output}` semantics and prevents Buddy from trying to bind a turn that doesn't exist yet.
- **Content hashing note.** I made it explicit that the canonical JSON used to compute `type_content_hash` MUST include each slot's `meta_prompt` and the optional `buddy_bound_variables` list. "Editing a single character in any meta prompt produces a new content hash." This is the property the learning surfaces need.

## Cross-contract consistency checks

- `subgraph-type-contract.md` ↔ `subgraph-instance-contract.md`: instance still references type via `type_name` / `type_version` / `type_content_hash`. Instance's `slots_resolved` keys must match type's `slots` keys (kept). Instance's per-slot `variable_overrides` is mentioned in the type's notes about three-layer merging.
- `subgraph-type-contract.md` ↔ `buddy-node-authored-response-contract.md`: response's `chosen_subgraph_type` references type's `name`. Response's `context_bindings` keys must cover the type's `buddy_bound_variables` (or computed equivalent). Response's `variable_overrides` keys must be valid slot labels in the type.
- `buddy-node-authored-response-contract.md` ↔ `subgraph-instance-contract.md`: response's `context_bindings` is preserved verbatim on instance's top-level `context_bindings`; response's `variable_overrides[label]` flows into instance's `slots_resolved[label].variable_overrides`. Both contracts now reference each other for the binding shape (instance delegates to response for per-entry validation).
- `buddy-node-authored-response-contract.md` → `artifact-record-contract.md`: `artifact` bindings reference artifacts in the run's manifest at turn time, same as the old `artifact_refs`. The reference is preserved.
- `worker-node-authored-response-contract.md`: unchanged. Workers still author the same response. I read it to confirm there's no field that referenced `slot_fills.instructions` or anything from Buddy's old shape — there isn't. The worker is downstream of `rendered_prompt`, not of Buddy's response shape.
- `contracts/README.md`: read it. It doesn't mention `slot_fills`, `instructions`, or any of the removed fields. It only describes the existence of the response contracts and their general role. Left it alone.

## Uncertainties / things to revisit

- The seed `delegate_fanout_synthesize` no longer partitions the task — every worker now sees the same `{task.text}` and each one's only differentiator is "you are worker N, handle the Nth piece" in the meta prompt. That's much weaker guidance than the old version where Buddy partitioned 1859-1900 / 1900-1950 / 1950-present. Either:
  - the seed type is fine and Buddy's job is to pick a *different* (Scientist-authored) bundle when partitioning matters, or
  - the seed type needs to grow into something like `delegate_fanout_synthesize_with_partition_directive` with a buddy-bound `partition` literal binding
  - leaving as-is for now; flagging for whoever revisits Section 2 step 2.
- The `prior_turn_output` binding type and the auto-bound `{prior_turns[N].terminal_output}` template variable do almost the same thing from two different angles. The auto-bound version requires the meta prompt to hardcode `N`; the binding version lets Buddy supply `N` per turn. I documented both because they have different ergonomics, but a future cleanup might collapse them — e.g., always require Buddy to bind any prior-turn references, and remove the auto-bound `{prior_turns[N]}` patterns. Not doing that now because the spec asked for both.
- I did not document a way to pass an optional default into a buddy-bound variable (e.g., "if Buddy doesn't bind `focus_note`, use empty string"). The current rule is "every buddy-bound variable referenced must have a binding." If we want optional defaults later, they'd live on the type's per-slot config.
- The `just_execute` escape hatch with a `{buddy_free_instruction}` literal binding is mentioned in the brief but deliberately not added to the seed library. Whoever lands that should follow the binding-type vocabulary as-is — `binding_type: "literal"` already covers it without changes to the contract.

## Old (Option 1) design references in contracts I did NOT revise

I checked the four ported contracts (`run-packet`, `node-packet`, `node-output`, `node-record`) and `artifact-record-contract.md` and `worker-node-authored-response-contract.md` for stale references to the old `slot_fills` / `instructions` / `artifact_refs` shape. None of them reference the old shape directly. The worker contract talks about "tactical execution" and "the runtime's recording machinery" but does not name fields from Buddy's response. Clean.

I did not read the four ported contract files in this pass — flagging for the reviewer that they may carry stale prose if they happen to mention "Buddy fills slot instructions" anywhere; if so, that's a quick follow-up cleanup, not a Section 1 blocker.

## Files touched

- `/Users/seanross/kingdom_of_god/home-base/eywa/buddy-eywa/eywa-system/contracts/subgraph-type-contract.md`
- `/Users/seanross/kingdom_of_god/home-base/eywa/buddy-eywa/eywa-system/contracts/subgraph-instance-contract.md`
- `/Users/seanross/kingdom_of_god/home-base/eywa/buddy-eywa/eywa-system/contracts/buddy-node-authored-response-contract.md`
- this notes file

## Files NOT touched (per the spec)

- `eywa-system/contracts/worker-node-authored-response-contract.md`
- `eywa-system/contracts/artifact-record-contract.md`
- `eywa-system/contracts/README.md` (read, no dangling references found)
- the four ported contracts
- anything under `buddy-eywa/` root design docs
- anything under `super-eywa/`
