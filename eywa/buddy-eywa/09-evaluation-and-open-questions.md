# 09 — Evaluation and Open Questions

## Evaluation summary

During the design conversation on 2026-04-07, two subagents were spawned to pressure-test the direction: a Claude-based Plan subagent and a Codex-based rescue subagent. The Plan subagent returned a thorough evaluation; the Codex subagent did not return a substantive response (returned "ok" only and can be re-run later if desired).

The Plan subagent's evaluation is reproduced below, lightly edited for integration into this doc.

### Top strengths identified

1. **Aligns with the north star.** Pushes more behavior into named, comparable variables (subgraph types) instead of imperative orchestration. Bonsai/Scientist get a clean catalog to reason over.
2. **Recursion through one primitive.** "A slot with `buddy: always` is itself a host" is genuinely elegant — same DNA at every level, which is exactly the node-first promise.
3. **Clean learning unit.** Subgraph type + slot fillings + outcome is a much better atomic record than "what did `agent_chooses` decide on turn 3" — the Scientist can A/B at the type level and per-slot variable level.

### Top risks identified

1. **Two control planes coexist** (original concern). If multi-turn nodes inside slots AND a multi-turn Buddy loop wrapping them both exist, that's two recursion mechanisms with different semantics.

   **Resolution adopted:** slots are strictly single-turn. All adaptivity lives at Buddy boundaries. There is only one control plane — the Buddy loop, nested recursively. This is baked into the design in `04-workers-slots.md`.

2. **Buddy turn boundary becomes a god object.** All adaptivity migrates there. Risk that Buddy becomes the kitchen-sink prompt (pick subgraph, fill slots, judge prior outputs, decide done).

   **Partial resolution:** Buddy's output schema is tight — four fields only (type, fills, variable overrides, done vs pick). But the prompt template does need to carry a lot of context (prior turns, artifact inventory, library summary). Mitigation is to keep Buddy's prompt well-structured and to record it faithfully so the Scientist can watch for signs of prompt bloat reducing decision quality.

3. **Subgraph-type proliferation without theory.** The Scientist will happily generate `delegate_fanout_synthesize_v7_with_review_lite`. Without a strong "what is the same vs different" equivalence relation, the catalog becomes folklore and learning signal degrades faster than it accumulates.

   **Resolution adopted:** content-addressed type identity. Every subgraph instance records the content hash of the type spec it used. Two types with identical structure are automatically recognized as equivalent. The Scientist has a clean grouping key for analyses even as the library grows organically.

4. **Large DSL surface area.** `inputs_from` + per-slot variable defaults + buddy policy + early-terminate + artifact refs adds up to a real workflow language.

   **Partial resolution:** start with only the 2-type seed library and the minimum schema. Drop the `inputs_from` feature for v1 if linear slot order covers the seeded types (it does for `just_execute` and for the "parallel workers → synthesizer" shape of `delegate_fanout_synthesize`, which only needs the synthesizer to reference its workers).

   **Partially unresolved:** as new types get added to the library, the DSL surface will grow. Discipline is required to keep the spec schema minimal and to resist feature creep from individual type proposals.

5. **Migration shim + backfill is a trap.** Writing a script that retroactively wraps old runs in the new format is the kind of work that quietly takes 2x estimate and entrenches the new model before it's been validated on live runs.

   **Resolution adopted:** no write-time backfill. Use a read-time adapter for historical data if needed. Old run files stay untouched on disk.

6. **Recursion budgets are subtle.** `max_buddy_turns_per_host` per level multiplies through the tree. Pathological cost blowups will be hard to predict and debug.

   **Resolution adopted:** three hard budgets at run level: `max_buddy_turns_per_host`, `max_host_depth`, `max_total_nodes_per_run`. The last one is the global safety net that catches multiplicative blowups regardless of per-host settings.

