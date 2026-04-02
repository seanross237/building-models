# Exploration History

---

## Exploration 001: QD↔HQEC Literature Search (Exploration A)

**Verdict: HIGH CONFIDENCE NOVELTY**

The QD↔HQEC connection is not published. 24+ keyword searches, 15 specific papers examined. Zero papers found connecting Zurek's R_δ to entanglement wedge reconstruction or the RT formula. Zurek's 2022 comprehensive review does not mention AdS/CFT. HaPPY paper does not mention QD/pointer states.

**Formal mapping (5 entries formally correct, 3 approximate):**
- Fragment↔Subregion: formally exact
- "Fragment knows S" (I(S:F_k)≥(1-δ)H_S) ↔ x∈W(R_k): formally exact (sourced from HQEC theorem)
- Fragment entropy↔RT formula: formally exact (RT 2006)
- Redundancy formula R_δ ≤ S_max/S_T: rigorously derivable from RT + HQEC + subadditivity
- APPROXIMATE: pointer states (QD requires einselection; HQEC is basis-independent), S_T identification (local bulk Hilbert space dim depends on cutoff), δ-threshold (binary in HQEC vs continuous in QD)

**5 structural gaps identified:**
1. Pointer states: no holographic analogue of einselection mechanism
2. Planck scale: both frameworks break down
3. δ-threshold: HQEC is binary, QD uses continuous δ; requires approximate QEC
4. Dynamics: QD is temporal; HQEC is a static code
5. Excited states: HQEC has phase transitions (Page transition) that break continuous QD picture

**Unexpected finding:** HaPPY code achieves EXACTLY 50% of classicality budget maximum — R_δ = S_max/(2·S_T) — because perfect tensors have threshold at exactly half the boundary. This is the cleanest quantitative prediction of the framework.

**Adjacent work:** Ferté & Cao (2023) on QD encoding phase transitions; "Ensemble Projection Hypothesis" (AJMP 2026) loosely mentions Zurek+holography without formalizing.

**Computations flagged:** (1) Verify R_δ = S_max/(2·S_T) for HaPPY code numerically via tensor contraction; (2) Extend to random tensor network models.

---

## Exploration 002: BH Universal Constants Literature Verification (Exploration B)

**Verdict: NOT PUBLISHED**

All three constants are new. 18 papers examined, all 11 required search queries run.

| Constant | Verdict |
|----------|---------|
| S = 1/(540 ln2) ≈ 0.002672 bits | NOT PUBLISHED — specific search returns zero results |
| ⟨N⟩ = ζ(3)/(24π⁴) ≈ 5.14×10⁻⁴ | NOT PUBLISHED — Gray et al. (2016) use ζ(3) for rates, not occupation number |
| R_1bit = 7.21 r_s | NOT PUBLISHED — "classicality horizon" concept absent from BH literature |
| T_H × r_s = ħc/(4πk_B) | IMPLICITLY KNOWN, NOT NAMED — present in every BH paper but never isolated |

**Character of novelty:** "Overlooked 5-line calculation from fully known ingredients." The algebraic cancellation (all π factors cancel, 540=9×60 emerges cleanly) makes it surprising this went unnoticed.

**Closest prior work:**
- Kim (arXiv:2112.01931): entropy of Hawking radiation in spherical box near BH — curved-space calculation at R≥3r_s, different from naive flat-space 1/(540 ln2)
- Gray et al. (arXiv:1506.03975): uses ζ(3) in emission rate formula — closely related but differs by geometric factor + (flux vs volume)
- arXiv:2407.21114: shows T=1/(4πr+) explicitly, establishing T_H×r_s identity

**Unexpected findings:**
- 1/540 = 1/(9×60): the 60 from Stefan-Boltzmann, the 1/9 from geometry — all π factors cancel exactly
- Giddings "atmospheric radius" R_a ≈ 2.68 r_s (luminosity matching) is a different scale from R_1bit = 7.21 r_s — distinct physics

**Computation flagged:** Curved-space correction to 1/(540 ln2) using Page's stress tensor at r_s (vs naive flat-space blackbody). ~50-100 lines scipy.

---

## Exploration 003: Experimental Test Proposal (Exploration C) — PARTIAL SUCCESS (exceeds criteria)

**Three systems in non-trivially constraining regime [COMPUTED]:**

| System | S_eff (bits) | R_max | Status |
|--------|-------------|-------|--------|
| 20-ion trap, n̄=0.01 | 4.86 | 3.86 | TIGHT (< 10) |
| GaAs nanodot 10nm, 4K | 10.25 | 9.25 | TIGHT (< 10) |
| 50-ion trap, n̄=0.1 | 72.5 | 71.5 | CONSTRAINED |
| BEC sonic horizon, L=100μm | 474.9 | 473.9 | CONSTRAINED |

**Key finding:** 20-ion trap at n̄ ~ 0.003 (achievable with current ground-state cooling): R_max < 0 — classicality budget FORBIDS redundant copies. Tuning n̄ from 0.01 to 0.001 produces a **classicality phase transition** at n̄_c ≈ 0.003. Measurable via mutual information tomography with current quantum hardware.

**Concrete protocol:** Prepare 1-qubit system ion + N−1 sideband-cooled environment ions. Tune n̄. Measure I(S:F_k) for ~10 motional mode fragments. Check R_obs ≤ R_max(n̄).

**Unexpected findings:**
1. Inflation Hubble patch: R_max = −0.979, same as BH horizon. Both are de Sitter; formula "knows" they're equivalent.
2. Below n̄ ~ 0.001, classicality is forbidden in a 20-ion trap — achievable today.
3. Nanodot 10nm: Bekenstein bound S_Bek = 0.23 bits < 1 bit at 4K (Bekenstein doesn't apply for photon-energy-dominated case).

**Computations flagged:** Critical n̄_c analytic solution; optimal fragment partition; dynamical Lindblad simulation of QD in ion trap.

---

## Exploration 004: Island Formula and Page Transition (Exploration D) — SUCCESS

**Two distinct classicality transitions [COMPUTED]:**

1. **Exterior transition at t_classical ≈ (2/S_BH)·t_Page**: Hawking radiation accumulates 1 bit → exterior QD-classical. For solar BH: t_class/t_Page = 2×10^{-77} — nearly instant.

2. **Interior transition at t = t_Page**: Island appears. R_δ_int has **discontinuous jump** from −1 to S_BH/2−1 — a quantum phase transition.

**Verdict on novelty [CONJECTURED]:** "Page-time classicality transition" for interior operators is a restatement of known HQEC/entanglement-wedge result in QD language. What QD adds: quantitative R_δ budget, two-stage structure as organizing principle, measurement-theoretic criterion for "classical observability."

**Unexpected findings:**
- CFT model: Page time is exponentially early (t_Page ≪ t_evap/2) for large S_BH
- Interior R_δ jump is DISCONTINUOUS — replica geometry phase transition

---
