---
topic: TTH adversarial claims assessment — novelty ratings, prior art, attack verdicts
confidence: verified
date: 2026-03-28
source: thermal-time/strategies/strategy-003/explorations/exploration-002/REPORT.md (adversarial review)
---

## Summary

Systematic adversarial review of all TTH claims from the thermal-time mission: prior art search (arXiv, JHEP, PhilSci Archive), three conceptual attacks, and null hypothesis testing. **Claim 3 (excited-state modular flow) is the strongest result (novelty 4/5). The "preparation-history time" interpretation is novel (4/5). Claim 2 (product-state identity) should be demoted to verification status (1/5, known from Takesaki).**

## Novelty Ratings and Prior Art

| Claim | Description | Novelty | Closest Prior Art | What's Genuinely New |
|-------|-------------|---------|-------------------|---------------------|
| 1 | Post-quench modular flow = pre-quench dynamics | 2.5/5 | K = βH₀ is textbook; Cardy-Tonni 2016/2018 (entanglement Hamiltonians in CFT — computes K_A form after quenches but NOT correlator dynamics); Hollands-Sanders 2017 (mathematical framework, no dynamics test) | Explicit spectral comparison (disjoint peaks), √3 asymptotic discrepancy, TTH framing |
| 2 | Product-state identity (C_global = C_local) | 1/5 | Takesaki Vol. II Theorem IX.4.2 (tensor product modular operators); Bratteli-Robinson | Nothing algebraically novel. Numerical confirmation to 10⁻¹⁶ useful as pipeline check only |
| 3 | Excited-state modular flow at wrong frequencies, growing with N | **4/5** | **Lashkari-Liu-Rajagopal 2021** (arXiv:1811.05052) — modular flow operators for excited states (coherent/squeezed in GFF), but does NOT compare correlator dynamics to physical time evolution; Lashkari 2016 (modular Hamiltonian matrix elements via replica trick); Casini-Huerta 2009 (lattice modular Hamiltonians, no excited states) | Zero spectral weight at physical frequency (0.01%), N^{0.33–0.44} continuum divergence, domain map across state types, explicit TTH test framing |
| 4 | Squeezed states: quantitative (not structural) TTH discrepancy | 3/5 | None found. BCH formula K_sq ≈ βH + O(r) is standard math | 7.8% vs. 102% explicit comparison; "correct frequencies, wrong amplitudes" characterization; structural vs. quantitative taxonomy. **Caveat: single data point (r=0.3, λ=0.3)** |
| Central | "Modular time is preparation-history time" | **4/5** | NOT found in Connes-Rovelli 1994, Rovelli later papers, Martinetti-Rovelli, Swanson 2020, Chua 2024, Paetz thesis, arXiv:1807.04651 | Explicit articulation that modular time generates dynamics under the Hamiltonian that CREATED the state; unifying explanation for TTH success/failure pattern across all regimes tested |

## Conceptual Attack Results

### Attack 1: "TTH Was Never Meant for Non-Equilibrium States" — FAILS

Connes-Rovelli 1994 explicitly define thermal time for ANY faithful state via Tomita-Takesaki, not just KMS states. The attack misrepresents TTH's intended scope. **Weakened version has some merit:** TTH is most interesting for quantum gravity (where there's no background time), not nonrelativistic QM. But this doesn't invalidate the claims as tests of what TTH predicts.

### Attack 2: "Modular Flow of Excited State IS the Correct Time" — PARTIALLY SUCCEEDS

**This is the strongest attack.** For quantum gravity contexts (no background spacetime), there's no external "physical time" standard. The attack reveals a genuine interpretive ambiguity. **However, it fails for the specific test cases:** (1) In the Rindler case, the observer is fixed (accelerating), and TTH gives the wrong answer for that observer. (2) In the post-quench case, the experimentally measured correlator C_QM(t) under H_AB(λ) is unambiguous. **Impact:** Numerical claims unaffected. The interpretation "TTH fails" should be qualified: "fails to match physically measured dynamics in operationally well-defined settings."

### Attack 3: "The Lattice Is Not Type III" — WEAKENED BY DATA

Finite lattices are type I (M_{2^N}(ℂ)), not type III₁. However: (1) discrepancy GROWS with N (the continuum prediction is worse, not better); (2) the mismatch is qualitative (zero spectral weight), requiring the type-transition to introduce spectral content at a currently absent frequency; (3) lattice modular Hamiltonians are known to converge (Casini-Huerta 2009, Eisler-Peschel 2009); (4) squeezed state result (exact K_R, no Gaussian approximation) eliminates approximation artifacts.

## Null Hypothesis Assessment

The null hypothesis (standard QM without TTH explains everything) is partially correct for all claims:
- **Claim 1:** K = -log ρ = βH₀ is algebraically trivial. The computation, spectral analysis, and √3 asymptotic add value.
- **Claim 3:** K_excited ≠ H is qualitatively obvious. The quantitative findings (zero spectral weight, N-scaling) are genuinely new.
- **Claim 4:** K_sq ≈ βH + O(r) explains the pattern. The taxonomy and explicit numbers add specificity.

## Recommended Claim Priority

1. **Claim 3** — highest priority for rigorous proof (strongest, most novel)
2. **Central interpretation** — needs more examples and analytic grounding
3. **Claim 4** — needs systematic r-λ parameter space study
4. **Claim 1** — essentially proven but should be presented carefully re: algebraic content
5. **Claim 2** — demote to verification status (known result)
