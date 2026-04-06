# Prompt Family Results

This folder holds the generated results page for the prompt-family experiment loop.

It is designed to be manifest-driven and file-first:

- read grading rows either from `data-system/grading/runs/` batch summaries or from `data-system/grading/experiment-runs/` prompt-family experiment summaries
- resolve node variables from the stored `run-history/` artifacts
- render a static HTML dashboard with the selected variables, prompt text, scores, and artifact links
- keep the generated HTML self-contained so it can be opened directly from disk

Primary entry point:

- `build_prompt_family_results_page.py`

Generated outputs:

- `results.json`
- `index.html`

Supported source summaries:

- `data-system/grading/runs/live-batch-v1-summary.json`
- `data-system/grading/experiment-runs/<benchmark-id>/<experiment-run-id>.json`

Regenerate it with:

```bash
python3 data-system/derived-views/prompt-family-results/build_prompt_family_results_page.py
```

Or point it at a prompt-family experiment run explicitly:

```bash
python3 data-system/derived-views/prompt-family-results/build_prompt_family_results_page.py \
  --summary data-system/grading/experiment-runs/transmute-three-failures-v1/<experiment-run-id>.json
```

The page shows:

- experiment rows grouped by question
- per-row scores and validation state
- resolved variables selected for the run
- prompt-family variant ids and comparison deltas when present
- prompt render excerpts from the stored run-history replay
- direct file links to grading records, run packets, node records, prompt snapshots, and raw model outputs
