# Route: Smith Transfer -- Making Smith's Twist-Family Result Uniform

**Goal:** Transfer Smith's per-family density-zero result for rank >= 2 in quadratic twist families to a density-zero result for ALL elliptic curves ordered by height. If successful: classical BSD for 100% of curves.

**Status:** FUNDAMENTAL OBSTRUCTION IDENTIFIED

**Bottom line:** The naive transfer from twist families to height ordering FAILS -- not because of Smith's convergence rate, but because the height function grows as d^6 under twisting, so most curves ordered by height have twist depth D ~ 1 where Smith's asymptotic result provides no information. The conductor ordering is better (D ~ sqrt(N/N_0)) but still insufficient. This route CANNOT work without fundamentally new ideas beyond making Smith's rate uniform.

---

## 1. Smith's Results: What Is Actually Proved

### 1.1 The Three Smith Papers

**Paper I: arXiv:1702.02325 (2017, unsubmitted)**
- Title: "2^infinity-Selmer groups, 2^infinity-class groups, and Goldfeld's conjecture"
- Result: For E/Q with full rational 2-torsion and no rational cyclic 4-subgroup, the 2^infinity-Selmer groups of quadratic twists have the Delaunay distribution. In particular, among twists E^d with |d| < N, the number with rank >= 2 is o(N).
- Restriction: Requires E[2](Q) = (Z/2Z)^2 and no cyclic 4-isogeny.

**Paper II: arXiv:2207.05674 + arXiv:2207.05143 (2022, to appear in JAMS)**
- Title: "The distribution of l^infinity-Selmer groups in degree l twist families I & II"
- Result (Theorem 1.2): For E/Q satisfying Assumption 1.1, the density of quadratic twists with 2^infinity-Selmer corank r is 1/2 for r in {0,1} and 0 for r >= 2.
- Assumption 1.1 requires ONE of:
  (1) A(Q)[2] = 0
  (2) A(Q)[2] = Z/2Z with certain isogeny conditions
  (3) A(Q)[2] = (Z/2Z)^2 with no cyclic degree-4 isogeny over Q
- "Most" E/Q satisfy Assumption 1.1 (since most have trivial torsion, by Bhargava et al.)
- **KEY: Remark 1.3 gives explicit rate** (see Section 2 below)

**Paper III: arXiv:2503.17619 (2025, submitted)**
- Title: "The Birch and Swinnerton-Dyer conjecture implies Goldfeld's conjecture"
- Result (Theorem 1.1): For ANY E/Q, the density of quadratic twists with 2^infinity-Selmer corank r is 1/2 for r in {0,1} and 0 for r >= 2.
- Removes ALL technical conditions on E from the 2022 paper.
- The 2-Selmer rank distribution in Cases IV and V (balanced isogenies) differs from the Poonen-Rains model:
  - Case I (generic): P(high Selmer rank) ~ 2^{-r^2/2}
  - Case IV (one balanced isogeny): ~ 2^{-3r^2/8}
  - Case V (two balanced isogenies): ~ 2^{-r^2/4}
- No explicit convergence rate stated.

### 1.2 Smith's Proof Method

Smith's 2025 proof does NOT use a classical Markov chain/random walk. The architecture is:

1. **Case analysis on 2-torsion structure:** Curves classified into Cases I-V based on isogeny structure.
2. **Random matrix model:** Distribution of 2^k-Selmer ranks governed by P^Mat(r | m x n) and P^Alt(r | n) from random matrices/alternating forms over F_2.
3. **Fixed point Selmer group:** The "base layer" of the l^infinity-Selmer group. When "stable" across a grid class, the 2^k-Selmer ranks form a Markov chain (Theorem 1.5, JAMS paper).
4. **Cassels-Tate pairing:** Transitions governed by kernel dimensions of alternating forms from Cassels-Tate pairings. Equidistribution of quadratic residue symbols (Chebotarev) drives randomness.
5. **Grid + regridding:** Squarefree integers partitioned by factoring through disjoint prime sets. Regridding (Section 6, JAMS) handles passage to natural ordering.
6. **Isogeny duality (2025):** Proposition 1.18 decomposes r_{2^infinity}(E^d) via dual isogenies.

