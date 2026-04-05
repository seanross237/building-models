# Birch & Swinnerton-Dyer Conjecture — Attack Approaches

**Date:** 2026-04-04
**Goal:** Explore 5 cross-functional computational approaches to making progress on BSD

## The Problem

For an elliptic curve E over Q:
- **Rank conjecture:** rank(E(Q)) = ord_{s=1} L(E,s)
- **Exact formula:** The leading coefficient of L(E,s) at s=1 equals (|Sha| * Omega * Reg * prod(c_p)) / |E(Q)_tors|^2
- **Open frontier:** rank >= 2 cases, finiteness of Sha, the exact leading coefficient

## Approaches

### 1. ML on LMFDB — Symbolic Regression for Conjecture Discovery
**Status:** Classification well-explored (He, Lee, Oliver 2019-2024). Conjecture generation via symbolic regression is UNTRIED.
**Idea:** Use genetic programming / symbolic regression on LMFDB data to discover closed-form relationships between BSD invariants that humans haven't found. Move beyond "predict rank" to "discover new intermediate invariants."
**Novelty:** Partial — classification done, conjecture generation novel
**Agent findings:** [approach-1-ml/](approach-1-ml/)

### 2. Statistical Mechanics / RG Flow on L-functions
**Status:** NOVEL. Ingredients exist (primon gas, Bost-Connes, Samart 2024 Ising-L-function bridge) but nobody has assembled them toward BSD.
**Idea:** Model L(E,s) as a partition function, primes as energy levels, rank as phase transition order. Apply renormalization group flow to track how coarse-grained prime data flows toward s=1 critical behavior.
**Novelty:** Yes — specific RG flow → rank program is unstudied
**Agent findings:** [approach-2-statmech/](approach-2-statmech/)

### 3. TDA / Persistent Homology on Selmer Groups
**Status:** NOVEL. Zero prior work applying computational topology to arithmetic geometry data.
**Idea:** Build point clouds from Selmer group data / reduction types across primes. Run persistent homology. Hypothesis: topological features (Betti numbers, persistence barcodes) detect rank and Sha structure — since Sha literally measures cohomological obstructions (holes).
**Novelty:** Yes — completely open territory
**Agent findings:** [approach-3-tda/](approach-3-tda/)

### 4. Quantum Error Correction meets Arithmetic Cohomology
**Status:** NOVEL. Zero prior work connecting QEC code theory to Selmer/Sha structure.
**Idea:** The Selmer exact sequence 0 → E(Q)/pE(Q) → Sel_p(E) → Sha[p] → 0 is a chain complex over F_p — the same structure CSS quantum codes are built from. Sha has a symplectic form (Cassels-Tate pairing), matching CSS orthogonality conditions. Construct quantum codes from Selmer data; "logical qubits" = rank, "syndrome" = Sha. Quantum information bounds (Singleton, Hamming) then constrain BSD invariants. Park & Park (Feb 2026) showed Cassels-Tate IS a BF functional — BF theory generates topological quantum codes.
**Novelty:** Yes — completely unexplored
**Prior approach (archived):** LLM-Guided Formal Proof Search — demoted to long-term (8-15yr timeline). See [approach-4-lean/](approach-4-lean/)
**Agent findings:** [approach-4-qec/](approach-4-qec/)

### 5. Holographic / Arithmetic Gauge Theory Simulation
**Status:** NOVEL. Kim's arithmetic Chern-Simons + Park & Park's arithmetic BF theory (Feb 2026) provide framework. Nobody has built computational simulations.
**Idea:** Discretize the arithmetic Chern-Simons / BF functional onto a computational lattice. Numerically extract BSD invariants. The Cassels-Tate pairing IS an arithmetic BF functional — simulate it.
**Novelty:** Yes — theory waiting for someone to build the simulation
**Agent findings:** [approach-5-holographic/](approach-5-holographic/)

## Progress Tracker

| Approach | Agent | Status | Key Finding |
|----------|-------|--------|-------------|
| 1. ML / Symbolic Regression | bsd-ml | **Complete** | BSD decomposition: Omega*Reg*Tam/Tors^2 = sqrt(N) * exp(SUM beta_p * a_p) * exp(C_r). Cross-validated R^2=0.984 (rank 1), 0.951 (rank 2). Effective beta_p ~ 3.6/p^{4.2}, NOT naive 1/p Euler product (which gives negative R^2). Correction delta_p = beta_p - 1/p ~ -0.61/p^{0.80}. a_2 dominates (partial corr 0.92 with BSD RHS after N-conditioning). C_r linear in rank (slope -0.39). Murmuration sum with s*=0.84 gives 98% binary rank classification. 5 conjectures formulated. |
| 2. Stat Mech / RG Flow | bsd-statmech | **Complete** | Running coupling g(Λ)=log|L_Λ(E,1)|/log(Λ) separates rank classes with Cohen's d>9 (rank 0 vs 1) to d>18 (rank 0 vs 2). 100% OOS classification accuracy on 50 test curves. Free energy F=-log|L| is linear in rank with slope≈log(log(Λ)), R²=0.98. Framework reinterprets explicit formula as RG flow; rank = universality class. Works with only 25 primes (95% accuracy). |
| 3. TDA / Persistent Homology | bsd-tda | Deployed | — |
| 4. Quantum Error Correction | bsd-qec | **Complete** | Poitou-Tate exact sequence gives valid CSS quantum code. Sha[p] = logical qubits (delocalized quantum info), E(Q)/pE(Q) = stabilizer generators, local conditions = checks. CSS orthogonality from Cassels-Tate alternating pairing. Code distance d=1 (Sha elements zero-weight locally), so Singleton trivial. CSS capacity bound gives dim Sha[p] <= (1-1/p)*dim H^1(G_S,E[p]) ~ omega(N). Verified dim Sha[p]=2 on 16 curves with nontrivial Sha (N<5000). Arithmetic toric code (BF theory, Park&Park) matches 3/11 curves via Legendre-symbol graph. BSD reformulated: stabilizer rank = ord_{s=1} L(E,s). |
| ~~4-old. Lean Proof Search~~ | ~~bsd-lean~~ | ~~Complete (archived)~~ | ~~8-15yr timeline, demoted to long-term~~ |
| 5. Holographic Simulation | bsd-holo | **Complete** | First computational arithmetic gauge theory simulation. Euler product on lattice gives r=-0.919 rank correlation (near-perfect). BF partition function detects Sha (r=+0.937 with log\|Sha\|). Gauge susceptibilities detect rank (r=-0.946 on focused suite). Spectral dimension of lattice Laplacian correlates with rank (r=+0.479). 30 curves, ranks 0-3, \|Sha\| in {1,4,9,25,49}. |
