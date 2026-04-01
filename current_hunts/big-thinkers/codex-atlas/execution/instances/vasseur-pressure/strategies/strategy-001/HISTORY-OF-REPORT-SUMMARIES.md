# Exploration History

## Exploration 001: Extract the Precise Definition of Beta from Vasseur (2007)

### Goal
Extract the precise mathematical definition of the pressure exponent β from Vasseur's De Giorgi iteration framework for Navier-Stokes regularity.

### Outcome: SUCCESS — All 7 deliverables answered with equation-level precision.

### Key Takeaway

**β is NOT a pressure integrability exponent.** It is the nonlinear recurrence exponent in the De Giorgi level-set iteration. Specifically, Vasseur's Proposition 3 gives:

`U_k ≤ C_p^k (1 + ||P||_{Lp(L1)}) U_{k-1}^{β_p}`

where U_k measures energy on level sets v_k = [|u| - (1-2^{-k})]_+. If β > 3/2, ALL suitable weak solutions are regular (Conjecture 14 + Appendix proof). Current best: β < 4/3 (strictly), from a single term — the non-divergence part of the local pressure P_k^{21}. All other terms (transport, nonlocal pressure, local pressure in divergence form) exceed 3/2. The gap to close is > 1/6.

The bottleneck is: ∫|P_k^{21}| · |d_k| · 1_{v_k>0} dx dt, where P_k^{21} is bounded in all L^q by CZ theory independently of U_{k-1}. This "constant" bound (not depending on the level set energy) is what kills the exponent — the pressure doesn't get small even when the velocity is near its truncation level.

### DNS Computability: PARTIALLY computable
U_k, the pressure decomposition, and the bottleneck integral are all computable on periodic grids. The empirical β can be extracted by fitting the recurrence for k = 0,...,~12. Main adaptation: replace nested balls with periodic domain. Main limitation: single-flow non-universality.

### Unexpected Findings
The CZ slack measured earlier (7.6-17.5×) is on the FULL pressure, but the bottleneck involves P_k^{21} — a specific piece of the decomposed pressure involving u(1-v_k/|u|), which is bounded by 1. If CZ slack persists for this specific piece, the empirical β could significantly exceed 4/3.

### Computations Identified
1. **Empirical β measurement from DNS** — compute U_k for k=0,...,12 on Taylor-Green and anti-parallel tube flows, fit recurrence exponent. ~100 lines Python/spectral. Would reveal whether β > 4/3 or even > 3/2 empirically.
2. **CZ slack on P_k^{21} specifically** — decompose DNS pressure into the De Giorgi local/nonlocal pieces and measure CZ tightness on each piece separately. ~150 lines. Would identify whether the slack is in the bottleneck term or elsewhere.

---

## Exploration 004: CZ Slack on De Giorgi Pressure Decomposition

### Goal
Determine whether the CZ slack for the De Giorgi bottleneck piece P_k^{21} depends on the iteration depth k, which would directly improve the recurrence exponent beta beyond 4/3.

### Outcome: SUCCESS (NEGATIVE RESULT)

### Key Takeaway

**The CZ slack for P_k^{21} is k-INDEPENDENT.** The tightness ratio converges to a constant by k ~ 3-4 and shows no systematic improvement with iteration depth. The hypothesis that CZ slack could improve beta is falsified.

Specifically at q=2: P21 tightness converges to IC-dependent constants (TGV: ~0.40, AP: ~0.58, RG: ~0.26) that are stable across k. At higher q (4, 6, 8), the same pattern holds with greater slack but the same k-independence.

**P21 has LESS CZ slack than the full pressure** (1.7-3.9× at q=2 vs 7.6-17.5× for full pressure). The bottleneck piece is actually HARDER to improve via CZ arguments — it saturates the CZ bound more than the overall pressure does.

Results are virtually Re-independent (<0.5% variation), suggesting CZ tightness is a structural/topological property, not a viscous dynamics effect.

### What This Rules Out
The "CZ slack improves beta" path is closed. The CZ bound on P_k^{21} already captures the correct scaling — the constant C_q has numerical slack, but this slack doesn't grow with k.

