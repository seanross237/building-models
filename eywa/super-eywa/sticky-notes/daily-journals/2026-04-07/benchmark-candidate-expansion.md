# Benchmark Candidate Expansion

Goal:
- expand the question bank with diverse candidates that `google/gemma-4-26b-a4b-it` is likely to miss on a first attempt
- include both binary/exact-answer questions and score-gradient tasks
- prefer candidates with clear validation and known failure pressure

## Best Immediate Adds From Existing Local Libraries

These are already in the repo tree somewhere, but not promoted into the current `data-system/grading` bank.

### 1. Old HLE leftovers not yet in current grading

Best immediate promotions:

- `HLE Q2` Stainless Steel Ferrite Level
  - type: exact numeric
  - likely failure mode: niche materials-science knowledge / diagram recall
  - old baseline signal: Opus answered `50`, correct was `10`
- `HLE Q7` 2D Lattice Adsorption Grand Partition Function
  - type: exact numeric pair
  - likely failure mode: stat-mech setup + computation
  - old baseline signal: Opus answered `Z=8.34, <k>=6.32`, correct was `Z=4.61, <k>=1.66`
- `HLE Q9` CARS Microscopy with Broadband Pump
  - type: multiple choice
  - likely failure mode: niche spectroscopy fact
  - old baseline signal: Opus answered `C`, correct was `B`
- `HLE Q14` ReAl12 Crystal Coordination Polyhedra
  - type: exact structured answer
  - likely failure mode: computational crystallography / tool use
  - old baseline signal: Opus gave a Re-centered answer, key is Al-centered polyhedra

Good secondary promotions:

- `HLE Q5` Perovskite XRD Bragg Reflections
  - Opus got it, but Sonnet missed it
  - likely Gemma failure probability still looks high because it is niche crystallography
- `HLE Q6` 57Fe Mossbauer Largest Hyperfine Field
  - Opus got it, Sonnet missed it
  - likely Gemma miss if it lacks the orbital-angular-momentum fact
- `HLE Q11` Organic A-site Cations for 3D Lead Halide Perovskites
  - classic Aziridinium knowledge trap
- `HLE Q12` Protaetia Cuprea Elytron Optics
  - subtle structure-to-function biology question

Why this bucket is strong:
- clean exact or multiple-choice validation
- already benchmark-shaped
- several are knowledge-first questions where better prompting alone will not rescue weak models

Local source:
- `older_stuff/architecture-exploring-with-benchmarks/benchmark-questions/hle/questions.md`

### 2. Old BBEH reasoning tasks not yet in current grading

Best candidates:

- `hyperbaton`
  - type: multiple-choice / exact
  - likely failure mode: induction of custom adjective-order rules
  - old signal: both Opus and Sonnet failed consistently
- `sarc_triples`
  - type: exact 3-bit classification
  - likely failure mode: sarcasm discrimination
  - old signal: both Opus and Sonnet failed consistently
- `sportqa`
  - type: exact multi-select
  - likely failure mode: over-selection under uncertainty
  - old signal: both Opus and Sonnet failed consistently
- `word_sorting`
  - type: exact first-error localization
  - likely failure mode: finds an error but not the first one
  - old signal: both Opus and Sonnet failed consistently
- `zebra_puzzles`
  - type: exact
  - likely failure mode: long-horizon constraint propagation
  - old signal: variance-heavy even for stronger models

Why this bucket is strong:
- very different from science-domain HLE items
- mostly reasoning-first, not retrieval-first
- good fit for architecture and verification experiments

Local sources:
- `older_stuff/architecture-exploring-with-benchmarks/analysis.md`
- `older_stuff/architecture-exploring-with-benchmarks/Architecture-Automated-Exploration/question-bank/questions/logic-bbeh.md`

### 3. Old ARC-AGI tasks

Best candidates:

- `ARC Q2` Key-Color Mapping
  - type: exact grid match
  - likely failure mode: abstraction + induced symbolic mapping
- `ARC Q3` Flood Fill Enclosed Regions
  - type: exact grid match
  - likely failure mode: closed-vs-open region detection
- `ARC Q4` Fractal Self-Similar Tiling
  - type: exact grid match
  - likely failure mode: recursive pattern expansion

