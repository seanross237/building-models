# EPG Graviton Scrutiny: Can a Spin-2 Massless Particle Emerge from Entanglement Transitions?

**Iteration 14 — Verification Mode**
**Date:** 2026-03-20
**Subject:** Does EPG have a concrete mechanism for producing a spin-2 massless graviton?

---

## Executive Summary

**EPG does NOT have a concrete graviton mechanism.** None of the three candidate mechanisms (mutual information as metric, random tensor network perturbations, replica field theory) has a published calculation that derives a spin-2 massless propagator from entanglement transition physics. The best results come from the AdS/CFT program (Faulkner et al. 2014, Lashkari et al. 2014), which derives linearized Einstein equations from entanglement first law — but these are AdS/CFT results that ASSUME holographic duality, not independent derivations from MIPT physics. EPG's path from "entanglement phase transition" to "graviton" remains: entanglement -> (hand-wave) -> geometry -> (invoke AdS/CFT) -> gravitons. There is no calculation analogous to FDCG's concrete rank-2 gauge theory -> Goldstone boson mechanism.

**The scalar-to-tensor problem is real and unresolved.** The MIPT order parameter (entanglement entropy) is a scalar. Getting spin-2 from a scalar requires either (a) the order parameter is secretly a tensor (but it isn't — S(A) is a number for each region A), or (b) there's a collective/geometric mechanism that promotes scalar fluctuations to tensor fluctuations (possible but undemonstrated), or (c) one invokes holographic duality as an axiom rather than deriving it.

**Comparison with FDCG:** FDCG has a concrete mechanism — the rank-2 symmetric tensor gauge field A_ij has spin-2 built into its fundamental degrees of freedom. The graviton IS the Goldstone boson of broken dipole symmetry, with the tensor structure inherited from the rank-2 gauge field. EPG has no comparable mechanism.

---

## The Core Problem: Scalar Order Parameter, Tensor Fluctuations

### The MIPT Order Parameter

In an MIPT, the order parameter is the scaling of entanglement entropy:
- **Volume-law phase:** S(A) ~ |A| (entropy scales with volume of region)
- **Area-law phase:** S(A) ~ |dA| (entropy scales with boundary area)

The transition is between these two scaling behaviors. The natural order parameter is something like:

**phi = lim_{|A|->inf} S(A)/|A|**

This is a SCALAR. It's a single number characterizing the entanglement scaling of the state. Near the critical point, phi -> 0 from the volume-law side, and the transition occurs at phi = 0.

### Why Scalar -> Spin-2 Is Hard

In standard Landau-Ginzburg theory, fluctuations of a scalar order parameter are scalar (spin-0). The propagator of phi fluctuations is:

**G(k) = 1/(k^2 + m^2)**

This is a spin-0 propagator. To get a spin-2 propagator (the graviton), you need:

**G_{ijkl}(k) = (P^TT)_{ijkl} / k^2**

where P^TT is the transverse-traceless projector. This has a completely different tensor structure.

**There is no known mechanism in Landau-Ginzburg theory that promotes a scalar order parameter to a rank-2 tensor fluctuation.** The tensor structure must come from somewhere.

### Three Candidate Mechanisms

---

## Mechanism 1: The Metric IS the Entanglement Structure

### The Claim
Following Van Raamsdonk (2010), the mutual information I(A:B) between spatial regions A and B determines the geodesic distance between them. If so, the COLLECTION of mutual informations {I(A:B)} for all pairs of regions defines a metric. Fluctuations of this collection are metric fluctuations, which have spin-2.

### What Van Raamsdonk Actually Showed

Van Raamsdonk (2010) argued that:
1. In AdS/CFT, reducing entanglement between two CFT subsystems causes the dual bulk geometry to pinch off
2. Disentangling degrees of freedom makes spacetime regions "pull apart"
3. Therefore entanglement is the "glue" of spacetime

**This is a qualitative argument within AdS/CFT.** It does NOT:
- Derive a metric from entanglement data without assuming AdS/CFT
- Show that mutual information fluctuations have spin-2 character
- Produce a graviton propagator
- Work outside the holographic setting

### The Cao-Carroll Program (2016-2018)

Cao, Carroll, and Chatwin-Davies (arXiv:1606.08444, 1712.02803) attempted to go further:
1. Start with a factorized Hilbert space H = tensor product of H_a
2. Define distances from mutual information: d(a,b) ~ 1/I(a:b)
3. Use Radon transforms to construct a spatial metric from entanglement data
4. Argue that entanglement equilibrium -> linearized Einstein equations

**What they actually achieved:**
- Showed that GIVEN a state with the right entanglement structure, you CAN define a metric via Radon transform
- Argued (not derived) that time evolution consistent with entanglement equilibrium implies linearized Einstein equations

**What they did NOT achieve:**
- They did not show the resulting metric fluctuations have spin-2
- They did not compute a graviton propagator
- The Radon transform reconstruction ASSUMES the entanglement data has the right structure to define a smooth metric — this is circular if your question is "why does geometry emerge?"
- The argument requires "entanglement equilibrium" which is itself an assumption equivalent to Einstein's equations

### The Faulkner-Lashkari-Van Raamsdonk Result (2014)

The strongest result in this direction:

Faulkner et al. (arXiv:1312.7856) and Lashkari et al. (arXiv:1308.3716) showed:
- In a holographic CFT, the entanglement first law (delta_S = delta_<H_mod>) for all ball-shaped regions is EQUIVALENT to the linearized Einstein equations in the bulk
- This is an EXACT mathematical equivalence within AdS/CFT

**This IS a derivation of linearized gravity (including spin-2) from entanglement.** But:

1. **It requires AdS/CFT as input.** The Ryu-Takayanagi formula S = Area/4G is assumed, not derived. Without RT, you can't convert entanglement entropy statements into geometric statements.

2. **It works in the bulk of AdS, not on a lattice or in an MIPT.** The entanglement first law is a statement about the CFT vacuum and small perturbations thereof — not about a phase transition.

3. **The spin-2 nature comes from the bulk metric, which is assumed to exist.** The argument goes: entanglement first law -> constraints on bulk metric -> these constraints ARE the linearized Einstein equations. The metric (and its spin-2 character) is put in by hand via RT.

4. **There is no MIPT anywhere in this construction.** The entanglement structure is that of a CFT ground state, not a state near an entanglement phase transition.

### Verdict on Mechanism 1

**The mutual information -> metric -> spin-2 chain EXISTS but is NOT an EPG result.** It's an AdS/CFT result that assumes holographic duality. EPG claims that the MIPT IS the mechanism that creates the holographic duality, but this claim has no supporting calculation. The logical chain is:

EPG claims: MIPT -> holographic duality -> geometry -> graviton
What's demonstrated: holographic duality (assumed) -> entanglement first law -> linearized Einstein equations

**The gap between "MIPT" and "holographic duality" is precisely the gap EPG needs to fill, and it hasn't.**

---

## Mechanism 2: Random Tensor Network Graviton

### The Claim
In random tensor networks (RTN), the network geometry discretizes a holographic bulk spacetime. Perturbations of the network (changing tensors, connectivity) correspond to bulk metric perturbations. In the continuum limit, these should include a massless spin-2 mode.

### What Hayden-Nezami-Qi-Swingle (2016) Showed

Hayden et al. (arXiv:1601.01694) showed:
1. Random tensor networks with large bond dimension satisfy the Ryu-Takayanagi formula
2. The entanglement entropy of boundary regions obeys RT for both connected and disconnected regions
3. The network has properties analogous to AdS/CFT: bulk reconstruction, error correction, etc.

**What they did NOT show:**
- They did not compute the spectrum of bulk fluctuations
- They did not derive a graviton propagator
- They did not show that perturbations of the network have spin-2 character
- They did not take a continuum limit

### The "Emergent Holographic Forces" Result (2025)

A recent result (Phys. Rev. X 15, 021078, 2025) showed:
- Optimized tensor networks furnish excitations with attractive interactions
- One- and two-particle energies match predictions for matter coupled to AdS gravity at long distances
- Key features of AdS physics emerge naturally

**This is promising but does NOT constitute a graviton derivation.** The paper shows emergent attractive forces resembling gravity, but does not isolate a massless spin-2 mode or compute its propagator.

### The Fundamental Problem with RTN Perturbation Theory

To derive a graviton from a random tensor network, you would need to:

1. Define a "background" tensor network (the vacuum geometry)
2. Classify perturbations of the network (changing individual tensors, adding/removing nodes, changing connectivity)
3. Show that these perturbations decompose into irreducible representations of the network's symmetry group
4. Identify a spin-2 sector among these perturbations
5. Show this sector is massless (gapless) and has the right propagator

**Nobody has done steps 2-5.** The main obstacle: tensor network perturbation theory is not well-developed. Unlike field theory where we expand around a classical solution, there's no standard framework for expanding around a "background tensor network."

The closest attempt is the work on "discrete gravity on random tensor networks" (Qi-Yang, JHEP 2017), which showed that RTN path integrals can be mapped to discrete gravity partition functions. But this is a formal mapping, not a derivation of a graviton propagator.

### Verdict on Mechanism 2

**No published calculation derives a spin-2 mode from random tensor network perturbations.** The RTN -> holography connection is established (Hayden et al. 2016), but the step from "holographic-like properties" to "graviton propagator" has not been taken. This is an open problem in the tensor network / holography community, not a solved one.

---

## Mechanism 3: The Replica Field Theory Produces Gravity

### The Claim
The MIPT replica trick maps the problem to a statistical mechanics model. If this stat mech model is in the same universality class as random geometry (like CDT or 2D quantum gravity), then gravitational physics emerges.

### What the MIPT Replica Theory Actually Is

The MIPT replica field theory, as developed by Jian-You-Vasseur-Ludwig (arXiv:1908.08051) and extended by subsequent work (arXiv:2302.12820, 2303.07848), maps the MIPT to:

1. **For random Haar circuits:** An effective spin model on the replica space, with permutation symmetry S_n (for n replicas). The volume-law phase corresponds to the "paramagnetic" phase, the area-law phase to the "ordered" phase.

2. **For free fermions:** A nonlinear sigma model (NLSM) on an orthogonal matrix target space O(n) in the replica limit n -> 0.

3. **For general monitored systems:** The effective field theory is a variant of the NLSM with large replica symmetry, depending on the symmetry class of the underlying dynamics.

### Does This Produce Gravity?

**No.** The MIPT replica field theories are:
- NLSMs on internal symmetry groups (permutation groups, orthogonal groups)
- The target space is a group manifold or coset space, NOT spacetime
- The fluctuations are in the replica/symmetry space, NOT in a geometric/gravitational sector
- There is no metric, no curvature, no Einstein equation anywhere in these field theories

The MIPT replica field theory is structurally similar to the replica field theories used in disordered systems (Anderson localization, spin glasses). These are well-understood and have NOTHING to do with gravity.

### Could There Be a Hidden Connection?

A speculative connection: in 2D, some NLSM target spaces can be related to 2D quantum gravity via matrix models. For example:
- The Gross-Witten-Wadia model (unitary matrix integral) is equivalent to 2D Yang-Mills and has connections to 2D gravity
- Random matrix theory (which appears in MIPT through the stat mech model) has connections to 2D gravity via topological recursion

But these connections are specific to 2D and to matrix models, not to general MIPT field theories. In dimensions > 2, there is no known connection between NLSM replica field theories and gravitational physics.

### Verdict on Mechanism 3

**The MIPT replica field theory has no connection to gravity in any published work.** The field theory describes entanglement dynamics in replica space, not gravitational dynamics in physical space. The speculative 2D connections via matrix models are extremely remote and would not produce a spin-2 graviton in 3+1 dimensions.

---

## The Real Question: Where Does Spin-2 Come From?

### The Information-to-Geometry Pipeline

EPG's implicit argument is a two-step pipeline:

**Step 1:** Entanglement structure -> geometry (via MIPT + some version of "geometry = entanglement")
**Step 2:** Geometry -> graviton (standard: fluctuations of a metric are spin-2)

Step 2 is trivially correct — IF you have a metric, its fluctuations include a spin-2 mode. The entire burden falls on Step 1.

### Why Step 1 Fails for Spin-2

Step 1 requires showing that the entanglement structure near the MIPT critical point defines a METRIC — not just a scalar, not just a distance function, but a full rank-2 symmetric tensor field g_ij(x).

The problem: entanglement entropy S(A) defines a function on REGIONS, not on POINTS. To get a metric, you need either:

**(a) Inverse Radon transform (Cao-Carroll approach):** Given S(A) for all regions A, reconstruct g_ij(x) at each point. This requires:
- S(A) to be a smooth function of the region shape and position
- The region-to-entropy map to be invertible
- The resulting g_ij to satisfy Einstein's equations
All three are ASSUMPTIONS, not derivations.

**(b) Mutual information as distance (Van Raamsdonk approach):** I(A:B) -> d(A,B) -> g_ij. This requires:
- I(A:B) to define a metric (triangle inequality, etc.)
- The resulting metric to be smooth and differentiable
- Again, these are assumptions

**(c) Direct construction (EPG would need this):** Show that the MIPT order parameter, when restricted to the area-law phase, naturally factorizes into a tensor g_ij. This would require:
- The area-law S(A) ~ |dA| to encode g_ij via S(A) = integral over dA of sqrt(g)
- The critical fluctuations of this encoding to have rank-2 structure
- A calculation demonstrating this

**Nobody has done (c).** This is what EPG would need to claim a concrete graviton mechanism.

### The Fundamental Obstacle

Here's why (c) is so hard: even in the area-law phase, S(A) ~ integral sqrt(g) d(area) determines g_ij only up to diffeomorphisms (any metric with the same area elements gives the same entropy). But diffeo-equivalence IS the gauge symmetry of gravity. So in principle, the entanglement entropy contains exactly the right information — modulo diffeomorphisms — to specify a metric.

The question is whether the DYNAMICS of the entanglement (near the MIPT) naturally produce Einstein's equations for this metric. The Faulkner et al. result says YES, but only within AdS/CFT. Outside of AdS/CFT, this remains completely open.

---

## Comparison with FDCG

### FDCG's Graviton Mechanism (Concrete)

1. **Start:** Rank-2 symmetric tensor gauge field A_ij on a lattice
2. **Gauge symmetry:** A_ij -> A_ij + d_i d_j alpha (fracton gauge invariance)
3. **Matter:** Fracton dipoles P_i = phi* d_i phi
4. **Condensation:** Dipoles condense, <P_i> != 0
5. **Goldstone theorem:** Broken dipole symmetry has 3 generators -> 3 Goldstone bosons pi_i
6. **Metric:** h_ij = d_i pi_j + d_j pi_i (automatically symmetric rank-2 tensor)
7. **Gauge redundancy:** Removes longitudinal modes, leaving 2 transverse-traceless polarizations = spin-2 graviton
8. **Propagator:** G_{ijkl}(k) = P^TT_{ijkl} / k^2 (massless spin-2, matching linearized GR)

**Every step is a calculation.** The spin-2 nature comes from the rank-2 gauge field, which is there from the beginning. The graviton is the Goldstone boson of a symmetry-breaking process, with the tensor structure inherited algebraically.

### EPG's Graviton Mechanism (Schematic)

1. **Start:** Random quantum circuit with tunable measurement rate
2. **Phase transition:** Volume-law -> area-law entanglement (MIPT)
3. **???:** The area-law phase "is" classical spacetime
4. **???:** Entanglement fluctuations near criticality "are" metric fluctuations
5. **???:** These have spin-2 because "the metric has spin-2"
6. **No propagator computed**

Steps 3-5 are all hand-waving. The spin-2 nature is asserted, not derived.

### The Comparison Is Devastating

| Feature | FDCG | EPG |
|---------|------|-----|
| Partition function Z | YES (tensor gauge theory) | NO |
| Order parameter tensor structure | Rank-2 from A_ij | Scalar (S(A)) |
| Goldstone/fluctuation mechanism | Explicit (broken dipole symmetry) | None |
| Spin-2 derivation | Algebraic (h_ij = d_i pi_j + d_j pi_i) | Assumed |
| Propagator | Computed (conditional on g2=0) | Not computed |
| Gauge redundancy -> 2 polarizations | Demonstrated | Not addressed |
| Einstein equations | Hydrodynamic limit (nonlinear gap exists) | Not derived |

---

## What Would a Graviton Propagator Look Like in EPG?

### The EPG "Theorist" Sub-Agent's Claim (Iteration 2)

From the THEORIES.md entry: "1/k^2 entanglement fluctuation propagator must match graviton propagator (sharp falsifiable test)"

This refers to the idea that the replica field theory of entanglement fluctuations near the MIPT critical point should have a 1/k^2 propagator, and this should match the graviton propagator.

### Why This Is Wrong (Or At Least Wildly Incomplete)

1. **A 1/k^2 propagator is SCALAR.** The graviton propagator is 1/k^2 times a TENSOR structure (P^TT projector). Having 1/k^2 alone only means you have a massless field — it could be any spin.

2. **The replica field theory produces NLSM fluctuations**, which are matrix-valued (in replica space), not tensor-valued (in physical space). Even if you get 1/k^2, the fluctuations are in the WRONG space.

3. **To get a graviton propagator from EPG, you would need to:**
   - Define a metric operator M_ij(x) in terms of entanglement data
   - Compute <M_ij(x) M_kl(y)> near the MIPT critical point
   - Show this equals (P^TT)_{ijkl} / |x-y|^{d-2} (Fourier transform of 1/k^2)
   - Show the tensor structure is transverse-traceless

   Nobody has done ANY of these steps.

### A Speculative EPG Propagator

IF EPG were to succeed, the graviton propagator would presumably come from:

**<delta S(A_x) delta S(A_y)>_critical**

where A_x and A_y are small ball-shaped regions centered at x and y, and the expectation is over the MIPT critical ensemble.

But S(A) is a scalar, so <delta S(A_x) delta S(A_y)> is a scalar 2-point function. To get a tensor, you'd need to consider how S(A) varies with the SHAPE of A, not just its position:

**G_ij,kl(x,y) = d^2/d(epsilon_ij) d(epsilon_kl) <delta S(A_x(epsilon)) delta S(A_y(epsilon'))>|_{epsilon=epsilon'=0}**

where epsilon_ij is a small deformation of the region shape. This is essentially the "shape derivative" of the entanglement entropy, and it IS a rank-2 tensor by construction.

**This is actually a reasonable approach.** The "entanglement metric" could be defined as the second shape derivative of the entanglement entropy. In holographic CFTs, this DOES reproduce the bulk metric (this is essentially the Faulkner et al. result in different language).

**But nobody has computed this at an MIPT critical point.** The entire question is whether the MIPT critical fluctuations of this shape-dependent entanglement entropy have the right properties (massless, 2 polarizations, correct coupling).

---

## Assessment: Is There a Published Calculation?

### For Each Mechanism:

| Mechanism | Published Calculation? | Produces Spin-2? | Specific to EPG/MIPT? |
|-----------|----------------------|-------------------|----------------------|
| 1. Mutual info as metric | Cao-Carroll (2016-2018): reconstruction possible IF structure is right. Faulkner et al. (2014): linearized Einstein from entanglement first law | YES (within AdS/CFT) | NO (requires holographic duality) |
| 2. Random tensor network | Hayden et al. (2016): RTN reproduces RT formula. No graviton calculation. | NOT SHOWN | NO (no perturbation spectrum computed) |
| 3. Replica field theory | Jian-You-Vasseur-Ludwig (2019+): NLSM in replica space | NO (wrong space) | NO (NLSM is not gravity) |

### The Honest Answer

**EPG does not have a concrete graviton mechanism.**

The closest thing to a graviton derivation from entanglement is the Faulkner et al. (2014) result, which derives linearized Einstein equations from the entanglement first law within holographic CFTs. This IS spin-2 and IS rigorous, but:

1. It requires holographic duality (AdS/CFT) as input
2. It operates in the CFT ground state, not at an MIPT
3. It doesn't show that the MIPT is the mechanism creating the holographic duality

EPG's unique contribution would be showing that the MIPT itself creates the conditions for holographic duality (and hence for spin-2 gravitons). This is the gap, and it is ENORMOUS.

---

## What This Means for EPG's Score

### The "Write Z" Demand

EPG cannot write Z. The partition function of the MIPT is:

**Z_MIPT = Tr over measurement outcomes [ product of unitaries and projectors ]**

This is a well-defined object in quantum information theory, but:
- It's a partition function for entanglement dynamics, not for gravity
- The replica version (Z^n averaged over measurement outcomes) maps to a spin model or NLSM, neither of which is a gravitational theory
- There is no path from Z_MIPT to Z_gravity without additional (unjustified) steps

### The "Compute a Propagator" Demand

EPG cannot compute a graviton propagator. The 1/k^2 entanglement fluctuation propagator mentioned in the sub-agent analysis is:
- Scalar, not tensor
- In replica space, not physical space
- Not demonstrated to have any connection to the graviton propagator

### The "Derive Einstein's Equations" Demand

EPG claims that "Einstein's equations emerge as RG flow equations for this phase transition." This is:
- An analogy, not a derivation
- RG flow equations (beta functions) are scalar equations for coupling constants, not tensor equations for a metric
- The actual MIPT RG flow (which IS computed) describes how entanglement entropy transitions between area-law and volume-law, not how a metric satisfies Einstein's equations

---

## Revised EPG Assessment

### What Survives:
1. **The conceptual insight** that entanglement structure and geometry are related (supported by Van Raamsdonk, Faulkner et al., Cao-Carroll)
2. **The MIPT as a model for geometrogenesis** (the area-law phase DOES resemble classical geometry in that it satisfies an area law, matching Ryu-Takayanagi)
3. **The universality argument** (if geometry = entanglement, then the universality of gravity follows from the universality of entanglement phase transitions)
4. **Testable predictions** about fractal dimension at the MIPT critical point (though ~2.5D may conflict with CDT's ~2.0D)
5. **Near-term experimental pathway** (quantum computing experiments)

### What Fails:
1. **No graviton mechanism** — the scalar-to-tensor problem is unresolved
2. **No partition function** — Z_MIPT is not Z_gravity
3. **No propagator** — the 1/k^2 claim is scalar, not tensor
4. **No Einstein equations derivation** — the RG flow analogy is not a derivation
5. **Relies on AdS/CFT** for the only rigorous entanglement -> gravity results
6. **The MIPT is a transition in entanglement ENTROPY (scalar)** — the tensor structure of gravity must come from somewhere, and EPG doesn't say where
7. **No nonlinear gravity** — even the best holographic results (Faulkner et al.) only get linearized equations; nonlinear extensions (arXiv:1705.03026) exist but still within AdS/CFT

### Proposed Score Revision: 7.2 -> 5.5

| Criterion | Before | After | Reason |
|-----------|--------|-------|--------|
| Novelty | 7 | 6 | Still novel framing, but "entanglement = geometry" is now mainstream (Van Raamsdonk, AdS/CFT community) |
| Internal Consistency | 6 | 4 | Scalar order parameter cannot produce spin-2 without additional mechanism. Gap is structural. |
| Testability | 7 | 6 | Quantum computing experiments still feasible, but what exactly would they test? |
| Elegance | 8 | 6 | Beautiful idea, but "beautiful idea without calculations" is not physics |
| Survivability | 6 | 3 | The spin-2 problem is the same severity as DQCP's "weakly first-order" problem |
| Connection Potential | 9 | 8 | Still connects to many fertile areas (MIPT, QEC, tensor networks, holography) |

**Average: 5.5**

### The Shape-Derivative Path Forward

The ONE speculative path that could save EPG is the shape-derivative approach:
- Define the "entanglement metric" as d^2 S(A)/d(shape)^2
- Compute this at the MIPT critical point
- Show it has the right tensor structure and dynamics

This is a CONCRETE calculation that could be done (at least numerically in a (1+1)D MIPT model). If the shape-dependent entanglement entropy fluctuations at the MIPT critical point have spin-2 character, EPG lives. If they don't, EPG is dead.

**This should be the next step if anyone wants to pursue EPG.**

---

## References

- Van Raamsdonk, M. "Building up spacetime with quantum entanglement" Gen. Rel. Grav. 42, 2323 (2010) [arXiv:1005.3035]
- Swingle, B. "Entanglement Renormalization and Holography" Phys. Rev. D 86, 065007 (2012) [arXiv:0905.1317]
- Qi, X.-L. "Exact holographic mapping and emergent space-time geometry" (2013) [arXiv:1309.6282]
- Faulkner, T. et al. "Gravitation from Entanglement in Holographic CFTs" JHEP 03, 051 (2014) [arXiv:1312.7856]
- Lashkari, N. et al. "Gravitational dynamics from entanglement 'thermodynamics'" JHEP 04, 195 (2014) [arXiv:1308.3716]
- Hayden, P. et al. "Holographic duality from random tensor networks" JHEP 11, 009 (2016) [arXiv:1601.01694]
- Cao, C. and Carroll, S.M. "Bulk Entanglement Gravity without a Boundary" Phys. Rev. D 97, 086003 (2018) [arXiv:1712.02803]
- Cao, C. et al. "Space from Hilbert Space: Recovering Geometry from Bulk Entanglement" (2016) [arXiv:1606.08444]
- Jian, C.-M. et al. "Measurement-induced criticality in random quantum circuits" Phys. Rev. B 101, 104302 (2020) [arXiv:1908.08051]
- Jian, C.-M. et al. "Nonlinear sigma models for monitored dynamics of free fermions" Phys. Rev. X 13, 041045 (2023) [arXiv:2302.12820]
- Faulkner, T. et al. "Quantum corrections to holographic entanglement entropy" JHEP 11, 074 (2013) [arXiv:1307.2892]
- "Emergent Holographic Forces from Tensor Networks and Criticality" Phys. Rev. X 15, 021078 (2025)
- Pretko, M. "Emergent gravity of fractons: Mach's principle revisited" Phys. Rev. D 96, 024051 (2017) [arXiv:1702.07613]
- Afxonidis et al. "Canonical analysis of fracton gravity" (2024) [arXiv:2406.19268]
