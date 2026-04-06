# Gemma 4 26B A4B IT Benchmark Note

- Label: `gemma426b_a4b_it_benchmark_2026_04_06`
- Runtime provider: `openrouter`
- Model: `google/gemma-4-26b-a4b-it`
- Consolidated summary: `data-system/grading/runs/gemma426b_a4b_it_benchmark_2026_04_06__summary.json`
- Manual review overlay: `data-system/grading/runs/gemma426b_a4b_it_benchmark_2026_04_06__manual-review.json`

Snapshot:

- Completed stored runs: `28`
- Timed-out runs: `3`
- Auto-graded completed runs: `5`
- Correct: `1`
- Wrong: `4`
- Completed but ungraded: `23`

Manual review overlay:

- Format-only recoveries from the 4 auto-graded wrong runs: `0`
- Additional manually counted correct runs: `0`
- Additional manually judged incorrect / non-solution runs: `16`
- Additional manually judged partial / uncertain runs: `7`
- Final total that should count as correct: `1`
- Final total incorrect / non-solution: `20`
- Final total partial / uncertain: `7`
- Completed runs with token and wall-time metrics: `28`
- Completed runs missing token or wall-time metrics: `0`

Timed-out questions:

- `atlas-derived-A9-yang-mills-mass-gap-proof-gap`
- `coding-B1-usaco-2024-us-open-platinum-identity-theft`
- `coding-B2-usaco-2023-us-open-gold-tree-merging`

Notes:

- Per-question run artifacts were written under `data-system/run-history/` when execution completed.
- Per-question grading records were written under `data-system/grading/runs/` when grading reached record-write.
- The timed-out cases only wrote partial run directories with `run_packet.json`; they did not reach `node_record.json` or `run_summary.json`.
