---
topic: Vasseur beta current value 4/3 — bottleneck analysis
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-001; Vasseur 2007 Section 4"
---

## Finding

The current best beta in Vasseur's De Giorgi iteration is **strictly less than 4/3**. This comes from a single bottleneck term: the non-divergence part of the local pressure P_k^{21}.

### Term-by-term exponent table

| Term | Source | Exponent of U_{k-1} | vs 3/2? |
|------|--------|---------------------|---------|
| Transport: int|v_k|^2 | Sobolev + Chebyshev | **5/3** | > 3/2 |
| Transport: int|v_k|^3 | Sobolev + Chebyshev | **5/3** | > 3/2 |
| Nonlocal pressure P_k^1 | Harmonic regularity + Chebyshev | **5/3(1-1/p)** -> 5/3 | > 3/2 for p > 10 |
| Local pressure P_k^{21} (divergence part) | CZ + Chebyshev | **5/3(1-1/q)** -> 5/3 | > 3/2 for large q |
| **Local pressure P_k^{21} (non-divergence part)** | **CZ + L^2 of d_k** | **4/3 - 5/(3q)** -> **4/3** | **< 3/2** |
| Local pressure P_k^{22}, P_k^{23} | CZ + Sobolev | **5/3** | > 3/2 |

### Why P_k^{21} is the bottleneck

The pressure P_k^{21} satisfies -Delta P_k^{21} = Sum_{i,j} partial_i partial_j [phi_k u_j(1 - v_k/|u|) u_i(1 - v_k/|u|)]. The factors u(1-v_k/|u|) are BOUNDED BY 1 (Lemma 10), so the RHS is bounded independently of U_{k-1}. By CZ/Riesz: ||P_k^{21}||_{L^q} <= C_q. No additional power of U_{k-1} can be extracted.

The non-divergence term gives:
```
int int |P_k^{21}| * |div(u*v_k/|u|)| dx dt  <=  ||P_k^{21}||_{L^q} * ||d_k||_{L^2} * ||1_{v_k>0}||_{L^{2q/(q-2)}}
```

Combined exponent: 1/2 + 5(q-2)/(6q) = 4/3 - 5/(3q), approaching 4/3 from below as q -> inf.

### The fundamental obstruction

**The pressure is not small even when the velocity is close to its level set truncation.** P_k^{21} contributes U_{k-1}^0 = 1 to the exponent, while all other terms contribute at least U_{k-1}^{1/2}.

### Gap to regularity

The gap is 1/6 = 3/2 - 4/3. This is NOT "small" in perturbation theory terms — it represents a qualitative failure where the current method cannot extract enough nonlinearity from the pressure's interaction with the level sets. The 4/3 bound is also NOT tight; it comes from worst-case Holder pairings.

### Possible routes to close the gap

1. Better pressure regularity for P_k^{21} (beyond generic CZ)
2. Sign/cancellation properties in the non-divergence term
3. Modified iteration (different v_k or different decomposition)
4. Exploit the specific structure of P_k^{21}'s RHS (bounded factors)

### S2-E001 Sharpness Audit Cross-Reference

A complete line-by-line sharpness audit (Strategy-002, Exploration 001) traces every sub-exponent and classifies all 5 free parameters as exhausted. The ONLY potentially improvable step is the Chebyshev inequality applied to NS solutions (tight for general L^{10/3} functions but potentially loose for functions satisfying NS). The full sensitivity table and 5/6 genealogy are in `proposition-3-sharpness-audit.md`.

### S2-E003 Universal Formula and Chebyshev Circularity

S2-E003 established the universal formula beta = 1 + s/n for De Giorgi iterations across dissipative PDEs (confirmed on Burgers, 2D NS, 3D NS, SQG, MHD, fractional NS). The 4/3 for 3D NS is NOT NS-specific — it is the generic dimensional value for H^1 dissipation in 3D. Furthermore, the Chebyshev step identified by S2-E001 as the single improvable link is NOT independently improvable: all six potential improvement routes (support-restricted, Holder interpolation, Lorentz refinement, gradient/isoperimetric, L^2 Chebyshev, PDE-based integrability) either fail or reduce to the original regularity problem. Improving L^{10/3} to L^4 Chebyshev requires H^{5/4} regularity (the Lions threshold). Full analysis in `chebyshev-universality-and-model-pde-comparison.md`.

### S2-E004 Compensated Compactness / Commutator Route Closed

S2-E004 tested whether compensated compactness (CLMS div-curl lemma) or commutator estimates (CRW) could improve the CZ bound on P^{21} and thereby improve beta. **Definitively closed** at three independent levels: (1) no div-curl structure — truncation breaks div(u)=0 with O(1) compressibility error; (2) commutator decomposition remainder dominates (61% of P^{21} in L^2, 18x at high frequencies); (3) CRW is vacuous for bounded multipliers (u^{below} is bounded, so ||u^{below}||_{BMO} = O(||u^{below}||_{L^infty})). Informal theorem: beta = 4/3 is sharp within the class of methods using energy inequality + Sobolev/interpolation + CZ theory (including commutator/CLMS variants) + Chebyshev estimates. To beat 4/3, one must inject structural information beyond these four ingredients. Full analysis in `compensated-compactness-commutator-obstruction.md`.

