# Exploration 005 Summary: Cross-Term Decoherence Lemma

## Goal
Prove ||C(Q)|| ≤ 2(d+1) for all Q (the decoherence lemma), completing the mass gap proof at β < 1/(2d).

## Outcome: CRITICAL NEGATIVE + PARTIAL POSITIVE

**The decoherence lemma is FALSE for d ≥ 3.** Adversarial gradient ascent found ||C|| = 11.68 > 10 = 2(d+1) at d=4 (verified, SU(2) errors < 10⁻¹⁵). Also ||C|| = 8.60 > 8 at d=3. The counterexample is near an anti-instanton where D ≈ 0.

**The lemma IS true for d = 2.** Proved via per-plaquette Cauchy-Schwarz + lattice aggregation matching the signed adjacency.

## Verification Scorecard
- **[VERIFIED] ×3**: F = -2(β₀I+[β⃗×])R formula, per-plaquette ||C_□|| ≤ 3, d=2 decoherence
- **[COMPUTED] ×4**: d≥3 counterexamples, gradient ascent landscape, aligned/misaligned norm analysis, dimension scaling
- **[CONJECTURED] ×0**

## Key Takeaway
The β < 1/(2d) mass gap bound CANNOT be obtained by bounding D and C separately. The counterexample has ||C|| > 2(d+1) but |λ(H)| < 4d, because |D| is small. The full Hessian satisfies |λ(H)| < 4d in ALL tested configs, but via D/C anti-correlation, not individual bounds.

## Proof Gaps Identified
1. The per-plaquette bound ||C_□|| ≤ 3 (proved) loses inter-plaquette sign structure when aggregated
2. The aggregation bound ||C|| ≤ ||A_struct|| matches the target only for d=2 (where ||A_struct|| = ||A_total||)
3. For d ≥ 3, ||A_struct|| > ||A_total|| because unsigned overlap exceeds signed overlap

## Unexpected Findings
- **F has closed-form SVD**: singular values exactly (2, 2, 2|β₀|) where β₀ = Re Tr(MN)/2
- **Counterexample to decoherence**: flat is NOT the global max of ||C|| — anti-instanton + GD achieves 17% above
- **D/C anti-correlation is structural**: configs maximizing ||C|| have D ≈ 0, keeping |λ(H)| bounded

## Computations for Next Steps
1. Prove |λ(H)| ≤ 4d directly (bypassing D/C decomposition) — most promising path
2. Formalize the D/C anti-correlation: if |D| ≤ δ then ||C|| ≤ f(δ) with δ + f(δ) ≤ 4d
3. Try alternative Hessian decompositions (e.g., by plaquette groups, Fourier modes)
