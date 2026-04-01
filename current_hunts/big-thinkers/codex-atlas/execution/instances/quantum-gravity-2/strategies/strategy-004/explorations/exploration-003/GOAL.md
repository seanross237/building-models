# Exploration 003: Inflation — Sharpened Predictions from NGFP Constraint

## Mission Context

The Unified QG+F–AS Framework predicts Starobinsky inflation from the R² term. Both frameworks give r ≈ 0.003, so r alone doesn't discriminate. But there's a tension: current CMB+DESI data give n_s = 0.9737 ± 0.0025, which is 2.3σ above the standard Starobinsky prediction of n_s ≈ 0.967. The unified framework has TWO potential resolution paths:
1. The NGFP logarithmic correction parameter b shifts n_s upward (Bonanno-Platania)
2. The R³ six-derivative extension from the NGFP truncation hierarchy shifts n_s upward

If the unified framework can PREDICT the correct n_s from first principles (not as a free parameter), that would be a genuine discriminating prediction testable by LiteBIRD (~2036).

## Your Task

**One question:** Can the unified framework's NGFP predict specific values for the inflationary correction parameters b and/or δ₃, and do these values resolve the n_s tension?

## What You Must Deliver

### Part A: Derive b from NGFP Critical Exponents

The Bonanno-Platania formula is:
```
L_eff = M_P² R/2 + (a/2) R²/[1 + b ln(R/μ²)]
```

The claim is: b ~ θ/(16π²) ~ O(10⁻²), where θ are NGFP critical exponents.

**Your job:**
1. Find the derivation of this b ~ θ/(16π²) relation. Is it a proper derivation or an estimate?
2. Use the specific NGFP critical exponents from multiple truncations:
   - Einstein-Hilbert: θ = 1.55 ± 3.83i
   - R² truncation: θ₁ = 2.38, θ₂,₃ = 1.26 ± 2.74i
   - Full 4th-order (Benedetti et al.): θ₀ = 2.51, θ₁ = 1.69, θ₂ = 8.40, θ₃ = -2.11
3. Compute b for each truncation. What is the spread? Is there convergence?
4. For each b value, compute the resulting n_s and r using:
   - n_s = 1 - 2/N_eff where N_eff is modified by b
   - r = 3(1 - β/(6α))(n_s - 1)²/(1 + b ln(R/μ²))
5. Does the predicted b resolve the n_s tension? Is b = 0 or b ~ 10⁻² the unified prediction?

### Part B: Six-Derivative δ₃ from NGFP Truncation Hierarchy

The R³ correction δ₃ ≈ -1.19 × 10⁻⁴ resolves the n_s tension (giving n_s ≈ 0.974). The unified framework claims this should emerge from the NGFP at the six-derivative truncation level.

**Your job:**
1. Search for published NGFP calculations at six-derivative (R³) truncation level:
   - Falls, Litim, Schröder 2019 (PRD 99, 126015): computed fixed-point values for R³ term
   - Knorr, Ripken, Saueressig 2019: six-derivative FRG
   - Codello, D'Odorico, Pagani: f(R) to high polynomial order
2. Extract the NGFP fixed-point value for the R³ coupling
3. Map it to δ₃ in the notation of the six-derivative QG+F extension
4. Compare: does the NGFP-predicted δ₃ match the δ₃ ≈ -1.19 × 10⁻⁴ needed for n_s tension resolution?
5. If yes: this is a STRONG discriminating prediction. If no: quantify the disagreement.

### Part C: Classification

For EACH prediction derived, classify as:
- DISCRIMINATING: distinguishes unified from compatible-but-separate
- NOVEL: neither QG+F alone nor AS alone predicts this
- CONSISTENCY CHECK: true for unified, also true for separate
- INHERITED: predicted by one or both standalone

**Key discrimination test:** In standalone QG+F, b = 0 and δ₃ is a free parameter. In standalone AS, b is undetermined (depends on truncation). In the unified theory, b and δ₃ are BOTH determined by the NGFP. If the NGFP-determined values agree with observation, the prediction is DISCRIMINATING. If they're free in both standalone frameworks, it's only NOVEL if the unified theory fixes them.

## Pre-loaded Context

**QG+F inflation:**
- r ∈ [0.0004, 0.0035], n_s ≈ 0.967 (N = 60)
- Bianchi-Gamonal 2025: r ≈ 3(1 - β/(6α))(n_s - 1)²
- β > 0 from C² systematically reduces r
- n_s determined by R² alone; C² fakeon does NOT shift it
- R³ (six-derivative) correction: δ₃ ≈ -1.19×10⁻⁴ gives n_s ≈ 0.974, r ≈ 0.0045
- δ₃ must be TREE-LEVEL (loop-generated is 6 orders too small)

**AS inflation:**
- Codello et al. 2014: R² from NGFP gives Starobinsky, r ≈ 0.003
- Bonanno-Platania: logarithmic NGFP corrections via b parameter. b = 0: pure Starobinsky. b ~ 10⁻²: r up to 0.01, n_s up to 0.975
- b is NOT uniquely determined by AS alone — depends on truncation
- Most AS models cluster near r ≈ 0.003 with b ≈ 0

**Observational timeline:**
- LiteBIRD: σ(r) < 10⁻³, launch 2032, results ~2036-2037
- Simons Observatory enhanced: σ(r) ~ 0.001, ~2034
- DESI DR3: improved BAO → tighter n_s constraint by ~2027

## Failure Path

If you find that b and δ₃ CANNOT be computed from the NGFP (e.g., they depend on truncation-dependent quantities that haven't converged):
1. State clearly what quantity blocks the computation
2. Give the RANGE of b and δ₃ across available truncations
3. Assess: is this a "prediction" or just a "parameter window"?
4. If just a window: does the unified framework at least NARROW the window compared to standalone QG+F (where δ₃ is completely free)?

## Output

Write findings to:
- `explorations/exploration-003/REPORT.md` (200-400 lines)
- `explorations/exploration-003/REPORT-SUMMARY.md` (30-50 lines, write LAST)
