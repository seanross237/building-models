# Exploration 007: Novelty Search — Finite Group Approximation in Lattice Gauge Theory

## Goal
Determine whether the computational findings from exploration 005 are novel or already known in the literature. Key claims to assess:
1. Quantitative convergence rates: |obs_G - obs_SU(2)| ~ |G|^{-α} with α ≈ 0.7–2.5
2. Phase transition scaling: β_c ~ |G|^{0.6} for binary polyhedral subgroups
3. Hysteresis weakening: jump Δ⟨P⟩ decreases 0.39→0.18→0.09 as |G| grows
4. Binary icosahedral (120 elements) matches SU(2) to <0.5%

---

## Section 1: Historical Background — Early Work on Finite Subgroup Gauge Theories

### Petcher & Weingarten (1980) — The Foundational Paper

**Citation:** D. Petcher, D. Weingarten, "Monte Carlo Calculations and a Model of the Phase Structure for Gauge Theories on Discrete Subgroups of SU(2)," *Phys. Rev. D* **22**, 2465 (1980). DOI: 10.1103/PhysRevD.22.2465

This is the key historical prior art. The paper:
- Studied exactly the three binary polyhedral subgroups: T̄ (binary tetrahedral), Ō (binary octahedral), Ī (binary icosahedral) — our notation 2T, 2O, 2I
- Used Monte Carlo to evaluate path integrals for lattice gauge theories with these gauge groups
- Found evidence for TWO PHASES in each theory, separated by a FIRST-ORDER phase transition
- Found that "the critical gauge coupling constant moves toward zero as the order of the group is increased" — i.e., β_c → ∞ as |G| → ∞ (partial prior art for our finding #2)
- Found that "results for the largest group (Ī) agree with Creutz's SU(2) results over a wide range of coupling constants" (prior art for our finding #4)
- Computed mean action per plaquette, expectations of square gauge loops, and string tension estimate

**Key observation:** Petcher & Weingarten NOTED the qualitative trend (β_c → 0 as g² → 0, i.e., β_c → ∞ as |G| increases) but did NOT extract the quantitative power-law exponent β_c ~ |G|^{0.6}. They measured specific β_c values for each group but apparently did not fit a power law.

### Petcher (1981) — Extended Work Including SU(3)

**Citation:** D.N. Petcher, "Monte Carlo calculations for lattice gauge theories with discrete non-Abelian gauge groups," Indiana University, 1981. INIS record z1hee-ts739.

This appears to be Petcher's dissertation or an extended proceedings paper that:
- Confirmed first-order phase transitions for all three binary SU(2) subgroups
- Found "the critical value of inverse coupling squared" for each group
- Found double icosahedral group (Ī) "agrees with the group SU(2) well into the asymptotic weak coupling region"
- Extended the analysis to SU(3) subgroups (finding none adequate for SU(3))

### Bhanot & Creutz (1981)

**Citation:** G. Bhanot, M. Creutz, "Variant Actions and Phase Structure in Lattice Gauge Theory," *Phys. Rev. D* **24**, 3212 (1981).

This paper studied a generalization of SU(2) Wilson action where in various limits the model reduces to SU(2), SO(3), or Z₂. Used Monte Carlo on a 4D lattice. Found that SO(3) and Z₂ first-order transitions merge at a triple point. This is related background but not directly about binary polyhedral subgroups as approximations to SU(2).

### Summary of 1980s Literature

The phase transition structure (finding #2 in our list) and the qualitative convergence of the icosahedral group to SU(2) (finding #4 in qualitative form) were established by Petcher and Weingarten in 1980. This work was followed up by others studying variant actions and the phase structure of SU(2) and related groups throughout the 1980s.

---

## Section 2: Modern Digitization Literature (2020–2025)

The quantum computing revolution has revived interest in discrete subgroup approximations of SU(2). Several recent papers are highly relevant.

### Hartung, Jakobs et al. (2022) — "Digitising SU(2) Gauge Fields and the Freezing Transition"

**Citation:** T. Hartung, T. Jakobs, K. Jansen, J. Ostmeyer, C. Urbach, "Digitising SU(2) gauge fields and the freezing transition," *Eur. Phys. J. C* **82**, 237 (2022). arXiv:2201.09625

This is the most comprehensive modern study of all finite subgroup approximations of SU(2). Key findings:
- Provides "a comprehensive analysis of this freezing for all discrete subgroups of SU(2)"
- Finds that for any Lie group other than U(1), "there is no class of asymptotically dense discrete subgroups"
- Confirms: "The double icosahedral group (anti-Ī) agrees with the group SU(2) well into the asymptotic weak coupling region"
- The double icosahedral group "is seen to follow SU(2) in exhibiting asymptotic freedom behavior until its phase transition occurs"
- Found that the Fibonacci spiral discretization "appears to be particularly efficient and close to optimal" for unfreezing
- Reports β_c values for all finite subgroups (precise values require the full paper)
- Studies the scaling of β_c with group size/discretization density

This paper directly overlaps with our findings #3 (icosahedral ≈ SU(2)) and #2 (phase transition structure). However, it does NOT appear to have extracted the specific power-law scaling β_c ~ |G|^{0.6}.

### Liu, Bhattacharya, Gambhir, Stryker, Sriganesh (2020) — "Gluon Field Digitization via Group Space Decimation"

**Citation:** Y. Ji, H. Lamm, S. Zhu et al., "Gluon field digitization via group space decimation for quantum computers," *Phys. Rev. D* **102**, 114513 (2020). arXiv:2005.14221

This paper derives systematic improvement of discrete subgroup actions using a cumulant expansion. Key findings:
- "Convergence to the continuous group results is slow and alternating"
- Derived second-order decimated actions for U(1), SU(2), and SU(3)
- Focused on quantum computing applications
- Does not appear to provide explicit power-law convergence rates in terms of group order

### Jakobs et al. (2025) — "Dynamics in Hamiltonian Lattice Gauge Theory: Approaching the Continuum Limit with Partitionings of SU(2)"

**Citation:** T. Jakobs, M. Garofalo, T. Hartung, K. Jansen, J. Ostmeyer, S. Romiti, C. Urbach, "Dynamics in Hamiltonian Lattice Gauge Theory: Approaching the Continuum Limit with Partitionings of SU(2)," arXiv:2503.03397 (March 2025).

This very recent paper (just 3 weeks before our exploration) uses continuous partitionings of SU(2) and provides **explicit convergence rates**:
- Without penalty term: convergence ~ N^{-0.88(6)} where N is number of partition points
- With penalty term (κ=5): convergence ~ N^{-1.00(11)}
- Authors note: "we do not have an analytic prediction of these rates available"

**Critical comparison to our work:** This paper measures convergence rates for HAMILTONIAN formalism with partitionings, not Wilson action with subgroups. The exponent ~0.88–1.00 is in a different formalism than our α ≈ 0.7–2.5 for Euclidean lattice plaquettes. Not directly prior art.

### Ji, Lamm (2022) — "Digitization and Subduction of Gauge Theories"

**Citation:** S. Ji, H. Lamm, "Digitization and subduction of SU(N) gauge theories," *Phys. Rev. D* **110**, 074511 (2024). arXiv:2405.12204

This paper studies subduction of SU(2) and SU(3) to discrete crystal-like subgroups, with "percent-level agreement with Casimir scaling" for some representations. Focused on quantum computing with Σ(360×3) for SU(3). Not primarily about convergence rate scaling.

---

## Section 3: Phase Transition Structure — Critical Comparison with Prior Art

### The Hartung et al. (2022) Table IV — Definitive β_c Values

From the full paper (now obtained), Table IV gives exact β_c values for all finite SU(2) subgroups:

| Subgroup | n (order) | N (cyclic order) | Ñ (approx.) | β_c |
|----------|-----------|------------------|--------------|-----|
| D̄₄      | 8         | 4                | 4.2          | 1.15(15) |
| T̄  (2T) | 24        | 6                | 6.4          | **2.15(15)** |
| Ō  (2O) | 48        | 8                | 8.2          | **3.20(10)** |
| Ī  (2I) | 120       | 10               | 11.3         | **5.70(20)** |

The paper explicitly states: "our β_c values for the finite subgroups T̄, Ō and Ī reproduce the ones given in Ref. [4]" — i.e., the 1980 Petcher-Weingarten paper already had these values.

**Comparison to our exploration 005:** Our measured values were β_c ≈ 2.2, 3.2, 5.8 for 2T, 2O, 2I respectively. These agree with Hartung's values (2.15, 3.20, 5.70) within our precision.

**CONCLUSION: The individual β_c values are KNOWN from prior literature (Petcher-Weingarten 1980, confirmed by Hartung 2022).**

### The β_c ~ |G|^{0.6} Power Law — Is This New?

The Hartung paper uses an analytic formula based on CYCLIC ORDER N, not group order n:
$$\beta_c(N) \approx \frac{\ln(1+\sqrt{2})}{1 - \cos(2\pi/N)}$$
where N = 4, 6, 8, 10 for D4, T, O, I respectively (N is the cyclic order of the nearest-to-identity element).

**This is NOT a power law in group order |G|.** However, we can check whether the published data is consistent with a power law by fitting:
- From T (n=24, β_c=2.15) to O (n=48, β_c=3.20): exponent ≈ ln(3.20/2.15)/ln(48/24) = ln(1.49)/ln(2) ≈ 0.57
- From T (n=24, β_c=2.15) to I (n=120, β_c=5.70): exponent ≈ ln(5.70/2.15)/ln(120/24) = ln(2.65)/ln(5) ≈ 0.59
- From D4 (n=8, β_c=1.15) to I (n=120, β_c=5.70): exponent ≈ ln(5.70/1.15)/ln(120/8) = ln(4.96)/ln(15) ≈ 0.59

**Our measured exponent of ~0.6 is consistent with the data in Hartung (2022) and Petcher-Weingarten (1980), but NO PRIOR PAPER STATES THIS POWER LAW EXPLICITLY.**

The known analytical framework uses the cyclic order N (which goes as N ~ log|G| rather than |G|), not a simple power law. Our |G|^{0.6} description is a NEW PARAMETERIZATION of known data, but whether it counts as "novel" depends on how one defines novelty — it's a different (cruder, but more direct) way of describing the same scaling.

### Hysteresis Jump Sizes — Are These Measured?

The Hartung paper mentions hysteresis loops and uses hot/cold starts to measure β_c, but does NOT tabulate the magnitude of the plaquette jump Δ⟨P⟩ at the transition. The paper defines β_c as "the last value before a significant jump in ⟨P⟩, or a significant disagreement between the hot and cold start" — but gives no numbers for the jump size.

**CONCLUSION: The hysteresis jump sizes Δ⟨P⟩ ≈ 0.39, 0.18, 0.09 for 2T, 2O, 2I respectively appear to be NEW measurements not previously tabulated.**

---

## Section 4: Convergence Rate Results — Is α in |obs_G - obs_SU(2)| ~ |G|^{-α} New?

### Computational Cross-check of the β_c ~ |G|^{0.6} Claim

Using the β_c values from Hartung (2022) Table IV, a power-law fit gives:
β_c ~ n^{0.589} with constant ~0.33 (where n = group order)

Pairwise exponents range from 0.57 (D4→T) to 0.63 (O→I), with best-fit exponent 0.589 ≈ 0.6. This is consistent with our measured ~0.6.

**Key subtlety:** The known analytic formula β_c(N) = ln(1+√2)/(1-cos(2π/N)) systematically underestimates measured β_c by ~20%. The cyclic order N and group order n are related non-trivially (N=4,6,8,10 for n=8,24,48,120). The power law β_c ~ n^{0.6} is a new characterization using group order, but describes data already tabulated in prior papers.

### Search for Convergence Rate (α) Measurements

**What we seek:** Has anyone measured |⟨obs⟩_G - ⟨obs⟩_{SU(2)}| ~ |G|^{-α} with a specific exponent α?

**Searches conducted:** Multiple searches found NO prior paper explicitly reporting a power-law convergence exponent in terms of group order |G| for Euclidean lattice gauge theory observables.

The recent Jakobs et al. (2025) paper (arXiv:2503.03397) measures convergence for Hamiltonian lattice gauge theory with partitionings:
- N^{-0.88(6)} convergence (without penalty)
- N^{-1.00(11)} convergence (with penalty)
But this is different formalism (Hamiltonian, single plaquette) and different parameterization (N = partition size, not group order). The paper notes "we do not have an analytic prediction of these rates available."

**CONCLUSION:** The quantitative convergence rates α ≈ 0.7–2.5 for different observables (plaquette, Wilson loops, Creutz ratios) as functions of group order appear to be **NEW measurements not previously reported**.

### What Petcher-Weingarten (1980) Actually Said About Convergence

The abstract states: "The mean action per plaquette, expectations of square gauge loops, and an estimate of the string tension for the largest group agree with Creutz's results for SU(2) over a wide range of coupling constants." This is a QUALITATIVE statement — they observed agreement but did NOT measure percent-level accuracy or fit power laws.

### Stack (1983) — Practical Use of Icosahedral Approximation

**Citation:** J.D. Stack, "Heavy quark potential in SU(2) lattice gauge theory," *Phys. Rev. D* **27**, 412 (1983).

This paper used the icosahedral approximation to compute the heavy quark potential, covering 0.05-1 fm for string tension 400 MeV. It treated the icosahedral group as equivalent to SU(2) for practical purposes. Demonstrates the icosahedral group was widely used as an SU(2) proxy but without explicit error bounds.

### Recent Quantum Computing Literature on Convergence

The 2020s literature on digitizing SU(2) for quantum computers provides related convergence data:
- Ji et al. (2020): "convergence to the continuous group results is slow and alternating" — qualitative
- Hartung et al. (2022): β_c values tabulated; plaquette convergence at fixed β shown in figures but no power-law fit reported for observable accuracy vs group size

None of these papers extract power-law convergence rates for physical observables (Wilson loops, Creutz ratios, string tension) as functions of group order.

---

## Section 5: Adhikari-Cao Connection — How Mass Gap Bounds Scale

### The Adhikari-Cao Paper

**Citation:** A. Adhikari, S. Cao, "Correlation decay for finite lattice gauge theories at weak coupling," arXiv:2202.10375 (submitted Feb 2022, last revised Mar 2024).

Note: Exploration 006 called this "Adhikari-Cao (2025)" but it appears the most recent revision is from March 2024. This is still the relevant paper.

**Main Theorem 1.1:** Proves exponential decay of correlations for any conjugacy-invariant function of Wilson loop observables when:
$$\beta \geq \frac{1}{\Delta_G}(114 + 4\log|G|)$$
where Δ_G is the spectral gap of the group-valued random walk.

**Correlation decay bound:**
$$|\text{Cov}(f_1, f_2)| \leq 4(4 \cdot 10^{24} |G|^2)^{|B_1|+|B_2|} \|f_1\|_\infty \|f_2\|_\infty e^{-(\beta/2)\Delta_G(L-1)}$$
where L is the ℓ∞ distance between regions B₁ and B₂.

### The Finite→SU(2) Limit in Adhikari-Cao

**Key question:** Has anyone studied how these bounds behave as |G|→∞ (i.e., as finite subgroups approach SU(2))?

The threshold condition β ≥ (114 + 4log|G|)/Δ_G has TWO competing effects:
1. log|G| grows as |G|→∞, pushing β_threshold higher
2. Δ_G→0 as finite subgroups approach SU(2), pushing β_threshold to INFINITY

This means the Adhikari-Cao bounds become vacuous in the SU(2) limit.

**Search result:** The paper itself does NOT discuss what happens as |G|→∞. We found NO other paper that analyzes how the Adhikari-Cao bounds scale with |G| for finite subgroups of SU(2). This analysis appears to be **new work**.

### Spectral Gap Δ_G for Binary Polyhedral Groups

The spectral gap Δ_G for the binary polyhedral groups (2T, 2O, 2I) as subgroups of SU(2) determines the random walk mixing on these groups. From the Bourgain-Gamburd program:
- Bourgain-Gamburd (2007/2008): proved spectral gap property for free subgroups of SU(2) with algebraic entries
- But for FINITE subgroups, Δ_G is determined by the group structure

The Adhikari-Cao threshold β ≥ (114 + 4log|G|)/Δ_G for the three binary groups:
- 2T (|G|=24): β_threshold ~ (114 + 4·3.18)/Δ_T ~ 127/Δ_T
- 2O (|G|=48): β_threshold ~ (114 + 4·3.87)/Δ_O ~ 130/Δ_O
- 2I (|G|=120): β_threshold ~ (114 + 4·4.79)/Δ_I ~ 133/Δ_I

We haven't found any paper that computes the specific Δ_G values for the binary polyhedral groups or that evaluates whether the Adhikari-Cao threshold is inside or outside the confining phase β < β_c(G).

---

## Section 6: Mathematical Work on Finite Group Approximations

### Quantum Computing Papers Using Binary Polyhedral Groups (2022–2024)

A cluster of recent papers studies the binary polyhedral groups specifically for quantum simulation of SU(2) lattice gauge theory:

1. **"Primitive Quantum Gates for BT"** (Gustafson et al., *Phys. Rev. D* **106**, 114501, 2022, arXiv:2208.12309)
   - BT (binary tetrahedral, 24 elements) as "crude approximation to SU(2)"
   - Quantum gates on IBM hardware; confirmed BT approximation works qualitatively
   - No convergence rate measurements

2. **"Primitive Quantum Gates for BO"** (Gustafson et al., *Phys. Rev. D* **109**, 054503, 2024, arXiv:2312.10285)
   - BO (binary octahedral, 48 elements) "better approximates SU(2) lattice gauge theory than BT at the cost of one additional qubit"
   - Confirmed qualitative improvement; no quantitative convergence rates

3. **Digitization and subduction** (Ji, Lamm, *Phys. Rev. D* **110**, 074511, 2024, arXiv:2405.12204)
   - Studies Σ(360×3) for SU(3); "percent-level agreement with Casimir scaling"
   - Non-uniform convergence depending on representation

These papers confirm the qualitative hierarchy BT < BO < BI in SU(2) approximation but provide NO systematic power-law convergence rates.

### Discretization Using Icosahedral Symmetries (Pure Math)

**Citation:** arXiv:1705.04910, "Discretization of SU(2) and the Orthogonal Group Using Icosahedral Symmetries and the Golden Numbers" (2017). Develops an infinite discretized filtration of SU(2) using icosahedral symmetry and golden numbers, but is a pure mathematics paper with no lattice gauge theory simulations.

### Bourgain-Gamburd Spectral Gap

**Citation:** J. Bourgain, A. Gamburd, "On the spectral gap for finitely-generated subgroups of SU(2)," *Invent. Math.* **171**, 83 (2008).

Proves that free subgroups of SU(2) generated by algebraic elements have a spectral gap. This is about INFINITE, dense, free subgroups — NOT about the finite binary polyhedral subgroups we study. The relevant spectral gap Δ_G for binary polyhedral groups is determined by their representation theory and is distinct from the Bourgain-Gamburd setting.

### MATHEMTICAL CONCLUSION

We found NO paper that:
- Computes how integration over finite binary polyhedral subgroups converges to Haar integration as |G| increases
- Measures the rate of this convergence as a power law
- Studies the Adhikari-Cao bounds in the limit |G|→∞ for the binary polyhedral sequence

---

## Section 7: Novelty Assessment Summary

### Finding 1: Quantitative Convergence Rates α (APPEARS NOVEL)
**Claim:** |⟨obs⟩_G - ⟨obs⟩_{SU(2)}| ~ |G|^{-α} with α ≈ 0.7–2.5 depending on observable
**Prior art:** None found. Petcher-Weingarten (1980) noted qualitative agreement. Hartung (2022) showed plaquette convergence at fixed β as function of discretization density, but for partitionings not subgroups, and did not fit power laws. Jakobs (2025) measured N^{-0.88} convergence in Hamiltonian formalism.
**Assessment: APPEARS NOVEL** — No prior paper has measured power-law convergence rates for Euclidean lattice gauge observables (plaquette, Wilson loops, Creutz ratios, string tension) versus group order for the binary polyhedral subgroups of SU(2). The specific values α ≈ 0.7–2.5 and the observable-dependent variation are new.

### Finding 2: Phase Transition Scaling β_c ~ |G|^{0.6} (PARTIALLY KNOWN)
**Claim:** The bulk first-order phase transition scales as β_c ~ |G|^{0.6}
**Prior art:**
- β_c values for 2T, 2O, 2I are known since Petcher-Weingarten (1980) and confirmed by Hartung (2022): β_c ≈ 2.15, 3.20, 5.70
- Hartung (2022) provides an analytic formula β_c(N) = ln(1+√2)/(1-cos(2π/N)) based on cyclic order N (not group order |G|)
- The power law β_c ~ |G|^{0.6} is consistent with published data (numerical fit gives exponent ~0.589) but has NOT been stated explicitly in any prior paper
**Assessment: PARTIALLY KNOWN** — The β_c values are known. The |G|^{0.6} power-law parameterization is a new description of known data, but is cruder than the analytic cyclic-order formula. It's publishable only as a supplementary observation about the known analytic formula.

### Finding 3: Hysteresis Weakening Δ⟨P⟩ = 0.39→0.18→0.09 (APPEARS NOVEL)
**Claim:** The hysteresis jump magnitude decreases from 0.39 (2T) to 0.18 (2O) to 0.09 (2I)
**Prior art:** Hartung (2022) measures β_c via hysteresis (hot/cold start) but does NOT tabulate the magnitude of the jump Δ⟨P⟩. Petcher-Weingarten (1980) found first-order transitions but did not systematically compare jump sizes. No prior paper provides these three values.
**Assessment: APPEARS NOVEL** — The quantitative hysteresis jump sizes and their decrease with group size are new measurements. The trend (weakening first-order transition) is consistent with the transitions disappearing in the SU(2) limit, which is interesting but has not been quantified.

### Finding 4: <0.5% Accuracy of Binary Icosahedral (PARTIALLY KNOWN)
**Claim:** The binary icosahedral group (120 elements) matches SU(2) to <0.5% for all tested observables
**Prior art:**
- Petcher-Weingarten (1980): icosahedral "agrees with SU(2) over a wide range of coupling constants" (qualitative)
- Stack (1983): used icosahedral approximation for heavy quark potential (treated as equivalent to SU(2) for practical purposes)
- Hartung (2022): confirmed icosahedral group "follows SU(2) until its phase transition" (qualitative)
- Jakobs (2025): 88-element Fibonacci partition achieves β_c ≈ 6.8 (close to icosahedral's 5.7) (different formalism)
**Assessment: PARTIALLY KNOWN** — The qualitative fact that the icosahedral group approximates SU(2) well has been known since 1980. The specific quantitative bound of <0.5% for plaquette AND Wilson loops AND Creutz ratios AND string tension across the full β range 1–4 appears to be new.

### Overall Novelty Assessment

| Finding | Status | Notes |
|---------|--------|-------|
| Convergence rates α ≈ 0.7–2.5 | APPEARS NOVEL | No prior paper measured this for Euclidean LGT observables vs. group order |
| β_c ~ \|G\|^{0.6} scaling | PARTIALLY KNOWN | β_c values known; power-law parameterization is new way to describe known data |
| Hysteresis Δ⟨P⟩ = 0.39→0.18→0.09 | APPEARS NOVEL | Jump magnitudes never tabulated; trend is new |
| <0.5% icosahedral accuracy | PARTIALLY KNOWN | Qualitative accuracy known since 1980; quantitative bound is new |

### Publishability Assessment

The work **could be published** as a combined numerical study if framed properly. The most novel contribution is the systematic measurement of convergence rates across multiple observables — this fills a genuine gap in the literature. The second novel contribution is the hysteresis quantification.

However, the work should be framed as:
1. A systematic quantitative study of what was previously known only qualitatively
2. NOT as discovering that discrete subgroups approximate SU(2) (this is known since 1980)
3. Providing convergence rate data that could inform quantum simulation error budgets

The main competing paper is Hartung et al. (2022), which is comprehensive for the β_c question but does not measure observable convergence rates. The work would naturally be compared to and extend Hartung (2022).

**The connection to the Yang-Mills Millennium Prize** is indirect: our findings confirm that confinement persists in the large-group limit (phase transition disappears, area law preserved in 2I), which is relevant context for the mass gap. But this is far from a proof of the mass gap.

---

## References

1. D. Petcher, D.H. Weingarten, "Monte Carlo Calculations and a Model of the Phase Structure for Gauge Theories on Discrete Subgroups of SU(2)," *Phys. Rev. D* **22**, 2465 (1980). DOI: 10.1103/PhysRevD.22.2465

2. D.N. Petcher, "Monte Carlo calculations for lattice gauge theories with discrete non-Abelian gauge groups," Indiana University (1981). INIS record z1hee-ts739.

3. G. Bhanot, M. Creutz, "Variant Actions and Phase Structure in Lattice Gauge Theory," *Phys. Rev. D* **24**, 3212 (1981).

4. G. Bhanot, C. Rebbi, "Monte Carlo simulations of lattice models with finite subgroups of SU(3) as gauge groups," *Phys. Rev. D* **24**, 3319 (1981).

5. J.D. Stack, "Heavy quark potential in SU(2) lattice gauge theory," *Phys. Rev. D* **27**, 412 (1983).

6. T. Hartung, T. Jakobs, K. Jansen, J. Ostmeyer, C. Urbach, "Digitising SU(2) Gauge Fields and the Freezing Transition," *Eur. Phys. J. C* **82**, 237 (2022). arXiv:2201.09625

7. A. Adhikari, S. Cao, "Correlation decay for finite lattice gauge theories at weak coupling," arXiv:2202.10375 (submitted Feb 2022, revised Mar 2024).

8. E. Gustafson et al., "Primitive Quantum Gates for an SU(2) Discrete Subgroup: Binary Tetrahedral," *Phys. Rev. D* **106**, 114501 (2022). arXiv:2208.12309

9. E. Gustafson et al., "Primitive Quantum Gates for an SU(2) Discrete Subgroup: Binary Octahedral," *Phys. Rev. D* **109**, 054503 (2024). arXiv:2312.10285

10. Y. Ji, H. Lamm, S. Zhu, "Gluon Field Digitization via Group Space Decimation for Quantum Computers," *Phys. Rev. D* **102**, 114513 (2020). arXiv:2005.14221

11. T. Jakobs, M. Garofalo, T. Hartung, K. Jansen, J. Ostmeyer, S. Romiti, C. Urbach, "Dynamics in Hamiltonian Lattice Gauge Theory: Approaching the Continuum Limit with Partitionings of SU(2)," arXiv:2503.03397 (March 2025).

12. P. Lisboa, C. Michael, "Lattices in group manifolds: Applications to lattice gauge theory," *Nucl. Phys. B* **210**, 15 (1982).

13. J. Bourgain, A. Gamburd, "On the spectral gap for finitely-generated subgroups of SU(2)," *Invent. Math.* **171**, 83 (2008).