### 1.3 The Klagsbrun-Mazur-Rubin Markov Model (Separate)

KMR (2013, arXiv:1303.6507) constructed an explicit Markov model:
- Transition: from Selmer rank r, go to r-1 with prob (1 - 2^{-r}), go to r+1 with prob 2^{-r}
- Stationary distribution: c_n = prod_{j>=1}(1+2^{-j})^{-1} * prod_{j=1}^n 2/(2^j-1)
- **Key:** Transition probabilities INDEPENDENT OF E. Only initial distribution depends on E.
- Convergence uses effective Chebotarev bounds, not spectral gaps.

---

## 2. The Explicit Convergence Rate

### 2.1 Smith's Bound (Remark 1.3, arXiv:2207.05674)

**Exact statement:** Given A/Q satisfying Assumption 1.1, there exist positive constants c, C > 0 such that for H > C:

    #{d in Z : 0 < |d| <= H and r_{2^inf}(A^d/Q) >= 2} / (2H) <= exp(-c * (log log log H)^{1/2})

### 2.2 E-Dependence of Constants

**c and C depend on E.** Sources of dependence:

1. **Effective Chebotarev:** For K = Q(E[2])/Q, the error degrades as ~ 1/sqrt(log disc(K/Q)). Since disc(K/Q) <= N(E)^6 and [K:Q] <= 6, this is ~ 1/sqrt(log N(E)). Very mild.

2. **Grid construction:** O(log N(E)) bad primes.

3. **Fixed point Selmer group stability:** May need different grid sizes.

**Plausible estimate:** c(E) >= c_0 / (log N(E))^{1/2} for absolute c_0 > 0.

### 2.3 Rate Analysis

| H | (log log log H)^{1/2} | exp(-c * ...) for c=1 |
|---|---|---|
| 10^10 | 1.07 | 0.34 |
| 10^100 | 1.30 | 0.27 |
| 10^1000 | 1.43 | 0.24 |
| 10^(10^6) | 1.74 | 0.18 |

Triply-logarithmic convergence is EXTREMELY slow. Smith notes this is "about two logarithms better than" conjectured H^{-1/4+eps}.

---

## 3. THE FUNDAMENTAL OBSTRUCTION: Transfer Fails

### 3.1 Setup

Every E/Q in short Weierstrass form y^2 = x^3 + ax + b is uniquely E_0^d where E_0 is twist-minimal and d is squarefree. The key relationship:

    **ht(E_0^d) = d^6 * ht(E_0)**

So twists with height <= H satisfy |d| <= D(E_0) := (H/ht(E_0))^{1/6}.

### 3.2 The Weight Distribution Problem

Among all curves with ht <= H, decompose by twist class. The proportion with rank >= 2 is a weighted average:

    prop(rank >= 2) = sum_{E_0} w(E_0) * f(E_0, D(E_0))

where w(E_0) = D(E_0) / sum D and f is the proportion of twists with rank >= 2.

The CDF of the weight distribution is **(h_0/H)^{2/3}**, where h_0 = ht(E_0).

**This means:**

| h_0/H | Weight below | D(E_0) at boundary |
|---|---|---|
| 0.001 | 1.0% | 3.16 |
| 0.01 | 4.6% | 2.15 |
| 0.10 | 21.5% | 1.47 |
| 0.50 | 63.0% | 1.12 |
| 0.90 | 93.2% | 1.02 |
| 0.99 | 99.3% | 1.00 |

**50% of the weight comes from E_0 with twist depth D <= 1.19.
90% from D <= 1.56. 99% from D <= 2.15.**

### 3.3 Why This Kills the Transfer

Smith's result says f(E_0, D) -> 0 as D -> infinity. But for D ~ 1 (which carries most of the weight), Smith's bound is vacuous. The proportion f(E_0, 1) is just "is E_0 itself rank >= 2?", which could be 0 or 1.

The weighted average is dominated by curves that are barely twisted (d = 1 or d small), where Smith's asymptotic result provides no information.

