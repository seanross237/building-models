# Agent: Architect | Run: h2-speed-of-light | Date: 2026-03-26

---

## HYPOTHESIS (raw)

"The speed of light isn't a speed limit on matter — it's the rate at which time converts into space. In relativity, space and time trade off. What if c is the exchange rate of a fundamental conversion process? The universe is 'spending' time to 'buy' space, and that's what expansion is."

---

## FRAMEWORK: Temporal-Spatial Conversion (TSC) Model

### Definitions

**D1.** *Minkowski metric* — The spacetime interval ds^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2. The minus sign encodes the fundamental asymmetry between time and space: they contribute to the interval with opposite signs. The constant c is the dimensional conversion factor that makes time and space commensurable (converts seconds to meters).

**D2.** *Four-velocity* — For any massive particle, the four-velocity u^mu = dx^mu / d(tau) satisfies u_mu u^mu = -c^2. This is a constraint, not a dynamical equation: it says that any massive particle's trajectory through spacetime has a fixed "speed through spacetime" of magnitude c.

**D3.** *Proper time* tau — The time measured by a clock co-moving with the object. For an object at rest in some frame, d(tau) = dt. For an object moving at velocity v, d(tau) = dt * sqrt(1 - v^2/c^2). Motion through space "costs" proper time.

**D4.** *Rapidity* phi — The hyperbolic angle parametrizing boosts: v = c tanh(phi). In terms of rapidity, the four-velocity components are u^0 = c cosh(phi), u^i = c sinh(phi) n^i, where n^i is the unit spatial direction. The hyperbolic identity cosh^2(phi) - sinh^2(phi) = 1 encodes the four-velocity constraint.

**D5.** *Hubble flow* — In FLRW cosmology, the metric is ds^2 = -c^2 dt^2 + a(t)^2 [dr^2/(1-kr^2) + r^2 d(Omega)^2], where a(t) is the scale factor. The expansion of space is described by da/dt > 0. Comoving observers (those at rest in the Hubble flow) have four-velocity u^mu = (c, 0, 0, 0) in comoving coordinates — they are "at rest" yet space expands around them.

**D6.** *Conversion process (proposed)* — The claim that c is not merely a unit-conversion constant or a speed limit, but the rate of an active physical process in which "temporal extent" is transformed into "spatial extent."

---

### Premises (Established Physics)

**P1. [Four-velocity constraint]** Every massive particle moves through spacetime with |u| = c. This is a kinematic identity in special relativity. An object at rest moves entirely through time (u = (c, 0, 0, 0)). An object moving at speed v redistributes its spacetime motion: more through space, less through time. The total magnitude is always c.

**P2. [Time dilation]** A moving clock runs slow: d(tau) = dt sqrt(1 - v^2/c^2). The faster you move through space, the slower you move through time. This is not an effect *on* clocks; it is the geometry of spacetime. The relationship is hyperbolic, not linear: as v -> c, d(tau) -> 0.

**P3. [Lightlike limit]** A massless particle (photon) moves at v = c and has d(tau) = 0. It moves entirely through space, not at all through time. Its worldline is null: ds^2 = 0. This is the extreme case of the time-space trade-off: ALL of the "spacetime budget" goes to space, none to time.

**P4. [Cosmological expansion]** The scale factor a(t) of the FLRW universe increases with cosmic time t. Comoving observers measure increasing proper distances between each other. The expansion rate H = (da/dt)/a has units of inverse time (or equivalently, velocity per unit distance: km/s/Mpc).

**P5. [de Sitter limit]** In a universe dominated by a cosmological constant Lambda, the scale factor grows exponentially: a(t) ~ exp(H_Lambda t), where H_Lambda = sqrt(Lambda c^2 / 3). The expansion is driven by vacuum energy, not by the motion of matter through space.

**P6. [Dimensional role of c]** In natural units where c = 1, space and time are measured in the same units. The constant c is, at minimum, the conversion factor between temporal and spatial units. In the Minkowski metric, it appears as the coefficient that makes ct and x commensurable. In Einstein's equations, it appears in G_munu = (8 pi G / c^4) T_munu, setting the scale at which energy curves spacetime.

---

### Derivation Chain

#### Step 1: The four-velocity constraint as a conservation law

**S1.** From P1, every massive particle satisfies u_mu u^mu = -c^2. Decompose this in a given frame:

> c^2 = (u^0)^2 - |u_spatial|^2 = c^2 gamma^2 - v^2 gamma^2 = c^2 gamma^2 (1 - v^2/c^2) = c^2

This is an identity: the "total rate of motion through spacetime" is always c. The distribution between time and space is variable, but the total is conserved.

