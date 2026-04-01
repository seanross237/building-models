# Exploration 006 Code

All scripts use Python 3 + NumPy. Run from this directory.

## Scripts

1. **full_operator_check.py** — Main verification: builds M(Q) and D(Q)=M(Q)-M(I) for 50 configs, checks all eigenvalues. Finding: M(Q) ≼ M(I) is FALSE.

2. **pure_gauge_and_spectrum.py** — Pure gauge isometry verification: checks M(Q)=Ad_G^T M(I) Ad_G, isospectrality, and λ_max(M(Q))≤4d for 45 configs.

3. **top_eigenspace_check.py** — KEY: Projects R(Q) onto the 9-dim top eigenspace of K_curl. Finding: P^T R(Q) P ≼ 0 for all 42 configs. Also: abelian decomposition and trace analysis.

4. **gradient_ascent_fast.py** — Gradient ascent on λ_max(M(Q)) and λ_max(P^T R P). Finding: both plateau well below their upper bounds.

5. **quick_gradient.py** — Faster gradient ascent variant (fewer steps, 10 trials).

6. **abelian_and_gradient.py** — Abelian config sector analysis (τ₃ vs τ₁τ₂ block decomposition).

7. **analytical_trace_proof.py** — Trace analysis: Tr(M(Q))=const, Tr(M²) varies.

## Key finding
`top_eigenspace_check.py` contains the most important result: the correct inequality is P^T R(Q) P ≼ 0 (a 9×9 matrix condition), not the full operator inequality R(Q) ≼ 0 (which is false).
