<!-- explorer-type: math -->

# Exploration 006: Non-CZ Pressure Handling — Direct Energy Estimates Bypassing Calderón-Zygmund

## Goal

Determine whether the pressure contribution to the De Giorgi iteration can be estimated WITHOUT using Calderón-Zygmund singular integral bounds on P^{21}. Specifically, test whether integration by parts on the pressure Poisson equation Δp = -∂_i∂_j(u_iu_j) produces a bound on the bottleneck integral ∫∫P^{21}·v_k that gives a better U_{k-1} exponent than the standard CZ route.

## Background

### Why this is the last constructive direction

Strategy-002 explorations 001-005 have systematically closed ALL standard analytical improvements within the CZ framework:
- E001: All free parameters optimized. Only the Chebyshev step has potential slack.
- E003: Chebyshev is NOT independently improvable (circular with regularity). β = 1+s/n universal.
- E002: DNS confirms constant slack only (no U_{k-1}^{-δ} scaling).
- E004: Compensated compactness/commutator methods fail (3 independent obstructions).
- E005: LP frequency decomposition fails (Bernstein penalty, CZ optimal freq-by-freq).

**Every one of these explorations accepted CZ as the tool for handling pressure.** The chain is:
1. P^{21} = R_iR_j(u_i^{below} · u_j^{above}) via CZ
2. ||P^{21}||_{L^{3/2}} ≤ C ||u^{below}||_{L^3} ||u^{above}||_{L^3} via CZ boundedness on L^{3/2}
3. Substitute into the bottleneck integral using Hölder

The question is: what if we never invoke CZ at all?

### The alternative approach

The pressure satisfies Δp = -∂_i∂_j(u_iu_j). For the truncated pressure P^{21}:

∫∫ P^{21} · v_k dx dt

Instead of bounding ||P^{21}||_{L^p} first, we could:
1. Use the weak formulation: ∫P^{21}·v_k = ∫(-Δ)^{-1}∂_i∂_j(u_i^{below}·u_j^{above}) · v_k
2. Integrate by parts: move derivatives from the CZ kernel onto v_k or onto the product u^{below}·u^{above}
3. This produces terms like ∫(u^{below}·u^{above})·∂_i∂_j(-Δ)^{-1}v_k or ∫(u^{below}·u^{above})·(Riesz transforms of v_k)

The hope: distributing derivatives differently might avoid the exponent configuration that forces β = 4/3.

### What could go wrong

1. Integration by parts might reintroduce CZ in disguise (Riesz transforms on v_k are still CZ operators)
2. The NS-specific pressure decomposition P = P^{11} + P^{12} + P^{21} + P^{22} might be essential — a direct approach might lose the beneficial cancellation between pieces
3. The De Giorgi truncation complicates integration by parts (v_k = [|u| - λ_k]_+ is Lipschitz but not smooth)

## Specific Computation Tasks

### Task 1: Write out the direct estimate

Starting from I_k = ∫∫ P^{21}_k · v_k · 1_{v_k>0} dx dt:

1. Substitute P^{21} = (-Δ)^{-1}∂_i∂_j(u_i^{below} · u_j^{above})
2. Integrate by parts to move the ∂_i∂_j(-Δ)^{-1} operator onto v_k:
   I_k = ∫∫ (u_i^{below} · u_j^{above}) · R_iR_j(v_k · 1_{v_k>0}) dx dt
   (where R_i = ∂_i(-Δ)^{-1/2} are Riesz transforms)
3. Now the CZ operator acts on v_k, not on u^{below}·u^{above}. What are the available bounds on ||R_iR_j(v_k)||_{Lp}?
4. Apply Hölder to the product. What is the resulting bound on I_k in terms of U_{k-1}?

**Key check:** Does this just reproduce the same exponent configuration as the standard CZ route but from the other side?

### Task 2: Test the "pressure as test function" approach

An alternative: instead of integration by parts, treat the pressure integral as a duality pairing:

I_k = <P^{21}, v_k · 1_{v_k>0}>

