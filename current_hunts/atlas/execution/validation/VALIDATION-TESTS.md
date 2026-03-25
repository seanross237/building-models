# Validation Test Suite

Structured tests for physics theories, organized from easiest to hardest. Work through them in order as your theory matures. **Skip any test whose prerequisites aren't met** — that's normal and expected.

---

## Tier 1: Structural Sanity

*Run these first. If these fail, your theory has foundational issues.*

---

### Test 1.1: Well-Defined Action or Partition Function

**Category:** Structural
**Difficulty:** Basic
**Prerequisites:** You have written down a theory (not just verbal ideas).
**The Test:** Does your theory have an explicit action S or partition function Z = integral D[fields] exp(-S)?
**Expected Result:** A concrete mathematical expression for S or Z with all terms defined.
**Method:** Write out S. Identify every field, coupling, and integration measure. Check that all indices contract and dimensions match.
**Pass Criteria:** S or Z is written explicitly with no undefined symbols.
**If it fails:** You have a framework or an idea, not a theory yet. That's fine — formalize it before proceeding.
**Skip if:** You're still in the brainstorming / conceptual phase.

---

### Test 1.2: Correct Degrees of Freedom

**Category:** Structural
**Difficulty:** Basic
**Prerequisites:** An action or equations of motion exist.
**The Test:** How many propagating degrees of freedom does your theory have in d=4?
**Expected Result:** A massless graviton in 4D has exactly **2** physical degrees of freedom (helicity +2 and -2). A massive graviton has **5**.
**Method:** Count DOF using the formula: DOF = (field components) - (constraints from EOM) - (gauge redundancies). For a symmetric tensor h_uv in 4D: 10 components - 4 Bianchi identities - 4 diffeomorphisms = 2.
**Pass Criteria:** 2 DOF for massless spin-2, or 5 DOF for massive spin-2 (with mass within experimental bounds).
**If it fails:** Extra DOF usually signal ghosts or extra fields. Identify them — they might be physical (scalar mode, etc.) or pathological.
**Skip if:** Your theory isn't yet at the point where you can count propagating modes.

---

### Test 1.3: Gauge Symmetry

**Category:** Structural
**Difficulty:** Basic
**Prerequisites:** A linearized version of the theory exists.
**The Test:** Does your theory have a gauge symmetry consistent with linearized diffeomorphisms?
**Expected Result:** The linearized action should be invariant under h_uv -> h_uv + partial_u xi_v + partial_v xi_u for arbitrary vector xi_u.
**Method:** Substitute the gauge transformation into your linearized action and verify it vanishes (or changes by a total derivative).
**Pass Criteria:** Linearized diffeo invariance holds, or there's a Stueckelberg mechanism that restores it.
**If it fails:** Without diffeomorphism invariance, your theory likely doesn't describe gravity. Check whether you've broken the symmetry intentionally (massive gravity) or accidentally.
**Skip if:** Your theory is inherently discrete or non-perturbative and doesn't have a linearized regime yet.

---

### Test 1.4: Ghost Freedom

**Category:** Structural
**Difficulty:** Intermediate
**Prerequisites:** You can compute the propagator or Hamiltonian.
**The Test:** Are there any negative-norm states (ghosts) in the physical spectrum?
**Expected Result:** No ghosts — all physical states have positive norm. The Hamiltonian is bounded from below.
**Method:** Compute the propagator. Check that all residues at poles have the correct sign. Equivalently, verify the kinetic terms all have the same sign. For higher-derivative theories: decompose into spin sectors and check each one.
**Pass Criteria:** All propagator residues positive (or zero for gauge modes). No Boulware-Deser ghost (for massive gravity). No Ostrogradsky ghost (for higher-derivative theories).
**If it fails:** Ghosts mean the vacuum is unstable. This is fatal unless you have a mechanism to decouple them (e.g., they appear only above a cutoff). See Boulware-Deser (1972), Ostrogradsky theorem.
**Skip if:** You can't yet compute the propagator.

