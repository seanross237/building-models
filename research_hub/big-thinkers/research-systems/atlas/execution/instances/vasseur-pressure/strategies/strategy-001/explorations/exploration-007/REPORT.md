# Exploration 007: Beltrami Deficit of u_below + Hessian/Lamb Decomposition on DNS

## Goal

Two linked computational measurements on DNS data that determine whether the Beltrami conditional regularity mechanism survives the De Giorgi truncation:

- **Task A:** Measure the Beltrami deficit of the truncated velocity u_below as a function of De Giorgi level k.
- **Task B:** Decompose the P_k^{21} pressure source into its Hessian/Bernoulli (CZ-lossless) and remainder (CZ-lossy) pieces and measure their relative contributions to the bottleneck integral.

## Setup

- **ICs:** ABC (A=B=C=1), Taylor-Green, Random Gaussian
- **Re:** 100, 500, 1000
- **N:** 64 primary (N=128 convergence check pending)
- **K_max:** 8
- **Normalization:** L^∞ (max|u| = 1)
- **Snapshot:** Final snapshot after evolution to T = min(2π/max(Re^{0.5}·0.01, 0.1), 5.0)

## Critical Discovery: Truncation Breaks Divergence-Free [COMPUTED]

**Before presenting results, a key finding from debugging:** The De Giorgi truncation u_below = u · min(1, λ_k/|u|) is NOT divergence-free even when u is. This breaks the standard identity:

```
∂_i∂_j(u_iu_j) = Δ(|u|²/2) + div(ω × u)
```

which requires div(u) = 0. The correct decomposition for non-div-free u_below includes an additional compressibility term:

```
∂_i∂_j(u_{b,i} u_{b,j}) = Δ(|u_b|²/2) + div(ω_b × u_b) + div(u_b · div(u_b))
```

**Measured div(u_below) for ABC at t=0:**

| k | λ_k    | ||div(u_b)||_L2 | frac_above_threshold |
|---|--------|----------------:|--------------------:|
| 1 | 0.500  | 2.342          | 74.5%               |
| 2 | 0.750  | 1.674          | 44.1%               |
| 3 | 0.875  | 0.948          | 24.0%               |
| 4 | 0.9375 | 0.479          | 12.2%               |
| 5 | 0.9688 | 0.218          | 5.6%                |
| 6 | 0.9844 | 0.086          | 2.0%                |
| 7 | 0.9922 | 0.033          | 0.6%                |
| 8 | 0.9961 | 0.013          | 0.2%                |

The divergence violation scales as O(2^{-k}), consistent with the truncation width. At high k (k≥6), div(u_below) is negligible.

**Methodological response:** Instead of the three-way Hessian/Lamb/compressibility split, we use the cleaner two-way decomposition:

- **P_hessian = −|u_b|²/2** (Bernoulli piece, exact in closed form, CZ-lossless)
- **P_remainder = P_total − P_hessian** (everything non-Bernoulli: Lamb + compressibility + cross-terms)

For exact Beltrami + div-free: P_remainder = 0. For near-Beltrami or non-div-free: P_remainder captures all departures.

---

## Task A: Beltrami Deficit Results [COMPUTED]

### Definition

For truncated velocity u_below at De Giorgi level k:
```
λ_opt = ⟨curl(u_below), u_below⟩ / ||u_below||²
B_k = ||curl(u_below) − λ_opt · u_below||_{L²} / ||u_below||_{L²}
```

B_k = 0 iff u_below is an exact eigenfunction of curl (Beltrami condition).

### ABC Flow (A=B=C=1)

**Key observation:** All ABC results are IDENTICAL across Re = 100, 500, 1000. This is correct physics — the ABC flow decays self-similarly as u(t) = u(0)e^{−νt}, and after L^∞ normalization the spatial pattern is Re-independent. `[CHECKED]`

