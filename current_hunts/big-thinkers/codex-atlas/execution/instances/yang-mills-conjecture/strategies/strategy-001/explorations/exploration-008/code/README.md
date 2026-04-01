# Exploration 008 Code

All scripts are Python 3 with numpy. Run from the `code/` directory.

## Scripts (in order)

1. **task1_eigenspace.py** — Builds the full 192x192 M(Q) matrix and verifies the 9D eigenspace at Q=I. Tests restricted Rayleigh quotients. (EXPENSIVE — takes ~30 min for adversarial part)

2. **task2_pervertex_general.py** — Builds the 12x12 per-vertex matrix M_12 and tests the constrained eigenvalue. Key results: constrained max = 15.997 (adversarial), unconstrained can reach ~21.

3. **task3_budget_decomposition.py** — Budget identity verification, per-plaquette gap analysis, gap = f_same + cross decomposition. Key result: max harmful cross/f_same = 0.082.

4. **task4_proof_attempt.py** — Adversarial search for violations and gap structure analysis. 200 trials, all below 15.77.

5. **task5_uniform_color_proof.py** — Tests uniform-color bound for all spatial patterns s. Adversarial: max ratio = 14.86 (below 16).

6. **task6_definitive_verification.py** — Large-scale verification (100K random, 10K extreme, 500 adversarial). (May still be running)

7. **task7_key_identity.py** — Verifies the three key algebraic identities (budget, per-plaquette expansion, combined bound).
