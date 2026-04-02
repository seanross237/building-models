---
topic: No paper since 2007 has improved beta beyond 4/3 in De Giorgi NS iteration
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-005, updated S2-E007"
---

## Finding

A comprehensive survey of post-Vasseur-2007 literature reveals that **no publication has attempted or claimed to improve the recurrence exponent beta beyond 4/3** in the De Giorgi iteration for standard Navier-Stokes regularity. The 4/3 barrier is untouched as of early 2025.

### Post-2007 Landscape Table

| Year | Authors | Result | Relation to beta |
|------|---------|--------|------------------|
| 2007 | Vasseur | New proof of partial regularity via De Giorgi | beta < 4/3 (Prop 3), bottleneck is P_k^{21} |
| 2010 | Vasseur | Higher derivatives estimate for 3D NS | Uses De Giorgi, proves nabla^2 u in L^{4/3,inf} |
| 2010 | Caffarelli-Vasseur | De Giorgi method for regularity (survey) | Pedagogical review, no beta improvement |
| 2012 | Caffarelli-Vasseur | De Giorgi method for nonlocal fluid dynamics | Extension to nonlocal operators |
| 2014 | Choi-Vasseur | Fractional higher derivatives (AIHP) | beta = 7/6 used (WEAKER, sufficient for goal) |
| 2016 | Vasseur | De Giorgi method survey (Morningside) | Review, no improvement |
| 2018 | Colombo-De Lellis-Massaccesi | CKN for hyperdissipative NS | Different framework |
| 2021 | Vasseur-Yang | Second derivatives estimate | De Giorgi on vorticity, not velocity beta |
| 2021 | Barker-Prange | Quantitative regularity | De Giorgi-type, different problem |
| 2022 | Albritton-Barker-Prange | Epsilon regularity | Weak-strong uniqueness, not De Giorgi |
| 2022 | Lei-Ren | Quantitative partial regularity | Log improvement of CKN, not De Giorgi |
| 2024 | Lei-Ren | Quantitative CKN via pigeonhole | Logarithmic improvement only, not De Giorgi |
| 2025 | Fernandez-Dalgo | Dynamic pressure decomposition | Paraboloid geometry, Gronwall, NOT beta |
| 2025 | Vasseur (arXiv:2503.02575) | Survey of De Giorgi methods | **Confirms no improvement:** "is optimal for suitable solutions" and "up to now, nobody has produced another regularity that goes beyond this for general solutions" |

### Three Orthogonal Directions the Community Pursued

1. **Higher regularity applications:** Using De Giorgi framework (accepting beta < 4/3) to prove integrability of higher derivatives (Vasseur 2010, CV14, Vasseur-Yang 2021).
2. **Alternative regularity frameworks:** Epsilon-regularity, concentration/quantitative methods, weak-strong uniqueness — different techniques entirely.
3. **Extensions to other equations:** Hyperdissipative NS, nonlocal operators.

### Strategic Implication

The absence of attempts confirms the problem is hard AND suggests that improving beta beyond 4/3 would be genuinely novel. Vasseur's Conjecture 14 (beta > 3/2 implies regularity of all suitable weak solutions) remains open. The gap from 4/3 to 3/2 is > 1/6 and no approach has narrowed it.

### S2-E007 Update: Vasseur 2025 Survey and Extended Literature

**Vasseur (March 2025, arXiv:2503.02575)** provides definitive author confirmation: the CKN result "is optimal for suitable solutions" and "up to now, nobody has produced another regularity that goes beyond this for general solutions." This is the strongest possible evidence for the barrier's persistence — the originator of the method confirming it 18 years later.

**Tao (2016, JAMS) connection:** Shows that blowup can occur for "averaged NS" — proving that any regularity proof must use the *specific algebraic structure* of the NS nonlinearity. Generic methods like De Giorgi iteration (which use only energy-level properties + quadratic structure) cannot suffice for full regularity. The mechanism-level reconstruction from `tao-averaged-ns-delayed-transfer-circuit.md` sharpens this: Tao's averaged equation embeds a deliberately engineered five-mode delayed-abrupt-transfer circuit with independently tuned couplings `ε`, `ε^2 exp(-K^10)`, `ε^(-1) K^10`, `ε^(-2)`, `K`. The concrete firewall question for exact NS is therefore not "do generic energy/cancellation/scaling features survive?" but "can the exact NS triadic geometry realize or forbid this coupling architecture?"

**Additional papers found (S2-E007, extending from 12 to 15):** Tang-Yu (2015, CMP) fractional NS; Colombo-Haffter (2020, JDE) global regularity for alpha near 5/4; Ozanski (2023, Analysis & PDE) fractional NS for Leray-Hopf. All concern modified equations (different scaling), consistent with the obstruction being specific to s=1, n=3.

See also: `s2-adversarial-review-beta-four-thirds.md` for the full adversarial assessment.
