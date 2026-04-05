# Exploration 006 Summary: Non-CZ Pressure Handling

## Goal
Test whether bypassing Calderón-Zygmund bounds on P^{21} — via integration by parts, H^1/BMO duality, W^{-1,q'}/W^{1,q} pairing, or CRW commutators — can improve the De Giorgi recurrence exponent beyond β = 4/3.

## What was tried
Computed U_{k-1} exponents for three non-CZ analytical routes. Ran DNS (Taylor-Green N=64/Re≈500, Kida-Pelz N=64/Re≈1000) comparing CZ vs direct bounds numerically. Surveyed 12 published approaches to pressure handling in NS regularity theory.

## Outcome: NEGATIVE — No non-CZ route improves β

**Three routes computed:**
- **Direct IBP:** β = 1 (WORSE — loses the CZ consolidation gain of 1/3)
- **H^1/BMO duality:** β = 4/3 (SAME — exponent invariant under CZ↔BMO exchange)
- **CRW commutator variant:** β ≤ 1 (SAME as direct — bounded multiplier blocks improvement)

**DNS confirms:** CZ bound is 2–3× tighter than direct bound at low k. Both overestimate I_k by 5–20×. Effective β_eff ≈ 2–3 in practice.

**Literature confirms:** No published work achieves β > 4/3 by any method. Curl formulation (Vasseur-Yang 2021) reproduces β = 4/3 via vortex stretching, confirming cross-formulation universality.

## Verification scorecard
- **[COMPUTED]:** 12 claims (exponent analysis for 3 routes, DNS bounds at 4 levels, α(p) table, consolidation gain ratios)
- **[CHECKED]:** 4 claims (literature cross-references)
- **[CONJECTURED]:** 4 claims (deep reason for tool-independence, open directions)
- **[VERIFIED]:** 0

## Key takeaway
**β = 4/3 is tool-independent.** The CZ consolidation gain (mapping the bilinear product to a single L^p function) is essential — it extracts exactly 1/3 from the Chebyshev level-set measure. The H^1/BMO route reproduces this same 1/3 through a different mechanism (BMO absorbs P^{21}, H^1 of v_k carries the full 4/3). The exponent is locked to the NS quadratic structure, not to the analytical tool.

## Unexpected findings
- **CZ becomes loose at high k:** The ratio ||P^{21}||_{L^{3/2}} / ||v_{k-1}||_{L^2}^2 grows from 0.2 (k=2) to 92 (k=5). CZ consolidation is most effective at low De Giorgi levels and increasingly wasteful at high levels.

## Computations identified
1. **Wolf's local harmonic+particular pressure decomposition** applied within De Giorgi iteration — genuinely CZ-free, structurally different from P^{ij}, untested for β.
2. **Tran-Yu nonlinearity depletion quantified at De Giorgi levels** — the 5–20× overestimate gap may be explained by |u|–|∇|u|| correlation.

## Proof gaps identified
- The claim "β = 4/3 is optimal across all analytical tools" is supported by computation on 3 routes but lacks a formal proof of optimality.
