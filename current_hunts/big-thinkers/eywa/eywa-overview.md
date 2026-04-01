# Eywa Overview

## Core Concept

A recursive tree of task nodes. When a parent plans, it scores each step with Complexity (1-10) and Importance (1-10). The orchestrator adjusts both scores by depth (subtracts the child's depth from each, min 1), then multiplies — if adjusted C × I > 30, the child becomes a planner; otherwise an executor. This naturally discourages deep planning. The tree grows as deep as the problem requires — there are no fixed tiers.

When a child completes (or fails), results flow back up to the parent, which decides: continue the plan, replan with new information, or escalate to its own parent. When continuing, the parent can write context from completed steps that gets merged into the next child's instructions.

## Node Lifecycle

1. **Receive task** — goal, relevant knowledge from the library
2. **Role assigned mechanically** — parent plan's C × I score determines executor or planner (root always plans)
3. **If executor:** do the work, return results to parent
4. **If planner:** create a plan with scored steps (C and I per step), then begin executing steps (spawning child nodes)
5. **On child completion:** re-evaluate — continue / replan / escalate
6. **Return results** to parent when goal is achieved (or escalate if it can't be)

## Plan Structure

Plans are rich data structures, not flat step lists. Each step carries:

- **Complexity (1-10)** — how hard this step is for a single agent to execute
- **Importance (1-10)** — how critical this step is to the overall goal
- **Dependencies** — which other steps must complete first, which can run in parallel
- **Confidence** — likelihood of success
- **Verifiability** — whether the output can be objectively checked

The orchestrator adjusts scores by depth and routes each child: adjusted C × I > 30 → planner, ≤ 30 → executor.

## Plan Review + Fortification

Plan review scales with the plan's Review tier — more critical plans get more scrutiny:

**Review: low** — Plan goes straight to execution. No review.

**Review: medium** — Plan → single reviewer → decider revises or approves.

**Review: high (future):** Generate 5 candidate plans → each gets a dedicated critic → each critique gets a judge evaluating if the critique is valid → final decider sees all 5 plans + 5 critiques + 5 judgments, picks the best plan or synthesizes from multiple.

The details of how review works and what reviewers check are an **open research area**.

## Upward Flow (Parent Decisions)

When a parent node gets results from a child, it decides:

- **Continue** — plan is on track, proceed to next step(s). Parent can write `output/context-for-next-step.md` to pass relevant findings from completed children to the next step.
- **Replan** — goal is still achievable but the approach needs to change based on what was learned
- **Escalate** — this node can't produce what its parent expects; push the problem up

The parent is re-spawned fresh from its state files + the child's results. It must be able to make good decisions from serialized state alone.

## Agent Model

**Ephemeral agents with file-based state.** Agents are spawned for a single job, do their work, write state to disk, and terminate. When a parent needs to react (child completed, escalation received), it is re-spawned fresh, reading its full state from files.

This means state serialization quality is critical — a re-spawned parent must pick up where it left off without losing the nuance of why it made its plan. Each node writes a **state brain dump** at the end of every action — not just what it decided, but what it considered and rejected, what its hunches are, and what it would do next and why. This captures the "dark knowledge" that structured state files miss.

&& Persistent vs. ephemeral is an open question. Starting ephemeral.

## Orchestration

A **bash orchestrator** handles all spawning, polling, completion detection, and health checking. Reasoning agents never poll or spawn children directly — they read files, think, write files, and die. The orchestrator is the spine. It costs zero tokens — pure bash.

### Design Principles

- **Task-as-file spawning:** Write goal.md, send the agent a short prompt ("Read your goal and execute"). Avoids paste limits, makes tasks inspectable on disk.
- **Completion signal:** Each node writes `result.md` as its final action. Orchestrator watches for this file.
- **Atomic status transitions:** All status writes use flock-based locking. Every transition checks the current status matches the expected value before writing (compare-and-swap) to prevent double-fires from consecutive poll cycles.
- **Idempotent handlers:** Every handler is safe to run twice. Check "does the child directory already exist?" before creating. Check "is there already a tmux session?" before spawning. Etc.
- **Orchestrator logging:** Every status transition, agent spawn, zombie detection, and health check is logged to `mission-NNN/orchestrator.jsonl` with timestamps. Essential for post-run review.

### Node Statuses

```
pending           → goal.md written, no agent spawned yet
retrieving        → knowledge retrieval agent is fetching relevant library content
running           → node agent is active, doing its work
needs_review      → agent wrote a plan flagged for review
reviewing         → reviewer agent is active
needs_decision    → reviewer done, decider needed
deciding          → decider agent is active
approved          → plan approved, ready to spawn first child
executing         → children being worked through
evaluating        → parent re-spawned to evaluate a child result/escalation
waiting_comp      → node waiting on long background computation
complete          → result.md written, done
escalated         → node escalated to parent
cancelled         → orphaned by parent replan
failed            → zombie killed, max retries exceeded
```

### Main Loop (every 10 seconds)

```
scan all node directories in the active mission tree

for each node:
  acquire flock on node's status file
  read status

  case status:

    "pending":
      → spawn knowledge retrieval agent for this node's goal
      → status → "retrieving"

    "retrieving":
      → check: has retrieval agent written retrieved_relevant_knowledge_from_library.md?
        → if yes: read for-orchestrator/agent-mode, spawn executor or planner, status → "running"
      → zombie check on retrieval agent

    "running":
      → check: does final-output.md exist? → status → "complete"
      → check: does plan.md exist? → determine review tier:
          → low: status → "approved"
          → medium: status → "needs_review"
      → check: does escalation.md exist? → status → "escalated"
      → check: does WAITING_FOR_COMPUTATION exist? → status → "waiting_comp"
      → zombie check:
          - check tmux session alive AND thinking indicator present
          - no file activity for > 3 min AND no thinking indicator:
              → attempt 1: nudge ("Continue where you left off.")
              → attempt 2: kill session + respawn
              → attempt 3: status → "failed"

    "needs_review":
      → spawn reviewer agent
      → status → "reviewing"

    "reviewing":
      → check: does review.md exist?
        → if yes: status → "needs_decision"
      → zombie check on reviewer (including tmux thinking indicator check)

    "needs_decision":
      → spawn decider agent
      → status → "deciding"

    "deciding":
      → check: has plan.md been updated to "status: approved"?
        → status → "approved"
      → check: does escalation.md exist?
        → status → "escalated"
      → zombie check on decider

    "approved":
      → read plan.md, find first step with no unmet dependencies
      → extract step's Complexity and Importance scores
      → if child directory already exists: skip (idempotency)
      → create child node directory: children/step-NN-name/
      → write child's parent-instructions-and-relevant-information.md (mechanical extraction from plan's Goal field)
      → write child's agent-mode: (C - depth) × (I - depth) > 30 → "planner", else → "executor"
      → write child's status → "pending"
      → status → "executing"

    "executing":
      → find the currently active child
      → if active child exists and is not terminal: do nothing
      → if current child is "complete":
          → if more steps remain in plan:
              → status → "evaluating"
              → re-spawn parent in evaluation mode
          → if all steps done:
              → status → "evaluating"
              → re-spawn parent in synthesis mode
      → if current child is "escalated" or "failed":
          → status → "evaluating"
          → re-spawn parent to handle escalation/failure

    "evaluating":
      → check: did parent agent write its decision?
          → "continue":
              → create next child (writes parent-instructions-and-relevant-information.md from plan Goal field)
              → if output/context-for-next-step.md exists, append to child's parent-instructions-and-relevant-information.md
              → status → "executing"
          → "replan" + updated plan.md:
              → cancel any unstarted children (status → "cancelled")
              → status → "approved" (restarts child spawning from new plan)
          → "escalate" + escalation.md written:
              → cancel any unstarted children
              → status → "escalated"
          → "synthesize" + result.md written:
              → status → "complete"
      → zombie check on parent agent

    "waiting_comp":
      → check: does computation result file exist?
        → if yes: re-spawn node to continue, status → "running"
      → check: exceeded time budget?
        → if yes: kill computation, status → "failed"

    "complete":
      → do nothing (parent's "executing" handler picks this up)

    "escalated":
      → do nothing (parent's "executing" handler picks this up)

    "cancelled":
      → kill tmux session if still alive, do nothing further

    "failed":
      → do nothing (parent's "executing" handler treats as escalation)

  release flock
```

### Spawning

```
spawn_agent(node_path, mode):
  session_name = sanitized derivation from node path + timestamp suffix

  # kill any existing session with base name (prevents collisions on respawn)
  tmux kill-session -t "$base_session_name" 2>/dev/null

  tmux new-session -d -s "$session_name"

  # mode determines which short prompt to send
  case mode:
    "executor":   "Read input/instructions-executor.md and execute the task."
    "planner":    "Read input/instructions-planner.md and design a plan."
    "retrieval":  "Read input/instructions-retrieval.md and retrieve relevant knowledge."
    "reviewer":   "Read input/instructions-reviewer.md and review the plan."
    "decider":    "Read input/instructions-decider.md and decide on the final plan."
    "evaluation": "Read input/instructions-evaluation.md and evaluate the child result."
    "synthesis":  "Read input/instructions-synthesis.md and synthesize all child results."

  tmux send-keys -t "$session_name" -l "$prompt"
  sleep 0.3
  tmux send-keys -t "$session_name" Enter

  log spawn event to orchestrator.jsonl
```

### Plan Format (Structured for Mechanical Extraction)

Plans must follow a strict format so the orchestrator can extract child goals without reasoning:

```markdown
## Plan
Status: draft | approved
Review: low | medium

### Step 1: {short-name}
Goal: {self-contained goal description — this becomes the child's goal.md verbatim}
Complexity: {1-10}
Importance: {1-10}
Dependencies: {none | step N, step M}
Independent: {yes | no}
Confidence: {high | medium | low}
Verifiable: {yes | partially | no}

### Step 2: {short-name}
Goal: {self-contained goal description}
...
```

The orchestrator extracts the `Goal:` field and writes it directly to the child's `input/parent-instructions-and-relevant-information.md`. If the evaluation agent wrote `output/context-for-next-step.md`, the orchestrator appends it under a `## Context From Prior Steps` section. No interpretation needed.

### Constraints

- **Max tree depth: 5.** A node at depth 5 must execute — it cannot plan. Prevents pathological over-decomposition.
- **V1: low and medium review tiers only.** High-importance (5-plan tournament) deferred until basic loop is proven.
- **V1: sequential execution only.** Independent steps still run one at a time. Dependency metadata is tracked for future parallel expansion.

## Node Types

Two types, assigned mechanically by the orchestrator based on the parent plan's Complexity × Importance scores:

- **Executor:** Receives goal + knowledge. Does the work directly, writes output/final-output.md. Cannot plan or decompose. Lean context (no plan-design guidance).
- **Planner:** Receives goal + knowledge + plan-design guidance. Decomposes the task into scored steps, writes output/plan.md. Children are assigned types based on their own C × I scores.

Root node is always a planner (no parent plan to score it). Nodes at max depth (5) are always executors regardless of score.

## Knowledge System

A persistent library with two sections:

- **Factual knowledge** — domain learnings accumulated across missions
- **Meta knowledge** — lessons about how the system itself works best (planning patterns, when to split, escalation heuristics, etc.)

The library is tree-structured with hierarchical indexes at each level, so retrieval can navigate top-down rather than flat-searching everything.

A **dedicated retrieval agent** fetches relevant knowledge for each node. How it decides what's relevant is an open question. &&

## Four Key Research Areas

These are the most important things to learn and improve over time:

### 1. Complexity × Importance Scoring
How well do parent planners score their steps? The depth-adjusted C × I threshold (> 30) is mechanical, but the inputs are subjective. Score inflation means too many planners (overhead). Deflation means executors get tasks too complex for one agent. Calibrating the scoring guidance and depth decay is the key lever.

### 2. Plan Design + Fortification
What are the best planning patterns for different problem types? How should plans be reviewed and strengthened? Includes the review/decider loop, plan metadata design, and recognizing problem types to match them with appropriate decomposition strategies.

### 3. Escalation Guidance
When should a node replan vs. escalate? Replanning too eagerly wastes completed work. Escalating too late means the parent's parent gets a mess. The core heuristic: "can I still produce what my parent expects from me?"

### 4. Knowledge Accumulation + Retrieval
How to build the library over time, what to store, how to retrieve the right knowledge for each node. The meta knowledge loop (learning about the system's own performance) feeds back into all three areas above.

## Decision Point Catalog

Every decision the system makes is logged with full reasoning. Post-run review assesses correctness. Findings feed into the meta knowledge library, improving guidance for future runs.

### Node-Level Decisions

**1. Complexity × Importance Scoring**
Parent planner scores each step's Complexity and Importance (1-10). Orchestrator adjusts by depth and routes mechanically (adjusted C × I > 30 → planner, ≤ 30 → executor).
- *Log:* Scores assigned, plan context.
- *Review:* Did executors struggle with tasks that should've been planners (scores too low)? Did planners create trivial sub-steps for tasks that should've been executors (scores too high)?

**2. Plan Design**
What steps, what order, what metadata for each.
- *Log:* Full plan + reasoning for structure choices.
- *Review:* Which steps ended up wrong, unnecessary, or missing? Did dependency labels match reality?

**3. Plan Importance Tier**
Which review tier this plan gets (low/medium/high).
- *Log:* Importance score + reasoning.
- *Review:* Did reviewed plans perform better? Did any unreviewed plan fail in a way review would've caught?

**4. Child Task Scoping**
How the parent writes goal.md for each child — what context to include, how specific.
- *Log:* The goal as written.
- *Review:* Did the child have to guess at things the parent should've specified? Did irrelevant context confuse it?

### Review-Level Decisions

**5. Critic Assessment**
What's wrong with this plan.
- *Log:* The critique.
- *Review:* Were identified weaknesses real? Did the plan fail at a point the critic missed?

**6. Judge Assessment** (high importance only)
Is this critique valid?
- *Log:* Judgment + reasoning.
- *Review:* Did the judge correctly sort valid critiques from bad ones?

**7. Final Plan Selection**
Decider picks or synthesizes from candidates.
- *Log:* What was chosen, why, what was rejected.
- *Review:* Would a rejected plan have performed better?

### Knowledge Decisions

**8. Knowledge Retrieval**
What's relevant for this node from the library.
- *Log:* What was retrieved, what the node actually used.
- *Review:* Was critical knowledge available but not fetched? Was irrelevant knowledge fetched that cluttered context?

### Upward Flow Decisions

**9. Continue / Replan / Escalate**
Parent evaluates child result and decides what happens next.
- *Log:* Decision + reasoning, what in the child's result drove the choice.
- *Review:* Did premature continues lead to wasted work? Did late escalations waste subtrees? Did replans improve things or just churn?

**10. Replan Design**
If replanning, what changes and what stays.
- *Log:* Old plan vs. new plan, trigger, which completed work was preserved vs. discarded.
- *Review:* Was the replan better? Did it discard work it shouldn't have?

**11. Escalation Content**
What to tell the parent when escalating.
- *Log:* The escalation message.
- *Review:* Did the parent above have enough info to act, or did it need to re-investigate?

**12. Result Synthesis**
How to combine children's outputs into this node's result.
- *Log:* Individual child results vs. synthesized result.
- *Review:* Was information lost? Was the synthesis faithful or did it editorialize?

### Orchestration Decisions

**13. Zombie Detection**
Is this agent stuck or just working?
- *Log:* Time elapsed, file activity timestamps, action taken (nudge/kill/respawn).
- *Review:* Did we kill agents that were actually making progress?

**14. Computation Detection**
Is this a long computation or a stuck agent?
- *Log:* WAITING_FOR_COMPUTATION marker presence, duration, outcome.
- *Review:* Were computation timeouts appropriate?

## V1 Scope

- Sequential execution only — steps run one at a time
- Plans still label each step as **dependent** or **independent** (metadata for future parallel execution)
- Two node types: executor and planner, assigned by depth-adjusted C × I threshold (> 30)
- Ephemeral agents with file-based state
- Full decision logging at every node for post-run review
- Low and medium plan review tiers only (no high-importance tournament)
- Max tree depth of 5
- 10-second orchestrator poll interval
- Orchestrator logs all transitions to JSONL

## Future Expansions

See `future-expansions/` for detailed designs.

- [Parallel execution](future-expansions/parallel-execution.md)
- [Triage agent split](future-expansions/triage-agent-split.md)
- [Persistent agents](future-expansions/persistent-agents.md)
- [High-importance plan tournament](future-expansions/high-importance-plan-tournament.md)
- [Time budgets](future-expansions/time-budgets.md)
- [Filesystem watches](future-expansions/filesystem-watches.md)
- [Token budget propagation](future-expansions/token-budget-propagation.md)

## Open && Questions

See `CLAUDE.md` for the full list of questions flagged for A/B testing.
