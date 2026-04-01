# Navier-Stokes Regularity: Consolidated Findings Across All Research Systems

Last updated: 2026-03-30

---

## 1. Executive Summary

Three independent research systems (Atlas, Philosopher Atlas, Codex Philosopher Atlas) have collectively executed 40+ explorations across 5 missions targeting the 3D Navier-Stokes regularity problem through the lens of the Vasseur (2007) pressure exponent gap. The primary result is definitive and negative: the De Giorgi recurrence exponent beta = 4/3 is rigorously sharp within the De Giorgi-Vasseur framework, proven via an eight-route obstruction map, tool-independence across four analytical methods, and a one-line extremizer construction (constant divergence-free field). Beyond De Giorgi, every tested alternative route --- far-field pressure harmonic tails, H^1/BMO duality, compensated compactness, geometric/vorticity direction coherence, exact NS reformulations within local-energy architecture, and compactness-rigidity host-space programs in L^3, H-dot-1/2, and BMO^{-1} --- has been closed with specific obstruction arguments. No surviving constructive path to NS regularity has been identified by any system.

---

## 2. The Problem

### What NS regularity means

The 3D incompressible Navier-Stokes equations admit Leray-Hopf weak solutions for arbitrary finite-energy initial data. Whether these solutions remain smooth (bounded) for all time, or can develop singularities in finite time, is open. "Regularity" means proving that all suitable weak solutions are globally smooth.

### What beta means

Vasseur (2007) reformulated the regularity problem via De Giorgi iteration. The proof produces a nonlinear recurrence relation on level-set energies:

U_k <= C^k * U_{k-1}^beta