---

### Test 1.5: Unitarity

**Category:** Structural
**Difficulty:** Intermediate
**Prerequisites:** S-matrix or scattering amplitudes are computable.
**The Test:** Is the S-matrix unitary (SS^dagger = 1)? Equivalently, is the optical theorem satisfied?
**Expected Result:** Total cross-sections are positive. Probabilities sum to 1. No negative probabilities at tree level.
**Method:** Check the optical theorem: Im[M(k->k)] = (1/2) sum_f integral |M(k->f)|^2. At tree level, check that all partial-wave amplitudes satisfy |a_l| <= 1.
**Pass Criteria:** Optical theorem satisfied at leading order. No negative partial-wave amplitudes.
**If it fails:** Unitarity violation at a scale Lambda means the theory needs UV completion above Lambda. This isn't necessarily fatal — it tells you where your effective theory breaks down. If unitarity is violated at *all* scales, the theory is sick.
**Skip if:** You can't yet compute scattering amplitudes.

---

### Test 1.6: Dimensional Consistency

**Category:** Structural
**Difficulty:** Basic
**Prerequisites:** An action is written down.
**The Test:** Do all terms in the action have consistent mass dimensions? Is the action dimensionless (in natural units)?
**Expected Result:** [S] = 0 in natural units (h-bar = c = 1). Each term in the Lagrangian density must have mass dimension d (= 4 in 4D).
**Method:** Assign dimensions to each field and coupling. Verify every term in L has [L] = d.
**Pass Criteria:** All terms dimensionally consistent. No dimensionful mismatches.
**If it fails:** Usually a typo or missing coupling constant. Easy fix, but important to catch.
**Skip if:** Never skip this one. Always check dimensions.

---

## Tier 2: Known Physics Recovery

*These verify your theory reproduces what we already know works. Run them once you have concrete expressions.*

---

### Test 2.1: Graviton Propagator Matches GR

**Category:** Quantitative
**Difficulty:** Intermediate
**Prerequisites:** A linearized propagator is derived.
**The Test:** In the appropriate limit, does your propagator match the linearized GR propagator?
**Expected Result:** The propagator should approach G_uv,ab(k) = (P^(2)_uv,ab - P^(0)_uv,ab / 2) / k^2, where P^(2) and P^(0) are the spin-2 and spin-0 projection operators (in de Donder gauge).
**Method:** Compute the propagator from your action. Take any new-physics parameters to zero (or the appropriate IR limit). Compare tensor structure and pole structure to the GR result.
**Pass Criteria:** Propagator matches GR in the IR/low-energy limit, up to gauge-dependent terms.
**If it fails:** Identify which term differs. Extra poles suggest extra particles. Wrong tensor structure suggests wrong DOF count (recheck Test 1.2).
**Skip if:** Your theory doesn't have a standard perturbative expansion around flat space.

---

### Test 2.2: Newton's Law Recovery