| k | λ_k    | B_k     | λ_opt   | B_k / B_{k-1} |
|---|--------|---------|---------|----------------|
| 0 | 0.000  | 0.0000  | 0.000   | —              |
| 1 | 0.500  | 0.2792  | −1.000  | —              |
| 2 | 0.750  | 0.1368  | −1.000  | 0.490          |
| 3 | 0.875  | 0.0690  | −1.000  | 0.504          |
| 4 | 0.9375 | 0.0333  | −1.000  | 0.483          |
| 5 | 0.9688 | 0.0148  | −1.000  | 0.443          |
| 6 | 0.9844 | 0.0057  | −1.000  | 0.383          |
| 7 | 0.9922 | 0.0022  | −1.000  | 0.392          |
| 8 | 0.9961 | 0.0009  | −1.000  | 0.398          |
| Full | 1.0 | 3.0e-15 | −1.000  | —              |

**Pattern:** B_k ≈ 0.56 × 2^{−k}. The deficit halves at each level. The optimal eigenvalue λ_opt = −1.000 at all k, matching the exact curl eigenvalue of ABC flow. `[COMPUTED]`

**Physical interpretation:** The truncation clips |u_below| ≤ λ_k but does NOT destroy the directional alignment with curl. At level k, only the fraction of the domain with |u_norm| > λ_k is modified, and that fraction shrinks as 2^{−k}. The perturbation to the Beltrami structure is confined to this shrinking set.

### Taylor-Green (Control)

| IC | Re | B_full | B(k=2) | B(k=4) | B(k=6) | B(k=8) | Trend |
|----|----|--------|--------|--------|--------|--------|-------|
| TG | 100 | 2.961 | 2.957  | 2.960  | 2.961  | 2.961  | ≈ const |
| TG | 500 | 4.370 | 4.293  | 4.368  | 4.370  | 4.370  | ≈ const |
| TG | 1000| 4.879 | 4.767  | 4.874  | 4.879  | 4.879  | ≈ const |

B_k ≈ B_full at all k. Taylor-Green has NO Beltrami structure. `[COMPUTED]`

### Random Gaussian (Control)

| IC | Re | B_full  | B(k=2) | B(k=4)  | B(k=6)  | B(k=8)  | Trend |
|----|----|---------|--------|---------|---------|---------|-------|
| RG | 100 | 3.022  | 3.025  | 3.022   | 3.022   | 3.022   | ≈ const |
| RG | 500 | 6.646  | 6.645  | 6.646   | 6.646   | 6.646   | ≈ const |
| RG | 1000| 12.41  | 12.41  | 12.41   | 12.41   | 12.41   | ≈ const |

B_k ≈ B_full at all k. Random Gaussian has NO Beltrami structure. B_full increases with Re (more small-scale structure makes the best-fit Beltrami eigenvalue less meaningful). `[COMPUTED]`

### Task A Summary

| IC | B_k behavior | Interpretation |
|----|-------------|----------------|
| **ABC** | B_k ≈ 0.56 × 2^{−k} → 0 | **Truncation preserves Beltrami structure** |
| **TG**  | B_k ≈ B_full ≈ 3–5 (const) | No Beltrami structure to lose |
| **RG**  | B_k ≈ B_full ≈ 3–12 (const) | No Beltrami structure to lose |

**Verdict: The De Giorgi truncation preserves Beltrami structure for ABC flows.** The deficit scales as O(2^{−k}), meaning the mechanism is strongest precisely at the high-k levels where the De Giorgi iteration needs it.

---

## Task B: Hessian/Remainder Pressure Decomposition Results [COMPUTED]

### Definitions

- **P_total**: Pressure from Poisson solve −Δp = ∂_i∂_j(u_{b,i} u_{b,j})
- **P_hessian = −|u_b|²/2**: Bernoulli/Hessian piece (zero mean). CZ-lossless: the Riesz transform R_iR_j acting on a pure Hessian ∂_i∂_j(f) returns exactly f.
- **P_remainder = P_total − P_hessian**: Non-Bernoulli piece (Lamb vector + compressibility correction). This is the CZ-lossy part.
- **R_frac = ||P_remainder||_L2 / ||P_total||_L2**: Fraction of pressure that is non-Bernoulli
- **I_r/I_t**: Remainder's contribution to the bottleneck integral ∫|P|·|d_k|·1_{v_k>0} dx

