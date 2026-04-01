# Proof Chains for Classicality Budget Claims

What would it take to make each claim bulletproof? Below is the logical dependency chain for each, the weakest link, and what a structured Atlas mission targeting that chain would look like.

---

### Claim 1: QD-HQEC Formal Mapping

**Current status:** A dictionary between Quantum Darwinism and Holographic QEC was written down. The HaPPY code 50% result is stated but not numerically verified. Five known gaps in the mapping are identified but not resolved. The "no one has done this" evidence is from search queries, not exhaustive review.

**Proof chain:**

1. Establish that the QD axioms (tensor product environment, redundancy definition, objectivity condition) can be stated in boundary-subregion language without loss of content.
2. Show that the HQEC reconstruction condition (x in entanglement wedge of R_k) is equivalent to the QD objectivity condition I(S:F_k) >= (1-delta)H_S under approximate QEC, not just analogous.
3. Resolve the pointer-state gap: demonstrate that einselection (dynamical, Hamiltonian-dependent) has a natural HQEC counterpart, or prove the mapping holds only for a restricted class of states where this gap closes.
4. Resolve the delta-threshold gap: show that the continuous delta parameter in QD maps to the approximate reconstruction fidelity in approximate QEC, with a quantitative relationship between the two.
5. Resolve the dynamics gap: either show that QD's temporal growth of R_delta maps to some HQEC process (e.g., modular flow, boundary time evolution) or explicitly characterize the mapping as kinematic-only.
6. Verify the HaPPY 50% result by tensor network contraction: compute R_delta for the HaPPY pentagon code and confirm R_delta = n/2 = S_max/(2*S_T).
7. Show the mapping is not an artifact of both frameworks being "quantum information in disguise" — demonstrate a non-trivial prediction that follows from the mapping but not from either framework alone.

**Weakest link:** Step 2. The mapping currently equates things that look similar but live in different mathematical structures. QD's mutual information condition is an information-theoretic statement about density matrices. HQEC's entanglement wedge reconstruction is a statement about operator algebra inclusion. Showing these are *equivalent* (not just analogous) under precise conditions is the hard mathematical step. Without it, the mapping is a suggestive dictionary rather than a theorem.

