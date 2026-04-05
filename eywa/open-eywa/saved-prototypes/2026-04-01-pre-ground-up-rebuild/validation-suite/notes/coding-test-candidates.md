# Eywa Coding Test Candidates

Coding-focused validation candidates for Eywa / Open-Eywa.

Priority order:

1. very hard tasks with a score gradient
2. a few very hard tasks with clean right-or-wrong outcomes

The goal is not to copy a public leaderboard wholesale. The goal is to pick a small set of hard tasks that give strong signal about planning quality, tool use, persistence, and debugging ability.

## Best Score-Gradient Sources

### 1. ALE-Bench

- Type: AtCoder Heuristic Contest tasks
- Signal: numeric score, rank, and performance, with partial credit
- Why it is strong:
  - genuinely hard
  - not just pass/fail
  - good for testing iterative improvement and search
  - good fit for multi-step agent behavior
- Why it is weaker:
  - more optimization-heavy than ordinary software engineering
  - less cleanly comparable to function-writing tasks
- Status: best current source for "make the score go up" coding tasks
- Source:
  - https://github.com/SakanaAI/ALE-Bench
  - https://sakanaai.github.io/ALE-Bench-Leaderboard/
  - https://openreview.net/forum?id=JCjGvbsOmQ

### 2. EvalPerf

- Type: code-generation tasks where efficiency matters after correctness
- Signal: performance score on correct solutions
- Why it is strong:
  - still has objective execution-based correctness
  - adds a real gradient beyond simple pass/fail
  - easier to integrate than full repo-patching benchmarks
- Why it is weaker:
  - still narrower than open-ended repo work
  - less like real software maintenance than SWE-bench-style tasks
- Status: best current source for "correct, then optimize" tasks
- Source:
  - https://evalplus.github.io/evalperf.html
  - https://github.com/evalplus/evalplus

## Best Binary Anchors

### 3. SWE-bench Pro

- Type: long-horizon repo bug-fixing tasks
- Signal: did the generated patch resolve the issue under automated evaluation
- Why it is strong:
  - very hard
  - high-value software engineering signal
  - directly tests repository navigation and patch quality
- Why it is weaker:
  - expensive to run
  - mostly gives set-level solve rate, not per-task partial credit
- Note:
  - prefer this over SWE-bench Verified for fresh serious evaluation
- Source:
  - https://labs.scale.com/papers/swe_bench_pro
  - https://www.swebench.com/SWE-bench/faq/
  - https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/

### 4. LiveCodeBench

- Type: hard contest-style coding tasks with hidden tests
- Signal: pass@1, pass@5, and solve rate on held-out / time-bounded tasks
- Why it is strong:
  - hard
  - contamination-aware
  - useful as a clean algorithmic anchor
- Why it is weaker:
  - still mostly pass/fail
  - less like repo maintenance than SWE-bench Pro
- Source:
  - https://livecodebench.github.io/
  - https://github.com/LiveCodeBench/LiveCodeBench

### 5. USACO Benchmark

- Type: olympiad-style programming problems with hidden tests
- Signal: accepted / not accepted, plus pass@1 in the benchmark paper
- Why it is strong:
  - very hard reasoning tasks
  - strong hidden-test discipline
  - good anchor for algorithmic depth
- Why it is weaker:
  - smaller and more specialized
  - mostly binary
- Source:
  - https://github.com/princeton-nlp/USACO
  - https://arxiv.org/abs/2404.10952

## Sources To Mine But Not Use As The Main Set

### APPS

- Strong large pool of coding problems
- Mostly older and more contamination-prone
- Better as a backup pool than as the core hard set
- Source:
  - https://github.com/hendrycks/apps

### BigCodeBench

- Strong harder-than-HumanEval function tasks
- Useful if we want more code-synthesis coverage
- Still less important than ALE-Bench, EvalPerf, or SWE-bench Pro for the current goal
- Source:
  - https://github.com/bigcode-project/bigcodebench
  - https://bigcode-bench.github.io/

### CodeContests

- Good raw source of hard contest tasks
- Better as a mining source than as the main benchmark harness
- Source:
  - https://github.com/google-deepmind/code_contests

## Recommended Initial Mix

If we want a first serious coding set, use:

- 4 to 6 ALE-Bench tasks
- 4 to 6 EvalPerf tasks
- 2 to 3 SWE-bench Pro tasks
- 2 to 3 LiveCodeBench or USACO tasks

This gives:

- real score gradients
- a few hard binary anchors
- both optimization-style and software-engineering-style pressure

## What To Avoid As The Core Set

- HumanEval / MBPP as the main coding benchmark
- tiny toy scripting tasks
- tasks without hidden tests or strong evaluation
- tasks whose only signal is "code runs once on one public example"

These can still be useful as smoke tests, but they are too weak for the main hard set.

## Next Step

Pick concrete tasks from the sources above and write them up in the same style as `test-case-candidates.md`:

- question / task
- expected evaluation method
- scoring rule
- why the task discriminates
- source

---

## Concrete Hard Picks

These are the first concrete coding tasks I would actually try.

### Score-Gradient Tasks

#### S1. AHC001 / AtCoder Ad
- **Question / Task:** Place many non-overlapping axis-aligned ad rectangles in a `10000 x 10000` square so each advertiser gets a rectangle containing its requested point and with area close to its requested target area.
- **Scoring:** Continuous score from advertiser satisfaction; higher is better.
- **Why It Discriminates:** This is a difficult geometric packing and local-search problem. It rewards iterative repair, spatial reasoning, and score-climbing instead of one-shot code generation.
- **Why It Fits:** Very hard, cleanly scored, and easy to compare across runs.
- **Source:**
  - https://atcoder.jp/contests/ahc001/tasks/ahc001_a

