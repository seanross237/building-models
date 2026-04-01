# Code README — Exploration 001

## Files

| File | Purpose |
|------|---------|
| `stage1_numerical.py` | Stage 1: 1000-sample numerical verification; M_12 sanity check |
| `stage2_3_adversarial.py` | Stage 2+3: Formula verification, SDP check, Riemannian gradient ascent |
| `stage4_sos.py` | Stage 4: Per-plaquette identity, f_same/cross analysis, obstruction |
| `stage4b_certificate_attempt.py` | Stage 4b: Per-plaquette ratio, algebraic block, 5000-sample M_9 analysis |
| `stage4c_algebraic_identity.py` | Stage 4c: Algebraic identities, decomposition formula |
| `stage5_epsilon.py` | Stage 5: Epsilon bound, gap rate near Q=I, full formula verification |

## Requirements

- Python 3.14+
- numpy (2.4+), scipy

No additional packages required (cvxpy not available; SDP done via eigenvalue tests).

## Run Order

```bash
python3 code/stage1_numerical.py
python3 code/stage2_3_adversarial.py   # ~135s
python3 code/stage4_sos.py             # ~30s
python3 code/stage4b_certificate_attempt.py  # ~90s
python3 code/stage4c_algebraic_identity.py   # ~15s
python3 code/stage5_epsilon.py         # ~20s
```

## Key Functions

- `construct_M12(R_list, D_dict)` → 12×12 matrix of per-vertex quadratic form
- `compute_constraint_basis()` → 12×9 orthonormal basis W for V = {sum T_mu = 0}
- `lambda_max_M9(M12, W)` → max eigenvalue of M_12 restricted to V
- `adversarial_ascent(...)` → Riemannian gradient ascent on SO(3)^10