**Even with a uniform rate:** exp(-c * (log log log D)^{1/2}) * log(H) -> INFINITY, not zero. The log(H) factor from summing over twist classes overwhelms the triply-logarithmic decay.

Concretely: at H = 10^48, the bound with c = 1 gives exp(-1.3) * log(10^48) ~ 0.27 * 110 ~ 30. Far from zero.

### 3.4 Primitivity Confirms the Problem

Verification: among (a,b) pairs with max(4|a|^3, 27b^2) <= 10^6, exactly **96.4% are twist-minimal** (no prime p with p^2|a and p^3|b). The primitive fraction is 1/zeta(5) = 0.9644.

So 96.4% of curves ARE their own minimal twist representative. For these, there are no other twists to average over. Smith's family result is irrelevant.

### 3.5 Conductor Ordering: Better But Still Fails

Under quadratic twist, conductor grows as d^2 (not d^6), so conductor ordering gives deeper twist penetration:

| N_0/N | Weight below | D at boundary |
|---|---|---|
| 0.001 | 10.0% | 31.6 |
| 0.01 | 21.5% | 10.0 |
| 0.10 | 46.4% | 3.2 |
| 0.50 | 79.4% | 1.4 |
| 0.90 | 96.5% | 1.1 |

Better than height ordering (50% of weight at D ~ 2.8 vs D ~ 1.2), but still most weight is on barely-twisted curves.

### 3.6 The "Wrong Direction" Problem

The deepest way to understand the obstruction:

- **Smith controls the twist direction:** Fix E_0, vary d. Among d=1,...,D, rank >= 2 is rare.
- **Height ordering needs the base curve direction:** Fix d, vary E_0. Among E_0 with ht <= X, what fraction have rank(E_0^d) >= 2?

For **d = 1**: "what fraction of E_0 have rank >= 2?" This IS the original question. Smith provides zero information.

For **d = 2**: "what fraction of E_0 have rank(E_0^2) >= 2?" By Bhargava-Shankar applied to the family {E_0^2 : ht(E_0) <= X}, the average Sel_p is still sigma(p), giving the same 16.25% bound. Each fixed d gives the SAME bound independently.

**Analogy:** Knowing that a random COLUMN of a matrix is mostly zero does NOT tell you that a random ROW is mostly zero. Smith slices the (E_0, d) parameter space along columns (fixed E_0, varying d). Height ordering samples along rows (fixed d = 1, varying E_0). The information is orthogonal.

### 3.7 Formal Statement of the Obstruction

**Proposition.** Let f_E(D) be the proportion of quadratic twists E^d with |d| <= D having rank >= 2. Suppose f_E(D) <= g(D) for all E and some function g with g(D) -> 0 as D -> infinity. Then the naive transfer:

    prop(rank >= 2 | ht <= H) <= sum_{E_0} w(E_0) * g(D(E_0))

does NOT necessarily go to zero because the weight w is concentrated on E_0 with D(E_0) ~ 1.

Specifically, for g(D) = exp(-c * (log log log D)^{1/2}):

    sum w(E_0) * g(D(E_0)) >= (1 - epsilon) * g(H^{epsilon/6})

and g(H^{epsilon/6}) = exp(-c * (log log(epsilon * log H / 6))^{1/2}) which goes to 0 only triply-logarithmically, while the weight on the complementary region (1 - epsilon) approaches 1.

The product does NOT tend to zero because the weight on barely-twisted curves (g ~ 1) dominates.

---

## 4. What CAN Smith's Result Do?

Despite the transfer failing for height ordering, Smith's result has genuine content:

### 4.1 Density Zero in Twist Families (Proved)

For any FIXED E, among its quadratic twists, rank >= 2 has density zero. This is unconditional and applies to every E/Q.

### 4.2 Conditional BSD in Twist Families

Combined with known results:
- Smith: 2^inf-Selmer corank <= 1 for 100% of twists
- If 2^inf-Selmer corank = rank (true under BSD): rank <= 1 for 100% of twists
- Rank 0 BSD proved (Kato + Kolyvagin + Gross-Zagier)
- Rank 1 BSD proved (Gross-Zagier + Kolyvagin + BCS)
- Therefore: BSD for 100% of twists of E (conditional on BSD implying rank = 2^inf-corank)

