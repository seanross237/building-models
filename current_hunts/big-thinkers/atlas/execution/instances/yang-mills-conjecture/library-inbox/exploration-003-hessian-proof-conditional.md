# Exploration 003: Prove the Hessian Eigenvalue Bound

## Goal
Prove λ_max(HessS(Q)) ≤ 4d for all Q ∈ SU(2)^E (β=1, N=2, iσ_a basis), verify the SZZ mass gap threshold, and characterize obstructions.

## Stage 1: SZZ Mass Gap Threshold — VERIFIED [CHECKED]

**SZZ conventions** (arXiv:2204.12737):
- Metric: ⟨X,Y⟩ = -Tr(XY) on su(N), giving |X|² = 2|c|² in our iσ_a coords
- Action: S_SZZ = Nβ_SZZ Σ Re Tr(Q_p). Related to ours by β_ours = N² β_SZZ = 4β_SZZ for SU(2)
- Ricci: Ric(X,X) = (N/2)|X|²_SZZ = 2|c|² for SU(2) per edge

**Bakry-Émery condition**: Ric + Hess(V) ≥ K g, where V = S (our action), Hess(V) = H (our Hessian).

In our coordinates: 2δ_{ij} + H_{ij} ≥ (K/2)(½)δ_{ij}, giving **K = 2 + λ_min(H)** (in |v|²_SZZ metric: K = 1 + λ_min(H)/2). Mass gap iff K > 0 iff **λ_min(H) > -2** for all Q.

**SZZ result** (Lemma 4.1): Gershgorin-type bound |H(v,v)| ≤ 8(d-1)|v|² per edge. This gives:
- d=4: spectral radius ≤ 24 → β_ours < 2/24 = **1/12 ≈ 0.083**

**Our conjecture**: λ_max(H) ≤ 4d = 16 (at flat, β=1, N=2). If this also bounds |λ_min|:
- d=4: spectral radius ≤ 16 → β_ours < 2/16 = **1/8 = 0.125** (1.5× improvement over SZZ)

**Normalization correction**: The GOAL claims bound 4d·(β/N) = 8 for d=4, β=1, N=2. The actual flat max eigenvalue is **4d = 16** in iσ_a coords (= 8d·β/N in general). The GOAL has a factor-of-2 error.

## Stage 2: Proof Attempts

### Attempt 1: Gershgorin — FAILS [COMPUTED]
At flat d=4: diagonal=6, off-diag row sum=18, Gershgorin=24. Target=16. **50% overcount.**
Random configs: ratio up to 1.78×. Structurally too loose.

### Attempt 2: Per-plaquette — FAILS for d ≥ 3 [COMPUTED]
Per-plaquette Hessian max eigenvalue = 4.0 (at flat). Edge sharing gives factor 2(d-1).
Total: 8(d-1) = 24 for d=4. Same as Gershgorin. Works only for d=2 (tight at 8).
Per-plaquette Hessians are NOT PSD at random Q (500/500 non-PSD).

### Attempt 3: Fourier Analysis at Flat — KEY RESULT [VERIFIED]

At flat, H is translation-invariant and color-diagonal. Fourier block at wavevector k:

**K̂(k) ~ (8β/N) [|s(k)|² I_d − s(k)s(k)ᵀ]**   where s_μ(k) = sin(πk_μ/L)

Eigenvalues: **(8β/N)|s|²** (multiplicity d−1) and **0** (multiplicity 1).

**λ_max = (8β/N)d = 4d** for β=1, N=2. Achieved at k=(L/2,...,L/2) (staggered mode) when L even.

Verified for d=2,3,4, L=2,3,4. Formula exact.

### Attempt 4: D + C Decomposition — CONDITIONAL PROOF [COMPUTED]

**The key decomposition**: H(Q) = D(Q) + C(Q) where:
- D = self-term (diagonal): D_{(e,a),(e,a)} = (β/N) Σ_{□∋e} Re Tr(U_□)
- C = cross-term (off-block-diagonal between different edges)

**Proven bounds**:
1. **D_max(Q) ≤ 2(d-1)** since Re Tr(U_□) ≤ 2 for SU(2) [VERIFIED]
2. **D_min(Q) ≥ -2(d-1)** since Re Tr(U_□) ≥ -2 [VERIFIED]

**Flat connection values**:
- D_flat = 2(d-1) I (scalar), λ_max(D) = 2(d-1)
- λ_max(C_flat) = 2(d+1), λ_min(C_flat) = -2(d-1)
- Check: 2(d-1) + 2(d+1) = **4d** ✓ (exact decomposition of λ_max(H))

**Numerical evidence** (200–500 configs per d):

