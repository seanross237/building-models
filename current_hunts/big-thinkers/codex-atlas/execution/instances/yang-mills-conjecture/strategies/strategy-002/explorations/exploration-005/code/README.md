# Exploration 005: Code

## Files

### stage1_polarization_verify.py
Tests the crude polarization bound from the GOAL. Shows it FAILS — correction/baseline ratio can exceed 10. Also demonstrates the antisymmetric part is roughly 50/50 signed.

### stage2_advanced_approaches.py
Tests 8 different structural approaches:
1. Symmetric-part-only delta (PSD! but via wrong decomposition)
2. Plaquette groupings (opposite faces, vertices — all fail)
3. VCBL decomposition (remainder deeply negative)
4. Cholesky pattern (M9 always rank 9 for D≠I)
5. **KEY: M9 is affine in D** (verified to 3.5e-15)
6. **KEY: M9 >= 0 over all contractions** (0/2000 violations)
7. D=-I extreme (always PSD, min eig = 3.85)

### stage3_proof_verification.py
Verifies all 6 steps of the proof:
- Step 1: Algebraic identity 2(||u||·||v|| - u·v) = ||u-v||² - (||u||-||v||)²
- Step 2: Σ||u-v||² = 4Σf + |Σa|²
- Step 3: F decomposition: F = 2Σf + Σ(||u||-||v||)²
- Full chain: sum_S >= F >= 0 (5000 trials, 0 violations)
- Adversarial: min F ≈ 0 (at T on axes)

### stage4_final_verification.py
High-precision final verification:
- 50K random trials
- 10K adversarial starts + gradient optimization
- Full M9 eigenvalue adversarial search

## Running
```bash
python3 stage1_polarization_verify.py   # ~10 sec
python3 stage2_advanced_approaches.py   # ~30 sec
python3 stage3_proof_verification.py    # ~2 min
python3 stage4_final_verification.py    # ~15 min
```

All scripts use numpy and scipy. No other dependencies.
