# Exploration 008: Prove max λ[R(Q)|_P] ≤ −W(Q)/12

## Mission Context
This is a YANG-MILLS mission (strategy-003), Phase 3. Do not confuse with other missions.

## What Has Been Established

**Phase 1-2 findings (all explorations, 7 total):**

1. **Correct target** (E005): NOT "M(Q) ≼ M(I)" (FALSE — Tr(R(Q))=0 prevents this). The correct target is:
   - λ_max(M(Q)) ≤ 4d for all Q ∈ SU(2)^E
   - Equivalently: P^T R(Q) P ≼ 0, where P = 9-dim top eigenspace of M(I) (eigenvalue 4d=16)

2. **Structural facts proved:**
   - M(I) = K_curl, λ_max(K_curl) = 4d (analytical, Fourier theorem)
   - M(Q_pure) = Ad_G^T M(I) Ad_G (pure gauge isometry, analytical)
   - Tr(M(Q)) = Tr(M(I)) for ALL Q (structural invariant)
   - B_□ B_□^T = 4I₃ per plaquette (color invariant)
   - E[M(Q)] = 2(d-1)I = 6I (Haar average)

3. **Families proved** (λ_max ≤ 4d):
   - Q = pure gauge (isospectral)
   - Q = single-link perturbation (gauge-equivalent to pure gauge)
   - Q = uniform (all links equal): via Fourier + (2I+R+R^T) ≼ 4I for R ∈ SO(3)
   - Q = flat connections (gauge transform to I)

4. **Key formula from library** (provisional — verified for 20 configs):
   ```
   max λ[R(Q)|_P] = −W(Q)/12
   min λ[R(Q)|_P] = −W(Q)/3
   ```
   where W(Q) = Σ_□ (1 − Re Tr(U_□)/N) ≥ 0 is the Wilson action density (≥ 0 always).

5. **If the formula max λ[R(Q)|_P] ≤ −W(Q)/12 holds for all Q**: Since W(Q) ≥ 0, this immediately gives P^T R(Q) P ≼ 0 (i.e., all eigenvalues of the 9×9 matrix P^T R(Q) P are ≤ 0). THIS CLOSES THE PROOF.

## Your Goal

**Investigate and attempt to prove: max λ[R(Q)|_P] ≤ −W(Q)/12.**

## Task 1 (Priority 1): Verify the formula numerically at scale

Compute max λ[P^T R(Q) P] and W(Q) for 200+ diverse configurations:
- 50 random Haar (L=2, SU(2), d=4)
- 50 Gibbs samples β = 0.5, 1.0, 2.0, 4.0
- 20 near-identity (ε = 0.01, 0.1, 0.5, 1.0, 2.0, π)
- 20 pure gauge (should give max λ = 0 and W = 0)
- 20 abelian (diagonal) configs
- 40 adversarial (gradient ascent on max λ[P^T R P] / W(Q))

For each config, compute:
- max_eig = λ_max(P^T R(Q) P) using numpy eigvalsh
- W_Q = Σ_□ (1 - Re Tr(U_□)/N) using plaquette holonomies
- ratio = max_eig / (-W_Q / 12)  [should be ≤ 1]
- min_eig = λ_min(P^T R(Q) P)
- ratio_min = min_eig / (-W_Q / 3)  [should be ≤ 1]

**Report:** For all 200+ configs, does max λ[P^T R P] ≤ -W/12? Does min λ[P^T R P] = -W/3?

## Task 2 (Priority 1): Analytical proof attempt

**Approach A: Direct computation for staggered modes.**

For v = v_stag ⊗ n (staggered spatial mode × fixed color direction n ∈ su(2)):

1. Compute v^T M(Q) v explicitly:
   ```
   v^T M(Q) v = Σ_□ |B_□(Q, v)|²
   ```
   For staggered v, v_{x,μ} = (−1)^{|x|+μ} n. So:
   ```
   B_□(Q, v) = (−1)^{|x|} × [n + Ad_{Q_{x,μ}}(−1)^μ n − Ad_{Q_{x,μ}Q_{x+μ,ν}}(−1)^{μ+ν} n − Ad_{U_□^{-1} Q_{x,ν}^{-1}}(−1)^{ν+1} n]
   ```
   (sign pattern from plaquette orientation)

2. For a fixed plaquette □ at base site x, expand |B_□(Q, v)|²:
   ```
   |B_□|² = |A₁ + A₂ - A₃ - A₄|²
   ```
   where Aᵢ = Rᵢ(n) and Rᵢ ∈ SO(3) are the adjoint transport rotations.

3. For Q=I, all Rᵢ = I, so:
   ```
   |B_□(I, v)|² = |n + n - n - n|² × (−1)^{signs} → 4|n|²  [per staggered mode unit]
   ```
   Wait — need to be careful about signs. At Q=I: B_□(I,v) = ω_□(v) = Σ_{e∈□} s_e v_e = (−1)^{|x|}(s₁ v_{x,μ} + s₂ v_{x+μ,ν} + s₃ v_{x+ν,μ} + s₄ v_{x,ν}) × ...
   At Q=I: |B_□(I, v_stag)|² = 4|n|² exactly (since the 4 signs contribute coherently for the staggered mode).

