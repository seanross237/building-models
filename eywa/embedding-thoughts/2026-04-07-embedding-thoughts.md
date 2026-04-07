# Embedding Thoughts — 2026-04-07

Notes on how Super-Eywa could categorize tasks so that similar future tasks can benefit from past learnings. The goal of categorization here is compression: squeeze the essence of a task into something that lets us match it to prior runs and borrow what worked.

## The core framing

A good categorization is one that **reduces uncertainty about which variables will win**. That gives us a verifiable test: if knowing a task's category lets us pick better variables than random, the category is pulling weight.

## Strategy spectrum

### Simple starting points
- **Handcrafted axis set** — domain, output type, reasoning depth, verifiability, ambiguity, tool-need, open/closed-form. LLM fills them in.
- **Free-form LLM tags** — then cluster tags after N runs to find a de facto taxonomy.
- **Pure embedding retrieval** — skip categories entirely, store tasks as vectors, use nearest-neighbor.
- **Structured task signature** — fixed JSON schema the model fills (more compressible than tags, more expressive than fixed labels).

### Thorough, verifiable
The key test: a categorization is good iff knowing the category reduces uncertainty about which variables win.
- Build a scoring harness with held-out tasks that have known best variable sets from the grading bank
- Metric: **category-conditional regret** — pick the variable set that won on same-category historical tasks, measure gap vs oracle-best
- Lower regret = better taxonomy. A/B different taxonomies on the same data.
- Related metrics: mutual information between category and best-variable; variance of outcome within a category (want low)
- Ablation: drop one axis at a time, see which actually move the metric — kills dead-weight dimensions

## Recomputability — the architectural bet

A core requirement: categorizations and scores must be **relabelable later**, and all efficacy scores recomputable.

**Principle — raw facts + derived views**
- Runs are immutable raw truth; taxonomies and scores are derived views over them
- Scores are a pure function: `score(taxonomy_version, runs) → table`
- Swap the taxonomy, re-run the function, get new scores — runs never change

**What makes this work**
- Each run record must store enough raw material that any future axis can still be computed from it: task prompt, variables used, node I/O, tool traces, final grade
- Treat a taxonomy as a versioned artifact (`taxonomy_v3.json` or a small function), content-hashed so cached scores know when to invalidate
- Thin `apply_taxonomy(run) → category_vector` step; scoring is a group-by on that

**Folder shape that supports it**
- `run-history/` — append-only, immutable
- `taxonomies/` — versioned categorization configs
- `derived-views/scores/<taxonomy_hash>/...` — recomputable, deletable anytime

**Nice side effects**
- A/B two taxonomies on the exact same run set
- Bonsai can propose a new taxonomy, score it retroactively, and compare — no new runs needed
- Plays well with Potter later: dry-run equivalence already assumes recomputation is safe

**Risk** — under-capturing the raw run. Worth a one-time pass on "what would I need to compute any reasonable future axis?" before the log format sets.

## Task embeddings

An embedding is a dense vector (say 1536 floats) that encodes "what this task is about" in a way where similar tasks end up near each other.

**Why bother alongside handcrafted axes**
- Categories compress hard; embeddings compress soft — they catch similarity your axes didn't think to name
- Nearest-neighbor retrieval just works: pull the k closest past tasks, look at which variables won for them
- Zero taxonomy design required to start getting value
- Mix-and-match: filter by category first, then rank by embedding distance inside the category

### Options for how to create them

**Option 1 — Off-the-shelf API, raw text**
- Send task prompt to OpenAI `text-embedding-3-small`, Voyage, Cohere. L2-normalize. Store `{model, dim, vector}`. Cosine similarity for retrieval.

**Option 2 — Local model, same shape**
- Small local encoder (`bge-small`, `e5-base`, `nomic-embed-text`). Free, offline, reproducible.

**Option 3 — Preprocess before embedding** ← chosen direction
- Instead of raw task text, embed a normalized signature: LLM first produces a short structured summary (domain, goal, output shape, constraints), then embed that string
- Cleaner because raw prompts are noisy and stylistically varied across sources
- Nearest-neighbors match on task essence, not wording

**Option 4 — Multi-field embedding**
- Embed task text, rubric, and expected output shape separately; concatenate or weighted-sum
- Lets you weight fields later ("match me on rubric shape more than wording")

**Option 5 — Learned contrastive embedding (later)**
- Once enough run outcomes exist, fine-tune a small encoder so tasks that shared a winning variable set pull together
- Needs real data volume — not worth it day one

**Practical bits regardless of option**
- Store `model_id` + `model_version` + `vector` + `created_at` per run
- Keep raw task text so you can re-embed anytime a better model drops
- Index: brute-force cosine is fine up to ~100k; FAISS/hnswlib later

## Chosen direction — preprocessing LLM + hybrid retrieval

### Single LLM call, two outputs

The preprocessor returns one JSON object that contains both axis labels and the embedding input text:

```
{
  "axes": {
    "output_type": "...",
    "verifiability": "...",
    "domain": "...",
    "reasoning_depth": "...",
    ...
  },
  "essence": "A short normalized summary of the task's goal,
              constraints, and expected output shape."
}
```

- `axes` feeds the category filter
- `essence` is the string sent to the embedding model
- One model call, consistent view of the task, no drift between "what the categorizer thought" and "what got embedded"

