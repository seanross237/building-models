---
topic: Compensated compactness / commutator route to improving beta — three-layer obstruction and SQG-NS structural gap
confidence: verified
date: 2026-03-30
source: "vasseur-pressure s2-exploration-004; CLMS 1993; CRW 1976; Caffarelli-Vasseur 2010"
---

## Main Finding: Route 3 (Commutator / Compensated Compactness) Is Definitively Closed

The compensated compactness / commutator approach to improving beta beyond 4/3 in the De Giorgi iteration for 3D Navier-Stokes fails at **three independent levels**. Both analytical computation and numerical DNS verification confirm each obstruction.

## The P^{21} Bilinear Form (Exact)

The bottleneck pressure P^{21} arises from the tensor product f_{ij} = u_i^{above} * u_j^{below}, where u = u^{below} + u^{above} is Vasseur's amplitude truncation at threshold lambda_{k-1} = 1 - 2^{-(k-1)}.

On {|u| > lambda_{k-1}}: f_{ij} = (u_i/|u|)(u_j/|u|) * v_{k-1} * lambda_{k-1}

This is a **rank-1 tensor** (unit direction x unit direction) times a scalar. Therefore:

P^{21}_{k-1} = R_iR_j[(u_hat_i * u_hat_j) * v_{k-1} * lambda_{k-1} * 1_{|u|>lambda_{k-1}}]

Standard CZ theory gives ||P^{21}||_{L^r} <= C lambda_{k-1} ||v_{k-1}||_{L^r}, producing beta = 1/2 + 5/6 = 4/3. [COMPUTED]

## Three-Layer Obstruction

### Layer 1: No Div-Curl Structure

Neither u^{above} nor u^{below} is divergence-free or curl-free after truncation. On {|u| > lambda}:

- div(u^{below}) = -lambda * (u . nabla|u|) / |u|^2 [COMPUTED]
- Bound: ||div(u^{below})||_{L^2} <= ||nabla u||_{L^2} — the full enstrophy [COMPUTED]

DNS compressibility ratios ||div(u^{below})||_{L^2} / ||nabla u||_{L^2}: 0.07-0.14 at operationally relevant thresholds (NOT small). [COMPUTED]

The bilinear form is a tensor product (not a contraction), so CLMS (1993) div-curl lemma cannot be applied — CLMS handles first-order cancellations but the NS pressure is a second-order (div-div) structure. The enstrophy-order compressibility error means truncation-based approaches cannot access Hardy space improvements. [COMPUTED]

### Layer 2: Commutator Remainder Dominates

Decomposing P^{21} into commutators:

P^{21} = Sum_j R_j[u_j^{below} * (-Delta)^{-1/2} div(u^{above})] + Sum_{ij} R_j[[R_i, u_j^{below}] u_i^{above}]

- **First term (remainder):** Arises from div(u^{above}) != 0. NOT a commutator, NO regularity gain. In SQG, R^perp(anything) is automatically div-free, so this term is **identically zero**. For NS, it is O(1).
- **Second term (commutator):** Genuine commutators [R_i, u_j^{below}] u_i^{above}, but CRW gives only the standard CZ bound.

DNS verification (Taylor-Green, lambda = 50% of max|u|): [COMPUTED]
- Commutator part: 72% of ||P^{21}||_{L^2}
- Remainder (div-error): **61%** of ||P^{21}||_{L^2}
- At wavenumber k=20: remainder spectral energy 18x commutator spectral energy

The commutator part has good high-frequency regularity (faster spectral decay), but the non-commutator remainder **dominates high frequencies** and negates any potential gain. [COMPUTED]

### Layer 3: CRW Vacuous for Bounded Multipliers

Coifman-Rochberg-Weiss (1976): ||[T, b]f||_{L^p} <= C ||b||_{BMO} ||f||_{L^p}

Applied to our setting: ||[R_iR_j, u_j^{below}]u_i^{above}||_{L^p} <= C ||u^{below}||_{BMO} ||u^{above}||_{L^p}

Since u^{below} is bounded by lambda_{k-1}: ||u^{below}||_{BMO} <= 2||u^{below}||_{L^infty} <= 2*lambda_{k-1}

This is **identical** to the direct CZ bound. The L^infty -> BMO trade is vacuous for bounded multipliers. CRW helps when the multiplier is unbounded-but-BMO (like log|x|); for bounded u^{below}, it provides zero improvement. [COMPUTED]

DNS confirmation: ||[R_1, u_1^{below}] u_1^{above}||_{L^2} / ||R_1(u_1^{above} u_1^{below})||_{L^2} = 0.19 — commutator is a proper fraction of the direct term. [COMPUTED]

## The SQG-NS Structural Gap (Precise Identification)

SQG (Caffarelli-Vasseur 2010) succeeds for three reasons, **all of which fail for NS**:

| Property | SQG | NS |
|----------|-----|-----|
| Active quantity | Scalar theta | Vector u |
| Truncation preserves div-free? | YES (R^perp of anything is div-free) | NO (truncating |u| breaks div(u)=0) |
| Nonlinearity | LINEAR in theta (drift = R^perp theta) | QUADRATIC in u (pressure = R_iR_j(u_i u_j)) |
| Commutator structure | Natural: [R^perp, theta^{below}] . nabla theta_k | Blocked: product of two velocity factors |
| Divergence remainder | Zero (identically) | O(1), 61% of P^{21} |
| CRW improvement | Meaningful (regularity gain from commutator) | Vacuous (u^{below} is bounded) |

