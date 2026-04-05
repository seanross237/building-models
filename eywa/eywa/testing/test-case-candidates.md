# Eywa Test Case Candidates

Test cases for scoring Eywa runs. Every case has an objectively verifiable answer. Runs are also scored on token usage and wall-clock time.

---

## Tier A: Atlas-Derived (Deep Decomposition)

Novel findings from Atlas missions, posed as questions where the discovery is the ground truth. These originally took multi-hour, multi-exploration runs to solve.

### A1. Compton-Unruh Resonance Falsification
- **Question:** Does a particle's Compton frequency resonate with Unruh radiation at cosmological acceleration a ~ cH_0?
- **Correct Answer:** No. Matching acceleration a* ~ 2.69x10^33 m/s^2 is 43 orders of magnitude above cH_0. Boltzmann suppression: exp(-10^42).
- **Scoring:** Binary (correctly dismisses as impossible + identifies dimensional gap)
- **Domain:** Physics / dimensional analysis
- **Source:** Atlas Compton-Unruh mission (8 explorations)

### A2. Unruh-de Sitter Temperature Ratio = MOND Interpolation
- **Question:** What is the ratio T_U(a)/T_dS(a) of flat-space Unruh temperature to de Sitter-modified Unruh temperature?
- **Correct Answer:** T_U(a)/T_dS(a) = a/sqrt(a^2 + c^2*H_0^2) = mu_MOND(x), x = a/cH_0. Reproduces galaxy rotation curves (NGC 3198: chi^2/dof = 1.21, NGC 2403: chi^2/dof = 0.52).
- **Scoring:** Exact algebraic identity match + numerical fit verification
- **Domain:** Physics / gravity / galactic dynamics
- **Source:** Atlas Compton-Unruh mission

### A3. Black Hole Classicality Constants
- **Question:** What are the universal dimensionless constants governing single-photon Hawking radiation classicality?
- **Correct Answer:** Three constants: S_Hawking = 1/(540 ln 2) ~ 0.00267 bits; <N_photons> = zeta(3)/(24*pi^4) ~ 5.14x10^-4; R_1bit = 7.21 r_s
- **Scoring:** Exact numerical match on 3 values
- **Domain:** Physics / black hole thermodynamics
- **Source:** Atlas Classicality Budget mission

### A4. Ghost-Free Theories Cannot Reach d_s = 2
- **Question:** Can ghost-free, Lorentz-invariant theories produce spectral dimension d_s = 2 in the UV?
- **Correct Answer:** No. Proof via Hadamard's factorization theorem + Kallen-Lehmann spectral representation. All ghost-free nonlocal theories give d_s -> 0, not 2.
- **Scoring:** Binary (correct conclusion) + proof structure verification
- **Domain:** Physics / quantum gravity
- **Source:** Atlas Quantum Gravity mission (25 explorations)

### A5. Vasseur Pressure Exponent Sharpness
- **Question:** Can the De Giorgi recurrence exponent beta = 4/3 be improved for 3D Navier-Stokes?
- **Correct Answer:** No. All four De Giorgi chain steps are individually tight. Constant field u(x) = (c, 0, 0) is a one-line extremizer proof.
- **Scoring:** Binary (correct conclusion) + extremizer construction + identification that all 8 alternative routes are blocked
- **Domain:** Mathematics / PDE regularity
- **Source:** Atlas Vasseur Pressure mission

### A6. Universal De Giorgi Exponent Formula
- **Question:** What is the De Giorgi exponent for dissipative PDEs with varying diffusion order s in dimension n?
- **Correct Answer:** beta = 1 + s/n. De Giorgi proves regularity only when beta >= 3/2, requiring s/n >= 1/2.
- **Scoring:** Exact formula match + verification across 6+ PDEs (3D NS, 2D NS, 1D Burgers, SQG, MHD, fractional NS)
- **Domain:** Mathematics / PDE regularity
- **Source:** Atlas Vasseur Pressure mission

### A7. QD-HQEC Mapping
- **Question:** Is there a formal relationship between quantum Darwinism and holographic quantum error correction?
- **Correct Answer:** Formal isomorphism: System <-> bulk operator; environment fragment <-> boundary subregion; "fragment knows system" <-> entanglement wedge reconstruction. Zero cross-citations between communities across 20+ years.
- **Scoring:** Mapping correctness (3 correspondences) + citation gap discovery
- **Domain:** Physics / quantum information
- **Source:** Atlas Classicality Budget mission