| d | max(D) | max(C_lmax) | flat C_lmax | max(D+C_lmax) | 4d |
|---|--------|-------------|-------------|---------------|-----|
| 2 | 1.94   | 4.64        | 6.00        | 5.83          | 8   |
| 3 | 3.50   | 6.63        | 8.00        | 9.08          | 12  |
| 4 | 4.96   | 7.59        | 10.00       | 12.11         | 16  |

**λ_max(C(Q)) ≤ λ_max(C_flat) for ALL tested Q** ✓

If provable: λ_max(H) ≤ D_max + C_max ≤ 2(d-1) + 2(d+1) = 4d. **QED (conditional on C bound)**

### Cross-term Kernel Bound — PROVED [VERIFIED]

**Theorem**: For any M, N ∈ SU(2), the 3×3 matrix F_{ab} = Re Tr(iσ_a M iσ_b N) satisfies **||F||_op ≤ 2**.

**Proof**: For unit u, v ∈ ℝ³, define U = û·iσ, V = v̂·iσ ∈ SU(2) (quarter-turns: U†U = I, det U = 1). Then Σ u_a F_{ab} v_b = Re Tr(UMVN). Since UMVN ∈ SU(2): |Tr(UMVN)| ≤ 2. ∎

**Empirical**: ||F||_op = **2.000000 exactly** for all 20000 random (M,N) pairs tested. The norm is CONSTANT on SU(2)², not just bounded.

## Stage 3: Numerical Support [COMPUTED]

### Eigenvalue survey (d=4, L=2, β=1, N=2):
- **λ_max**: flat = 16.0 (= 4d), random max = 8.68 (54% of flat)
- **λ_min**: flat = 0.0, random min = -8.73
- Spectral radius max from random: 8.73 (55% of 4d)
- **λ_max ≤ 4d**: YES for all configs tested ✓
- **|λ_min| ≤ 4d**: YES for all configs tested ✓

### Perturbation from flat (d=4, 50 random directions each):
| ε   | λ_max        | λ_min   |
|-----|-------------|---------|
| 0.0 | 16.00 (1.000) | 0.00   |
| 0.05| 15.89 (0.993) | -0.99  |
| 0.10| 15.56 (0.973) | -2.13  |
| 0.20| 14.32 (0.895) | -4.47  |
| 0.50| 10.23 (0.639) | -8.59  |
| 1.00| 8.72 (0.545)  | -8.50  |
| 2.00| 8.34 (0.521)  | -8.58  |

λ_max **monotonically decreases** from flat. λ_min saturates at ~-8.5 (about 4d/2).

## Stage 4: Proof Status and Obstruction Report

### What is PROVED:
1. **Fourier formula at flat**: λ_max(H_flat) = (8β/N)d = 4d [VERIFIED]
2. **Cross-term kernel bound**: ||F_{ab}||_op ≤ 2 [VERIFIED — algebraic proof]
3. **Self-term monotonicity**: D(Q) ≤ D_flat in Loewner order [VERIFIED]
4. **SZZ threshold conversion**: our β_ours = N²β_SZZ [CHECKED]

### What is CONDITIONALLY proved:
5. **λ_max(H(Q)) ≤ 4d for all Q** — requires proving ||C(Q)||_op ≤ 2(d+1) [COMPUTED, not proved]

### The OBSTRUCTION to a complete proof:
The missing lemma: **"Cross-term decoherence"** — show that the cross-term operator norm ||C(Q)||_op is maximized at flat connections.

**Why it should be true**: At flat, all cross-term 3×3 kernels are F = -2I₃ (proportional to identity, maximally coherent in color space). C_flat = (2β/N) A ⊗ I₃ where A is the spatial cross-term matrix. At non-flat Q, each kernel F^{pq} becomes a different 3×3 matrix with ||F||=2 but arbitrary orientation. The color "misalignment" between different plaquette pairs reduces the total norm.

**Formal statement needed**: For C(Q) = Σ (spatial coefficients) ⊗ (3×3 color kernels), with each kernel having ||F||_op = 2 and the spatial structure fixed by the lattice geometry, the operator norm is maximized when all color kernels are proportional to I₃.

This is related to: matrix-valued concentration inequalities, operator-valued Cauchy-Schwarz, or perhaps a direct SO(3)-averaging argument (since the color kernels are related by adjoint rotations).

### Mass gap improvement if proved:
| Method | Bound | β_ours threshold (d=4) | Standard β_lat |
|--------|-------|----------------------|----------------|
| SZZ Gershgorin | 24 | 1/12 ≈ 0.083 | 1/3 ≈ 0.33 |
| CNS vertex | 12 | 1/6 ≈ 0.167 | 2/3 ≈ 0.67 |
| **Our conjecture** | **16** | **1/8 = 0.125** | **1/2 = 0.50** |
| Deconfinement | — | ~2.3 | ~2.3 |