### What This Does NOT Rule Out
1. Structural bounds beyond CZ (div-curl estimates exploiting u_below bounded + divergence-free)
2. Cancellation between pressure pieces (treating P21+P22+P23 jointly)
3. Alternative velocity splittings (adapted thresholds)
4. Other bottleneck paths (Chebyshev, interpolation, energy inequality manipulation)

### Verification
- Decomposition exact to 1e-15 [VERIFIED]
- N=64 vs N=128 convergence: <0.2% deviation [VERIFIED]
- All tightness measurements [COMPUTED]

---

## Exploration 003: Tran-Yu on Galilean Invariance and Pressure

### Goal
Assess whether Tran-Yu's use of Galilean invariance for pressure improvement can improve Vasseur's De Giorgi recurrence exponent beta beyond 4/3.

### Outcome: SUCCESS — Grade (C): Not applicable to the De Giorgi bottleneck.

### Key Takeaway

**The Tran-Yu program operates in a fundamentally different framework (global L^q energy) than Vasseur's De Giorgi iteration (local level-set energy on nested balls).** The two frameworks have different pressure objects, different energy functionals, and different iteration structures.

Most critically: **the pressure Poisson equation is Galilean-invariant for divergence-free flows.** A constant frame shift u → u - u_0 does NOT change the CZ norm of the pressure at all, because the cross-terms vanish exactly when div u = 0. The Tran-Yu improvement comes from reducing the *velocity factor* in the L^q energy estimate (better constant), not from improving the pressure bound (which is impossible via Galilean boost).

The Tran-Yu program (5 papers, 2015-2021) provides:
- Better constant via frame shift: YES (modest)
- Better exponent: NO
- Structural improvement to De Giorgi bottleneck P_k^{21}: NO

Three structural reasons the approach can't be inserted into De Giorgi:
1. Different energy functionals (global L^q vs local level-set U_k)
2. Different pressure objects (full pressure p vs decomposed P_k^{21})
3. CZ bound on P_k^{21} unchanged by Galilean boost (source bounded by 1 regardless of frame)

### Unexpected Findings
1. **Choi-Vasseur (2014, AIHP)** introduces a three-way pressure decomposition P = P_1k + P_2k + P_3 that absorbs the "bad" non-divergence pressure term P_3 into the velocity equation. This is a different and potentially more relevant approach to the P_k^{21} bottleneck than anything in Tran-Yu.
2. **arXiv:2501.18402** — "Dynamic Refinement of Pressure Decomposition" (January 2025). Very recent, directly relevant to pressure decomposition improvements.
3. Tran-Yu's velocity-pressure anti-correlation (Bernoulli-type) might explain why empirical CZ bounds on P_k^{21} could be tighter than worst-case.

### Leads Identified
- The Choi-Vasseur (2014) alternative decomposition that absorbs P_3
- Dynamic refinement approach (arXiv:2501.18402)
- Velocity-pressure anti-correlation as explanation for DNS slack

---

## Exploration 002: Empirical Beta from DNS via De Giorgi Iteration

### Goal
Measure the De Giorgi recurrence exponent beta_effective on 3D NS DNS across 5 ICs × 3-4 Re values. Determine whether beta > 4/3 (analytical slack) or beta ≤ 4/3 (gap is genuine).

### Outcome: INCONCLUSIVE-TO-NEGATIVE — All beta_eff < 4/3. Branch determination: Path B.

### Key Takeaway

**All 21 DNS cases yield beta_eff < 4/3**, ranging from 0.35 (random Gaussian) to 1.01 (ABC at Re=1000). The more directly comparable **bottleneck exponent** gamma (measuring the pressure integral I_k ~ U_{k-1}^gamma):
- gamma > 4/3 ONLY for smoothest flows (laminar, Re=100)
- gamma DECREASES with Re for ALL ICs
- At Re ≥ 500, gamma drops to 0.5-0.6 for turbulent ICs

This suggests the 4/3 analytical bound is close to sharp for general turbulent flows.