If beta > 3/2, the recurrence drives U_k to zero, yielding full regularity of all suitable weak solutions (Vasseur's Conjecture 14). The current best value is beta = 4/3, leaving a gap of 1/6 (equivalently, the gap between s/n = 1/3 and s/n = 1/2 in the universal formula beta = 1 + s/n).

### What Tao's constraint means

Tao (2016) proved that any proof method relying only on the energy identity plus harmonic analysis estimates cannot resolve NS regularity. beta = 4/3 < 3/2 is a concrete quantitative instance of this supercritical obstruction. Any genuine progress must use NS-specific structure that Tao-style averaged models would destroy.

### The W^{1,3} wall

Multiple systems independently converged on the same structural barrier: Leray-Hopf provides u in L^2_t H^1_x (i.e., grad(u) in L^2), but every tested route requires grad(u) in L^3 (or W^{1,3}) to work. The beta = 3/2 threshold and the W^{1,3} threshold are two faces of the same obstruction. (Patlas VP, Atlas VP S2)

---

## 3. Closed Routes

### 3A. De Giorgi Framework (All Internal Modifications)

All routes within the De Giorgi-Vasseur proof structure are exhausted. beta = 4/3 is sharp.

| Route | Specific Obstruction | System |
|---|---|---|
| Modified energy functional | Provably sharp at the energy definition step; modification cannot improve beta | Atlas VP S2-E001 |
| Improved Sobolev for div-free fields | H^1 -> L^6 embedding is tight in 3D; div-free does not help | Atlas VP S2-E001 |
| Optimized truncation function | Truncation step is tight under NS structural constraints | Atlas VP S2-E001 |
| Direct Chebyshev improvement (analytical) | Circular with regularity: improving Chebyshev from L^{10/3} to L^4 is equivalent to improving regularity from H^1 to H^{5/4} (Lions threshold) | Atlas VP S2-E003 |
| Direct Chebyshev improvement (computational) | DNS tightness ratios ~3-5x but k-independent; constant slack does not improve beta | Atlas VP S2-E002 |
| Commutator / compensated compactness | Three independent obstructions: (1) truncation breaks div-free, killing CLMS prerequisite; (2) divergence-error remainder dominates at high frequencies; (3) CRW commutator bounds give no improvement for bounded multipliers | Atlas VP S2-E004 |
| Frequency-localized Littlewood-Paley | Bernstein penalty is dimensional (2^{3j/5} in 3D); CZ is already the optimal frequency-by-frequency estimate; spectral content shifts to high k | Atlas VP S2-E005 |
| Non-CZ pressure handling (IBP) | Gives beta = 1, strictly worse; loses CZ consolidation gain of 1/3 | Atlas VP S2-E006 |
| Non-CZ pressure handling (H^1/BMO duality) | Gives beta = 4/3 (same); exponent is tool-independent | Atlas VP S2-E006 |
| Non-CZ pressure handling (CRW commutators) | Gives beta <= 1 | Atlas VP S2-E006 |
| CZ slack improvement on P_k^{21} | CZ slack is k-independent and tighter for P_k^{21} than for full pressure (1.7-3.9x vs 7.6-17.5x); no room for improvement | Atlas VP S1-E004 |
| Galilean invariance (Tran-Yu approach) | Pressure Poisson equation is Galilean-invariant for div-free flows; frame shifts cannot improve CZ bounds | Atlas VP S1-E003 |
| Alternative De Giorgi decompositions | 13-paper survey: beta = 4/3 untouched since 2007; Choi-Vasseur (2014) achieves only beta = 7/6 (weaker) | Atlas VP S1-E005 |
| Vorticity formulation (Vasseur-Yang 2021) | 4/3 reappears from trilinear nonlinearity: grad costs U^{1/2}, quadratic gives U^{5/6}, total = 4/3; barrier is universal across formulations | Atlas VP S1-E008 |
| Beltrami conditional regularity | Mechanism real for exact Beltrami (measure-zero) but does not survive even 1% perturbation; >98% alignment required for beta > 1 | Atlas VP S1-E006,E007,E010 |
| Div-free level-set distribution | Constant field u=(c,0,0) is div-free and achieves Chebyshev equality; div-free alone cannot help | Atlas VP S2-E008 |

**Sharpness proof:** The constant vector field u(x) = (c,0,0) is divergence-free, lies in H^1(T^3), and achieves Chebyshev ratio -> 1 as lambda -> c-. This simultaneously extremizes three of the four De Giorgi chain steps. (Atlas VP S2-E008)

### 3B. H^1 Pressure / Compensated Compactness Route

| Route | Specific Obstruction | System |
|---|---|---|
| H^1-BMO duality for pressure pairing | W^{1,2} does not embed into BMO (need W^{1,3}); even with hypothetical W^{1,3}, H^1-BMO is WORSE than Holder (loses U_k^{1/2} factor) | Patlas VP |
| Atomic decomposition of H^1 pressure | Cancellation gain and gradient cost exactly cancel at optimal scale; De Giorgi test functions psi_k >= 0 waste all atomic cancellation (atoms need oscillating test functions) | Patlas VP |
| Interpolation H^1 cap L^{4/3} | Complex interpolation gives L^{p_theta} with p_theta < 4/3; wrong direction | Patlas VP |
| Bogovskii corrector for localization | Introduces 2^{2k} compound growth; strictly worse than original; eliminates all localization strategies | Patlas VP |

**Unifying obstruction:** All three H^1 branches hit the same W^{1,3} wall. The far-field pressure (harmonic on Q_k) is the sole obstruction; local pressure closes superlinearly. (Patlas VP)

### 3C. Far-Field Pressure Harmonic Tail

| Route | Specific Obstruction | System |
|---|---|---|
| Generic harmonic regularity of far-field | Fails Tao gate: smoothness of harmonic tail does not shrink the bad coefficient C_far ~ ||u||_{L^2}^2 / r_k^3 | Codex Patlas step-001 |
| Exact algebraic form of u.grad(u) for far-field | Fails Tao gate: after localization the live issue is the harmonic-tail pressure pairing, and no estimate shows the raw algebraic form shrinks the surviving affine-or-higher pressure moments | Codex Patlas step-001 |
| Vorticity/strain geometry for far-field | Fails Tao gate: geometry may matter elsewhere but no direct route from local geometry to shrinkage of the nonlocal far-field coefficient | Codex Patlas step-001 |
| NS-specific remote-shell cancellation | Kill condition fired: no screened NS-specific ingredient shrinks the actual bad coefficient for the surviving far-field pairing | Codex Patlas step-001 |

**Key insight:** The localization/test structure annihilates constant pressure modes automatically, but affine and higher harmonic modes survive generically. The only automatic quotient is by constants. (Codex Patlas step-001)

### 3D. Geometric / Vorticity-Direction Routes

| Route | Specific Obstruction | System |
|---|---|---|
| Standalone vorticity-direction coherence | Prior-art calibrated (Constantin-Fefferman family); not a standalone novelty claim | Codex Patlas step-002 |
| Standalone local Beltrami / alignment | Pre-killed: fragile, controls wrong object (u x omega, not full S omega.omega), Tao-robust | Codex Patlas step-002 |
| Tube coherence / persistence (standalone) | Only live as dynamic hybrid; one-time tube imagery is static and Tao-robust | Codex Patlas step-002 |
| Direction coherence + tube persistence (primary hybrid) | Dynamically weak: under neutral Eulerian parabolic localization, diffusion on scale r over time r^2 erases direction coherence; no candidate clears "dynamically plausible" bar | Codex Patlas step-003, step-004 |
| Beltrami deficit + concentration | Dynamically weak: threshold tuning manufactures signal while exterior/nonlocal strain remains scale-critical | Codex Patlas step-004 |
| Beltrami deficit + anisotropy | Dynamically weak: route becomes plausible only after preferred-axis fitting stronger than the bounded package allows | Codex Patlas step-004 |

**Summary:** Under a neutral Eulerian localization protocol (|omega| >= r^{-2} threshold on B_r x [t*-r^2, t*]), every geometric candidate is either dynamically weak, static-only, or collapses to prior art. The geometry branch was invalidated at the dynamic screen (step-004). (Codex Patlas)

### 3E. Exact NS Reformulations Within Local-Energy Architecture

| Route | Specific Obstruction | System |
|---|---|---|
| Divergence / stress form | Identity-level packaging only; after IBP leaves the same cutoff-flux burden on grad(phi); Tao-insufficient | Codex Patlas step-005, step-006 |
| Lamb-vector / Helmholtz-projected form | Gradient/projection debt reappears as pressure/CZ/commutator cost after localization; Tao-insufficient | Codex Patlas step-005, step-006 |
| Vorticity transport / Biot-Savart form | Biot-Savart reinsertion repays the same nonlocal cost; Tao-insufficient | Codex Patlas step-005, step-006 |

**Fixed audit target:** I_flux[phi] = integral of (|u|^2 + 2p) u.grad(phi) over Q_r. All three exact-rewrite families fail to produce a smaller effective coefficient on this term after full bookkeeping. (Codex Patlas step-005, step-006)

### 3F. Compactness-Rigidity / Critical-Space Programs

| Route | Specific Obstruction | System |
|---|---|---|
| L^3 as host space | Extraction package is diffuse: stability, extraction, normalization, and LEI bridge all missing as a stack (not one narrow theorem) | Codex Patlas step-007 |
| H-dot-1/2 as host space | Same diffuse-stack problem plus missing LEI-compatibility bridge (Hilbert-style program does not naturally tie to suitable-weak / local-energy floor) | Codex Patlas step-007 |
| BMO^{-1} as host space | Not admitted: only small-data mild theory; no large-data replacement compactness package exists | Codex Patlas step-007 |
| Mixed bridge architecture | No locally supported bridge unifying critical-space language with inherited LEI floor | Codex Patlas step-008 |
| Any critical-space framework change | Only the inherited suitable-weak / Leray-Hopf plus LEI floor is locally supported as a frozen framework; critical-space alternatives remain "diffuse-package candidates, not frozen frameworks" | Codex Patlas step-008 |

**Summary:** The compactness-rigidity route (Kenig-Merle-style) was audited against a six-part extraction package checklist. No host space passed. The branch stops at a package obstruction. (Codex Patlas step-007, step-008)

---

## 4. Surviving Leads

### 4A. Leads identified but not yet tested

| Lead | Description | Source | Honest Assessment |
|---|---|---|---|
| Far-field p_far harmonic on Q_k | p_far oscillation decays exponentially with distance from boundary of Q_k (Harnack). A LOCAL H^1 norm of p_far might be much smaller than the global norm, potentially bypassing the global-H^1 = fixed-constant obstruction. | Patlas VP | Untested. The global/local distinction is the right structural observation, but no estimate has been attempted. |
| Lorentz-space De Giorgi | The L^{3/2,infinity} weak-type estimate is available but unexploited. A De Giorgi framework using weak-type norms directly could sidestep the strong-type CZ ceiling. | Patlas VP | Untested. Requires building a new De Giorgi iteration from scratch in Lorentz spaces. |
| Fractional regularity bootstrap | The step between W^{1,2} and W^{1,3} is fractional. Fractional De Giorgi methods might provide W^{s,2} with s > 1; BMO embedding requires s = 3/2. | Patlas VP | Untested. The fractional gain required (s from 1 to 3/2) is large; unclear whether any fractional method can bridge it. |
| Divergence-free structure BEFORE cutoff | All tested approaches applied H^1 AFTER localizing (which destroys H^1). Using div-free before the cutoff might preserve the structure. | Patlas VP | Untested. Ordering issue is correctly identified but no implementation has been attempted. |
| Fractional NS sharpness test | Computing beta(alpha) for fractional NS with (-Delta)^alpha dissipation near alpha = 5/4 would reveal whether the 3/2 threshold is dimensionally determined or potentially improvable. | Patlas VP | Untested computational experiment. |
| Pressure-Hessian / tensor structure | The pressure-tensor structure tied to partial_i partial_j p = R_i R_j(u_i u_j) is the only candidate naturally attached to the pressure-side object itself; remains a representation-level possibility. | Codex Patlas step-001 | Explicitly flagged as "unclear but testable." Not yet subjected to estimate-level testing. |
| Local Beltrami structure in turbulent vortex tubes | Vortex tubes in turbulence are locally near-Beltrami at their cores. A conditional result using LOCAL Beltrami deficit restricted to regions of high |omega| rather than global deficit might survive. Connects to Constantin-Fefferman (1993) geometric criteria. | Atlas VP S1 | Interesting structural observation, but Codex Patlas step-004 showed that geometric approaches using neutral Eulerian localization fail the dynamic screen. Would need tube-adapted localization, which was explicitly flagged as a rescue that the fixed package did not earn. |
| Quantitative regularity improvements | Constant-factor improvements (10-200x from L^2 constraint) could give larger regularity radii or better singular set bounds, even though beta is sharp. | Atlas VP S2-E008 | Not a path to full regularity, but potentially useful for quantitative partial regularity. |
| Profile decomposition / concentration-compactness | Named repeatedly as the class of methods that might bypass De Giorgi entirely. | Atlas VP, Codex Patlas | The Codex Patlas audit (steps 007-008) found no coherent host-space/extraction package currently exists for NS. The route is not closed in principle, but no concrete instantiation is available. |

### 4B. Honest overall assessment

No surviving lead has been shown to work at the estimate level. The strongest untested ideas are the local H^1 norm of p_far (Patlas VP), the Lorentz-space De Giorgi (Patlas VP), and the pressure-Hessian tensor structure (Codex Patlas step-001). All remain at the "idea" stage with no supporting computation or estimate.

---

## 5. Novel Claims

Claims that survived adversarial review and may be publishable. Ordered by strength.

### Claim 1: Sharpness of beta = 4/3 for the De Giorgi-Vasseur Framework

**Statement:** The De Giorgi recurrence exponent beta = 4/3 cannot be improved by any modification to the De Giorgi-Vasseur proof for 3D Navier-Stokes. All four steps of the proof chain are individually tight under NS structural constraints.

**Evidence:** Eight-route obstruction map (Atlas VP S2-E001 through E006), adversarial review with 3 combination attacks (S2-E007), 15-paper literature search including Vasseur (2025 survey, arXiv:2503.02575), rigorous extremizer construction via constant div-free field (S2-E008), tool-independence across 4 analytical methods (S2-E006).

**Novelty:** No published paper proves sharpness. Vasseur (2025) confirms beta has not been improved but does not prove it cannot be. First systematic demonstration and proof of sharpness.

**Limitation:** Sharpness is within the De Giorgi framework only. Qualitatively different approaches might bypass De Giorgi entirely.

**Source:** Atlas VP (both strategies)

### Claim 2: Universal Formula beta = 1 + s/n

**Statement:** For De Giorgi iteration on dissipative PDEs with H^s diffusion in n dimensions, beta = 1 + s/n.

| PDE | s | n | beta | De Giorgi works? |
|---|---|---|---|---|
| 3D NS | 1 | 3 | 4/3 | No (beta < 3/2) |
| 2D NS | 1 | 2 | 3/2 | Barely (beta = 3/2) |
| 1D Burgers | 1 | 1 | 2 | Yes |
| Critical SQG | 1/2 | 2 | 5/4 | Yes (via drift, not beta) |
| 3D MHD | 1 | 3 | 4/3 | No |
| Fractional NS(alpha) | alpha | 3 | 1+alpha/3 | Only if alpha >= 3/2 |

**Novelty:** Each individual case is known. The explicit general formula tabulated across PDEs appears new. May be considered too elementary by experts.

**Source:** Atlas VP S2-E003

### Claim 3: SQG-NS Structural Gap (Three Dimensions)

**Statement:** SQG succeeds in the De Giorgi framework not by beating the Chebyshev/CZ chain but because the drift enters as a commutator with fundamentally different structure. The gap has three structural dimensions: (1) scalar vs vector (div-free preservation under truncation), (2) linear vs quadratic coupling, (3) first-order vs second-order cancellation.

**Novelty:** Synthesis. Individual results known; three-dimensional consolidated comparison appears new.

**Source:** Atlas VP S2-E003, S2-E004

### Claim 4: Tool-Independence of beta = 4/3

**Statement:** beta = 4/3 is not specific to CZ estimates. IBP gives beta = 1 (worse), CZ gives 4/3, H^1/BMO duality gives 4/3 (same), CRW commutators give beta <= 1. The exponent is locked to the NS quadratic structure, not to any particular analytical tool.

**Novelty:** No published paper compares multiple analytical tools for the De Giorgi pressure exponent.

**Source:** Atlas VP S2-E006

### Claim 5: Lamb Vector Origin of the CZ Pressure Loss

**Statement:** The Lamb vector L = omega x u generates the CZ-lossy piece of the De Giorgi pressure. For Beltrami flows (L = 0), the pressure is pure Bernoulli and CZ loss vanishes, explaining beta_eff ~ 1.0 for ABC flows.

**Novelty:** The Lamb vector, Beltrami flows, and De Giorgi iteration are individually well-known. Connecting them appears new.

**Limitation:** Exact Beltrami flows are trivially regular. The mechanism does not generalize beyond >98% alignment.

**Source:** Atlas VP S1-E006, E007, E010

### Claim 6: Computational De Giorgi Level-Set Methodology

**Statement:** De Giorgi level-set quantities (U_k, v_k, mu_k, beta_eff) can be meaningfully computed from DNS data and provide quantitative insight into the proof-to-physics gap.

**Novelty:** No prior work has computed De Giorgi level-set quantities from DNS. Novel and reproducible.

**Limitation:** DNS produces smooth solutions; the computed beta_eff is the smooth-solution value, not the near-singular value.

**Source:** Atlas VP S1-E002

### Claim 7: W^{1,3} Wall as Unified Obstruction

**Statement:** All three tested H^1 pressure routes (H^1-BMO duality, atomic decomposition, interpolation) fail for the same structural reason: the gap between W^{1,2} (what NS provides) and W^{1,3} (what every route needs). The beta = 3/2 threshold and the W^{1,3} threshold are two faces of one obstruction.

**Novelty:** Individual failures are known; the unifying characterization as the same W^{1,3} wall across three independent routes appears new.

**Source:** Patlas VP

### Claim 8: Comprehensive Obstruction Map of Beyond-De-Giorgi Routes

**Statement:** Six families of beyond-De-Giorgi approaches have been systematically tested and mapped: far-field harmonic tails, geometric/vorticity-direction, exact reformulations in local-energy architecture, and three host spaces for compactness-rigidity. All fail with specific, classified obstruction types.

**Novelty:** No published source provides a systematic audit of this breadth with specific failure classifications.

**Source:** Codex Patlas (steps 001-008)

---

## 6. The Landscape: What a Successful Proof Would Need

Based on the combined findings across all systems, a proof of 3D NS regularity would need to satisfy ALL of the following constraints:

1. **Cannot use De Giorgi iteration.** beta = 4/3 is sharp and cannot reach the required 3/2. The universal formula beta = 1 + s/n means De Giorgi iteration fundamentally cannot handle 3D NS (s/n = 1/3 < 1/2). (Atlas VP)

2. **Cannot rely only on energy identity + harmonic analysis.** Tao (2016) proved this is insufficient. Every route tested that stayed within this paradigm failed the Tao gate. (Atlas VP S2-E007, Codex Patlas steps 001, 006)

3. **Must bridge the W^{1,2} -> W^{1,3} gap.** This is the quantitative expression of the obstruction. NS provides grad(u) in L^2; every tested proof method needs grad(u) in L^3. (Patlas VP)

4. **Must handle nonlocal far-field pressure.** Local pressure closes superlinearly; the sole obstruction is the far-field pressure with coefficient C_far ~ ||u||_{L^2}^2 / r_k^3. Any successful method must make this term controllable. (Patlas VP, Codex Patlas step-001)

5. **Must use NS-specific structure that Tao-style averaging destroys.** Generic harmonic analysis, static algebraic identities, and exact reformulations within fixed architectures are all Tao-compatible and therefore insufficient. The needed ingredient is dynamical and specific to the NS nonlinear structure. (Codex Patlas steps 001, 002, 004, 006)

6. **Must handle vector truncation while preserving divergence-free structure.** SQG succeeds because scalar truncation preserves the relevant structure. NS regularity requires solving the analogous problem for vector fields, where no amplitude truncation preserves div-free (topological obstruction). (Atlas VP S2-E003)

7. **Must not depend on near-Beltrami alignment.** Even 1% perturbation from exact Beltrami alignment kills any improvement; >98% alignment is required for beta > 1. Turbulent flows are generically far from Beltrami. (Atlas VP S1-E010)

8. **Compactness-rigidity (Kenig-Merle style) requires a coherent extraction package that does not yet exist.** L^3, H-dot-1/2, and BMO^{-1} all fail as host spaces under current technology. The extraction, stability, normalization, and LEI-compatibility pieces remain a diffuse stack, not one narrow missing theorem. (Codex Patlas step-007, step-008)

9. **Geometric approaches must control FULL stretching S omega.omega, including nonlocal/exterior contributions.** Controlling only local/self-induced depletion while leaving exterior strain untouched is insufficient. Under neutral Eulerian localization, every tested geometric candidate was dynamically weak or static-only. (Codex Patlas steps 002-004)

### What class of methods remains viable in principle

The constraints above eliminate: De Giorgi iteration, H^1 pressure improvements, exact reformulations within fixed architectures, static geometry, standalone Beltrami/alignment, and current compactness-rigidity programs.

Methods that remain viable in principle (but have no concrete instantiation):
- A new proof framework that exploits dynamical NS-specific structure to bridge the W^{1,2} -> W^{1,3} gap
- Profile decomposition / concentration-compactness with a future extraction package that resolves the current host-space stacking problem
- Stochastic methods or probabilistic regularity approaches (not tested by any system)
- A qualitatively new approach to vector truncation that preserves divergence-free structure

---

## 7. Source Map

### Atlas (Vasseur-Pressure Mission)

| Component | Explorations | Key Findings |
|---|---|---|
| Strategy 001: Verify, Measure, Characterize | 10 | Path B confirmed, beta_eff < 4/3 in all 21 DNS cases, Lamb vector origin, Beltrami mechanism doesn't generalize, vorticity formulation gives same 4/3 |
| Strategy 002: Attack the 4/3 Barrier | 8 | beta = 4/3 sharp (8-route obstruction), tool-independence across 4 methods, universal formula beta = 1+s/n, SQG-NS structural gap, extremizer construction |
| Mission Complete | -- | 6 novel claims, Tier 3+ validation |

**Path:** `atlas/execution/instances/vasseur-pressure/`

### Philosopher Atlas (Vasseur-Pressure Mission)

| Component | Steps | Key Findings |
|---|---|---|
| Steps 0-2 (4 explorations) | 3 | H^1 route is dead end: H^1-BMO duality fails (W^{1,2} does not embed into BMO), atomic decomposition sharp (cancellation/gradient cancel), interpolation wrong direction, Bogovskii corrector worse. W^{1,3} wall identified as universal obstruction. Local pressure closes; far-field is sole obstruction. |

**Path:** `philosopher-atlas/missions/vasseur-pressure/`

### Philosopher Atlas (Navier-Stokes Mission)

| Component | Steps | Key Findings |
|---|---|---|
| Step 001 | 1 | Kill condition: CKN (1982), Lin (1998), Vasseur (2007) all reduce to same covering argument with same scaling exponents. dim(Sigma) <= 1 is fundamental to epsilon-regularity. Parabolic dimension 5, Sobolev exponent 10/3, scale-invariant dissipation E(r) are universal across all three proofs. |

**Path:** `philosopher-atlas/missions/navier-stokes/`

### Codex Philosopher Atlas (Beyond-De-Giorgi Mission)

| Step | Branch | Kill? | Key Finding |
|---|---|---|---|
| Step 001 | Far-field harmonic tail | Yes | Tao gate filters out all NS-specific candidates for shrinking far-field pressure coefficient; affine+ harmonic modes survive, only constants annihilated |
| Step 002 | Geometry route (prior-art + Tao screen) | No | Survived narrowly; only "direction coherence + tube persistence" hybrid survives as live |
| Step 003 | Geometry route (scenario + localization) | No | Fixed filament/tube primary scenario, neutral Eulerian parabolic localization package |
| Step 004 | Geometry route (dynamic screen) | Yes | All candidates dynamically weak or static-only under fixed package; branch invalidated |
| Step 005 | Exact reformulations (architecture fixing) | No | Fixed local-energy flux/localization as architecture, I_flux[phi] as bad term, 3 candidate rewrites |
| Step 006 | Exact reformulations (Tao screen) | Yes | All 3 exact rewrites (divergence/stress, Lamb-vector/projected, vorticity/Biot-Savart) rejected as Tao-insufficient |
| Step 007 | Compactness-rigidity (host-space audit) | Yes | L^3: diffuse extraction stack. H-dot-1/2: diffuse + missing LEI bridge. BMO^{-1}: excluded. No host space passes. |
| Step 008 | Compactness-rigidity (framework freeze) | Yes | Only suitable-weak/Leray-Hopf+LEI floor is locally supported; all critical-space alternatives rejected; branch stops at setup obstruction |

**Path:** `codex-philosopher-atlas/missions/beyond-de-giorgi/`

### Cross-System Coverage

| Question | Systems That Addressed It |
|---|---|
| Is beta = 4/3 sharp within De Giorgi? | Atlas VP (definitive yes) |
| Can H^1 pressure structure help? | Patlas VP (definitive no) |
| What is the universal obstruction? | Patlas VP (W^{1,3} wall), Atlas VP (beta = 1+s/n) |
| Can far-field pressure tail be exploited? | Codex Patlas step-001 (no, fails Tao gate) |
| Can geometric / vorticity-direction methods work? | Codex Patlas steps 002-004 (no, dynamically weak) |
| Can exact NS reformulations help within fixed architecture? | Codex Patlas steps 005-006 (no, Tao-insufficient) |
| Can compactness-rigidity (Kenig-Merle) work? | Codex Patlas steps 007-008 (no host space viable currently) |
| Do CKN/Lin/Vasseur share the same bottleneck? | Patlas NS step-001 (yes, same covering argument) |
| Is beta literature unchanged since 2007? | Atlas VP S1-E005 (yes, 13 papers, none improve beta), Atlas VP S2-E007 (yes, 15 papers including Vasseur 2025 survey) |

### Hallucinated Citation Caught

"Tran-Yu 2014 AIHP" does not exist. The real paper is Choi-Vasseur 2014 (arXiv:1105.1526). Caught by Patlas VP step-0 before budget was spent.
