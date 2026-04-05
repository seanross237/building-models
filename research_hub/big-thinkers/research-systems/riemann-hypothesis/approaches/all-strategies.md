# Riemann Hypothesis — 10 Unconventional Attack Strategies

## Direction 1: Quasicrystal Diffraction Theory (Materials Science x Number Theory)

Freeman Dyson proposed that the zeta zeros form a 1D quasicrystal — long-range order but no periodicity. The mathematical apparatus of aperiodic tiling theory and diffraction measure theory might prove the zeros must sit on the critical line because that's the only configuration producing a "pure point" diffraction spectrum.

### Strategy 1A: "The Cut-and-Project Guillotine"

**Core idea:** Work backwards from the zeros to construct the higher-dimensional lattice that projects to produce them. The natural candidate lattice lives in the adeles (packaging all prime completions of Q). The periodic lattice is Q embedded diagonally; the irrational "cut" is the functional equation's symmetry at Re(s)=1/2. Prove the projection window is compact only when the strip collapses to the critical line. Baake-Strungaru's theorem (Meyer set + pure point diffraction => regular model set with compact window) provides the bridge.

**Crux move:** Proving zeros are a harmonious (Meyer) set — requires showing pairwise differences are uniformly discrete. Montgomery's pair correlation conjecture gives strong evidence but isn't proven.

**Novelty:** Partially novel. Dyson's conjecture is known. One contested 2024 preprint (Shaughnessy) attempts a Fourier self-duality argument. But nobody has built the explicit adelic model set with a concrete projection window, and nobody has even numerically tested whether the zeros satisfy the Meyer set condition.

**Success looks like:** An explicit adelic model set whose projected points match the zeros to arbitrary precision, with a theorem that non-critical-line zeros would rupture the compactness of the acceptance domain.

---

### Strategy 1B: "Bragg or Bust"

**Core idea:** Skip structure, attack via the diffraction measure directly. The autocorrelation of the zeros is exactly the pair correlation function (Montgomery, Goldston-Pintz-Yildirim). Prove that a zero off the critical line injects singular continuous components into the diffraction spectrum — the pathological middle ground that real quasicrystals never exhibit. The mechanism: an off-line zero creates "ghost peaks" at spacing epsilon that can't tile any reciprocal lattice. By Hof's theorem, this produces singular continuous diffraction. Then use Solomyak's theorem (substitution tilings can't have singular continuous diffraction) and argue the primes' multiplicative structure IS a substitution system.

**Crux move:** Formalizing "primes act as a substitution system" rigorously enough for the dynamical prohibition on singular continuous spectrum to apply.

**Novelty:** Partially novel. The diffraction framing is implicit in Dyson's work but nobody has computed the actual diffraction measure or made the substitution connection.

**Success looks like:** A theorem stating that any Delone set whose pair correlation matches the known asymptotics of zeta-zero spacings, and whose diffraction has no singular continuous component, must be supported on a single vertical line.

---

## Direction 2: Primon Gas Thermodynamics (Statistical Mechanics x Information Theory x Number Theory)

The "primon gas" (Julia 1990) has partition function Z(beta) = zeta(beta). Each prime p contributes a "primon" with energy log(p). Hartnoll-Yang (2025) found this gas emerges naturally near black hole singularities.

### Strategy 2A: "The Entropy Ceiling" [TOP 3 — EXPERIMENT ATTEMPTED]

