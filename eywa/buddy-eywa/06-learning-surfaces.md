# 06 — Learning Surfaces

## The premise

Buddy-Eywa's clean separation of strategic (Buddy) and tactical (Worker) decisions gives the Scientist **independent learning surfaces** that can be optimized without interfering with each other. Adding the artifact store gives a third surface. Together they cover the three fundamental questions the system needs to answer to improve over time:

1. **Strategic** — What sequence of subgraph types works best for a given task context?
2. **Tactical** — What prompt profiles, models, and variables produce the best worker outputs for a given kind of assignment?
3. **Informational** — What kinds of artifacts, produced by which slots, are most valuable to which downstream slots?

Each is a different question with a different data shape, sample size, and signal-to-noise ratio.

## Surface 1 — Buddy-turn table

**One row per Buddy decision.**

```
buddy_turn_id
run_id
host_node_id
host_depth
turn_number
task_features                ← derived: task type tags, length, keywords, etc.
prior_turns_summary          ← compact view of what's happened so far at this host
artifact_inventory_summary   ← compact view of what artifacts existed at decision time
chosen_type                  ← library type id, or "done"
chosen_type_content_hash     ← precise spec hash
slot_fills_summary           ← per-slot instruction summaries
subgraph_instance_id         ← which instance resulted
terminal_output_summary      ← compact view of what the subgraph produced
fail_fast_triggered          ← did any slot fail-fast in the resulting subgraph?
downstream_host_final_score  ← eventual grading score for the run this turn was part of
```

### Questions this surface answers

- For tasks that look like X, which subgraph types score highest?
- When Buddy pivots after a fail-fast, which pivot choices recover best?
- Does picking `delegate_fanout_synthesize` after a `just_execute` plan score better than going straight to `delegate`?
- At what depth does Buddy stop adding value (i.e., nested Buddies just add overhead without improving scores)?

### Sample characteristics

