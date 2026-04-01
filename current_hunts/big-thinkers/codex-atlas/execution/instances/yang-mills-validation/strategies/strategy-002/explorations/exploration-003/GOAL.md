# Exploration 003: Path B — Flat Connections Maximize λ_max(H_actual)

## Mission Context

We are repairing a proof gap in a mass gap result for SU(2) Yang-Mills at β < 1/6. The gap: the B² formula HessS(v,v) = (β/(2N)) Σ|B□|² is exact at flat connections (Q where all U□ = I) but NOT at generic Q. However, the inequality λ_max(H_actual) ≤ λ_max(H_formula) holds numerically for all ~300 tested configurations.

**Key prior result (E001):** The ratio r(Q) = λ_max(H_actual)/λ_max(H_formula) satisfies:
- r = 1.0 at flat connections (equality)
- r < 1.0 for all non-flat configs (strict inequality)
- gap = 1 - r scales as ε² near flat connections (gap ≈ 0.6·ε²)
- max non-flat r = 0.981 (one-hot π rotation on single link)

**This suggests flat connections are the GLOBAL maximizers of λ_max(H_actual(Q)).** If proved, the proof chain is repaired: max_Q λ_max(H_actual(Q)) = λ_max(H_actual(I)) = 4β, and the Bakry-Émery threshold gives β < N²/(8(d-1)).

## Your Task: Prove Flat Connections are Local (and Hopefully Global) Maximizers

### Part 1: Perturbation Theory at Q = I

At flat connection Q = I:
- H_actual(I) = H_formula(I) = the lattice curl-curl operator
- λ_max(H_actual(I)) = 4β (for d=4, SU(2))
- The top eigenvalue has degeneracy = (d-1)(N²-1) = 9 for d=4, N=2
- The top eigenvectors are the "staggered modes": v_{x,μ,a} = (-1)^{|x|+μ} · c_μ · δ_{a,a₀} where c = (c₁,...,c_d) satisfies Σc_μ = 0

**Compute the first-order perturbation of λ_max:**

Consider Q(t) = {exp(t · δQ_e) · I_e} where δQ_e ∈ su(2) is an arbitrary perturbation on each link.

1. The Hessian at Q(t) is H(t). At t=0: H(0) = H_actual(I).
2. First-order: dH/dt|_{t=0} = some matrix depending on δQ.
3. By degenerate perturbation theory: the first-order shift of the top eigenvalue is the largest eigenvalue of the 9×9 matrix:

   Δ_ij = ⟨v_i | dH/dt|_{t=0} | v_j⟩

   where {v_i} are the 9 degenerate top eigenvectors at Q = I.

4. **If all eigenvalues of Δ are ≤ 0 for ALL δQ:** flat connections are local maxima.

5. **Compute this numerically:**
   - Pick 20 random δQ directions (each δQ_e random su(2) on each of the 64 links)
   - For each: compute H_actual(Q(t)) at t = -0.01, 0, 0.01, 0.02 using finite differences
   - Extract λ_max(H(t)) for each t
   - Verify λ_max(H(t)) ≤ λ_max(H(0)) = 4β for t ≠ 0

### Part 2: Second-Order Analysis

If first-order shows Δ = 0 for all δQ (which would happen if symmetry forbids first-order perturbation — this is likely since H(I) has maximal symmetry):

1. Compute the second-order correction: d²λ_max/dt²|_{t=0}
2. If d²λ/dt² < 0 for all δQ: flat is a strict local max (consistent with gap ∝ ε²)
3. The second-order correction involves:
   - ⟨v_i | d²H/dt²|_{t=0} | v_j⟩ (direct second derivative)
   - Σ_{k not in top eigenspace} |⟨v_i | dH/dt | w_k⟩|² / (λ_max - λ_k) (level repulsion from non-top modes)

### Part 3: Numerical Verification

On L=2, d=4, β=1.0, SU(2):

1. **Line scans:** For 20 random perturbation directions δQ:
   - Compute λ_max(H_actual(exp(t·δQ))) for t ∈ {0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0}
   - Plot or tabulate λ_max(t). It should decrease monotonically from 4β at t=0.
   - Fit: λ_max(t) = 4β - c·t² + O(t³). What is c? Is it always positive?

2. **Gauge orbit check:** The flat connection Q = I has a gauge orbit (Q_e → g(x)·I·g(y)⁻¹ = g(x)g(y)⁻¹). All points on this orbit should give the same λ_max = 4β. Verify for 5 random gauge transformations.

3. **Non-flat local maxima search:** Starting from 10 random non-flat configs, run gradient ASCENT on λ_max(H_actual(Q)). Do all trajectories converge to flat connections (gauge orbit of I)?

### Part 4: Toward a Rigorous Proof

Based on Parts 1-3, assess:

1. **Is flat a local max?** (First/second order perturbation theory)
2. **Is flat the unique global max?** (Gradient ascent convergence)
3. **What's the proof path?**
   - If the Weitzenböck identity M(Q) = M(I) + R(Q) gives R(Q) ≼ 0 (known from prior work for the formula Hessian), does a similar identity hold for H_actual?
   - Can you write H_actual(Q) = H_actual(I) + D(Q) where D(Q) has negative top eigenvalue?
   - Is there a convexity/concavity argument? (The space of SU(2) configs is compact.)

## Conventions

- SU(2): N = 2, generators Tₐ = iσₐ/2
- Inner product: ⟨X,Y⟩ = -2 Tr(XY)
- Wilson action: S(Q) = -(β/2) Σ_□ Re Tr(U□) (β/N = β/2 for N=2)
- LEFT perturbation: Q → exp(t·v) · Q
- H_actual: full Hessian of S by central finite differences (h=1e-4)
- H_formula: (β/(2N)) × Σ B□ᵀ B□ with LEFT adjoint B□ formula
- At Q = I: both agree, λ_max = 4β = 4.0 for β = 1.0

## Success Criteria

- **Full success:** Proof that flat connections are global maximizers of λ_max(H_actual)
- **Partial success:** Proof that flat connections are strict local maxima (with computed second-order coefficient), plus numerical evidence for global
- **Failure:** Discovery of a non-flat local maximum of λ_max(H_actual), or first-order perturbation increasing λ_max

## Output

Write REPORT.md incrementally. All code in code/. Write REPORT-SUMMARY.md when done (≤30 lines).
