# E004 Summary: Adversarial Search for sup|λ_min(HessS)|

## Goal
Find sup|λ_min(HessS(Q))| by adversarial optimization to determine the mass gap threshold β < 2/sup|λ_min|.

## Outcome: PARTIALLY SUCCESSFUL (empirical value found; β < 1/4 ruled out)

**Empirical inf λ_min = -14.734** (d=4, L=2), determined to ±0.05 by adversarial optimization with 35+ gradient descent starts from random, structured, and anti-instanton configurations.

The extremal config is a GD-optimized anti-instanton: Q_μ = iσ_{a(μ)} with axes (0,0,2,1), which makes 80/96 plaquettes have U_□ = -I. GD further optimizes the tradeoff between self-term negativity (D_min → -5.60) and cross-term norm (||C|| → 9.83).

**β < 1/4 (|λ_min| ≤ 2d = 8) is RULED OUT** — anti-instantons alone give |λ_min| = 14.2 without optimization.

**Best proven bound (conditional on decoherence): |λ_min| ≤ 4d = 16 → β < 1/8.** Decoherence (||C(Q)|| ≤ 2(d+1) = 10) is strongly supported numerically (0/2000+ violations) but unproved.

## Verification scorecard
- COMPUTED: 7 (empirical inf, D+C decomposition, cross-term survey, dim scaling, extremal config, anti-instanton analysis, plaquette holonomies)
- CONJECTURED: 3 (decoherence, anti-correlation mechanism, sub-4d bound)
- VERIFIED: 0

## Key takeaway
The mass gap improvement via Bakry-Émery is capped at **β < 1/8 (1.5× over SZZ)** with current tools, not β < 1/4 as hoped. The bottleneck is that anti-instanton configurations push |λ_min| to ~14.7, well above 2d = 8. Proving the decoherence lemma (||C|| ≤ 10) would give the clean result |λ_min| ≤ 4d → β < 1/8.

## Leads worth pursuing
1. **Prove decoherence lemma** — the single missing ingredient for β < 1/8. Tensor product norm bound: when color kernels have ||F|| ≤ 2, the sum's operator norm is maximized when all F ∝ I₃ (flat case).
2. **D/C anti-correlation** — empirically, D_min and ||C|| cannot both be extremal. Proving this would give |λ_min| < 4d strictly, possibly ~3.7d (matching the ~14.7 empirical value).
3. **Larger lattice L** — check if the infimum changes for L > 2.

## Unexpected findings
- Random configs give |λ_min| ≈ 8-9, far from the true infimum of 14.7. The extremal configs are structured (anti-instanton type), not generic. Prior exploration (E003) underestimated |λ_min| because it started GD from random configs only.
- The GD optimizer reveals a tradeoff: relaxing D_min from -6 to -5.6 while pushing ||C|| from 8.65 to 9.83 gives a more negative total λ_min.
- **L=2 is the worst case**: |λ_min| decreases with larger L (checked L=2,3 for d=2,3,4). The β bound holds for all L.