7. **Fail-fast as the only escape hatch is brittle.** Real runs will want partial success, retry-with-different-variables, late-binding context — all things pure-DAG forbids.

   **Partial resolution:** the Buddy loop handles all of these at the turn boundary. "Partial success" = Buddy sees some workers succeeded and some fail-fasted and picks a follow-up that builds on what worked. "Retry with different variables" = Buddy picks the same subgraph type again with different slot fills. "Late-binding context" = artifacts created by early turns are available in later turns.

   **Unresolved:** if real runs reveal a pattern where these Buddy-turn workarounds are painful or slow, the system may need mid-flight features (true cancellation, intra-subgraph retries). Explicitly deferred to v2.

### Best alternative considered

The Plan subagent proposed an alternative: **"Plans as data, executor stays dumb."**

Keep the current node as the only execution unit. Add one new variable: `plan` — a small, declarative, *flat* list of step records the node authors on its first turn (or inherits from a parent). Each step is `{label, instructions, variable_overrides, inputs_from}`. The engine just executes the plan steps and feeds results back.

**Tradeoffs:**
- Wins: one control plane, no DSL beyond what already exists (variable overrides + child instructions), still gives Bonsai a learnable artifact (the plan shape + which plans worked). The "library" emerges as clusters of observed plans that the Scientist can name retroactively, not as a hand-seeded taxonomy.
- Costs: less upfront structure for the Scientist to lean on; harder to enforce "this is a review-then-execute pattern" by construction. The alternative defers the catalog decision until you have data to ground it, which is cleaner but also punts on the expressive power that named types give Buddy.

**Why we're not taking the alternative:** the "plans as data" approach is a strictly lighter-weight version of buddy-eywa but loses the named-type library that gives Buddy clean composable choices. The named library is what makes Buddy's prompt tractable ("here are 12 choices, pick one") vs. "author a plan from scratch every turn." Buddy-eywa's explicit library is a better fit for the long-term vision of a system that learns patterns and applies them.

However, the alternative is worth keeping in mind as a fallback: if the buddy-eywa direction proves too heavy during implementation, retreating to "flat plans with no typed library" is a smaller but still worthwhile step forward.

### Bottom-line recommendation from the Plan subagent

*"Ship it with significant modifications":*
1. Eliminate intra-node multi-turn inside slots — **adopted**
2. Seed only 2 subgraph types — **adopted**
3. Skip backfill — **adopted**
4. Defer Scientist work — **adopted**

Plus additional suggestions incorporated:
- Content-address type specs — **adopted**
- Drop `inputs_from` for v1 if not needed by the seeded types — **conditionally adopted**; keeping the field in the contract but allowing types to omit it, letting the first two seeded types avoid its complexity until needed

## Open questions

### Design questions still to resolve

1. **Should `inputs_from` be in the spec from day one, or added later?**

   The seeded `delegate_fanout_synthesize` needs it (synthesizer references workers). Decision: keep it in the contract but keep it simple (list of label strings only). Add richer semantics (conditional edges, weighted inputs, etc.) only if real needs emerge.

2. **How does Buddy receive the library's type catalog in its prompt?**

   Options: full type specs inlined (bloats the prompt as the library grows), name + description only (loses structural detail), name + description + slot labels (middle ground). Decision tentative: name + description + slot labels for v1, revisit once the library has >10 types.

3. **What happens when Buddy picks a type but fills its slots with instructions that don't match the slot roles?**

   Validation at Buddy's response parse time: are all slot labels present in the fills? Yes/no, easy. Semantic matching ("does the instruction for `reviewer` actually describe a review?") is out of scope for v1 validation; if Buddy authors nonsense slot instructions, the worker will produce nonsense output and Buddy will see that on the next turn and recover.

4. **Do we need a "generic fallback" type for when Buddy is uncertain?**

   `just_execute` is already the fallback — it's the minimum-commitment choice. If Buddy doesn't know what to do, picking `just_execute` with the original task as the instructions is a safe default. No separate fallback type needed.