**What a structured Atlas run would look like:**
- Exploration 1: Formalize both conditions in a common mathematical language (operator-algebraic QI). Produce a precise conjecture statement with all quantifiers explicit.
- Exploration 2: Attack the pointer-state gap. Survey einselection in exactly solvable models and check whether HQEC's code subspace picks out the same preferred basis.
- Exploration 3: Attack the delta-threshold gap. Derive the quantitative relationship between delta and approximate QEC fidelity using known bounds from Beny-Oreshkov or Junge et al.
- Exploration 4: Numerically verify the HaPPY 50% result via tensor network contraction.
- Exploration 5: Derive a non-trivial prediction from the mapping. Best candidate: use known HQEC results (e.g., entanglement wedge nesting, Python's lunch) to predict new QD phenomena that can be checked in spin-chain simulations.
- Exploration 6: Adversarial review of the full chain — attempt to construct a counterexample where the dictionary entries hold individually but the mapping fails as a whole.

---

### Claim 2: The Classicality Budget Formula

**Current status:** The formula R_delta <= (S_max/S_T - 1)/(1-delta) is derived from 5 axioms. The derivation appears mathematically sound. The "tensor product catch-22" (budget constraining only where its assumptions break down) was identified as SERIOUS and partially resolved via holographic reformulation, but not fully closed.

**Proof chain:**

1. Verify axiom 1 (tensor product structure) holds in each claimed domain of applicability, or replace it with a weaker assumption that still yields the bound.
2. Confirm that the Holevo bound (axiom 5) is the tightest available bridge — rule out that a tighter bound (e.g., accessible information for specific channel types) would change the formula's form.
3. Resolve the tensor product catch-22 completely: either (a) prove the holographic boundary reformulation rigorously yields the same formula without assuming bulk tensor product structure, or (b) explicitly delineate the domain of validity and accept the formula is only non-vacuous there.
4. Show the bound is achievable (not just an upper bound): exhibit at least one physical system where R_obs approaches R_max, proving the bound is not loose by orders of magnitude.
5. Demonstrate that R_delta is a genuinely new physical quantity — show it cannot be algebraically recovered from the Bekenstein bound plus standard QD definitions in a single step (i.e., the Holevo bridge is doing real work, not just rephrasing).

**Weakest link:** Step 3. The catch-22 is the structural problem: the budget is interesting at horizons and Planck scale, but tensor product structure (axiom 1) is precisely what breaks down there. The holographic reformulation was described as a resolution but not rigorously completed. If the formula only holds where it is vacuous, it is not physically meaningful as a bound.

**What a structured Atlas run would look like:**
- Exploration 1: Rigorous holographic reformulation. Start from boundary subregion entropy (RT formula) and boundary mutual information. Derive the budget without ever invoking bulk tensor product structure. State all assumptions.
- Exploration 2: Achievability analysis. Pick 2-3 systems where the budget is non-vacuous (ion trap, quantum dot) and compute or simulate the actual R_obs. How close does it get to R_max?
- Exploration 3: Tightness of the Holevo step. For the specific quantum channels arising in QD (complementary channels of the decoherence interaction), compute the accessible information and compare to Holevo. If accessible information is much less than Holevo, the budget could be tightened.
- Exploration 4: Adversarial — attempt to derive R_delta directly from Bekenstein + QD definitions without using Holevo. If you can, the Holevo bridge is not doing real work.

---

### Claim 3: Black Hole Universal Constants

**Current status:** Three constants (S_Hawking, N_photons, R_1bit) were computed using flat-space blackbody approximation at the Hawking temperature. Literature search found no prior publication of these specific numerical values. The derivation uses T_H * r_s = hbar*c/(4*pi*k_B), which is standard.

**Proof chain:**

1. Verify the flat-space blackbody approximation: confirm that using Stefan-Boltzmann at T_H in a sphere of radius r_s is physically justified (not just dimensionally correct). What are the greybody corrections?
2. Compute the curved-space corrections. Page's stress tensor, greybody factors, and backscattering modify the flat-space result. Determine whether the corrections change the constants by O(1) or just O(%) factors.
3. Establish that the specific sphere radius r_s is physically meaningful. Why r_s and not 2r_s or 3r_s? The choice of integration volume is a free parameter that changes the numerical constants.
4. Confirm the algebraic cancellation (1/540 = 1/(9*60)) is exact and not an artifact of approximations that hide order-unity corrections.
5. Demonstrate physical significance: show that R_1bit = 7.21 r_s corresponds to an observable or operationally meaningful boundary (e.g., where a specific measurement protocol transitions from possible to impossible).

**Weakest link:** Step 2/3 together. The constants are computed in flat-space thermodynamics applied at a specific radius. Near a black hole, spacetime is curved, greybody factors modify the spectrum, and the choice of "one Schwarzschild radius away" as the integration volume is somewhat arbitrary. If curved-space corrections or a different natural length scale change the leading coefficient, the specific numbers 1/(540 ln 2) and 7.21 lose their claimed universality. They would still be order-of-magnitude correct, but "universal constant" implies exactness.

**What a structured Atlas run would look like:**
- Exploration 1: Compute greybody factors for a Schwarzschild BH and determine the corrected S_Hawking. Quantify the flat-space error.
- Exploration 2: Justify or replace the choice of r_s as integration radius. Survey what other natural length scales exist (photon sphere at 3r_s/2, ISCO at 3r_s, etc.) and whether any of them produce cleaner constants.
- Exploration 3: Compute the constants using Page's stress tensor in Hartle-Hawking state. Compare to flat-space values.
- Exploration 4: If the constants survive corrections, prove the physical significance of R_1bit as an operational boundary for a specific measurement task.

---

### Claim 4: Ion Trap Classicality Phase Transition

**Current status:** A phase transition at n_bar_c ~ 0.003 is predicted from the budget formula applied to a 20-ion trap. The experimental protocol is sketched. No Lindblad simulation of the actual dynamics has been done — the prediction is purely from the upper bound.

**Proof chain:**

1. Confirm the budget formula applies to the ion trap system: verify that the 20-ion motional mode environment satisfies tensor product structure (axiom 1) to sufficient approximation.
2. Validate the entropy model: confirm that S_eff for the phonon environment at mean occupation n_bar is correctly computed (thermal state entropy of N harmonic oscillators).
3. Show the budget is achievable in this system: simulate or analytically solve the specific decoherence dynamics (system qubit coupling to motional modes) and show R_obs actually approaches R_max, not just that R_max exists.
4. Characterize the phase transition: is it sharp (discontinuous in some derivative of R_obs) or a smooth crossover? The budget gives a sharp cutoff, but the actual dynamics may smooth it out.
5. Confirm experimental feasibility: verify that shadow tomography of ~10-mode fragments is achievable at the required n_bar, and that the measurement itself does not inject enough entropy to move n_bar above the critical value.
6. Rule out trivial explanations: show the transition is not simply "below n_bar_c there is not enough entropy in the environment to carry any information" (which would be trivially true and not a QD-specific prediction).

**Weakest link:** Step 3. The budget is an upper bound. The actual redundancy achieved depends on the Hamiltonian, the coupling structure, and the timescale. If R_obs is far below R_max (e.g., R_obs ~ 0 for all n_bar because the coupling is too weak), the phase transition predicted by the bound would be unobservable. The mission never simulated the dynamics to check whether the bound is approached.

**What a structured Atlas run would look like:**
- Exploration 1: Lindblad simulation. Model the standard ion-trap decoherence Hamiltonian (system qubit + N motional modes with known coupling). Compute R_obs(t) as a function of time and n_bar. Does R_obs approach R_max?
- Exploration 2: Phase transition characterization. From the simulation, extract R_obs(n_bar) at the steady state. Is the transition sharp or smooth? At what n_bar does R_obs first exceed 1?
- Exploration 3: Experimental feasibility deep-dive. Consult trapped-ion experimental parameters (coupling strengths, decoherence rates, measurement fidelities). Determine whether the required mutual information measurement is feasible within coherence times.
- Exploration 4: Trivial-explanation check. Compute the maximum mutual information the environment can carry as a function of n_bar, independent of QD. If this already shows a phase transition at the same n_bar_c, the QD budget adds nothing.

---

### Claim 5: Two-Stage Classicality Through BH Evaporation

**Current status:** Exterior classicality (from Hawking radiation entropy accumulation) and interior classicality (from island/Page transition) are described. The mission itself rates this as "LOW-MEDIUM" novelty — mostly repackaging known HQEC results in QD language.

**Proof chain:**

1. Verify the exterior classicality calculation: confirm t_classical ~ (2/S_BH) * t_Page using the correct Hawking emission rate and the classicality budget.
2. Verify the interior classicality calculation: confirm R_delta_int jumps from -1 to S_BH/2 - 1 at the Page time, using the island formula correctly.
3. Show the two-stage structure is not just a trivial consequence of "information accumulates gradually, then the island appears" — identify what QD adds beyond what is already known from the Page curve and entanglement wedge reconstruction.
4. Demonstrate that R_delta is a more informative quantity than the binary "reconstructable / not reconstructable" of standard HQEC — show a scenario where the R_delta value matters (e.g., distinguishes between cases that HQEC treats identically).

**Weakest link:** Step 3. The mission document itself acknowledges this is largely a repackaging. The exterior stage is "Hawking radiation accumulates entropy" (known). The interior stage is "Page transition enables reconstruction" (known). What would make this non-trivial is identifying a physical scenario where the R_delta quantification reveals something the binary HQEC picture misses.

**What a structured Atlas run would look like:**
- Exploration 1: Identify a concrete physical question where R_delta > 1 vs R_delta = 1 matters observationally. For example: does R_delta predict different decoherence rates for different Hawking radiation observables?
- Exploration 2: Compute R_delta(t) through the full evaporation using a more realistic model (not just linear + island jump). Does the Page transition produce a smooth or discontinuous change in R_delta?
- Exploration 3: Adversarial — attempt to derive all "new" predictions of the two-stage picture from standard HQEC + Page curve alone. If you can, the QD framing adds no content.

---

## Summary: Priority Order for Future Missions

Ranked by which proof chain, if completed, would add the most value:

1. **Claim 1 (QD-HQEC mapping):** Highest payoff, hardest chain. The equivalence-vs-analogy question (step 2) is the key gate. A mission structured around formalizing the mapping in operator-algebraic language and finding a non-trivial prediction would either establish a real result or expose it as mere analogy.

2. **Claim 4 (ion trap phase transition):** Highest experimental impact. The entire chain hinges on step 3 (achievability). A single Lindblad simulation mission would resolve whether this is a real prediction or a vacuous bound.

3. **Claim 2 (budget formula):** The catch-22 resolution (step 3) is the structural bottleneck. A mission focused on the holographic reformulation would either put the formula on solid ground or confirm it is only valid where vacuous.

4. **Claim 3 (BH constants):** Clean and self-contained. A single mission computing greybody corrections and justifying the integration volume would either confirm or correct the specific numbers.

5. **Claim 5 (two-stage BH classicality):** Lowest priority. Only worth pursuing if step 3 (non-trivial QD content beyond HQEC) can be affirmatively answered, which likely depends on Claim 1's proof chain being completed first.
