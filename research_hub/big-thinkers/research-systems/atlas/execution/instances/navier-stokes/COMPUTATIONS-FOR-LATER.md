# Computation Registry

Computations identified during explorations that would significantly advance the mission. Maintained by the strategizer, read by the missionary and future strategizers.

## 1. Vortex Stretching Slack Ratio for Model Flows — PARTIALLY DONE
- **What:** For DNS flows (Taylor-Green, ABC, random-phase), compute the ratio (actual VS)/(Ladyzhenskaya bound) at each timestep
- **Status:** DONE for Taylor-Green at Re=100,500,1000,5000 (exploration 002). Min slack = 237×, grows ∝ Re^0.28.
- **Remaining:** ABC flow, Kida vortex, random-phase Gaussian, concentrated vortex tubes, adversarial initial conditions
- **Source:** Exploration 001 (Top 5, Rank 1); Exploration 002 (measured)
- **Difficulty:** Easy with existing infrastructure (code/slack_measurements.py)

## 2. NS-Specific Ladyzhenskaya Constant — NOT STARTED
- **What:** Compute C_{L,div-free} = sup{||u||_{L⁴}/(||u||_{L²}^{1/4}||∇u||_{L²}^{3/4}) : u ∈ H¹(T³), ∇·u = 0}
- **Why:** If C_{L,div-free} < C_L (general), the vortex stretching chain slack drops by C_ratio². Current 4.3× slack in F1 suggests significant room.
- **Source:** Exploration 001 (Top 5, Rank 4); Exploration 002 confirmed 4.3× slack in F1
- **Difficulty:** Medium (~50 lines, gradient descent on div-free Fourier modes)

## 3. CKN ε* Estimation — NOT STARTED
- **What:** Set up and attempt to solve the optimization problem for the minimal parabolic energy concentration ε* guaranteeing regularity
- **Why:** ε* is completely uncomputed — making it explicit would quantify partial regularity
- **Source:** Exploration 001 (Top 5, Rank 3)
- **Difficulty:** Hard (novel PDE/variational problem)

## 4. Agmon+Gronwall Slack on Burgers Analog — NOT STARTED
- **What:** For 1D Burgers equation, compute actual ||u||_{H^s} growth vs. Gronwall bound
- **Why:** Quantifies how loose the Gronwall amplification is on a simpler model problem
- **Source:** Exploration 001 (Top 5, Rank 2)
- **Difficulty:** Easy-Medium

## 5. Sharp 3D Brezis-Gallouet-Wainger Constant — NOT STARTED
- **What:** Compute the sharp constant C in ||u||_{L^∞} ≤ C||u||_{H^1}(1 + log^{1/2}(1 + ||u||_{H^{3/2}}/||u||_{H^1}))
- **Why:** Would tighten the BKM criterion
- **Source:** Exploration 001 (Top 5, Rank 5)
- **Difficulty:** Medium

## 6. Vortex Stretching Hölder Decomposition — NEW (from E002)
- **What:** Decompose the 237× vortex stretching slack into its three sources: (a) compute ||S||_{L²}||ω||²_{L⁴} intermediate quantity to isolate Hölder loss, (b) compute the strain-vorticity alignment tensor to quantify the geometric factor
- **Why:** Tells us exactly where the 9× geometric slack comes from and whether it's exploitable
- **Source:** Exploration 002 (Section 5.1)
- **Difficulty:** Easy-Medium (extend existing measurement code)

## 7. Higher Re + Longer Time Simulations — NEW (from E002)
- **What:** N=256, Re=1000-5000 to T=15 (turbulent regime) — TGV develops full turbulence only after t≫5
- **Why:** Current data captures only laminar-transitional regime. Slack structure may change qualitatively in fully developed turbulence
- **Source:** Exploration 002 (Section 4.2 caveat)
- **Difficulty:** Medium (computational cost scales as N³·T)

## 8. Adversarial Initial Conditions — NEW (from E002)
- **What:** Search for initial conditions that MINIMIZE the vortex stretching slack ratio (gradient-based optimization or parametric sweeps over vortex tube configurations)
- **Why:** Current 237× is for TGV — adversarial ICs could be much tighter. The minimum over all ICs bounds how tight the bound can actually be.
- **Source:** Strategy mandate (Phase 2); Exploration 002 finding that min slack depends on IC geometry
- **Difficulty:** Hard (optimization in high-dimensional space)
