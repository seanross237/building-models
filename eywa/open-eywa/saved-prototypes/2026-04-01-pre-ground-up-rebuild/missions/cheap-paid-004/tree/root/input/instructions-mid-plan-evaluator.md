# Open-Eywa Instructions: mid-plan-evaluator

Decide whether this node should `continue`, `replan`, or `escalate`.

If prior state is missing, proceed using the plan and child result.

## Current Plan

## Plan
Status: approved
Review: low

### Step 1: Define Open-Eywa
Goal: Write a concise definition of Open-Eywa, suitable for a human operator skimming the mission folder for the first time.
Complexity: 2
Importance: 8
Dependencies: none
Independent: yes
Confidence: high
Verifiable: yes

### Step 2: Explain File-Based Nature
Goal: Explain why Open-Eywa is file-based, focusing on the benefits for human operators and the system. This explanation should be concise and understandable for a first-time user.
Complexity: 3
Importance: 8
Dependencies: step 1
Independent: no
Confidence: high
Verifiable: yes

### Step 3: Identify Top-Level Folders for Inspection
Goal: Identify and list the top-level folders within the mission tree that a human operator should inspect first to understand the mission's status and structure. Provide a brief rationale for each.
Complexity: 4
Importance: 9
Dependencies: none
Independent: yes
Confidence: high
Verifiable: yes

### Step 4: Describe Mission Tree Health Indicators
Goal: Describe how to determine if a run is healthy or stuck by examining the mission tree alone. This should include observable indicators and potential red flags.
Complexity: 4
Importance: 9
Dependencies: none
Independent: yes
Confidence: high
Verifiable: yes

### Step 5: Synthesize Operator Note
Goal: Combine the outputs of Steps 1-4 into a single, concise operator note. The note should be readable by a human skimming the mission folder for the first time and fit comfortably on one page.
Complexity: 3
Importance: 10
Dependencies: step 1, step 2, step 3, step 4
Independent: no
Confidence: high
Verifiable: yes


## Current State

The latest child result failed, but the plan can still proceed. The failure to find `stuff-for-agents/library/factual/INDEX.md` and `stuff-for-agents/library/meta/INDEX.md` should be monitored. The next step is to explain the file-based nature of Open-Eywa.

## Latest Child Status

complete

## Latest Child Result

A run can be considered healthy if the mission tree shows consistent progress and activity. Observable indicators include:

*   **Regular updates to `state.md` files:** Healthy runs will frequently update their `state.md` files to reflect progress. This indicates that the worker is actively processing tasks.
*   **Completion of sub-tasks:** As a worker progresses, sub-tasks within the mission tree should be marked as complete. This can be observed by changes in file content or the creation of new files indicating completion.
*   **Absence of long-running, uncompleted tasks:** If a particular branch of the mission tree remains stagnant for an extended period without any updates or progress, it could indicate a stuck process.
*   **Consistent file modification times:** Healthy activity within a mission directory will be reflected in recent modification times for files. Stale modification times can be a red flag.

Potential red flags that might indicate a stuck run include:

*   **Stagnant `state.md` files:** If a `state.md` file hasn't been updated for a significant duration, the worker associated with that branch may be stuck.
*   **Unfinished tasks without apparent reason:** If tasks are consistently failing or not progressing, and there are no clear error messages or reasons for the failure, it could indicate a deeper issue.
*   **Circular dependencies or deadlocks:** While harder to detect solely from file content, a pattern of tasks repeatedly attempting and failing to complete due to unmet dependencies could signal a deadlock.
*   **Lack of expected output files:** If a worker is supposed to generate certain output files upon completion of a task, and these files are consistently missing, it suggests the task is not completing successfully.

To effectively monitor the health of a run, one would typically look for a pattern of consistent, forward progress across the mission tree, with regular updates and task completions. Conversely, stagnation, repeated failures, or a lack of expected progress are indicators of a potentially stuck run.

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

