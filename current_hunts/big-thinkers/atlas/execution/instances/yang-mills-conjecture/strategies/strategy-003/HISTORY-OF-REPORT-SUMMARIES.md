# Exploration History

## Exploration 001: Counterexample Verification + SZZ Framework Clarification

### Goal
Verify E007's counterexample (λ_max(M(Q)) ≈ 16.08) and clarify the SZZ Hessian relationship.

### Outcome: Conjecture 1 is FALSE, but the mass gap argument survives

**Conjecture 1 (λ_max(M(Q)) ≤ 16) is definitively false.** The clean counterexample Q_e = iσ₃ (all links) gives λ_max(M) = 24 exactly. This is a flat connection with Z₂ holonomy (-I around each torus cycle). Even random configs exceed 16 in 21% of cases.

**However, the Hessian of S is NOT (β/2N)M.** There is a large curvature correction. At Q = iσ₃, the full 192×192 Hessian (computed by finite differences) has λ_max = 4.0 = (β/2N)×16, even though (β/2N)M has λ_max = 6.0. The correction exactly compensates.

**The correct proof target is the Hessian, not M.** Numerical evidence suggests λ_max(HessS) ≤ (β/2N)×4d for all Q — verified at Q=I, Q=iσ₃, and random Q (where it's much smaller).

### Verification Scorecard
- **VERIFIED:** 5 (λ_max=16 at Q=I, λ_max=24 at Q=iσ₃, eigenvector construction, Hessian spectrum at iσ₃, gauge mode orthogonality)
- **COMPUTED:** 4 (1000-config random survey, gradient ascent, Stage 2 element comparison, staggered decomposition)
- **CONJECTURED:** 1 (λ_max(HessS) ≤ (β/2N)×4d universally)

### Key Findings
- sup λ_max(M) = 24 = 6d (not 4d=16), achieved at Z₂ flat connections
- The modes exceeding 16 in M are "gauge-lifted" modes: gauge zero-modes at Q=I that become physical at non-trivial flat connections, but remain in the Hessian nullspace
- At random Q: v^T HessS v / (β/2N) v^T M v ≈ 0.02–0.09 (Hessian far below M away from flat connections)
- Diagonal Hessian blocks: HessS_{ee} = (β/4N) Σ_{□∋e} Re Tr(U_□) × I₃
- Off-diagonal Hessian has non-trivial color mixing via Im Tr(σ_a U_□)
- Revised Conjecture: λ_max(HessS(Q)) ≤ (β/2N) × 4d for all Q

## Exploration 002: Derive the Wilson Action Hessian Analytically

### Goal
Derive the explicit analytical formula for the Hessian of the lattice Wilson action for SU(2), verify it, and characterize the correction C(Q) = M(Q) - (2N/β)HessS(Q).

### Outcome: SUCCESS

**The formula:**
- Self-terms: H[(e,a),(e,b)] = (β/N) δ_{ab} Σ_{□∋e} Re Tr(U_□) — diagonal in color, proportional to sum of plaquette traces
- Cross-terms: H[(ep,a),(eq,b)] = -(β/N) sp sq Re Tr(Lp iσa mid iσb Rq) — transported basis elements

**Key findings:**
1. At flat connections (U_□ = I): HessS = (β/2N)M exactly, C = 0
2. Self-term correction C_self ≥ 0 always (from Re Tr(U) ≤ 2 for SU(2))
3. Total correction C is NOT PSD — but max eigenvalue of HessS is still bounded
4. λ_max(HessS(Q)) ≤ 4d (in iσ_a basis), achieved at flat connections. Gradient ascent in d=4 reached only 85% of bound.
5. E001's claim that HessS ≠ (β/2N)M at Q=iσ₃ was a normalization error — both are flat connections where equality is exact.

### Verification
- 4 VERIFIED (key identity, self-term formula, flat-connection equality, C_self ≥ 0)
- 2 COMPUTED (FD cross-check 12 configs max rel err < 1.4e-6, eigenvalue bound scan)
- 1 CONJECTURED (global max eigenvalue ≤ 4d)

### Proof gaps
- No analytical proof that cross-terms cannot amplify eigenvalue beyond flat bound
- Cross-term kernel has bounded operator norm but bound isn't tight enough for direct proof
- Proving the bound likely requires Fourier analysis of the Hessian at flat connections plus perturbative argument

## Exploration 003: Prove the Hessian Eigenvalue Bound

### Goal
Prove λ_max(HessS(Q)) ≤ 4d for all Q. Three proof approaches + SZZ threshold verification.

### Outcome: CONDITIONAL PROOF — one lemma away

**Proof via D+C decomposition:** H = D(self-term) + C(cross-term). D_max ≤ 2(d-1) [PROVED]. λ_max(C_flat) = 2(d+1) [VERIFIED]. Sum = 4d ✓. λ_max(C(Q)) ≤ 2(d+1) for ALL tested configs [COMPUTED, 200-1000 per d]. MISSING: proof of "cross-term decoherence lemma" (||C(Q)|| ≤ ||C_flat)||).

