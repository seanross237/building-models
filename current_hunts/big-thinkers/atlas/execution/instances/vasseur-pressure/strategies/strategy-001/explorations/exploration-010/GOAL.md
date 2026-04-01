<!-- explorer-type: math -->

# Exploration 010: Perturbed-ABC Near-Beltrami Test + Leray Projection

## Goal

Address the adversarial review's #1 weakness: the Beltrami-De Giorgi mechanism (B_k = O(2^{-k}), pressure >95% Bernoulli) is only demonstrated for EXACT Beltrami flows, which are trivially regular. Test whether the mechanism extends to NEAR-Beltrami flows.

## Background

Exploration 007 showed that for exact ABC (Beltrami) flows:
- B_k = ||curl(u_below) − λ·u_below||/||u_below|| ≈ 0.56 × 2^{-k}
- Pressure remainder fraction R_frac ≈ O(2^{-k})
- Controls (TG, RG): B_k ≈ const (no improvement with k)

The adversarial review (E009) flagged: "B_k = O(2^{-k}) for exact Beltrami is trivially true — any smooth structural property shrinks under smooth truncation. The interesting question is near-Beltrami."

## Task A: Perturbed-ABC — Near-Beltrami B_k Behavior

### Setup

Generate perturbed-ABC initial conditions:
```
u_perturbed = (1-ε) · u_ABC + ε · u_random
```

where u_ABC is the standard ABC flow (A=B=C=1) and u_random is a random divergence-free field with the same energy spectrum (k^{-5/3}, projected div-free). The factor (1-ε) ensures the perturbation is properly weighted.

After generating, normalize so max|u| = 1 (L^∞ normalization, matching E002/E007).

### Perturbation Levels

ε = 0.01, 0.05, 0.1, 0.2, 0.5

These span from "almost pure Beltrami" (ε=0.01) to "half random" (ε=0.5).

### Measurements (for each ε)

At Re = 500, N = 64:

1. **Run DNS** to time T_final = 2.0 (enough for the flow to evolve beyond the initial condition)
2. **Compute B_k(u_below) for k = 0, ..., 8** (same as E007)
3. **Compute R_frac for k = 0, ..., 8** (Bernoulli remainder fraction, same as E007)
4. **Compute β_eff** via the De Giorgi recurrence fit (same as E002)

### Output Tables

Table A1 — Beltrami deficit vs k by perturbation level:
| ε | B_0 | B(k=2) | B(k=4) | B(k=6) | B(k=8) | Trend | B_k/B_0 at k=8 |
|---|---|---|---|---|---|---|---|

Table A2 — Remainder fraction vs k by perturbation level:
| ε | R(k=2) | R(k=4) | R(k=6) | R(k=8) | Trend |
|---|---|---|---|---|---|

Table A3 — β_eff vs perturbation level:
| ε | β_eff | std_err | BN_exp (γ) | R² |
|---|---|---|---|---|

### Key Questions

1. **Does B_k decrease with k for near-Beltrami flows?**
   - If B_k/B_0 → 0 as k increases (like exact Beltrami): mechanism generalizes
   - If B_k ≈ B_0 at all k (like TG/RG controls): mechanism is specific to exact Beltrami
   - If B_k/B_0 decreases but to a nonzero limit: partial generalization

2. **Is the degradation continuous in ε?**
   - Plot β_eff vs ε. If β_eff decreases smoothly from ~1.0 (ε=0) to ~0.5 (ε=0.5): continuous
   - If there's a sharp transition at some ε_critical: threshold behavior

3. **Does time evolution destroy Beltrami structure?**
   - Compare B_k at t=0 vs t=T_final. For ε > 0, the NS evolution will generically break Beltrami structure. How fast? Is B_0(t=T_final) >> B_0(t=0)?

## Task B: Leray-Projected u_below

### Motivation

Exploration 007 discovered that div(u_below) ≠ 0 — the truncation breaks incompressibility. This invalidates the Hessian/Lamb decomposition identity. The adversarial review suggested projecting u_below onto divergence-free fields via Leray projection:

```
u_below_df = P_Leray(u_below) = u_below − ∇Δ^{-1}(div u_below)
```

On a periodic domain, this is spectral: zero out the irrotational component in Fourier space.

### Measurements

For exact ABC (ε=0) at Re = 500:

1. Compute u_below_df = P_Leray(u_below) for k = 0, ..., 8
2. Compute B_k(u_below_df) — the Beltrami deficit of the div-free projected truncation
3. Compute the Hessian/Lamb decomposition for u_below_df (now valid since div = 0)
4. Compute the Lamb vector contribution to the bottleneck integral

Compare with the unprojected results from E007.

### Key Question

Does Leray projection change the picture?
- If B_k(u_below_df) ≈ B_k(u_below): div issue is negligible, E007 results stand
- If B_k(u_below_df) is significantly different: the div issue matters and E007 needs correction

## Prior Code

All infrastructure from E002 and E007:
- `exploration-002/code/ns_solver.py` — DNS solver
- `exploration-002/code/degiorgi_measure.py` — De Giorgi level-set computation
- `exploration-007/code/` — Beltrami deficit and Bernoulli/remainder decomposition

**IMPORTANT:** Use the CORRECTED sign convention from E007 (P_hat = -k_ik_j FFT(u_iu_j)/|k|², with the minus sign).

## Success Criteria

✅ **Success:**
- B_k measured for all 5 perturbation levels × 9 k-values
- β_eff measured for all 5 perturbation levels
- Clear determination of whether B_k improvement generalizes to near-Beltrami
- Leray projection comparison for exact ABC
- All values tagged [VERIFIED]/[COMPUTED]

❌ **Failure:**
- Perturbed ABC is unstable at Re=500 → reduce Re to 100
- B_k computation is numerically noisy → increase snapshot count
- Leray projection introduces artifacts → compare at t=0 (known-answer check)

## Output Format

Task A Results (tables A1-A3 + key questions answered) → Task B Results → Combined Interpretation → Implications for Claim 5. Include ALL code.
