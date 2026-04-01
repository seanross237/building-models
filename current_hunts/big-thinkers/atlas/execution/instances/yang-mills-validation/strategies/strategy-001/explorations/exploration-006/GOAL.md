# Exploration 006: d=5 Anomaly Resolution

## Mission Context

The prior mission found that for d=5, the staggered mode v_{x,μ} = (−1)^{|x|+μ} is NOT the maximum eigenvector of M(I). They found λ_max = 5β (not the staggered mode's 4.8β). This needs explanation: is d=4 special, or does the proof carry through for all d?

## CRITICAL CONVENTION WARNING

**Use the LEFT perturbation B_□ formula:**
```
P3 = Q1 @ Q2 @ Q3.conj().T           # INCLUDES Q3 inverse
P4 = Q1 @ Q2 @ Q3.conj().T @ Q4.conj().T  # = U_plaq
```

**Convention:** S = −(β/N) Σ Re Tr(U_□), |A|² = −2Tr(A²), N=2.

## Goal

For d=3,4,5,6, compute the exact Hessian eigenspectrum at Q=I via Fourier analysis and determine whether the proof of β < 1/6 (or its analog) works in each dimension.

## Tasks

### Task 1: Fourier Analysis of M(I) for General d
At Q=I, M(Q) = M(I) = Σ_□ B_□^T B_□ where B_□ = discrete curl.

In Fourier space with momentum k ∈ {0, 1, ..., L-1}^d (using k_μ = 2πn_μ/L), the operator decomposes as:

K(k) = A(k)·I_d − B(k)·J_d

where J_d is the d×d all-ones matrix, and:
- A(k) = Σ_μ |c_μ|² = Σ_μ 4sin²(πk_μ/L)
- B(k) = Σ_{μ<ν} |c_μ|²|c_ν|² / ... (this needs careful derivation)

Actually, the exact formula from the prior mission:
- The momentum-space operator at k has spatial eigenvalues λ_j(k) for j=1,...,d
- At k=(π,...,π): λ_max = 4d (for direction vectors orthogonal to (1,...,1))

For each d, compute:
1. λ_max(M(I)) by building the full Hessian on L=2 and diagonalizing
2. The staggered mode eigenvalue (should be 4d for even d)
3. The TRUE maximum eigenvalue and its eigenvector structure
4. For d=5: identify the non-staggered maximum eigenvector

### Task 2: Compute for d=3,4,5,6 on L=2
For each dimension:
- Build full Hessian at Q=I (SU(2), L=2)
- d=3: n_links = 3×2³ = 24, n_dof = 72
- d=4: n_links = 4×2⁴ = 64, n_dof = 192
- d=5: n_links = 5×2⁵ = 160, n_dof = 480
- d=6: n_links = 6×2⁶ = 384, n_dof = 1152

Compute:
1. λ_max(H) for each d
2. H_norm(I) = λ_max(H) / (8(d-1)Nβ)
3. The triangle inequality bound: HessS ≤ (β/(2N))×4×2(d-1) = 4(d-1)β/N
4. K_S > 0 threshold: β < N²/(8(d-1)) = 1/(2(d-1)) for N=2

Results table:
| d | λ_max(H) | H_norm(I) | Staggered eigenvalue | CS bound | β threshold |
|---|----------|-----------|---------------------|----------|------------|
| 3 | ? | ? | ? | ? | ? |
| 4 | 4β | 1/12 | 4β | 6β | 1/6 |
| 5 | ? | ? | ? | ? | ? |
| 6 | ? | ? | ? | ? | ? |

### Task 3: d=5 Maximum Eigenvector Analysis
For d=5 at Q=I:
1. Find the maximum eigenvector(s)
2. Describe their structure: are they staggered? What is the spatial structure?
3. Compare with the staggered mode: how much larger is λ_max vs the staggered eigenvalue?
4. Does the formula H_norm = ⌈d/2⌉⌊d/2⌋/(N²d(d-1)) from the prior mission give the correct value for d=5?

### Task 4: Does the Triangle Inequality Proof Generalize?
The β < 1/6 proof uses:
1. CS: |B_□|² ≤ 4 Σ|v_e|² (dimension-independent)
2. Link count: each link in 2(d-1) plaquettes (dimension-dependent)
3. Result: HessS ≤ (β/(2N))×4×2(d-1)×|v|² = 4(d-1)β|v|²/N

For general d, N=2: β < N/(2×4(d-1)/N) = N²/(8(d-1)) = 1/(2(d-1))
- d=3: β < 1/4
- d=4: β < 1/6
- d=5: β < 1/8
- d=6: β < 1/10

The triangle inequality proof works for ALL d. But is it tight for all d?

## Success Criteria
- [ ] λ_max computed for d=3,4,5,6 at Q=I
- [ ] Results table filled in
- [ ] d=5 anomaly explained: what eigenvector achieves λ_max?
- [ ] Triangle inequality generalization verified

## What to Write
Write REPORT.md and REPORT-SUMMARY.md. Put all code in code/ subdirectory.