### 4.3 Improving the 16.25% Bound?

Smith's result might combine with Bhargava-Shankar to SLIGHTLY improve the 16.25% bound, by providing better information within twist classes. But this would give a constant improvement, NOT density zero.

---

## 5. Computational Evidence

### 5.1 Rank >= 2 Proportions in Twist Families

| Base curve | Conductor | Twists with rank >= 2 (|d| <= 500) | Proportion |
|---|---|---|---|
| 11a1 | 11 | 43/612 | 7.03% |
| 14a1 | 14 | 46/612 | 7.52% |
| 15a1 | 15 | 50/612 | 8.17% |
| 17a1 | 17 | 70/612 | 11.44% |
| 19a1 | 19 | 37/612 | 6.05% |
| 37a1 | 37 | 53/612 | 8.66% |
| 43a1 | 43 | 46/612 | 7.52% |
| 53a1 | 53 | 46/612 | 7.52% |
| 77a1 | 77 | 35/612 | 5.72% |
| 91b1 | 91 | 34/612 | 5.56% |
| 389a1 | 389 | 65/612 | 10.62% |

(Both positive and negative d counted, using analytic rank)

### 5.2 Decay Rate for 11a1 (Extended Range, positive d only)

| d bound | Twists counted | rank >= 2 | Proportion | log(prop) |
|---|---|---|---|---|
| d <= 817 | 500 | 31 | 6.20% | -2.78 |
| d <= 1637 | 1000 | 66 | 6.60% | -2.72 |
| d <= 2463 | 1500 | 94 | 6.27% | -2.77 |
| d <= 3287 | 2000 | 118 | 5.90% | -2.83 |
| d <= 4109 | 2500 | 148 | 5.92% | -2.83 |
| d <= 4930 | 3000 | 175 | 5.83% | -2.84 |

Very slow decline from ~6.2% to ~5.8% over range d <= 5000. Consistent with Smith's triply-logarithmic convergence. The log(proportion) barely changes, confirming the rate is far slower than polynomial.

### 5.3 Comparison: Case I vs Case III

| Curve | 2-torsion | Smith case | Prop(rank>=2, d<=2000) |
|---|---|---|---|
| 11a1 | E[2] = 0 | Case I | 6.58% |
| 15a1 | E[2] = (Z/2Z)^2 | Case III | 7.98% |

Full 2-torsion curves have higher proportion, consistent with 2-Selmer rank distribution being "wider" (Case III has slower decay 2^{-r^2/4} vs 2^{-r^2/2}).

### 5.4 Dependence on Conductor

No clear monotone relationship between conductor and proportion of rank >= 2 twists at fixed D = 500. The proportion varies from 5.6% to 11.4%, seemingly depending more on the curve's arithmetic (2-torsion structure, isogenies) than on the conductor alone.

For 5077a1 (conductor 5077, d <= 1500): 11.4% rank >= 2, comparable to smaller-conductor curves. The convergence rate does NOT appear to degrade drastically with conductor.

---

## 6. Alternative Approaches to Density Zero

### 6.1 Multi-Prime Selmer Independence (Most Promising)

If Sel_p groups are independent across primes p, then P(rank >= 2) <= prod_p P(dim Sel_p >= 2) = 0.

**Status:** Proved over F_q(t) in large-q limit (Feng-Landesman-Rains 2022). Completely open over Q.

### 6.2 Selmer Averages for p > 5

If avg|Sel_p| = sigma(p) proved for infinitely many p, with independence, density zero follows.

**Status:** Parametrization for p > 5 does not exist. Fundamental obstacle.

### 6.3 Analytic Non-Vanishing

Need L(E,1) != 0 or L'(E,1) != 0 for 100% of curves.

**Status:** Iwaniec-Sarnak 50% barrier. Any improvement eliminates Landau-Siegel zeros. Currently impossible.

### 6.4 Direct Random Matrix Behavior

Prove Poonen-Rains directly for all E/Q by height, not just in twist families.

