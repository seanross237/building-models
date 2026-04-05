# Exploration 005: Prove the Cross-Term Decoherence Lemma

## Mission Context

We are proving that the Wilson action Hessian for lattice SU(2) Yang-Mills satisfies |λ(HessS)| ≤ 4d for all Q ∈ SU(2)^E on the d-dimensional hypercubic torus (d=4 is the target). If proved, this gives a mass gap at β < 1/8 via Bakry-Émery.

**The proof is 90% complete.** We have:
1. The verified Hessian formula: H = D(self-term) + C(cross-term)
2. D ∈ [-2(d-1), 2(d-1)] — PROVED
3. At flat connections: ||C_flat||_op = 2(d+1), and D_flat = 2(d-1), giving λ_max = 4d
4. ||C(Q)||_op ≤ 2(d+1) for ALL 2000+ tested configs — COMPUTED, 0 violations

**The one missing piece is the Decoherence Lemma:**

> **Lemma (Decoherence):** For all Q ∈ SU(2)^E, ||C(Q)||_op ≤ ||C_flat||_op = 2(d+1).

If this is proved, the full result follows immediately:
- |λ(H)| ≤ |D| + ||C|| ≤ 2(d-1) + 2(d+1) = 4d
- β < 2/(4d) = 1/(2d) = 1/8 for d=4

**Your SOLE task: prove this lemma.** Everything else is done.

## The Cross-Term Operator C(Q)

### Definition

C(Q) is the 3|E| × 3|E| matrix formed by the cross-terms of the Hessian. For edges ep, eq sharing a plaquette □:

C[(ep,a),(eq,b)] = −(β/N) sp sq Re Tr(Lp (iσa) mid_{pq} (iσb) Rq)

where:
- β=1, N=2
- sp = +1 for forward edges, −1 for backward
- Lp, mid_{pq}, Rq are context matrices from the plaquette holonomy decomposition
- (ep,a) means edge ep, color index a ∈ {1,2,3}

### Block structure

C has a natural decomposition: for each pair of distinct edges (ep, eq) sharing a plaquette, there is a 3×3 color block:

C_{ep,eq} = −(1/2) sp sq F(Lp, mid, Rq)

where F_{ab}(M,N) = Re Tr(iσa M iσb N) is the color kernel.

### Key facts about F

1. **||F(M,N)||_op = 2** for ALL M, N ∈ SU(2). [PROVED in E003]
   Proof: For unit u,v ∈ ℝ³, uᵀFv = Re Tr((û·iσ)M(v̂·iσ)N). Since (û·iσ), M, (v̂·iσ), N ∈ SU(2), their product is in SU(2), and |Tr(SU(2))| ≤ 2. ∎

2. **At flat connections (all context matrices = I):** F(I,I) = Re Tr(iσa · iσb) = −2δab. So F_flat = −2I₃ for ALL plaquette pairs.

3. **At general Q:** F(M,N) is a 3×3 matrix with ||F|| = 2 and eigenvalues in [-2, 2], but the eigenvalues and eigenvectors depend on M and N.

### The spatial structure

We can write C(Q) = Σ_□ Σ_{p<q∈□} s_p s_q · A_{ep,eq} ⊗ F^{pq}(Q)

where:
- A_{ep,eq} is the spatial adjacency: a (|E| × |E|) matrix with 1 at position (ep,eq) and (eq,ep)
- F^{pq}(Q) is the 3×3 color kernel for that edge pair
- The sum is over all plaquettes □ and all pairs (p,q) of edges within □

**At flat connections:** F^{pq} = -2I₃ for all pairs, so:
C_flat = (−2I₃) ⊗ A_total = −I₃ ⊗ (2A_total)

where A_total = Σ_□ Σ_{p<q} s_p s_q A_{ep,eq}. The eigenvalues of C_flat are -2 times the eigenvalues of A_total. The max eigenvalue of A_total is (d+1) (from the Fourier analysis at flat).

So ||C_flat||_op = 2(d+1).

## What You Need to Prove

||C(Q)||_op ≤ 2(d+1) for all Q.

Equivalently: for all unit vectors v = (c_{e,a}) ∈ ℝ^{3|E|}:

|vᵀ C(Q) v| ≤ 2(d+1) · |v|²

## Proof Approaches to Try

### Approach 1: Tensor Product Norm Bound

C(Q) = Σ_i A_i ⊗ F_i(Q) where A_i are symmetric matrices (spatial) and F_i are 3×3 matrices (color) with ||F_i|| ≤ 2.

**At flat:** C_flat = A_total ⊗ (−2I₃), so ||C_flat|| = 2||A_total|| = 2(d+1).

**General Q:** Is there a bound ||Σ A_i ⊗ F_i|| ≤ max_i ||F_i|| · ||Σ A_i|| when A_i are PSD?

