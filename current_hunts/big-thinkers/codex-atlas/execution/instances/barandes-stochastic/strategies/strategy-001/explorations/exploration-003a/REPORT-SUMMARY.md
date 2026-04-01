# Exploration 003a — Summary

## Goal
For a qubit (N=2), explicitly construct the phase freedom space (Barandes) and the consistent history family space (CH), then compare their dimensions and structure.

## What Was Done
1. **Phase freedom:** Analytically parameterized all unitary Θ with |Θ_ij|² = Γ = [[½,½],[½,½]]. Found dim = 2 (T² topology). Verified with 1000 numerical samples.
2. **Consistent histories:** For 3-time histories (t₀, t₁, t₂) with pure initial state ρ₀ = |+⟩⟨+|, proved analytically and numerically that t₁ must be the eigenbasis of the evolved state {|+⟩, |−⟩}, while t₂ is completely unconstrained (any basis is consistent). Consistent family space has dim = 2 (S² topology).
3. **General N scaling:** Computed phase freedom and realm selection dimensions for N = 2–6 via Jacobian rank analysis at solution points.

## Outcome: Partial match (coincidental)

**Verification scorecard:** 9 [VERIFIED], 3 [COMPUTED], 1 [CONJECTURED]

## Key Takeaway

**The dimensions match at N=2 (both = 2), but this is coincidental.** The spaces have different topologies (T² vs S²), and the match breaks immediately at N > 2 (phase freedom = 4 vs realm selection = 6 at N=3; diverges further for larger N). No structural map between the spaces was found.

## Important Secondary Results

- **Asymmetric consistency structure in CH:** For pure-state 3-time qubit histories, the t₁ basis is completely determined (must be eigenbasis of ψ₁), but t₂ is fully free. This asymmetry stems from the rank-1 nature of ρ₀.
- **Jacobian rank reduction at solutions:** For uniform Γ, the complex unitarity constraints have Jacobian rank strictly less than 2× the number of complex equations (due to proportional gradients at solutions). This is crucial for correct dimension counting.
- **Phase freedom grows sub-quadratically** in N (empirical: 2, 4, 7, 8, 14 for N = 2–6) while realm selection grows as N(N−1) (quadratic). No clean formula found for phase freedom.

## Proof Gaps
- The coincidence at N=2 may not be entirely coincidental — a deeper analysis of the relationship between Hadamard-type phase freedom and flag manifold dimensions could reveal structure. Worth investigating with mixed initial states (where CH becomes more constrained).

## Unexpected Findings
- For the specific system (H = σ_x, ρ₀ = |+⟩⟨+|), the evolved state stays proportional to |+⟩ at all times (energy eigenstate). This makes the "natural" consistent family deterministic (P(+,+) = 1). The system is special in this regard — a generic Hamiltonian would give a non-trivial t₁ constraint and more interesting probability distributions.

## Computations for Later
- Repeat with mixed initial state ρ₀ (rank > 1) where CH constraints become more complex
- Test with non-uniform Γ (different Hamiltonian or evolution time)
- Investigate whether the gauge group structure (2N−1 dimensional diagonal rephasing) relates to the constraint rank deficit
