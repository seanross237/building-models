# Exploration 004: Characterize λ_min(HessS) and Prove the Decoherence Lemma

## Mission Context

We are proving mass gap bounds for lattice SU(2) Yang-Mills on the d-dimensional hypercubic torus.

**The mass gap condition** (from Bakry-Émery, verified in E003):
β < 2 / sup_Q |λ_min(HessS(Q; β=1))|

where the Hessian is the 3|E|×3|E| matrix with entries:
- Self-terms: H[(e,a),(e,b)] = (β/N) δ_{ab} Σ_{□∋e} Re Tr(U_□)
- Cross-terms: H[(ep,a),(eq,b)] = −(β/N) sp sq Re Tr(Lp iσ_a mid iσ_b Rq)

The Hessian is computed with respect to the basis {iσ_a} for su(2) (so v_e = Σ c_{e,a} iσ_a). β=1, N=2 throughout.

**What's already proved/computed:**
1. λ_max(HessS) ≤ 4d = 16 (d=4), conditional on decoherence lemma. Achieved at flat connections. [E003]
2. At flat connections: λ_min = 0, λ_max = 4d. [E002-E003]
3. Away from flat: λ_min goes negative. Numerically: λ_min ≈ -8.5 for random Q (d=4). [E003]
4. The D+C decomposition: H = D + C where D is self-term (diagonal) and C is cross-term. [E003]
5. D ∈ [-2(d-1), 2(d-1)] (from Re Tr ∈ [-2, 2]). [PROVED]
6. ||C(Q)||_op is conjectured ≤ ||C_flat||_op = 2(d+1). [COMPUTED, not proved]
7. Cross-term kernel ||F_{ab}||_op = 2 exactly for all SU(2). [PROVED]

**The mass gap improvement table:**
| sup |λ_min| | β threshold (d=4) | Improvement over SZZ |
|-------------|-------------------|---------------------|
| 16 (= 4d)  | 1/8               | 1.5×               |
| 8 (= 2d)   | 1/4               | 3×                 |
| 4 (= d)    | 1/2               | 6×                 |

## Your Tasks

### Stage 1: Find sup |λ_min(HessS)| by Adversarial Search

**This is the most important stage.** The exact value of sup |λ_min| determines the mass gap improvement.

For L=2, d=4 (192×192 Hessian):
1. Implement the analytical Hessian formula (not finite differences — too slow for optimization)
2. Run gradient DESCENT on λ_min(HessS(Q)): minimize the smallest eigenvalue
   - 20 independent random starts
   - Edge-by-edge optimization (minimize λ_min by optimizing one link at a time)
   - 100+ iterations per start
3. Try structured starts:
   - Q_e = exp(θ iσ₃) with θ ∈ {π/4, π/2, 3π/4, π} (various angles)
   - Mixed: half links = I, half = iσ₃
   - "Checkerboard": alternating Q_e = I and Q_e = iσ_a by sublattice
4. Record the most negative λ_min found. Save the configuration.

**Critical outputs:**
- What is the empirical inf λ_min(HessS)?
- Is it close to -2d = -8? Or -4d = -16? Or something else?
- What type of configuration achieves it?

### Stage 2: Understand the Extremal Configuration

For the configuration Q* that minimizes λ_min:
1. What is the Wilson action S(Q*)?
2. What are the plaquette holonomies U_□? Are they near -I (anti-instanton)?
3. What is the corresponding eigenvector v*? Is it staggered? Localized? Fourier?
4. How does Q* relate to known special configurations?
5. Compute D(Q*) and C(Q*) separately. Which contributes more to the negative eigenvalue?

### Stage 3: Prove |λ_min(HessS)| ≤ C for the best C you can

**Approach 1 — D+C bound:**
λ_min(H) ≥ D_min + λ_min(C)

D_min = -2(d-1) (proved). If ||C||_op ≤ 2(d+1) (decoherence lemma):
λ_min ≥ -2(d-1) - 2(d+1) = -4d

This gives |λ_min| ≤ 4d → β < 1/8. Matches the λ_max bound.

But the numerics show |λ_min| ≈ 8.5 ≪ 16 for d=4. So D_min + C_min is too pessimistic — D and C don't both reach their worst case simultaneously.

