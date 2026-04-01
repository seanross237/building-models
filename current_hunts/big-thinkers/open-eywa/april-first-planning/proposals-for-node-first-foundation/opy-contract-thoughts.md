# Node Contract Spec

This is the concrete contract for an Open-Eywa node. It defines every file, every legal state, every transition, every validation, and every invariant. If something is not in this document, it is not part of the node contract.

---

## 1. The Node Directory

A node is a directory. Every node has exactly five subdirectories:

```
<node>/
  input/
  output/
  for-orchestrator/
  system/
  children/
```

No other top-level entries. If a node directory exists, all five subdirectories exist. They are created atomically at node creation time.

---

## 2. File Manifest

### input/ — Immutable context, written before the node starts

| File | Format | Written by | When | Required? |
|---|---|---|---|---|
| `goal.md` | markdown | orchestrator | node creation (root only) | yes (root) |
| `parent-instructions.md` | markdown | orchestrator | node creation (children) | yes (children) |
| `context.md` | markdown | orchestrator | child creation, if prior-step context exists | no |
| `knowledge.md` | markdown | librarian agent | retrieval phase | no (written if retrieval runs) |
| `instructions-<role>.md` | markdown | orchestrator | before each agent spawn | yes (per spawn) |

Rules:
- A node must have exactly one of `goal.md` or `parent-instructions.md`. Root nodes get `goal.md`. Child nodes get `parent-instructions.md`.
- `knowledge.md` replaces v1's `retrieved_relevant_knowledge_from_library.md`.
- `instructions-<role>.md` is regenerated before each spawn. Multiple may exist if the node has been through multiple roles (librarian, then planner, etc.).
- Nothing in `input/` is ever deleted or overwritten after initial write, except `instructions-<role>.md` which is regenerated per-spawn.

### output/ — Artifacts produced by agents

| File | Format | Written by | When | Required? |
|---|---|---|---|---|
| `plan.md` | markdown | planner agent | planning phase | only for planner nodes |
| `review.md` | markdown | plan-reviewer agent | review phase | only if review ran |
| `final-output.md` | markdown | worker or synthesizer agent | work or synthesis phase | required for completed outcome |
| `state.md` | markdown | any agent | during runs | no (advisory) |
| `escalation.md` | markdown | any escalation-eligible agent | when escalating | required for escalated outcome |

Rules:
- `final-output.md` is THE terminal artifact. A node cannot reach outcome=completed without it.
- `escalation.md` is THE escalation artifact. A node cannot reach outcome=escalated without it.
- `state.md` is advisory. Agents write it to leave breadcrumbs for later runs. The orchestrator never gates decisions on it.
- `plan.md` becomes authoritative for child creation once the orchestrator marks it approved (by writing the approval marker inline or in a separate control file — see for-orchestrator section).
- Agents may write other files into `output/` (e.g., `context-for-next-step.md`). These are not part of the contract but are not forbidden.

### for-orchestrator/ — Control state, mostly orchestrator-written

| File | Format | Written by | Read by | Content |
|---|---|---|---|---|
| `status` | plain text | orchestrator only | orchestrator | One of: `pending`, `running`, `done`, `failed`, `timed_out` |
| `phase` | plain text | orchestrator only | orchestrator, humans | Current sub-phase of `running`. See phase list. |
| `outcome` | plain text | orchestrator only | orchestrator, parent | One of: `completed`, `escalated`, `cancelled`. Written when status becomes `done`. |
| `failure-reason` | plain text | orchestrator only | orchestrator, humans | Written when status becomes `failed` or `timed_out`. See reason list. |
| `mode` | plain text | orchestrator | orchestrator | The role for the node's primary agent: `planner`, `worker`, etc. |
| `eval-decision` | plain text | evaluator/synthesizer agent | orchestrator | One of: `continue`, `replan`, `escalate`, `synthesize`. Consumed and deleted by orchestrator after reading. |
| `cost.json` | JSON | orchestrator | orchestrator | See cost tracking section. |
| `waiting` | plain text | agent (via tool) | orchestrator | Marker: background computation in progress. Contains job ID. |
| `computation-result` | plain text | background job script | orchestrator | Marker: background computation finished. Contains job dir path. |

