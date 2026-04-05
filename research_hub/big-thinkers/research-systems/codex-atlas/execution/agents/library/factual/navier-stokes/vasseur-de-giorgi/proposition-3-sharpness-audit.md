---
topic: Proposition 3 sharpness audit — complete sensitivity table and improvable steps
confidence: verified
date: 2026-03-30
source: "vasseur-pressure s2-exploration-001; Vasseur 2007 Section 4 pages 14-24"
---

## Finding

A line-by-line decomposition audit of Vasseur (2007) Proposition 3 traces exactly how each sub-exponent contributes to beta = 4/3, classifies every step as sharp or potentially loose, identifies all free parameters, and pinpoints the SINGLE potentially improvable link in the chain.

## The 4/3 = 1/2 + 5/6 Decomposition

The bottleneck exponent 4/3 arises from two factors forced together by the non-divergence-form pressure interaction -P_{k21} * div(u v_k/|u|):

- **1/2**: from ||d_k||_{L^2} <= U_{k-1}^{1/2} — the gradient/dissipation bound (DEFINITIONAL, from U_k definition)
- **5/6**: from ||1_{v_k>0}||_{L^2} <= C^k U_{k-1}^{5/6} — the measure/indicator bound (chain of 5 steps)

## Sensitivity Table

| Step | Tool | Exponent contribution | dB/dδ | Sharp? | Notes |
|------|------|----------------------|-------|--------|-------|
| 3a | Sobolev H^1→L^6 (3D) | Feeds into 5/6 via Chebyshev | ~1/6 indirect | **YES** | H^1→L^{6+δ} would give β = 4/3 + δ/6, but Sobolev exponent 6 is provably optimal in 3D |
| 3a | L^∞L^2 ∩ L^2L^6 interpolation | Determines L^{10/3} exponent | N/A | **YES** | 10/3 is the unique interpolation exponent |
| 3a | Energy definition U_k^{1/2} | 1/2 in ||v_{k-1}||_{L^{10/3}} <= U_{k-1}^{1/2} | Direct | **YES** (definitional) | |
| 3b | Chebyshev on L^{10/3} | 5/3 = (10/3)*(1/2) in measure bound | 1/2 | **YES** (abstract) | Tight for arbitrary functions. NS structure unused. |
| 3b→5b | L^2 norm of indicator | **5/6 = (5/3)*(1/2)** | **dβ/dδ = 1** (direct additive) | **YES** given 5/3 input | q=2 forced by Holder pairing in Step 5b |
| 5b | Gradient factor ||d_k||_{L^2} | **1/2** | **dβ/dδ = 1** (direct additive) | **YES** (definitional) | d_k^2 is part of U_k |
| 5b | Non-divergence pressure | Forces Holder pairing → 1/2 + 5/6 | N/A (structural) | **UNKNOWN** | Only step not provably sharp |
| 4 | Non-local pressure P_{k1} | β_p > 3/2 for p > 10 | N/A | **YES** | Not the bottleneck |

## The 5/6 Genealogy (Complete Chain)

```
H^1(R^3) → L^6(R^3)              [Sobolev: 1/6 = 1/2 - 1/3, SHARP in 3D]
     ↓
L^2_t L^6_x ∩ L^∞_t L^2_x       [available norms from energy]
     ↓ (interpolation, SHARP)
L^{10/3}_{t,x}                    [parabolic Sobolev: 3/(10/3) = 3/10]
     ↓
||v_{k-1}||_{L^{10/3}} ≤ C U_{k-1}^{1/2}    [equation (10), SHARP by definition]
     ↓ (Chebyshev at level 2^{-k})
|{v_k > 0}| ≤ 2^{10k/3} U_{k-1}^{5/3}       [SHARP abstractly, POTENTIALLY LOOSE for NS]
     ↓ (L^2 norm)
||1_{v_k>0}||_{L^2} ≤ C^{k/2} U_{k-1}^{5/6}  [5/6 = (5/3)/2, SHARP given measure bound]
```

## The Single Potentially Improvable Step

**Step 4 (Chebyshev on L^{10/3})** is the ONLY step that is sharp for general functions but potentially loose for NS solutions. All other steps are either definitional, algebraically optimal (Sobolev, interpolation), or structurally forced (Holder pairing).

