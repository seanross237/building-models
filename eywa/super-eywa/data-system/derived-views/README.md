# Derived Views

This folder is for views derived from preserved run truth.

Examples include:

- simplified run tables
- richer run and node tables
- summaries and indexes

Current v1 derived outputs written per run:

- `derived/timeline.json`
- `derived/timeline.md`
- `derived/simple-run-row.json`

Prompt-family experiment view:

- `prompt-family-results/`
- built from `prompt-family-results/build_prompt_family_results_page.py`
- can ingest either legacy batch summaries or prompt-family experiment summaries
- shows per-question scores, selected variables, prompt render excerpts, variant comparisons, and file paths back to the source grading/run-history artifacts
