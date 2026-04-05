# Exploration 007: BMO Norms, Intermittency Calibration, and BKM vs Ladyzhenskaya Advantage

## Mission Context

We have established that the vortex stretching bound in 3D NS has 158-237× slack, with 63% from the Ladyzhenskaya constant looseness. Exploration 006 showed that this looseness is a **statistical property** (NS solutions behave like random-phase fields) — NOT a provable worst-case improvement.

Two remaining tightening paths are live:
1. **BKM advantage:** Our data shows the Agmon inequality has 12× slack vs. Ladyzhenskaya's 158× — meaning the BKM approach to regularity is ~13× tighter for NS flows. This comparison is NOT remarked on in the existing literature. Kozono-Taniuchi (2000) showed that BMO norms give an even tighter criterion than L^∞.
2. **Intermittency:** Bradshaw-Farhat-Grujić (2019) showed spatial intermittency can algebraically reduce the scaling gap. If our NS flows have measurable intermittency, it could explain the C_{L,eff}/C_L ratio.

Your job is to quantify both of these on our DNS data.

## Your Goal

### Part A: BKM vs Ladyzhenskaya — Precise Quantification

Using the Taylor-Green vortex DNS data at Re=100, 500, 1000, 5000 (from exploration 002's solver infrastructure), compute:

1. **At each timestep, the "BKM slack ratio":**
   - Bound: C_{BKM} × ‖ω‖_{L^∞} × (1 + log(1 + ‖ω‖_{H^1}/‖ω‖_{L²})) [the BKM/BW inequality for ‖∇u‖_{L^∞}]
   - Actual: ‖∇u‖_{L^∞}
   - Ratio = Bound/Actual

2. **Compare systematically:**

| Re | Ladyzhenskaya min slack (from E002) | BKM min slack (new) | Ratio (Lad/BKM) |
|---|---|---|---|

3. **The "BKM advantage factor"** = Ladyzhenskaya_slack / BKM_slack at each timestep. Report the time-averaged and minimum values. This directly quantifies how much tighter BKM is than Ladyzhenskaya for NS flows.

### Part B: BMO Norms — The Kozono-Taniuchi Advantage

Kozono-Taniuchi (2000) proved that the blowup criterion for NS can use ‖ω‖_{BMO} instead of ‖ω‖_{L^∞}. Since BMO ⊃ L^∞ (BMO is a larger space), this gives a strictly tighter criterion.

Compute:
1. **‖ω‖_{BMO}** at each timestep for the TGV at Re=100, 500, 1000, 5000.
   - BMO norm: ‖f‖_{BMO} = sup_{B} (1/|B|) ∫_B |f - f_B| dx, where the sup is over all balls B and f_B is the mean of f on B.
   - On T³, compute this by sampling balls of various radii r at various centers, and computing the mean oscillation.
   - Use at least 5 radii (r = L/4, L/8, L/16, L/32, L/64 where L=2π) and 100+ random centers per radius.

2. **The BMO/L^∞ ratio:** ‖ω‖_{BMO}/‖ω‖_{L^∞} at each timestep.
   - If this ratio ≪ 1, it quantifies the Kozono-Taniuchi advantage: BMO-based arguments are tighter by this factor.

3. **Report the table:**

| Re | ‖ω‖_{L^∞} mean | ‖ω‖_{BMO} mean | BMO/L^∞ ratio | Trend with Re |
|---|---|---|---|---|

### Part C: Spatial Intermittency Measures

Compute the following intermittency measures for the vorticity field:

1. **Flatness** F₄ = ‖ω‖⁴_{L⁴} / (‖ω‖²_{L²})² at each timestep.
   - For Gaussian random fields: F₄ = 5/3 ≈ 1.667 (isotropic 3D vector)
   - For intermittent fields: F₄ > 5/3
   - Report F₄ vs time for each Re.

2. **Volume fraction of high-vorticity regions:**
   μ(λ) = Vol({x : |ω(x)| > λ × ‖ω‖_{L^∞}}) / Vol(T³)
   for λ = 0.1, 0.3, 0.5, 0.7, 0.9.
   - If μ(0.5) ≪ 1, vorticity is spatially intermittent.

3. **Effective Ladyzhenskaya constant vs flatness:**
   Plot C_{L,eff} (from exploration 004 data or recomputed) against F₄.
   - Exploration 006 predicted C_{L,eff} ~ F₄^{-1/4} × constant for Gaussian fields.
   - Does this prediction hold for the actual DNS data?

### Part D: Synthesis — "Intermittency-Corrected Enstrophy Bound"

Based on Parts A-C, formulate a **conditional tighter enstrophy bound:**

If the vorticity flatness satisfies F₄ ≤ F_max, then the vortex stretching integral satisfies:

|∫ S_{ij}ω_iω_j dx| ≤ C(F_max) × ‖ω‖^{3/2}_{L²} × ‖∇ω‖^{3/2}_{L²}

where C(F_max) < C²_L for F_max < some threshold.

This would be a **conditional tighter bound** — tighter than the standard Ladyzhenskaya bound when the flatness is bounded. Compute C(F_max) numerically as a function of F_max.

## Existing Code

Use the solver and measurement infrastructure from exploration 002: `../exploration-002/code/`. You'll need to add BMO computation and intermittency measures.

## Output Format

### BKM vs Ladyzhenskaya Table
| Re | Lad min slack | BKM min slack | BKM advantage factor | BMO/L^∞ ratio |
|---|---|---|---|---|

### Intermittency Summary
| Re | F₄ (peak enstrophy) | μ(0.5) | C_{L,eff}/C_L | Predicted C_{L,eff}/C_L from F₄ |
|---|---|---|---|---|

### Candidate Theorem
State the tightest conditional bound your data supports, with numerically determined constants.

## Success Criteria
- BKM slack ratio computed for at least 3 Re values
- BMO norm computed for at least 2 Re values
- Flatness F₄ computed and compared to the Gaussian prediction
- A conditional bound formulation (even rough)
- Assessment of which quantity (BMO, flatness, intermittency) best explains the 158× slack

## Failure Criteria
- No BMO computation attempted
- BKM comparison without systematic Re sweep
- No synthesis connecting the measurements to a potential bound improvement

## Critical Instructions
- Tag all numerical claims with [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED]
- **Part A (BKM comparison) is highest priority** — this is the most promising novel finding
- **Part B (BMO) is computationally the hardest** — the ball sampling may be expensive. If it's too slow at high resolution, use N=32 for BMO and report the resolution limitation.
- Write results incrementally — Part A first, then B, then C, then D.

## File Paths
- Existing code: ../exploration-002/code/
- Your code: code/ (create this directory)
- Report: REPORT.md
- Summary: REPORT-SUMMARY.md