Rules:
- **`status` is the single most important file in the system.** Only the orchestrator writes it. Agents never touch it. Every write to `status` is logged.
- **`phase` is informational.** The orchestrator sets it when it knows what's happening. It is never used as a gate for decisions — decisions are based on status + file inspection. Phase exists so a human reading the directory can see what's going on.
- **`outcome` only exists when status is `done`.** It is never written before status transitions to done.
- **`failure-reason` only exists when status is `failed` or `timed_out`.**
- **`eval-decision` is ephemeral.** The orchestrator reads it, acts on it, and deletes it. Stale decision files must not drive fresh transitions. If the file exists when a new evaluator is about to be spawned, the orchestrator deletes it first.
- **`mode` is written at creation and may be updated by the orchestrator** (e.g., if complexity/importance routing changes the assignment).
- **`cost.json` is updated synchronously** after every run completes, before the orchestrator takes any other action on that node.

### system/ — Run history and internal bookkeeping

```
system/
  runs/
    run-001/
      meta.json
      loop.jsonl
      usage.json
      stdout.log
      stderr.log
    run-002/
      ...
  artifacts/
    python/
    sage/
    lean/
  jobs/
    <job-id>/
      command.txt
      cwd.txt
      status.txt
      pid.txt
      stdout.txt
      stderr.txt
      started_at.txt
      finished_at.txt
      returncode.txt
      run.sh
```

Rules:
- Run directories are numbered monotonically: `run-001`, `run-002`, etc. Never overwritten.
- `meta.json` is THE record of what happened in a run. See run record section.
- `loop.jsonl` is append-only per-turn log of the agent loop.
- `usage.json` is the token/cost summary for that run.
- `artifacts/` holds generated scripts (python, sage, lean). Organized by type.
- `jobs/` holds background computation metadata. Same structure as v1.
- Nothing in `system/` is read by agents. It is purely for the orchestrator and post-run inspection.

### children/ — Child nodes

```
children/
  step-01-<slug>/     # full node structure, recursively
  step-02-<slug>/
```

Rules:
- Children are created by the orchestrator, not by agents.
- Child naming: `step-NN-<slug>` where NN is zero-padded step number and slug is a sanitized short name from the plan.
- Each child is a complete node with the same five subdirectories.
- Children are independent nodes. They do not share files with siblings or parents except through the orchestrator assembling context.

---

## 3. Status Model

### The Enum (closed, never extended)

```python
class NodeStatus(str, Enum):
    PENDING   = "pending"
    RUNNING   = "running"
    DONE      = "done"
    FAILED    = "failed"
    TIMED_OUT = "timed_out"
```

### Legal Transitions

```
pending   -> running
running   -> done
running   -> failed
running   -> timed_out
pending   -> done        (only for cancellation: outcome=cancelled)
pending   -> failed      (only for cost cap on creation)
```

No other transitions are legal. `done`, `failed`, and `timed_out` are terminal — no transitions out.

### The Write Protocol

Every status write follows this protocol:

```python
def write_status(node, expected: str, new: str, **kwargs) -> bool:
    current = read(node / "for-orchestrator/status")
    if current != expected:
        return False  # someone else changed it
    write(node / "for-orchestrator/status", new)
    log_event(node, "status_change", from=expected, to=new, **kwargs)
    return True
```

The expected-value check prevents double transitions. If the status has already moved (e.g., by a concurrent poll cycle), the write is silently skipped.

---

## 4. Phase Model

### The Enum (open, can be extended without changing the state machine)

```python
class NodePhase(str, Enum):
    RETRIEVING      = "retrieving"
    PLANNING        = "planning"
    REVIEWING       = "reviewing"
    DECIDING        = "deciding"
    EXECUTING       = "executing"
    EVALUATING      = "evaluating"
    SYNTHESIZING    = "synthesizing"
    WORKING         = "working"
    WAITING_COMPUTE = "waiting_compute"
```

### Rules

- Phase is only meaningful when status is `running`.
- Phase is set by the orchestrator at the same time as the action that causes the phase (e.g., spawning a planner sets phase to `planning`).
- Phase is never used as a gate. The orchestrator decides what to do based on status + file inspection. Phase is a human-readable label for what's currently happening.
- When status leaves `running`, the orchestrator clears the phase file (deletes it or writes empty).
- New phases can be added freely. Adding a phase requires: (1) add to the enum, (2) set it in the orchestrator when the corresponding action happens. No other changes needed.

---

## 5. Outcome Model

### The Enum (closed for done, open for failure reasons)