Why this bucket is strong:
- adds a non-language abstraction modality without needing images
- exact validation is trivial
- easy to store as text-only JSON grids

Local source:
- `older_stuff/architecture-exploring-with-benchmarks/benchmark-questions/arc-agi/questions.md`

## Best External Sources To Mine Next

These are not yet integrated locally as concrete current-bank questions, but they look strong.

### 4. HLE-Verified

- why:
  - same basic value as HLE, but with a cleaner answer set
  - reduces noise from bad or ambiguous original HLE items
- why Gemma is likely to struggle:
  - expert-domain, mostly short-answer / MC
  - even strong frontier models do not saturate HLE-style questions
- good use:
  - mine 10 to 20 verified text-only questions across science, engineering, and math

Public source:
- `https://arxiv.org/abs/2602.13964`
- `https://github.com/SKYLENAGE-AI/HLE-Verified`

### 5. GPQA

- why:
  - graduate-level, Google-proof science questions
  - much harder than standard science QA
- why Gemma is likely to struggle:
  - benchmark was designed to be difficult even for PhD-level humans and strong frontier models
- good use:
  - add a small protected set of biology / physics / chemistry MC questions

Public source:
- `https://arxiv.org/abs/2311.12022`

### 6. OlympiadBench and MathArena

- why:
  - harder and less contamination-prone than old AIME-only pools
  - good for exact-answer and proof-style math
- why Gemma is likely to struggle:
  - olympiad-level math remains unsolved territory for most open models
- good use:
  - prefer recent uncontaminated competition problems over old public AIME items

Public sources:
- OlympiadBench: `https://arxiv.org/abs/2402.14008`
- MathArena: `https://arxiv.org/abs/2505.23281`

### 7. GAIA

- why:
  - strong tool-use and general-assistant benchmark
  - conceptually simple tasks with exact final answers
- why Gemma is likely to struggle:
  - requires search, tool use, file handling, and multi-step execution
- good use:
  - mine a small text-only subset of answer-verifiable tasks
  - probably keep separate from the pure QA bank

Public source:
- `https://arxiv.org/abs/2311.12983`

## Best Score-Gradient Families To Add

These are better than one-off exact-answer coding problems if the goal is to measure improvement loops.

### 8. ALE-Bench

- why:
  - purpose-built for score-based algorithm engineering
  - iterative improvement is the point
- likely Gemma profile:
  - should produce weak-to-middling first attempts
  - should show clear room for score improvement

Public source:
- `https://openreview.net/forum?id=JCjGvbsOmQ`

### 9. EvalPerf

- why:
  - code must be correct first, then efficient
  - gives a numeric efficiency gradient instead of just pass/fail
- likely Gemma profile:
  - first attempt often passes correctness but underperforms badly on DPS

Public source:
- `https://evalplus.github.io/evalperf.html`

### 10. LiveBench / SWE-bench subsets

- why:
  - cleaner modern coding evaluation than toy programming questions
  - strong infrastructure and scoring
- likely Gemma profile:
  - repo-level tasks will likely expose navigation and patching weaknesses

Public sources:
- LiveBench: `https://github.com/LiveBench/LiveBench`
- SWE-bench FAQ: `https://www.swebench.com/SWE-bench/faq/`

## Recommended Next Promotion Set

If I were adding the next batch now, I would start with this mix:

1. `HLE Q2` Ferrite Level
2. `HLE Q7` Lattice Adsorption
3. `HLE Q9` CARS Microscopy
4. `HLE Q14` ReAl12 Polyhedra
5. `BBEH hyperbaton`
6. `BBEH sarc_triples`
7. `BBEH word_sorting`
8. `BBEH zebra_puzzles`
9. `ARC Q2` Key-Color Mapping
10. `ARC Q3` Flood Fill Enclosed Regions
11. one `ALE-Bench` task
12. one `EvalPerf` task

Why this set:
- science knowledge
- formal reasoning
- abstraction
- computation/tool use
- score-gradient coding

It would stress very different failure modes instead of overloading one domain.

## Recommended Classification Rule

When adding candidates, tag each with one dominant pressure:

- `knowledge-first`
- `reasoning-first`
- `computation-first`
- `tool-use-first`
- `score-gradient`

That will make it easier to interpret Gemma failures later.
