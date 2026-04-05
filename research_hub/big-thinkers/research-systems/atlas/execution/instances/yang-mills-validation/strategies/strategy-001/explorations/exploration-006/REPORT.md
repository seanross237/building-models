# Exploration 006: d=5 Anomaly Resolution — REPORT

## Goal
For d=3,4,5,6, compute the exact Hessian eigenspectrum at Q=I via numerical Hessian construction, explain why d=5 gives λ_max > staggered-mode value, and verify whether the triangle inequality proof generalizes to all dimensions.

## Convention
- S = −(β/N) Σ Re Tr(U_□), N=2, SU(2)
- LEFT perturbation: P3 = Q1@Q2@Q3†, P4 = Q1@Q2@Q3†@Q4† = U_plaq
- HessS(v,v) = (β/(2N)) Σ_□ |B_□(v)|² where B_□ = discrete curl
- M(I) = Σ_□ b_□ b_□ᵀ (geometric/scalar Hessian at Q=I)
- λ_max(H) = (β/(2N)) × λ_max(M(I))
- H_norm = λ_max(H) / (8(d−1)Nβ)

---

## Section 1: Sanity Check (d=4, Q=I)

**Expected from E003:** λ_max(H) = 4β at Q=I for d=4, N=2.

**Result:** `[VERIFIED]`

```
lambda_max(M)   = 16.0000000000
lambda_max(H)   = 4.0000000000
Expected = 4*beta = 4.0
Match: True

Staggered mode H eigenvalue = 4.0000000000
Staggered is eigvec: True
```

The sanity check passes. Staggered mode IS an eigenvector with eigenvalue 4β for d=4. Consistent with E003.

---

## Section 2: Dimension Scan d=3,4,5,6

All computed at Q=I on L=2 lattice. Code: `code/hessian_dimension_scan.py`.

### Key Result: λ_max(M(I)) = 4d for ALL d `[VERIFIED]`

| d | n_links | λ_max(M) | λ_max(H)/β | Stag eig/β | H_norm | CS threshold β < |
|---|---------|----------|------------|------------|--------|------------------|
| 3 | 24      | 12.0000  | 3.000000   | 2.666667   | 0.093750 | 0.250000 = 1/4 |
| 4 | 64      | 16.0000  | 4.000000   | 4.000000   | 0.083333 | 0.166667 = 1/6 |
| 5 | 160     | 20.0000  | 5.000000   | 4.800000   | 0.078125 | 0.125000 = 1/8 |
| 6 | 384     | 24.0000  | 6.000000   | 6.000000   | 0.075000 | 0.100000 = 1/10 |

### Formulas `[COMPUTED]`

```
lambda_max(M(I)) = 4d
lambda_max(H)    = (beta/(2N)) * 4d = d*beta   [for N=2]
H_norm(I)        = d*beta / (8*(d-1)*N*beta) = d / (16*(d-1))   [for N=2]
```

Explicit H_norm values:
- d=3: H_norm = 3/32 = 0.09375
- d=4: H_norm = 4/48 = 1/12 ≈ 0.08333 ✓ (matches E003)
- d=5: H_norm = 5/64 = 0.078125
- d=6: H_norm = 6/80 = 3/40 = 0.075

### Eigenvalue Multiplicities at Q=I `[COMPUTED]`

The eigenvalues of M(I) are exactly 4k for k=0,1,...,d. The multiplicity of the maximum eigenvalue 4d is exactly d−1. The full spectrum on L=2 has a Pascal-triangle structure.

| d | Distinct eigenvalues of M(I) (with multiplicities) |
|---|-----------------------------------------------------|
| 3 | 12(×2), 8(×6), 4(×6), 0(×10) |
| 4 | 16(×3), 12(×12), 8(×18), 4(×12), 0(×19) |
| 5 | 20(×4), 16(×20), 12(×40), 8(×40), 4(×20), 0(×36) |
| 6 | 24(×5), 20(×30), 16(×75), 12(×100), 8(×75), 4(×30), 0(×69) |