```python
class NodeOutcome(str, Enum):
    COMPLETED = "completed"
    ESCALATED = "escalated"
    CANCELLED = "cancelled"

class FailureReason(str, Enum):
    COST_CAP_EXCEEDED   = "cost_cap_exceeded"
    MAX_RETRIES         = "max_retries_exceeded"
    ZOMBIE_DETECTED     = "zombie_detected"
    API_TIMEOUT         = "api_timeout"
    NO_ARTIFACTS        = "no_artifacts_produced"
```

### Rules

- `outcome` is written to `for-orchestrator/outcome` at the same time as `status` transitions to `done`.
- `failure-reason` is written to `for-orchestrator/failure-reason` at the same time as `status` transitions to `failed` or `timed_out`.
- A node with status=done MUST have an outcome file. A node with status=failed or timed_out MUST have a failure-reason file.
- FailureReason can grow as we discover new failure modes. Adding a reason requires no state machine changes.

---

## 6. Role Artifact Contracts

Each role has a list of required artifacts. A run satisfies its contract when all required artifacts exist OR the role is escalation-eligible and `escalation.md` exists.

| Role | Required artifacts | Escalation-eligible? |
|---|---|---|
| `librarian` | `input/knowledge.md` | no |
| `planner` | `output/plan.md` | yes |
| `worker` | `output/final-output.md` | yes |
| `plan-reviewer` | `output/review.md` | no |
| `plan-decider` | approved `output/plan.md` | yes |
| `mid-plan-evaluator` | `for-orchestrator/eval-decision` | yes |
| `synthesizer` | `output/final-output.md` + `for-orchestrator/eval-decision` (value: `synthesize`) | yes |

### Adding a new role

Adding a new role (e.g., `verifier`) requires:
1. Add a row to this table with required artifacts and escalation eligibility.
2. Write a system prompt at `stuff-for-agents/<role>/system-prompt.md`.
3. Add config entry for model, tools, token limits.
4. Add orchestrator logic for when to spawn it.

The status enum does not change. The directory layout does not change. The validation functions gain one row.

---

## 7. The Three Handoff Validations

### 7a. Node Creation Validation

Called by the action executor after creating a child node directory. Fails loudly.

```python
def validate_node_creation(node_dir: Path) -> None:
    goal = node_dir / "input" / "goal.md"
    instructions = node_dir / "input" / "parent-instructions.md"
    assert goal.exists() or instructions.exists(), \
        f"Node {node_dir.name} has no goal"
    
    status_file = node_dir / "for-orchestrator" / "status"
    assert status_file.exists(), \
        f"Node {node_dir.name} has no status file"
    assert status_file.read_text().strip() == "pending", \
        f"Node {node_dir.name} status is not pending"
    
    mode_file = node_dir / "for-orchestrator" / "mode"
    assert mode_file.exists(), \
        f"Node {node_dir.name} has no mode file"
```

### 7b. Run Completion Validation

Called by the orchestrator after a run exits (process death or clean exit). Returns bool — does not raise.

```python
REQUIRED_ARTIFACTS = {
    "librarian":          ["input/knowledge.md"],
    "planner":            ["output/plan.md"],
    "worker":             ["output/final-output.md"],
    "plan-reviewer":      ["output/review.md"],
    "plan-decider":       [],  # checks plan approval inline
    "mid-plan-evaluator": ["for-orchestrator/eval-decision"],
    "synthesizer":        ["output/final-output.md", "for-orchestrator/eval-decision"],
}

ESCALATION_ELIGIBLE = {"planner", "worker", "plan-decider", "mid-plan-evaluator", "synthesizer"}

def validate_run_completion(node_dir: Path, role: str) -> bool:
    if role in ESCALATION_ELIGIBLE and (node_dir / "output" / "escalation.md").exists():
        return True
    required = REQUIRED_ARTIFACTS.get(role, [])
    return all((node_dir / path).exists() for path in required)
```

### 7c. Node Completion Validation

Called by the action executor before writing status=done. Fails loudly.

```python
def validate_node_completion(node_dir: Path, outcome: str) -> None:
    if outcome == "completed":
        assert (node_dir / "output" / "final-output.md").exists(), \
            f"Cannot complete {node_dir.name}: no final-output.md"
    elif outcome == "escalated":
        assert (node_dir / "output" / "escalation.md").exists(), \
            f"Cannot escalate {node_dir.name}: no escalation.md"
    elif outcome == "cancelled":
        pass  # no artifact needed
    else:
        raise ValueError(f"Unknown outcome: {outcome}")
```

