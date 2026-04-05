<!-- explorer-type: standard -->

# Exploration 003: Analytical Chebyshev Improvement and Model PDE Comparison

## Goal

Determine whether the Chebyshev estimate |{v_{k-1} > 2^{-k}}| ≤ C^k U_{k-1}^{5/3} can be analytically improved for Navier-Stokes solutions by exploiting structural properties (divergence-free, energy inequality, NS dynamics). Additionally, test the universality of the 4/3 barrier by analyzing whether the same Chebyshev step produces 4/3 on model PDEs.

## Background

Strategy-002 exploration-001 (decomposition audit) identified the Chebyshev inequality at the truncation level set as the **only potentially improvable step** in the entire De Giorgi chain for Vasseur (2007) Proposition 3. The other 4 steps are provably sharp.

The Chebyshev estimate uses:
|{|f| > λ}| ≤ λ^{-p} ||f||_{Lp}^p

with p = 10/3 (from the parabolic L^{10/3} embedding). This is sharp for ARBITRARY L^{10/3} functions. But NS solutions are not arbitrary:
- u is divergence-free: div(u) = 0
- u satisfies the energy inequality: d/dt ∫|u|² + 2ν∫|∇u|² ≤ 0
- u solves NS: the dynamics constrain the spatial structure
- The truncated velocity v_k inherits partial structure from u

**The question:** Do any of these structural constraints improve the level-set estimate?

## Specific Tasks

### Task 1: Survey distributional estimates for structured function classes

Search the mathematical literature for results on how structural constraints improve level-set estimates. Specifically:

1. **Divergence-free constraint:** For div-free vector fields in L^p(R³), are there better distributional estimates than Chebyshev? Key references to check:
   - Coifman-Lions-Meyer-Semmes (1993): div-curl estimates give Hardy space H¹ improvements
   - Bourgain-Brezis (2004, 2007): improved estimates for div-free and curl-free fields
   - Does div(u) = 0 constrain the distribution function μ(λ) = |{|u| > λ}|?

2. **Energy + Sobolev constraint:** For f ∈ H¹(R³) ∩ L²(R³) with ||∇f||_{L²} ≤ E, does the combined L² + H¹ membership give a better level-set bound than either alone? The De Giorgi functional U_k includes BOTH ||v_k||_{L²} and ||∇v_k||_{L²}. Could the joint constraint be exploited?

3. **Parabolic constraint:** For functions in L^{10/3}(R³ × [0,T]) that also satisfy a parabolic PDE, are there improved distributional estimates? Parabolic regularity gives additional spatial smoothness that generic L^{10/3} functions don't have.

### Task 2: Analyze the specific Chebyshev application in De Giorgi

The Chebyshev bound is applied to a SPECIFIC function: v_{k-1} = [|u| - (1-2^{-(k-1)})]_+. This truncation has structure:
- It's supported on a set that shrinks with k (the set where |u| exceeds the threshold)
- It inherits partial divergence-free structure from u (though truncation breaks div-free exactly)
- Its L^{10/3} norm is bounded by U_{k-1}^{1/2} × (Sobolev embedding)

Analyze: Can the truncation structure (supported on shrinking sets, controlled gradient) improve the distributional estimate? The key geometric question: for a function supported on a set of measure M, does the level-set distribution λ^{-p}||f||_p^p have a correction term involving M?

### Task 3: Test on model PDEs (universality check)

Apply the De Giorgi framework to model PDEs and track what the Chebyshev step produces:

1. **1D Burgers equation:** u_t + uu_x = νu_xx. Quadratic nonlinearity in 1D. What does the De Giorgi iteration give? What Sobolev embedding is used? Is the Chebyshev step sharp? Expected β = ?

2. **2D surface quasi-geostrophic (SQG):** θ_t + u·∇θ = -κ(-Δ)^α θ, u = ∇⊥(-Δ)^{-1/2}θ. Quadratic nonlinearity in 2D with fractional diffusion. De Giorgi methods have been successfully applied to SQG (Caffarelli-Vasseur 2010). What β do they achieve? Is it 4/3 or different?

3. **3D MHD equations:** quadratic but with different algebraic structure (magnetic tension vs Reynolds stress). If De Giorgi has been applied, what β results?

For each model PDE:
- Identify the Chebyshev step and note the embedding exponent p
- Determine whether β = 1/2 + (p-2)/(2p) × dimension or some other formula
- If β ≠ 4/3, identify which structural difference causes the deviation

### Task 4: Synthesize

Based on Tasks 1-3, produce a verdict:
- **Is there a known analytical improvement to Chebyshev for NS solutions?** (Yes/No with reference)
- **Is the 4/3 universal across model PDEs?** (List of β values by PDE)
- **What is the most promising analytical route to improving the Chebyshev step?** (Ranked list)

## Success Criteria

1. Survey of ≥ 3 relevant papers on distributional estimates for structured (div-free, energy-bounded) functions
2. Analysis of the specific truncation structure and whether it helps
3. De Giorgi β values (or equivalent) for at least 2 model PDEs
4. A clear ranked list of the most promising routes to improving the Chebyshev step

## Failure Criteria

- Only reproducing standard Chebyshev with no analysis of NS-specific improvements
- No model PDE comparison
- Vague conclusions without specific mathematical arguments

## Key References

- Vasseur (2007): arXiv:0607017, Proposition 3
- Caffarelli-Vasseur (2010): "Drift diffusion equations with fractional diffusion and the quasi-geostrophic equation" — De Giorgi for SQG
- Coifman-Lions-Meyer-Semmes (1993): compensated compactness and Hardy spaces
- Bourgain-Brezis (2004, 2007): div-free L^p estimates
- Strategy-001 exploration-008: vorticity De Giorgi gives same 4/3
- Strategy-002 exploration-001: decomposition audit identifying Chebyshev as the single target

## Notes

- This is a READING and ANALYSIS task. No computation needed.
- Be precise about what is PROVEN vs CONJECTURED. If you find a result that could improve Chebyshev, state exactly what the improvement would be (quantitatively) and what conditions are required.
- The Caffarelli-Vasseur (2010) SQG result is particularly important because they used De Giorgi methods and SUCCEEDED (proving regularity). Understanding why they succeeded where NS fails is critical.
- If the literature has nothing on improved distributional estimates for div-free fields, say so explicitly — that itself is a valuable finding (it means this direction is genuinely unexplored, not just unfruitful).