**Category:** Quantitative
**Difficulty:** Basic
**Prerequisites:** A non-relativistic limit can be taken.
**The Test:** In the non-relativistic, weak-field limit, does your theory produce F = -GMm/r^2?
**Expected Result:** The gravitational potential V(r) = -GM/r at distances r >> l_P (and r >> any new length scale in your theory).
**Method:** Compute the static potential from the propagator: V(r) = -(1/M_Pl^2) integral d^3k/(2pi)^3 [exp(ik.r) / k^2] = -G M / r. If your theory has modifications, check they're suppressed at large r.
**Pass Criteria:** V(r) -> -GM/r for r >> 50 um (the shortest scale where Newton's law is tested).
**If it fails:** Your theory predicts a non-Newtonian force. Check: does it give V(r) ~ -GM/r * (1 + alpha * exp(-r/lambda))? If so, alpha and lambda must be within experimental bounds (Adelberger et al.).
**Skip if:** Your theory is only defined at Planck-scale energies and you haven't worked out the IR limit.

---

### Test 2.3: Three-Graviton Vertex

**Category:** Quantitative
**Difficulty:** Advanced
**Prerequisites:** Cubic interaction terms are computed.
**The Test:** Does the three-graviton vertex match General Relativity's?
**Expected Result:** The cubic vertex from expanding the Einstein-Hilbert action to third order in h_uv. This is a specific (lengthy) tensor structure involving momenta and polarizations.
**Method:** Expand your action to cubic order in the graviton field. Compare the resulting vertex factor to the GR result (e.g., Sannan 1986, or DeWitt's vertex). Check on-shell amplitudes if off-shell comparison is too gauge-dependent.
**Pass Criteria:** On-shell 3-graviton amplitude matches GR. Equivalently, the theory passes the Weinberg-Witten theorem requirements for a massless spin-2 particle.
**If it fails:** Different cubic vertices mean your theory departs from GR at the nonlinear level. This is allowed for modified gravity theories, but the deviations must be consistent with all binary pulsar and GW observations.
**Skip if:** You haven't computed interaction terms yet, or your theory is intrinsically non-perturbative.

---

### Test 2.4: Lorentz Invariance

**Category:** Consistency
**Difficulty:** Intermediate
**Prerequisites:** The theory is formulated in a way where Lorentz symmetry can be assessed.
**The Test:** Is Lorentz invariance preserved, or if broken, are violations below experimental bounds?
**Expected Result:** Either exact Lorentz invariance, or violations parametrically smaller than the bounds in EXPERIMENTAL-DATA.md (photon: delta_c/c < 10^-33; gravity: delta_c/c < 10^-15).
**Method:** Identify any preferred frame or direction in the theory. Compute the leading Lorentz-violating operators. Compare their coefficients to the SME (Standard Model Extension) data tables.
**Pass Criteria:** All Lorentz-violating coefficients within known bounds. Or: the theory is exactly Lorentz invariant.
**If it fails:** Lorentz violation bounds are incredibly tight. Even Planck-suppressed violations (E/M_Pl) are borderline constrained. If your theory violates Lorentz invariance, you need a mechanism to suppress it well below E/M_Pl.
**Skip if:** Your theory is manifestly Lorentz invariant by construction.

---

### Test 2.5: Equivalence Principle

**Category:** Consistency
**Difficulty:** Intermediate
**Prerequisites:** The theory couples to matter.
**The Test:** Does your theory satisfy the Einstein equivalence principle? Specifically: does gravity couple universally to all forms of energy-momentum?
**Expected Result:** All matter fields couple to gravity through the same metric. No composition-dependent forces. The Eotvos parameter eta < 10^-14.
**Method:** Check that the theory has a single metric that all matter couples to (no bi-metric coupling). Compute any composition-dependent fifth forces. Compare to MICROSCOPE bounds.
**Pass Criteria:** Universal coupling to a single metric, or composition-dependent effects below eta = 10^-14.
**If it fails:** EP violations are extremely constrained. If your theory has a scalar field that couples differently to different matter species, quantify the resulting eta parameter.
**Skip if:** Your theory doesn't include matter coupling yet.

---

### Test 2.6: Correct Linearized Equations of Motion

**Category:** Quantitative
**Difficulty:** Basic
**Prerequisites:** Equations of motion are derived.
**The Test:** Do the linearized equations of motion match the linearized Einstein equations?
**Expected Result:** Box h_uv - partial_u partial^a h_av - partial_v partial^a h_au + partial_u partial_v h + eta_uv (partial^a partial^b h_ab - Box h) = -16 pi G T_uv (in Lorenz gauge: Box h_uv = -16 pi G (T_uv - eta_uv T/2)).
**Method:** Linearize your EOM around flat space: g_uv = eta_uv + h_uv. Compare to the standard linearized Einstein equations.
**Pass Criteria:** Exact match in appropriate limit/gauge.
**If it fails:** Mismatch reveals extra terms in your theory that modify linearized gravity. Determine if they're consistent with bounds on parametrized post-Newtonian parameters.
**Skip if:** Your theory doesn't linearize around flat space.

---

## Tier 3: Quantitative Checks

*Run these when your theory produces specific numbers. This is where theories live or die.*

---

### Test 3.1: Graviton Mass Bound

**Category:** Quantitative
**Difficulty:** Basic
**Prerequisites:** The theory has a definite statement about the graviton mass (zero or nonzero).
**The Test:** If the graviton is massive, is m_g < 1.2 x 10^-22 eV?
**Expected Result:** m_g = 0 (massless graviton) or m_g below the LIGO bound.
**Method:** Read off the graviton mass from the propagator pole: G(k) ~ 1/(k^2 - m_g^2). Convert to eV.
**Pass Criteria:** m_g = 0 or m_g < 1.2 x 10^-22 eV.
**If it fails:** The theory predicts a graviton mass above the experimental bound. It's ruled out by LIGO observations. Consider whether the mass is a free parameter that can be tuned, or a prediction.
**Skip if:** You haven't computed the propagator poles.

---

### Test 3.2: Gravitational Wave Speed

**Category:** Quantitative
**Difficulty:** Intermediate
**Prerequisites:** The theory predicts a GW propagation speed.
**The Test:** Is |c_gw/c - 1| < 5 x 10^-16?
**Expected Result:** c_gw = c exactly, or deviations below 5 x 10^-16.
**Method:** Derive the dispersion relation for gravitational waves in your theory. The group velocity at LIGO frequencies (~100 Hz) must match c to the stated precision.
**Pass Criteria:** |c_gw/c - 1| < 5 x 10^-16 at frequencies ~10-1000 Hz.
**If it fails:** GW170817 + GRB 170817A killed many theories this way (e.g., most covariant Galileon models, many Horndeski theories). If your theory fails this test, it's essentially ruled out unless the modification turns on only at very different scales.
**Skip if:** Your theory predicts c_gw = c by construction (e.g., it preserves the full diffeomorphism group).

---

### Test 3.3: Lorentz Violation Parameters

**Category:** Quantitative
**Difficulty:** Advanced
**Prerequisites:** The theory has calculable Lorentz-violating operators.
**The Test:** Are all Lorentz-violating SME coefficients within experimental bounds?
**Expected Result:** All coefficients in the SME (Standard Model Extension) below the bounds tabulated in Kostelecky & Russell data tables.
**Method:** Map your theory's Lorentz-violating terms onto the SME framework. Extract the relevant coefficients. Compare to the data tables in EXPERIMENTAL-DATA.md.
**Pass Criteria:** All coefficients within bounds.
**If it fails:** Identify which sector (photon, electron, graviton, etc.) violates the bound and by how much. Often the fix is a symmetry that suppresses the problematic operators.
**Skip if:** Your theory is exactly Lorentz invariant, or you haven't computed the LV operators yet.

---

### Test 3.4: Black Hole Entropy

**Category:** Quantitative
**Difficulty:** Advanced
**Prerequisites:** The theory can describe black hole solutions and their thermodynamics.
**The Test:** Does your theory reproduce S_BH = A / (4 l_P^2) for large (semiclassical) black holes?
**Expected Result:** S = A/(4G) + (logarithmic and sub-leading corrections are allowed and interesting).
**Method:** Compute the entropy using your theory's framework (microstate counting, Wald formula, entanglement entropy, etc.). Compare the leading term to Bekenstein-Hawking.
**Pass Criteria:** Leading term is A/(4G). Subleading corrections should be computable and well-defined.
**If it fails:** The leading-order coefficient being wrong is a serious problem. The Bekenstein-Hawking formula is one of the most robust results in quantum gravity. Subleading corrections (e.g., -3/2 log A) are theory-dependent and debatable.
**Skip if:** Your theory doesn't yet have black hole solutions, or BH thermodynamics hasn't been worked out.

---

### Test 3.5: Spectral Dimension Running

**Category:** Quantitative
**Difficulty:** Advanced
**Prerequisites:** The theory has a notion of scale-dependent geometry (e.g., a running spectral dimension).
**The Test:** Does the spectral dimension run from d_s ~ 4 (IR) to d_s ~ 2 (UV)?
**Expected Result:** d_s -> 4 at large distances, d_s -> ~2 at the Planck scale. This is observed in CDT, Asymptotic Safety, Horava-Lifshitz, spin foams, and causal sets — suggesting it's a universal feature of quantum gravity.
**Method:** Compute the return probability P(sigma) on your quantum geometry. Extract d_s = -2 d(log P)/d(log sigma). Check the UV and IR limits.
**Pass Criteria:** d_s(IR) = 4.0 +/- 0.1, d_s(UV) in the range 1.5-2.5. A smooth interpolation between the two is ideal.
**If it fails:** Not getting d_s -> 2 in the UV doesn't kill your theory — it's not an experimental measurement, it's a theoretical benchmark. But matching this pattern would be a strong consistency check across QG approaches.
**Skip if:** Your theory doesn't have a notion of scale-dependent geometry, or this computation isn't feasible yet.

---

### Test 3.6: Post-Newtonian Parameters

**Category:** Quantitative
**Difficulty:** Intermediate
**Prerequisites:** The theory can be expanded in the post-Newtonian approximation.
**The Test:** Are the parametrized post-Newtonian (PPN) parameters consistent with observations?
**Expected Result:** gamma_PPN = 1, beta_PPN = 1 (GR values), or deviations within observational bounds.
**Method:** Expand the metric in powers of v/c for a static spherically symmetric source. Read off gamma_PPN (from the spatial part) and beta_PPN (from the time-time part at post-Newtonian order). Compare to Cassini (gamma) and lunar ranging (beta) bounds.
**Pass Criteria:** |gamma - 1| < 2.3 x 10^-5, |beta - 1| < 8 x 10^-5.
**If it fails:** Many modified gravity theories fail here. The PPN parameters are among the most constraining tests. Use Will (2014) "The Confrontation between General Relativity and Experiment" as a reference.
**Skip if:** Your theory doesn't yet have a post-Newtonian expansion.

---

## Tier 4: Novel Predictions

*Run these when your theory is mature. A good theory doesn't just reproduce known physics — it predicts something new.*

---

### Test 4.1: Novel Prediction Exists

**Category:** Prediction
**Difficulty:** Basic
**Prerequisites:** The theory passes Tiers 1-3 (at least partially).
**The Test:** Does your theory predict at least one observable that standard GR does not?
**Expected Result:** A specific, quantitative prediction. Not "there might be quantum gravity effects" but "this observable has value X +/- Y."
**Method:** Survey your theory's predictions. Identify anything that goes beyond classical GR + quantum field theory on curved spacetime.
**Pass Criteria:** At least one quantitative prediction identified.
**If it fails:** A theory with no novel predictions is not empirically distinguishable from GR. Push harder — compute corrections to known observables, identify new phenomena, or predict new particles/fields.
**Skip if:** The theory isn't mature enough for predictions yet. But if you've been working for many iterations without predictions, this is a flag.

---

### Test 4.2: Prediction Is Quantitative

**Category:** Prediction
**Difficulty:** Intermediate
**Prerequisites:** A novel prediction exists (Test 4.1 passes).
**The Test:** Can you give a number (or range of numbers) for the prediction?
**Expected Result:** A predicted value with error bars or a parametric expression relating the prediction to known constants.
**Method:** Compute the predicted observable to leading order. Estimate theoretical uncertainties.
**Pass Criteria:** A numerical value or parametric formula with identified uncertainties.
**If it fails:** Qualitative predictions ("something happens at the Planck scale") are useful for motivation but not for experimental verification. Push for numbers.
**Skip if:** The calculation is genuinely intractable at this stage.

---

### Test 4.3: Prediction Is Testable

**Category:** Prediction
**Difficulty:** Intermediate
**Prerequisites:** A quantitative prediction exists (Test 4.2 passes).
**The Test:** Is the prediction testable with current or near-future (next 20 years) experiments?
**Expected Result:** A specific experiment or observation that could confirm or falsify the prediction.
**Method:** Compare your predicted value to the sensitivity of current and planned experiments (LIGO/Virgo/KAGRA, LISA, Einstein Telescope, CMB-S4, tabletop experiments, etc.).
**Pass Criteria:** At least one planned or feasible experiment can reach the sensitivity needed.
**If it fails:** A prediction that requires a Planck-energy accelerator isn't falsifiable in practice. Look for amplification mechanisms, low-energy signatures, or cosmological windows.
**Skip if:** You haven't surveyed the experimental landscape.

---

### Test 4.4: Distinguishability

**Category:** Prediction
**Difficulty:** Advanced
**Prerequisites:** Testable predictions exist (Test 4.3 passes).
**The Test:** Can your theory's predictions be distinguished from those of other quantum gravity approaches?
**Expected Result:** At least one prediction that differs quantitatively from the predictions of LQG, string theory, asymptotic safety, etc.
**Method:** Compare your predictions against published predictions from competing approaches. Identify observables where they disagree.
**Pass Criteria:** At least one distinguishing observable identified.
**If it fails:** Your theory might be a reformulation of an existing approach (which is fine, if it offers new insights). Or you need to find a more discriminating observable.
**Skip if:** You're not at the stage of comparing with other approaches.

---

## Tier 5: Unification Checks

*These are the ultimate tests. Run them only if your theory claims to unify gravity with other forces or explain fundamental questions. Most theories won't reach this tier, and that's okay.*

---

### Test 5.1: Standard Model Gauge Group

**Category:** Unification
**Difficulty:** Advanced
**Prerequisites:** The theory claims to contain or derive matter content.
**The Test:** Can SU(3) x SU(2) x U(1) emerge from your theory?
**Expected Result:** The Standard Model gauge group appears naturally — either as a subgroup of a larger symmetry, or from a geometric/topological mechanism.
**Method:** Identify the gauge symmetries in your theory. Check if SU(3) x SU(2) x U(1) is contained (possibly after symmetry breaking).
**Pass Criteria:** SM gauge group emerges without ad hoc assumptions.
**If it fails:** This is an aspirational goal. Most quantum gravity theories don't achieve this. Note it as an open problem and move on.
**Skip if:** Your theory is only about quantum gravity and doesn't claim to unify with matter.

---

### Test 5.2: Fermion Content

**Category:** Unification
**Difficulty:** Advanced
**Prerequisites:** The theory claims to explain matter.
**The Test:** Can the known fermion spectrum (3 generations of quarks and leptons) emerge?
**Expected Result:** Chiral fermions with the correct quantum numbers appear. Three generations emerge naturally (or at least are accommodated).
**Method:** Identify fermionic degrees of freedom in your theory. Check chirality, gauge representations, and generation structure.
**Pass Criteria:** Chiral fermions with correct SM quantum numbers. Three generations.
**If it fails:** Getting chiral fermions from a gravitational theory is notoriously hard. Note the difficulty and what would be needed.
**Skip if:** Not a unification theory.

---

### Test 5.3: Cosmological Constant

**Category:** Unification
**Difficulty:** Advanced
**Prerequisites:** The theory has a vacuum state with definite energy.
**The Test:** Can your theory explain or constrain the value of the cosmological constant (Lambda ~ 10^-122 in Planck units)?
**Expected Result:** Either: (a) Lambda is derived from the theory, or (b) there's a mechanism that naturally gives a small Lambda, or (c) the theory at least doesn't make it worse (no new fine-tuning).
**Method:** Compute the vacuum energy in your theory. Compare to the observed value.
**Pass Criteria:** Any progress on the CC problem is valuable. Deriving the exact value would be extraordinary.
**If it fails:** You're in good company — nobody has solved this. Note it as open.
**Skip if:** You're not addressing vacuum energy.

---

### Test 5.4: Dark Matter Candidate

**Category:** Unification
**Difficulty:** Intermediate
**Prerequisites:** The theory has matter-like excitations beyond the Standard Model.
**The Test:** Does your theory contain a dark matter candidate?
**Expected Result:** A stable, electrically neutral, weakly-interacting massive particle. Or: a modified gravitational dynamic that reproduces dark matter phenomenology.
**Method:** Identify stable massive states in the spectrum. Check their interactions with SM particles. Or: derive the rotation curve / structure formation predictions.
**Pass Criteria:** A viable DM candidate consistent with Omega_DM ~ 0.27, direct detection bounds, and structure formation.
**If it fails:** Not fatal — many theories of quantum gravity don't address DM. But it's a big win if yours does.
**Skip if:** Not relevant to your theory's scope.

---

### Test 5.5: Hierarchy Problem

**Category:** Unification
**Difficulty:** Advanced
**Prerequisites:** The theory contains the Higgs field or an equivalent mechanism.
**The Test:** Does your theory explain why m_Higgs << M_Planck (the hierarchy problem)?
**Expected Result:** A natural mechanism that protects the Higgs mass from Planck-scale radiative corrections.
**Method:** Compute the radiative corrections to scalar masses in your framework. Check if there's a symmetry or mechanism that keeps them small.
**Pass Criteria:** Higgs mass is naturally light (no fine-tuning of order 10^-30 or worse).
**If it fails:** The hierarchy problem is unsolved. Note what your theory says about it and move on.
**Skip if:** Not relevant to your theory's scope.

---

## Summary Table

| Test | Tier | What It Checks | Difficulty |
|------|------|----------------|------------|
| 1.1 | 1 | Action/partition function exists | Basic |
| 1.2 | 1 | Correct DOF (2 for graviton) | Basic |
| 1.3 | 1 | Gauge symmetry (diffeos) | Basic |
| 1.4 | 1 | Ghost freedom | Intermediate |
| 1.5 | 1 | Unitarity | Intermediate |
| 1.6 | 1 | Dimensional consistency | Basic |
| 2.1 | 2 | Propagator matches GR | Intermediate |
| 2.2 | 2 | Newton's law recovery | Basic |
| 2.3 | 2 | Three-graviton vertex | Advanced |
| 2.4 | 2 | Lorentz invariance | Intermediate |
| 2.5 | 2 | Equivalence principle | Intermediate |
| 2.6 | 2 | Linearized EOM match GR | Basic |
| 3.1 | 3 | Graviton mass bound | Basic |
| 3.2 | 3 | GW speed bound | Intermediate |
| 3.3 | 3 | Lorentz violation parameters | Advanced |
| 3.4 | 3 | Black hole entropy | Advanced |
| 3.5 | 3 | Spectral dimension running | Advanced |
| 3.6 | 3 | Post-Newtonian parameters | Intermediate |
| 4.1 | 4 | Novel prediction exists | Basic |
| 4.2 | 4 | Prediction is quantitative | Intermediate |
| 4.3 | 4 | Prediction is testable | Intermediate |
| 4.4 | 4 | Distinguishable from alternatives | Advanced |
| 5.1 | 5 | SM gauge group emerges | Advanced |
| 5.2 | 5 | Fermion content | Advanced |
| 5.3 | 5 | Cosmological constant | Advanced |
| 5.4 | 5 | Dark matter candidate | Intermediate |
| 5.5 | 5 | Hierarchy problem | Advanced |