---

## 8. Cost Tracking Contract

### cost.json format

```json
{
  "self_usd": 0.42,
  "children_usd": 1.87,
  "total_usd": 2.29,
  "cap_usd": 10.00
}
```

### Rules

- `self_usd` = sum of all this node's run costs (from `system/runs/*/usage.json`).
- `children_usd` = sum of all children's `total_usd`.
- `total_usd` = `self_usd` + `children_usd`.
- `cap_usd` = inherited from mission config, can be overridden per-node.
- Updated synchronously after every run completes, before the orchestrator takes any other action on the node.
- The orchestrator also re-aggregates children costs when a child's status changes.

### Enforcement

```python
def check_cost_cap(node_dir: Path) -> bool:
    cost_file = node_dir / "for-orchestrator" / "cost.json"
    if not cost_file.exists():
        return True
    cost = json.loads(cost_file.read_text())
    return cost["total_usd"] <= cost["cap_usd"]
```

If `check_cost_cap()` returns False, the orchestrator transitions the node to `failed` with reason `cost_cap_exceeded`. No model consultation. Hard kill.

The orchestrator checks the cost cap:
- Before every agent spawn
- After every run completes
- After every child status change

---

## 9. Run Record Contract

### meta.json format

```json
{
  "run_id": "run-003",
  "role": "planner",
  "model": "anthropic/claude-sonnet-4",
  "variant": {},
  "started_at": "2026-04-01T14:30:00Z",
  "finished_at": "2026-04-01T14:32:15Z",
  "pid": 48291,
  "exit_reason": "artifacts_satisfied",
  "iterations": 4,
  "prompt_tokens": 6200,
  "completion_tokens": 2100,
  "cost_usd": 0.18,
  "artifacts_produced": ["output/plan.md", "output/state.md"]
}
```

### Fields

| Field | Type | Set when |
|---|---|---|
| `run_id` | string | spawn time |
| `role` | string | spawn time |
| `model` | string | spawn time |
| `variant` | object | spawn time (empty until A/B testing is implemented) |
| `started_at` | ISO 8601 | spawn time |
| `finished_at` | ISO 8601 or null | run exit |
| `pid` | int | spawn time |
| `exit_reason` | string | run exit |
| `iterations` | int | run exit |
| `prompt_tokens` | int | run exit (summed from usage) |
| `completion_tokens` | int | run exit (summed from usage) |
| `cost_usd` | float | run exit (summed from usage) |
| `artifacts_produced` | list of strings | run exit (files written during run, relative to node) |

### exit_reason values

| Value | Meaning |
|---|---|
| `artifacts_satisfied` | All required artifacts for this role now exist |
| `max_iterations` | Hit the iteration limit without satisfying artifacts |
| `error` | LLM API error or uncaught exception |
| `zombie_killed` | Orchestrator killed this run for inactivity |
| `cost_cap` | Run stopped because node cost cap was reached |

---

## 10. Eval-Decision Contract

The evaluator and synthesizer write `for-orchestrator/eval-decision`.

### Legal values

| Value | Written by | Meaning |
|---|---|---|
| `continue` | mid-plan-evaluator | Proceed to next plan step |
| `replan` | mid-plan-evaluator | Cancel remaining steps, re-enter planning |
| `escalate` | mid-plan-evaluator | Give up, punt to parent |
| `synthesize` | synthesizer | Synthesis is done, node can complete |

### Consumption protocol

1. Orchestrator reads the file.
2. Orchestrator acts on the value.
3. Orchestrator deletes the file.

If the file contains an unrecognized value, the orchestrator logs a warning and treats it as an error (does not silently ignore).

If the file exists when a new evaluator is about to be spawned, the orchestrator deletes it first. Stale decisions must never drive fresh transitions.

---

## 11. Plan Approval Contract

Plans go through: draft -> reviewed -> approved.

The orchestrator determines the review tier from the plan (or from config):
- `low`: auto-approve, skip review
- `high`: spawn reviewer, then decider

Approval is marked by the presence of `Status: approved` in `output/plan.md` (inline marker). This is the only place the orchestrator reads markdown content, and it's a simple string match, not parsing.

