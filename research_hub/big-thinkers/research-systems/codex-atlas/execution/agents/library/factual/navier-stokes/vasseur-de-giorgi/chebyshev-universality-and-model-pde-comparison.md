---
topic: Chebyshev universality — beta = 1 + s/n formula, model PDE comparison, circularity of Chebyshev improvement
confidence: verified
date: 2026-03-30
source: "vasseur-pressure s2-exploration-003; Vasseur 2007; Caffarelli-Vasseur 2010; Brigati-Mouhot 2025"
---

## Main Finding: Universal De Giorgi Exponent Formula

The generic De Giorgi recursion exponent for a dissipative PDE with H^s dissipation in n spatial dimensions is:

> **beta = 1 + s/n**

This formula arises from the chain: H^s Sobolev embedding -> L^{2n/(n-2s)} -> parabolic interpolation -> L^{2+4s/n}_{t,x} -> Chebyshev -> measure bound U^{(1+2s/n)/1} -> indicator L^2 norm U^{(1/2+s/n)} -> combined with gradient factor U^{1/2} to give beta = 1 + s/n.

Confirmed by Brigati-Mouhot (arXiv:2510.11481, 2025) for scalar elliptic/parabolic: beta = 1 + 2/d (their formulation uses spatial dimension d only; for the parabolic version with H^1 dissipation, equivalent to 1 + 1/d which matches 1 + s/n with s=1).

## Comprehensive Model PDE Table

| PDE | d | s | Sobolev target | Parabolic q | Cheb. measure exp. | Beta = 1+s/d | Closes? | Why? |
|-----|---|---|---------------|------------|-------------------|-------------|---------|------|
| 1D Burgers | 1 | 1 | L^infty | L^6 | 3 | 2 | YES | H^1 -> L^infty in 1D |
| 2D NS | 2 | 1 | L^p (all p) | L^4 | 2 | 3/2 | BORDERLINE | Known: Ladyzhenskaya |
| 3D NS | 3 | 1 | L^6 | L^{10/3} | 5/3 | 4/3 | NO | Open problem |
| 4D NS (hyp.) | 4 | 1 | L^4 | L^3 | 3/2 | 5/4 | NO | Worse than 3D |
| 3D MHD | 3 | 1 | L^6 | L^{10/3} | 5/3 | 4/3 | NO | Same as 3D NS |
| SQG (2D, s=1/2) | 2 | 1/2 | L^4 | L^3 | 3/2 | 5/4 | YES* | Commutator + extension |
| SQG extension | 3 | 1 | L^6 | L^{10/3} | 5/3 | 4/3 | YES* | Drift is multiplicative |
| Frac NS alpha=5/4 | 3 | 5/4 | L^12 | L^{11/3} | 11/6 | 17/12 | NO** | De Giorgi misses Lions |
| Frac NS alpha=3/2 | 3 | 3/2 | L^infty | L^4 | 2 | 3/2 | BORDERLINE | De Giorgi just reaches |

*SQG closes despite generic beta = 5/4 because the drift term is multiplicative (controlled by BMO^{-1} norm), not an additional power of U_{k-1}.
**Fractional NS at alpha = 5/4 has regularity (Lions 1969), but De Giorgi gives beta = 17/12 < 3/2.

## Chebyshev Step Is NOT Independently Improvable

The Chebyshev inequality applied to L^{10/3} functions is SHARP for arbitrary functions. The question is whether NS solutions have better distributional decay than arbitrary L^{10/3} functions. Analysis of six potential improvement routes:

1. **Support-restricted Chebyshev**: Support constraint from previous De Giorgi level is WEAKER than direct Chebyshev in the convergent regime (U_{k-2}^{5/3} > U_{k-1}^{5/3} when U_k decreasing).
2. **Holder interpolation with different q < 10/3**: Total exponent on U is 5/3 INDEPENDENT of q. The redistribution is information-preserving; optimization over q is flat.
3. **Lorentz space refinement**: L^{p,q} Lorentz theory refines constants, not the decay exponent. Distribution function decay rate lambda^{-p} is determined by Lebesgue exponent p, not Lorentz second index.
4. **Gradient/isoperimetric approach**: Gradient information already fully exploited through H^1 -> L^6 Sobolev embedding. Coarea/isoperimetric recovers W^{1,1} -> L^{3/2} (weaker than H^1 -> L^6).
5. **L^2 Chebyshev**: Gives |A_k| <= C^k U_{k-1} which is WEAKER than L^{10/3} Chebyshev (U_{k-1}^{5/3} << U_{k-1} for small U_{k-1}).
6. **PDE-based integrability beyond L^{10/3}**: Would require bootstrapping beyond H^1 regularity, which is EQUIVALENT to proving regularity. CIRCULAR.

**The fundamental circularity**: Improving the Chebyshev step from L^{10/3} to L^4 requires H^{5/4} regularity (Lions threshold). The gap in the Chebyshev step IS the regularity gap, repackaged. Improving Chebyshev is not an independent route to regularity; it IS the regularity problem.

## SQG Caffarelli-Vasseur 2010 Success Mechanism

The SQG regularity proof succeeds NOT by improving Chebyshev but through three structural differences from NS:

1. **No pressure**: SQG is a scalar advection equation. The P_k^{21} non-divergence pressure bottleneck is entirely absent.
2. **Scalar equation**: Truncated function w_k is scalar, simplifying Holder pairings. No cross-terms between components.
3. **Drift structure**: Via Caffarelli-Silvestre harmonic extension, the nonlinearity enters as a drift b contributing a bounded multiplicative factor (controlled by ||b||_{BMO^{-1}}), not an additional power of U_{k-1}.

The actual De Giorgi beta in the extension framework is 4/3 (same as 3D NS!), but the iteration closes because the drift term produces U_k <= C^k * (1 + ||b||_{BMO^{-1}}) * U_{k-1}^{4/3}, where the BMO^{-1} factor is a bounded constant independent of k.

The commutator structure [(-Delta)^{1/2}, u] (Kato-Ponce estimate) provides additional regularity for the nonlinear term, but the most fundamental difference is the absence of pressure.

## Div-Free Level-Set Distribution — RESOLVED (S2-E008)

**Does div(u) = 0 improve the distribution function |{|u| > lambda}| beyond lambda^{-p} ||u||_{L^p}^p?**

**NO.** S2-E008 proved this conclusively. The constant field u_n = (lambda + 1/n, 0, 0) is div-free, in H^1(T^3), and achieves Chebyshev ratio -> 1 as n -> infinity. This is a constructive proof that the supremum of the Chebyshev ratio over all div-free H^1 fields equals 1 — identical to unconstrained fields.

The structural reason: div-free constrains the DIRECTION field u/|u|, not the MAGNITUDE distribution |u|. Three families demonstrate this: constant fields achieve arbitrary constant magnitude, shear flows u = (f(x_2,x_3), 0, 0) achieve arbitrary 2D profiles, and curls u = curl(A) achieve arbitrary 3D variation — all while remaining div-free.

Prior literature context (unchanged):
- CLMS (1993) div-curl lemma: improves BILINEAR products (u_i u_j -> H^1), not individual field distribution
- Bourgain-Brezis (2004, 2007): improves solutions to div/curl equations at L^1 endpoint, not distribution functions
- Van Schaftingen (2004, 2013): endpoint Sobolev for cancelling operators, irrelevant at L^{10/3}

**This question is now CLOSED.** Div-free cannot improve the Chebyshev exponent. Full analysis in `chebyshev-sharpness-constant-field-extremizer.md`.

## 3D MHD Confirmation

De Giorgi iteration applied to MHD (He-Xin 2005; Jiu-Wang; Chamorro-He 2020) gives beta = 4/3, identical to NS. The magnetic tension B . nabla B has the same scaling (quadratic, one derivative) and produces the same type of pressure interaction. The formula beta = 1 + s/n = 1 + 1/3 = 4/3 holds for both u and B independently.

