# Computation Registry

Computations identified during explorations that would significantly advance the mission. Maintained by the strategizer, read by the missionary and future strategizers.

## 1. Operationally Relevant S_max (Thermal/Environmental Entropy)

**What:** Replace the Bekenstein bound with the thermally accessible entropy for each system (using statistical mechanics, partition functions) and redo the classicality budget. The Bekenstein bound is the theoretical maximum; actual systems use vastly less.
**Why it matters:** The Bekenstein-based budget is absurdly generous for macroscopic systems. Using actual thermodynamic entropy could yield physically interesting (tighter) budgets — this is the most likely path to making the classicality budget operationally relevant.
**What it resolves:** Whether the classicality budget constrains anything above Planck scale when using realistic entropy measures.
**Source:** Explorations 001 and 002 (Phase 1)
**Difficulty:** Moderate (50-100 line scipy script per system, requires partition function calculations)
**Specifics:** For the brain: S_thermal ~ kN_A ln(W) for relevant degrees of freedom. For a lab region: ideal gas entropy S = NkB[5/2 + ln(V/N × (2πmkBT/h²)^(3/2))].

## 2. Near-Horizon Budget with Proper GR

**What:** Compute the classicality budget for an observer at various proper distances from a BH horizon, using the Bousso covariant entropy bound.
**Why it matters:** The BH horizon is where Bekenstein is saturated — the budget is tightest. This is the most physically interesting regime above Planck scale.
**What it resolves:** Whether the budget predicts something non-trivial about classical reality near horizons, connecting to complementarity and firewalls.
**Source:** Explorations 001 and 002
**Difficulty:** Moderate (needs careful GR calculation with Schwarzschild metric)
**Specifics:** Bousso bound: S[L] ≤ A/(4G) for lightsheets. Compute for shells at r = r_s(1+ε) for various ε.

## 3. Saturation Check for Non-Spin Models

**What:** Numerically simulate quantum Darwinism in a harmonic oscillator or photonic environment and compare achieved R_δ with the budget bound.
**Why it matters:** Zurek's spin models saturate the budget. If realistic environments also saturate it, the bound is tight (not just a loose ceiling). If they don't, the gap tells us something about the inefficiency of real decoherence.
**What it resolves:** Whether the classicality budget is practically achievable beyond idealized spin models.
**Source:** Exploration 001
**Difficulty:** Substantial (~200 lines Python with QuTiP, open quantum system simulation)

## 4. Budget at the Decoherence Boundary

**What:** For a many-body quantum system with tunable decoherence, compute how the classicality budget changes as decoherence strength varies. Look for a "classicality phase transition."
**Why it matters:** Could identify the precise point where classical reality becomes possible — a phase transition in the classicality budget.
**Source:** Exploration 002
**Difficulty:** Substantial (needs QuTiP or similar open quantum system simulation)

## 5. Early Universe Budget vs. Temperature/Time

**What:** Compute the classicality budget as a function of cosmic time/temperature, from Planck epoch to present.
**Why it matters:** The early universe was hot and dense — the budget may have been tight enough to constrain classical reality. This could connect to the emergence of classicality in cosmology.
**Source:** Exploration 002
**Difficulty:** Moderate (cosmological scaling relations + Bekenstein bound)

## 6. Formal Proof that N·log₂(d_e) ≤ S_max for Physical Environments

**What:** Carefully apply the Bekenstein bound to the environment's Hilbert space in specific models, establishing that the abstract quantum Darwinism capacity N·log₂(d_e) is bounded by S_max.
**Why it matters:** Would definitively establish the classicality budget as a theorem rather than a conjecture — closing the gap between Tank (2025)'s abstract formula and the physical bound.
**What it resolves:** Whether the bridge from QD to Bekenstein is rigorous or involves hidden assumptions.
**Source:** Exploration 003
**Difficulty:** Moderate (careful dimensional analysis and physics)

## 7. Comparison with Bousso's Channel Capacity Bound

**What:** Compute whether Bousso (2017) "Universal limit on communication" gives a tighter or looser constraint than Bekenstein when applied to environmental redundancy.
**Why it matters:** Bousso's bound is about dynamic information flow (channel capacity), which may be more natural for the "environment as communication channel" picture in quantum Darwinism.
**What it resolves:** Whether there's an alternative derivation path that's potentially tighter and more physically motivated.
**Source:** Exploration 003
**Difficulty:** Moderate (needs mapping between static entropy and dynamic channel capacity)

## 8. HaPPY Code QD Redundancy Verification