**Important caveat (from explorer):** Empirical beta_eff and Vasseur's analytical beta_p are DIFFERENT quantities. beta_eff < 4/3 on smooth DNS solutions doesn't prove the bound is tight — smooth solutions decay faster than the De Giorgi geometric rate regardless. The bottleneck exponent is more directly comparable.

### Results Table (selected)

| IC | Re | beta_eff | std_err | BN_exp (gamma) |
|---|---|---|---|---|
| ABC | 1000 | **1.009** | 0.008 | 1.103 |
| ABC | 500 | 0.983 | 0.021 | 1.146 |
| VortexTubes | 1000 | 0.730 | 0.115 | 1.154 |
| TaylorGreen | 100 | 0.737 | 0.108 | **1.403** |
| RandomGauss | 1000 | 0.386 | 0.072 | 0.618 |

### ABC (Beltrami) Flow is Special
- beta_eff INCREASES toward 1.0 with Re (0.90 → 0.98 → 1.01)
- Best R² values (0.983 → 0.999) — recurrence model fits perfectly
- Bottleneck gamma stays > 1.0 at all Re
- The Beltrami property (curl u = u) provides genuine analytical leverage

### Convergence
ABC results converge excellently (N=64 vs N=128 differ by <2%). TG has modest resolution dependence but qualitative picture unchanged.

### Leads Identified
1. **Conditional regularity via Beltrami-near structure** — ABC's favorable scaling suggests a conditional result exploiting velocity-vorticity alignment
2. **Refined De Giorgi functional** — modifying d_k² to remove non-monotone threshold term
3. **Pressure structure at turbulent scales** — gamma saturates at Re ~ 500-1000

---

## Exploration 005: Choi-Vasseur (2014) Alternative Decomposition and Post-2007 Landscape

### Goal
Determine whether alternative pressure decompositions improve beta beyond 4/3, and survey the broader post-2007 De Giorgi landscape.

### Outcome: SUCCESS — Clear negative result. Beta = 4/3 barrier UNTOUCHED since 2007.

### Key Takeaway

**No paper since Vasseur (2007) has improved beta beyond 4/3.** The barrier is untouched and the community has moved orthogonally.

**Choi-Vasseur (2014)** introduces P = P_{1,k} + P_{2,k} + P_3 where P_3 (k-independent, from outer cutoff derivatives) is absorbed into the velocity equation via a time-dependent truncation level E_k(t). The trick: E_k rises by the accumulated ∇P_3, and the resulting sign is favorable (Eq. 47). This removes P_3 entirely from the energy inequality. However:
- Achieved exponent is only beta = 7/6 (WEAKER than 4/3) — explicitly noted as "not optimal" but sufficient for their purpose (fractional higher derivative integrability)
- The P_k^{21} bottleneck lives inside P_{2,k}, which CV14 don't further decompose
- The three-way decomposition does NOT bypass the fundamental bottleneck

**arXiv:2501.18402** (Fernandez-Dalgo 2025) uses dynamic pressure decomposition in paraboloid geometry for epsilon-regularity. Uses Gronwall methods, NOT De Giorgi iteration. Does not address beta at all.

### Post-2007 Landscape (13 papers surveyed)
The literature divides into:
1. Higher regularity via De Giorgi (accepting beta < 4/3): Vasseur 2010, CV14, Vasseur-Yang 2021
2. Alternative frameworks (not De Giorgi): Colombo-De Lellis, Barker-Prange, Lei-Ren
3. Extensions to other equations: hyperdissipative NS, nonlocal operators

**Nobody is directly attacking beta > 4/3.** The community implicitly treats this as a hard open problem.

### Leads Identified
1. **Vasseur-Yang (2021):** De Giorgi on the VORTICITY equation, avoiding pressure entirely. Different attack that might circumvent P_k^{21} bottleneck.
2. **P_3 absorption trick extensibility:** Could more terms be absorbed via time-dependent truncation levels?
3. **Routes to improve beta (interpretation):** Exploit cancellations in source quadratic structure, use regularity of source beyond CZ, change test function, or avoid pressure entirely (vorticity approach)

---

## Exploration 006: Beltrami-Near Structure and Geometric Conditional Regularity

