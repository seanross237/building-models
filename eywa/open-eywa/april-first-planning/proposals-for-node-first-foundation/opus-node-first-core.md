# Opus Node-First Core

A concrete, implementable proposal for the Open-Eywa node foundation. This specifies actual field names, actual file paths, actual JSON schemas, and actual state transitions. An engineer should be able to start coding from this document.

---

## 1. What a node fundamentally is

A node is a directory on disk. It represents one bounded unit of work. It has:

- A **goal** (immutable, set at creation)
- A **status** (one of 5 values, written only by the orchestrator)
- A **phase** (what's happening inside "active", tracked in a JSON file)
- A **contract/** directory (JSON files the orchestrator reads)
- A **human/** directory (markdown files humans read)
- A **work/** directory (artifacts produced by agents)
- A **system/** directory (logs, run records, internal bookkeeping)
- A **children/** directory (child nodes, same structure recursively)

A node does not know what agent will work on it. It does not care what model is used. It knows its goal, its current state, and what has been produced so far.

**The node directory IS the data model.** There is no database. There is no in-memory state that isn't derived from files. If you `rm -rf` the node directory, that node ceases to exist. If you copy it, you have a clone.

---

## 2. What a node owns

| Owned thing | Location | Format | Mutable? |
|---|---|---|---|
| Goal | `contract/goal.json` | JSON | No |
| Status + phase | `contract/status.json` | JSON | Yes (orchestrator only) |
| Plan (machine) | `contract/plan.json` | JSON | Yes (planner agent) |
| Eval decision | `contract/eval.json` | JSON | Yes (evaluator agent) |
| Review verdict | `contract/review.json` | JSON | Yes (reviewer agent) |
| Cost tracking | `contract/cost.json` | JSON | Yes (orchestrator only) |
| Node config | `contract/config.json` | JSON | No (set at creation) |
| Goal (readable) | `human/goal.md` | Markdown | No |
| Plan (readable) | `human/plan.md` | Markdown | Yes |
| Final output | `human/final-output.md` | Markdown | Yes |
| Review (readable) | `human/review.md` | Markdown | Yes |
| Escalation reason | `human/escalation.md` | Markdown | Yes |
| Library knowledge | `human/knowledge.md` | Markdown | Yes |
| Work artifacts | `work/*` | Any | Yes |
| Run history | `system/runs/` | JSON + logs | Append-only |
| Background jobs | `system/jobs/` | JSON | Yes |
| Children | `children/` | Directories | Append (new children) |

A node does NOT own: its agent, its prompt, its model choice, its tool set. Those are supplied by the orchestrator at spawn time.

---

## 3. What an agent run is relative to a node

An agent run is a single process that:

1. Receives a prepared `AgentInput` (JSON, assembled by the orchestrator)
2. Reads from the node directory
3. Does work using tools
4. Writes artifacts back into the node
5. Produces an `AgentOutput` (JSON, validated by the orchestrator)
6. Exits

Key properties:

- **One at a time.** At most one agent run is active per node. Enforced by PID tracking.
- **Stateless.** No memory persists between runs. Context is reconstructed from files.
- **Many per node.** A single node may see runs from: librarian, planner, reviewer, decider, worker, evaluator, synthesizer. Each is a separate process.
- **Disposable.** If a run crashes, the orchestrator can spawn a fresh one.

Strict separation:

- The **orchestrator** reads `contract/` files and decides what to do. It never calls the LLM.
- The **agent runner** calls the LLM, manages the tool loop, writes files. It never reads `contract/status.json` or modifies node state directly.

---

## 4. The node state model

### Top-level status (5 values, closed enum)

```
pending -> active -> complete
                  -> escalated
                  -> cancelled
```

Five statuses. The orchestrator's state machine operates on these five values and nothing else.

### Phase (internal to "active")

When a node is `active`, it's in one of these phases:

| Phase | Meaning |
|---|---|
| `retrieving` | Librarian is fetching knowledge |
| `planning` | Planner is decomposing the task |
| `reviewing` | Reviewer is critiquing the plan |
| `deciding` | Decider is finalizing the plan |
| `executing` | Children are being worked through |
| `evaluating` | Mid-plan evaluator is checking a child result |
| `synthesizing` | Synthesizer is combining child outputs |
| `working` | Worker is doing direct work |
| `waiting_compute` | Background computation in progress |

Phases are informational. The core state machine only sees the 5 top-level statuses. New phases can be added without changing the state machine.

### status.json schema

```json
{
  "status": "active",
  "phase": "planning",
  "updated_at": "2026-04-01T14:22:03Z",
  "active_run_id": "run-002",
  "active_run_pid": 48291,
  "run_count": 2,
  "outcome": null,
  "outcome_reason": null
}
```

Terminal state example:

```json
{
  "status": "complete",
  "phase": null,
  "updated_at": "2026-04-01T14:45:12Z",
  "active_run_id": null,
  "active_run_pid": null,
  "run_count": 5,
  "outcome": "completed",
  "outcome_reason": "final-output.md validated"
}
```

Outcome values: `completed`, `escalated`, `cancelled`, `cost_cap`, `max_retries`, `timeout`.

---

## 5. State machine transitions

### Transition diagram

```
                  +-----------+
                  |  pending  |
                  +-----+-----+
                        |
                   orchestrator spawns first agent
                        |
                        v
                  +-----+-----+
          +------>|  active    |<------+
          |       +--+--+--+--+       |
          |          |  |  |          |
     replan/retry    |  |  |     child completes,
          |          |  |  |     more work to do
          +----------+  |  +----------+
                        |
           artifact contract satisfied
           OR escalation file written
           OR orchestrator detects failure
                        |
              +---------+---------+
              |         |         |
              v         v         v
         +--------+ +--------+ +--------+
         |complete| |escalated| |cancelled|
         +--------+ +--------+ +--------+
```

### Legal transitions

| From | To | Trigger |
|---|---|---|
| `pending` | `active` | Orchestrator spawns first agent (librarian or worker) |
| `active` | `complete` | `human/final-output.md` exists and validated |
| `active` | `escalated` | Agent wrote `contract/eval.json` with `"decision": "escalate"` |
| `active` | `cancelled` | Parent replanned, this node is no longer needed |
| `active` | `active` | Phase change within active (internal, no status transition) |

There is no `failed` status. Failure is a terminal `complete` with `outcome` set to `cost_cap`, `max_retries`, or `timeout`. This keeps terminal states to three (complete, escalated, cancelled) and encodes failure reason in the outcome field rather than multiplying statuses.

### What the orchestrator does in each state

**pending:**
1. Read `contract/goal.json` and `contract/config.json`
2. Spawn librarian (if library retrieval is enabled) or the initial agent role
3. Transition to `active`, set phase

**active (by phase):**

| Phase | Entry trigger | Orchestrator action | Exit trigger |
|---|---|---|---|
| `retrieving` | Node just became active | Wait for librarian run to finish | `human/knowledge.md` exists |
| `planning` | Knowledge ready (or skipped) | Spawn planner | `contract/plan.json` exists |
| `reviewing` | Plan exists, review required | Spawn reviewer | `contract/review.json` exists |
| `deciding` | Review exists | Spawn decider | `contract/plan.json` updated with `"approved": true` or escalation |
| `executing` | Plan approved | Create next unstarted child, or wait for active child | All children terminal |
| `evaluating` | A child just completed | Spawn mid-plan evaluator | `contract/eval.json` exists with `continue` / `replan` / `escalate` |
| `synthesizing` | All children complete | Spawn synthesizer | `human/final-output.md` exists |
| `working` | Node routed to worker | Spawn worker | `human/final-output.md` exists or escalation |
| `waiting_compute` | Agent started background job | Poll `system/jobs/` | Job complete, re-spawn agent |

**complete:** No action. Terminal.

**escalated:** No action. Terminal. Parent's evaluator handles it.

**cancelled:** No action. Terminal. Orchestrator recursively cancels children.

### What can go wrong per state

| State | Failure mode | Orchestrator response |
|---|---|---|
| `pending` | Goal file missing | Cannot create node. Validation error at creation time. |
| `active` | Agent crashes without output | Increment `run_count`, retry if under limit, else mark `complete` with `outcome: "max_retries"` |
| `active` | Agent writes invalid JSON to `contract/` | Agent runner rejects it, run marked failed, retry |
| `active` | Cost cap exceeded | Mark `complete` with `outcome: "cost_cap"` |
| `active` | Wall-clock timeout | Mark `complete` with `outcome: "timeout"` |
| `active` | Zombie PID (process dead, no output) | Kill, increment run count, retry |
| `active` | Agent writes `contract/eval.json` with unknown decision | Validation rejects it, run marked failed, retry |

---

## 6. Node directory spec

### Full layout

```
<node>/
  contract/
    goal.json              # REQ  | written by orchestrator at creation | read by orchestrator + agent runner
    status.json            # REQ  | written by orchestrator only        | read by orchestrator
    config.json            # REQ  | written by orchestrator at creation | read by orchestrator + agent runner
    plan.json              # OPT  | written by planner agent            | read by orchestrator
    review.json            # OPT  | written by reviewer agent           | read by orchestrator
    eval.json              # OPT  | written by evaluator/decider agent  | read by orchestrator
    cost.json              # REQ  | written by orchestrator             | read by orchestrator
  human/
    goal.md                # REQ  | written by orchestrator at creation | read by humans
    plan.md                # OPT  | written by planner agent            | read by humans
    final-output.md        # OPT  | written by worker/synthesizer       | read by humans + parent synthesizer
    review.md              # OPT  | written by reviewer agent           | read by humans
    escalation.md          # OPT  | written by agent on escalation      | read by humans
    knowledge.md           # OPT  | written by librarian agent          | read by humans + subsequent agents
  work/
    ...                    # OPT  | written by agents                   | read by agents (scratch space)
  system/
    runs/
      run-001/
        input.json         # what the agent received (AgentInput)
        output.json        # what the agent returned (AgentOutput)
        meta.json          # timing, model, cost, exit reason
        loop.jsonl         # per-turn agent loop log
      run-002/
        ...
    jobs/
      job-<id>.json        # background computation metadata
  children/
    step-01-<slug>/        # child node, same structure recursively
    step-02-<slug>/
```

REQ = required (must exist for node to be valid). OPT = created as needed by agents.

### contract/goal.json

```json
{
  "schema_version": 1,
  "node_id": "step-02-prove-convergence",
  "parent_id": "root",
  "goal": "Prove that the sequence converges for all initial values > 0",
  "created_at": "2026-04-01T14:00:00Z",
  "depth": 1,
  "complexity": 8,
  "importance": 9
}
```

Immutable after creation. The `node_id` is also the directory name.

### contract/config.json

```json
{
  "schema_version": 1,
  "initial_mode": "planner",
  "cost_cap_usd": 5.00,
  "timeout_seconds": 3600,
  "max_retries": 5,
  "review_required": true,
  "library_retrieval": true,
  "model_overrides": {}
}
```

Set at creation based on mission config + routing rules. The orchestrator reads this to know how to handle the node.

### contract/plan.json

Written by the planner agent. Read by the orchestrator to create children.

```json
{
  "schema_version": 1,
  "approved": false,
  "steps": [
    {
      "id": "step-01-establish-bounds",
      "goal": "Establish upper and lower bounds for the sequence",
      "mode": "worker",
      "complexity": 5,
      "importance": 8,
      "depends_on": []
    },
    {
      "id": "step-02-monotonicity",
      "goal": "Prove the sequence is eventually monotone",
      "mode": "worker",
      "complexity": 7,
      "importance": 9,
      "depends_on": ["step-01-establish-bounds"]
    }
  ],
  "rationale": "Split into bounds and monotonicity, then convergence follows from bounded monotone sequence theorem"
}
```

The `approved` field starts `false`. The decider sets it to `true` (or the plan is replaced). The orchestrator only creates children from an approved plan.

### contract/review.json

Written by the reviewer agent.

```json
{
  "schema_version": 1,
  "verdict": "needs_revision",
  "issues": [
    {
      "severity": "major",
      "step_id": "step-02-monotonicity",
      "description": "Monotonicity approach assumes positivity, which hasn't been established yet"
    }
  ],
  "strengths": ["Good decomposition", "Complexity scores are reasonable"],
  "recommendation": "Add a step to establish positivity before the monotonicity proof"
}
```

Verdict values: `approve`, `needs_revision`, `reject`.

### contract/eval.json

Written by the mid-plan evaluator, decider, or any agent that needs to signal a decision.

```json
{
  "schema_version": 1,
  "decision": "continue",
  "reason": "Child step-01 completed successfully with valid bounds",
  "replan_instructions": null
}
```

Decision values: `continue`, `replan`, `escalate`.

If `replan`, the `replan_instructions` field tells the planner what to change. The orchestrator cancels remaining children and re-enters the planning phase.

### contract/cost.json

Written and maintained by the orchestrator.

```json
{
  "schema_version": 1,
  "self_usd": 0.42,
  "children_usd": 1.87,
  "total_usd": 2.29,
  "cap_usd": 5.00,
  "runs": [
    {"run_id": "run-001", "role": "librarian", "cost_usd": 0.08},
    {"run_id": "run-002", "role": "planner", "cost_usd": 0.34}
  ]
}
```

Updated after every run completes. `total_usd = self_usd + children_usd`. The orchestrator checks `total_usd <= cap_usd` before every spawn.

### system/runs/run-NNN/meta.json

```json
{
  "run_id": "run-002",
  "role": "planner",
  "model": "anthropic/claude-sonnet-4",
  "variant": null,
  "started_at": "2026-04-01T14:10:00Z",
  "finished_at": "2026-04-01T14:12:30Z",
  "pid": 48291,
  "cost_usd": 0.34,
  "tokens_in": 6200,
  "tokens_out": 2100,
  "iterations": 4,
  "artifacts_produced": ["contract/plan.json", "human/plan.md"],
  "exit_reason": "artifacts_satisfied"
}
```

Exit reason values: `artifacts_satisfied`, `escalated`, `max_iterations`, `error`, `output_validation_failed`, `zombie_killed`, `timeout`.

---

## 7. Completion, failure, and escalation

### Completion conditions

A node transitions to `complete` with `outcome: "completed"` when ALL of:

1. No active run
2. `human/final-output.md` exists
3. For planner nodes: all children are terminal
4. `total_usd <= cap_usd`

Validation function:

```python
def can_complete(node: Node) -> bool:
    if node.status.active_run_pid is not None:
        return False
    if not (node.path / "human" / "final-output.md").exists():
        return False
    if node.has_children():
        if not all(c.is_terminal() for c in node.children()):
            return False
    if node.cost.total_usd > node.config.cost_cap_usd:
        return False
    return True
```

### Escalation conditions

A node transitions to `escalated` when:

1. An agent wrote `contract/eval.json` with `"decision": "escalate"`
2. `human/escalation.md` exists (agent should write it; if missing, orchestrator writes a stub)

The parent's evaluator receives the escalation and decides what to do.

### Failure conditions (orchestrator-driven)

| Condition | Outcome value | What happens |
|---|---|---|
| `cost.total_usd > config.cost_cap_usd` | `cost_cap` | Immediate transition to `complete` with outcome |
| `status.run_count >= config.max_retries` | `max_retries` | No more retries, transition to `complete` |
| Wall-clock since `goal.created_at` > `config.timeout_seconds` | `timeout` | Kill active run if any, transition to `complete` |

Agents never mark themselves as failed. They either produce output, escalate, or crash. The orchestrator detects and categorizes failure.

### Cancellation

The orchestrator sets a node to `cancelled` when a parent replans and this node is no longer part of the new plan. The orchestrator recursively cancels all descendants.

---

## 8. Agent input/output contract

### AgentInput (assembled by orchestrator, written to system/runs/run-NNN/input.json)

```json
{
  "schema_version": 1,
  "role": "planner",
  "node_id": "step-02-prove-convergence",
  "goal": "Prove that the sequence converges for all initial values > 0",
  "depth": 1,

  "system_prompt_path": "stuff-for-agents/planning/planner/system-prompt.md",
  "tools_enabled": ["read_file", "write_file", "edit_file", "run_python", "run_sage"],

  "context": {
    "knowledge": "Contents of human/knowledge.md or null",
    "parent_output": "Contents of parent's human/final-output.md or null",
    "sibling_outputs": [
      {"node_id": "step-01-establish-bounds", "output": "Contents of step-01's human/final-output.md"}
    ],
    "prior_plan": null,
    "prior_review": null
  },

  "role_output_schema": {
    "contract_files": {
      "plan.json": {"required": true, "schema": "plan_v1"}
    },
    "human_files": {
      "plan.md": {"required": false}
    }
  },

  "constraints": {
    "max_iterations": 20,
    "write_paths": ["human/", "work/", "contract/plan.json"],
    "read_paths": ["*"]
  }
}
```

Key design: the `role_output_schema` tells the agent runner exactly what files this role must produce and what schemas they must conform to. New roles define new output schemas without changing the protocol.

The `context` block is assembled by the orchestrator from sibling and parent files. The agent never has to figure out where to find context -- it's delivered.

### AgentOutput (produced by agent runner, written to system/runs/run-NNN/output.json)

```json
{
  "schema_version": 1,
  "role": "planner",
  "run_id": "run-002",
  "exit_reason": "artifacts_satisfied",
  "artifacts_written": [
    {"path": "contract/plan.json", "valid": true},
    {"path": "human/plan.md", "valid": true}
  ],
  "escalation": null,
  "error": null
}
```

If the agent escalated:

```json
{
  "schema_version": 1,
  "role": "worker",
  "run_id": "run-003",
  "exit_reason": "escalated",
  "artifacts_written": [
    {"path": "contract/eval.json", "valid": true},
    {"path": "human/escalation.md", "valid": true}
  ],
  "escalation": {
    "reason": "The problem requires group theory results not available in the current library"
  },
  "error": null
}
```

### Validation flow

1. Agent runner calls LLM, manages tool loop
2. Agent writes files to `human/`, `work/`, `contract/<role-specific files>`
3. Agent runner reads back all files listed in `role_output_schema`
4. For each `contract/` file: validate against declared JSON schema
5. If validation passes: write `output.json` with `exit_reason: "artifacts_satisfied"`
6. If validation fails: write `output.json` with `exit_reason: "output_validation_failed"`, orchestrator decides whether to retry
7. Agent runner writes `meta.json` with timing and cost data
8. Agent process exits

The orchestrator never touches the LLM. The agent runner never touches `contract/status.json`. Clean separation.

### How this stays stable as new agent types are added

The `AgentInput` and `AgentOutput` structures are role-agnostic. The role-specific part is:

- `role_output_schema` in the input (what files to produce)
- `artifacts_written` in the output (what was actually produced)

Adding a `verifier` role means defining:

```json
"role_output_schema": {
  "contract_files": {
    "verification.json": {"required": true, "schema": "verification_v1"}
  },
  "human_files": {
    "verification.md": {"required": false}
  }
}
```

No changes to AgentInput/AgentOutput structure. No changes to the agent runner. Just a new schema definition and orchestrator routing logic.

---

## 9. The orchestrator as a pure function

### Core idea

```python
def tick(tree: dict[str, Node]) -> list[Action]:
    """Read the entire tree. Return actions. No side effects."""
    actions = []
    for node_id, node in tree.items():
        actions.extend(_tick_node(node))
    return actions
```

Actions are value objects:

```python
@dataclass
class SpawnAgent:
    node_id: str
    role: str
    model: str | None = None

@dataclass
class CreateChild:
    parent_id: str
    step: PlanStep  # from contract/plan.json

@dataclass  
class UpdateStatus:
    node_id: str
    new_status: str
    phase: str | None = None
    outcome: str | None = None
    reason: str | None = None

@dataclass
class CancelNode:
    node_id: str
    reason: str

Action = SpawnAgent | CreateChild | UpdateStatus | CancelNode
```

### The decision table

This replaces a chain of if/else. Each row is independently testable.

| Status | Phase | Condition | Action |
|---|---|---|---|
| `pending` | - | always | `SpawnAgent(librarian)` if retrieval enabled, else `SpawnAgent(initial_mode)` + `UpdateStatus(active)` |
| `active` | `retrieving` | run finished, `human/knowledge.md` exists | `UpdateStatus(active, phase=planning or working)` + `SpawnAgent(mode)` |
| `active` | `retrieving` | run finished, no knowledge file | retry or fail |
| `active` | `planning` | run finished, `contract/plan.json` valid | if review required: `UpdateStatus(active, phase=reviewing)` + `SpawnAgent(reviewer)` else: approve and start executing |
| `active` | `planning` | run finished, no valid plan | retry or fail |
| `active` | `reviewing` | run finished, `contract/review.json` exists | `UpdateStatus(active, phase=deciding)` + `SpawnAgent(decider)` |
| `active` | `deciding` | run finished, plan approved | `UpdateStatus(active, phase=executing)` + `CreateChild(first step)` |
| `active` | `deciding` | run finished, escalated | `UpdateStatus(escalated)` |
| `active` | `executing` | active child exists | wait (no action) |
| `active` | `executing` | child just completed | `SpawnAgent(evaluator)` + `UpdateStatus(active, phase=evaluating)` |
| `active` | `evaluating` | eval decision = continue, more children | `CreateChild(next step)` + `UpdateStatus(active, phase=executing)` |
| `active` | `evaluating` | eval decision = continue, no more children | `SpawnAgent(synthesizer)` + `UpdateStatus(active, phase=synthesizing)` |
| `active` | `evaluating` | eval decision = replan | cancel remaining children + `UpdateStatus(active, phase=planning)` + `SpawnAgent(planner)` |
| `active` | `evaluating` | eval decision = escalate | `UpdateStatus(escalated)` |
| `active` | `synthesizing` | run finished, `human/final-output.md` exists | `UpdateStatus(complete, outcome=completed)` |
| `active` | `working` | run finished, `human/final-output.md` exists | `UpdateStatus(complete, outcome=completed)` |
| `active` | `working` | run finished, escalated | `UpdateStatus(escalated)` |
| `active` | `waiting_compute` | job complete | re-spawn the agent that started the job |
| `active` | any | cost cap exceeded | `UpdateStatus(complete, outcome=cost_cap)` |
| `active` | any | retry limit exceeded | `UpdateStatus(complete, outcome=max_retries)` |
| `active` | any | timeout exceeded | `UpdateStatus(complete, outcome=timeout)` |

This table IS the orchestrator. Each row maps to a test case. The `tick()` function walks the tree and pattern-matches against these rows.

### The executor

```python
def execute(actions: list[Action], tree: Tree, runner: AgentRunner):
    """Apply actions to the filesystem. Side effects happen here."""
    for action in actions:
        match action:
            case SpawnAgent(node_id, role, model):
                input_json = build_agent_input(tree[node_id], role)
                runner.spawn(node_id, input_json, model)
            case CreateChild(parent_id, step):
                create_child_directory(tree[parent_id], step)
            case UpdateStatus(node_id, new_status, phase, outcome, reason):
                write_status(tree[node_id], new_status, phase, outcome, reason)
                log_transition(node_id, new_status, outcome, reason)
            case CancelNode(node_id, reason):
                cancel_recursively(tree[node_id], reason)
```

Separation: `tick()` is pure logic, testable without a filesystem. `execute()` is side effects, tested with integration tests.

---

## 10. Logging as a reader

The orchestrator does not instrument itself with logging calls scattered through the code. Instead:

1. Every `write_status()` call appends to `orchestrator.jsonl` (one line per transition)
2. Every agent run produces `system/runs/run-NNN/meta.json` and `loop.jsonl`
3. A separate **log reader** can reconstruct the full mission timeline by:
   - Walking all nodes
   - Reading `contract/status.json` for current state
   - Reading `system/runs/*/meta.json` for run history
   - Reading `orchestrator.jsonl` for transition history

The file tree is self-describing. The log reader is a view, not an instrumenter. This means you can add new visualizations, dashboards, or analysis tools without modifying the orchestrator.

### orchestrator.jsonl entry format

```json
{
  "ts": "2026-04-01T14:22:03Z",
  "event": "status_change",
  "node_id": "step-02-prove-convergence",
  "from_status": "pending",
  "to_status": "active",
  "phase": "retrieving",
  "outcome": null,
  "run_id": "run-001",
  "cost_usd_at_transition": 0.00
}
```

---

## 11. Hard in code vs. soft in model behavior

### Hard (enforced in code, tested, never delegated to the model)

| Rule | Where enforced |
|---|---|
| Status transitions follow the state machine | `write_status()` with transition validation |
| Only 5 legal status values | Enum in `write_status()` |
| Only orchestrator writes `contract/status.json` | Agent sandbox path whitelist |
| Agents write only to allowed paths per role | Path whitelist in agent runner |
| One active run per node | PID check before spawn |
| Cost cap kills the node | Check before every spawn |
| Completion requires artifacts on disk | `can_complete()` checks file existence |
| Every status transition is logged | Inside `write_status()` |
| Run records are append-only | Monotonic run numbering |
| Agent output is schema-validated | JSON schema check in agent runner |
| Retry limit enforced | `run_count` check before spawn |
| Children only created from approved plans | `plan.json.approved == true` check |

### Soft (model judgment)

| Behavior | Why soft |
|---|---|
| How a plan decomposes a task | Many valid decompositions |
| How a review critiques a plan | Quality varies, but verdict field is validated |
| How a worker reasons | Contract is the output file, not the process |
| How a synthesizer combines outputs | Judgment call |
| How verbose the markdown is | Markdown is for humans |
| Whether to escalate vs. keep trying | Judgment, but the eval file is validated |

---

## 12. Extensibility

Adding a new agent type (e.g., `verifier`) requires:

1. A system prompt at `stuff-for-agents/<role>/system-prompt.md`
2. An output schema (what `contract/` and `human/` files the role produces)
3. A config entry (model, tools, token limits)
4. Orchestrator routing logic (when to spawn it -- a new row in the decision table)

It does NOT require: new status values, new directory structures, changes to AgentInput/AgentOutput, changes to the state machine, or changes to the core validation functions.

---

## 13. A/B testability

Each run record includes a `variant` field. To A/B test:

1. Define variants in mission config
2. Run the same mission with different variants (or split per-node)
3. Compare at the node level: same goal, same structure, different run records
4. Metrics: cost, time, success rate, iteration count, output quality (via judge)

Because runs are isolated in `system/runs/run-NNN/`, there's no collision. You can reset a node to `pending` and re-run with a different variant.

---

## 14. Risks and tradeoffs

### Risk 1: Orchestrator becomes a pile of conditionals

The 5-status model pushes sub-phase logic into file inspection. Without discipline, `tick()` becomes untestable.

**Mitigation:** The decision table (Section 9) is the structure. Each row is one test case. If you can't express a new behavior as a row in the table, the design needs rethinking, not more if/else.

### Risk 2: JSON schema drift

If `contract/plan.json` has one shape for planner-v1 and a different shape for planner-v2, downstream consumers break.

**Mitigation:** Every contract file includes `"schema_version": N`. The orchestrator validates against the declared version. Breaking changes increment the version. Old versions stay supported during migration.

### Risk 3: Agents write garbage JSON

Models produce malformed JSON regularly. If `contract/plan.json` is invalid, the node is stuck.

**Mitigation:** The agent runner validates all JSON before writing to `contract/`. Invalid output -> `exit_reason: "output_validation_failed"` -> orchestrator retries. The agent never directly writes to `contract/`; the agent runner mediates.

### Risk 4: Dual-write overhead

Agents now produce JSON (for the orchestrator) and markdown (for humans). More tokens, more cost.

**Mitigation:** Agents produce JSON only. The agent runner (or a post-processing step) renders markdown from the JSON. This keeps agents focused on structured output and makes markdown formatting consistent. Cost increase is minimal since the rendering is deterministic, not LLM-generated.

### Risk 5: Migration from current system

The current system uses `for-orchestrator/` with text files and parses markdown. `contract/` with JSON is a breaking change.

**Migration path:**
1. Build the new node layout alongside the old one
2. Write an adapter that reads old-format nodes and presents them as new-format
3. New missions use the new format
4. Old missions continue working through the adapter
5. Once all active missions complete, remove the adapter

### Risk 6: Phase explosion

As the system grows, new phases get added to active. If phases become load-bearing (orchestrator behavior changes based on phase value), we've just recreated the 14-status problem.

**Mitigation:** Phases are advisory. The orchestrator's decision table keys on `(status, file_conditions)`, not `(status, phase)`. The phase is set for human readability and logging. The orchestrator derives what to do from what files exist, not from the phase string. This is a discipline rule that must be enforced in code review.

### Risk 7: The contract/ directory becomes a dumping ground

Teams add new JSON files to `contract/` for every new feature, and the directory grows unbounded.

**Mitigation:** Strict rule: a file in `contract/` must be read by the orchestrator's `tick()` function. If the orchestrator doesn't read it, it belongs in `work/` or `human/`. This is checkable: grep the orchestrator code for `contract/` file reads and compare against the directory listing.

### Tradeoff: Simplicity vs. expressiveness

This design cannot express peer-to-peer node communication, parallel child execution, or conditional branching within a plan. Those features require extensions.

**Why this is acceptable:** The current system doesn't have them either. This design does not prevent adding them later -- it just doesn't design for them now. The contract/ protocol is extensible. New file types can be added. The decision table can grow new rows. But the core 5-status state machine stays fixed.
