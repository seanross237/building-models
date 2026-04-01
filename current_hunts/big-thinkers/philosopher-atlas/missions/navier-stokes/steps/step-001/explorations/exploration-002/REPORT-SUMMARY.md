# Exploration 002: Lin (1998) — REPORT SUMMARY

## Goal
Extract 5 structural features from Lin's (1998) simplified proof of CKN partial regularity for Navier-Stokes, and compare each with CKN (1982).

## What Was Tried
Literature research on Lin (1998) via web search and cross-referencing with CKN survey papers, textbook treatments (Robinson–Rodrigo–Sadowski), and subsequent papers that cite and analyze Lin's method (Vasseur, Seregin–Shilkin, Barker–Wang). Five structural features were extracted and compared.

## Outcome: Succeeded

All five features extracted with precise mathematical content.

## The Five Features

**1. Epsilon-Regularity Criterion:** Lin uses C(r) + D(r) < ε₀, i.e., (1/r²)∫∫_{Q_r}(|u|³+|p|^{3/2}) < ε₀. This is *simpler* than CKN's criterion (which also required A(r)+E(r) small), but has the same parabolic scaling (both dimensionless under NS rescaling). Lin drops A and E from the hypothesis because his compactness argument recovers them from C+D in the limit.

**2. Covering Argument:** Identical to CKN. Parabolic Vitali covering, same disjoint-cylinder counting estimate ∑rᵢ ≤ (1/ε₀)∫|∇u|² → P¹(Σ)=0. Lin's ε-criterion uses C+D, but the covering step re-introduces E(r) via the local energy inequality (E ≥ c(C+D)), restoring the same P¹ bound via the same mechanism.

**3. Localization Mechanism:** **Lin's core innovation.** CKN uses explicit cutoff functions φ (with |∇φ|~1/r) and tracks three error terms (T₁, T₂, T₃) through an iterative decay estimate. Lin replaces this with blow-up/compactness/contradiction: rescale a singular sequence uₙ(y,s)=rₙu(zₙ+rₙy, rₙ²s), show C+D→0 in the rescaled frame, extract a convergent subsequence via Aubin–Lions, identify the limit as ũ≡0 (regular), reach contradiction. The Young/absorption steps (Y1–Y4 in CKN) do not disappear — they are hidden in the compactness infrastructure (energy-class bounds for the blow-up sequence) rather than appearing explicitly.

**4. Critical Scaling Exponents:** Identical to CKN. The NS parabolic scaling u~r⁻¹, p~r⁻² forces C(r) and D(r) to be scale-invariant. The blow-up sequence uses exactly this scaling. The dimension-1 bound comes from E(r)=(1/r)∫|∇u|² being scale-invariant, forcing ∫|∇u|²≥ε₀r on the singular set. The parabolic dimension N=5 and Sobolev exponent 10/3=2N/(N-2) appear identically in both proofs.

**5. Free-Parameter vs. Fixed-Constant Estimates:** Lin does not eliminate lossiness — the same Young's inequality steps (Y1–Y4) are present but invisible, bundled into the "uniform bounds for the compactness step." The threshold ε₀ is completely opaque in Lin's proof (it emerges from a contradiction with no explicit formula), whereas in CKN one can at least trace which constants enter (even if ε₀ is still not numerically computed in CKN either).

## Key Takeaway

**Lin's proof is a streamlining of CKN, not a structural departure.** The bottleneck — scale-invariance of E(r) forces dim(Σ) ≤ 1 via the r¹ scaling of ∫|∇u|² — is identical and unchanged. The compactness argument repackages the same constraints more elegantly but opens no new path to improving the dimension bound. If anything, Lin's approach is *worse* for diagnosing potential improvements, because it hides where the lossiness enters.

## Leads Worth Pursuing

- Lin's use of C(r)+D(r) as the primary criterion (without A+E) shows the ε-regularity input can be weakened. Could further weakening of the criterion (e.g., allowing r→0 at different rates for velocity vs. pressure) change the dimension bound? Probably not, since the bound comes from the covering step via E(r), not the criterion.
- Ladyzhenskaya–Seregin (1999) push Lin's approach further, showing the C+D criterion implies Hölder continuity (stronger conclusion). Worth checking if their stronger conclusion changes the covering argument.

## Unexpected Findings

The report uncovered a subtle issue in Section 4: naively using C(r) in the covering argument (rather than E(r)) would only give dim(Σ) ≤ 2 (since ∑rᵢ² ≤ (1/ε₀)∫|u|³ < ∞). The dimension ≤ 1 bound requires re-introducing E(r) via the local energy inequality, even though Lin's ε-criterion doesn't use E(r) as input. This means the dimension-1 bound is *more directly* tied to the dissipation ∫|∇u|² than Lin's criterion suggests — the P¹(Σ)=0 result cannot be derived from C+D alone without passing through E(r).

## Computations Identified

None needed for this exploration — the structural analysis is purely analytical. The key quantities (C(r), D(r), E(r) and their scaling) are known in closed form.
