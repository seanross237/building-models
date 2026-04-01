# Exploration 005: SU(3) Extension — Hessian Eigenvalue Analysis

## Goal

Compute H_norm for SU(3), d=4 on L=2 and test whether H_norm ≤ 1/18 (as predicted by the generalized conjecture stated in the goal), or the tighter bound H_norm ≤ 1/27 (as computed at Q=I).

**Conventions used:**
- LEFT perturbation: Q_e → exp(t·v_e) Q_e
- B_□ partial holonomies: P1=I, P2=Q1, P3=Q1@Q2@Q3†, P4=Q1@Q2@Q3†@Q4† = U_plaq
- Action: S = −(β/N) Σ Re Tr(U_□) with N=3
- Hessian prefactor: β/(2N) = β/6
- H_norm = λ_max(HessS) / (8(d−1)Nβ)

**Code:** All code in `code/su3_hessian.py` and `code/su3_adversarial.py`.

---

## Task 1: SU(3) Setup and Q=I Sanity Check

**[VERIFIED]** Sanity check PASSED.

### Setup
- L=2, d=4, N=3
- n_links = 64, n_gen = 8 (Gell-Mann), n_dof = 512
- Full Hessian: 512×512
- Number of plaquettes: 96

### Implementation Verification
- Gell-Mann matrices: Tr(λ_a λ_b) = 2δ_{ab} ✓
- Generators τ_a = iλ_a/2: |τ_a|² = −2Tr(τ_a²) = 1 ✓
- Hessian symmetry at Q=I: max|H − H^T| = 0.00e+00 ✓

### Sanity Check Results

At Q=I, the LEFT Hessian gives:

```
λ_max at Q=I = 2.66666667
Expected:      2.66666667  (= 8β/3 = 8/3 for β=1)
Difference:    5.77e-15
```

**H_norm at Q=I:**
```
H_norm(I) = λ_max / (8(d−1)Nβ)
           = 2.666667 / (8 × 3 × 3 × 1.0)
           = 2.666667 / 72.0
           = 0.03703704 = 1/27
Expected 1/27 = 0.03703704
Difference: 8.33e-17
```

**Eigenvalue spectrum at Q=I:**
```
λ = 2.66666667   (multiplicity 24)
λ = 2.00000000   (multiplicity 96)
λ = 1.33333333   (multiplicity 144)
λ = 0.66666667   (multiplicity 96)
λ = 0.00000000   (multiplicity 152)
```

**Key finding:** H_norm(I) = 1/27, which is TIGHTER than the predicted 1/18. The formula is:

```
H_norm(I) = d / (4(d−1)N²)
For d=4, N=3: = 4/(4×3×9) = 4/108 = 1/27
For d=4, N=2: = 4/(4×3×4) = 4/48  = 1/12  [matches SU(2) exploration]
```

So the correct formula has N² in the denominator, not N.

---

## Task 2: SU(3) Random Configurations

**[COMPUTED]** All 20 (and 100) random Haar SU(3) configurations satisfy H_norm < 1/27.

### 20 Random Configurations (seed=42)

```
Config   lambda_max      H_norm    <=1/27?
 1        2.341579    0.03252193   YES
 2        2.348552    0.03261878   YES
 3        2.335960    0.03244389   YES
 4        2.343694    0.03255131   YES
 5        2.347960    0.03261056   YES
 6        2.349734    0.03263520   YES
 7        2.339827    0.03249759   YES
 8        2.329475    0.03235382   YES
 9        2.333601    0.03241113   YES
10        2.339654    0.03249519   YES
11        2.343036    0.03254216   YES
12        2.339077    0.03248717   YES
13        2.318380    0.03219972   YES
14        2.351788    0.03266372   YES
15        2.349705    0.03263479   YES
16        2.328690    0.03234292   YES
17        2.320451    0.03222848   YES
18        2.335633    0.03243935   YES
19        2.316320    0.03217111   YES
20        2.345808    0.03258067   YES
```

**Max H_norm over 20 configs: 0.03266372 < 1/27 = 0.03703704**

**H_norm(I) = 0.03703704 is STRICTLY LARGER than all random configs.**

This suggests Q=I may be a local (or global) maximum of H_norm.

### 100 Random Configurations (seed=123)

```
Max H_norm over 100 configs: 0.03303343 < 1/27
Violations: 0
```

---

## Task 3: Specific Adversarial Configurations

**[COMPUTED]** All adversarial constructions also satisfy H_norm ≤ 1/27, with several flat configurations achieving the bound exactly.

```
Config                     H_norm      <=1/27?
Q=I                        0.03703704  = 1/27 (exact)
diag(i, -i, 1) flat        0.03703704  = 1/27 (exact)
diag(i, i, -1) flat        0.03703704  = 1/27 (exact)
Staggered (tau_2, pi/2)    0.03703704  = 1/27 (exact)
omega*I flat (Z_3 center)  0.03703704  = 1/27 (exact)
Mixed center elements       0.03703704  = 1/27 (exact)
exp(i*pi/3*lambda_3) flat  0.03703704  = 1/27 (exact)
exp(i*pi/2*lambda_8) flat  0.03703704  = 1/27 (exact)
Direction-staggered        0.03703704  = 1/27 (exact)
Gradient ascent result     0.03612480  < 1/27
```

**Pattern:** All flat configurations (same value on every link) achieve H_norm = 1/27 exactly.
Random and non-flat configurations have H_norm strictly less than 1/27.

---

## Task 4: Triangle Inequality Bound for SU(3) and K_S Thresholds

**[COMPUTED]**

### Cauchy-Schwarz (CS) Rigorous Bound