### Goal
Survey geometric regularity criteria for NS exploiting velocity-vorticity alignment. Determine whether Beltrami-near structure can improve De Giorgi exponent β.

### Outcome: SUCCESS — Grade (B): Promising but needs work.

### Key Takeaway

**The mechanism is identified and verified.** For exact Beltrami flows (curl u = λu):
- Lamb vector L = ω × u = 0 identically
- Nonlinear advection u·∇u = ∇(|u|²/2) is a pure gradient
- Pressure p = −|u|²/2 + const — a pointwise Bernoulli function, NO CZ inversion needed
- The pressure Poisson source is a pure Hessian → CZ "loss" is zero

This fully explains ABC's beta_eff ≈ 1.0 (exploration 002).

**For near-Beltrami flows** (u = u_B + εv), the "bad" pressure requiring CZ bounds enters at O(ε). The degradation is continuous and linear. The pressure source decomposes as:
- Hessian piece Δ(|u|²/2): CZ-lossless, exact inversion
- Lamb vector piece div(L): O(ε), CZ-lossy — this is the piece that generates the bottleneck

**Main obstacle:** De Giorgi truncation u_below breaks Beltrami property — even when u is Beltrami, u_below = u·min(1, λ_k/|u|) is NOT Beltrami. Need to quantify how much structure survives in u_below.

### Geometric Regularity Literature
- Constantin-Fefferman (1993): Lipschitz direction of ω → regularity
- Beirao da Veiga-Berselli (2002): Hölder-1/2 direction of ω → regularity
- Vasseur (2007): Direction of u conditions → regularity
- **No existing paper connects these geometric criteria to De Giorgi iteration** — this is unexplored territory and could be novel

### Leads Identified
1. **Hessian/Lamb decomposition of P_k^{21}**: Split bottleneck pressure into CZ-lossless Hessian piece and CZ-lossy Lamb piece. Measure on DNS.
2. **Beltrami deficit of u_below**: Compute B(u_below) = ||curl(u_below) − λu_below||/||u_below|| vs k on ABC DNS data. Determines if truncation preserves structure.
3. **Novel conditional result**: "If Beltrami deficit B(u) < ε₀, then β > 3/2" — no existing paper formulates this.

### Unexpected Findings
- Exact Beltrami on T³: u(t) = u₀ exp(−νλ²t) — exponential decay preserving spatial structure, trivially regular
- Gap: beta_eff ≈ 1.0 (ABC) still below 3/2 — Beltrami structure alone is insufficient, must combine with something else

---

## Exploration 008: Vasseur-Yang (2021) Vorticity-Based De Giorgi

### Goal
Determine whether Vasseur-Yang's vorticity-based De Giorgi avoids the pressure bottleneck limiting β < 4/3.

### Outcome: SUCCESS — Grade C (Instructive negative result). The 4/3 barrier is UNIVERSAL.

### Key Takeaway

**The pressure is genuinely eliminated.** Vasseur-Yang introduce v = −curl φ♯Δ⁻¹φ ω, a localized minus-one-derivative of vorticity, satisfying a pressure-free evolution equation. De Giorgi iteration on v proves |v| ≤ 1 under smallness conditions.

**However, a new 4/3 bottleneck appears.** The recurrence is U_k ≤ C^k U_{k-1}^{min{4/3, 5/3 − 2/(3p₃)}}. The 4/3 comes NOT from pressure but from the interior trilinear form:

- ‖∇(β_k v)‖_{L²} costs U_{k-1}^{1/2} (one derivative)
- Two nonlinear v factors at truncation level cost U_{k-1}^{5/6}
- Total: 1/2 + 5/6 = **4/3**

**The 4/3 barrier is universal for De Giorgi iterations on NS — NOT specific to pressure.** When pressure is removed, the same 4/3 reappears from the trilinear nonlinearity. This strongly suggests no reformulation preserving quadratic nonlinearity will break the barrier.

### Comparison Table

