# Computation Registry

Computations identified during explorations that would significantly advance the mission. Maintained by the strategizer, read by the missionary and future strategizers.

## 1. Phase Freedom = Realm Selection Formal Test (from E002)
**What:** For a qubit (N=2), explicitly construct the space of all Theta matrices consistent with a given Gamma (the three-dimensional phase freedom per Doukas). Then construct the set of all consistent histories families {P_alpha} with D(alpha,alpha')=0 for the same system. Check if the two spaces have the same dimension and structure.
**Why:** Would provide quantitative evidence for the phase freedom = realm selection structural equivalence identified in E002.
**What it resolves:** Whether this connection is a deep mathematical isomorphism or a superficial analogy.
**Source:** Exploration 002, Section 4.4 / Finding 3.
**Difficulty:** Medium — requires explicit matrix construction for N=2. Both spaces should be small enough to enumerate.
**Equations:** Theta satisfies Gamma_ij = |Theta_ij|^2. Decoherence functional D(alpha,alpha') = Tr(K_alpha rho_0 K_{alpha'}^dagger) where K_alpha = P_{alpha_n}...P_{alpha_1}. Consistency: Re[D(alpha,alpha')] = 0 for alpha != alpha'.

## 2. Indivisibility Measure on Concrete Systems (from E001/E002)
**What:** For standard quantum systems (qubit under various Hamiltonians, 2-qubit entangled states), compute the degree of indivisibility — quantify how far the transition kernel Gamma is from satisfying Chapman-Kolmogorov at intermediate times.
**Why:** Would test whether indivisibility provides a useful quantitative diagnostic for quantum behavior.
**What it resolves:** Whether indivisibility is a binary on/off property or a continuous measure with physical meaning.
**Source:** Exploration 001 (definition of ISP) + Exploration 002 (Level 2 classification).
**Difficulty:** Medium — requires constructing Gamma from known quantum evolution and testing composition at various intermediate times.
**Equations:** Test: ||Gamma(t<-s) - Gamma(t<-r)Gamma(r<-s)||_1 for various r between s and t.

## 1b. UPDATE: Computation 1 COMPLETED (E003a)
**Result:** Dimensions match at N=2 (both = 2) but topologies differ (T² vs S²). Match breaks at N>2 (phase freedom grows sub-quadratically, realm selection grows as N(N-1)). Hypothesis partially refuted. Coincidental match. See E003a REPORT.md for full details.

## 3. Tsirelson Bound Derivation Assumption Audit (from E004)
**What:** Trace the exact steps of Barandes/Hasan/Kagan arXiv:2512.18105 and identify at what point complex amplitudes Theta are assumed vs. derived from ISP axioms.
**Why:** The CHSH/Tsirelson characterization is the strongest structural claim in the entire Barandes program. If Theta is assumed (not derived from ISP axioms), the argument is partially circular.
**What it resolves:** Whether causal local ISP → Tsirelson is a genuinely new derivation or standard QM in stochastic dress.
**Source:** Exploration 004, Section 1.5 and Leads #2.
**Difficulty:** Low — careful reading of one paper's proof structure.
**Equations:** The key step: does causal locality + ISP axioms → Theta must be a unitary matrix? Or is Theta assumed unitary from the start?

## 4. Real-vs-Complex Tension in ISP for N=2 (from E004)
**What:** Barandes (2602.01043) claims real orthogonal matrices suffice for N=2. Renou et al. (2021, arXiv:2101.10870) showed real QM fails entanglement tests experimentally. Do these results clash?
**Why:** If ISP says N=2 needs no complex numbers, but experiments show real QM fails for entangled qubits, there may be a tension or a scope clarification needed.
**What it resolves:** Whether the "complex numbers from indivisibility" derivation is consistent with experimental evidence.
**Source:** Exploration 004, Lead #3.
**Difficulty:** Low — conceptual analysis, likely resolved by noting Renou involves entangled (multi-qubit) systems while Barandes' N=2 claim is single-system.