### A8. Thermal Time Hypothesis Fails for Excited States
- **Question:** Does modular flow generate correct time evolution for excited quantum states?
- **Correct Answer:** No. For excited states, modular flow oscillates at entanglement-spectrum frequencies (not physical Hamiltonian frequencies). Discrepancy grows as N^{0.33-0.44} in continuum limit. Modular flow generates evolution under the Hamiltonian that prepared the state, not the current one.
- **Scoring:** Binary (correct conclusion) + scaling law identification + preparation-history interpretation
- **Domain:** Physics / quantum foundations
- **Source:** Atlas Thermal Time mission

### A9. Yang-Mills Mass Gap Proof Has Irreparable Gap
- **Question:** Is beta < 1/6 the correct mass gap threshold for lattice Yang-Mills, and does the B^2 formula proof hold?
- **Correct Answer:** Threshold is numerically correct, but proof via B^2 formula is irreparably broken (lambda_max(H_actual) > lambda_max(H_formula) for one-hot perturbations by up to 2.6%). Triangle inequality on M(Q) itself is proven; direct Hessian path is viable but untested.
- **Scoring:** Identifies proof gap + provides alternative route or derives correct threshold
- **Domain:** Mathematics / gauge theory
- **Source:** Atlas Yang-Mills Validation mission

### A10. Riemann Hypothesis Super-Rigidity Gap
- **Question:** Can a Hermitian matrix eigenvalue spectrum match the Riemann zeta zeros' 47% super-rigidity (Delta_3_sat = 0.155)?
- **Correct Answer:** No. Best construction achieves Delta_3_sat = 0.24. GUE statistics are easy (any matrix does it), but super-rigidity requires prime-orbit structure no matrix encodes.
- **Scoring:** Binary (correct conclusion) + identification of quantitative gap (0.155 vs 0.24)
- **Domain:** Mathematics / spectral theory
- **Source:** Atlas Riemann Hypothesis mission

---

## Tier B: Architecture-Experiment-Derived (Discriminating Questions)

Questions from BBEH/HLE benchmarks where architecture choice determined correctness. These are faster to run but clearly separate good from bad orchestration.

### B1. Constraint-First Planning (Ceramic Sintering)
- **Question:** Which effect is unlikely to arise from coarsening gas evolution during ceramic sintering? (6 options: A-F)
- **Correct Answer:** C — Large, randomly distributed voids
- **Scoring:** Exact match (single letter)
- **Domain:** Materials science
- **Discrimination:** M2 constraint-first got 2/2; all other approaches got 0/15
- **Source:** Architecture Exp, SCI-10

### B2. Sign-Sensitive Derivation (Exciton Rydberg Energy)
- **Question:** Band gap 3eV, screened Coulomb, 1s exciton peak at 1eV. What is Rydberg energy for n=3?
- **Correct Answer:** -0.08 eV
- **Scoring:** Exact numerical match (sign matters)
- **Domain:** Physics / condensed matter
- **Discrimination:** Both Sonnet and Opus got positive values; only sign-explicit prompting fixed it
- **Source:** Architecture Exp, SCI-03

### B3. Ambiguity Detection (Pronoun Disambiguation)
- **Question:** "The investigator wanted to interview the witness in person but he was too late. On his way, he got stuck in traffic." Which option correctly explains the pronoun antecedent? (5 options)
- **Correct Answer:** E — Ambiguous
- **Scoring:** Exact match (single letter)
- **Domain:** Natural language understanding
- **Discrimination:** Baseline 1/4, adversarial elimination 3/4
- **Source:** Architecture Exp, LOGIC-05

### B4. Hensel Lifting Verification
- **Question:** Find least prime p where there exists n: n^4+1 = 0 (mod p^2). Then find least m where m^4+1 = 0 (mod p^2).
- **Correct Answer:** 110 (p=13, m=110)
- **Scoring:** Exact numerical match
- **Domain:** Number theory
- **Discrimination:** Sonnet got 155 (wrong lift), Opus got 110 (correct)
- **Source:** Architecture Exp, MATH-03

### B5. Combinatorial Probability (Random Chords)
- **Question:** Disk divided into 4 quadrants. 25 additional random chords (endpoints in different quadrants). Expected number of regions?
- **Correct Answer:** 204
- **Scoring:** Exact numerical match
- **Domain:** Combinatorics / probability
- **Discrimination:** Sonnet got 104, Opus got 204
- **Source:** Architecture Exp, MATH-08