4. For Q ≠ I:
   ```
   |B_□(Q, v_stag)|² = |R₁ n + R₂ n − R₃ n − R₄ n|²
   ```
   where Rᵢ = Ad_{Pᵢ} ∈ SO(3). Show this is ≤ 4|n|² with equality iff all Rᵢ = I.

5. **Key step:** Expand:
   ```
   |R₁ n + R₂ n − R₃ n − R₄ n|² = 4|n|² + 2(cross terms with signs)
   ```
   The cross terms involve ⟨Rᵢ n, Rⱼ n⟩ = n^T Rᵢ^T Rⱼ n = ⟨n, R_{ij} n⟩ where R_{ij} = Rᵢ^T Rⱼ ∈ SO(3).

   The sum of all cross terms = Σ_{i<j} s_i s_j ⟨n, R_{ij} n⟩ where s_i ∈ {+1,+1,−1,−1}.

   Show this is ≤ 0 by bounding ⟨n, R n⟩ in terms of Re Tr(U_□).

**Approach B: W(Q) and the plaquette holonomy.**

The Wilson action density W(Q) = Σ_□ (1 − Re Tr(U_□)/N) involves plaquette holonomies U_□ ∈ SU(2). For SU(2), Re Tr(U)/N = cos θ where U = exp(iθ n̂·τ).

When U_□ is close to I, cos θ_□ ≈ 1 and W_□ ≈ 0. When U_□ = −I (maximal), cos θ_□ = −1 and W_□ = 2.

The conjectured formula:
```
max λ[P^T R(Q) P] = -W(Q)/12 = -(1/12) Σ_□ (1 - cos θ_□)
```
suggests each plaquette contributes a negative shift of −(1/12)(1 − cos θ_□) to the maximum eigenvalue. This is additive in the plaquette curvatures.

**Approach C: Per-plaquette Taylor expansion.**

For a single active plaquette (U_□ = exp(iθ F), all others I):
1. Compute R(Q)|_P as a function of θ
2. Show max λ = −(1/12)(1 − cos θ)

This is a clean single-plaquette computation. At small θ: max λ ≈ −θ²/24 (negative). At θ = π: max λ = −1/6.

## Task 3 (Priority 2): Tight bound vs exact formula

The library says "max λ = −W/12 for single-link, verified for 20 configs." Check:
1. Is it an EQUALITY or just an upper bound?
2. For random Q, what is max λ / (−W/12)? Is it always ≤ 1? Is it sometimes close to 1?
3. For abelian configs, max λ = 0 (achieved at the invariant τ₃ direction) — what is W for these?

## Task 4 (Priority 3): Connection to Jiang (2022)

Jiang (2022) arXiv:2211.17195 gives: Δ_A = B_A + Ric + F, where F(i,j,k) = ρ(A(i,j)A(j,k)) − ρ(A(i,k)).

For the hypercubic lattice with SU(2):
- F(i,j,k) is the holonomy defect = Ad(G_{ik}) − Ad(G_{ij})Ad(G_{jk}) = −(Ad(U_□) − I)
- R(Q) corresponds to −F

So R(Q)|_P ≼ 0 iff F|_P ≽ 0.

Can we show F|_P ≽ 0 using the structure of SO(3) = SU(2)/Z₂?
- For each plaquette: F|_P has contribution +(Ad(U_□) − I)|_P ≽ 0?
- For U_□ = exp(iθ n̂·τ): Ad(U_□) − I = rotation by 2θ around n̂ minus identity. Eigenvalues of (R−I) are {−2, 2cos(2θ)−1, 2cos(2θ)−1}... need more care.

## Success Criteria

**Full success:** Prove max λ[P^T R(Q) P] ≤ 0 for all Q analytically (closes the main theorem).

**Strong partial success:** Prove max λ[P^T R(Q) P] ≤ −cW(Q) for some c > 0 (bound in terms of Wilson action).

**Partial success:** Verify the formula numerically for 200+ configs AND identify the key algebraic step needed for the proof.

**Useful failure:** Show that the formula breaks down for some class of configs, narrowing the proof strategy.

## Output Format

Write REPORT.md section by section:
1. Numerical verification (200+ configs, ratio max_eig / (-W/12))
2. Approach A: staggered mode direct computation
3. Approach B: W(Q) structure
4. Approach C: single-plaquette exact formula
5. Jiang connection
6. Summary: proved / partial / gap

Write REPORT-SUMMARY.md (1 page): What was proved? Is max λ ≤ -W/12 verified?

## Notes

- This is a MATH COMPUTATION task — use numpy for numerical verification, sympy for algebra.
- Write REPORT.md section by section (after each section completes).
- The single-link case was verified for ε ∈ {0, 0.1, 0.5, 1.0, π/2, π} in E005. Build on this.
- Convention: S = −(β/N) Σ_□ Re Tr(U_□). |A|² = −2Tr(A²). Generators τ_a = iσ_a/2, so |τ_a|² = 1/2.
- CRITICAL: The B_□ formula has a known correction (backward edges include holonomy transport). Use the formula verified by E001 finite differences, NOT the original GOAL.md formula.