**Approach 2 — Per-plaquette bound on the full Hessian:**
Each plaquette contributes h_□(v) to HessS. What is the most negative per-plaquette contribution?

h_□(v) = self-terms + cross-terms for edges of □
       = (β/N)[Re Tr(U_□)(Σ_e |c_e|²) + cross-terms]

If h_□(v) ≥ -C_plaq × Σ_{e∈□} |c_e|², then summing over plaquettes:
HessS(v,v) ≥ -C_plaq × 2(d-1) × |c|²

This gives |λ_min| ≤ 2(d-1) × C_plaq. Compute C_plaq numerically and analytically.

**Approach 3 — Exploit the Bakry-Émery structure directly:**
The Bakry-Émery condition Γ₂ ≥ K gives:
K = Ric + HessS = (per-edge Ric) + HessS

Since each edge contributes Ric = 2 (in our coordinates) and each edge participates in 2(d-1) plaquettes:
K(v,v) = 2|c|² + HessS(v,v)

If we can show K(v,v) ≥ 0 for β ≤ β₀: this means mass gap at β ≤ β₀.
K = 0 iff HessS(v,v) = -2|c|², i.e., HessS has eigenvalue -2.

Is there a direct way to show that the per-edge Ricci contribution (2) PLUS the per-edge Hessian contribution cannot sum to < 0? This would bypass the eigenvalue bound entirely and prove the mass gap directly.

**Approach 4 — Anti-concentration:**
λ_min is negative because self-terms become negative (Re Tr < 0) while cross-terms add coherently. But Re Tr(U_□) = -2 at U_□ = -I, which requires very specific Q. Can you show that if SOME plaquettes have Re Tr = -2, others must have Re Tr close to +2, limiting the total negativity?

### Stage 4: Decoherence Lemma Attempt

**Statement:** For the cross-term operator C(Q) = Σ spatial_coefficients ⊗ color_kernels, with each 3×3 color kernel having ||F||_op = 2, the operator norm ||C(Q)||_op is maximized when all color kernels equal -2I₃ (the flat-connection value).

**Proof attempts:**
1. **Jensen/convexity:** C(Q) is a sum of rank-≤3 contributions. Each has operator norm ≤ 2 × |spatial coefficient|. The sum's operator norm is maximized when all point in the same direction. Since -2I₃ is "maximally aligned" (proportional to identity), this is the coherent maximum.

2. **SO(3) averaging:** The color kernel F_{ab}(M,N) = Re Tr(iσ_a M iσ_b N). If we average over the SO(3) action on the color indices (induced by conjugation Q → gQg⁻¹), the average of F should be proportional to I₃ × (trace of F). Since ||F|| = 2 and Tr(F) = Re Tr(MN) (compute this!), the "most isotropic" F maximizes the norm.

3. **Direct calculation:** For a specific plaquette pair, expand ||C_{pair}(Q)|| as a function of the link variables and show it's ≤ the flat-connection value.

### Stage 5: Synthesis

Combine your findings:
1. What is the empirical sup |λ_min|?
2. What is the proved bound on |λ_min|?
3. Is the decoherence lemma proved?
4. What is the resulting mass gap threshold?

If you achieve |λ_min| ≤ 2d = 8 (proved): this is the best possible outcome — mass gap at β < 1/4.
If you achieve |λ_min| ≤ 4d = 16 (via decoherence): mass gap at β < 1/8 — still valuable.
If you can't prove either: characterize the obstruction precisely.

## Success Criteria

- Empirical sup |λ_min| determined to ±0.1 by adversarial optimization (≥20 starts)
- At least one bound on |λ_min| proved (even if weaker than 2d)
- Decoherence lemma: proved OR clear obstruction identified
- The extremal configuration characterized (what type, what symmetry)

## Failure Criteria

- Cannot implement the analytical Hessian (formula from E002 is not reproducible)
- Adversarial search finds |λ_min| > 4d (contradicting all prior numerics — would be a major surprise)

## Output

Write to REPORT.md (≤ 250 lines) and REPORT-SUMMARY.md (≤ 30 lines). Write incrementally.
