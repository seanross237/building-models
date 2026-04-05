---
topic: Strategy-002 adversarial review — beta = 4/3 obstruction confirmed, novel claim rankings, Tao supercritical connection
confidence: verified
date: 2026-03-30
source: "vasseur-pressure strategy-002 exploration-007"
---

## Finding

Comprehensive adversarial review of the Strategy-002 beta = 4/3 obstruction result. **All seven closure arguments survive attack, all three combination attacks fail, and a 15-paper literature search confirms no published improvement since 2007.** Vasseur himself confirmed this in a March 2025 survey (arXiv:2503.02575). Five novel claims ranked by publishability; Claims 1-4 combined form a publishable paper. Six missing directions identified, with SDP formalization ranked highest priority.

## Literature Search (15 papers)

Three categories of post-2007 work identified:
1. **Same beta, more extracted:** Vasseur (2010), Choi-Vasseur (2014), Vasseur-Yang (2021) — sharper derivative estimates in better function spaces, but beta = 4/3 unchanged.
2. **Better beta for modified equations:** Fractional NS with (-Delta)^alpha, alpha > 1 — Tang-Yu (2015), Colombo-De Lellis-Massaccesi (2018/2022), Colombo-Haffter (2020), Ozanski (2023). At alpha = 5/4 the gap closes completely.
3. **Alternative approaches bypassing De Giorgi:** Lei-Ren (2024, logarithmic improvement via pigeonhole), Barker-Prange (2021, quantitative blowup rates), Albritton-Barker-Prange (2023, weak-strong uniqueness epsilon-regularity).

**Key addition:** Vasseur (2025, arXiv:2503.02575) states CKN partial regularity "is optimal for suitable solutions" and "up to now, nobody has produced another regularity that goes beyond this for general solutions."

## Tao (2016) Supercritical Barrier Connection

Tao (2016, JAMS) shows that any proof of global regularity must use the *specific algebraic structure* of the NS nonlinearity — generic methods like De Giorgi iteration on the energy inequality cannot suffice. This independently explains why beta = 4/3 is stuck: the De Giorgi framework uses only energy-level structural information (Sobolev, Chebyshev, CZ), not the specific NS nonlinearity beyond its quadratic structure.

## Seven Route Attacks — All Closures Hold

| Route | Attack attempted | Weakness found? | Verdict |
|-------|-----------------|-----------------|---------|
| 1. Modified functional | Non-L^2 energies, vorticity, Orlicz | Speculative only | Closure holds (weakest) |
| 2. Improved Sobolev | NS structure beyond div-free | No | Closure holds (strong) |
| 3. Optimized truncation | Frequency, multi-scale, div-preserving | No | Closure holds |
| 4. Chebyshev circularity | Non-integer s, loopholes | No | Closure holds (exact formula) |
| 5. DNS representativeness | Near-singular solutions | Legitimate but mitigated by ABC | Closure holds (with caveat) |
| 6. Different commutator | Fractional, Coifman-Meyer | Wrong bottleneck | Closure holds |
| 7. Anisotropic LP | Direction-dependent Bernstein | Total cost unchanged | Closure holds |

**Weakest closure:** Route 1 (modified functional) — not because a specific improvement is known, but because the space of non-standard functionals is large and unexplored. **Strongest challenge:** Route 5 (DNS representativeness) — legitimate concern mitigated by ABC Beltrami example already showing Chebyshev-tight distribution.

## Three Combination Attacks — All Fail

1. **Commutator + LP:** Both methods work in easy regimes (low k AND low j); both fail in the hard regime (high k AND high j) simultaneously.
2. **Modified functional + improved embedding:** Gains from better embedding exactly offset by worse nonlinear estimates (higher-order functional requires controlling more nonlinear terms).
3. **Truncation + compensated compactness:** Div-free-preserving truncations either destroy De Giorgi iteration structure (spectral) or introduce nonlocal complications (Leray projection) that negate compensated compactness gains.

