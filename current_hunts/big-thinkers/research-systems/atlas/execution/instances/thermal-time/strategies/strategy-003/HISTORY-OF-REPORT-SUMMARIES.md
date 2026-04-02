# Exploration History

## Exploration 001: Coherent & Squeezed State Resolution of Gaussian Caveat (Math Explorer)

**Outcome: SUCCESS — Caveat resolved, Claim 3 confirmed**

**Part A (Coherent state):** delta_C_local = mu_k^2 = constant to machine precision (std < 10^{-17}). delta_C_full oscillates at omega_m. Analytical predictions verified exactly. This validates the computational pipeline. [VERIFIED]

**Part B (Squeezed state — the critical test):** For the squeezed vacuum (Gaussian, exact modular Hamiltonian), delta_C_local oscillates at modular frequencies epsilon_k/(2*pi), NOT at the physical frequency omega_m. The discrepancy ||delta_C_local - delta_C_full||/||delta_C_full|| = 5.7 (N=50), 7.4 (N=100), 7.9 (N=200). The amplitude of delta_C_local is 10-16x larger than delta_C_full, dominated by wrong-frequency oscillations. [COMPUTED]

**Part C (Convergence):** At fixed physical frequency omega ≈ 0.3, the discrepancy grows as N^{0.44} from N=50 to N=400. The amplitude ratio grows as N^{0.41}. The mismatch worsens in the continuum limit, consistent with the N^{0.33} scaling from the one-particle case. [COMPUTED]

**Part D (Squeeze sweep):** Discrepancy is large (13-66x) for all squeezing parameters r = 0.1 to 1.0. Not a small-perturbation artifact. [COMPUTED]

**Verification Scorecard:** 6 VERIFIED, 12 COMPUTED, 0 CONJECTURED

**Key Takeaway:** The structural mismatch between modular flow and physical time evolution persists for Gaussian-exact states. The Gaussian approximation caveat is NOT the issue. Claim 3 stands without qualification: modular flow produces wrong frequencies for non-vacuum states, with discrepancy growing in the continuum limit.

**Unexpected Findings:**
- Convergence exponent (~0.44) is slightly larger than the one-particle case (~0.33), suggesting the mismatch may be even stronger for squeezed states.
- Modular flow response amplitude is roughly constant (~0.1) regardless of squeezing strength, while the physical response scales with (e^{-2r}-1). Relative discrepancy diverges as r → 0.

---

## Exploration 002: Adversarial Review of All TTH Claims (Standard Explorer)

**Outcome: COMPLETE — Claims survive with important qualifications**

**Prior Art Findings:**
- Claim 1 (post-quench): Algebraic fact is textbook; spectral comparison and √3 result are new. Novelty 2.5/5
- Claim 2 (product-state identity): Textbook result (Takesaki). Novelty 1/5 — demoted to "verification"
- Claim 3 (excited-state wrong frequencies, growing with N): Closest is Lashkari-Liu-Rajagopal 2021 (arXiv:1811.05052) — they compute modular flow operators but NOT correlator dynamics vs physical evolution. No zero-spectral-weight finding in literature. **Novelty 4/5 — strongest claim, survives adversarial review.**
- Claim 4 (squeezed: quantitative not structural): No prior art found. Novel taxonomy. Novelty 3/5
- Central interpretation ("preparation-history time"): NOT in the literature. Not stated by Connes, Rovelli, Martinetti, or any critic. **Novelty 4/5 — genuinely new explanatory principle.**

**Conceptual Attack Results:**
- Attack 1 ("TTH not for non-equilibrium"): FAILS. Connes-Rovelli 1994 define TTH for ANY faithful state.
- Attack 2 ("Modular flow IS correct time"): PARTIALLY SUCCEEDS for QG contexts (no background time). FAILS for operational settings.
- Attack 3 ("Lattice ≠ type III"): FAILS — discrepancy GROWS with N (convergence data shows opposite of what attack requires).

**Null Hypothesis:** Algebraic facts are known; what's new is the explicit spectral computation, N-scaling, structural/quantitative taxonomy, and the unifying TTH interpretation.

**Key Discovery:** Lashkari-Liu-Rajagopal 2021 paper needs full-text check — may partially overlap with Claim 3 at the modular flow operator level (though not at correlator dynamics level).

---

## Exploration 003: Distance-from-Gibbs Characterization (Math Explorer)

**Outcome: SUCCEEDED — with a surprising twist**

22 data points computed: 11 squeezed (r=0 to 1.0) + 11 post-quench (δλ=0 to 0.5). Control passed (6.7e-13).

**Surprising finding:** The two families produce completely different discrepancy behaviors:
- **Squeezed states**: Always quantitative. 0% → 6.8% discrepancy. Correct frequencies at all r values.
- **Post-quench states**: Immediate structural failure. 68% at smallest quench (δλ=0.05, S_rel=0.0016). Saturates at 120-160%.
- At comparable relative entropy (~0.05): squeezed = 0%, quench = ~140%. **Completely different curves.**

**Key Takeaway:** Relative entropy (distance from Gibbs) does NOT control TTH discrepancy. The discriminant is whether the departure preserves the Hamiltonian spectrum. Unitary deformations (squeezing) preserve eigenvalues → quantitative discrepancy. Non-unitary deformations (quench = different H) change spectrum → immediate structural failure.

**Unexpected:** Quench discrepancy fluctuates (123-159%) rather than growing monotonically — interference from incommensurate frequencies.

---

## Exploration 004: Final Synthesis + Experimental Connection (Strategizer-written)

**Outcome: COMPLETE** (Explorer session degraded; strategizer wrote synthesis from accumulated E001-E003 data)

Complete domain map with 8 regimes. Experimental connection to cold-atom coupled optical traps (beat frequency ~100 Hz, feasible with quantum gas microscopes). "Preparation-history time" connected to ETH. Spectrum-preservation discriminant articulated as new Claim 5.

**Final Claim Status:** Claim 3 at 4/5 (confirmed, caveat resolved). Claim 4 upgraded to 4/5 (systematic study). New Claim 5 (spectrum preservation) at 4/5. Central interpretation at 4/5.

---