If we can bound v_k · 1_{v_k>0} in a space X such that P^{21} ∈ X* with a better bound, we improve.

Candidates for X:
- H^1 (Hardy space): then X* = BMO. Is P^{21} ∈ BMO? What's the BMO norm?
- W^{1,q} for some q: the De Giorgi functional controls ||∇v_k||_{L^2}, so v_k ∈ H^1 ⊂ L^6.
- Lorentz spaces L^{p,q}: might give logarithmic improvements.

For each candidate, compute: what exponent does the duality pairing give?

### Task 3: The "commutator with test function" variant

A third approach: write

I_k = ∫∫ u_i^{below} · u_j^{above} · R_iR_j(v_k · 1_{v_k>0}) dx dt
    = ∫∫ u_j^{above} · [R_iR_j, u_i^{below}](v_k · 1_{v_k>0}) dx dt + ∫∫ u_j^{above} · u_i^{below} · R_iR_j(v_k · 1_{v_k>0}) dx dt

The commutator [R_iR_j, u_i^{below}] gains regularity by CRW theorem (if u^{below} ∈ BMO).

But wait — E004 already checked CRW and found no improvement for bounded multipliers. Does moving CZ to the other side of the pairing change this? Analyze carefully.

### Task 4: Numerical test on DNS

Using existing DNS infrastructure:

1. Compute I_k via both routes:
   - Standard CZ route: bound ||P^{21}||_{L^{3/2}}, then Hölder
   - Direct route: compute ∫(u^{below}·u^{above})·R_iR_j(v_k) numerically

2. Compare the effective U_{k-1} exponents from both routes. Are they the same or different?

3. If different: which route gives a better bound at each De Giorgi level k?

### Task 5: Survey existing non-CZ pressure approaches

Search for any published De Giorgi or partial regularity approaches to NS that handle pressure differently:
- Does Caffarelli-Kohn-Nirenberg (1982) use CZ?
- Does the original De Giorgi-Nash-Moser theory for scalar equations have a pressure analog?
- What about Seregin-Šverák or Escauriaza-Seregin-Šverák?
- Has anyone applied De Giorgi to NS with pressure handled via energy methods?

## Success Criteria

1. At least two distinct non-CZ routes computed explicitly with resulting U_{k-1} exponents [REQUIRED]
2. Verdict: does any non-CZ route improve β beyond 4/3? [REQUIRED]
3. If improvement: full pipeline trace through De Giorgi chain [CONDITIONAL]
4. If no improvement: identify whether the non-CZ route gives the SAME exponent (suggesting the 4/3 is independent of the method) or a WORSE exponent (CZ is actually helpful) [CONDITIONAL]
5. Numerical comparison of CZ vs non-CZ bounds on DNS data [REQUIRED]

## Failure Criteria

- Only describing the integration-by-parts idea without computing the exponents
- Missing the check for whether CZ is reintroduced in disguise
- No numerical verification

## Key References

- Vasseur (2007): arXiv:0607017 — standard CZ approach to pressure
- Caffarelli-Kohn-Nirenberg (1982): partial regularity for NS (pressure handling method)
- Strategy-002 E001: sensitivity table showing β = 4/3 chain
- Strategy-002 E004: CRW commutator bounds (no improvement for bounded multipliers)
- Strategy-001 code: `../strategy-001/explorations/exploration-002/code/`

## Important Notes

- **Tag all results** with [VERIFIED], [COMPUTED], [CHECKED], [CONJECTURED].
- **Watch for CZ in disguise.** If you move ∂_i∂_j(-Δ)^{-1} onto v_k, you're still applying a CZ operator (Riesz transforms). The question is whether the EXPONENT CONFIGURATION changes, not whether CZ disappears entirely.
- **The De Giorgi truncation 1_{v_k>0} complicates integration by parts.** It introduces a distributional boundary term on {v_k = 0}. Handle this carefully.
- **If all non-CZ routes give β = 4/3:** this is a STRONG result. It means the barrier is genuinely intrinsic to the NS nonlinear structure, independent of the analytical tool used to handle pressure. Worth stating precisely.
