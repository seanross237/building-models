# Code for Exploration 002

All scripts require Python 3 with numpy and scipy. Run with `/opt/homebrew/bin/python3`.

## Scripts

| File | Purpose |
|---|---|
| `step1_single_plaquette.py` | Verify d²/dt² Re Tr(U□) = Re Tr(w²U) + Σ Re Tr([wᵢ,wⱼ]U) for single plaquettes |
| `step2_su2_crossproduct.py` | Initial (buggy) cross-product formula test |
| `step2_sign_debug.py` | **Correct** cross-product formula: comm = +(1/2) L⃗·b⃗ |
| `step3_debug.py` | Verify one-parameter formula matches FD (establishes formula is correct) |
| `step3_hessian_v2.py` | Full 192×192 Hessian: analytical vs FD vs B² formula |
| `step4_bound_analysis.py` | Decompose C, check per-plaquette, multi-config analysis |
| `step4_final_analysis.py` | **Main result**: corrected C = C_curv + C_comm decomposition |

## Key result

Run `step4_final_analysis.py` for the complete analysis including:
- SU(2) product identity verification
- Exact matrix decomposition C = C_curv + C_comm
- Spectral analysis showing C is not PSD but λ_max inequality holds
- Top eigenvector analysis showing the compensation mechanism
