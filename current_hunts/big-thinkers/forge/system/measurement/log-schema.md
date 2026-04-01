# Forge — Log Schemas

All logs use JSONL format (one JSON object per line). Log files live at `missions/<mission-id>/logs/`.

---

## restarts.jsonl

Records every stop-hook restart event. Used to track loop health and iteration velocity.

```json
{
  "timestamp": "2026-03-28T14:30:00Z",
  "agent_type": "planner",
  "session": "/Users/.../.claude/projects/.../session-uuid.jsonl",
  "strategy": "strategy-001",
  "iteration_before": 4,
  "iteration_after": 5,
  "trigger": "stop_hook"
}
```

| Field | Type | Description |
|---|---|---|
| `timestamp` | string (ISO 8601 UTC) | When the restart occurred |
| `agent_type` | string | Agent that was restarted: `"planner"`, `"conductor"` |
| `session` | string | Transcript path of the restarted session |
| `strategy` | string | Strategy directory name (e.g., `"strategy-001"`) or `"conductor"` |
| `iteration_before` | number | Iteration count before this restart |
| `iteration_after` | number | Iteration count after this restart |
| `trigger` | string | What caused the restart: `"stop_hook"` |

---

## token-usage.jsonl

Records token consumption per agent turn. Logged by the agent itself (not the hook).

```json
{
  "timestamp": "2026-03-28T14:32:00Z",
  "agent_type": "planner",
  "strategy": "strategy-001",
  "task_id": "task-003",
  "iteration": 5,
  "input_tokens": 45000,
  "output_tokens": 3200,
  "cache_read_tokens": 38000,
  "cache_write_tokens": 7000,
  "model": "claude-opus-4-6-20250327"
}
```

| Field | Type | Description |
|---|---|---|
| `timestamp` | string (ISO 8601 UTC) | When the turn completed |
| `agent_type` | string | Which agent: `"planner"`, `"worker"`, `"conductor"` |
| `strategy` | string | Strategy directory name |
| `task_id` | string or null | Task being worked on (null for planner-level work) |
| `iteration` | number | Current loop iteration |
| `input_tokens` | number | Input tokens consumed |
| `output_tokens` | number | Output tokens generated |
| `cache_read_tokens` | number | Tokens read from prompt cache |
| `cache_write_tokens` | number | Tokens written to prompt cache |
| `model` | string | Model identifier used |

---

## timing.jsonl

Records wall-clock duration of tasks and strategy phases. Used to identify bottlenecks.

```json
{
  "timestamp": "2026-03-28T15:10:00Z",
  "event": "task_complete",
  "agent_type": "worker",
  "strategy": "strategy-001",
  "task_id": "task-003",
  "started_at": "2026-03-28T14:45:00Z",
  "ended_at": "2026-03-28T15:10:00Z",
  "duration_seconds": 1500,
  "outcome": "success"
}
```

| Field | Type | Description |
|---|---|---|
| `timestamp` | string (ISO 8601 UTC) | When this timing entry was recorded |
| `event` | string | What finished: `"task_complete"`, `"strategy_complete"`, `"mission_complete"` |
| `agent_type` | string | Agent that performed the work |
| `strategy` | string | Strategy directory name |
| `task_id` | string or null | Task ID (null for strategy/mission-level events) |
| `started_at` | string (ISO 8601 UTC) | When the work began |
| `ended_at` | string (ISO 8601 UTC) | When the work ended |
| `duration_seconds` | number | Wall-clock duration in seconds |
| `outcome` | string | Result: `"success"`, `"failure"`, `"timeout"`, `"abandoned"` |

---

## efficacy.jsonl

Records task-level outcome quality assessments. Logged by the Planner when it reviews worker results.

```json
{
  "timestamp": "2026-03-28T15:15:00Z",
  "strategy": "strategy-001",
  "task_id": "task-003",
  "approach": "code-analysis",
  "goal_achieved": true,
  "quality_score": 4,
  "useful_findings": 2,
  "wasted_effort": false,
  "notes": "Worker found the root cause and proposed a fix. One tangent on logging was unnecessary."
}
```

| Field | Type | Description |
|---|---|---|
| `timestamp` | string (ISO 8601 UTC) | When the assessment was made |
| `strategy` | string | Strategy directory name |
| `task_id` | string | Task that was assessed |
| `approach` | string | Approach or method the task used |
| `goal_achieved` | boolean | Whether the task accomplished its stated goal |
| `quality_score` | number (1-5) | Overall quality: 1=useless, 2=poor, 3=adequate, 4=good, 5=excellent |
| `useful_findings` | number | Count of findings that advanced the strategy |
| `wasted_effort` | boolean | Whether significant work was spent on unproductive paths |
| `notes` | string or null | Brief Planner commentary on the result |

---

## retrieval-quality.jsonl

Records how well the agent's context reconstruction worked after a restart. Logged by the Planner at the start of each iteration (after executing the startup sequence).

```json
{
  "timestamp": "2026-03-28T14:31:00Z",
  "strategy": "strategy-001",
  "iteration": 5,
  "files_read": ["state.json", "STRATEGY.md", "HISTORY.md", "REASONING.md"],
  "state_reconstruction_success": true,
  "missed_context": null,
  "stale_context_detected": false,
  "worker_result_pending": true,
  "notes": "Picked up where left off. Worker task-003 completed while down — processed its result."
}
```

| Field | Type | Description |
|---|---|---|
| `timestamp` | string (ISO 8601 UTC) | When reconstruction completed |
| `strategy` | string | Strategy directory name |
| `iteration` | number | Current iteration (post-restart) |
| `files_read` | array of strings | Files the agent read during reconstruction |
| `state_reconstruction_success` | boolean | Whether the agent successfully understood its position |
| `missed_context` | string or null | Description of any context that was lost or unclear |
| `stale_context_detected` | boolean | Whether the agent found outdated information in its state files |
| `worker_result_pending` | boolean | Whether a worker result was waiting to be processed |
| `notes` | string or null | Agent's assessment of the reconstruction quality |
