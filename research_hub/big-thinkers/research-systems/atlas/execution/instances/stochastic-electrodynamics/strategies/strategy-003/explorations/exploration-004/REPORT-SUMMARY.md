# Exploration 004 — Report Summary

## Goal
Final adversarial synthesis of all novel claims from SED Strategies 1–3, prior art search on "field quantization necessity," and grand synthesis answering the central mission question.

## What Was Tried
- Web searches on 7 key papers: Santos (2022), Boyer (2019), Nieuwenhuizen (2015, 2020), de la Peña & Cetto (2014), Pesquera & Claverie (1982), Faria-França-Sponchiado (2005/2006), Ibison & Haisch (1996)
- Full fetch of Nieuwenhuizen (2020) Frontiers paper and arXiv abstracts for Santos, Boyer
- Adversarial review of all 7 claims (S1-A through S3-C)
- Prior art search for "field quantization is necessary" as an explicit prior conclusion

## Outcome: Tier 4 (Good Success)

### Prior Art Situation — Critical Finding
The grand synthesis conclusion ("field quantization is necessary for nonlinear systems") is NOT genuinely novel:
- **Santos (2022)** proves SED = O(ħ) QED exactly, and fails for nonlinear systems at O(ħ²) — the mathematical implication is clear even without an explicit sentence
- **Nieuwenhuizen (2020)** states it explicitly in the hydrogen context: "SED is not a basis for quantum mechanics" after exhausting all renormalization fixes
- **Boyer (2019)** implicitly accepts it ("closest classical *approximation*")
- **de la Peña & Cetto (2014)** explicitly deny it (they believe LSED can reproduce QM) — the debate is live in the literature

### Claim Verdicts
| Claim | Verdict | Novelty |
|-------|---------|---------|
| S1-A: First numerical simulation quartic oscillator, 17.8% excess | PARTIALLY VERIFIED | 3/5 |
| S1-B: ω³ positive feedback mechanism | CONJECTURED | 2/5 |
| S2-A: Tunneling ratio formula R²=0.9998 | PARTIALLY VERIFIED | 2/5 |
| S2-B: ω_local=√2 universality | VERIFIED (trivial) | 1/5 |
| S2-C: ω³ unified root cause | CONJECTURED | 2/5 |
| S2-D: 1D correlator C_xx=cos(ω₀d/c) | PARTIALLY VERIFIED | 2/5 |
| S3-A: T_ion(L) power law, L=1.0 → 19,223 periods | PARTIALLY VERIFIED | 3/5 |
| S3-B: 3D correlator C_xx=j₀−j₂/2 | VERIFIED (standard) | 2/5 |
| S3-C: Hierarchy 0.183 < 0.257 < 0.303 | PARTIALLY VERIFIED | 3/5 |

### Key Takeaway
**The mission's best and honestly novel output is the convergence law: Δ(⟨x²⟩) ∝ τ^{0.23} × ω_max^{-0.18} for the quartic oscillator.** This quantitatively demonstrates that the SED failure is physically irreducible — not just "hard to fix." No prior paper appears to have this specific result.

The next-best contribution is the **T_ion(L) power law** T_ion ≈ 37,527 × L^{6.44} for hydrogen with physical τ, which extends Nieuwenhuizen's qualitative observation to a quantitative table.

The grand synthesis conclusion ("field quantization is necessary") is valid and well-supported but is not a new claim. Our contribution is systematic quantitative evidence across three systems in one investigation — a compilation argument, not a conceptual breakthrough.

## Leads Worth Pursuing
- None urgent. The SED mission has been thorough and reached a clear conclusion.
- The de la Peña/Cetto "Emerging Quantum" framework has not been quantitatively tested against our specific numbers (e.g., does their LSED predict a different ⟨x²⟩ for the quartic oscillator?). This is a potential future adversarial target.
- The C_xx(d) correlator as an experimental discriminant (SED predicts nonzero inter-site correlations; QM predicts zero for uncoupled oscillators) is an unexplored experimental proposal.

## Unexpected Findings
- **Nieuwenhuizen (2020) conclusion is stronger than expected**: he explicitly says "SED is not a basis for quantum mechanics" — a clear, definitive statement from an SED practitioner who spent years trying to make hydrogen work. This weakens any claim that our grand synthesis is novel.
- **de la Peña & Cetto remain unrefuted on their own terms**: They have a different theoretical program (LSED vs classical SED) that avoids some failures by design. The fact that their optimistic program has never produced specific quantitative predictions for nonlinear systems that could be tested against our numbers is itself informative.

## Computations Identified
None new. All computationally intensive work has been completed in prior strategies. The convergence law (τ^{0.23} × ω_max^{-0.18}) was computed in Strategy-001 and is the single most robust quantitative output from the mission.