The gap is **structural, not technical**: scalar vs. vector, linear vs. quadratic, first-order vs. second-order. No rearrangement of the NS terms can produce the SQG commutator structure because the fundamental nonlinearity is different. [COMPUTED]

## Div-Free Truncation Impossibility

Attempts to construct a divergence-free truncation (to eliminate the remainder term) face a topological obstruction: a continuous map u -> T(u) that is (a) divergence-free when u is, (b) bounded by lambda, and (c) equals u when |u| <= lambda, would need to be a retraction of the div-free ball onto a div-free sub-ball — which is topologically impossible for vector fields in 3D by degree theory arguments. [COMPUTED]

## Informal Sharpness Theorem

**beta_{DG}(NS) = 4/3** for any method using only: (a) energy inequality, (b) Sobolev/interpolation, (c) CZ theory for pressure (including commutator/CLMS variants), (d) Chebyshev/level-set estimates.

To beat 4/3, one must inject structural information about NS solutions beyond these four ingredients. [CONJECTURED]

## Remaining Directions (Post-Route 3, Updated Post-S2-E005)

1. **Nonlinear lower bounds on ||d_k||_{L^2}**: Use the NS equation itself (not just the energy inequality) to show dissipation on level sets has a minimum related to velocity excess
2. ~~**Frequency-localized De Giorgi**~~ **CLOSED by S2-E005**: LP decomposition cannot improve beta. Bernstein exchange rate 2^{3j/5} is dimensional and structural; CZ is already the optimal frequency-by-frequency estimate; LP gives 5-10x worse bounds than direct CZ. Four independent lines of evidence (spectral peak shift, growing I_hi, Bernstein inflation, analytical exponent chain). See `frequency-localized-degiorgi-lp-obstruction.md`.
3. **Quantitative unique continuation**: Exploit that NS solutions cannot vanish to infinite order on sets of positive measure
4. **Topological/geometric constraints**: Use vortex line structure or helicity conservation

## Verification Scorecard

| Tag | Count |
|-----|-------|
| [VERIFIED] | 0 |
| [COMPUTED] | 14 |
| [CHECKED] | 2 |
| [CONJECTURED] | 1 |

## S2-E006 Confirmation: CRW Consistently Vacuous

S2-E006 independently confirmed Layer 3 (CRW vacuous for bounded multipliers) by testing the commutator route from the test-function side (moving CZ to v_k). Result: beta <= 1, identical to direct IBP. The multiplier u^{below} has the same BMO norm regardless of which side CZ acts on, so commutator improvements are vacuous in both directions. Additionally, S2-E006 showed the direct IBP route gives beta = 1 (WORSE than CZ by 1/3), quantifying the CZ consolidation gain. The three non-CZ routes (IBP, H^1/BMO, CRW) all fail to improve beta, establishing tool-independence of the 4/3 barrier. See `non-cz-pressure-routes-tool-independence.md`.

## S2-E007 Adversarial Review of Informal Sharpness (Claim 3)

S2-E007 adversarial review assessed the informal sharpness theorem as **the most significant novel claim** from Strategy-002: correctness 7/10 (informal, not rigorous), novelty 8/10, significance 8/10, publishability 6/10 standalone. The systematic closure of seven routes with clear mathematical reasons per route is genuinely new work. Strongest counterargument: "the class of techniques is not well-defined, so the claim is vacuous." This is serious — without a formal definition, it is a summary of failed attempts rather than a theorem. However, the seven specific routes span the natural approaches, and each closure is individually rigorous.

Three combination attacks tested against these closures all failed: (1) commutator + LP fails in the hard regime (high k AND high j); (2) modified functional + improved embedding gains offset by worse nonlinear estimates; (3) truncation + compensated compactness div-free-preserving truncations destroy either iteration structure or compensated compactness gains.

**SDP formalization path:** Setting up SDP (sum-of-squares relaxation) to find the optimal bound on |{|u| > lambda}| given all NS constraints could upgrade the informal sharpness to a rigorous computer-assisted result. Identified as highest-priority missing direction.

See `s2-adversarial-review-beta-four-thirds.md` for full adversarial analysis.

## Cross-References

- [proposition-3-sharpness-audit.md](proposition-3-sharpness-audit.md) — Identified direction (b) "alternative to Holder pairing" as open; S2-E004 tested via commutator, confirmed non-viable within CZ class
- [chebyshev-universality-and-model-pde-comparison.md](chebyshev-universality-and-model-pde-comparison.md) — SQG success mechanism further characterized (div-free preservation, scalar nature, commutator structure)
- [beta-current-value-four-thirds.md](beta-current-value-four-thirds.md) — Route 3 (compensated compactness) now definitively closed
- [vorticity-degiorgi-universal-barrier.md](vorticity-degiorgi-universal-barrier.md) — Third evidence point for universality: CZ+commutator class is also sharp at 4/3
- [frequency-localized-degiorgi-lp-obstruction.md](frequency-localized-degiorgi-lp-obstruction.md) — S2-E005 closes direction 2 (frequency-localized De Giorgi); LP decomposition cannot improve beta
- [non-cz-pressure-routes-tool-independence.md](non-cz-pressure-routes-tool-independence.md) — S2-E006 confirms CRW vacuity and establishes tool-independence of 4/3
