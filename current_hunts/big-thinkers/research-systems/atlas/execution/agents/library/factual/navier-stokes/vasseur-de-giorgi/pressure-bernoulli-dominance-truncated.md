---
topic: Truncated pressure is Bernoulli-dominated for Beltrami flows — R_frac = O(2^{-k}), CZ-lossy piece vanishes
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-007"
---

## Finding

For ABC (Beltrami) flows, the pressure of the De Giorgi-truncated velocity u_below is dominated by the Bernoulli piece P_hessian = -|u_b|^2/2 at all levels k. The non-Bernoulli remainder (CZ-lossy) contributes a geometrically vanishing fraction of both the pressure norm and the bottleneck integral.

### Decomposition

- **P_hessian = -|u_b|^2/2**: Bernoulli piece (exact closed form, CZ-lossless -- no Calderon-Zygmund inversion needed)
- **P_remainder = P_total - P_hessian**: Non-Bernoulli piece (Lamb + compressibility, CZ-lossy)
- **R_frac = ||P_remainder||_{L^2} / ||P_total||_{L^2}**: Remainder fraction
- **I_r/I_t**: Remainder contribution to bottleneck integral

### ABC Flow Results (all Re identical)

| k | R_frac | I_r/I_t |
|---|--------|---------|
| 2 | 0.146  | 0.171   |
| 4 | 0.037  | 0.044   |
| 6 | 0.004  | 0.008   |
| 8 | 0.0004 | 0.002   |

At k=4, only 4.4% of the bottleneck comes from the non-Bernoulli remainder. At k=8, it is 0.2%. [COMPUTED]

### Control ICs: No Bernoulli Dominance

| IC | R_frac(k=4) | I_r/I_t(k=4) | R_frac(k=8) | I_r/I_t(k=8) |
|----|-------------|---------------|-------------|---------------|
| TG Re=500  | 1.180 | 0.53  | 1.179 | 0.63  |
| TG Re=1000 | 1.153 | 0.34  | 1.152 | 0.73  |
| RG Re=500  | 1.542 | 11.06 | 1.542 | 9.07  |
| RG Re=1000 | 1.732 | 15.82 | 1.732 | 6.19  |

R_frac > 1 means the non-Bernoulli remainder exceeds the total pressure in L^2 norm (Hessian and remainder partially cancel, giving smaller P_total). Massive cancellation in the bottleneck integral. No Bernoulli dominance at any k. [COMPUTED]

### Effective CZ Constant

For the De Giorgi iteration, the effective CZ constant at level k is:

```
C_eff(k) ~ 1 + epsilon_k * (C_q - 1)
```

where epsilon_k = I_r/I_t. For ABC at k=4: epsilon_4 = 0.044, so C_eff ~ 1.0 (essentially no CZ loss). For non-Beltrami flows: epsilon_k ~ 1 or larger, so C_eff ~ C_q (full CZ loss).

### Why div(u_below) != 0 Does Not Matter

The truncation breaks incompressibility: ||div(u_below)||_{L^2} = O(2^{-k}). This invalidates the standard three-way Hessian/Lamb/compressibility decomposition. The clean two-way Bernoulli/remainder decomposition is used instead. The fact that the total remainder STILL vanishes as O(2^{-k}) despite the incompressibility violation is the stronger statement: the Beltrami property provides enough geometric structure to overcome the divergence violation.

### Verification

- Full ABC field at t=0: B_deficit = 3.0e-15 (machine precision zero)
- At k=8: R_frac = 3.8e-4 -> 0
- Sign convention verified: P_total -> -|u|^2/2 = P_hessian for exact Beltrami
- Initial v1/v2 code had sign error (R_frac ~ 2.0 everywhere); caught by t=0 sanity check; corrected in v3

### Implications for Conditional Regularity

The Beltrami conditional regularity mechanism (E006) survives the De Giorgi truncation. The CZ bottleneck that limits beta to 4/3 for generic flows is effectively removed for Beltrami flows at high k. beta_eff can approach the geometric limit (~5/3 in 3D) rather than being capped by CZ losses. This is Re-independent (intrinsic to spatial geometry).

### Open Questions

1. Does B_k = O(2^{-k}) hold for perturbed ABC flows (ABC + noise)?
2. Do turbulent flows develop local Beltrami regions where this mechanism applies?
3. Is the O(2^{-k}) scaling universal for flows with helical structure?

## E009 Adversarial Assessment

The Bernoulli dominance result shares the same limitations as `beltrami-deficit-truncation-survival.md`: (a) trivially expected for exact Beltrami (smooth function under smooth truncation), (b) the div(u_below) != 0 issue means the "Bernoulli" piece is not strictly the pressure of u_below, and (c) near-Beltrami behavior is uncharacterized. The "effective CZ constant C_eff ~ 1.0" conclusion is valid as a measurement but does not establish that a small effective CZ constant implies improved beta in the De Giorgi recurrence. Grade: C+ (linked to Claim 5 weaknesses). See `beltrami-deficit-truncation-survival.md` for the full adversarial critique.

## E010 Definitive Negative Result

**Near-Beltrami behavior is now characterized: Bernoulli dominance does NOT generalize.**

| eps | R_floor (remainder fraction at high k) |
|-----|----------------------------------------|
| 0.00 | ~0 |
| 0.01 | 0.014 (1.4%) |
| 0.05 | 0.073 (7.3%) |
| 0.20 | 0.346 (34.6%) |
| 0.50 | 1.285 (R > 1, decomposition meaningless) |

The ">95% Bernoulli" claim holds only for eps < ~0.01. Leray projection reduces R_frac at low k by ~2x but does not change the high-k picture. **Answers open question #1: No, B_k does NOT hold for perturbed ABC; answers #2/#3: Not testable because mechanism doesn't activate.** See `../../near-beltrami-negative-result.md` for full data.