If A_i are NOT PSD (they aren't — A_{ep,eq} has entries ±1), this doesn't work directly.

**Modified approach:** Can you decompose A_i = A_i⁺ − A_i⁻ (positive/negative parts) and bound each?

### Approach 2: Kronecker/Tensor Inequality

If ||F_i|| ≤ 2 for all i, and we define T = Σ A_i ⊗ I₃, then:
||C(Q)|| = ||Σ A_i ⊗ F_i|| ≤ ||T|| · max_i ||F_i|| / ||I₃|| ?

No, this is wrong. Try instead:

For any x = Σ_e x_e ⊗ n_e (spatial-color decomposition), where x_e ∈ ℝ (spatial at edge e) and n_e ∈ ℝ³ (color at edge e):

xᵀ C(Q) x = Σ_{□,p<q} s_p s_q x_{ep} x_{eq} · n_{ep}ᵀ F^{pq}(Q) n_{eq}

≤ Σ |x_{ep}| |x_{eq}| · ||F^{pq}|| · |n_{ep}| · |n_{eq}|

= 2 · Σ |x_{ep}| |x_{eq}| |n_{ep}| |n_{eq}|

= 2 · xᵀ |A_total| x    (where |A_total| uses |entries| instead of signed entries)

But |A_total| has larger norm than A_total (loses the sign structure). This gives a bound ≥ 2(d+1), so it's too loose.

### Approach 3: Cauchy-Schwarz on Color Misalignment

At flat, all color factors align: n_{ep}ᵀ F^{pq} n_{eq} = -2 n_{ep}ᵀ n_{eq} for ALL pairs. The maximum of vᵀ C v occurs when all n_e are equal (uniform color direction).

At general Q, the color factors F^{pq} rotate the color direction differently for each pair. The Cauchy-Schwarz inequality:

|n_{ep}ᵀ F^{pq} n_{eq}| ≤ ||F^{pq}|| · |n_{ep}| · |n_{eq}| = 2 |n_{ep}| |n_{eq}|

is tight only when n_{ep} and n_{eq} are aligned with the top singular vectors of F^{pq}. But different pairs have different top singular vectors (at non-flat Q), so the global maximum requires a compromise.

**Can you formalize this "compromise" into a bound?**

### Approach 4: Direct Per-Plaquette Bound

For each plaquette □, the cross-term contribution is:
C_□ = Σ_{p<q∈□} s_p s_q A_{ep,eq} ⊗ F^{pq}

At flat, C_□ has operator norm ≤ 4 per plaquette (from the per-plaquette Hessian analysis in E003).

Each edge is in 2(d-1) plaquettes, so ||C|| ≤ ||Σ_□ C_□|| ≤ sum_□ ||C_□|| = ... (overcounts by edge overlap).

This approach probably gives the Gershgorin-like 8(d-1) bound. But maybe a tighter per-plaquette bound is possible using the sign structure s_p s_q.

### Approach 5: Variational/SDP

Set up the optimization: max ||C(Q)||_op over Q ∈ SU(2)^E.

The constraint is Q_e ∈ SU(2) for each edge. The color kernels F^{pq} depend on the context matrices, which are products of link variables. The optimization has structure — can you use KKT conditions at the maximum (flat connection) to show it's a global maximum?

At flat: dC/dQ = 0 (by symmetry — flat is a critical point of ||C||). The question is whether it's a maximum. Compute d²||C||/dQ² at flat — if negative definite, flat is a local maximum of ||C||.

**This is the most promising approach.** Verify numerically that ||C(Q+εW)|| < ||C_flat|| for small ε and random perturbation directions W.

### Approach 6: Schur Product / Hadamard Bound

C(Q) can be written as a Schur (entrywise) product of the spatial matrix with the color matrix. The Schur product theorem states ||A ∘ B|| ≤ ||A|| · max diagonal of B. Does this help?

## Numerical Verification Requirements

For EVERY proof approach you attempt:
1. Implement it numerically for L=2, d=4
2. Compute the bound it gives for 50+ random Q configs
3. Compare the bound to the actual ||C(Q)||_op
4. Report: does the approach give a bound ≤ 2(d+1) = 10?

## Success Criteria

- The decoherence lemma is PROVED (complete algebraic argument, verified numerically)
- OR: a clear proof for a WEAKER bound ||C(Q)|| ≤ C with C < 4d (which combined with |D| ≤ 2(d-1) gives |λ| < 6d-2 — still useful)
- OR: a clear obstruction report explaining why the lemma is hard to prove with elementary tools, with specific suggestions for what technique might work

## Failure Criteria

- All approaches fail to give a bound ≤ 2(d+1)
- Cannot verify the approaches numerically

## Output

Write to REPORT.md (≤ 250 lines) and REPORT-SUMMARY.md (≤ 30 lines). Write incrementally after each approach.