| Feature | Velocity (Vasseur 2007) | Vorticity (Vasseur-Yang 2021) |
|---|---|---|
| Bottleneck term | P_k^{21} (pressure) | Trilinear form T_∇ (nonlinearity) |
| β achieved | < 4/3 | ≤ 4/3 |
| β needed | > 3/2 (unconditional) | > 1 (conditional, small U₀) |
| Source of 4/3 | CZ gives k-independent bound | ∇ costs U^{1/2}, cubic gives U^{5/6} |

The iteration still closes (β > 1 suffices for their purpose) because blow-up scaling gives small U₀. This gives improved Lorentz regularity but NOT unconditional global regularity.

### Beltrami Connection
For exact Beltrami: the trilinear form simplifies (Lamb vector = 0, stretching = pure gradient). Same favorable properties as velocity approach. For near-Beltrami: trilinear bottleneck enters at O(ε²) — even more favorable than the velocity approach where the bad pressure enters at O(ε).

### Mission Reframing
The target should not be "avoid pressure" or "improve CZ" but rather "break the derivative-vs-nonlinearity tradeoff" (1/2 + 5/6 = 4/3). This is the irreducible structural origin of the barrier.

---

## Exploration 007: Beltrami Deficit of u_below + Hessian/Lamb Decomposition

### Goal
Determine whether the Beltrami mechanism (from E006) survives the De Giorgi truncation u_below = u·min(1, λ_k/|u|).

### Outcome: SUCCESS — Mechanism SURVIVES.

### Key Results

**Task A — Beltrami deficit:**
- ABC: B_k ≈ 0.56 × 2^{-k} — deficit vanishes GEOMETRICALLY with k
- Controls (TG, RG): B_k ≈ B_full ≈ 3-12 (constant, large)
- λ_opt = -1.000 at all k for ABC (matching exact curl eigenvalue)
- All ABC results are Re-independent (self-similar decay, L∞-normalized pattern invariant)

**Task B — Pressure decomposition (Bernoulli + remainder):**
- ABC at k=4: remainder fraction R_frac = 3.7%, bottleneck contribution I_r/I_t = 4.4%
- ABC at k=8: R_frac = 0.04%, I_r/I_t = 0.2%
- Controls: R_frac > 1 (remainder EXCEEDS total due to massive cancellation)

**The money table:**

| IC | R_frac k=4 | I_r/I_t k=4 | R_frac k=8 | I_r/I_t k=8 |
|---|---|---|---|---|
| **ABC** | **0.037** | **0.044** | **0.0004** | **0.002** |
| TG Re=500 | 1.180 | 0.53 | 1.179 | 0.63 |
| RG Re=500 | 1.542 | 11.06 | 1.542 | 9.07 |

### Unexpected Findings
- Truncation breaks div-free: div(u_below) ≠ 0, scaling as O(2^{-k}). Invalidates standard Hessian/Lamb identity. Two-way Bernoulli/remainder split is the correct approach.
- Sign error in prior code (E002/E004) — doesn't affect |P| measurements but matters for signed decompositions. Caught and corrected.
- Even without div-free structure, pressure remains Bernoulli-dominated for ABC. The Beltrami property provides enough geometric structure.

### Proof Gaps
- O(2^{-k}) scaling of B_k is computed, not proved analytically
- Connection from "small remainder fraction" to "improved β_eff" needs rigorous CZ-split argument

### Implications
For Beltrami flows: the CZ bottleneck is effectively removed from De Giorgi iteration. β_eff can approach the geometric limit (~5/3) rather than being CZ-capped at 4/3. For generic flows: full CZ loss applies. The mechanism is Re-independent.

---

## Exploration 010: Perturbed-ABC Near-Beltrami Test + Leray Projection

### Goal
Test whether the Beltrami-De Giorgi mechanism extends to near-Beltrami flows (addresses E009 adversarial review weakest link).

### Outcome: Mechanism does NOT generalize (critical negative result).

### Key Results

**B_k decay LOST for any ε > 0:**
| ε | B(k=2) | B(k=8) | B(k=8)/B(k=2) | Trend |
|---|---|---|---|---|
| 0.00 | 0.137 | 0.001 | 0.006 | Exponential decay |
| 0.01 | 0.149 | 0.063 | 0.42 | Decays then PLATEAUS |
| 0.05 | 0.346 | 0.324 | 0.94 | Nearly flat |
| 0.10 | 0.675 | 0.675 | 1.00 | Flat |

