<!-- explorer-type: math -->

# Exploration 004: Commutator / Compensated Compactness Analysis of the De Giorgi Bottleneck

## Goal

Determine whether the bottleneck integral in the De Giorgi iteration for 3D Navier-Stokes has compensated compactness structure (div-curl type) that could be exploited via Hardy space estimates to improve the recurrence exponent beyond β = 4/3. This is the "Route 3" attack identified by exploration-003 as the most promising remaining direction.

## Background

### The state of play

Strategy-002 explorations 001 and 003 have established:

1. **The 4/3 = 1/2 + 5/6 decomposition has exactly one potentially improvable step:** the Chebyshev estimate on the level set |{v_{k-1} > 2^{-k}}|. All other steps are provably sharp.

2. **BUT: the Chebyshev step is NOT independently improvable.** Improving it from L^{10/3} to L^4 is equivalent to improving regularity from H^1 to H^{5/4} — circular with the regularity problem itself. The universal formula β = 1 + s/n confirms this.

3. **The SQG precedent shows a different mechanism works.** In Caffarelli-Vasseur (2010), the drift enters the De Giorgi iteration as a commutator [(-Δ)^{1/2}, u·] rather than as a product. This commutator structure provides an extra power of U_{k-1} that the standard product estimate misses. SQG in the Caffarelli-Silvestre extension has the SAME β = 4/3 as 3D NS at the Chebyshev level — the improvement is entirely in how the drift couples.

4. **The NS bottleneck integral is a bilinear form of div-free fields.** The key term is:

   I_k = ∫∫ P_{k21} · v_k · 1_{v_k > 0} dx dt

   where P_{k21} = -Δ^{-1} ∂_i∂_j (u_i^{below} · u_j^{above}) is the Calderón-Zygmund transform of a product of two velocity fields (one truncated below, one above). The product u^{below} ⊗ u^{above} involves div-free fields — exactly the setting where Coifman-Lions-Meyer-Semmes (1993) compensated compactness gives Hardy space H^1 improvements.

### The CLMS theorem (key tool)

Coifman-Lions-Meyer-Semmes (1993): If E ∈ L^p(R^n), B ∈ L^q(R^n) with 1/p + 1/q = 1, and div(E) = 0 and curl(B) = 0, then E · B ∈ H^1(R^n) (the real Hardy space). This is stronger than L^1 — Hardy space H^1 has better duality properties (dual is BMO, not L^∞).

The question: does the bilinear form in P_{k21} have this div-curl structure?

### What needs to be checked

The bottleneck term in Vasseur's proof involves:
1. P_{k21} is a Calderón-Zygmund singular integral of u^{below} ⊗ u^{above}
2. u^{below} = u · β_{k-1}(|u|)/|u| is approximately div-free (truncation introduces a compressibility error)
3. u^{above} = u - u^{below} is supported on {|u| > λ_{k-1}}

The CLMS improvement would apply if:
- One factor is (approximately) divergence-free
- The other factor is (approximately) curl-free (or a gradient)
- The product goes through a CZ transform

## Specific Computation Tasks

### Task 1: Write out the exact bilinear form

Starting from Vasseur (2007) Proposition 3, write the bottleneck integral I_k explicitly:
- What are the exact expressions for u^{below} and u^{above} in terms of the truncation β_k?
- What is the exact form of P_{k21} = R_i R_j (u_i^{below} · u_j^{above}) where R_i = ∂_i(-Δ)^{-1/2} are Riesz transforms?
- Write I_k = ∫∫ F(u^{below}, u^{above}, v_k) dx dt with all terms explicit.

### Task 2: Check div-curl structure

For the bilinear form in I_k:
1. **Divergence of u^{below}:** Compute div(u^{below}) = div(u · min(1, λ_{k-1}/|u|)). Since div(u) = 0, this is:
   div(u^{below}) = u · ∇(min(1, λ_{k-1}/|u|))
   This is NON-ZERO but supported only on {|u| > λ_{k-1}} and bounded by |∇|u||. Quantify: how large is this compressibility error relative to the main term?

2. **Structure of u^{above}:** Is u^{above} = u · (1 - min(1, λ_{k-1}/|u|)) related to a gradient? Probably not directly, but check whether R_i R_j(u_i^{below} u_j^{above}) has any special structure when both factors come from the same velocity field u.

