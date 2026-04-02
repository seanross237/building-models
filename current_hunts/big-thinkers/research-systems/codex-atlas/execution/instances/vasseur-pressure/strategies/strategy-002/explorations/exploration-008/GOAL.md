<!-- explorer-type: math -->

# Exploration 008: SDP Formalization of Chebyshev Sharpness Under NS Constraints

## Goal

Use semidefinite programming (or linear programming / convex optimization) to determine whether the Chebyshev bound |{|u| > λ}| ≤ λ^{-10/3} ||u||_{L^{10/3}}^{10/3} can be improved when the additional constraints div(u) = 0, ||u||_{L^2} ≤ E, and ||∇u||_{L^2} ≤ D are imposed. If the optimization shows Chebyshev is tight even under these constraints, this formalizes the claim that β = 4/3 cannot be improved by exploiting NS structure in the Chebyshev step.

## Background

### The informal sharpness theorem

Strategy-002 (8 explorations) has established that β = 4/3 cannot be improved by:
1. Modified energy functional (sharp by construction)
2. Improved Sobolev embedding for div-free (H¹→L⁶ sharp)
3. Optimized truncation function (irrelevant to β)
4. Direct Chebyshev improvement (circular with regularity — β = 1+s/n)
5. DNS level-set measurement (constant 3-5× slack, k-independent)
6. Commutator / compensated compactness (3 independent obstructions)
7. Frequency-localized Littlewood-Paley (Bernstein penalty, CZ optimal freq-by-freq)
8. Non-CZ pressure handling (tool-independent — IBP, H¹/BMO, CRW all ≤ 4/3)

The adversarial review (E007) confirmed all closures survive and rated the seven-route obstruction (Claim 3) as the most significant novel result, recommending SDP formalization as the path to rigor.

### What the SDP would prove

The Chebyshev step is the SINGLE potentially improvable step in the De Giorgi chain (E001). The question is: for functions satisfying NS structural constraints, can |{|f| > λ}| be better than λ^{-p}||f||_p^p?

If we can show that the answer is NO (or that any improvement is too small to affect β), then the Chebyshev step is provably sharp under NS constraints, completing the formalization.

## Specific Computation Tasks

### Task 1: Formulate the primal optimization problem

**Primal problem (continuous):**
```
maximize |{x ∈ Ω : |u(x)| > λ}|
subject to:
  div(u) = 0 on Ω = [0,2π]³
  ||u||_{L^2(Ω)} ≤ E
  ||∇u||_{L^2(Ω)} ≤ D
  ||u||_{L^{10/3}(Ω)} ≤ S
```

**Finite-dimensional relaxation:**
Truncate to Fourier modes |k| ≤ N (try N = 4, 8, 16):
- u(x) = Σ_{|k|≤N} û_k e^{ikx} with û_{-k} = conjugate(û_k), k · û_k = 0 (div-free)
- ||u||_{L^2}² = Σ |û_k|²
- ||∇u||_{L^2}² = Σ |k|² |û_k|²
- ||u||_{L^{10/3}} and |{|u|>λ}| must be evaluated by quadrature on a spatial grid