- Volume: moderate — maybe 2 to 10 Buddy turns per host, plus nesting. Hundreds to low thousands per bench run of the full grading suite.
- Signal-to-noise: relatively high — each Buddy turn is a distinct strategic choice with a clear outcome. But the downstream score attribution problem is real (it's hard to know if turn 1 or turn 3 was the decisive choice).
- Time scale: decisions spread across seconds to minutes of wall-clock time.

## Surface 2 — Slot-execution table

**One row per worker execution.**

```
slot_execution_id
run_id
subgraph_instance_id
subgraph_type_id
subgraph_type_content_hash
slot_label                      ← e.g., "worker_1", "synthesizer", "researcher_a"
slot_role                       ← from the type, e.g., "research area A"
host_depth                      ← depth of the outer host
assignment_text                 ← Buddy's instructions for this slot
upstream_input_summaries        ← summaries of inputs from upstream slots
upstream_artifact_refs          ← which artifacts were loaded for this worker
resolved_variables              ← model, prompt profile, temperature, budget
output_summary                  ← worker's authored output summary
output_size_tokens
output_quality_score            ← if gradable directly
fail_fast_triggered
downstream_subgraph_score       ← terminal output quality of the containing subgraph
downstream_run_score            ← eventual grading score for the run
```

### Questions this surface answers

- For `researcher`-role slots, which prompt profile produces the highest-quality findings?
- Does using a cheaper model for `worker`-role slots in `delegate_fanout_synthesize` cost much in downstream quality?
- Which slot roles are most sensitive to model choice? Which are insensitive?
- What's the typical output size for a `synthesizer` slot, and do larger outputs correlate with higher scores?

### Sample characteristics

- Volume: high — every worker in every subgraph in every run contributes one row. Thousands to tens of thousands per bench run.
- Signal-to-noise: good for tactical tuning because individual slot executions are almost identical apart from the variables being tested. Great for controlled A/B experiments.
- Time scale: individual slot executions are seconds to tens of seconds.

## Surface 3 — Artifact-usage table

**One row per artifact reference event** — i.e., each time an artifact is loaded into a worker's prompt as a referenced artifact.

```
artifact_usage_id
run_id
artifact_id
artifact_type                    ← text_markdown, code_python, etc.
artifact_size_bytes
created_by_slot_role             ← which kind of slot produced it
created_by_subgraph_type
created_at_turn_number
used_by_slot_role                ← which kind of slot consumed it
used_by_subgraph_type
used_at_turn_number              ← could be same-turn (edges) or cross-turn
hops_between_creation_and_use    ← 0 = same subgraph, 1 = next Buddy turn, etc.
superseded                       ← did this artifact get replaced?
superseded_after_n_hops
downstream_run_score
```

### Questions this surface answers

- Do artifacts created by `planner` slots produce higher-scoring runs when consumed immediately vs. after a few more turns?
- Do superseded plans correlate with better final scores (meaning revision matters) or worse (meaning the initial plan was wasted work)?
- Which artifact types are consumed most frequently? Which are created but never read?
- Is there a reliable pattern where "compiled research → plan → implementation" beats "plan → research → implementation" for a given task class?

### Sample characteristics

- Volume: moderate to high — depends on how heavily workers use artifacts, but should be comparable to slot executions.
- Signal-to-noise: lower than slot executions because the causal story ("this artifact helped this downstream slot") is harder to disentangle. Better used for hypothesis generation than for tight optimization.
- Time scale: spans multiple Buddy turns within a run.

## Why three surfaces and not one

A naive design would collapse all of this into "run-level outcomes" and try to learn everything from final grading scores. That approach suffers from:

- **Blame attribution** — which decision actually mattered? Hard to tell from a final score alone.
- **Signal dilution** — strategic choices cascade into tactical outcomes, so tactical signals get swamped by strategic ones.
- **Sample starvation** — if you only learn per run, your sample size is runs. If you learn per slot execution, your sample size is orders of magnitude larger.

Separating the surfaces lets each one use its own signal on its own terms:

- Buddy-level improvements benefit from fewer, higher-quality decisions and strategic clustering
- Worker-level improvements benefit from high-volume controlled experimentation
- Artifact-level insights benefit from pattern recognition across information flows

## Trajectory over time

### Month 1–2: Pure data collection

No learning yet. Every Buddy turn, every slot execution, every artifact usage lands on disk with full context. Grading bench scores runs end-to-end. Build the laboratory's row-level stores:

```
data-system/laboratory/
  buddy-turns/        ← one file per turn
  slot-executions/    ← one file per slot run
  artifact-usages/    ← one file per artifact load event
```

Supabase sync (already exists in current super-eywa) becomes the derived denormalized view for querying.

### Month 2–4: Eyeball analysis by the Scientist

Manual clustering. Patterns emerge from reading the data. First hand-rolled rules land as simple lookup tables:

- `buddy-policies/task_feature_hints.json` — "for math word problems, prefer `delegate_fanout_synthesize` over `just_execute`"
- `slot-variable-policies/per_role_defaults.json` — "for `reviewer`-role slots, default to prompt profile B with a lower-cost model"

These are *suggestions* to Buddy and to the engine, not replacements for runtime decision-making.

### Month 4–8: First real experiments

A/B runs on the grading bench. Two type variants go head-to-head on a fixed question set. Prompt profile variants per slot role tested the same way. Winners land; losers move to a graveyard folder with notes. The library starts growing from observed wins, not guesses.

### Month 8–18: First learned components

- **Buddy ranker** — a small model (or nearest-neighbor index) that, given a task context, ranks the top 3 subgraph types. Trained on the buddy-turn table. Used as a prompt hint to Buddy, not as a replacement — Buddy still authors the final decision.
- **Prompt profile selector** — per slot role, a simple model or lookup that picks the best default profile given assignment features.
- **Artifact-flow insights** — Scientist publishes "architecture insights" documents in the lab describing information-flow patterns that work, and new subgraph types are designed to capture them.

### Month 18+: Maturity

The library has 20 to 40 validated subgraph types. Buddy is informed by learned rankers that keep improving as new data lands. Workers have per-slot-role variable defaults tuned on thousands of real executions. Retired variants live in a graveyard with explanatory notes. The Scientist becomes less about inventing new types and more about noticing edge cases where current types underperform.

## The commitment required now

**Record everything faithfully, from day one, even when no one is reading the data yet.**

If the three surfaces are recorded with full context from the first buddy-eywa runs, then when the Scientist arrives in month 3 the data is already deep. If the recording is skimpy or inconsistent, the Scientist has to rerun everything to get usable data, which is painful.

This means:
- Every Buddy prompt and response gets saved, not just summarized
- Every worker prompt and response gets saved, not just summarized
- Every artifact creation and read is logged
- All metadata is stored even if current Scientist doesn't read it yet

Storage is cheap, rerunning experiments is not. Err on the side of recording more.

## What the Scientist will NOT do (at least not early)

To keep the early-stage system honest:

- No automated subgraph type generation from learned signals
- No automated slot-level variable tuning in production
- No runtime decision-making from learned policies (they stay advisory to Buddy's prompts)
- No replacement of Buddy with a pure learned policy — Buddy stays an authored agent, with learned signals as context hints

These can come later once there's enough data to trust automation. Until then, the Scientist is a human-in-the-loop research function that uses the tables to propose changes, which get validated on the bench.
