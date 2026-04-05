# Eywa Beta Design: The Recipe Model

## One-Sentence Summary

Every node is a blank cell that runs a **recipe** — a single, versioned configuration object that contains all the variables — and the system learns which recipes work best for which tasks.

## The Core Insight

Sean's vision says: nodes are identical, variables are the knobs, optimize the knobs. The typical approach is to have 15-20 independent variables (model, temperature, system prompt style, planning depth, etc.) and try to optimize them individually or in combinations.

This design takes a different angle: **don't optimize knobs — optimize recipes.**

A recipe is the atomic unit of variation. It's a named, versioned JSON object that bundles all the variables together. Instead of asking "what temperature should this node use?", you ask "which recipe should this node use?" This is simpler because:

1. **One decision, not twenty.** The optimization layer picks one thing: a recipe name. Not a matrix of independent variables.
2. **Recipes are human-readable.** You can name them, describe them, compare them side-by-side.
3. **Recipes compose naturally.** A tree-level recipe sets defaults; a node can override with its own recipe. Two layers, not twenty.
4. **Recipes evolve.** Version them. Fork them. The system can mutate a recipe to create a variant and test it.

## The Three Pieces

### 1. Eywa (The Runner)

Eywa takes a task and runs it. The moving parts:

#### What Is A Node?

A node is a directory on disk:

```
node-{id}/
  input.json      # task + instructions from parent
  recipe.json     # the recipe this node used (frozen copy)
  output.json     # what this node produced
  children/       # child node directories (if any)
  trace.json      # timing, token counts, model calls — raw telemetry
```

That's it. Five concerns, five files. No `system/` subfolder, no status machine. Status is implicit: if `output.json` exists, the node is done.

#### What Is A Recipe?

A recipe is a JSON file with a flat-ish schema:

```json
{
  "name": "methodical-v3",
  "version": 3,
  "model": "anthropic/claude-sonnet-4",
  "approach": "plan-then-execute",
  "planning_depth": "shallow",
  "system_tone": "concise-analytical",
  "decomposition": "allowed",
  "max_children": 4,
  "retry_on_fail": true,
  "knowledge_retrieval": "on-demand"
}
```

The recipe schema is fixed and small — maybe 8-12 fields to start. Each field is a high-level lever, not a micro-knob. For example, `system_tone` is a named style ("concise-analytical", "exploratory-verbose", "socratic"), not a raw system prompt. The actual prompt text is derived from the tone name by a fixed mapping function. This means:

- Variables are enumerable and categorical, which makes optimization tractable.
- You can describe any recipe in one line: "methodical-v3: Sonnet, plan-then-execute, shallow planning, concise."
- The recipe schema can grow over time, but starts small.

#### How Does A Node Run?

```
receive task + recipe
  |
  [expand recipe] — look up prompt templates, tool policies, etc. from recipe values
  |
  [call model] — single model call with expanded prompt
  |
  model says one of:
    "answer: ..."    → write output.json, done
    "plan: [...]"    → create child nodes, each with task + recipe, wait for results, synthesize
    "need_info: ..." → use retrieval tool, then re-prompt
  |
  write trace.json with telemetry
```

The node lifecycle has exactly three outcomes: answer directly, decompose into children, or retrieve information and retry. No status machine. The orchestrator simply walks the tree depth-first.

#### How Do Variables Flow?

Two layers only:

1. **Tree recipe** — set at mission start. Every node inherits this by default.
2. **Node recipe override** — optionally, a parent can assign a different recipe to a specific child (e.g., "use the deep-analysis recipe for the hardest subtask").

The override is an explicit parent decision, not an automatic system. This keeps it simple and inspectable.

### 2. Bonsai (The Learner)

Bonsai's job: given past run data, pick better recipes for future runs.

#### The Scoreboard

Every completed run produces a row:

```json
{
  "run_id": "run-047",
  "task_fingerprint": "math-combinatorics-medium",
  "task_tags": ["math", "combinatorics", "medium"],
  "task_text_hash": "a3f2...",
  "recipe_name": "methodical-v3",
  "recipe_hash": "b7e1...",
  "score": 0.85,
  "tokens_used": 12400,
  "wall_time_s": 34,
  "cost_usd": 0.08,
  "node_count": 3,
  "timestamp": "2026-04-03T14:22:00Z"
}
```

This is a flat CSV/JSONL file. One row per run. No database needed initially.

#### The Optimization Ladder

Exactly as Sean described, but operating on whole recipes:

**Level 1 — Best Average Recipe.**
Run the benchmark suite with each recipe. Pick the one with the highest average score. Use it as default. This is a bash script.

**Level 2 — Best Recipe Per Category.**
Simple heuristic lookup: "for math tasks, use methodical-v3; for creative tasks, use exploratory-v2." A JSON lookup table mapping task tags to recipe names. Still trivially simple.

**Level 3 — Recipe Selector Model.**
An ML model (or even just an LLM call) that takes task features and outputs a recipe name. Trained on the scoreboard data. This comes later.

#### Recipe Evolution

Bonsai can also create new recipes by mutation:

1. Take the best-performing recipe.
2. Change 1-2 fields (e.g., swap model, change planning depth).
3. Name it as a new version.
4. Run it through the benchmark suite.
5. If it scores better, it enters the recipe library.

This is literally Sean's "mutation rate" insight from the Rhyme-Eval reflections, applied to system configuration.

### 3. The Benchmark Suite (The Gym)

A directory of tasks with known-good answers:

```
benchmarks/
  tasks/
    math-001.json    # { "task": "...", "answer": "42", "tags": ["math", "arithmetic", "easy"], "scorer": "exact" }
    code-012.json    # { "task": "...", "answer": "...", "tags": ["code", "python", "medium"], "scorer": "functional" }
    ...
  scorers/
    exact.py         # did the output match exactly?
    functional.py    # did the code pass the test cases?
    similarity.py    # cosine similarity to reference answer
  results/
    scoreboard.jsonl # the flat results file
```

Scorers are pluggable. Start with `exact` and `functional`. Add `similarity` (agent-judged) later.

Running the suite: `python3 run_benchmark.py --recipe methodical-v3` runs every task with that recipe, appends results to the scoreboard.

### What's Not Here (By Design)

- **No Potter yet.** The code optimizer is explicitly later. The design is simple enough that it doesn't need one yet.
- **No ML model yet.** Start with averages and heuristics. The data format supports ML when the time comes.
- **No embedding pipeline yet.** Task tags + exact text hash are enough for Level 1 and Level 2. Embeddings come with Level 3.
- **No status machine.** Nodes are done or not done. Recovery is "re-run the node." This can get more sophisticated later.
- **No persistent agents.** Every node is a fresh model call. No memory between nodes except what the parent passes as input.

## Why This Might Actually Work

1. **It's small.** The whole system is: a node runner, a recipe expander, a benchmark harness, and a scoreboard. Maybe 500-800 lines of Python.
2. **It records cleanly.** Every run is one scoreboard row. Every node is one directory. No hidden state.
3. **It optimizes the right thing.** Instead of searching a 20-dimensional variable space, you're comparing named recipes. The search space is manageable.
4. **It's human-debuggable.** You can look at any node's directory, see what recipe it used, see what it produced. No log archaeology.
5. **It builds toward ML.** The scoreboard format is already a training dataset. When you're ready, the features (task tags) and label (best recipe) are right there.

## The Metaphor

Eywa is a **kitchen**. Each node is a **cook station** — same equipment, same layout. The recipe tells the cook what to make and how. Bonsai is the **head chef** who, after tasting many dishes, writes a cheat sheet: "For seafood, use Recipe 7. For desserts, use Recipe 12." The benchmark suite is the **tasting panel** that scores every dish.

The kitchen never changes. The recipes evolve.
