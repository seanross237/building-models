# Mission: Prove Conjecture 1 — Yang-Mills Hessian Bound

Prove that for all gauge configurations Q ∈ SU(2)^E on the d=4 hypercubic torus:

  λ_max(M(Q)) ≤ 4d = 16

Equivalently: for all tangent vectors v,

  Σ_□ |B_□(Q, v)|² ≤ 4d |v|²

Equivalently: the top-eigenspace projection satisfies P^T R(Q) P ≼ 0 for all Q, where R(Q) = M(Q) − M(I).

**If proved:** This gives H_norm ≤ 1/12 for all Q, which via the Bakry-Émery condition (SZZ Theorem 1.3) yields a mass gap for lattice SU(2) Yang-Mills at β < 1/4 — a 12× improvement over Shen-Zhu-Zhu (2023) and 6× over Cao-Nissim-Sheffield (2025).

## Context

A prior Atlas mission on Yang-Mills (3 strategies, 30 explorations, March 2026) established:

1. **Proved** H_norm ≤ 1/8 for all Q → mass gap at β < 1/6 (8× SZZ). This is rigorous.
2. **Proved** H_norm = 1/12 exactly at Q=I, achieved by the staggered mode v_{x,μ} = (−1)^{|x|+μ}.
3. **Proved** pure gauge isometry: λ_max(M(Q_pure)) = 4d for all pure gauge Q.
4. **Proved** trace invariant: Tr(M(Q)) is constant over all Q → the full operator inequality M(Q) ≼ M(I) is structurally impossible.
5. **Numerically confirmed** H_norm ≤ 1/12 for 500+ diverse configurations including adversarial gradient ascent. Zero violations.
6. **Proved** the conjecture for 4 special families: pure gauge, flat connections, uniform Q, single-link.

The gap between the proved β < 1/6 and the conjectured β < 1/4 reduces to this single inequality.

## Prior Art and Key References

- SZZ: arXiv:2204.12737 (Shen-Zhu-Zhu 2023). Bakry-Émery mass gap, Lemma 4.1, β < 1/48.
- CNS: arXiv:2509.04688 (Cao-Nissim-Sheffield Sept 2025). β < 1/24.
- Jiang: arXiv:2211.17195 (2022). Discrete Weitzenböck identity. F = holonomy defect, no sign proved.

## DO NOT TRY — Proven Dead Ends

The previous mission tried 7 proof approaches. All hit structural obstructions:

1. **Full operator inequality M(Q) ≼ M(I)**: IMPOSSIBLE — Tr(R(Q)) = 0 forces R to have both positive and negative eigenvalues for any Q ≠ I.
2. **Global geodesic concavity**: FAILS — F''(Q,W) > 0 found in 8/10 random Q ≠ I. Q=I is only a local maximum.
3. **Per-plaquette Hessian factoring**: FALSE for Q ≠ I — ratio up to 8383× for random Haar Q.
4. **Coulomb gauge / perturbative Fourier**: Gribov problem at large fields. Works perturbatively but breaks for finite coupling.
5. **Jiang Weitzenböck F ≼ 0**: Jiang proves no sign for F. His framework is too general (any graph).
6. **Schur / Haar average**: E[M(Q)] = 2(d−1)I but average ≠ maximum. Can't detect measure-zero maximizers.
7. **Triangle inequality refinement**: Caps at H_norm ≤ 1/8. Structurally cannot reach 1/12 — the factor 3/2 gap between 8(d−1)=24 and 4d=16 requires global Fourier structure.

## Most Promising Untried Approach

**Staggered-mode Weitzenböck**: For v = v_stag = (−1)^{|x|+μ} e_{a₀}:

  v^T R(Q) v = Σ_□ [|Σ_k c_k Ad_{P_k}(n)|² − 4] |n|²

where c_k ∈ {±1} are staggered signs, R_k = Ad_{P_k} ∈ SO(3) are partial holonomy rotations.

The per-plaquette bound |Σ c_k R_k n|² ≤ 4 is FALSE in general. But the SUM over all plaquettes may satisfy Σ_□ |Σ c_k R_k n|² ≤ 4 n_plaq |n|² by exploiting the staggered sign structure on the hypercubic lattice.

**Key identity to prove:** The staggered pattern c_k = (−1)^{|x_k|+μ_k} creates cancellations in the global plaquette sum that force the inequality.

## Other Observations That May Help

- **Exact Weitzenböck formula** (single-link): max λ[R(Q)|_P] = −W(Q)/12 where W(Q) is the Wilson action density. Holds with R² = 1.000000. The −1/12 coefficient is exactly the H_norm threshold.
- **Decoherence mechanism**: Q ≠ I introduces adjoint rotations that "misalign" contributions to B_□, reducing coherent interference. Random Q gives λ_max ≈ 2β (half the maximum). The staggered mode's constructive interference is maximized only at Q=I.
- **Q=I is a strict local maximum** of λ_max(M(Q)): F''(0) < 0 for all multi-edge perturbation directions W.
- **Gauge orbit characterization** (numerical): λ_max(M(Q)) = 4d if and only if Q is pure gauge. Proving this "iff" would close the conjecture (the "if" direction is proved).

## Strategy Guidance

- This is a proof problem, not a survey. Spend computation budget on testing proof ideas, not cataloguing more known results.
- The 7 dead ends above are HARD stops. Do not revisit them even partially.
- The proof likely requires exploiting the hypercubic lattice structure (staggered signs, Fourier analysis) in a way that per-plaquette arguments cannot.
- Use math explorers heavily — any claimed proof must be verified computationally.
- If the conjecture appears unprovable with current techniques, characterize WHY as precisely as possible. "We couldn't do it" is not useful. "The proof requires X, and X fails because Y" is useful.

## Definitions and Conventions

Use SZZ conventions throughout:
- S(Q) = −(β/N) Σ_□ Re Tr(U_□)
- |A|² = −2 Tr(A²) for A ∈ su(N)
- N = 2, d = 4
- B_□(Q,v) = v_{e₁} + Ad_{Q_{e₁}}(v_{e₂}) − Ad_{Q_{e₁}Q_{e₂}Q_{e₃}⁻¹}(v_{e₃}) − Ad_{U_□}(v_{e₄})
  (backward edges include their OWN link in the partial holonomy — this was a corrected formula)