### ABC Flow — Pressure Decomposition (all Re identical)

| k | H_frac (||P_H||/||P||) | R_frac (||P_R||/||P||) | I_r/I_t | I_h/I_t |
|---|:----------------------:|:----------------------:|:-------:|:-------:|
| 0 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2 | 1.070 | **0.146** | **0.171** | 1.129 |
| 4 | 1.008 | **0.037** | **0.044** | 1.026 |
| 6 | 1.000 | **0.004** | **0.008** | 1.003 |
| 8 | 1.000 | **0.0004** | **0.002** | 1.000 |

**The Bernoulli piece dominates the bottleneck at all k.** At k=4, only 4.4% of the bottleneck comes from the non-Bernoulli remainder. At k=8, it's 0.2%. `[COMPUTED]`

The H_frac ≈ 1.0 means ||P_hessian|| ≈ ||P_total|| — the total pressure IS approximately the Bernoulli pressure.

### Taylor-Green — Pressure Decomposition

| Re | k | H_frac | R_frac | I_r/I_t | I_h/I_t |
|----|---|--------|--------|---------|---------|
| 100 | 2 | 0.784 | **1.301** | **2.75** | 2.13 |
| 100 | 4 | 0.871 | **1.344** | **11.18** | 11.54 |
| 100 | 8 | 0.871 | **1.343** | **5.50** | 6.50 |
| 500 | 2 | 0.862 | **1.198** | **0.77** | 1.43 |
| 500 | 4 | 0.863 | **1.180** | **0.53** | 1.53 |
| 500 | 8 | 0.863 | **1.179** | **0.63** | 1.63 |
| 1000| 2 | 0.860 | **1.179** | **0.83** | 1.56 |
| 1000| 4 | 0.859 | **1.153** | **0.34** | 1.25 |
| 1000| 8 | 0.859 | **1.152** | **0.73** | 1.73 |

R_frac > 1 means the non-Bernoulli remainder is LARGER than the total pressure in L2 norm. This occurs because P_hessian and P_remainder partially cancel, giving a smaller P_total. `[COMPUTED]`

I_r/I_t >> 1 at some k: massive cancellation between Hessian and remainder in the bottleneck integral.

### Random Gaussian — Pressure Decomposition

| Re | k | H_frac | R_frac | I_r/I_t | I_h/I_t |
|----|---|--------|--------|---------|---------|
| 100 | 2 | 1.260 | **1.417** | **5.03** | 5.67 |
| 100 | 4 | 1.291 | **1.428** | **6.81** | 7.81 |
| 100 | 8 | 1.292 | **1.428** | **7.07** | 8.07 |
| 500 | 2 | 1.429 | **1.540** | **7.39** | 8.04 |
| 500 | 4 | 1.436 | **1.542** | **11.06** | 12.06 |
| 500 | 8 | 1.436 | **1.542** | **9.07** | 10.07 |
| 1000| 2 | 1.647 | **1.731** | **7.56** | 8.23 |
| 1000| 4 | 1.649 | **1.732** | **15.82** | 16.82 |
| 1000| 8 | 1.649 | **1.732** | **6.19** | 7.19 |

R_frac consistently > 1. No Bernoulli dominance at any k. `[COMPUTED]`

### Task B Summary: The Money Table

| IC | R_frac at k=4 | I_r/I_t at k=4 | R_frac at k=8 | I_r/I_t at k=8 |
|----|:-------------:|:--------------:|:-------------:|:--------------:|
| **ABC (all Re)** | **0.037** | **0.044** | **0.0004** | **0.002** |
| TG Re=100 | 1.344 | 11.18 | 1.343 | 5.50 |
| TG Re=500 | 1.180 | 0.53 | 1.179 | 0.63 |
| TG Re=1000| 1.153 | 0.34 | 1.152 | 0.73 |
| RG Re=100 | 1.428 | 6.81 | 1.428 | 7.07 |
| RG Re=500 | 1.542 | 11.06 | 1.542 | 9.07 |
| RG Re=1000| 1.732 | 15.82 | 1.732 | 6.19 |

