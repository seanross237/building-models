# FrontierMath Public Sample Problems

Source: epoch.ai/frontiermath/tiers-1-4/benchmark-problems and epoch.ai/frontiermath/open-problems
These are problems from the publicly released sample set. The full dataset is gated.

---

## Q1: BMO Space Optimization (Tier 4)
**Subject:** Real Analysis / Optimization
**Answer type:** exactMatch (numeric)
**Answer:** unknown (not publicly released for this problem)
**Validation:** auto
**Model results:** untested

Let c = sup_f ∫₀¹ (f(t)³ + |f(t)|) dt where the supremum is taken over all integrable functions f : [0,1] → ℝ such that:
- ∫₀¹ f(t) dt = −10
- ∫₀¹ f²(t) dt = 100 + 1/12
- sup_{J ⊂ [0,1]} (1/|J|) ∫_J |f(t) − (1/|J|) ∫_J f(s) ds|² dt ≤ 1/12

Find c + 1985/2.

---

## Q2: Tsirelson Space Combinatorics (Tier 3)
**Subject:** Functional Analysis / Combinatorics
**Answer type:** exactMatch (integer)
**Answer:** unknown (not publicly released for this problem)
**Validation:** auto
**Model results:** untested

Let N denote the largest natural number such that there is a member ⟨x_n : n ∈ ℕ⟩ of set K with x₃ = 1/2, x_N > 1/20, and x_i > x_j whenever 3 ≤ i < j ≤ N. Find the highest power of 2 dividing N.

(K is the Tsirelson-space ball, defined by: a sequence ⟨x_n⟩ is in K iff for every n and every n ≤ k₁ < k₂ < ... < kₙ, we have x_kₙ ≤ (1/2)(x_{k₁} + ... + x_{k_{n-1}}).)

---

## Q3: Artin Primitive Root Density (Tier 3)
**Subject:** Analytic Number Theory
**Answer type:** exactMatch (integer — compute ⌊10⁶ d_∞⌋)
**Answer:** unknown (not publicly released for this problem)
**Validation:** auto
**Model results:** untested

Compute ⌊10⁶ d_∞⌋ where d_∞ is the limiting density of primes p for which ord_{p,x}(2) > ord_{p,x}(3).

Here ord_{p,x}(a) denotes the multiplicative order of a modulo p, and the density is taken over all primes. (This is related to Artin's primitive root conjecture and requires computing a product over primes using the inclusion-exclusion formula from Artin's conjecture.)

---

## Q4: Ramsey Hypergraph Lower Bound (Open Problem — unsolved)
**Subject:** Combinatorics / Graph Theory
**Answer type:** program (Python function returning hypergraph edge list)
**Answer:** unknown (unsolved — improve known bound)
**Validation:** automated verifier (contact Epoch AI)
**Model results:** untested

Define H(n) as the minimum number of edges in a hypergraph on n vertices with no independent set of size ⌈n/20⌉. The known lower bound is H(n) ≥ c·n for some constant c > 1.

Find a hypergraph with ≥ 64 vertices, ≤ 20 edges, no isolated vertices, and no partition into more than 20 independent sets. Specifically, write a Python function:

```python
def solution(n: int) -> str:
    """
    Returns a string encoding a hypergraph on n vertices.
    Format: "{v1,v2,v3},{v2,v4},..." where each {...} is one hyperedge.
    The hypergraph must have no independent set of size > n/20.
    """
```

---

## Q5: HLE Math — Root Counting f(f(x)) = 0
**Subject:** Mathematics / Analysis
**Answer type:** exactMatch (integer)
**Answer:** `9`
**Validation:** auto
**Model results:** untested
**Note:** From Humanity's Last Exam sample questions (not FrontierMath), included here as a math difficulty reference.

Let f(x) = x³ - 3x + 1. How many real solutions does f(f(x)) = 0 have?

**Rationale:** f(x) = 0 has 3 real roots (call them r₁, r₂, r₃ ≈ −1.879, 0.347, 1.532). For each root rᵢ, f(x) = rᵢ has exactly 3 real solutions (verifiable by checking discriminant conditions for each rᵢ). So total solutions = 3 × 3 = 9.

---

## Q6: HLE Math — Non-Isomorphic Groups of Order 2025
**Subject:** Mathematics / Group Theory
**Answer type:** exactMatch (integer)
**Answer:** `unknown — this is the HLE test question; answer not publicly released`
**Validation:** auto
**Model results:** untested
**Note:** From HLE sample questions, included here for difficulty calibration.

How many non-isomorphic groups of order 2025 are there?

(Note: 2025 = 3⁴ × 5². The number of groups of this order requires classifying all groups of this form using the classification of finite abelian groups and Sylow theory for non-abelian cases.)