The question: do NS solutions near a potential singularity have |{v_{k-1} > lambda}| decaying faster than lambda^{-10/3}? If |{v_k > 0}| <= C^k U_{k-1}^{5/3+delta} for some delta > 0, then beta = 4/3 + delta/2. Need delta > 1/3 to reach 3/2.

Related to: regularity of level sets of |u|, concentration phenomena near singular points, Kolmogorov scaling structure. No such structural improvement is currently known.

## Free Parameters (All Exhausted)

1. **Truncation function** v_k = [|u| - (1-2^{-k})]_+: Any truncation satisfying monotonicity + level gap + energy capture gives the SAME exponents. **No improvement possible.**
2. **Sobolev target exponent** L^{10/3}: Uniquely determined by H^1→L^6 (sharp in 3D) + energy norms. **No improvement possible.**
3. **Holder conjugate pairs** in pressure bound: Optimized. Different pairings trade off between the two factors but cannot improve the sum. **No improvement possible.**
4. **Pressure decomposition** P = P_{k1} + P_{k2}: Vasseur's innovation isolates the bottleneck but is not its source. Alternative decompositions (Choi-Vasseur) redistribute but don't eliminate. **Limited improvement potential.**
5. **Cutoff functions** eta_k, phi_k: Affect only the C^k constant, not beta. **No improvement possible.**

## Three Improvement Directions

(a) **Structural Chebyshev improvement**: Show |{v_{k-1} > 2^{-k}}| <= C^k U_{k-1}^{5/3+delta} for NS solutions. Need delta > 1/3. MOST PROMISING but no known result.

(b) **Alternative to the Holder pairing in Step 5b**: Estimate the non-divergence pressure term without requiring d_k in L^2 paired with indicator in L^2. Requires fundamentally new pressure decomposition.

(c) **Different energy quantities U_k**: Modify the definition to change the 1/2 and/or 5/6 contributions. Requires abandoning the De Giorgi framework.

## Cross-Comparison Confirmation

The vorticity formulation (Vasseur-Yang 2021) produces the SAME 4/3 from the SAME 1/2 + 5/6 chain, despite eliminating pressure entirely. The non-divergence trilinear form T_∇[alpha_k v, rho_k beta_k v, beta_k v] involves the same gradient factor (U^{1/2}) and Chebyshev indicator factor (U^{5/6}). This confirms the 4/3 is intrinsic to the NS quadratic nonlinearity, not to pressure handling. See `vorticity-degiorgi-universal-barrier.md`.

## S2-E003 Chebyshev Circularity Assessment

S2-E003 tested whether the Chebyshev step (identified above as the single potentially improvable link) can be independently improved. **Verdict: NO.** Six routes analyzed, all ruled out or circular:

1. Support-restricted Chebyshev: weaker in convergent regime (U_{k-2}^{5/3} > U_{k-1}^{5/3})
2. Holder interpolation with different q: exponent independent of q (information-preserving)
3. Lorentz space refinement: affects constants, not decay exponents
4. Gradient/isoperimetric: already exploited via H^1 -> L^6 Sobolev
5. L^2 Chebyshev: strictly weaker for small U_{k-1}
6. PDE-based integrability beyond L^{10/3}: circular with regularity

The Chebyshev improvement from L^{10/3} to L^4 requires H^{5/4} regularity (the Lions threshold). The gap in the Chebyshev step IS the regularity gap. Direction (a) above (structural Chebyshev improvement) is therefore NOT independently achievable; direction (b) (alternative to Holder pairing) or (c) (different energy quantities) remain the only non-circular options. Full analysis in `chebyshev-universality-and-model-pde-comparison.md`.

**Open question RESOLVED (S2-E008)**: Does div(u)=0 improve |{|u|>lambda}| beyond lambda^{-p} ||u||_p^p? **NO.** The constant field u = (lambda+epsilon, 0, 0) is div-free, in H^1, and achieves ratio -> 1. Div-free constrains the direction field of u, not its magnitude distribution. Any smooth magnitude distribution is realizable by a div-free field (constant fields, shear flows, curls). The Chebyshev inequality is therefore PROVABLY TIGHT for div-free fields. Direction (a) (structural Chebyshev improvement) is CLOSED. See `chebyshev-sharpness-constant-field-extremizer.md`.

### S2-E002 DNS Numerical Measurement of Chebyshev Slack

