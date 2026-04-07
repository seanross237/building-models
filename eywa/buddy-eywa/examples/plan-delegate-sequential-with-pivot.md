# Example — Plan, Delegate Sequentially, Pivot on Failure

## The scenario

The user's task is substantial and benefits from an initial plan, then sequential execution of the plan's steps, with the option to re-evaluate and pivot after each step.

Example task: *"Build a small CLI tool that fetches RSS feeds, filters by keyword, and prints results as markdown."*

## How this runs with the 2-type seed library

No special subgraph type is needed. Sequential-with-checkpoints falls out naturally from Buddy's turn loop.

### Buddy turn 1 — plan

**Buddy's pick:** `just_execute`

**Slot fills:**
- `worker`: "Produce a step-by-step plan for building the requested CLI tool. Keep steps coarse-grained (3-5 steps). Output the plan as an artifact titled 'Plan v1'."

**Result:** worker produces `art_0001` containing something like:

```
1. Parse the RSS feed URL from command line arguments.
2. Fetch the RSS feed content over HTTP.
3. Parse the feed and extract entries.
4. Filter entries by the user-supplied keyword.
5. Format filtered entries as markdown and print to stdout.
```

### Buddy turn 2 — execute step 1

**Buddy's pick:** `just_execute`

**Slot fills:**
- `worker`: "Implement step 1 of the plan in art_0001: parse the RSS feed URL and keyword from command line arguments. Use argparse. Output a Python module file as an artifact titled 'cli_entry_v1'."
- `worker.artifact_refs`: `["art_0001"]`

**Result:** worker produces `art_0002` with a working argparse skeleton.

### Buddy turn 3 — execute step 2

**Buddy's pick:** `just_execute`

**Slot fills:**
- `worker`: "Implement step 2 of the plan: fetch the RSS feed content over HTTP. Extend the code from art_0002. Handle basic errors like connection failures and non-200 responses. Output an updated artifact titled 'cli_entry_v2'."
- `worker.artifact_refs`: `["art_0001", "art_0002"]`

**Result:** worker produces `art_0003` with HTTP fetching added.

### Buddy turn 4 — execute step 3 (which fails)

**Buddy's pick:** `just_execute`

**Slot fills:**
- `worker`: "Implement step 3 of the plan: parse the feed and extract entries. Extend the code from art_0003. Output as 'cli_entry_v3'."
- `worker.artifact_refs`: `["art_0001", "art_0003"]`

**Worker's response:**

```json
{
  "output": "The plan assumed RSS format, but the test URL returned an Atom feed. RSS-specific parsing won't cover both formats. The plan as written is too narrow.",
  "output_summary": "Plan assumed RSS only; real feeds include Atom. Plan needs revision.",
  "fail_fast": {
    "triggered": true,
    "reason": "The plan specified RSS parsing but real-world feeds often use Atom. The implementation approach needs to be revised before proceeding."
  }
}
```

The subgraph terminates early with this worker's output. Buddy sees the fail-fast reason in the accumulated state on his next turn.

### Buddy turn 5 — pivot, revise the plan

Buddy's context now shows:
- The original task
- Prior turns 1-3 succeeded (plan + step 1 + step 2)
- Turn 4 fail-fasted: plan is too narrow, RSS-only parsing won't work
- Artifact inventory: art_0001 (plan), art_0002, art_0003 (code drafts)

**Buddy's pick:** `just_execute`

**Slot fills:**
- `worker`: "Revise the plan in art_0001. The previous plan assumed RSS-only feed parsing; real feeds include Atom. Update the plan to handle both formats (e.g., use the `feedparser` library). Output the revised plan as an artifact titled 'Plan v2' that supersedes art_0001."
- `worker.artifact_refs`: `["art_0001"]`

**Result:** worker produces `art_0004` with `supersedes: "art_0001"`, containing a revised plan that uses `feedparser`.

### Buddy turn 6 — execute the revised step 3

**Buddy's pick:** `just_execute`

**Slot fills:**
- `worker`: "Implement the revised step 3: use feedparser to parse the feed and extract entries, handling both RSS and Atom. Extend the code from art_0003. Output as 'cli_entry_v4'."
- `worker.artifact_refs`: `["art_0004", "art_0003"]`

(Notice the artifact_refs now point to the revised plan art_0004, not the original art_0001. Buddy is updating context as he goes.)

**Result:** worker produces `art_0005` with feedparser-based parsing.

### Buddy turns 7, 8 — finish steps 4 and 5

Similar to turns 2-3. Buddy picks `just_execute` for each remaining step, updates artifact_refs to the latest code version, and workers produce successive versions.

### Buddy turn 9 — done

Buddy sees the final working code artifact. Declares `turn_decision: done`, final_answer references the latest code artifact.

## What would have happened without fail-fast

Without the fail-fast escape hatch, worker in turn 4 would have tried to implement step 3 as specified (RSS-only), produced broken code, and Buddy would have seen the output on turn 5 and had to infer the problem from the broken output. Fail-fast lets the worker hand Buddy a clean, explicit "this won't work and here's why" signal, which speeds up the pivot.

## What would have happened if this were a crystallized type

If the Scientist had previously crystallized a type like `plan_then_sequential_execute_with_checkpoints`:

```json
{
  "name": "plan_then_sequential_execute_with_checkpoints",
  "slots": {
    "planner":    {"role": "write a step-by-step plan", "buddy": "never"},
    "step_1":     {"role": "execute step 1", "buddy": "never", "inputs_from": ["planner"]},
    "step_2":     {"role": "execute step 2", "buddy": "never", "inputs_from": ["planner", "step_1"]},
    "step_3":     {"role": "execute step 3", "buddy": "never", "inputs_from": ["planner", "step_2"]},
    "step_4":     {"role": "execute step 4", "buddy": "never", "inputs_from": ["planner", "step_3"]},
    "step_5":     {"role": "execute step 5", "buddy": "never", "inputs_from": ["planner", "step_4"]}
  },
  "terminal": "step_5"
}
```

This would run as one subgraph instance. If `step_3` fail-fasts, the whole subgraph terminates early. Buddy sees the failure on his next turn and picks a pivot — exactly as in the composed version, just with fewer turns before the pivot point.

The composed version gives Buddy a checkpoint after every step; the crystallized version gives Buddy one checkpoint at the end (or on fail-fast). Composed is more flexible, crystallized is more efficient. The Scientist's job is to figure out which one scores better for each task category and teach Buddy accordingly.
