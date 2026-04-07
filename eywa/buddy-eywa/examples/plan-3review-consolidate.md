# Example — Plan, 3-way Review, Consolidate (the motivating example)

## The scenario

This is the example that originally motivated Buddy-Eywa in the 2026-04-07 design conversation. Sean described it as: an agent makes a plan, then has it reviewed by 3 agents separately, and they pass their output to another agent that consolidates it all, and the consolidator passes back its thoughts to the original.

This example shows both the "composed from seed" version and the "crystallized as a type" version.

## Version 1 — Composed from the 2-type seed library

### Buddy turn 1 — plan

**Buddy's pick:** `just_execute`

**Slot fills:**
- `worker`: "Produce a detailed plan for the following task: [original task]. Output the plan as an artifact titled 'Plan v1'."

**Result:** `art_0001` = the plan.

### Buddy turn 2 — 3-way review

**Buddy's pick:** `delegate_fanout_synthesize`

**Slot fills:**
- `worker_1`: "Review the plan in art_0001 from a correctness angle. Look for logical errors, missing steps, incorrect assumptions. Be specific. Don't restate the plan — just your critique." with `artifact_refs: ["art_0001"]`
- `worker_2`: "Review the plan in art_0001 from a completeness angle. What's missing? What edge cases aren't handled?" with `artifact_refs: ["art_0001"]`
- `worker_3`: "Review the plan in art_0001 from a feasibility angle. What's hard to actually implement? What dependencies or resources are assumed but not specified?" with `artifact_refs: ["art_0001"]`
- `synthesizer`: "Combine the three reviews into a single consolidated review document. Deduplicate overlapping points. Prioritize the most important concerns. Output as an artifact titled 'Consolidated Review of Plan v1'." with `artifact_refs: ["art_0001"]`

**Result:** the subgraph runs. Workers 1-3 each produce a critique. The synthesizer produces `art_0002` = consolidated review.

### Buddy turn 3 — revise the plan

Buddy's context shows original task, plan (art_0001), consolidated review (art_0002).

**Buddy's pick:** `just_execute`

**Slot fills:**
- `worker`: "Revise the plan in art_0001 to address the concerns in art_0002. Keep structure similar. Output the revised plan as an artifact titled 'Plan v2' that supersedes art_0001." with `artifact_refs: ["art_0001", "art_0002"]`

**Result:** `art_0003` = revised plan, supersedes art_0001.

### Buddy turn 4 — done

Buddy sees the revised plan. Decides it addresses the review concerns well enough. `turn_decision: done`, final_answer references art_0003.

## Version 2 — Crystallized as a single subgraph type

Say Scientist notices this 4-turn sequence recurring on many planning tasks. Crystallizes it:

### `plan_3review_consolidate.json`

```json
{
  "name": "plan_3review_consolidate",
  "version": "v1",
  "description": "Produce a plan, review it from 3 angles, consolidate the reviews, and produce a revised plan. Good for high-stakes planning tasks where correctness matters more than speed.",
  "slots": {
    "planner": {
      "role": "produce the initial plan",
      "buddy": "never"
    },
    "reviewer_correctness": {
      "role": "review the plan for logical correctness",
      "buddy": "never",
      "inputs_from": ["planner"]
    },
    "reviewer_completeness": {
      "role": "review the plan for completeness and edge cases",
      "buddy": "never",
      "inputs_from": ["planner"]
    },
    "reviewer_feasibility": {
      "role": "review the plan for practical feasibility",
      "buddy": "never",
      "inputs_from": ["planner"]
    },
    "consolidator": {
      "role": "consolidate the three reviews and produce a revised plan",
      "buddy": "never",
      "inputs_from": ["planner", "reviewer_correctness", "reviewer_completeness", "reviewer_feasibility"]
    }
  },
  "terminal": "consolidator"
}
```

### How the same task runs with the crystallized type

**Buddy turn 1:**

Buddy picks `plan_3review_consolidate` and fills all 5 slots. One subgraph instance runs:

```
                [ planner ]
                     ↓
     ┌───────────────┼───────────────┐
     ↓               ↓               ↓
[reviewer_    [reviewer_     [reviewer_
 correctness]  completeness]  feasibility]
     ↓               ↓               ↓
     └───────────────┼───────────────┘
                     ↓
              [ consolidator ]
                     ↓
                  terminal
```

1. Planner runs (no upstream).
2. All three reviewers run, each with the planner's output as input.
3. Consolidator runs, with inputs from all three reviewers AND the original plan.
4. Consolidator produces the revised plan.
5. Terminal output = consolidator's output.

**Buddy turn 2:**

Buddy sees the terminal output. Decides done. Host terminates in 2 turns.

## Tradeoff between composed and crystallized

**Composed (version 1):**
- 4 Buddy turns, more prompt calls
- Buddy gets to inspect the plan before committing to review it (could pivot if the initial plan is obviously bad)
- Buddy gets to inspect the reviews before committing to revision (could choose not to revise if reviews are all positive)

**Crystallized (version 2):**
- 2 Buddy turns (one to pick, one to declare done)
- Subgraph runs atomically — all 5 workers run, no mid-flight interruption
- Lower overhead if the pattern is the right one for this task

## The "buddy on the consolidator" variant

Scientist might create a variant where the consolidator has `buddy: always`:

```json
"consolidator": {
  "role": "consolidate the three reviews and produce a revised plan",
  "buddy": "always",
  "inputs_from": ["planner", "reviewer_correctness", "reviewer_completeness", "reviewer_feasibility"]
}
```

With this variant:
1. Planner and reviewers run as before.
2. When it's time for consolidator, the engine spawns a nested Buddy for the consolidator slot.
3. Consolidator's nested Buddy runs its own loop. Maybe turn 1 is `just_execute` to draft a consolidated review, turn 2 is `just_execute` to produce a revised plan based on the review, turn 3 is done.
4. Nested Buddy's final answer becomes the consolidator slot's output.
5. Consolidator's output flows to terminal, subgraph terminates.

This gives the consolidator "adaptive" behavior without breaking the single-control-plane rule. It's just the same Buddy primitive applied one level deeper.

## What Sean originally asked about

In the 2026-04-07 conversation, Sean asked: "the consolidator passes back its thoughts to the original." This was the "loopback" question.

Resolution: in Buddy-Eywa, "passing back to the original" is expressed by:
1. The consolidator is the terminal slot of the subgraph.
2. Its output becomes the subgraph's terminal output.
3. That terminal output flows into Buddy's accumulated state as "the result of this turn."
4. Buddy's next turn sees the consolidator's output and decides what to do with it — including potentially picking another `just_execute` to do one more pass at the original planner's role, if needed.

The "loop" isn't inside the subgraph (DAGs are acyclic). The "loop" is at the Buddy turn level, which is where all iteration lives.