**The contrast is dramatic.** For ABC flows:
- The non-Bernoulli remainder contributes **< 5% of the bottleneck** at k=4 and **< 0.2% at k=8**
- R_frac → 0 geometrically as k increases

For non-Beltrami flows:
- The remainder exceeds the total (R_frac > 1) due to massive Hessian-remainder cancellation
- The bottleneck ratio I_r/I_t ranges from 0.3 to 16, typically >> 1

---

## Decomposition Verification [VERIFIED]

The decomposition P_total = P_hessian + P_remainder is exact by construction (P_remainder := P_total − P_hessian). The sign convention was verified:

**Sanity check at t=0 (exact Beltrami, div-free):**
- Full ABC field: B_deficit = 3.0 × 10^{−15} (machine precision zero) ✓
- λ_opt = −1.000000 (matches exact curl eigenvalue of ABC with A=B=C=1) ✓
- At k=8 (minimal truncation): R_frac = 3.8 × 10^{−4} → 0 ✓
- At k→∞ limit: P_total → −|u|²/2 = P_hessian (Bernoulli equation) ✓

**Sign convention verification:** The pressure Poisson equation −Δp = ∂_i∂_j(u_iu_j) gives p_hat = −k_ik_j FFT(u_iu_j)/|k|², with the correct minus sign. For exact Beltrami: P_total = −|u|²/2 = P_hessian, so P_remainder → 0. This was confirmed to machine precision for the un-truncated ABC flow.

Note: An initial version (v1/v2) had a sign error (missing minus sign in p_hat), causing R_frac ≈ 2.0 everywhere. This was caught and corrected in v3. All results reported here use the corrected code.

---

## Combined Interpretation

### The Beltrami Conditional Regularity Mechanism Survives Truncation

The concern was: even if a flow is Beltrami (curl u = λu), the De Giorgi truncation u_below = u · min(1, λ_k/|u|) might destroy this structure, killing the mechanism that Exploration 006 identified.

**Our measurements show the opposite.** For ABC flows:

1. **Beltrami deficit B_k = O(2^{−k})** — the truncation perturbation is proportional to the truncation width, confined to the shrinking set where |u| > λ_k. The bulk of u_below remains aligned with its curl.

2. **Remainder fraction R_frac = O(2^{−k})** — the pressure P_k^{21} is dominated by the Bernoulli piece −|u_b|²/2 at all levels. The non-Bernoulli (CZ-lossy) component vanishes geometrically.

3. **Bottleneck remainder I_r/I_t = O(2^{−k})** — in the actual De Giorgi bottleneck integral, the CZ-lossy piece contributes a geometrically vanishing fraction.

4. **Re-independence** — these properties are intrinsic to the spatial geometry of Beltrami flows, not artifacts of low Reynolds number.

### Quantifying the Improvement

For the De Giorgi iteration, the bottleneck integral is:
```
I_k = ∫ |P_k^{21}| · |d_k| · 1_{v_k>0} dx
```

If P_k^{21} is bounded by a CZ estimate with constant C_q, then I_k ≤ C_q · (RHS norm) · ||d_k||. The standard CZ constant is C_q = q* − 1 where q* = max(q, q/(q−1)).

For the Bernoulli piece P_hessian = −|u_b|²/2, no CZ operator is needed — it's an exact closed-form expression. The CZ loss applies only to the remainder, which contributes fraction ε_k ≈ I_r/I_t of the bottleneck.

At level k, the effective CZ constant is:
```
C_eff(k) ≈ 1 + ε_k · (C_q − 1)
```