**β_eff degrades continuously:**
| ε | β_eff | Mechanism works? |
|---|---|---|
| 0.00 | 1.009 | Yes (exact eigenstate) |
| 0.01 | 1.067 | Marginal |
| 0.05 | 0.888 | No (β < 1) |
| 0.20 | 0.585 | No |
| 0.50 | 0.278 | No |

β > 1 threshold crossed at ε ≈ 0.02 — flow must be >98% Beltrami.

**Leray projection:** Minor correction (~16% at k=1, <1% at k≥5). Qualitative picture preserved. Resolves div(u_below) ≠ 0 issue from E007.

**Physical explanation:** For exact Beltrami, the Lamb vector is zero EVERYWHERE. Truncation only perturbs the clipping boundary (shrinks with k). For near-Beltrami, the Lamb vector is nonzero at ALL velocity magnitudes — truncation cannot remove it, so B_k → B_full.

**Viscous evolution** improves Beltrami alignment (B_full drops ~50% over T=2.0) but not enough to restore B_k decay.

### Implications for the Strategy
The Beltrami-De Giorgi connection is real but specific to exact Beltrami (measure-zero). Cannot be used for conditional regularity of generic flows. The >98% Beltrami threshold makes it physically irrelevant for turbulence.

---

## Exploration 009: Adversarial Review + Final Synthesis

### Goal
Stress-test all 6 major claims from explorations 001-008. Identify novel contributions and weaknesses.

### Outcome: SUCCESS — All claims reviewed. Significant weaknesses identified.

### Grades

| Claim | Grade | Strongest Attack | Novelty |
|---|---|---|---|
| 1. 4/3 universal | B | Induction from 2 cases, not theorem | Partially novel |
| 2. CZ slack k-independent | C+ | Wrong regime (smooth solutions) | Novel |
| 3. beta_eff < 4/3 | C | DNS smooth = tautology | Novel methodology |
| 4. Beltrami = no CZ loss | B+ | Trivial regularity of exact Beltrami | Partially novel |
| 5. Truncation preserves B | C+ | Trivial for smooth, unproven for near-B | Novel (but trivial) |
| 6. Gap is genuine | C+ | Category error: smooth ≠ near-singular | Partially novel |

### Strongest Finding
**The Beltrami-De Giorgi connection (Claims 4+5):** Lamb vector L = ω × u generates the CZ-lossy piece of the De Giorgi pressure. L=0 (Beltrami) eliminates CZ loss. This connects flow geometry to the analytical bottleneck in a way no published paper does. Novel synthesis of known components.

### Biggest Weakness
**Smooth-solution limitation.** Claims 2, 3, 6 rely on DNS of smooth solutions, but De Giorgi operates on near-singular solutions. DNS cannot diagnose tightness in the relevant regime.

### Weakest Link: Claim 5
- B_k = O(2^{-k}) for exact Beltrami is trivial (smooth truncation on smooth functions)
- Doesn't address near-Beltrami (the only interesting case)
- div(u_below) ≠ 0 unresolved
- Missing connection from small B_k to improved β

### Novel Claims Identified
1. **Beltrami-De Giorgi connection** — Lamb=0 eliminates CZ loss in De Giorgi pressure. Novel synthesis.
2. **Computational De Giorgi methodology** — extracting U_k, γ, CZ ratios from DNS. Novel methodology.
3. **Dual-mechanism universality of 4/3** — CZ loss in velocity AND derivative-nonlinearity in vorticity both give 4/3. Novel framing.

### Strategy-002 Recommendations
1. Make Beltrami-De Giorgi connection rigorous (analytical Lamb-vector bound on β)
2. Abandon DNS tightness program (fundamental smooth-solution limitation)
3. Investigate near-Beltrami behavior of u_below for generic turbulent flows
4. Use vorticity formulation (Vasseur-Yang 2021) as better vehicle — Lamb enters at O(ε²)