Multiplicity of λ_max = d−1 in all cases.

### Note on Prior Mission Formula

The prior mission conjectured H_norm = ⌈d/2⌉⌊d/2⌋/(N²d(d-1)):
- This formula equals d/(4(d-1)N²) only for **even d** (where ⌈d/2⌉⌊d/2⌋ = d²/4)
- For **odd d** it gives the staggered mode eigenvalue, not the true maximum
- The correct formula for H_norm(I) for ALL d is **d/(4(d-1)N²) = d/(16(d-1)) for N=2**

---

## Section 3: d=5 Maximum Eigenvector Analysis

### The d=5 "Anomaly" Explained `[VERIFIED]`

The maximum eigenvectors of M(I) for all d have the form:

```
v_{x,mu} = c_mu * (-1)^|x|   where |x| = sum_i x_i
```

with the Rayleigh quotient formula:

```
Q(c) = 4 * sum_{mu<nu} (c_mu - c_nu)^2 / sum_mu c_mu^2
     = 4 * [d*|c|^2 - (c·1)^2] / |c|^2
     = 4 * [d - (c·1)^2 / |c|^2]
```

**Maximum:** Q = 4d, achieved when Σ_μ c_μ = 0 (i.e., c ⊥ (1,...,1)).

**The staggered mode** has direction vector c_μ = (−1)^μ.

Σ_{μ=0}^{d-1} (−1)^μ = (1 − (−1)^d) / 2:
- **Even d:** sum = 0, so staggered mode achieves maximum Q = 4d ✓ (d=4, d=6)
- **Odd d:** sum = 1, so staggered mode gives Q = 4(d² − 1)/d < 4d ✗ (d=3, d=5)

**For d=5 specifically:**
- Staggered c = (1,−1,1,−1,1), sum = 1
- Q_stag = 4 × (25 − 1)/5 = 4 × 24/5 = 96/5 = 19.2 → H eigenvalue 4.8β
- Maximum at c = (4,−1,−1,−1,−1) (sum=0): Q = 20 → H eigenvalue 5β
- The max eigenspace is 4-dimensional (d−1 = 4 independent modes with Σ c_μ = 0)

**Verification:** Mode v_{x,μ} = c_μ(−1)^|x| with c=(4,−1,−1,−1,−1) is a confirmed eigenvector with Rayleigh quotient = 20 `[VERIFIED]` (residual < 10⁻⁸).

### Why d=4 Is Special

For d=4, the alternating sequence (1,−1,1,−1) sums to zero, so the staggered mode happens to lie in the maximum eigenspace. For d=5, (1,−1,1,−1,1) sums to 1, so the staggered mode falls short of the maximum by exactly 4/5 of a unit in Rayleigh quotient.

This is **not a physical anomaly** — it's a combinatorial fact about the parity of d.

---

## Section 4: Triangle Inequality Proof Generalization

### Proof Sketch for General d `[CONJECTURED: proof valid; threshold analytically derived]`

At Q ≠ I, the LEFT perturbation B_□(v) formula is:
```
B_□(v) = Ad_{P1}v_{e1} + Ad_{P2}v_{e2} − Ad_{P3}v_{e3} − Ad_{P4}v_{e4}
```
where P_i are partial holonomies.

**Step 1 (CS bound):** Since Ad_P is an isometry for any P ∈ SU(N):
```
|B_□(v)|² ≤ (|v_{e1}| + |v_{e2}| + |v_{e3}| + |v_{e4}|)² ≤ 4(|v_{e1}|² + ... + |v_{e4}|²)
```

**Step 2 (link counting):** Each link in 2(d−1) plaquettes:
```
Σ_□ |B_□(v)|² ≤ 4 × 2(d−1) × |v|² = 8(d−1)|v|²
```

**Step 3 (Hessian bound):**
```
HessS(v,v) = (β/(2N)) Σ_□ |B_□(v)|² ≤ (β/(2N)) × 8(d−1) × |v|² = 4(d−1)β|v|²/N
```