**Structural coherence:** The failures reflect tight interlocking of the three core ingredients (amplitude truncation, H^1->L^6 Sobolev, L^{10/3} Chebyshev). No combination can escape all three simultaneously.

## Novel Claim Rankings

| Claim | Correctness | Novelty | Significance | Publishability | Fatal flaw? |
|-------|-------------|---------|--------------|----------------|-------------|
| 3. Seven-route informal sharpness | 7/10 | 8/10 | 8/10 | 6/10 | Informal — needs formalization |
| 2. SQG-NS structural gap | 9/10 | 6/10 | 6/10 | 4/10 | "Obvious" to experts |
| 4. Div-free level-set question | 9/10 | 8/10 | 5/10 | 4/10 | Likely negative for pure div-free |
| 1. Beta = 1+s/n formula | 7/10 | 5/10 | 4/10 | 3/10 | Folklore/elementary |
| 5. Paraproduct transition | 7/10 | 5/10 | 3/10 | 2/10 | Computational only |

**Most publishable combination:** Claims 1-4 as a single paper: "On the sharpness of the De Giorgi exponent beta = 4/3 for 3D Navier-Stokes." The paper would present the universal formula (Claim 1), the systematic seven-route obstruction (Claim 3), the SQG comparison (Claim 2), and the div-free open question (Claim 4).

**Claim 3 (seven-route obstruction) is most significant** — the systematic closure of seven routes with clear mathematical reasons per route is genuinely new work. The strongest counterargument ("class of techniques not well-defined") is serious but mitigated by the fact that seven specific routes span the natural approaches and each closure is individually rigorous.

**Claim 4 caveat:** Axisymmetric toroidal field u(x) = f(|x|)(x x e_z)/|x| is divergence-free with |u(x)| = |f(|x|)| an arbitrary radial profile — likely kills the pure div-free version. The NS-specific version (does NS dynamics improve level sets?) remains genuinely open but is essentially the millennium problem.

## Missing Directions Identified

| Direction | Novelty | Feasibility | Potential | Priority |
|-----------|---------|-------------|-----------|----------|
| SDP/computer-assisted | High | High | Medium-High | **1st** |
| Non-CZ pressure (E006) | Medium | High | Medium | **2nd** (since completed) |
| Probabilistic/stochastic | High | Medium | Medium | 3rd |
| Geometric level sets | Medium | Low | Low-Medium | 4th |
| Turbulence scaling | Low | Low | Low | 5th |
| Microlocal analysis | Low | Low | Low | 6th |

**SDP approach is most actionable:** Set up SDP (sum-of-squares relaxation) to find the optimal bound on |{|u| > lambda}| given all available NS constraints (div-free, energy inequality, Sobolev bounds). If SDP returns beta > 4/3, there's an improvement. If 4/3, it's a computer-assisted sharpness proof. This would upgrade Claim 3 from informal to rigorous.

## Remaining Challenges

1. **Claim 3 needs formalization** — without rigorous definition of "the class of energy+Sobolev+CZ+Chebyshev techniques," the claim is a summary of failed attempts, not a theorem.
2. **E006 gap closed** — non-CZ pressure handling completed (beta = 4/3 is tool-independent).
3. **SDP formalization path** identified as most actionable next step for rigorous sharpness.

## Cross-References

- `post-2007-beta-landscape.md` — Vasseur 2025 survey now added as definitive confirmation
- `compensated-compactness-commutator-obstruction.md` — three combination attacks tested against its findings
- `chebyshev-universality-and-model-pde-comparison.md` — Claim 1 (beta formula) and Claim 2 (SQG gap) verified
- `strategy-001-adversarial-synthesis.md` — S1 adversarial precedent; S2 review is broader (7 routes vs 6 claims)
- `non-cz-pressure-routes-tool-independence.md` — E006 completed after E007 review flagged it as gap