3. **Test numerically:** On DNS data (reuse Strategy-001 code at `../strategy-001/explorations/exploration-002/code/`):
   - Compute div(u^{below}) and quantify ||div(u^{below})||_{L²} / ||u^{below}||_{H¹}
   - Compute the bilinear form u^{below} ⊗ u^{above} and test whether its CZ transform R_i R_j(u_i^{below} u_j^{above}) has better integrability than L^1 (test: is it in a Lorentz space L^{1,q} with q < ∞?)

### Task 3: Analyze the SQG commutator mechanism

In Caffarelli-Vasseur (2010), the key step that beats β = 4/3 is a commutator estimate:
[(-Δ)^{1/2}, u·]f = (-Δ)^{1/2}(uf) - u·(-Δ)^{1/2}f

This commutator is more regular than either term alone (it gains a derivative). Write out:
1. What the SQG commutator estimate gives (what power of U_{k-1} does it produce?)
2. What the analogous object would be for NS: is there a "commutator" form of P_{k21}?
3. Specifically: can P_{k21} be written as P_{k21} = [R_iR_j, u^{below}·]u_j^{above} + lower-order? If so, does the commutator [R_iR_j, u^{below}·] gain regularity?

The Coifman-Rochberg-Weiss (1976) commutator theorem says [R_i, b]f ∈ L^p if b ∈ BMO and f ∈ L^p. Check whether this applies.

### Task 4: Compute the improvement (if any)

If Tasks 2 or 3 identify exploitable structure:
1. **Quantify the improvement.** Instead of ||P_{k21}||_{L^{3/2}} ≤ C ||u^{below}||_{L^3} ||u^{above}||_{L^3} (the standard CZ bound), does the compensated compactness or commutator structure give ||P_{k21}||_{H^1} ≤ C ||u^{below}||_{L^2} ||u^{above}||_{L^2} (or similar)?
2. **Trace through the De Giorgi chain.** If P_{k21} has better integrability by δ (e.g., L^{3/2+δ} instead of L^{3/2}), what does the full recurrence exponent become? Use the sensitivity table from exploration-001.
3. **Check for poison pills.** Does the improvement in one step worsen another step? (The "flat optimization" finding from E003 means we need to be very careful here.)

If no exploitable structure is found:
1. Explain precisely WHY the div-curl / commutator structure fails for NS. What property of the NS nonlinearity prevents the CLMS improvement?
2. Compare with what makes SQG different — identify the specific structural gap.

## Success Criteria

1. Explicit bilinear form of I_k with all terms written out [REQUIRED]
2. Quantification of div(u^{below}) compressibility error (analytical + numerical) [REQUIRED]
3. Verdict on CLMS applicability with specific mathematical argument [REQUIRED]
4. Analysis of commutator reformulation possibility [REQUIRED]
5. If improvement found: full pipeline trace showing net effect on β [CONDITIONAL]
6. If no improvement: precise identification of the structural obstruction [CONDITIONAL]

## Failure Criteria

- Vague claims about "compensated compactness might help" without computing the specific bilinear form
- No numerical verification of the compressibility error
- Missing the SQG comparison

## Key References

- Vasseur (2007): arXiv:0607017, Proposition 3 — the bottleneck integral
- Coifman-Lions-Meyer-Semmes (1993): "Compensated compactness and Hardy spaces" — the div-curl theorem
- Coifman-Rochberg-Weiss (1976): "Factorization theorems for Hardy spaces" — commutator estimates
- Caffarelli-Vasseur (2010): "Drift diffusion equations with fractional diffusion and the quasi-geostrophic equation" — SQG success mechanism
- Strategy-001 code: `../strategy-001/explorations/exploration-002/code/` — DNS solver and De Giorgi measurement
- Strategy-002 E001: decomposition audit (sensitivity table)
- Strategy-002 E003: analytical Chebyshev analysis (Route 3 identification, SQG mechanism)

## Important Notes

- **Tag all results** with [VERIFIED], [COMPUTED], [CHECKED], [CONJECTURED].
- **Worst-case discipline:** If a compensated compactness improvement is found, it must work for ARBITRARY suitable weak solutions, not just smooth DNS. The improvement must be in the analytical bound, not just a numerical observation.
- **The compressibility error is critical.** Truncation breaks div-free. If div(u^{below}) is O(1) (not small), CLMS cannot apply directly. Quantify this error FIRST before pursuing the full analysis.
- **Reuse existing DNS code.** The spectral solver and De Giorgi truncation infrastructure from Strategy-001 exist. Extend; don't rewrite.
