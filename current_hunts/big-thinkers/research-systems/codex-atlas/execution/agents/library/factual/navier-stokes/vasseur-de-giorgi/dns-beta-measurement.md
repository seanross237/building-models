---
topic: DNS measurement of beta_effective — approaches and computability
confidence: provisional
date: 2026-03-30
source: "vasseur-pressure exploration-001"
---

## Finding

The De Giorgi recurrence exponent beta can be empirically measured from DNS data. Three approaches are defined:

### Approach A: Direct Iteration Measurement — **TESTED (E002)**

Compute U_k for k = 0, 1, ..., K_max from DNS velocity fields. Fit log(U_k) = a*k + beta * log(U_{k-1}) via least squares. Requires: computing |u| on grid, level set truncations v_k, gradient norms d_k, supremum + integral for U_k. All standard L^p norms on periodic domains. **E002 result: 21 cases (5 ICs x 3-4 Re x 2 resolutions). All beta_eff < 4/3. Maximum beta_eff = 1.01 (ABC, Re=1000). See `dns-beta-empirical-results.md` for full data.** Critical design choice: L^inf normalization required (L^2 normalization makes level sets trivially empty for smooth flows).

### Approach B: Bottleneck Term Measurement — **TESTED (E002)**

Directly measure the exponent of U_{k-1} in the specific non-divergence pressure integral I_k = int int |P_k^{21}| * |d_k| * 1_{v_k>0} dx dt. Requires solving a Poisson equation for P_k^{21} (spectral on periodic domains). Theoretical prediction: I_k ~ U_{k-1}^{4/3 - 5/(3q)}. **E002 result: Bottleneck exponent gamma DECREASES with Re for all ICs. At Re>=500, most ICs show gamma < 1 (far below 4/3). ABC maintains gamma > 1. The 4/3 bound is NOT loose — it captures a genuine turbulence effect. See `bottleneck-exponent-dns.md` for full data.**

### Approach C: CZ Slack as Proxy — **TESTED, DOES NOT HELP**

Measure the ratio between the theoretical CZ bound on P_k^{21} and its actual value. If CZ slack factor is S, effective beta may be modified. **E004 result: CZ slack for P_k^{21} converges to a k-independent constant by k ~ 3-4 (1.7-3.9x at q=2, 5.5-18.4x at q=8). The slack does NOT grow with k, so it cannot improve beta.** P21 actually has LESS slack than the full pressure (1.7-3.9x vs 7.6-17.5x). CZ slack proxy approach is eliminated as a route to beta improvement.

### DNS Computability Assessment

**Computable:** U_k for finite k; recurrence exponent via regression; pressure decomposition P = P_k^1 + P_k^2 (FFT Poisson solve); bottleneck integral I_k; CZ slack in De Giorgi context.

**Not computable (or limited):** k -> inf limit (finite grid gives ~10-15 useful levels at 512^3); epsilon -> 0 limit (analytical, not computational); universality across all flows (fundamental: DNS gives evidence, not proof).

### Key Adaptations for Periodic Domains

1. Replace nested balls B_k with full periodic domain (no spatial nesting needed)
2. Normalize so U_0 <= 1 (simple rescaling)
3. K_max ~ 10-15 for typical resolutions
4. Spectral methods for Poisson solves in pressure decomposition

### Key Questions for DNS

- Does empirical beta exceed 4/3? (CZ bound has exploitable slack in De Giorgi context)
- Does it exceed 3/2? (dramatic evidence for regularity)
- ~~Is the CZ slack on P_k^{21} comparable to the 7.6-17.5x slack on full pressure?~~ **ANSWERED (E004): P21 CZ slack is 1.7-3.9x at q=2, LESS than full pressure. And it is k-independent.**

| Obstacle | Severity | Workaround |
|----------|----------|------------|
| Finite k | Low | ~10-15 levels suffice for fitting |
| No nested balls | Low | Full periodic domain or windowed sub-domains |
| Resolution limits on v_k | Medium | Limits K_max; use highest resolution |
| Single-flow non-universality | High | Multiple ICs (TGV, anti-parallel, random) |
| Cannot prove beta > 3/2 | Fundamental | DNS provides evidence, not proof |

## Connection to Prior Work

The beta measurement is related to but distinct from CZ slack measurements. CZ slack enters through the bound on P_k^{21}, but beta also depends on Sobolev gain, Chebyshev structure, and geometric constants. It is theoretically possible for CZ slack to be large but beta to remain < 3/2.