**Key algebraic result:** Cross-term kernel ||F_{ab}||_op = 2 EXACTLY for all SU(2) — proved via û·iσ ∈ SU(2) ⟹ |Tr(UMVN)| ≤ 2.

**SZZ mass gap threshold:** Our β = N²β_SZZ = 4β_SZZ for SU(2). The Bakry-Émery condition gives K = 2 + λ_min(H). Mass gap iff K > 0.

**Mass gap improvement table:**
| Method | Bound | β threshold (d=4) |
|--------|-------|-------------------|
| SZZ Gershgorin | 24 | 1/12 |
| Our λ_max conjecture | 16 | 1/8 |
| If |λ_min| ≤ 2d | 8 | 1/4 |

**Critical discovery:** The mass gap depends on |λ_min(HessS)|, not λ_max. At flat connections λ_min = 0. Away from flat, λ_min goes to ~-8.5 (d=4). If |λ_min| ≤ 2d, mass gap at β < 1/4.

**Proof approaches that FAILED:**
- Gershgorin: 50% overcount (gives 24 not 16)
- Per-plaquette: same as Gershgorin for d ≥ 3

**What WORKED:**
- Fourier analysis at flat: K̂(k) = (8β/N)[|s|²I_d - s·sᵀ], eigenvalue (8β/N)|s|² with max 4d
- D+C decomposition: conditional on decoherence lemma

## Exploration 004: Characterize λ_min(HessS) and Prove Decoherence Lemma

### Goal
Find sup|λ_min(HessS(Q))| by adversarial optimization to determine mass gap threshold β < 2/sup|λ_min|.

### Outcome: PARTIALLY SUCCESSFUL — empirical value found; β < 1/4 ruled out

**Empirical inf λ_min = -14.734** (d=4, L=2), determined to ±0.05 by adversarial optimization with 35+ gradient descent starts. The extremal config is a GD-optimized anti-instanton: Q_μ = iσ_{a(μ)} with axes (0,0,2,1), making 80/96 plaquettes have U_□ = -I.

**β < 1/4 is RULED OUT** — anti-instantons give |λ_min| = 14.2 without optimization, far exceeding 2d = 8.

**Best achievable: β < 1/8 (1.5× over SZZ)** — conditional on decoherence lemma (||C(Q)|| ≤ 2(d+1) = 10), which gives |λ_min| ≤ 4d = 16.

**Key findings:**
- D/C anti-correlation: maximal self-term negativity (D=-6) forces cross-term decoherence (||C||≈8.65 < 10)
- L=2 is worst case — |λ_min| decreases with larger L
- Decoherence strongly supported: 0/2000+ configs exceed flat value ||C_flat|| = 10
- Dimension scaling: |λ_min|/4d ≈ 0.85-0.92 (sub-4d bound exists but unproved)
- Random configs give |λ_min| ≈ 8-9, far from true infimum of 14.7 — structured anti-instantons needed

## Exploration 005: Cross-Term Decoherence Lemma — Proof Attempt

### Goal
Prove ||C(Q)|| ≤ 2(d+1) for all Q (decoherence lemma), completing the mass gap proof at β < 1/(2d).

### Outcome: CRITICAL NEGATIVE + PARTIAL POSITIVE

**The decoherence lemma is FALSE for d ≥ 3.** Adversarial gradient ascent found ||C|| = 11.68 > 10 = 2(d+1) at d=4. Also ||C|| = 8.60 > 8 at d=3. Counterexample is near anti-instanton with D ≈ 0.

**The lemma IS true for d = 2.** Proved via per-plaquette Cauchy-Schwarz + lattice aggregation.

**Key discoveries:**
1. Color kernel F has closed-form SVD: SVs exactly (2, 2, 2|β₀|) where β₀ = Re Tr(MN)/2 [VERIFIED]
2. Per-plaquette decoherence PROVED: ||C_□|| ≤ 3 for all Q, all d
3. Aggregation loses inter-plaquette sign structure for d ≥ 3 (||A_struct||/||A_total|| = 1.8 for d=4)
4. D/C anti-correlation is structural: configs maximizing ||C|| have D ≈ 0, keeping |λ(H)| bounded

**The β < 1/8 result CANNOT be obtained by bounding D and C separately.** Must bound the full Hessian directly.

## Exploration 006: Direct Hessian Bound — Per-Plaquette and Anti-Correlation

### Goal
Prove |λ(HessS(Q))| ≤ 4d via three approaches: D/C anti-correlation, concavity, per-plaquette.

### Outcome: NEGATIVE on Approach B; C and A not run

**Approach B FAILS:** |D_min| + ||C|| ≤ 4d is FALSE. Uniform rotation at θ=2π/3 gives sum = 16.58 > 16. The actual eigenvalues are fine (λ_max=14.82) but the triangle inequality pathway cannot work.

**Key insight:** The gap between |λ(H)| ≤ 4d (empirically true) and |D|+||C|| ≤ 4d (false) means the proof CANNOT go through any norm-additive bound. The cancellation operates at the eigenvector level.

**Most promising remaining directions:**
1. Concavity of λ_max(H(Q)) — code written, not run
2. Per-plaquette ||H_□|| ≤ 4 + graph coloring aggregation — code written, not run

