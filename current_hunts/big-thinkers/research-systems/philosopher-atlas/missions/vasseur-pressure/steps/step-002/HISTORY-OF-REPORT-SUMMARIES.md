# History of Report Summaries — Step 2

## Exploration 001: H^1-BMO Duality Route (Branch 2B) — DEAD END

**Outcome:** H^1-BMO duality is provably no better than Hölder for the Vasseur De Giorgi pressure problem. Three independent structural reasons:

1. **BMO norm of ψ_k not U_k-controlled:** W^{1,2}(ℝ^3) ↛ BMO(ℝ^3) (need W^{1,3}). De Giorgi energy U_k only controls W^{1,2}, so ||ψ_k||_{BMO} cannot be bounded from U_k.

2. **Global H^1 norm = fixed constant:** ||p||_{H^1(ℝ^3)} ≤ C·E_0 (CLMS 1993). Same fixed constant as current far-field estimate. H^1-BMO does NOT make far-field coefficient U_k-dependent.

3. **H^1 localization fails:** φ_k · p ∉ H^1 when p ∈ H^1 (cutoffs destroy mean-zero atom structure). De Giorgi must localize to Q_k — this destroys H^1 structure.

**Bonus finding:** Even with hypothetical W^{1,3} regularity, H^1-BMO is WORSE than Hölder (loses U_k^{1/2} factor).

**Atomic decomposition (Branch 2C partial):** Mean-zero cancellation of atoms exactly saturates at the relevant scale (ρ ~ 2^{-2k}). No net gain.

**The #1 insight:** H^1 (global, cancellation-based) and De Giorgi (local, energy-based) are structurally incompatible. The W^{1,3} threshold is universal — both CZ ceiling and BMO control require it.

## Exploration 002: Interpolation Route (Branch 2A) — FAILURE

**Outcome:** No interpolation space (H^1, L^{4/3})_{θ,q} improves the De Giorgi pressure exponent. Three nested obstructions:

1. **Wrong Lebesgue direction:** Complex interpolation gives L^{p_θ} with p_θ < 4/3 — weaker, not stronger.
2. **Global-local mismatch:** Any H^1-involving interpolation norm of p is O(E_0) — the far-field pressure is never U_k-dependent.
3. **Cancellation waste:** H^1 atomic mean-zero cancellation requires oscillating test functions, but ψ_k ≥ 0 in De Giorgi, so all cancellation is wasted.

**W^{1,3} universality CONFIRMED:** Besov number computation shows W^{1,2} has number -1/2, W^{1,3} has number 0. Non-embedding confirmed.

**Unexpected:** Near-field pressure CAN give σ = 1 (linear). Only far-field gives σ = 1/2. The recursion "almost works."

---

## COMPLETE THREE-BRANCH OBSTRUCTION MAP

| Branch | Route | Primary Obstruction | Status |
|--------|-------|--------------------|----|
| 2B | H^1-BMO duality | W^{1,2} ↛ BMO; global H^1 = E_0; cutoffs destroy H^1 | DEAD END |
| 2C | Atomic decomposition | Mean-zero atoms saturate at scale ρ ~ 2^{-2k} | DEAD END |
| 2A | Interpolation | p_θ < 4/3; global E_0 bound; ψ_k ≥ 0 wastes cancellation | DEAD END |

**Kill condition MET:** All three branches fail. The W^{1,3} threshold is a genuine structural barrier.