### B6. Binary Representation Minimization
- **Question:** For each n, let k(n) = number of ones in binary representation of 2023*n. Find min k(n).
- **Correct Answer:** 3
- **Scoring:** Exact numerical match
- **Domain:** Number theory / binary arithmetic
- **Discrimination:** Sonnet got 4 (greedy stopped early), Opus got 3 (thorough search)
- **Source:** Architecture Exp, MATH-13

### B7. Sarcasm Classification
- **Question:** Classify three Reddit replies as sarcastic (0) or non-sarcastic (1). Determine 3-bit pattern.
- **Correct Answer:** 0,0,1
- **Scoring:** Exact match on 3-bit string
- **Domain:** Natural language understanding / pragmatics
- **Discrimination:** Baseline got first reply wrong; multi-perspective reasoning fixed it
- **Source:** Architecture Exp, LOGIC-14

### B8. Stack-Based Bracket Matching
- **Question:** Given sequence with mixed brackets (), [], {}, <>. Find first mistake in provided derivation steps.
- **Correct Answer:** Step 19
- **Scoring:** Exact numerical match
- **Domain:** Formal languages / stack-based reasoning
- **Discrimination:** Sonnet got 17, Opus got 19 (correct)
- **Source:** Architecture Exp, LOGIC-06

### B9. Polymer Adiabatic Force Law
- **Question:** Freely jointed polymer chain with n mass points joined by struts of length l. What is force law F(x) when thermally isolated?
- **Correct Answer:** F(x) = 3E(0)x/(nl)^2
- **Scoring:** Exact formula match (coefficient and powers)
- **Domain:** Physics / statistical mechanics
- **Discrimination:** Both models got wrong coefficients/powers; sign-explicit prompting needed
- **Source:** Architecture Exp, SCI-04

### B10. Mean-Field Lattice Gas Occupancy
- **Question:** Grand canonical ensemble, mean-field approximation. Given e = -(k_BT)/(2*pi), mu = 0.1*k_BT, z_h=4, z_v=8, T=300K. Find occupancy <n>.
- **Correct Answer:** 0.424
- **Scoring:** Numerical match (within 0.01)
- **Domain:** Chemistry / statistical mechanics
- **Discrimination:** Models systematically get wrong sign in double-counting factor; no architecture fully solved it
- **Source:** Architecture Exp, SCI-08

### B11. Board Game Rule Chaining
- **Question:** 45 rules of a complex board game. Chain rules forward. Does the butterfly reveal a secret to the fish?
- **Correct Answer:** Unknown (cannot be proved or disproved with given rules)
- **Scoring:** Binary (correct conclusion: "unknown")
- **Domain:** Logic / rule-based reasoning
- **Source:** Architecture Exp, LOGIC-02

### B12. Knowledge-Gated Domain Question (FTIR Gelation)
- **Question:** Given FTIR peaks at 1645, 1652, 1618, 1680 cm^-1 with heating behavior and concentration effects, explain protein gelation mechanism. (9 options)
- **Correct Answer:** C — Coiled-coils form upon gelation
- **Scoring:** Exact match (single letter)
- **Domain:** Biophysics / spectroscopy
- **Discrimination:** Both models wrong without retrieval; 100% fix rate with domain knowledge provided
- **Source:** Architecture Exp, SCI-01

---

## Scoring Framework

For every test case run, record:

| Metric | How |
|---|---|
| **Correctness** | 0 or 1 (binary match against answer) or partial credit where noted |
| **Total tokens** | Sum across all agents spawned (from orchestrator.jsonl) |
| **Wall-clock time** | Orchestrator start to root node `complete` status |
| **Tree depth** | Max depth reached |
| **Node count** | Total nodes spawned |
| **Replan count** | How many times any node replanned |
| **Escalation count** | How many times any node escalated |

## Notes

- Tier A cases originally required multi-hour Atlas runs. Getting them right with Eywa at lower cost = strong signal.
- Tier B cases have documented baseline vs. best-architecture performance. Eywa should at minimum match best-architecture results.
- Full question text for Tier B cases lives in `/older_stuff/architecture-exploring-with-benchmarks/Architecture-Automated-Exploration/question-bank/questions/`.
- Some Tier B candidates need the full multi-choice option text to be usable — pull from source files before running.
