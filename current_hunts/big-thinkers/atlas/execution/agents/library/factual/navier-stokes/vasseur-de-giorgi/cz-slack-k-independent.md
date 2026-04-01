---
topic: CZ slack for P_k^{21} is k-independent
confidence: verified
date: 2026-03-30
source: "vasseur-pressure strategy-001 exploration-004"
---

## Finding

**The Calderon-Zygmund (CZ) tightness ratio for the De Giorgi bottleneck pressure piece P_k^{21} converges to a k-independent constant by k ~ 3-4.** This means the CZ slack does NOT grow with the De Giorgi iteration depth, ruling out the hypothesis that exploiting CZ slack could improve the recurrence exponent beta beyond 4/3.

## Details

The CZ bound states ||P||_q <= C_q ||f||_q where C_q = max(q, q/(q-1)) - 1 (Iwaniec 1982). The **tightness ratio** = ||P||_q / (C_q * ||f||_q). If tightness decreases with k, the slack grows and beta could improve.

### Measured k-dependence (q=2, Re=500)

| IC | k=1 | k=4 | k=8 | Trend |
|---|---|---|---|---|
| Taylor-Green | 0.436 | 0.407 | 0.404 | DOWN -7.3% (converges) |
| Anti-parallel | 0.488 | 0.580 | 0.588 | UP +20.3% (converges) |
| Random Gaussian | 0.267 | 0.259 | 0.260 | FLAT -2.9% |

At higher q (4, 6, 8), all ICs show slight downward trends or flatness, but always **converging to a constant** by k ~ 3-4. Further increases in k produce < 1% change.

### Why this happens

As k increases, lambda_k = 1 - 2^{-k} -> 1. The velocity truncation u_below converges to u * min(1, 1/|u|) (unit speed cap), and the RHS tensor f^{21} = u_below x u_below stabilizes. Both ||P21||_q and C_q ||f21||_q grow proportionally, so their ratio converges.

### Overall CZ slack ranges (all cases, k >= 1)

| q | Min tightness | Max tightness | Slack range (1/tightness) |
|---|---|---|---|
| 2 | 0.259 | 0.588 | 1.7x - 3.9x |
| 4 | 0.098 | 0.276 | 3.6x - 10.2x |
| 6 | 0.067 | 0.212 | 4.7x - 14.9x |
| 8 | 0.054 | 0.182 | 5.5x - 18.4x |

The CZ bound has substantial slack (up to 18x at q=8), but this slack is **CONSTANT in k**.

### Re-independence

Tightness ratios at Re=100, 500, 1000 are essentially identical (differences < 0.5%), indicating this is a structural property of velocity field topology, not viscous dynamics.

### Grid convergence

N=64 and N=128 values agree to better than 0.2% for all k and q tested (Taylor-Green, Re=500).

## Hypothesis falsified

The hypothesis "if ||P_k^{21}||_q decreases relative to C_q as k increases, then the exponent contributed by this term improves with each De Giorgi step, potentially allowing beta > 4/3" is **FALSIFIED**.

## E009 Adversarial Assessment

**The entire measurement is on the wrong solutions.** The De Giorgi iteration matters near potential singularities — solutions at the edge of blow-up. DNS at N=64-128 with Re=100-1000 produces globally smooth solutions nowhere near singular. The CZ slack on smooth solutions tells us about the pressure structure of REGULAR flows, not about the behavior of the CZ bound at the critical level sets where regularity theory operates. The k-independence result might simply reflect that for smooth flows, the level sets {|u| > lambda_k} become empty at moderate k, so the tightness ratio measures numerical noise, not mathematical structure.

**Corrected framing:** "For smooth DNS solutions at Re=100-1000, the CZ tightness ratio of P_k^{21} converges to a k-independent constant by k~3-4, and P_k^{21} saturates the CZ bound more tightly than the full pressure. This rules out k-dependent CZ improvement mechanisms on smooth flows, but does not directly address near-singular behavior." Grade: C+ (methodologically sound, scope limited). **Novel** — no prior work computes CZ tightness ratios for individual De Giorgi pressure decomposition pieces from DNS.

## S2-E002 Companion: Chebyshev Tightness Ratios Also k-Independent

S2-E002 measured a different but related quantity: the Chebyshev tightness ratio at the measure-bound step (not the CZ step). De Giorgi Chebyshev ratios are also ~3-5x and k-independent, with the same interpretive conclusion: constant slack does not improve beta. The two measurements together (CZ tightness from E004 + Chebyshev tightness from S2-E002) establish that BOTH major inequalities in the De Giorgi chain have constant-only slack on smooth DNS solutions. See `dns-levelset-distribution-chebyshev-tightness.md`.

## What this does NOT rule out

1. **Structural improvement beyond CZ:** The CZ bound treats f^{21}_{ij} as arbitrary L^q data. The actual tensor has f^{21} = u_below x u_below with u_below bounded and divergence-free. Div-curl estimates could beat CZ in a k-dependent way.
2. **Cancellation between pressure pieces:** The De Giorgi argument treats P21, P22, P23 separately. Cancellations between pieces could produce tighter combined bounds.
3. **Different decomposition choices:** The lambda_k = 1 - 2^{-k} threshold is standard but not unique. An adapted splitting might produce better CZ properties.
4. **Other bottleneck paths:** Improvement to beta could come from Chebyshev, interpolation, or energy inequality steps instead.