**The level-set measure is non-convex** (it's a measure of a super-level set). Approximate:
- Use the indicator relaxation: replace 1_{|u|>λ} with a smooth approximation σ_ε(|u| - λ) where σ_ε is a sigmoid with width ε
- Or: use the Chebyshev-like upper bound: |{|u|>λ}| ≤ λ^{-q} ||u||_q^q and optimize over the dual variable q

### Task 2: Formulate the dual problem

The Lagrangian dual of the Chebyshev optimization:

**Dual (continuous):**
```
minimize μ E² + ν D² + ρ S^{10/3}
subject to:
  μ |u(x)|² + ν |∇u(x)|² + ρ |u(x)|^{10/3} ≥ 1_{|u(x)| > λ}
  for all div-free u and all x ∈ Ω
  μ, ν, ρ ≥ 0
```

This is equivalent to: for each x, the function g(v) = μ|v|² + ν|∇v|² + ρ|v|^{10/3} - 1_{|v|>λ} ≥ 0 for all v.

The pointwise constraint (ignoring ∇v) becomes:
μ|v|² + ρ|v|^{10/3} ≥ 1 for |v| > λ

This is a 1D optimization in |v|. Solve: find the minimum of μr² + ρr^{10/3} for r > λ. Set equal to 1 to get the dual constraint.

**Key question:** Does the div-free constraint help? Compare:
- Dual optimal value WITHOUT div-free → standard Chebyshev tightness
- Dual optimal value WITH div-free → NS-constrained Chebyshev tightness
- If they're equal: div-free doesn't help. If different: there's room.

### Task 3: Implement and solve

Write a Python script using CVXPY (or scipy.optimize) to solve:

1. **The pointwise dual** (no div-free, no spatial structure):
   - Optimize μ, ρ to minimize μE² + ρS^{10/3} subject to μr² + ρr^{10/3} ≥ 1 for all r > λ
   - This should reproduce the standard Chebyshev bound (verify!)

2. **The finite-dimensional primal** (with div-free):
   - Grid search or random sampling over div-free Fourier fields
   - For each div-free u with ||u||_{L^2} = E, ||∇u||_{L^2} = D, ||u||_{L^{10/3}} = S:
     compute |{|u| > λ}| and compare with λ^{-10/3} S^{10/3}
   - Find the field that MAXIMIZES the ratio |{|u|>λ}| / (λ^{-10/3} S^{10/3})

3. **The finite-dimensional dual with div-free** (if feasible):
   - Add the div-free constraint to the dual
   - Does the dual value decrease? (Lower dual → tighter constraint → div-free helps)

### Task 4: Test with concrete parameters

Use parameters from DNS:
- E = ||u||_{L^2} from Taylor-Green at Re = 500
- D = ||∇u||_{L^2} from the same
- S = ||u||_{L^{10/3}} from the same
- λ = various thresholds (50%, 70%, 90% of max|u|)

Compare:
- Chebyshev prediction: λ^{-10/3} S^{10/3}
- SDP optimal: max |{|u|>λ}| over div-free fields with these norms
- DNS actual: |{|u|>λ}| from the Taylor-Green simulation

### Task 5: Interpret for β

If the SDP shows Chebyshev is tight under NS constraints:
- State the result precisely: "For div-free fields in H¹(T³) with ||u||_{L^{10/3}} = S, we have max |{|u|>λ}| = λ^{-10/3} S^{10/3} (up to constants)."
- This means: the Chebyshev step in Vasseur's proof cannot be improved by exploiting div-free + energy + Sobolev structure.
- Combined with E001's sensitivity table: this PROVES the 4/3 is the best achievable within the De Giorgi framework.

If the SDP shows Chebyshev is NOT tight:
- Quantify the gap: how much better can |{|u|>λ}| be under div-free constraints?
- Translate to β: if the gap is δ, what does β become? (Use the sensitivity from E001)
- This would be EXTREMELY surprising given E003's circularity argument.

## Success Criteria

1. Pointwise dual solved and verified to reproduce Chebyshev [REQUIRED]
2. Finite-dimensional primal solved for at least N=4 with div-free constraint [REQUIRED]
3. Comparison of primal value (div-free) vs Chebyshev bound (unconstrained) [REQUIRED]
4. Interpretation for β: does the gap (if any) affect the De Giorgi exponent? [REQUIRED]
5. DNS comparison at concrete parameter values [DESIRED]

## Failure Criteria

- Formulating the problem but not solving it computationally
- Solving only the pointwise dual without the div-free constraint (this would just reproduce Chebyshev)
- No interpretation for β

## Key References

- Strategy-002 E001: sensitivity table for the De Giorgi chain
- Strategy-002 E003: circularity of Chebyshev improvement (β = 1+s/n)
- Strategy-002 E007: adversarial review recommending SDP formalization
- Bandeira, Mixon, et al.: SDP relaxations for optimization over structured function spaces
- CVXPY documentation: https://www.cvxpy.org/

## Important Notes

- **Tag all results** with [VERIFIED], [COMPUTED], [CHECKED], [CONJECTURED].
- **The key comparison is WITH vs WITHOUT div-free.** The unconstrained Chebyshev is known to be tight (just take f = λ+ε on a set of appropriate measure). The question is whether div-free changes this.
- **Start with the simplest version.** The pointwise dual (no spatial structure) is the baseline. Then add div-free. If div-free doesn't help even at N=4, it very likely doesn't help at all.
- **The result either way is valuable.** Tight → formal sharpness. Not tight → surprising discovery that would reopen the constructive program.
- **Watch for boundary effects.** Working on T³ (periodic box) means all fields have zero mean. This might affect the optimization.
