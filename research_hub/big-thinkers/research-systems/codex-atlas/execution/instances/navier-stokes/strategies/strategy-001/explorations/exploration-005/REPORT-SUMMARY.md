# Exploration 005 — Summary

## Goal
Literature survey of (1) improved vortex stretching bounds, (2) spectral/frequency-localized estimates, and (3) alternative enstrophy closure strategies for 3D NS. Context: 158× slack in the standard Ladyzhenskaya vortex stretching bound, decomposing as 63% C_L looseness + 31% geometric alignment + 6% symmetric factor.

## What Was Tried
Three parallel sub-agent literature searches covering: (1) geometric regularity criteria (Constantin-Fefferman, Grujić, Da Veiga-Berselli, Chae-Lee), (2) Besov/Littlewood-Paley methods (Koch-Tataru, Cheskidov-Shvydkoy, Gallagher-Koch-Planchon, Tao averaged NS), and (3) alternative closures (BKM, Kozono-Taniuchi BMO, Doering-Foias ladder, stochastic methods, Bradshaw-Farhat-Grujić intermittency). 28 papers surveyed with exact theorem statements.

## Outcome: Succeeded

**28 papers found and analyzed across all three topics.**

---

## Key Takeaway

**The dominant 63% Ladyzhenskaya constant bottleneck is untouched by all existing literature.** The entire geometric approach (Constantin-Fefferman, Grujić, 8 papers) operates by a fundamentally orthogonal mechanism: showing that when vorticity direction ξ is Hölder-coherent, the stretching term depletes *below* the Ladyzhenskaya threshold, making C_L irrelevant. When coherence fails, the full C_L is needed and no improvement is known. The spectral/Besov literature (Tao 2014 averaged NS) explicitly proves that *no harmonic analysis argument alone* can close the NS regularity problem — any tightening of C_L must exploit the differential structure of the actual NS nonlinearity. **No "spectral Ladyzhenskaya inequality" exists in the literature** — a version of the embedding W^{1,2} ↪ L^4 with a reduced constant for spectrally extended fields is an open problem.

---

## Specific Results

**Topic 1 — Geometric Vortex Stretching:**
- CF93: Lipschitz coherence of ξ in high-|ω| regions → regularity (qualitative, no C_L improvement)
- Da Veiga-Berselli 2002: Weakens to ½-Hölder coherence (critical exponent)
- Grujić 2009: Localizes geometric depletion to parabolic cylinders
- Grujić-Guberović 2010: Hybrid result — direction coherence Γ trades off against |ω| integrability with explicit scaling exponents. **Most relevant to our geometric 31% component.**
- Bradshaw-Farhat-Grujić 2019: Spatial intermittency algebraically reduces the "scaling gap" — **most relevant to our 63% C_L component.**

**Topic 2 — Spectral Methods:**
- Koch-Tataru (2001): BMO^{-1} largest scale-invariant existence class; no tighter trilinear bound
- Cheskidov-Shvydkoy (2010): B^{-1}_{∞,∞} regularity criterion — weaker than L³, not tighter
- Tao (2014): **Critical result** — averaged NS blows up despite satisfying all harmonic analysis bounds. Implies Besov methods alone cannot close NS regularity. Any tighter C_L must use differential NS structure.
- No paper found establishing tighter trilinear bounds for spectrally extended fields.

**Topic 3 — Alternative Closures:**
- BKM (1984): Avoids Ladyzhenskaya via log-Gronwall at L^∞ level. Our data shows 12× Agmon slack (vs. 158× Ladyzhenskaya slack) — BKM-type analysis may be tighter for NS.
- Kozono-Taniuchi (2000): Exploits Biot-Savart CZ structure to give BMO-based blowup criterion (strictly weaker than L^∞). Logarithmic improvement at BKM level. **BMO ‖ω‖ for NS flows is likely much smaller than ‖ω‖_{L^∞}**, giving potentially large effective improvement — unquantified.
- Doering-Foias ladder (1991): Confirms Ω^{3/2} obstruction rather than improving it
- Stochastic methods: No improvement over deterministic enstrophy bounds
- Protas group (2020): Numerically confirms max enstrophy ~ E₀^{3/2} is achievable in worst-case — bound is functionally tight even if constant is loose for typical flows