**Step 4 (K_S > 0 condition):** Requires HessS < (N/2)|v|² (Bochner condition):
```
4(d−1)β/N < N/2  ⟹  β < N²/(8(d−1))
```

**Thresholds by dimension for N=2:**
| d | β threshold | Fraction |
|---|-------------|----------|
| 3 | 1/4 = 0.250 | |
| 4 | 1/6 = 0.167 | ← from E003 |
| 5 | 1/8 = 0.125 | |
| 6 | 1/10 = 0.100| |
| d | 1/(2(d-1)) | |

**The proof is structure-identical for all d ≥ 2.** Only the threshold changes.

### Tightness of the CS Bound

At Q=I, the ratio λ_max(H) / (CS bound) = dβ / (2(d−1)β) = d/(2(d−1)):

| d | λ_max(H) | CS bound | ratio | H_norm × 8(d-1)Nβ = λ_max |
|---|----------|----------|-------|---------------------------|
| 3 | 3β | 4β | 0.75 | ✓ |
| 4 | 4β | 6β | 0.67 | ✓ |
| 5 | 5β | 8β | 0.625 | ✓ |
| 6 | 6β | 10β | 0.60 | ✓ |

The CS bound is NOT tight (bound is not saturated at Q=I) and the ratio decreases toward 1/2 as d→∞. This means the triangle inequality proof has increasing slack in higher dimensions.

### Does λ_max(M) = 4d Hold for Q ≠ I?

The proof that K_S > 0 only needs the CS bound (valid for all Q), not the exact λ_max. The question of whether λ_max(M(Q)) = 4d for all Q (not just Q=I) is the content of the main Conjecture 1. That conjecture was verified for d=4 by E003 on random configurations. For d≠4, this remains to be tested.

---

## Summary of All Results

### Complete Results Table `[COMPUTED]`

| d | λ_max(M(I)) | λ_max(H)/β | Stag eig/β | H_norm | β threshold |
|---|-------------|------------|------------|--------|-------------|
| 3 | 12 = 4×3    | 3.000      | 2.667      | 3/32   | 1/4 = 0.250 |
| 4 | 16 = 4×4    | 4.000      | 4.000      | 1/12   | 1/6 = 0.167 |
| 5 | 20 = 4×5    | 5.000      | 4.800      | 5/64   | 1/8 = 0.125 |
| 6 | 24 = 4×6    | 6.000      | 6.000      | 3/40   | 1/10 = 0.100|

### Analytical Formulas `[VERIFIED for d=3,4,5,6]`

```
lambda_max(M(I)) = 4d                        [all d]
lambda_max(H)    = d*beta/1 for N=2          [= d*beta]
H_norm(I)        = d / (16*(d-1))            [N=2, all d]
stag eigenvalue  = 4d*beta   for even d       [staggered IS max eigvec]
                 = 4(d^2-1)*beta/d  for odd d [staggered below max]
beta_threshold   = N^2 / (8*(d-1))           [for K_S > 0 via CS bound]
                 = 1 / (2*(d-1))  for N=2
```

### d=5 Anomaly Resolution `[VERIFIED]`

The d=5 maximum eigenvector has form v_{x,μ} = c_μ(−1)^|x| with Σ_μ c_μ = 0 (e.g. c = (4,−1,−1,−1,−1)). The staggered mode has Σ c_μ = 1 ≠ 0, putting it in a sublevel set with eigenvalue 4.8β instead of 5β. This is a consequence of the alternating sum Σ(−1)^μ being nonzero for odd d.

---

## Code Files

- `code/sanity_check.py` — Sanity check: λ_max = 4β at Q=I for d=4 ✓
- `code/hessian_dimension_scan.py` — Full dimension scan d=3,4,5,6
- `code/eigvec_analysis.py` — Eigenvector structure analysis and formula verification

All code uses LEFT perturbation convention with β=1, N=2, L=2.