**S2.** INTERPRETATION: This constraint can be read as a *budget*. Every massive particle has a fixed budget of c units of "spacetime velocity." This budget can be allocated to motion through time (contributing to u^0 = c gamma) or motion through space (contributing to |u_spatial| = v gamma). The allocation is governed by the hyperbolic geometry of Minkowski space: as spatial allocation increases, temporal allocation decreases, but the total invariant magnitude remains c.

**S3.** CLAIM: The TSC hypothesis elevates this budget-reading from a mathematical identity to a physical process. The claim is:

> c is not merely the magnitude of the four-velocity constraint. It is the *rate* of an active conversion process. A particle "at rest" (v = 0) has its entire budget in the time channel: it converts c meters of temporal extent per second of proper time. As it accelerates, some of this conversion is redirected to the spatial channel. The total conversion rate remains c.

#### Step 2: Photons as the fully-converted limit

**S4.** From P3, a photon has d(tau) = 0 and v = c. In the TSC interpretation:

> A photon has converted its ENTIRE temporal budget to spatial budget. It has no proper time — no temporal "motion" — and moves at c entirely through space. This is why c appears as a speed limit: it is the total conversion budget, and you cannot allocate more to space than the total.

**S5.** CLAIM: The "speed limit" interpretation of c is a *consequence* of the conversion-budget interpretation. The reason nothing massive can reach c is not that c is a wall, but that reaching c would require converting the entire temporal budget to spatial, which would require d(tau) = 0, which means the object ceases to experience time. For a massive particle, this requires infinite energy (gamma -> infinity) because the mass itself is a "temporal anchor" — the rest energy mc^2 represents the minimum temporal conversion rate.

#### Step 3: Rest mass as temporal conversion rate

**S6.** From D2, a particle at rest has four-velocity u = (c, 0, 0, 0). Its only "motion" is through time. The rest energy is E_0 = mc^2.

**S7.** CLAIM: In the TSC framework, the rest energy E_0 = mc^2 represents the *energy cost of temporal conversion*. A particle of mass m converts temporal extent at rate c (in its rest frame), and the energy required to sustain this conversion is mc^2. This is why energy and mass are equivalent: mass IS the conversion process, measured in energy units.

**S8.** Supporting observation: The de Broglie/Compton frequency f_C = mc^2 / h is the frequency of a particle's internal phase evolution in its rest frame. A particle at rest is not static — it oscillates at frequency f_C. In the TSC reading, this oscillation IS the temporal conversion process: the particle "ticks" through time at rate f_C, and each tick converts a quantum of temporal extent to maintain the particle's existence in the temporal dimension.

#### Step 4: Cosmological expansion as large-scale conversion

**S9.** From P4, the universe's spatial extent grows with cosmic time. The scale factor a(t) increases. Comoving observers are at rest (v = 0 in comoving coordinates), so their entire four-velocity budget is temporal: u = (c, 0, 0, 0).

**S10.** CLAIM: Cosmological expansion IS the macroscopic expression of the temporal-to-spatial conversion. The universe, as a whole, is "spending" cosmic time to "buy" new spatial extent. The expansion rate H is the macroscopic conversion rate: it describes how quickly cosmic time is being converted into new comoving distance.

**S11.** Connecting to de Sitter: In a Lambda-dominated universe, H -> H_Lambda = sqrt(Lambda c^2 / 3). The conversion rate asymptotes to a constant determined by the vacuum energy. In the TSC interpretation:

> Vacuum energy (Lambda) sets a *minimum temporal-to-spatial conversion rate* for the universe as a whole. Even in the absence of matter, the vacuum converts time into space at rate H_Lambda. This is why the cosmological constant drives exponential expansion: it is an irreducible conversion process inherent to the vacuum.

#### Step 5: The Hubble parameter as the macroscopic exchange rate

**S12.** CLAIM: The Hubble parameter H(t) is the macroscopic temporal-to-spatial exchange rate. Dimensionally, H has units of [1/time] or equivalently [velocity/distance]. The TSC interpretation reads H as: "per unit of cosmic time, a fraction H of each spatial distance is newly created by conversion from the temporal dimension."

**S13.** CLAIM: The relationship between c (the microscopic conversion rate for individual particles) and H (the macroscopic conversion rate for the universe) is analogous to the relationship between molecular speed and bulk thermodynamic flow. Individual particles convert at rate c through the four-velocity budget. The aggregate effect of many particles, plus the vacuum contribution, produces the bulk expansion rate H << c.

---

### Conclusions

**C1.** The speed of light c is the total temporal-spatial conversion budget per unit proper time for any massive particle. The four-velocity constraint |u| = c is the mathematical expression of this fixed budget.

