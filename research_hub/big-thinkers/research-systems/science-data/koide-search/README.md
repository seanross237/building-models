# Koide-like Search

This directory contains a first-pass systematic search for Koide-like relations in Standard Model parameters, along with a 10,000-sample Monte Carlo null comparison.

Run it with:

```bash
python3 run_koide_search.py
```

Outputs land in `output/` and `plots/`.

Method notes:

- PDG 2025 updated central values were used where available.
- The prompt's rounded charged-lepton masses are also evaluated separately to reproduce the classic Koide number.
- The systematic search space is fixed before looking at results: Koide scans, same-unit ratio scans, generalized sum rules on predeclared mass subsets, and sin^2-angle Koide checks.
- The null model randomizes each parameter independently within one order of magnitude of its observed value, then reruns the exact same search.
- Mixed-unit scans are included because the prompt asked for them, but the report flags their representation dependence.