**What:** Verify R_δ = S_max/(2·S_T) for the HaPPY code numerically by computing mutual information I(S:R_k) for different boundary regions R_k of varying sizes. Input: HaPPY code tensor structure (arXiv:1503.06237 Fig. 2). Output: redundancy count as a function of boundary fraction.
**Why it matters:** The 50% saturation of the classicality budget by the HaPPY code is the cleanest quantitative prediction of the QD↔HQEC mapping. Numerical verification would be the first concrete check of this novel connection.
**What it resolves:** Whether the R_δ = S_max/(2·S_T) result is an exact theorem or an approximation; whether it holds for non-perfect tensor codes.
**Source:** Strategy-002, Exploration 001 (QD↔HQEC literature search)
**Difficulty:** Moderate (~100 lines numpy/quimb, tensor network contraction)
**Specifics:** Use arXiv:1503.06237 Fig. 2 for the HaPPY pentagon code tensor structure. For each boundary fraction f = |R_k|/n (where n = total boundary qubits), count how many disjoint subregions R_k of that size have x ∈ W(R_k). Plot R_δ(f). Threshold should be at f = 0.5.

## 9. Curved-Space Correction to S = 1/(540 ln2)

**What:** Replace the naive flat-space Stefan-Boltzmann formula with the curved-space Hawking radiation stress tensor (Page's tensor) to compute the actual entropy density near the Schwarzschild horizon. The naive calculation assumes T = T_H uniformly; in curved space, the local temperature diverges as T_local ∝ T_H / sqrt(1 - r_s/r) near the horizon.
**Why it matters:** The 1/(540 ln2) result uses flat-space blackbody radiation at T = T_H evaluated at r = r_s. In reality, the local temperature diverges at the horizon (Tolman relation). The curved-space result may differ significantly.
**What it resolves:** Whether 1/(540 ln2) is the "correct" physical constant (it's the constant an observer at infinity assigns to the sphere) vs. what a local observer near the horizon would measure.
**Source:** Strategy-002, Exploration 002 (BH constants literature verification) — closest prior work: Kim arXiv:2112.01931
**Difficulty:** Moderate (~50-100 lines scipy, numerical integration of Page's stress tensor over sphere of radius r_s)
**Specifics:** Use Page's renormalized stress tensor ⟨T_μν⟩_ren from Christensen & Fulling (1977) in the Unruh vacuum. Integrate the energy density over the sphere r = r_s.

## 11. Ion Trap Classicality Phase Transition: Dynamical QD Simulation

**What:** Simulate the time evolution of I(S:F_k) as a system qubit decoheres into the motional modes of a 20-ion trap. Use a Lindblad master equation. Plot I(S:F_k)(t) for different n̄ values and check whether R_δ approaches R_max over time.
**Why it matters:** The experimental test proposal (E003) identified the ion trap phase transition at n̄_c ≈ 0.003 but used a static budget calculation. The dynamical simulation would show whether the budget is actually achievable in finite time with realistic coupling Hamiltonians, providing the full experimental protocol.
**What it resolves:** Whether the "classicality phase transition" is robust to dynamical effects, and what measurement time is needed.
**Source:** Strategy-002, Exploration 003 (experimental test)
**Difficulty:** Moderate (~50-100 lines Python, Lindblad master equation)
**Specifics:** Use QuTiP or scipy.linalg. System = 1 qubit. Environment = N-1 motional modes at temperature n̄. Coupling via Jaynes-Cummings. Track I(S:F_k)(t) for fragment = subset of modes.

## 12. Optimal Fragment Partition for Ion Trap QD

**What:** For N = 20 ions, find the partition of the 60 motional modes into fragments F_k that maximizes R_δ (measured redundancy). This is an information-theoretic optimization.
**Why it matters:** The experimental test needs to know the optimal measurement strategy to maximize the chance of observing the classicality budget constraint.
**Source:** Strategy-002, Exploration 003
**Difficulty:** Easy (~5-10 lines scipy.optimize or brute force for small N)
**Specifics:** Given coupling matrix J_{ij} between system qubit and motional modes, partition modes into fragments to maximize the count of fragments with I(S:F_k) ≥ (1-δ)H_S.

## 10. Island Formula: R_δ(t) Through BH Evaporation

**What:** Replace the RT formula with the quantum extremal surface (island) formula S(R) = min{ext}[Area(∂I)/4G + S_bulk(R ∪ I)] to compute how the classicality budget R_δ evolves as a function of evaporation time t.
**Why it matters:** Strategy-001 (exploration-007) conjectured that the Page time marks a "classicality transition" — before Page time, R_δ = 0 for BH interior; after Page time, R_δ ≥ 1 (collective verification becomes possible). This is currently labeled CONJECTURED and needs explicit computation.
**What it resolves:** Whether the Page transition creates a "classicality transition" — a moment when classical reality becomes possible for exterior observers of the BH interior. Whether this is a new perspective on the information paradox or just a restatement of known results.
**Source:** Strategy-002 STRATEGY.md (Exploration D), holographic-classicality-budget.md library entry
**Difficulty:** Moderate (~100-150 lines Python/sympy). Model: 2D JT gravity + 2D CFT (the canonical island formula computation). Use the Penington-Almheiri setup from arXiv:1911.09536.
**Specifics:** Start with the doubly holographic setup: S_Hawking(t) = t (growing entropy before Page time), then use the island formula to get the Page curve. Map this to R_δ(t) = S_Hawking(t)/S_T - 1 (no island phase) and R_δ(t) ≈ 0 (island phase). Check whether there's a classicality transition at the Page time.