### S2-E005 Frequency-Localized De Giorgi (LP Decomposition) Route Closed

S2-E005 tested whether Littlewood-Paley frequency decomposition of P^{21} could bypass the 4/3 barrier by applying stronger estimates on low-frequency modes. **Definitively closed** by four independent lines of evidence: (1) spectral peak of P^{21} shifts to higher frequencies with k (wrong direction); (2) high-frequency fraction of bottleneck integral grows from ~1% at k=1 to ~20% at k=6; (3) Bernstein inflation makes LP 5-10x worse than direct CZ; (4) all three LP approaches (Bernstein+L^2, commutator+Bernstein, paraproduct blocks) introduce a growing 2^{alpha J} factor. CZ IS the optimal frequency-by-frequency estimate; LP reveals the structure CZ handles implicitly, without improvement. Bernstein exchange rate 2^{3j/5} is dimensional and structural (Sobolev embedding cost in 3D). Additionally, paraproduct analysis reveals k-dependent character change: resonance dominates at low k, paraproduct at high k, so no single technique handles all De Giorgi levels. Of the four directions identified by S2-E004, LP (direction 2) is now closed; three remain (nonlinear dissipation lower bounds, quantitative unique continuation, topological/geometric constraints). Full analysis in `frequency-localized-degiorgi-lp-obstruction.md`.

### S2-E006 Non-CZ Pressure Routes and Tool-Independence

S2-E006 computed three non-CZ routes for bounding the pressure integral: (1) direct integration by parts (IBP) gives beta = 1 (WORSE by 1/3); (2) H^1/BMO duality gives beta = 4/3 (MATCHES CZ exactly via different mechanism); (3) commutator variant (CRW) gives beta <= 1 (same as IBP). Also tested: W^{-1,q'}/W^{1,q} corrected to beta <= 4/3; Lorentz refinement unchanged at 4/3. The CZ consolidation gain is exactly 1/3 — mapping the bilinear product into a single L^p function enables the Chebyshev level-set bound. Survey of 12 published approaches confirms NO method achieves beta > 4/3 (barrier has stood since 2007). DNS verification shows CZ 2-3x tighter than direct at low k, but CZ becomes loose at high k (ratio P^{21}/v_{k-1}^2 grows from 0.2 at k=2 to 92 at k=5). Both bounds overestimate I_actual by 5-20x (consistent with nonlinearity depletion). Two genuinely untested approaches identified: Wolf's local pressure decomposition (CZ-free) and Tran-Yu depletion (unquantified at De Giorgi levels). **Key structural conclusion: beta = 4/3 is TOOL-INDEPENDENT — the exponent is locked to the NS quadratic structure, not to any analytical method.** Full analysis in `non-cz-pressure-routes-tool-independence.md`.

### S2-E007 Adversarial Review — Obstruction Confirmed

S2-E007 adversarial review stress-tested the entire S2 obstruction result: (1) 15-paper literature search found no published improvement, with Vasseur (2025, arXiv:2503.02575) confirming the barrier; (2) all 7 closure arguments withstand attack — weakest is Route 1 (modified functional, speculative only); (3) all 3 combination attacks fail for structural reasons (tight interlocking of truncation, Sobolev, Chebyshev); (4) Tao (2016) independently explains why generic methods cannot resolve NS regularity. Novel claims ranked: seven-route obstruction (Claim 3) most significant at 8/10 novelty + 8/10 significance; Claims 1-4 combined publishable as "On the sharpness of the De Giorgi exponent beta = 4/3 for 3D Navier-Stokes." SDP formalization identified as most actionable next step for upgrading informal sharpness to rigorous. Full analysis in `s2-adversarial-review-beta-four-thirds.md`.

### S2-E008 Chebyshev Sharpness — All 4 Chain Steps Tight, beta = 4/3 SHARP (Rigorous)

S2-E008 proved that the Chebyshev bound is **provably tight for divergence-free fields**: the constant vector field u_n = (lambda + 1/n, 0, 0) is div-free, in H^1, and achieves Chebyshev ratio -> 1. This closes the SINGLE potentially improvable step identified by S2-E001. All four De Giorgi chain steps (energy, Sobolev, interpolation, Chebyshev) are now individually confirmed tight under NS constraints. The constant div-free field simultaneously extremizes three of the four steps. Key structural insight: div-free constrains the DIRECTION field, not the magnitude distribution, so it cannot improve Chebyshev. The L^2 and H^1 constraints improve the bound by constant factors only (10-200x), never changing the exponent. De Giorgi truncation is also tight (truncated constant field is constant). **beta = 4/3 is rigorously optimal within the De Giorgi-Vasseur framework — no step in the chain admits improvement.** The SDP formalization identified by S2-E007 as top priority turned out to be unnecessary; the analytic extremizer is elementary. Full analysis in `chebyshev-sharpness-constant-field-extremizer.md`.