### The LLM is doing two jobs
- **Categorizer** — produces structured axis labels for filtering
- **Compressor / denoiser** — rewrites the task into canonical form: goal, constraints, output shape, stripped of wording and style. The embedder sees clean signal instead of stylistic noise.

Mental model:
- **Axes** = discrete, legible, good for filtering and human inspection
- **Essence** = continuous, opaque, good for soft similarity
- **Raw task** = source of truth, preserved so both can be regenerated later

Rule of thumb: if two tasks would be solved the same way, their essences should read almost identically. That's the target the preprocessor prompt should optimize for.

### Full pipeline per task
1. Raw task lands in `run-history` (kept forever, untouched)
2. Preprocessor LLM → `signature.json` (axes + essence)
3. Embedder → `vector` from `signature.essence`
4. Store `{signature, vector, preprocessor_version, embed_model_version}` as a derived artifact

### At retrieval time
- Run the new task through the exact same pipeline
- Hard-filter past runs on 1–2 trusted axes
- Rank the survivors by cosine distance on essence vectors
- Return top-k + their winning variable sets

### Why this shape is nice
- Everything derived from raw; raw task is the only source of truth
- Bump preprocessor prompt → re-run on history → new axes and new essence, atomically in sync
- Bump embedding model → re-embed from stored essence strings (no preprocessor re-call needed)
- Both versions content-hashed so cached scores invalidate cleanly
- Axes stay legible, essence stays soft — both available

### One thing to watch
- Essence strings must be task-focused, not stylistic — otherwise you're just re-embedding surface wording
- Guardrail: preprocessor prompt explicitly tells the model to strip phrasing, keep structure/goal/constraints
- Later, A/B "essence embedding" vs "raw-text embedding" with the regret harness to confirm preprocessing is earning its keep

## Hybrid retrieval — filter then rank

### What it is — two-stage retrieval
1. Use handcrafted categories as a filter; drop past tasks that don't share key axes with the new task
2. Among what's left, rank by embedding distance; take top-k
3. Those k become your "similar past tasks" for borrowing winning variables

### Why it helps
- Embeddings are fuzzy — can pull surface-similar tasks that are categorically wrong (e.g., physics word problem next to a trivia question sharing vocabulary)
- Categories act as guardrails on high-confidence axes; embedding handles soft similarity inside the bucket
- Legibility bonus: explain a retrieval as "same output type + nearest in meaning"

### Why you might not
- Small categories → hard-filtering leaves nothing to rank
- Wrong labels → filter out genuinely useful neighbors
- Over-filtering collapses search space, hides cross-domain transfer

### Variants
- **Hard filter** — must match on axis X (e.g., output type, verifiability)
- **Soft filter** — bonus to same-category, still allow cross-category with a penalty
- **Per-axis policy** — some axes hard (output type), others soft (difficulty, domain)

### Recommendation
- Do it, but keep minimal at first
- Hard-filter on only 1–2 axes where crossing is clearly wrong (probably `output_type` and `verifiability`)
- Everything else stays soft or unfiltered
- A/B with leave-one-out regret: pure-embedding vs filtered-then-embedded vs category-only — let the data pick
- Short version: hybrid is the right shape, but trust embeddings more than labels until labels have earned it

## Validation

Splits by what's available. Cheap tests run day one; gold-standard test needs run outcomes.

### Cheap sanity checks (no run data needed)
- **Triplet probes** — hand-write ~20 sets of "A and B should be close, C should be far." Embedding fails any = red flag.
- **Paraphrase stability** — embed the same task with rewritten wording; distance should be small. Tests whether preprocessor is stripping style.
- **Cluster eyeball** — k-means or HDBSCAN on embeddings, read ~5 tasks per cluster, ask "does this feel coherent?"
- **Precision@k on known axes** — for each task, check whether its k nearest neighbors share its `output_type`/`verifiability`. Doesn't need outcomes, just labels.

### Gold-standard test (uses run outcomes)
- **Leave-one-out regret** — the one that matters
  1. For each past run where best variable set is known, hide it
  2. Retrieve its k nearest neighbors by embedding
  3. Pick the variable set that won most often among those neighbors
  4. Measure gap between that pick and true best
  5. Average gap across all runs = embedding's **regret**
- Lower regret = embedding actually predicts what we care about
- Same harness works for: raw-text vs essence, model A vs model B, filter+embed vs embed alone

### Variance-based (weaker but easier)
- For each task, pull its k neighbors and compute variance of which variable set won among them
- Low variance = embedding found a coherent cluster for variable selection
- Useful before enough runs exist for full regret numbers

### Staging
1. Day one: triplet probes + paraphrase stability + cluster eyeball
2. After ~50 graded runs: precision@k on known axes
3. After ~200 graded runs: leave-one-out regret becomes primary metric
4. Any new embedding or preprocessor must beat current one on regret before replacing it

### Bake in now
- Store `preprocessor_version` and `embed_model_version` on every vector
- Old regret scores stay interpretable across swaps — "under v2 preprocessor + v1 embedder, regret was X"

## Open questions / next steps

- Draft the minimal raw-run schema that keeps future taxonomies open (what must be captured at write time so no future axis is lost)
- Draft the preprocessor schema + prompt as a concrete starting point
- Decide initial axis set (probably 6–8 handcrafted)
- Pick initial embedding model (Option 1 API vs Option 2 local)
- Decide which 1–2 axes get hard-filtered in retrieval
- Where in the folder tree does this live? Likely straddles `data-system/` (storage, scoring) and Bonsai territory (not yet a folder)
