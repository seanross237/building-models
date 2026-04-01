# Open-Eywa Instructions: mid-plan-evaluator

Decide whether this node should `continue`, `replan`, or `escalate`.

If prior state is missing, proceed using the plan and child result.

## Current Plan

## Plan
Status: approved
Review: low

### Step 1: Define Open-Eywa
Goal: Write a concise definition of Open-Eywa for a human operator.
Complexity: 2
Importance: 8
Dependencies: none
Independent: yes
Confidence: high
Verifiable: yes

### Step 2: Explain File-Based Nature
Goal: Explain why Open-Eywa is file-based, focusing on benefits for human operators.
Complexity: 3
Importance: 8
Dependencies: none
Independent: yes
Confidence: high
Verifiable: yes

### Step 3: Identify Key Folders
Goal: Identify the top-level folders a human operator should inspect first in a mission tree.
Complexity: 4
Importance: 9
Dependencies: none
Independent: yes
Confidence: high
Verifiable: yes

### Step 4: Determine Run Health
Goal: Explain how to determine if a run is healthy or stuck by inspecting the mission tree alone.
Complexity: 4
Importance: 9
Dependencies: none
Independent: yes
Confidence: high
Verifiable: yes

### Step 5: Synthesize Operator Note
Goal: Combine the answers from the previous steps into a concise, single-page operator note.
Complexity: 3
Importance: 10
Dependencies: step 1, step 2, step 3, step 4
Independent: no
Confidence: high
Verifiable: yes


## Current State

The task is progressing as planned. Step 1 and Step 2 have been completed. The latest child result provided a list of top-level folders to inspect. The next step is to determine run health.

## Latest Child Status

complete

## Latest Child Result


To determine if a run is healthy or stuck by inspecting the mission tree alone, you should examine the contents and activity within the primary directories: `for-orchestrator/`, `input/`, `output/`, and `system/`.

### `for-orchestrator/`

*   **Healthy Run:** Look for files that indicate successful handoffs, progress updates, or expected communication with an orchestrator. The presence of new or updated files here suggests the process is interacting correctly with its environment.
*   **Stuck Run:** An empty `for-orchestrator/` directory, or one containing stale information, might indicate that the process is not communicating as expected or has stalled in its interaction with other components.

### `input/`

*   **Healthy Run:** Observe if files in the `input/` directory are being processed. This could mean they are being moved, deleted, or that new files are being generated based on them. Active consumption of input is a sign of a healthy, progressing run.
*   **Stuck Run:** If files in `input/` remain untouched over an extended period, or if the directory is unexpectedly empty when input is expected, it suggests the process is not able to proceed.

### `output/`

*   **Healthy Run:** A healthy run will show regular updates or new files appearing in the `output/` directory. The content of these files might also reveal progress or successful completion of tasks.
*   **Stuck Run:** A lack of new content in `output/`, or the consistent appearance of incomplete results or error messages, points to a stuck or failed run.

### `system/`

*   **Healthy Run:** Check logs or state files within the `system/` directory. Activity like new log entries, progress messages, or successful completion markers indicates the system is operating normally.
*   **Stuck Run:** Error logs, repeated error messages, or a complete absence of recent activity in `system/` files can be strong indicators of a problem or a stalled process.

### General Indicators of a Stuck Run:

*   **Lack of Activity:** No new files, no modifications to existing files, and no log updates across these directories over a significant timeframe.
*   **Stale Timestamps:** Files in critical directories have not been modified for a prolonged period.
*   **Error Indicators:** The presence of specific error files, error messages in logs, or files explicitly marking a failed state.
*   **Incomplete Processing:** Input files remain unprocessed, or output files are consistently incomplete or malformed.

By monitoring these directories and the nature of their contents, one can infer the health and progress of a run.


Write `for-orchestrator/eval-decision` with one of: `continue`, `replan`, or `escalate`.
Also update `output/state.md`.

# Continue / Replan / Escalate Guidance

## Continue

Choose continue when the plan is still on track and the next step still makes sense given what you have learned.

Action:

- write `continue` to `for-orchestrator/eval-decision`
- if needed, write `output/context-for-next-step.md`
- update `output/state.md`

## Replan

Choose replan when the goal is still achievable but the remaining steps should change.

Action:

- write an updated `output/plan.md` with `Status: draft`
- write `replan` to `for-orchestrator/eval-decision`
- update `output/state.md`

Preserve completed valid work when you replan.

## Escalate

Choose escalate when you can no longer produce what your parent expects.

Action:

- write `output/escalation.md`
- write `escalate` to `for-orchestrator/eval-decision`
- update `output/state.md`

## The Core Question

Can this node still produce what its parent expects, given what is now known?