**C2.** The "speed limit" character of c is a *consequence* of the budget being finite: you cannot allocate more to spatial motion than the total budget allows.

**C3.** Rest mass m represents a particle's temporal conversion rate, with mc^2 being the energy cost. A particle at rest is actively "converting" at rate c purely through the temporal channel.

**C4.** Cosmological expansion is the macroscopic expression of temporal-to-spatial conversion. The Hubble parameter H is the bulk conversion rate, related to but much smaller than the per-particle budget c.

---

### Predictions

#### Prediction 1: Expansion rate relates to the total temporal conversion budget

**Statement:** If cosmological expansion is genuinely temporal-to-spatial conversion, then the expansion rate H should be related to the total amount of "temporal budget" being converted to spatial extent. For a universe with matter density rho_m and vacuum energy density rho_Lambda:

> H^2 = (8 pi G / 3) (rho_m + rho_Lambda)

This IS the Friedmann equation. The TSC framework claims it is not merely an equation of motion for a(t), but a *conversion rate equation*: the left side is the square of the conversion rate, and the right side is the total "conversion fuel" (mass-energy density, which in the TSC reading is the density of temporal-conversion processes).

**Novelty concern:** This may be a verbal relabeling of the Friedmann equation, not a prediction.

#### Prediction 2: The fine structure of the time-space trade-off in gravitational fields

**Statement:** In a gravitational field, the metric component g_00 deviates from -c^2: g_00 = -(1 - 2GM/(rc^2)) c^2 (Schwarzschild). In the TSC interpretation, this means the local temporal conversion rate is *modified by gravity*: near a massive body, the "exchange rate" between time and space shifts, making time "cheaper" and space "more expensive." This is gravitational time dilation.

The TSC framework predicts that this modification is continuous and monotonic: as you approach the Schwarzschild radius r_s = 2GM/c^2, the temporal conversion rate goes to zero (from the perspective of a distant observer), corresponding to g_00 -> 0. At the horizon, the conversion fully stalls: the "exchange rate" diverges (infinite space per unit of far-away time).

**Novelty concern:** This is gravitational time dilation restated in conversion language. It may not predict anything beyond GR.

#### Prediction 3: A relationship between cosmic expansion and the vacuum's temporal-conversion rate

**Statement:** If the vacuum itself has an intrinsic temporal-to-spatial conversion rate, this should manifest as a minimum expansion rate that cannot be eliminated even in empty space. The cosmological constant Lambda is this minimum rate (squared, with appropriate dimensional factors):

> H_min^2 = Lambda c^2 / 3

The TSC framework adds an interpretive claim: Lambda is not a mysterious "dark energy" but the vacuum's intrinsic temporal-to-spatial conversion rate. The vacuum "ticks" — it has a de Sitter temperature T_dS = (h H_Lambda) / (2 pi k_B) associated with its horizon — and this ticking is the conversion process.

**Potentially novel element:** If the vacuum's temporal conversion rate is fundamental, then Lambda should be calculable from c and the Planck units:

> Lambda = alpha * l_P^{-2}

where alpha is a dimensionless number. The TSC framework does not determine alpha, but it claims Lambda is not a free parameter — it is set by the vacuum's conversion rate, which should be derivable from quantum gravity.

**Honest concern:** Every framework for quantum gravity claims Lambda should be calculable. This prediction is not specific enough to distinguish TSC from other approaches.

---

### Honesty Check

I flag the following concerns:

1. **S2-S3 (budget interpretation):** The four-velocity constraint |u| = c is a kinematic identity that follows from the definition of proper time. Calling it a "conversion process" adds physical content only if the "conversion" does something the identity does not. I have not identified what that something is.

2. **S5 (mass as temporal anchor):** The claim that "mass is a temporal anchor" is suggestive but not derived. I have not shown why mass should be *identified with* the temporal conversion rate rather than merely *correlated with* it.

3. **S10-S11 (expansion as conversion):** This is the most speculative step. The Friedmann equation describes how a(t) evolves given the energy content. Calling this a "conversion process" requires that something is genuinely being *converted* — that temporal extent is being *consumed* to *produce* spatial extent. I have not identified the mechanism of this consumption, nor have I shown that cosmic time is being "used up" in any measurable sense.

4. **S13 (c and H analogy):** The analogy between c (microscopic) and H (macroscopic) is loose. c is a Lorentz invariant; H is frame-dependent (it depends on the choice of cosmic time). They have different transformation properties, which weakens the analogy.

5. **All predictions:** Every prediction I have offered is either (a) a known result restated in TSC language, or (b) too vague to test. I have not produced a single prediction that distinguishes TSC from standard relativity.
