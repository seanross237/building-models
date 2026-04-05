# Data System — Detailed Target State

## Target Design

This doc describes the target shape of the `data-system/`.

It is the build-guiding target doc for the storage, grading, and correctness side of Super-Eywa.

It should stay aligned with the root Super-Eywa target docs and the Eywa target docs.

## What The Data-System Is

The data-system is the truth-preserving and evaluation layer around Eywa.

Its job is not just to archive raw runs.

Its job is to preserve and organize what happened in a form that can later be:

- reconstructed
- reorganized
- graded
- compared
- learned from

The data-system owns:

- preserved run truth
- preserved node truth
- replay artifacts
- grading question organization
- grading runs and scores
- correctness-suite artifacts
- derived summaries and tables

The data-system does not own:

- task execution
- node runtime behavior
- direct variable selection during execution

## Data-System North Star

The north star for the data-system is:

- preserve enough truth that a run can later be understood and, as much as possible, reconstructed
- keep effectiveness grading separate from correctness protection
- organize data cleanly enough that Bonsai can later learn from it without a redesign

The data-system should be built so that the preserved truth remains the source of reality, and any later tables, dashboards, or learning views are derived from that truth rather than replacing it.

## Canonical Truth Vs Derived Views

The data-system should have two layers:

- canonical preserved truth
- derived views

### Canonical Preserved Truth

This is the source of truth.

For each run, it should preserve:

- one `run_packet`
- one `node_packet` per node run
- one core node record per node run
- one replay record per node run

This canonical layer should be complete enough that later reorganizations do not require guessing what happened.

### Derived Views

These are query-friendly, comparison-friendly, and learning-friendly views built from the canonical truth.

Examples include:

- simplified run tables
- richer run and node tables
- question indexes
- grading summaries
- later benchmark summaries

The derived layer is important, but it should not become the only truth.

## Core Run Storage Contract

### Run Packet

Every overall run should preserve a `run_packet`.

At a high level, it should preserve:

- the original top-level task exactly as given
- run-level variables
- top-level context, constraints, and attachments
- root setup facts

### Node Packet

Every node run should preserve a `node_packet`.

At a high level, it should preserve:

- the node input
- the full resolved variables for that node
- node-specific setup facts

Even if run-level defaults and node-level overrides are also tracked, the full resolved variable set should always be preserved at the node level.

### Core Node Record

Every node run should preserve the same core record categories:

- `input`
- `variables`
- `state`
- `results`
- `prompt`
- `logging`

This is the clean, readable layer for understanding what happened.

### Replay Record

Every node run may also preserve a heavier replay record.

This is where the data-system should keep deeper reconstruction material such as:

- raw model request and response artifacts
- tool transcripts
- prepared prompt snapshots
- other heavy execution artifacts

The replay record should remain separate from the core node record so the default readable layer stays calm.

## Simplified And Richer Tables

The data-system should support both simple and richer derived views.

### Simplified Run Table

There should be a very simple run-level table with at least:

- `run_id`
- `task`
- `variables_json`
- `scores_json`

This table exists for easy comparison and later learning work.

It is intentionally simple and denormalized.

### Richer Derived Tables

The data-system should also support richer derived tables and views such as:

- runs
- node runs
- edges
- events
- artifacts
- replay references

These do not all need to be implemented immediately, but the preserved truth should make them straightforward to derive.

## Grading

The grading area is for effectiveness-oriented evaluation.

It should stay separate from the correctness suite.

The intended structure is:

- `grading/test-questions/`
- `grading/question-types/`
- `grading/grading_methods/`
- `grading/runs/`
- `grading/benchmarks/`
- `grading/all-test-questions.md`

### Test Questions

The canonical question files live in:

- `grading/test-questions/`

Every test question should be a single file that is easy for a human to read and easy for the system to index later.

At a high level, each question file should preserve:

- question id
- title
- type
- tags
- question or task text
- source
- grading method
- grading notes
- status
- notes

### Question Types

The type-based grouping layer lives in:

- `grading/question-types/`

This is an organizational and indexing layer.

It should help humans and agents browse the bank by type without changing where the canonical files live.

### Grading Methods

Reusable grading logic should live in:

- `grading/grading_methods/`

Examples include:

- exact match
- binary pass/fail
- numeric scoring
- test-suite-based grading
- later rubric or similarity grading

### Grading Runs

Actual runs against test questions should live in:

- `grading/runs/`

This area should preserve:

- which question was run
- which run or variant produced the answer
- what answer or artifact was submitted for grading
- the resulting score
- any grading metadata

### Benchmarks

Not every graded question needs to be part of an official benchmark set.

The `benchmarks/` area should be reserved for promoted and more stable benchmark collections or views.

This keeps the broader grading area from being confused with the smaller official benchmark subset.

## Correctness Suite

The correctness suite exists for a different purpose from grading.

Its job is to protect whether the machine is behaving correctly, not whether it is performing well on scored tasks.

The correctness side should eventually support things like:

- dry-run checks
- contract checks
- scenario checks
- later behavior-preserving equivalence checks for Potter

It should stay separate in both naming and structure from grading.

## V1 Priority

For v1, the data-system should prioritize:

- preserving raw truth
- preserving resolved variables
- preserving prompts
- preserving logging and graph facts
- preserving replay material separately
- organizing test questions cleanly
- keeping correctness and grading clearly separate

For v1, the data-system should not require:

- mature ML infrastructure
- a database-first architecture
- a finalized benchmark promotion pipeline
- a perfect tagging system

The first job is to preserve and organize the truth in a way that does not paint us into a corner later.

## What V1 Must Preserve

At minimum, v1 should preserve enough that a later system could reconstruct the important shape of a run.

That means preserving:

- the original task
- run-level variables
- node inputs
- node resolved variables
- prompts
- results
- logging
- graph relationships
- usage, time, and cost information when available
- replay material

If a run is also part of grading, the data-system should preserve:

- the question identity
- the submitted answer or artifact
- the score
- the grading method used

## Database Strategy

A database may later sit on top of this system, but the initial design should not depend on having one in place from day one.

The safer target is:

- preserve the canonical truth on disk first
- derive database tables or indexed views from that truth

This keeps the system flexible while still making later structured querying possible.

The intended first on-disk storage shape should follow:

- `run-history/run-layout-v1.md`

## Future Expansion

Later Bonsai work, including Gardener-style hypothesis generation, should consume the preserved truth and derived views from this data-system.

That later learning layer should not require the preserved run truth to be redesigned.

## Still To Decide

- the exact on-disk file and folder layout for preserved runs
- the exact serialization format for packets and records
- the exact `scores_json` schema for the simplified run table
- the exact question tag taxonomy
- the exact benchmark promotion rules
- the exact first correctness-suite substructure
- the exact database technology, if any, that should sit on top of the preserved truth
