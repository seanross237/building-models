# Code Directory

All scripts use Python 3 with numpy only (scipy unavailable due to version conflict).

## Scripts

- **stage1_verify_DI.py** — Initial verification that sum_S(D=I) ≠ 0 (correcting E003), derivation of the identity sum_S(D=I) = 6Σf + |Σ R^T T|².

- **stage1_proof.py** — Complete algebraic proof of sum_S(D=I) ≥ 0 with verification of all components: f(R^T,p)=f(R,p), diagonal counting, cross term factoring, null space characterization, and the Delta_S factoring identity.

- **stage2_delta_analysis.py** — Analysis of dead-end approaches: convexity (fails), budget vs cross ratio (0.29), VCBL(-I) decomposition (remainder negative), per-plaquette VCBL with optimal M (impossible due to rank).

- **stage2_proof_attempt.py** — Adversarial eigenvalue search (500 starts + gradient descent), budget/cross matrix analysis (B9≥C9 fails), M12 negative eigenspace analysis (2 negative eigs, NOT confined to V^perp).

- **stage3_squared_norms.py** — Intensive adversarial search (5000 starts), M12 PSD test (fails), Gershgorin bound (fails), off-diagonal NSD structure confirmation.

- **stage3_critical_T_proof.py** — **KEY SCRIPT**: Proves Critical T theorem (u=v on rotation axes), verifies z^T Δ z ≥ 0, checks 2×2 submatrix PSD, mega adversarial search (50K + 10K + gradient, min = 3.9e-13).

## Run Order
Run in order: stage1_proof.py → stage3_critical_T_proof.py (the key results).