#### S2. AHC012 / AtCoder 10th Anniversary
- **Question / Task:** Cut a circular cake with at most `K = 100` straight lines so the strawberry-count distribution of pieces matches the attendee-demand distribution as well as possible.
- **Scoring:** `round(10^6 * matched_pieces / total_requested_pieces)` on each case; higher is better.
- **Why It Discriminates:** Hard constrained optimization with global interactions between cuts. Good for planning, search, and refinement loops.
- **Why It Fits:** Strong score gradient and highly nontrivial solution space.
- **Source:**
  - https://atcoder.jp/contests/ahc012/tasks/ahc012_a

#### S3. AHC024 / Topological Map
- **Question / Task:** Compress a colored city map onto a `50 x 50` grid while preserving all color-adjacency relations and connectivity constraints, and maximize empty space.
- **Scoring:** `E + 1`, where `E` is the number of empty cells; higher is better.
- **Why It Discriminates:** This is graph-preserving compression under topology constraints. It is much more structural than standard contest tasks.
- **Why It Fits:** Hard and unusual. Strong signal on whether the agent can reason about invariants while optimizing globally.
- **Source:**
  - https://atcoder.jp/contests/ahc024/tasks/ahc024_a

#### S4. AHC030 / Polyomino Mining
- **Question / Task:** Given known polyomino oil-field shapes but unknown placements, recover all oil-containing cells with as little probing cost as possible using drilling, noisy aggregate queries, and final guesses.
- **Scoring:** Lower probing cost is better; contest score is derived from absolute and relative cost.
- **Why It Discriminates:** This is active information gathering under uncertainty. It tests experiment design, probabilistic reasoning, and adaptive search.
- **Why It Fits:** Probably the most agent-like AHC task in this list.
- **Source:**
  - https://atcoder.jp/contests/ahc030/tasks/ahc030_a

#### S5. AHC032 / Mod Stamp
- **Question / Task:** Choose up to `K = 81` placements of `3 x 3` stamps on a `9 x 9` board to maximize the sum of board entries modulo `998244353`.
- **Scoring:** Sum of final cell values modulo `998244353`; higher is better.
- **Why It Discriminates:** Very combinatorial and not easy to solve greedily. Good for search, beam methods, refinement, and modular arithmetic awareness.
- **Why It Fits:** Harder than it looks and gives a clean numeric objective.
- **Source:**
  - https://atcoder.jp/contests/ahc032/tasks/ahc032_a?lang=en

#### S6. AHC037 / Soda
- **Question / Task:** Starting from beverage `(0, 0)`, build a target set of `1000` beverages with desired sweetness and carbonation pairs using a sequence of monotone derivation operations with minimum total cost.
- **Scoring:** `round(10^6 * NL / (1 + C))`, where `C` is total cost and `L` is the max coordinate scale; higher is better.
- **Why It Discriminates:** This is effectively a hard constructive optimization / DAG design problem. It rewards reuse, abstraction, and discovering shared intermediate states.
- **Why It Fits:** Strong score gradient and good signal on whether the agent can invent efficient latent structure.
- **Source:**
  - https://atcoder.jp/contests/ahc037/tasks/ahc037_a

### Binary Anchors

#### B1. USACO 2024 US Open Platinum / Identity Theft
- **Question / Task:** Extend cows' bitstring IDs so no cow can be mistaken for another when some reported IDs are truncated.
- **Scoring:** Binary hidden-test acceptance.
- **Why It Discriminates:** Very hard string / trie / combinatorial reasoning task with strict correctness.
- **Why It Fits:** Good "clear right or wrong" anchor to pair with the scored AHC tasks.
- **Source:**
  - https://usaco.org/index.php?cpid=1428&page=viewproblem2

#### B2. USACO 2023 US Open Gold / Tree Merging
- **Question / Task:** Reconstruct a valid sequence of sibling-merge operations that transforms an initial rooted tree into a final rooted tree.
- **Scoring:** Binary hidden-test acceptance.
- **Why It Discriminates:** High-structure constructive task. Good test of whether the agent can produce a valid transformation sequence, not just compute a number.
- **Why It Fits:** Hard and precise.
- **Source:**
  - https://usaco.org/index.php?cpid=1331&page=viewproblem2

#### B3. USACO 2024 February Gold / Bessla Motors
- **Question / Task:** Given a large weighted graph with charging stations, identify all destinations that are reachable from at least `K` distinct charging stations within the specified range constraint.
- **Scoring:** Binary hidden-test acceptance.
- **Why It Discriminates:** Hard graph algorithm problem with large constraints and clear correctness.
- **Why It Fits:** Good binary anchor for large-scale graph reasoning.
- **Source:**
  - https://usaco.org/index.php?cpid=1401&page=viewproblem2

## Recommended First Trial Set

If we want to start testing soon, I would begin with:

- `AHC030 / Polyomino Mining`
- `AHC024 / Topological Map`
- `AHC037 / Soda`
- `AHC032 / Mod Stamp`
- `USACO Identity Theft`
- `USACO Tree Merging`

That gives:

- four genuinely hard scored optimization tasks
- two clean hard binary tasks
- a mix of geometry, topology, active search, construction, and graph/string reasoning

## Notes

- I intentionally prioritized tasks with public official statements and strong evaluation.
- I did not yet pin down specific `SWE-bench Pro` public instances here, because that needs a separate pass to avoid leaking solution patches while still choosing good issue statements.
- I also did not prioritize `EvalPerf` in the first concrete picks because the concrete visible tasks are often smaller and less brutal than the AHC / USACO tasks above.