## Fractional NS and the Lions Gap

For fractional NS with dissipation (-Delta)^alpha:
- De Giorgi beta = 1 + alpha/3
- Crosses 3/2 threshold at alpha = 3/2
- Lions (1969) proves regularity at alpha >= 5/4

This gap (5/4 vs 3/2) shows De Giorgi uses only one step of the energy bootstrap, while Lions iterates through multiple Sobolev levels. The De Giorgi method is structurally weaker than iterative energy methods for the fractional NS problem.

## S2-E004 SQG-NS Gap Further Characterized

S2-E004 provided a precise six-property comparison table characterizing the SQG-NS structural gap. The three key differences explaining why SQG's commutator mechanism cannot transfer to NS: (1) scalar vs. vector active quantity, (2) linear vs. quadratic nonlinearity, (3) truncation automatically preserves div-free in SQG (R^perp of anything is div-free) but NOT in NS (amplitude truncation breaks div(u)=0 with 0.07-0.14 compressibility ratio). The gap is structural, not technical — no rearrangement of NS terms can produce SQG commutator structure. DNS verification: divergence-error remainder is 61% of P^{21} in L^2 and dominates high frequencies by 18x. Full analysis in `compensated-compactness-commutator-obstruction.md`.

## S2-E002 DNS Numerical Confirmation

S2-E002 DNS measurements of mu(lambda) = |{|u| > lambda}|/|Omega| confirm that Chebyshev slack is IC-dependent and NOT universally improvable: Taylor-Green p~10 (massive slack), Random Gaussian p~8-9 (significant slack), ABC Beltrami p~2.1 (**below** 10/3 — Chebyshev is tight or optimistic). De Giorgi tightness ratios are ~3-5x and k-independent across all ICs, meaning the slack is CONSTANT per level and does not improve beta. This numerically confirms the analytical circularity result above. Full data in `dns-levelset-distribution-chebyshev-tightness.md`.

## S2-E007 Adversarial Verdicts on Claims 1 and 2

S2-E007 adversarial review assessed the universal formula (Claim 1) and SQG-NS gap (Claim 2):

**Claim 1 (beta = 1+s/n):** Correct (7/10), moderate novelty (5/10), moderate significance (4/10), low standalone publishability (3/10). The formula is implicit in the literature but NOT explicitly stated as a universal formula with comparison table. Elementary — any PDE specialist would derive it on demand. Strongest counterargument: "This is folklore." Suitable as a section in a survey/expository paper.

**Claim 2 (SQG-NS structural gap):** Correct (9/10), moderate-high novelty (6/10), moderate-high significance (6/10), moderate publishability as part of a paper (4/10). The individual facts are known but the systematic "3 dimensions of the gap" comparison is not found in a single paper. Strongest counterargument: "obvious to anyone who has read both proofs."

**Both claims survive adversarial review.** Most publishable as part of the combined Claims 1-4 paper.

## Cross-References

- [proposition-3-sharpness-audit.md](proposition-3-sharpness-audit.md) — Detailed sensitivity table for the 4/3 chain
- [vorticity-degiorgi-universal-barrier.md](vorticity-degiorgi-universal-barrier.md) — Independent 4/3 from trilinear form (supports universality)
- [beta-current-value-four-thirds.md](beta-current-value-four-thirds.md) — Term-by-term exponent table
- [post-2007-beta-landscape.md](post-2007-beta-landscape.md) — No paper has improved beta beyond 4/3
- [compensated-compactness-commutator-obstruction.md](compensated-compactness-commutator-obstruction.md) — SQG-NS structural gap precise characterization; commutator route definitively closed
- [dns-levelset-distribution-chebyshev-tightness.md](dns-levelset-distribution-chebyshev-tightness.md) — DNS numerical confirmation: IC-dependent tails, 3-5x constant Chebyshev tightness