Alternative (cleaner, consider adopting): a separate `for-orchestrator/plan-approved` marker file written by the orchestrator after the decider approves or after auto-approval. This eliminates the one case where the orchestrator reads inside a markdown file.

---

## 12. Child Creation Contract

When the orchestrator creates a child:

1. Parse the next unstarted step from `output/plan.md`.
2. Create the child directory with all five subdirectories.
3. Write `input/parent-instructions.md` with the step's goal.
4. Write `for-orchestrator/status` with `pending`.
5. Write `for-orchestrator/mode` with the computed role (`planner` or `worker`, based on complexity * importance vs threshold, capped by max depth).
6. Optionally write `input/context.md` if prior-step context exists.
7. Call `validate_node_creation()`.
8. Log the child creation event.

Children are created one at a time (sequential execution). The orchestrator creates the next child only after the current one reaches a terminal status and the evaluator says `continue`.

---

## 13. Invariants

These must hold at all times. Tests should verify them.

### Status invariants

- Every node has a `for-orchestrator/status` file.
- The status file contains exactly one of the five legal values.
- Terminal nodes (done, failed, timed_out) never transition again.
- A node with status=done always has `for-orchestrator/outcome`.
- A node with status=failed or timed_out always has `for-orchestrator/failure-reason`.
- A node with outcome=completed always has `output/final-output.md`.
- A node with outcome=escalated always has `output/escalation.md`.

### Run invariants

- At most one active run per node (checked by PID before spawn).
- Run directories are monotonically numbered and never reused.
- Every completed run has a `meta.json` with all required fields.
- `cost.json` is updated after every run exit.

### Tree invariants

- Every node has exactly one of `input/goal.md` or `input/parent-instructions.md`.
- Children are only created by the orchestrator, never by agents.
- Child directories follow the `step-NN-<slug>` naming convention.
- A node's `children_usd` in cost.json equals the sum of its children's `total_usd`.

### File boundary invariants

- Agents can only write inside their own node directory.
- Agents can read anything inside the repo.
- Agents never write to `for-orchestrator/status`, `for-orchestrator/phase`, `for-orchestrator/outcome`, or `for-orchestrator/failure-reason`.
- Agents may write to `for-orchestrator/eval-decision` (evaluator and synthesizer roles only).
- Agents may write to `for-orchestrator/waiting` (via background job tool only).

### Orchestrator log invariant

- Every status transition is logged to `orchestrator.jsonl` before the transition is considered complete.

---

## 14. The Orchestrator Event Log

### orchestrator.jsonl entry format

```json
{
  "ts": "2026-04-01T14:30:00Z",
  "event": "status_change",
  "node": "tree/root/children/step-01-analyze",
  "from_status": "running",
  "to_status": "done",
  "phase": "synthesizing",
  "outcome": "completed",
  "reason": null,
  "run_id": "run-005",
  "cost_total_usd": 2.31,
  "details": ""
}
```

### Event types

| Event | When |
|---|---|
| `status_change` | Any status transition |
| `phase_change` | Any phase change |
| `spawn` | Agent run spawned |
| `child_created` | New child node created |
| `run_completed` | Agent run exited |
| `run_failed_validation` | Run exited but didn't satisfy artifact contract |
| `cost_cap_exceeded` | Node killed for cost |
| `zombie_warning` | First strike for inactivity |
| `zombie_killed` | Run killed for inactivity |
| `eval_decision_consumed` | Eval decision read and deleted |
| `mission_complete` | Root node reached done/completed |
| `mission_failed` | Root node reached failed or done/escalated |

---

## 15. What This Spec Does Not Cover

These are explicitly out of scope for the node contract:

- **Workflow recipes**: how roles are sequenced within a node (retrieve -> plan -> review -> decide -> execute -> evaluate -> synthesize) is orchestrator logic, not a node contract. The node contract only says what files each role must produce and what statuses/outcomes are legal.
- **Prompt assembly**: how the orchestrator builds `instructions-<role>.md` from node context is an orchestrator implementation detail.
- **Model routing**: which model runs which role is config, not contract.
- **The tick() function**: the orchestrator's decision logic is covered in the architecture doc, not here. This spec defines what the decisions operate on.
- **A/B test mechanics**: the `variant` field in run records is a placeholder. The A/B framework is a future layer.
- **Cross-node communication**: nodes communicate through the tree (parent reads child outputs). No peer messaging.
- **Parallel child execution**: this spec assumes sequential. Parallel is a future extension.