**Core idea:** Construct the microcanonical entropy S(E) of the primon gas by Legendre-transforming log zeta(beta). Prove strict concavity S''(E) < 0 everywhere holds if and only if all zeros lie on Re(s) = 1/2. An off-line zero at sigma + it with sigma != 1/2 would produce a "bump" in the density of states that breaks concavity — a thermodynamically unstable phase (negative heat capacity where there shouldn't be one). This is a Lee-Yang-type violation where the zero pinches the real axis asymmetrically.

**Crux move:** Making the Legendre transform rigorous in the critical strip (where the Euler product breaks down). Likely requires truncated primon gas (primes up to N) with the concavity bound surviving N -> infinity.

**Novelty:** NOVEL. The primon gas canonical ensemble is well-studied (Julia 1990+). But nobody has done the microcanonical analysis. Knauf (1999) noted a vague Lee-Yang/RH overlap but never executed it. This specific thermodynamic stability argument is an open gap in the literature.

**Success looks like:** A theorem of the form "S(E) is strictly concave for all E > E_0 iff RH," reducing RH to a convexity statement in statistical mechanics.

---

### Strategy 2B: "Holographic Primon Censorship"

**Core idea:** Interpret zeros as quasi-normal modes of the gravitational approach to a black hole singularity (per Hartnoll-Yang). In AdS/CFT, quasi-normal modes must lie in specific half-planes dictated by unitarity of the dual CFT. Formulate an analogous unitarity bound: the boundary theory's two-point function must decay (not grow), forcing all resonances to Re(s) = 1/2. An off-line zero would be a mode growing unboundedly near the singularity — violating cosmic censorship and the Hayden-Preskill scrambling bound.

**Crux move:** Quantizing the primon gas in the gravitational background and proving the boundary theory is actually unitary.

**Novelty:** NOVEL in the specific framing. Remmen (2021) connected zeta to scattering amplitude unitarity. A 2022 modular bootstrap paper restated RH in CFT language. But the specific QNM/unitarity argument hasn't been made.

**Success looks like:** A proof that unitarity of any consistent UV-completion of the Kasner primon gas implies RH. Even a conditional result ("RH follows from unitarity of Theory X") would be a major reframing.

---

## Direction 3: Arithmetic Topology / TQFT (Knot Theory x QFT x Number Theory)

In arithmetic topology, primes correspond to knots, Spec(Z) behaves like a 3-manifold, and quadratic reciprocity is analogous to linking numbers.

### Strategy 3A: "The Chern-Simons Zeta Machine"

**Core idea:** Define a U(1) Chern-Simons functional on flat connections over Spec(Z), treating each prime p as a knot complement. Surgery on prime-knots yields Euler factors (1 - p^{-s})^{-1}, so the partition function is zeta(s). Invoke Chern-Simons reflection structure: for oriented 3-manifolds, Z(M) and Z(M-bar) are complex conjugates. If the arithmetic manifold has a natural orientation-reversing involution corresponding to s -> 1-s, zeros must lie on the fixed locus — the critical line.

**Crux move:** Extending Kim's arithmetic Chern-Simons theory from finite gauge groups to U(1) and showing the surgery formula along prime-knots reproduces the Euler product.

**Novelty:** Partially novel. Kim's framework exists for finite groups. A Feb 2026 paper extends to arithmetic BF theory. The U(1) extension is open.

**Success looks like:** A rigorously defined TQFT invariant Z_CS(M_Z, k) equal to zeta(k) with reflection-positivity forcing zeros to Re(k) = 1/2.

---

### Strategy 3B: "Knot Surgeries and the Explicit Formula Machine"

**Core idea:** Construct a framed link L_Z in S^3 whose components are indexed by primes (framings encode log(p)), such that the Reshetikhin-Turaev invariant of the surgered manifold reproduces Weil's explicit formula term-by-term. RH then follows if the surgery linking matrix is positive-definite — by Donaldson's theorem, the manifold bounds a positive-definite 4-manifold. Li's criterion (all Li coefficients positive iff RH) maps to eigenvalues of the linking matrix.

**Crux move:** Constructing L_Z explicitly and proving the linking matrix signature matches. Start with primes up to N, compute RT invariants, verify approximation of zeta in the critical strip.

**Novelty:** NOVEL. Arithmetic topology, the Weil explicit formula, and Kirby calculus all exist as mature fields. Nobody has assembled them into this specific construction. The Li coefficient / linking matrix eigenvalue correspondence is uncharted.

**Success looks like:** An explicit infinite framed link whose RT invariants recover zeta(s), with RH equivalent to positive-definiteness of the linking matrix.

---

## Direction 4: Quantum Reservoir Computing (Quantum Computing x Dynamical Systems x Number Theory)

Chaotic quantum systems produce energy level statistics matching zeta zeros via random matrix theory (GUE). The Hilbert-Polya conjecture says there should exist a self-adjoint operator whose eigenvalues are exactly the zeta zeros.

### Strategy 4A: "Billiard Table Inversion" [TOP 3 — EXPERIMENT ATTEMPTED]

**Core idea:** Treat the first 10,000 zeta zeros as a target spectrum and solve the inverse spectral problem — find a 2D billiard boundary whose Laplacian eigenvalues match them exactly. Parameterize boundaries via Fourier coefficients, run variational optimization (FEM eigensolvers + gradient descent). If the optimizer converges to a clean, describable geometry, you've found a candidate Hilbert-Polya operator.

**Crux move:** The inverse spectral problem is ill-posed ("Can you hear the shape of a drum?" is generically no). Must work within a restricted family (convex, analytic boundary, discrete symmetry) where uniqueness may hold.

**Novelty:** NOVEL. People have built abstract operators matching zeta zeros and done general inverse spectral numerics. Nobody has combined them: running a shape optimization to find a geometric billiard domain whose Laplacian eigenvalues match zeta zeros. Isospectralization tools exist (Cosmo et al. CVPR 2019). Application to zeta is untouched.

**Success looks like:** A specific billiard domain whose first N Laplacian eigenvalues match the first N zeta zeros to within numerical precision, accompanied by a proof that the boundary's regularity guarantees self-adjointness.

---

### Strategy 4B: "Chaotic Echo Spectroscopy"

**Core idea:** Use Loschmidt echo measurements in a high-Q microwave cavity shaped to the fundamental domain of SL(2,Z) (the modular billiard). Inject pulses, perturb the cavity, measure echo decay to reconstruct the effective Hamiltonian via quantum process tomography. The cavity's arithmetic symmetries (Hecke operators) should appear as symmetries of the reconstructed Hamiltonian.

**Crux move:** Proving a rigidity theorem — any self-adjoint operator on the modular surface with the correct Weyl law and correct Hecke symmetries must have spectrum equal to the zeta zeros.

**Novelty:** Partially novel. Microwave billiard experiments exist. The rigidity theorem framing is new.

**Feasibility:** LOW — requires physical lab equipment.

---

## Direction 5: Evolved Cellular Automata (Artificial Life x Complex Systems x Number Theory)

Simple CAs can generate complex behavior including prime-related structures. Use evolutionary search to find minimal generative mechanisms for prime distribution.

### Strategy 5A: "The Spectral Breeder" [TOP 3 — EXPERIMENT ATTEMPTED]

**Core idea:** Genetic programming framework where the genome encodes a 1D CA rule (radius-2 or radius-3). Fitness = how closely collision-event spacings match GUE pair-correlation statistics (the Montgomery-Odlyzko law). Run each CA for ~10^6 steps, extract collision positions, KS-test against the GUE kernel. Then take winning rules and construct their exact transfer matrix — if eigenvalues lie on a circle or line, you have a discrete Hilbert-Polya operator from a lookup table.

**Crux move:** The GUE-like regime lives in the narrow class-4 edge-of-chaos band. Need multi-objective fitness (Lyapunov dimension + transient length + GUE fit) to avoid getting trapped in trivial or fully chaotic attractors.

**Novelty:** COMPLETELY NOVEL. No paper uses evolutionary/genetic programming to breed CA rules matching GUE/zeta statistics. No paper proposes CA transfer matrices as candidate Hilbert-Polya operators.

**Success looks like:** A single CA rule whose collision-time spacings match GUE to 4+ sigma across multiple correlation functions, together with a proof that its transfer-matrix spectrum is unitarily equivalent to a Hermitian operator.

---

### Strategy 5B: "The Arithmetic Terrarium"

**Core idea:** Breed a 2D CA whose occupied sites at time T reproduce the primes up to T — inverting the Sieve of Eratosthenes with local growth rules. By Curtis-Hedlund-Lyndon, such a rule defines a shift space endomorphism whose dynamical zeta function (Ruelle-type, counting periodic orbits) would encode prime-counting information. A functional equation for the dynamical zeta could translate to a statement about Riemann zeros.

**Crux move:** Exact prime generation is impossible for finite-state CA (primes aren't a sofic shift). Relax the target: find a rule whose density matches li(x)/x with O(x^{1/2+epsilon}) error — that density condition IS RH.

**Novelty:** Somewhat novel. CA prime sieves exist. The dynamical zeta function connection is the new angle.

**Success looks like:** A CA rule with <=50 states whose site-occupation density provably satisfies |pi_CA(T) - li(T)| = O(T^{1/2} log T).
