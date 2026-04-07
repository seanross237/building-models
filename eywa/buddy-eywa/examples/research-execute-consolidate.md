# Example — Research, Execute, Consolidate

## The scenario

The user's task requires gathering information from three different areas, then executing something based on that research, then consolidating everything into a final answer.

Example task: *"Research the current state of X, Y, and Z in topic T, then write a 500-word primer for a technical audience."*

## Version 1 — Composed from the 2-type seed library

With only `just_execute` and `delegate_fanout_synthesize` in the library, Buddy composes the pattern across turns.

### Buddy turn 1

**Buddy's pick:** `delegate_fanout_synthesize`

**Slot fills:**
- `worker_1`: "Research the current state of X in topic T. Return a compact bullet-point summary with key facts, sources if possible, and notable recent developments."
- `worker_2`: "Research the current state of Y in topic T. Same format as worker_1."
- `worker_3`: "Research the current state of Z in topic T. Same format as worker_1."
- `synthesizer`: "Combine the three research outputs into a single compiled findings document. Preserve distinct claims with attribution to the source worker. Output the result as an artifact of type `text_markdown` titled 'Compiled Findings'."

### What happens during turn 1

1. Engine materializes the subgraph instance with 4 worker nodes.
2. Workers 1, 2, 3 each run (no upstream inputs), producing research outputs.
3. Synthesizer runs with `inputs_from: [worker_1, worker_2, worker_3]`, receives their outputs, produces a compiled findings document.
4. Synthesizer's authored response includes `artifacts_created: [{title: "Compiled Findings", ...}]` — the artifact is written to disk as `art_0001`.
5. The subgraph terminates. Terminal output = synthesizer's output.

### Buddy turn 2

Buddy's context now includes:
- The terminal output of turn 1 (the compiled findings)
- The artifact inventory with `art_0001` and its summary

**Buddy's pick:** `just_execute`

**Slot fills:**
- `worker`: "Write a 500-word primer for a technical audience on topic T, drawing on the compiled findings. Keep the tone accessible but precise. Output the primer as an artifact of type `text_markdown` titled 'T Primer Draft v1'."
- `worker.artifact_refs`: `["art_0001"]`

### What happens during turn 2

1. Engine materializes a 1-slot subgraph instance.
2. Worker runs with the compiled findings loaded into its prompt as a referenced artifact (full content).
3. Worker produces the primer draft and saves it as `art_0002`.
4. Subgraph terminates. Terminal output = worker's output.

### Buddy turn 3

Buddy sees: original task, turn 1's compiled findings, turn 2's primer draft, artifact inventory with `art_0001` and `art_0002`.

**Buddy's decision:** `turn_decision: done`, `final_answer`: references `art_0002` as the final primer.

Host terminates. Run final output = `art_0002`.

## Version 2 — After the Scientist crystallizes the pattern

Say the run history over some months shows this exact 3-turn sequence (research fan-out → execute with research → done) on many similar tasks with consistently high scores. The Scientist crystallizes a new type:

### `research_then_execute_then_consolidate.json`

```json
{
  "name": "research_then_execute_then_consolidate",
  "version": "v1",
  "description": "Fan out research in parallel, then execute a task using the compiled findings, then optionally polish. Good for tasks that need both information gathering and synthesis into a produced output.",
  "slots": {
    "researcher_a":  {
      "role": "research the first area",
      "buddy": "never"
    },
    "researcher_b":  {
      "role": "research the second area",
      "buddy": "never"
    },
    "researcher_c":  {
      "role": "research the third area",
      "buddy": "never"
    },
    "executor": {
      "role": "carry out the primary task using the research findings",
      "buddy": "never",
      "inputs_from": ["researcher_a", "researcher_b", "researcher_c"]
    },
    "consolidator": {
      "role": "produce the final polished answer, drawing on both the research and the executor's output",
      "buddy": "never",
      "inputs_from": ["researcher_a", "researcher_b", "researcher_c", "executor"]
    }
  },
  "terminal": "consolidator"
}
```

### How the same task runs with the crystallized type

**Buddy turn 1:**

Buddy picks `research_then_execute_then_consolidate` with slot fills for all 5 slots. One subgraph instance runs:

1. researcher_a, researcher_b, researcher_c run in parallel (no upstream)
2. executor runs once all three researchers have finished (inputs_from all three)
3. consolidator runs once executor has finished (inputs_from all three researchers AND executor)
4. Terminal output = consolidator's output

**Buddy turn 2:**

Buddy sees the terminal output. If it's strong enough, `turn_decision: done`. Host terminates in 2 turns instead of 3.

## Tradeoff between version 1 and version 2

**Version 1 (composed):**
- More Buddy checkpoints = more adaptability. If Buddy sees that research came back too thin, turn 2 can pick a different approach or another research round.
- Higher Buddy overhead — 3 Buddy prompt calls instead of 1.

**Version 2 (crystallized):**
- Single strategic commitment. Buddy trusts the pattern end-to-end.
- Lower overhead, faster.
- Less flexibility to pivot mid-execution. Pivots still possible at subgraph boundaries (fail-fast + next turn).

## What the Scientist studies to decide between them

The buddy-turn table shows both versions across many runs:
- Does version 2's lower-overhead cost translate into higher net scores?
- Does version 1's adaptability recover more from bad situations?
- For which task categories does each version win?

The answer probably isn't "always one or the other" but "version 2 for task categories where the pattern is reliable, version 1 for exploratory tasks where adaptability pays off." The Scientist's job is to make that distinction visible and teach Buddy (via prompt hints or learned policies) which to prefer when.