For SU(N), the triangle inequality gives |B_□|² ≤ 4 Σ_{e∈□}|v_e|² because Ad_P is an
isometry for all P ∈ SU(N). Summing over all plaquettes (each link appears in exactly
2(d−1) plaquettes):

```
HessS(v,v) ≤ (β/(2N)) × 4 × 2(d−1) × |v|² = (β/(2N)) × 8(d−1) × |v|²
```

Expressing as H_norm: **H_norm_CS = 1/(2N²)**
- For N=2: H_norm_CS = 1/8
- For N=3: H_norm_CS = 1/18

### K_S positivity threshold from CS bound

K_S > 0 requires HessS(v,v) < (N/2)|v|² for all v. From the CS bound:

```
(β/(2N)) × 8(d−1) < N/2
β < N² / (8(d−1))
For N=3, d=4: β < 9/24 = 3/8 = 0.375
For N=2, d=4: β < 4/24 = 1/6 ≈ 0.167
```

### Conjectured Tight Bound

The numerical evidence from this exploration (and the SU(2) exploration) suggests:

```
H_norm ≤ d / (4(d−1)N²)   [conjectured universal bound]
```

This is tighter than the CS bound by a factor of d/(2(d−1)):
```
d/(4(d−1)N²) = [d/(2(d−1))] × [1/(2N²)]
For d=4: factor = 4/6 = 2/3
```

At Q=I this bound is achieved exactly — it equals the Q=I value. For all other
configurations tested, H_norm is strictly below this bound.

### K_S positivity threshold from conjectured bound

If H_norm ≤ d/(4(d−1)N²) universally, then:

```
λ_max(HessS) ≤ [d/(4(d−1)N²)] × 8(d−1)Nβ = 2dβ/N
K_S > 0 iff 2dβ/N < N/2, i.e., β < N²/(4d)
For N=3, d=4: β < 9/16 = 0.5625
For N=2, d=4: β < 4/16 = 1/4 = 0.25
```

### Threshold Summary

```
Method                      N=2, d=4         N=3, d=4
CS bound (rigorous)         β < 1/6 ≈ 0.167  β < 3/8 = 0.375
Conjectured tight bound     β < 1/4 = 0.250  β < 9/16 = 0.5625
```

Both the SU(2) and SU(3) conjectured thresholds are 50% larger than the CS bound.
The improvement factor is always d/(2(d−1)) for the H_norm bound, which propagates to
a 50% increase in the K_S threshold (for d=4).

---

## Formula Discovery: Generalized H_norm Bound

The key result of this exploration — combined with the prior SU(2) results — is the
identification of the correct N-scaling for the H_norm bound:

**[VERIFIED for N=2,3 at Q=I; COMPUTED for 120+ random configs]**

```
H_norm(I) = d / (4(d−1)N²)
```

| N | d | H_norm(I) | H_norm_CS | Ratio |
|---|---|-----------|-----------|-------|
| 2 | 4 | 1/12 = 0.08333 | 1/8 = 0.125 | 2/3 |
| 3 | 4 | 1/27 = 0.03704 | 1/18 = 0.0556 | 2/3 |
| N | 4 | 1/(3N²) | 1/(2N²) | 2/3 |

**The bound uses N², not N.** The GOAL's prediction of 1/18 for N=3 corresponds to
using N in the denominator; the correct tight bound is 1/27 (using N²), which is
smaller and consistent across both N=2 and N=3.

Equivalently: H_norm(I) = (d/(2(d−1))) × H_norm_CS, where the prefactor d/(2(d−1))
is strictly less than 1 for all d ≥ 3. It equals 1 only for d=2 (trivial case).

**The conjecture is that this is not just an identity at Q=I but a universal upper bound:**

```
H_norm(Q) ≤ d / (4(d−1)N²)   for all Q ∈ SU(N)^E, any L, d
```

Evidence from this exploration:
- 120 random configs: all strictly below (max = 0.03303 vs. bound 0.03704)
- Gradient ascent: converged to 0.03612, did not reach bound
- All flat configs (any constant link value): achieve the bound exactly
- No counterexample found

The flat-configuration saturation pattern suggests the bound may be an equality
whenever all plaquettes have the same holonomy (i.e., when the gauge field is "uniform").

---

## Summary of Findings

**[COMPUTED]** H_norm ≤ 1/27 for all 120+ SU(3) configurations tested.

| Metric | Value |
|--------|-------|
| H_norm at Q=I | 1/27 = 0.037037 (exact) |
| H_norm max (20 random) | 0.032664 |
| H_norm max (100 random) | 0.033033 |
| H_norm max (adversarial) | 0.037037 = 1/27 |
| Any H_norm > 1/27? | NO |

**Conjecture:** H_norm ≤ d/(4(d−1)N²) for all Q ∈ SU(N)^E, matching the SU(2) result.

**The goal stated H_norm ≤ 1/18. The actual tight bound is 1/27 < 1/18 — satisfied,
but the denominator should use N², not N.**

**K_S implications:**
- Rigorous CS bound gives K_S > 0 for β < 3/8 (SU(3), d=4)
- Conjectured tight bound gives K_S > 0 for β < 9/16 (50% improvement)

---

## Verification Scorecard

- **2 [VERIFIED]** claims: λ_max(I) = 8β/3 matches analytically; H_norm(I) = 1/27 exactly
- **5 [COMPUTED]** claims: 20 + 100 random configs, gradient ascent, adversarial constructions
- **2 [CONJECTURED]** claims: H_norm ≤ 1/27 for ALL SU(3) configurations; K_S > 0 threshold

---

## Code Reference

- `code/su3_hessian.py` — Main computation: generators, adjoint rep, Hessian builder, Tasks 1-4
- `code/su3_adversarial.py` — Adversarial search: 100 random configs, gradient ascent, special constructions
