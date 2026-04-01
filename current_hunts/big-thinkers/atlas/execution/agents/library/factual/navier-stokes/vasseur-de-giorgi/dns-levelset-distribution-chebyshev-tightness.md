---
topic: DNS level-set distribution tails and De Giorgi Chebyshev tightness ratios
confidence: computed
date: 2026-03-30
source: "vasseur-pressure s2-exploration-002; DNS pseudo-spectral on T^3, N=128 (primary), N=64 (verification)"
---

## Main Findings

### 1. Velocity Distribution Tail Exponents Are IC-Dependent

The tail of the velocity distribution mu(lambda) = |{x : |u(x,t)| > lambda}| / |Omega| follows approximate power-law mu ~ lambda^{-p}, with exponent p depending critically on flow structure:

| IC type | p (fitted) | p - 10/3 | R^2 | Interpretation |
|---------|-----------|----------|-----|----------------|
| Taylor-Green | ~10 | +6.6 | 0.79 | Isolated velocity peaks; massive Chebyshev slack |
| Random Gaussian (k^{-5/3}) | ~8-9 | +5.0 | 0.95 | Localized peaks; significant slack; cleanest power-law |
| ABC Beltrami | ~2.1 | **-1.3** | 0.53 | Uniform |u| distribution (curl u = u); Chebyshev is TIGHT or OPTIMISTIC |

**Critical result: ABC Beltrami flow has p < 10/3.** The Chebyshev bound mu(lambda) <= lambda^{-10/3} ||u||_{10/3}^{10/3} is approximately tight (or even optimistic) for Beltrami tails. This means Chebyshev slack is NOT universal across NS solutions — it depends on flow geometry.

### 2. De Giorgi Chebyshev Tightness Ratios Are ~3-5x and k-Independent

The ratio (Chebyshev bound on |{v_{k-1} > 2^{-k}}|) / (actual |{v_{k-1} > 2^{-k}}|) was measured across all ICs and De Giorgi levels k=1..8:

| IC | Typical ratio | k-dependence | Fit: ratio ~ C^k |
|----|--------------|--------------|-------------------|
| Taylor-Green | 3.5 +/- 0.5 | Flat or slightly shrinking | C = 0.89 (R^2=0.79) |
| Random Gaussian | 4-10 | Some growth at high k (resolution?) | Variable |
| ABC Beltrami | 4.5 -> 3.5 | Slightly decreasing | C = 0.87 (R^2=0.94) |

The ratios **never grow exponentially with k**. They decrease or stay constant. This means Chebyshev slack does not accumulate across De Giorgi levels.

### 3. Constant Slack Does NOT Improve Beta

In the recurrence U_k <= C^k * U_{k-1}^beta:
- A constant multiplicative improvement at the Chebyshev step replaces C with C/3 (roughly) — changes the constant but **does NOT change beta = 4/3**.
- To improve beta, the slack would need to scale as U_{k-1}^{-delta}, giving |{v_{k-1} > 2^{-k}}| <= (something) * U_{k-1}^{5/3 + delta}.
- The numerical evidence shows the ratio is approximately constant (not scaling with U_{k-1}).

**The Chebyshev step has moderate slack for most flows, but the slack is constant per De Giorgi level and does not improve the exponent.** This numerically confirms the analytical circularity result of S2-E003.

## ABC Flow Is the Tightest Despite Flattest Distribution

The ABC flow has the broadest global velocity distribution (p ~ 2 < 10/3) but its De Giorgi tightness ratios are 3.5-5x — comparable to other flows. Near the maximum, even the ABC flow's truncated variables v_k concentrate. The global and De Giorgi-level behaviors decouple.

## Resolution and Consistency

- N=64 and N=128 qualitatively consistent (TG: p=8.6 vs 9.97; Random: p=9.15 vs 8.72; ABC: identical 2.07)
- 7 cases tested: TG (Re=100,500,1600), Random (Re=100,500), ABC (Re=100,500)
- 50 log-spaced lambda values; power-law fit in region mu in [10^{-4}, 0.3]

## Critical Caveats

1. **DNS solutions are smooth.** Whether the 3-5x slack persists for near-singular solutions is unknown.
2. **Power-law model appropriateness.** ABC has R^2=0.53 (poor power-law); TG has R^2~0.79; only Random gives convincing power-law tails (R^2~0.95).
3. **Same-regime caveat as CZ slack (E009 adversarial assessment applies).** These measurements are on smooth flows, not near the regularity boundary. The tightness at the analytical level may be different.

## Relationship to Other Findings

- **Complements S2-E003 (chebyshev-universality):** E003 proved analytically that Chebyshev improvement is circular with regularity. E002 confirms numerically that the slack is constant (not beta-improving) and IC-dependent (not universal).
- **Distinct from E004 (cz-slack-k-independent):** E004 measured CZ slack for the pressure term P_k^{21}. This entry measures Chebyshev slack at the measure-bound step — a different step in the De Giorgi chain.
- **Confirms proposition-3-sharpness-audit (S2-E001):** Step 3b (Chebyshev on L^{10/3}) was identified as the single potentially improvable step. E002 shows it has moderate slack but of the wrong type (constant, not scaling).

## Verification

| Tag | Count | Description |
|-----|-------|-------------|
| COMPUTED | 5 | mu(lambda) exponents (7 cases, ~30 snapshots), tightness ratios (7 cases, k=1..10), k-scaling, ABC tightness, IC-dependent tail structure |
| CHECKED | 1 | N=64 vs N=128 consistency |
| CONJECTURED | 3 | Implications for beta=4/3, persistence for near-singular solutions, structural nature of barrier |
