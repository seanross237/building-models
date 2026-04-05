# Exploration 004 Summary: Master Loop Contraction Estimate Optimization

## Goal
Find the maximum achievable β₀(4) under the CNS master loop framework (arXiv:2505.16585, Proposition 3.23), and determine if curvature input can bring it to 1/24.

## What Was Tried
1. Retrieved actual content of Proposition 3.23, Lemma 3.20, and Remark 1.4 from arXiv:2505.16585 via sub-agent
2. Derived β_max from first principles using the exact three-term contraction bound
3. Optimized over parameter choices (λ, γ, ρ) to find the true ceiling
4. Quantified the gap between master loop and Bakry-Émery
5. Computed required curvature coupling for hypothetical enhancement

## Outcome: Succeeded + Critical Correction

### Maximum β₀(4): Hard Ceiling at 1/(32e) ≈ 1/87

The exact contraction bound from Proposition 3.23 is:
```
||Mf|| ≤ (2dBλ + 2dB/(λN²) + 4dβγ/(λρN)) · ||f|| + boundary
```

Optimizing parameters (λ=1/N optimal by calculus, ρ=1/e required by Proposition 3.24, γ=1 minimum allowed):
```
Deformation term: 4dβe ≤ 1/2  →  β_max = 1/(8de) = 1/(32e) ≈ 1/87   [DERIVED]
```

**This is the hard ceiling of the current proof structure.** No further improvement is possible without a fundamentally new norm or proof technique.

### Critical Correction: Remark 1.4 is NOT About Curvature

**The GOAL.md's framing of Remark 1.4 is incorrect.** After reading the actual paper:

- Remark 1.4 asks about extending to **β ~ c_d N** via **signed cancellations in the merger term**
- The curvature κ = N/2 of U(N) is relevant to the *Glauber dynamics* approach ([SZZ23], CNS Sept 2025), NOT to the master loop/surface-sum approach
- The master loop proof involves no Riemannian geometry; curvature cannot enter without structural changes

The gap between master loop (1/87) and Bakry-Émery (1/24) is a gap between two different approaches, not a missing ingredient in one approach.

### Gap = 4e/3 ≈ 3.624

The gap factor is exactly **32e/24 = 4e/3 ≈ 3.624** — not a simple integer. [COMPUTED]

### Curvature Input: Structurally Impossible for Small N

Even hypothetically, to bring β_max to 1/24 via curvature coupling δ·κ:
- SU(2): need δ_norm = 2.624 (impossibly large — curvature term would need to exceed the entire contraction budget)
- SU(3): need δ_norm = 1.750 (large)
- Only at N ≳ 50 does the required coupling become small

And crucially: the proof has no mechanism for such coupling.

## Verification Scorecard
- **4 VERIFIED** (from paper text/structure)
- **4 DERIVED** (from verified premises via calculus/algebra)
- **2 COMPUTED** (numerical)
- **1 CONJECTURED** (interpretation of signed-cancellation path)

## Key Takeaway
**The master loop framework is hard-capped at β₀(4) = 1/(8de) ≈ 1/87, derived exactly from Proposition 3.23 with optimal parameters. Bridging the gap to 1/24 requires a fundamentally new proof structure — specifically, signed-cancellation bounds in the merger term — not curvature input. The two approaches (master loop and Bakry-Émery/dynamical) remain complementary and ununified.**

## Proof Gaps Identified

1. **Signed cancellations in merger term:** Remark 1.4's actual question: can the merger term bound 2dB/(λN²) be reduced via signed surface sums? This is the real open problem. Currently unknown if signed cancellations help when β is large.

2. **N-independence of string tension in Bakry-Émery:** The open question is whether the area law constant from the B-E approach depends on N (degrading as N→∞). Master loop gives N-independent γ; B-E status is open.

3. **Large-β regime β ~ c_d N:** Neither approach currently covers this; requires new ideas beyond current contraction argument.

## Unexpected Findings

1. **ρ = 1/e is not conservative — it's required.** The boundary term (Proposition 3.24) pins ρ = e^{-1} exactly. This means there's no room to improve the deformation term via ρ.

2. **Terms 1+2 are negligible at the optimal point.** At λ=1/N, γ=1, the splitting and merger terms contribute only ≈ 0.004 vs. the deformation term's binding constraint at 0.5. The ceiling is entirely from the deformation term.

3. **The GOAL.md's description of Remark 1.4 was incorrect**, and the hypothesized "curvature enhancement" direction is not supported by the paper. This is a significant finding for the strategizer's model of the CNS program.

## Computations Identified for Future Work

1. **Signed cancellation bound:** Estimate the *signed* sum of merger-term contributions for β ∈ [1/87, 1/24]. Does the signed sum stay bounded while the unsigned sum grows?

2. **Alternative norm:** What norm on loop space would give a contraction at β ~ c_d N? The norm λ^{ι(s)} γ^{area(s)} ρ^{B-K} would need to be replaced with something encoding signed surface weight.

3. **N-independence of B-E string tension:** Numerical test — compute the area law constant from the Bakry-Émery approach for N = 2, 3, 4, 5 and check if it depends on N.