S2-E002 measured the actual level-set distribution and De Giorgi Chebyshev tightness ratios via DNS. Key results: (1) tail exponent p is IC-dependent — Taylor-Green p~10 (massive slack), ABC Beltrami p~2.1 (below 10/3; Chebyshev tight or optimistic); (2) De Giorgi tightness ratios are ~3-5x and k-independent — constant multiplicative slack that does NOT improve beta. The numerical evidence confirms that direction (a) above has moderate slack of the wrong type: constant per De Giorgi level, not scaling with U_{k-1}. Full data in `dns-levelset-distribution-chebyshev-tightness.md`.

### S2-E004 Direction (b) Tested via Commutator

S2-E004 tested direction (b) — alternative to the Holder pairing in Step 5b — by attempting to use commutator estimates (CRW 1976) and compensated compactness (CLMS 1993) to improve the non-divergence pressure bound. **Confirmed non-viable within the CZ class:** three independent obstructions (no div-curl structure, commutator remainder dominance, CRW vacuous for bounded multipliers). The informal theorem: beta = 4/3 is sharp within energy + Sobolev + CZ (including commutator/CLMS) + Chebyshev. Only directions requiring structural information beyond these four ingredients remain open: nonlinear lower bounds on dissipation, frequency-localized De Giorgi, quantitative unique continuation, topological/geometric constraints. Full analysis in `compensated-compactness-commutator-obstruction.md`.

### S2-E005 LP/Frequency-Localized Route Also Non-Viable

S2-E005 tested whether Littlewood-Paley frequency decomposition could circumvent the Bernstein exchange rate and improve the pressure bound. **Non-viable:** the Bernstein factor 2^{3j/5} per LP block is exactly the dimensional cost of the Step 3b Chebyshev conversion (L^2 -> L^{10/3} requires 3/10 Sobolev derivatives). CZ already IS the optimal frequency-by-frequency estimate. LP gives 5-10x worse bounds than direct CZ. The Bony paraproduct decomposition further reveals a k-dependent character change (resonance at low k, paraproduct at high k) meaning no single analytical technique handles all De Giorgi levels. Direction 2 (frequency-localized De Giorgi) from S2-E004 is now CLOSED; three remain (nonlinear dissipation lower bounds, quantitative unique continuation, topological/geometric constraints). Full analysis in `frequency-localized-degiorgi-lp-obstruction.md`.

### S2-E006 Non-CZ Routes and the 1/2 + 5/6 Chain

S2-E006 tested three non-CZ pressure routes and confirmed the 1/2 + 5/6 chain is tool-independent. The H^1/BMO route recovers beta = 4/3 through a completely different mechanism: ||P^{21}||_{BMO} absorbs all U-dependence into a constant, and ||v_k||_{H^1} encodes the same level-set measure information via |A_k|^{1/2} * ||.||_{L^2} (Cauchy-Schwarz on H^1 norm). This confirms Step 5b (the non-divergence pressure pairing) is the structural bottleneck regardless of analytical tool, as the 1/2 (gradient) + 5/6 (measure) decomposition emerges from any method respecting the NS scaling. The IBP route gives beta = 1 (gap of exactly 1/3), quantifying the value of the Chebyshev extraction step — it provides the additional 5/6 - 1/2 = 1/3 that consolidation enables. Direction (b) (alternative to Holder pairing) is now closed by FIVE independent routes (CZ, commutator, LP, IBP, H^1/BMO); three remaining directions (nonlinear dissipation, unique continuation, topological/geometric) require structural information beyond the energy+Sobolev+CZ+Chebyshev class. Full analysis in `non-cz-pressure-routes-tool-independence.md`.

### S2-E008 Chebyshev Step Confirmed Sharp — Direction (a) CLOSED

S2-E008 proved that the Chebyshev step (identified by S2-E001 as the SINGLE potentially improvable link) is provably tight for divergence-free fields. The constant field u = (lambda+1/n, 0, 0) achieves Chebyshev ratio -> 1. Direction (a) (structural Chebyshev improvement via div-free constraint) is CLOSED. L^2 and H^1 constraints improve by constant factors only (10-200x). De Giorgi truncation is also tight. All four chain steps now confirmed tight. **All three S2-E001 directions (a, b, c) are now CLOSED within the De Giorgi-Vasseur framework.** Full analysis in `chebyshev-sharpness-constant-field-extremizer.md`.
