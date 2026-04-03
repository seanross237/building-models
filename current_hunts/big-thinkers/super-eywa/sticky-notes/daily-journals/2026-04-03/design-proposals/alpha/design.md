# Eywa Alpha Design

## The Core Idea

Every node is a cell. Same DNA, different gene expression. The variables are the genes that get switched on.

A cell doesn't know it's part of a liver or a brain. It just reads its instructions and its active genes, then does its work. Eywa nodes work the same way.

## The Three Systems

```
Eywa    — the organism (nodes that execute)
Bonsai  — the gardener (learns which variables work, prunes what doesn't)
Potter  — the glassblower (reshapes the code without changing behavior)
```

Potter is deferred. This design covers Eywa and the Bonsai data layer.

## Node Anatomy

A node is a directory on disk. Every node has exactly the same structure:

```
node-{id}/
  input.json       # what this node was asked to do
  variables.json   # the knobs for this run (merged: tree defaults + node overrides)
  output.json      # what this node produced
  metrics.json     # score, tokens, cost, wall_time, children_count
  children/        # child node directories (if any)
```

### input.json

```json
{
  "task": "the thing to do, in plain text",
  "context": "any supplementary info the parent decided to provide",
  "parent_id": "node-abc123 or null for root"
}
```

### variables.json

This is the heart. These are the knobs the system optimizes.

```json
{
  "_meta": {
    "source": "tree_defaults + node_overrides",
    "tree_run_id": "run-2026-04-03-001"
  },

  "model": "anthropic/claude-sonnet-4-20250514",
  "temperature": 0.3,

  "planning_mode": "direct | plan_then_execute | delegate",
  "planning_depth_budget": 3,
  "max_children": 5,

  "system_prompt_key": "worker-v2",
  "role_hint": "analyst | coder | researcher | generalist",

  "context_strategy": "minimal | parent_summary | full_chain",
  "context_token_budget": 4000,

  "tool_policy": "none | read_only | read_write | full",
  "tools_allowed": ["bash", "read", "grep", "write"],

  "retry_policy": "none | once | twice",
  "confidence_threshold": 0.8,

  "synthesis_strategy": "concatenate | summarize | best_of",
  "output_format": "prose | structured | code"
}
```

The variable schema is intentionally flat — no nesting, no indirection. Every variable name is a self-describing knob. New variables can be added without changing the node contract.

### How Variables Flow

```
Tree-level defaults (set at run start)
       |
       v
  Node-level overrides (set by parent or by Bonsai recommendation)
       |
       v
  variables.json = merge(tree_defaults, node_overrides)
```

Tree defaults are the "average best" settings. Node overrides are where task-specific optimization happens. Early on, most nodes just use tree defaults. As Bonsai learns, it starts recommending node-level overrides based on task similarity.

## Node Lifecycle

Five states, linear:

```
PENDING  -->  ACTIVE  -->  WORKING  -->  DONE
                              |
                              v
                           FAILED
```

1. **PENDING** — node directory created, input.json written, variables.json written
2. **ACTIVE** — orchestrator picks up the node, prepares the prompt
3. **WORKING** — model is called, node may spawn children (which start at PENDING)
4. **DONE** — output.json and metrics.json written
5. **FAILED** — something went wrong, error captured in output.json

The orchestrator is a simple loop: find the deepest PENDING node, activate it, let it work, collect its output, bubble up.

## The Prompt Assembly

When a node goes ACTIVE, the orchestrator assembles the prompt from:

1. The system prompt template (selected by `system_prompt_key`)
2. The task from `input.json`
3. Context (determined by `context_strategy`)
4. Tool availability (determined by `tool_policy`)
5. Output format guidance (determined by `output_format`)

The system prompt templates live in a known directory. The variables select and configure, but never generate — the bones are fixed, the variables just pick which bones to activate.

## Recording: The Data Bonsai Needs

Every run produces a clean dataset row. The schema:

```
run_id | node_id | task_text | task_tags | variables_hash | variables_json |
score | tokens_used | cost | wall_time_s | children_count | model | timestamp
```

### task_tags

Each task gets tagged along 5 axes (these are the "meta columns" Sean described):

| Axis | Example Values |
|------|---------------|
| **domain** | math, code, writing, analysis, research |
| **complexity** | atomic, moderate, compound |
| **verification** | exact_match, numeric, rubric, agent_rated |
| **reasoning_type** | deductive, inductive, creative, procedural |
| **depth** | shallow (1 step), medium (2-5 steps), deep (5+ steps) |

These tags enable similarity lookup: "find me past runs on moderate-complexity math tasks with exact_match verification."

## Benchmark Suite ("The Proving Ground")

A directory of tasks where we know the right answer:

```
benchmarks/
  index.json          # manifest of all tasks
  tasks/
    math-001.json     # { task, expected, scoring, tags }
    code-002.json
    ...
```

Each benchmark task:

```json
{
  "id": "math-001",
  "task": "What is the sum of the first 100 positive integers?",
  "expected": "5050",
  "scoring": "exact_match",
  "tags": {
    "domain": "math",
    "complexity": "atomic",
    "verification": "exact_match",
    "reasoning_type": "deductive",
    "depth": "shallow"
  }
}
```

Scoring types:
- `exact_match` — string equality
- `numeric_tolerance` — within epsilon
- `rubric` — checklist of required elements
- `agent_rated` — an LLM judge scores similarity (0-1)

The benchmark suite grows over time. Any verifiable task encountered in the wild can be promoted here.

## The Optimization Ladder

### Level 1: Best Average Variables

Run the full benchmark suite with different variable combinations. Track scores. Pick the variable set with the highest average score. This becomes the tree-level default.

### Level 2: Best by Category (Heuristics)

Group benchmark results by task tags. Find that math tasks do better with `temperature: 0.1` and `planning_mode: direct`, while research tasks prefer `temperature: 0.5` and `planning_mode: plan_then_execute`. Build a simple lookup table:

```json
{
  "math + atomic": { "temperature": 0.1, "planning_mode": "direct" },
  "research + compound": { "temperature": 0.5, "planning_mode": "plan_then_execute" }
}
```

When a new task comes in, match its tags to the lookup table. Override the tree defaults with the category-best variables.

### Level 3: ML Model

Given a task (embedded), predict optimal variables. Training data: the scored runs database. Input: task embedding. Output: variable recommendations with confidence scores.

This is later. The data collection and clean recording is what makes it possible.

## The Runs Database

```
data/
  runs.jsonl          # append-only log of every node execution
  benchmarks.jsonl    # scored benchmark runs (subset of runs)
  variable_configs/   # named variable sets that performed well
  leaderboard.json    # best variable set per task category
```

Each line in `runs.jsonl` is a complete record: task, tags, variables, score, metrics. This is the raw material for everything Bonsai does.

## What Makes This Design Work

1. **One contract.** Every node is identical in shape. No special cases.
2. **Variables are the only moving part.** Same code, different knobs. Clean separation.
3. **Flat variable schema.** Easy to record, easy to compare, easy to optimize. No hidden state.
4. **Recording is automatic.** Every node writes metrics.json. The data pipeline is just collecting what already exists.
5. **The optimization ladder is incremental.** Start with averages, graduate to heuristics, graduate to ML. Each level uses the same data.
6. **Benchmarks are additive.** New tasks slot in without changing anything. The suite only grows.
7. **Node independence.** Each node can be understood, scored, and optimized without knowing the rest of the tree. This is Sean's dream: "the rest of the tree is almost not important in that moment."

## What This Doesn't Cover Yet

- Potter (code optimization system) — deferred
- Embedding pipeline for task similarity — Level 3
- Automatic blindspot detection — future Bonsai feature
- Promotion of wild tasks to benchmarks — manual for now