**Status:** Smith's work is the closest to this, but only within twist families.

---

## 7. Revised Assessment

### 7.1 The Transfer Is Dead

The naive transfer from Smith's twist-family result to the height-ordered family is fundamentally obstructed by the geometry of the height function. The obstruction is:

1. ht(E^d) = d^6 * ht(E_0), so the twist parameter d only grows as H^{1/6}
2. In the height ball, 96.4% of curves are twist-minimal (d = 1)
3. The weight distribution concentrates on barely-twisted curves
4. Smith's rate exp(-c * (log log log D)^{1/2}) is too slow to overcome the log(H) counting factor

**This is NOT about uniformity of Smith's rate.** Even with perfectly uniform c(E) = c_0 > 0, the bound diverges because exp(-c * sqrt(log log log H)) * log H -> infinity.

### 7.2 Could a Better Rate Save the Transfer?

If Smith's rate were MUCH better -- say f(E,D) <= D^{-delta} for some delta > 0 -- then the transfer might work because:

    prop <= sum_{E_0} w(E_0) * D(E_0)^{-delta}

The weight w(E_0) ~ D(E_0) / H^{5/6}, so:

    prop ~ H^{-5/6} * sum D^{1-delta} ~ H^{-5/6} * integral (H/x)^{(1-delta)/6} x^{-1/6} dx

For delta > 0, the integral converges differently and gives prop -> 0.

**But:** Achieving f(E,D) <= D^{-delta} is equivalent to proving rank >= 2 has density zero in EACH twist family with polynomial rate. This is FAR beyond Smith's current result and likely requires the Poonen-Rains model to be proved.

### 7.3 What Is Still Valuable

1. **Smith's explicit rate** (Remark 1.3) is the strongest quantitative result on rank distribution in twist families.
2. **The 2025 paper** removing all conditions is a major milestone.
3. **The KMR Markov model** shows transition probabilities are E-independent.
4. **Computational data** confirms slow but real decay consistent with Smith.
5. **The obstruction analysis** clarifies exactly where the density-zero problem lies.

### 7.4 Updated Ranking of Approaches to Density Zero

1. **Multi-prime Selmer independence over Q** -- the only known route that directly gives density zero. Requires major breakthrough.
2. **Extend Selmer averages to p = 7** -- improves bound from 16.25% but NOT density zero.
3. **Smith transfer via conductor ordering** -- partially viable but still insufficient.
4. **Analytic non-vanishing** -- stuck at 50% barrier.
5. **Prove Poonen-Rains for all curves** -- strongest but hardest.

### 7.5 The Real Dream

The dream is NOT "make Smith's rate uniform and transfer" (this cannot work). The real dream is:

**Prove that Sel_2 and Sel_3 are independent for all E/Q ordered by height.**

Even this partial independence would give:
- P(rank >= 2) <= P(dim Sel_2 >= 2) * P(dim Sel_3 >= 2) = 0.581 * 0.361 = 0.210

Still not density zero, but a meaningful improvement over 16.25%. And if extended to Sel_5:
- P(rank >= 2) <= 0.581 * 0.361 * 0.207 = 0.043 = 4.3%

For density zero: need independence of Sel_p for ALL primes p (or at least infinitely many).

---

## 8. Lessons Learned

1. **Height vs twist ordering:** The d^6 growth of height under twisting makes twist families too "thin" in the height-ordered family. This is a geometric obstruction, not an analytic one.

2. **The role of the exponent:** If height grew as d^2 (like conductor), the transfer would be more viable. The exponent 6 in d^6 is the problem.

3. **Smith's methods prove MORE than we can use:** The per-family density-zero result is very strong, but it does not project down to the height-ordered family.

4. **The path to 100% BSD requires global methods:** Methods that work family-by-family (Smith) cannot reach the full family. We need methods that work for ALL curves simultaneously (Bhargava-Shankar, Poonen-Rains).

5. **The 16.25% bound may be tight for current methods:** Without multi-prime independence or Selmer averages for p > 5, the 16.25% Bhargava-Shankar bound may be essentially the best achievable.
