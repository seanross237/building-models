# Code for Exploration 002

## Files

- `compute_plaquette_contributions.py` — Main computation. Runs 36 configs (Haar, near-identity, Gibbs, abelian, adversarial). Tests plane-type, vertex-star, edge-star, cube-face groupings. Output: `/tmp/exploration002_output.txt`

- `deep_analysis.py` — Stress tests. 10,000 random Haar configs × 16 vertices = 160,000 cube-face tests. Adversarial attacks on individual cube sums. Finer grouping analysis (active-only, inactive-only, per-direction). Output: `/tmp/exploration002_deep.txt`

- `alg_test2.py` — Algebraic formula derivation and proof for simplified case (cross-links = I). Derives ∑|B|² = 32 + 8⟨n,W⟩ − |A|² and proves ≤ 64 by triangle inequality. Adversarial attack on general case confirms max = 64. Output: `/tmp/exploration002_alg2.txt`

## Run order
1. `python3 compute_plaquette_contributions.py` (≈60s)
2. `python3 deep_analysis.py` (≈120s)
3. `python3 alg_test2.py` (≈60s)

## Dependencies
numpy, scipy (standard)