---

## Leads Worth Pursuing

1. **"Spectral Ladyzhenskaya inequality":** Can one prove ‖f‖_{L^4} ≤ C_L(N) ‖f‖_{L²}^{1/2}‖∇f‖_{L²}^{1/2} with C_L(N) < C_L for functions supported on frequency band |ξ| ~ N? Tao's result says this won't close regularity alone, but it would directly quantify the 63% C_L slack.

2. **Bradshaw-Farhat-Grujić intermittency calibration:** Measure the spatial intermittency μ of the vorticity field in our test NS flows, and check whether the Bradshaw-Farhat-Grujić formula predicts the observed C_{L,eff} = 0.147 from μ.

3. **BMO norm comparison:** Compute ‖ω‖_{BMO} vs. ‖ω‖_{L^∞} for our NS test flows. If ‖ω‖_{BMO}/‖ω‖_{L^∞} ≪ 1, this gives a concrete improvement in the Kozono-Taniuchi framework that could account for part of the 12× Agmon slack.

4. **Grujić-Guberović trade-off quantification:** Measure the local Hölder coherence exponent β of ξ = ω/|ω| for our test flows, plug into the Grujić-Guberović scaling formula, and check if it explains the 31% geometric component.

---

## Unexpected Findings

1. **Tao (2014) is a hard obstruction for Besov-based improvements:** We expected that spectral methods might address the C_L bottleneck, but Tao's averaged NS paper definitively shows that no argument using only harmonic analysis bounds (which includes all Besov/Littlewood-Paley estimates) can close NS regularity. This rules out an entire class of approaches for the 63% C_L component.

2. **BKM is tighter than Ladyzhenskaya for NS:** Our data (12× Agmon slack vs. 158× Ladyzhenskaya slack) implies BKM-type analysis is ~13× tighter for NS flows. This is not remarked on in the literature and suggests that **translating BKM back to the enstrophy level** (via Kozono-Taniuchi) might give a much tighter effective enstrophy bound than the standard Ladyzhenskaya approach.

3. **The Protas group's finding confirms the bound is functionally tight:** Max enstrophy ~ E₀^{3/2} is numerically achievable for adversarial initial conditions. Combined with our observation that C_{L,eff} = 0.147 for the flows we tested, this suggests our test flows are *not* the adversarial worst case. The true adversarial minimum slack may be less than 158×.

---

## Computations Identified

1. **Spectral Ladyzhenskaya constant computation:** For functions with Fourier support restricted to a dyadic shell |ξ| ∈ [N/2, 2N], numerically optimize ‖f‖_{L^4} / (‖f‖_{L²}^{1/2}‖∇f‖_{L²}^{1/2}) to get C_L(N). Compare to C_L = 0.827. Requires: gradient descent on function space over a 3D periodic domain. ~100 lines scipy. Would directly tell us the spectral bottleneck.

2. **Intermittency factor vs. C_{L,eff}:** Given our NS simulation data (from explorations 002-004), compute the spatial intermittency measure μ = Vol({x: |ω(x)| > λ‖ω‖_{L^∞}}) / Vol(domain) for various λ. Then compare to the Bradshaw-Farhat-Grujić prediction C_{L,eff} ~ C_L · μ^α. Requires: reading the Bradshaw-Farhat-Grujić 2019 paper for the precise exponent α.

3. **BMO vs. L^∞ comparison for NS flows:** Compute ‖ω‖_{BMO}/‖ω‖_{L^∞} for our NS test flows. The BMO norm is the maximum of the average oscillation over all balls. This would quantify the potential improvement from the Kozono-Taniuchi framework. ~50 lines scipy/numpy.
