# Exploration 005 Code

## Files

- **hessian_core.py**: Core lattice + Hessian computation. Includes verified F formula with closed-form SVD.
- **approach_tests.py**: Tests all 6 proof approaches on d=4, L=2. Run: `python approach_tests.py`
- **gradient_ascent_C_norm.py**: Gradient ascent on ||C(Q)|| to find global max. Found counterexample ||C||=11.68 > 10. Run: `python gradient_ascent_C_norm.py` (~30min)
- **decoherence_proof.py**: Per-plaquette decoherence proof verification + lattice aggregation. Run: `python decoherence_proof.py` (~15min)
- **proof_attempt.py**: Schur product analysis, contraction bounds, per-entry analysis. Run: `python proof_attempt.py` (~5min)

## Dependencies
- numpy (tested with 1.24+)
- Python 3.8+

## Key result
The decoherence lemma ||C(Q)|| ≤ 2(d+1) is FALSE for d ≥ 3. Counterexample found by gradient ascending from anti-instanton configs.