5. **How does Buddy know when it's done?**

   Buddy's prompt includes explicit guidance: "if the accumulated state contains a terminal output that sufficiently answers the original task, author `turn_decision: done` with that output as `final_answer`." The judgment is up to Buddy's prompt quality. Scientist can later study how well Buddy makes this call.

6. **What if Buddy picks a type that doesn't exist in the library?**

   Validation catches it at parse time. The engine reports a parse error; Buddy's next-turn prompt includes the error and asks for a valid pick. Budget one retry per turn before giving up on the turn.

7. **When Buddy is nested (slot with `buddy: always`), what task does the nested Buddy see?**

   The slot's filled instructions become the nested Buddy's "original task." The nested Buddy works on that sub-task with its own accumulated state, budget, and artifact visibility (all artifacts in the run are still visible). When nested Buddy declares done, its final answer becomes the slot's output.

8. **Do nested hosts share artifact visibility with their parent?**

   Yes, in v1. All artifacts in a run are globally visible within that run. This is the simple choice. Per-host artifact scoping is a v2 feature if it becomes necessary.

9. **Should subgraph specs support "optional" slots?**

   Not in v1. All slots defined in a type must be filled when Buddy picks that type. If you want optional behavior, make two type variants. Keeping the schema simple matters.

10. **How do variable overrides interact with per-slot variable defaults?**

    Three-layer merge: (run-level defaults) ← (type's per-slot defaults) ← (Buddy's per-slot overrides). Latest wins. Well-defined, testable.

### Implementation questions

1. **Should `expand_node` and `expand_subgraph` live in `engine.py` or in separate files?**

   Probably separate files once they grow past a few hundred lines each. Start in `engine.py` during the refactor, extract when size demands.

2. **Where do the recorded learning surfaces live exactly?**

   Per-run copies under `run_dir/derived/` and aggregated copies under `data-system/laboratory/<surface>/`. Supabase sync extension handles the database view if needed.

3. **Should the Buddy role be a normal "node" in the run directory or have its own directory?**

   Normal node. Buddy just has `prompt_family: pick_subgraph`. All the same recording machinery applies. This keeps the bones uniform: Buddy is a node like any other.

4. **How is the subgraph instance ID generated?**

   Content hash + timestamp + counter. Example: `sg_inst_<short_hash>_<runid>_0001`. Deterministic enough for replay, unique enough for debugging.

### Research questions (for later)

1. **When does the library get too big?** After how many types does Buddy's choice-making get harder? Need to measure.

2. **What's the right depth limit?** How deep does nesting actually go in practice, and where does added depth stop helping?

3. **Can Buddy learn from its own past decisions within a run?** Buddy sees prior turns in accumulated state — is that enough context to avoid repeating mistakes within a single run? Need to measure.

4. **How stable are subgraph types once crystallized?** Does the library converge or keep churning? The Scientist's behavior over time should eventually stabilize to "notice edge cases" rather than "invent new structures constantly."

These research questions only matter once there's enough live run data to study, which is why the Scientist is deferred until after data collection is mature.

## Unresolved concerns worth tracking

- **Buddy prompt bloat** — as the library grows, Buddy's prompt has to represent more choices. This could make decisions slower, costlier, or lower-quality. Mitigation ideas: retrieve-relevant-types step before Buddy picks (a small filter based on task features), but that adds complexity. Track and revisit.

- **Attribution in learning surfaces** — when a run scores well, which Buddy turn was responsible? Traditional credit assignment is hard. For v1 the plan is to record context rich enough that the Scientist can eyeball attribution; automated attribution is a later problem.

- **Type library governance** — who decides when a proposed new type is "good enough" to stay? For v1, Sean decides. For v2+, this may need explicit criteria (minimum number of bench runs, minimum win margin, etc.) to prevent library rot.

- **Cost of multi-turn Buddy vs. single-decision today** — every Buddy turn is a prompt call. Multi-turn Buddy loops can cost 3-5x more tokens than today's single-pass orchestration. Whether the improved decision quality pays for the cost is an empirical question. Track token costs from chunk 12 onward and compare modes.
