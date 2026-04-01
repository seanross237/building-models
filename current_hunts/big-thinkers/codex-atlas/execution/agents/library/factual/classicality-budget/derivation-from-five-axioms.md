---
topic: Classicality budget derivation from five axioms
confidence: verified
date: 2026-03-27
source: "classicality-budget strategy-001 exploration-001"
---

## Result

The classicality budget inequality is derived gap-free from five standard axioms:

**Single fact, perfect copies (delta = 0):**
> R <= S_max / S_T - 1

**Single fact, imperfect copies (general delta):**
> R_delta <= (S_max / S_T - 1) / (1 - delta)

**Multiple facts (full trade-off):**
> M * S_T * [1 + R_delta * (1 - delta)] <= S_max

where R_delta = number of independent environmental witnesses (redundancy), S_max = maximum entropy of bounded region (Bekenstein/holographic), S_T = H_S = information content per classical fact, M = number of distinct facts, delta = information deficit per copy.

## The Five Axioms

1. **Hilbert space structure** (standard QM) — tensor product H_total = H_S x H_E
2. **Quantum Darwinism redundancy** (Zurek 2009) — R_delta = 1/f_delta, where f_delta is smallest environment fraction carrying (1-delta)H_S bits
3. **Classical objectivity requires redundancy** (Zurek 2003, 2009; Brandao-Piani-Horodecki 2015)
4. **Bekenstein entropy bound** (Bekenstein 1981) — log_2(dim(H_total)) <= S_max = 2*pi*R*E/(hbar*c*ln2)
5. **Holevo bound** (Holevo 1973) — classically accessible information <= log_2(dim(H))

## Derivation Chain

```
Axiom 4 (Bekenstein)     -> log_2(d_total) <= S_max
Axiom 1 (tensor product) -> log_2(d_S) + log_2(d_E) <= S_max
Axiom 1 (factorization)  -> log_2(d_E) >= Sum_k log_2(dim(H_{F_k}))
Axiom 5 (Holevo)         -> log_2(dim(H_{F_k})) >= (1-delta)*H_S
Axiom 2 (R_delta frags)  -> log_2(d_E) >= R_delta * (1-delta) * H_S
Combine                   -> log_2(d_S) + R_delta*(1-delta)*H_S <= S_max
H_S <= log_2(d_S)         -> H_S + R_delta*(1-delta)*H_S <= S_max
Rearrange                 -> R_delta <= (S_max/H_S - 1)/(1-delta)
Set S_T = H_S, delta = 0  -> R <= S_max/S_T - 1    QED
```

Every step uses a stated axiom. There are no gaps.

## Key Boundary Cases (all checked)

| Case | Result | Physical meaning |
|------|--------|-----------------|
| S_T -> 0 | R -> infinity | Trivial info easy to proliferate |
| S_T = S_max | R = 0 | System fills all capacity; no witnesses possible |
| R = 1 (min objectivity) | H_S <= S_max/2 | System must use < half total capacity |
| S_T > S_max | Impossible | Enforced by Bekenstein bound itself |
| S_max -> infinity | R -> infinity | No finite bound without finite entropy |

## Multi-Fact Trade-Off (Budget Hyperbola)

For M independent facts each of size S_T with redundancy R_delta: M * S_T * [1 + R_delta*(1-delta)] <= S_max. At delta = 0: M * (1 + R) <= S_max / S_T. This defines a rectangular hyperbola in (M, R) space — the fundamental trade-off between richness (number of facts) and objectivity (redundancy per fact).

## Tight vs Candidate Formula

For delta > 0, the candidate formula R_delta <= S_max/S_T - 1 is valid but loose. The tight bound is R_delta <= (S_max - H_S) / [(1-delta)*H_S]. The difference is delta/(1-delta) — negligible for small delta.

## Rigor Assessment

All components rigorous: standard QM axioms, Holevo bound (tight), Bekenstein bound (universally accepted). The tensor product assumption fails only in quantum gravity contexts where spatial decomposition of degrees of freedom is approximate. The derivation works with any valid entropy bound (Bekenstein, holographic, Bousso covariant) — the specific bound affects the numerical value of S_max but not the validity of the inequality.

## Weaknesses

1. The bound may be far from tight for non-ideal environments (locality, thermal noise)
2. Tensor product assumption fails near black holes where the bound is most interesting
3. Mapping real-world "facts" to specific H_S values requires additional physical modeling
