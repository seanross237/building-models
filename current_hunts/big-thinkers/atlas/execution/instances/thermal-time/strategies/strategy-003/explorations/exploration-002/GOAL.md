# Exploration 002: Adversarial Review of All TTH Claims

## Mission Context

We have tested the Connes-Rovelli Thermal Time Hypothesis (TTH) across 6+ regimes over two prior strategies and one additional exploration. The claims below need adversarial review: prior art search, numerical artifact checks, and conceptual stress-testing.

**Critical update from Exploration 001 (this strategy):** The Gaussian approximation caveat on Claim 3 has been RESOLVED. A squeezed vacuum state (Gaussian-exact modular Hamiltonian, no approximation) shows the same structural mismatch: modular flow at wrong frequencies, discrepancy growing as N^{0.44} in the continuum limit. Claim 3 now stands without qualification.

## Your Task: Three-Part Adversarial Review

### Part A: Prior Art Search

For EACH claim below, search for the closest prior art. Use web search and arXiv. The search MUST either find prior art or demonstrate convincingly that none exists (by documenting search terms used, papers checked, and negative results).

**Search terms to use (combine and vary):**
- "modular Hamiltonian quench" / "modular flow non-equilibrium" / "thermal time hypothesis test"
- "excited state modular Hamiltonian lattice" / "Bisognano-Wichmann excited state"
- "modular flow correlator" / "modular automorphism physical time"
- "thermal time preparation history" / "state-dependent time quantum"
- "modular flow spectral content" / "entanglement Hamiltonian dynamics"

**Authors to check (search for their papers on modular Hamiltonians, TTH, modular flow):**
- Lashkari, Casini, Huerta, Faulkner, Cardy, Tonni, Witten
- Rovelli, Connes, Martinetti, Hollands, Sanders
- Ciolli, Longo, Morinelli

**For each claim, report:**
(a) Closest prior art found (title, authors, arXiv ID, specific equation/section)
(b) What's genuinely new vs. what's a corollary of known results
(c) What an AQFT specialist would say about the claim

**CRITICAL: Search for the CONCLUSION, not just the technique.** Check whether "modular time tracks preparation history" or "modular flow generates pre-quench dynamics" has already been articulated by TTH researchers (Rovelli, Martinetti, Connes, etc.). The computational technique may be new but the conclusion may be known.

### Part B: Conceptual Attacks

Engage seriously with these three attacks. Don't dismiss them — steelman them, then respond.

**Attack 1: "TTH was never meant for non-equilibrium states."**
- Re-read Connes-Rovelli 1994 (gr-qc/9406019), specifically Sections 4-5.
- Does TTH require the state to be KMS? If so, testing non-KMS states is out-of-scope.
- If Claims 1, 3, and 4 are "demonstrations of TTH's limitations" rather than "falsifications of TTH," does this weaken their significance? Or is mapping the boundary of validity itself a contribution?

**Attack 2: "Modular flow of an excited state SHOULD differ from the boost — that's a feature, not a bug."**
- A TTH proponent could argue: the modular flow of an excited state defines the CORRECT notion of time for an observer in that state.
- Why is the boost "more physical" than the modular flow?
- Can we distinguish them experimentally? If not, is the "mismatch" just a matter of interpretation?

**Attack 3: "The lattice is not type III."**
- The half-lattice algebra is type I (finite-dimensional), not type III₁ (Rindler).
- Type III₁ is only recovered in the continuum limit.
- Are lattice results trustworthy predictors of continuum behavior?
- The convergence data shows discrepancy GROWING with N — does this strengthen or weaken the lattice-to-continuum extrapolation?

### Part C: Null Hypothesis Test

Frame the adversarial as: **Can these observations be explained by standard QM without TTH?** For each claim, ask: **Is this either known or wrong?**

Specifically:
1. "Post-quench modular flow = pre-quench dynamics" — is this just the tautology K = -log(rho) = beta*H_0 for a Gibbs state of H_0?
2. "Modular flow at wrong frequencies for excited states" — is this just saying the modular Hamiltonian is not the physical Hamiltonian (which is trivially true for excited states)?
3. "Squeezed states have quantitative not structural discrepancy" — is this just saying K_sq ≈ S(beta*H)S† ≈ beta*H + O(r)?