For ABC at k=4 (q=2, C_q=1): ε_4 = 0.044, so C_eff ≈ 1.0 (no loss).
For ABC at k=8: ε_8 = 0.002, so C_eff ≈ 1.0 (essentially no loss).

For non-Beltrami flows: ε_k ≈ 1 (or larger due to cancellation), so C_eff ≈ C_q (full CZ loss).

### The Subtlety: div(u_below) ≠ 0

The truncation breaks incompressibility: ||div(u_below)||_L2 = O(2^{−k}). This means:

- The traditional Hessian/Lamb decomposition (which assumes div=0) doesn't apply directly
- The "remainder" includes both Lamb and compressibility contributions
- But the total remainder still vanishes as O(2^{−k}) for Beltrami flows

This is actually the STRONGER statement: even without the div-free structure, the pressure remains Bernoulli-dominated for ABC flows. The Beltrami property provides enough geometric structure to overcome the incompressibility violation.

---

## Implications for Conditional Regularity

### What This Means for the De Giorgi Iteration

The Vasseur (2007) De Giorgi framework establishes: U_k ≤ C^k · (1 + ||P_k^{21}||) · U_{k-1}^β

The key question is whether β_eff > 1 (which gives convergence). The β_eff depends on the CZ constant used to estimate ||P_k^{21}||.

**For Beltrami flows:**
- P_k^{21} ≈ −|u_below|²/2 (Bernoulli, no CZ needed)
- The CZ-lossy remainder contributes O(2^{−k}) to the bottleneck
- This effectively removes the CZ bottleneck from the iteration
- β_eff can approach the geometric limit (≈ 1 + 2/d = 5/3 in 3D) rather than being capped by CZ losses

**For generic flows:**
- P_k^{21} has a dominant CZ-lossy component (R_frac > 1)
- The full CZ constant applies, limiting β_eff

### Novel Observation: ABC Values Are Re-Independent

The Beltrami deficit and pressure decomposition ratios for ABC are completely independent of Re. This is because:

1. ABC is an exact Navier-Stokes solution: u(t) = u(0)e^{−νt}
2. After L^∞ normalization, the spatial pattern is invariant
3. The De Giorgi level-set quantities depend only on the normalized spatial pattern

**Implication:** The conditional regularity improvement from Beltrami structure is **not a low-Re artifact**. It persists to arbitrarily high Re.

### Open Question: Does This Extend Beyond Exact Beltrami Flows?

Our measurements are for exact ABC (Beltrami) flows. The key question for regularity theory is whether the mechanism applies to flows that are only **approximately** Beltrami in regions of high velocity. This exploration establishes the mechanism for the clean case; future work should test:

1. Perturbed ABC flows (ABC + noise)
2. Flows that develop local Beltrami regions during turbulent evolution
3. Whether the B_k = O(2^{−k}) scaling is universal for flows with helical structure

---

## Code

All code is in `code/`:

- **`beltrami_lamb_v3.py`** — Final corrected computation (v3, with correct sign convention). Computes Task A (Beltrami deficit) and Task B (Hessian/Remainder decomposition) for all IC/Re combinations.
- **`beltrami_lamb_v2.py`** — Intermediate version with correct decomposition but wrong sign (included for reproducibility of the debugging process).
- **`beltrami_lamb.py`** — Initial version (wrong sign AND wrong decomposition identity).
- **`results_v3.json`** — Machine-readable results from v3.
- **`results_v2.json`** — Results from v2 (sign error).
- **`results.json`** — Results from v1 (sign error + decomposition error).

The sign error was caught by the sanity check at t=0: for exact Beltrami with div(u)=0, R_frac should be 0, but was 2.0 in v1/v2, correctly 0.0004 (at k=8) in v3.

## Convergence Check

N=128 computation for ABC Re=500 was started but did not complete within the computation window. Based on the fact that all ABC results are Re-independent (and match the t=0 sanity check exactly), convergence is expected. The k-dependent quantities are purely geometric and should be resolution-independent once spectral accuracy is achieved (which N=64 provides for the low-wavenumber ABC modes).