For each: if the answer is "yes, this is trivially known," rate the novelty as LOW but assess whether the explicit computation and systematic domain map add value beyond the trivial observation.

## Claims to Review

### Claim 1: Post-quench modular flow generates pre-quench dynamics
**Evidence:** Exact analytical formulas. C_QM(t) = A/2[cos(omega_+ t) + cos(omega_- t)], C_global(t) = A*cos(omega*t). Verified numerically to 10^{-9}. Spectral peaks disjoint. Asymptotic discrepancy = sqrt(3). (S2-E002)
**Prior art candidates:** Cardy & Tonni 2016 (arXiv:1602.08273), Hollands & Sanders 2017 (arXiv:1702.04924)
**Known weakness:** May be considered a trivial consequence of K = -log(rho_0) = beta*H_0 for the thermal state of H_0.

### Claim 2: Product-state identity (C_global = C_local for product states)
**Evidence:** Numerical (10^{-16}) and algebraic proof from [K_B, x_A ⊗ I_B] = 0. (S2-E002)
**Prior art candidates:** Takesaki Vol. II, Theorem IX.4.2 (tensor product modular operators)
**Known weakness:** Likely a known result.

### Claim 3 (STRONGEST — now with Gaussian caveat RESOLVED):
Excited-state (and squeezed-state) modular flow has structurally wrong frequency content
**Evidence:**
- One-particle state (Gaussian approx): Zero spectral weight at physical omega_m. Delta_disc ~ N^{0.33}. (S2-E003)
- Squeezed vacuum (EXACT, no approximation): Zero spectral weight at physical omega_m. Delta_disc ~ N^{0.44}. Discrepancy 5.7-14.4x across N=50-400. (S3-E001)
- Coherent state: delta_C_local = constant (no frequency content at all), delta_C_full oscillates at omega_m. (S3-E001)
**Prior art candidates:** Faulkner 2015 series (arXiv:1501.06444), Lashkari 2016 (arXiv:1508.03506), Casini-Huerta 2009 (arXiv:0903.5284)
**Known weakness:** Does the growing discrepancy just reflect the fact that the lattice approaches type III (where modular flow is more "different" from time translation)?

### Claim 4: Squeezed states have quantitative (not structural) TTH discrepancy
**Evidence:** Global TTH 7.8% for squeezed vs. 102% for post-quench (same lambda=0.3). Squeezed state has correct normal-mode frequencies. (S2-E002)
**Known weakness:** Single data point. Needs systematic study (planned for E003 of this strategy).

### Central Interpretation: "Modular time is preparation-history time"
**Evidence:** All 6+ regimes consistent. Post-quench → pre-quench dynamics. Gibbs/vacuum → current dynamics (because preparation = current). Squeezed (close to Gibbs) → approximate agreement.
**Prior art candidates:** This is the most important thing to check. Has Rovelli, Martinetti, Connes, or any AQFT researcher already stated this? Check their review papers and lecture notes.
**Known weakness:** May be considered an obvious rephrasing of K = -log(rho), which encodes the state (= preparation history), not the Hamiltonian.

## Output

Write REPORT.md and REPORT-SUMMARY.md in this directory.

**REPORT.md structure:**
1. Per-claim adversarial review (prior art found, novelty rating 1-5, verdict: confirmed/weakened/falsified)
2. Conclusion-level prior art assessment (has the "preparation-history time" interpretation been stated?)
3. Conceptual attack engagement (Attack 1, 2, 3)
4. Null hypothesis assessment
5. Consolidated claims table with final ratings

**REPORT-SUMMARY.md:** Concise summary with the consolidated claims table.

**Write REPORT.md incrementally** — complete each section and write it to the file before starting the next. Do not wait until the end to write everything.

## Success Criteria

1. For each claim: closest prior art identified (or specific evidence none exists)
2. Each conceptual attack engaged seriously (steelmanned, then responded to)
3. Null hypothesis considered for each claim
4. Final verdict for each claim: novelty rating (1-5), status (confirmed/weakened/falsified/known)
5. The central interpretation ("preparation-history time") has been specifically checked against Connes, Rovelli, Martinetti, and other TTH researchers

## Failure Criteria

- Prior art search is superficial (just listing paper titles without reading relevant sections)
- Conceptual attacks are dismissed rather than steelmanned
- No null hypothesis assessment
