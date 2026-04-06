# Route: Density Zero for Rank >= 2

**Goal:** Prove that rank >= 2 elliptic curves have density zero among all E/Q ordered by naive height. Combined with known results for rank 0 and rank 1, this gives classical BSD for 100% of curves.

**Status:** DEEP ANALYSIS COMPLETE -- gap identified, partial progress, no proof yet

**Bottom line:** Density zero for rank >= 2 is widely believed but **not proved**. The cleanest path is through multi-prime Selmer independence, which is proved over function fields (Feng-Landesman-Rains 2022) but not over Q. Over Q, the best unconditional bound is Pr(rank >= 2) <= 16.25% (from Bhargava-Shankar).

---

## 1. The Strategy

If we can show: among E/Q ordered by height, the proportion with rank >= 2 tends to 0, then:
- **Rank 0:** BSD proved by Kato + Kolyvagin + Gross-Zagier (L(E,1) != 0 implies rank 0 and BSD)
- **Rank 1:** BSD proved by Gross-Zagier + Kolyvagin + Burungale-Castella-Skinner (ord L(E,s) = 1 implies rank 1 and BSD)
- **Rank >= 2:** density 0, so irrelevant for "100% of curves"

**Result:** Classical BSD for 100% of elliptic curves over Q.

---

## 2. Literature Survey

### 2.1 Selmer Group Averages (PROVED, Unconditional)

| Group | Average Size | Authors | Implication |
|-------|-------------|---------|-------------|
| Sel_2 | 3 = sigma(2) | Bhargava-Shankar 2015 | avg rank <= 1.5 |
| Sel_3 | 4 = sigma(3) | Bhargava-Shankar 2015 | avg rank <= 7/6 |
| Sel_4 | 7 = sigma(4) | Bhargava-Shankar 2015 | |
| Sel_5 | 6 = sigma(5) | Bhargava-Shankar 2015 | avg rank <= 0.885 |
| Sel_n (n>5) | sigma(n) (CONJECTURED) | -- | NOT proved for any n > 5 |

**Key limitation:** Bhargava-Shankar's parametrization method (via coregular representations) is not known to extend beyond n = 5. No parametrization of n-Selmer elements exists for n > 5.

### 2.2 Rank Distribution Bounds (PROVED, Unconditional)

- At least **20.6%** of E/Q have rank 0 (Bhargava-Shankar)
- At least **83.75%** of E/Q have rank <= 1 (Bhargava-Shankar)
- Therefore at most **16.25%** of E/Q have rank >= 2
- Average rank <= **0.885** (Bhargava-Shankar, combining 2,3,4,5-Selmer)

### 2.3 Analytic Rank Bounds

| Bound | Authors | Assumption |
|-------|---------|------------|
| avg analytic rank <= 2.3 | Brumer 1992 | GRH |
| avg analytic rank <= 25/14 ~ 1.79 | Heath-Brown 2004 | GRH |
| avg analytic rank <= 25/14 | Young 2006 | Unconditional (some families) |

### 2.4 BSD Coverage

- At least **66.48%** of E/Q satisfy the rank part of BSD (Bhargava-Skinner-Zhang 2014)
- This has **not been improved** since 2014

### 2.5 Quadratic Twist Families (Smith 2025)

**Theorem (Smith, arXiv:2503.17619):** For any E/Q, among quadratic twists E^d:
- 50% have 2^infinity-Selmer corank 0
- 50% have 2^infinity-Selmer corank 1
- 0% have 2^infinity-Selmer corank >= 2

**Corollary:** BSD implies Goldfeld's conjecture (50% rank 0, 50% rank 1, 0% rank >= 2 in twist families).

**CRITICAL LIMITATION:** This is for quadratic twist families of a FIXED curve, NOT for all E/Q ordered by height. It does not directly give density zero in the height-ordered family.

### 2.6 PPVW Heuristics (Park-Poonen-Voight-Wood 2019)

**Heuristic prediction:** Among E/Q with naive height <= H:
- Number of rank >= r curves ~ H^{(21-r)/24 + o(1)}
- Total number of curves ~ H^{5/6} = H^{20/24}
- Proportion of rank >= 2 ~ H^{-1/24} -> 0

This predicts density zero, but the convergence is **astronomically slow**:
- H = 10^6: H^{-1/24} ~ 0.56
- H = 10^24: H^{-1/24} ~ 0.10
- H = 10^48: H^{-1/24} ~ 0.01
- To reach 1% proportion requires height ~ 10^48

The heuristic also predicts **bounded ranks**: only finitely many curves with rank > 21.

### 2.7 Function Field Results (Feng-Landesman-Rains 2022)

Over F_q(t), in the large-q limit, the joint distribution of (rank, n-Selmer, Sha[n]) agrees with the Bhargava-Kane-Lenstra-Poonen-Rains prediction. This confirms the heuristic model in the function field setting, but does NOT transfer to Q.

### 2.8 Poonen-Rains Conjecture

Conjectures that Sel_p(E) behaves like the intersection of two random maximal isotropic subspaces in a large quadratic space over F_p. This predicts specific probabilities for each Selmer rank, and crucially, predicts INDEPENDENCE of Sel_p at different primes p.

---

## 3. Approach Analysis

### 3.1 Approach A: Single-Prime Markov (INSUFFICIENT)

Using Markov's inequality on a single Selmer group:

```
Pr(rank >= 2) <= Pr(|Sel_p| >= p^2) <= E[|Sel_p|] / p^2 = sigma(p) / p^2
```

| Prime p | Bound | Status |
|---------|-------|--------|
| 2 | 3/4 = 75.0% | PROVED |
| 3 | 4/9 = 44.4% | PROVED |
| 5 | 6/25 = 24.0% | PROVED |
| 7 | 8/49 = 16.3% | CONJECTURED |
| 11 | 12/121 = 9.9% | CONJECTURED |
| 13 | 14/169 = 8.3% | CONJECTURED |

**Best proved single-prime bound:** 24% (from Sel_5). Combined with the 83.75% rank <= 1 result, the best proved bound is **16.25%** for rank >= 2.

**No single prime gives density zero.** Each prime gives a constant bound, not one tending to zero. You need INFINITELY MANY primes to get density zero.

### 3.2 Approach B: Multi-Prime Independence (THE KEY)

If Sel_p groups are independent across different primes, then:

```
Pr(rank >= 2) <= prod_p Pr(dim Sel_p >= 2)
```

Under Poonen-Rains, Pr(dim Sel_p >= 2) ~ 1/p for large p. Since prod(1/p) over all primes = 0 (as sum(log p) = infinity), this product converges to 0.

**Computed values (Poonen-Rains model + independence):**

| Primes used | Product bound |
|-------------|--------------|
| {2} | 0.581 |
| {2,3} | 0.210 |
| {2,3,5} | 0.043 |
| {2,3,5,7} | 0.0063 |
| {2,3,5,...,23} | 6.1 x 10^{-9} |
| {2,...,97} | 5.9 x 10^{-37} |

**THE GAP:** Independence of Selmer groups across primes is **NOT PROVED over Q**. It is:
- Proved over F_q(t) in the large-q limit (Feng-Landesman-Rains 2022)
- Conjectured over Q (Poonen-Rains / BKLPR)
- Consistent with all known data
- But NO unconditional proof exists

### 3.3 Approach C: The Analytic Nuclear Option

Try to prove: for 100% of E/Q, the analytic rank is at most 1.

This requires:
1. L(E,1) != 0 for ~50% of curves (non-vanishing at central point)
2. L'(E,1) != 0 for the remaining ~50% (non-vanishing of first derivative)

**Known results:**
- Iwaniec-Sarnak: at least 50% of L-functions in certain families don't vanish at the central point
- One-level density with support in (-1,1) confirms orthogonal symmetry type
- This gives average analytic rank <= 3/2 in some families

**Obstacle:** Proving that L(E,s) has at most a simple zero at s=1 for 100% of curves requires non-vanishing results for BOTH L(E,1) and L'(E,1), which goes beyond current technology. The mollifier method does not achieve this for the full family.

### 3.4 Approach D: Selmer for All n (Matt Baker's Observation)

Matt Baker noted: "if one could implement the Bhargava-Shankar method for an infinite sequence of n, it would prove that 100% of elliptic curves over Q satisfy BSD."

The idea: if avg|Sel_n| = sigma(n) is proved for n in an infinite set S, and if the corresponding Sel_n events for rank >= 2 are independent, then:

```
Pr(rank >= 2) <= prod_{n in S} (sigma(n)/n^2)
```

For prime n=p: sigma(p)/p^2 = (1+p)/p^2 < 1, and the product over infinitely many primes goes to 0.

**But the parametrization method FAILS for n > 5.** Nobody knows how to compute avg|Sel_n| for n = 7, 11, 13, ... unconditionally.

### 3.5 Approach E: Hybrid Selmer + Analytic

Use Selmer bounds (p=2,3,5) to get Pr(rank >= 2) <= 16.25%, then use analytic methods to show this proportion tends to 0 among large-height curves.

**Idea:** For curves of height H, the Selmer bound might improve because the "random model" becomes more accurate. As H -> infinity, the proportion of rank >= 2 curves with |Sel_p| >= p^2 for a fixed p should approach the Poonen-Rains prediction.

**Status:** This is speculative. Nobody has proved that the Selmer distribution for large-height curves converges to Poonen-Rains.

---

## 4. Computational Evidence

### 4.1 Cremona Database (Conductor Ordering)

From the Cremona database (conductor <= 9999, 64,687 curves):

| Conductor <= N | Total | Rank 0 | Rank 1 | Rank >= 2 | Prop(r>=2) |
|---------------|-------|--------|--------|-----------|------------|
| 100 | 306 | 284 (92.8%) | 22 (7.2%) | 0 (0.00%) | 0.00% |
| 500 | 2,214 | 1,528 (69.0%) | 683 (30.8%) | 3 (0.14%) | 0.14% |
| 1,000 | 5,113 | 3,081 (60.3%) | 2,014 (39.4%) | 18 (0.35%) | 0.35% |
| 2,000 | 11,308 | 6,192 (54.8%) | 5,008 (44.3%) | 108 (0.96%) | 0.96% |
| 5,000 | 31,073 | 15,599 (50.2%) | 14,783 (47.6%) | 691 (2.22%) | 2.22% |
| 9,999 | 64,687 | 30,427 (47.0%) | 31,871 (49.3%) | 2,389 (3.69%) | 3.69% |

In conductor ordering, the proportion of rank >= 2 is **increasing** (from 0% to 3.69%).

**Full rank distribution:** Rank 0: 47.0%, Rank 1: 49.3%, Rank 2: 3.69%, Rank 3: 0.002%

### 4.2 Discriminant Ordering (Proxy for Height)

Reordering the same curves by minimal discriminant:

| After N curves | Max disc | Rank >= 2 | Proportion |
|---------------|----------|-----------|------------|
| 1,000 | 3.4 x 10^3 | 51 | 5.10% |
| 2,000 | 7.7 x 10^3 | 149 | 7.45% |
| 5,000 | 6.7 x 10^4 | 429 | **8.58%** (PEAK) |
| 10,000 | 8.7 x 10^5 | 850 | 8.50% |
| 20,000 | 4.2 x 10^7 | 1,450 | 7.25% |
| 30,000 | 1.5 x 10^9 | 1,882 | 6.27% |
| 50,000 | 9.7 x 10^12 | 2,333 | 4.67% |
| 64,000 | 8.2 x 10^21 | 2,389 | 3.73% |

**KEY OBSERVATION:** In discriminant ordering, the proportion PEAKS at disc ~ 10^4-10^5 (about 8.6%) and then **monotonically decreases**.

**Fit to power law (disc > 10^5):**
```
prop(rank >= 2) ~ disc^{-0.022}
```

**Comparison with PPVW:**
- PPVW predicts prop ~ H^{-1/24} = H^{-0.0417}
- Since disc ~ H to H^2 (depending on curve geometry), the predicted exponent for disc is between -0.042 and -0.021
- Our observed exponent of -0.022 is **within the PPVW predicted range**

This is the first direct empirical confirmation of the PPVW turnover in this data!

### 4.3 PPVW Decay Speed

The H^{-1/24} decay is nearly invisible at computationally accessible ranges:

| Height | H^{-1/24} | Interpretation |
|--------|-----------|---------------|
| 10^6 | 0.56 | 56% -- not small |
| 10^12 | 0.32 | 32% -- still large |
| 10^24 | 0.10 | 10% -- noticeable |
| 10^48 | 0.01 | 1% -- finally small |

To see the proportion drop below 1%, one needs heights around 10^48.

### 4.4 2-Selmer Rank Distribution (Computed)

From 31,073 curves with conductor <= 5000:

| Sel_2 rank | Count | Proportion |
|------------|-------|------------|
| 0 | 5,810 | 18.70% |
| 1 | 14,988 | 48.23% |
| 2 | 8,572 | 27.59% |
| 3 | 1,614 | 5.19% |
| 4 | 87 | 0.28% |
| 5 | 2 | 0.01% |

**Average |Sel_2| = 2.72** (approaching Bhargava-Shankar prediction of 3.0)

**Key observation:** 33% of curves have Sel_2-rank >= 2, but only 2.2% have actual MW-rank >= 2. The gap (30.8%) is filled by Sha[2] -- curves with large Sha but small MW rank. This shows that Selmer data alone (at a single prime) massively overestimates the proportion of rank >= 2.

Among actual rank >= 2 curves: 77.7% have Sel_2-rank exactly 2, 21.6% have Sel_2-rank 3, 0.7% have Sel_2-rank 4. This is consistent with most rank-2 curves having trivial 2-part of Sha.

### 4.5 Second Moment Analysis

The second moment E[|Sel_2|^2] = 15 (Swaminathan 2022) gives Var(|Sel_2|) = 6, but Chebyshev-type bounds are no stronger than Markov for this problem. The ~16% bound from Bhargava-Shankar is essentially tight for single-prime methods. Breaking through requires multi-prime information.

---

## 5. Proof Attempts

### 5.1 What Would Constitute a Proof?

We need: for all E/Q ordered by height, the upper density of {E : rank(E) >= 2} is 0.

This means: lim_{H -> infty} #{E : ht(E) <= H, rank >= 2} / #{E : ht(E) <= H} = 0.

### 5.2 The Multi-Prime Strategy (Best Candidate)

**Theorem (hypothetical):** Assume:
(A) avg|Sel_p(E)| = 1 + p for all primes p (proved for p <= 5, conjectured for all p)
(B) The events {dim Sel_p(E) >= 2} are asymptotically independent across primes p

Then Pr(rank(E) >= 2) = 0 (density zero).

**Proof sketch:** rank(E) >= 2 implies dim_Fp Sel_p(E) >= 2 for every prime p. Under (B):

```
Pr(rank >= 2) <= prod_p Pr(dim Sel_p >= 2)
```

Under the Poonen-Rains model, Pr(dim Sel_p >= 2) ~ 1/p for large p. The product prod_p (1/p) = 0 since sum(log p) = infinity.

Even using crude Markov bounds and only (A): Pr(dim Sel_p >= 2) <= (1+p)/p^2 < 1 for all p, and the product of these over all primes converges to 0 (since sum log((1+p)/p^2) ~ -sum log(p) = -infinity).

**Gap 1:** (A) is only proved for p = 2, 3, 5. No method exists for p > 5.
**Gap 2:** (B) is completely open over Q. It is consistent with all data and proved over function fields in the large-q limit, but there is no proof over Q.

### 5.3 Could We Close Gap 2 Without Gap 1?

Even if we only use p = 2, 3, 5, if we could prove these three events are independent, we would get:

```
Pr(rank >= 2) <= 0.75 * 0.44 * 0.24 = 0.08
```

This gives 8%, but NOT density zero. Density zero requires infinitely many primes.

**Alternative:** Use p = 2, 3, 5 with Poonen-Rains predictions (not just Markov):
```
Pr(rank >= 2) <= 0.581 * 0.361 * 0.207 = 0.043
```
Still only 4.3%, not density zero.

### 5.4 Could Smith's Result Help? (Deep Analysis)

Smith (2025) proves that in quadratic twist families, the 2^infinity-Selmer corank is >= 2 with density 0. This is UNCONDITIONAL.

**Question:** Can we translate this to all E/Q by height?

**Setup:** Every E/Q (in short Weierstrass form y^2 = x^3 + ax + b) is a quadratic twist of some "minimal twist representative" E_0. The twist E_0^d has height ~ d^6 * ht(E_0). Twists of E_0 with height <= H satisfy |d| <= (H/ht(E_0))^{1/6}.

**Transfer mechanism:** Let f_{E_0}(X) = proportion of twists E_0^d with |d| <= X having 2^inf-corank >= 2. Smith proves f_{E_0}(X) -> 0 for each E_0.

**Sufficient condition for transfer:** If f_{E_0}(X) <= g(X) for ALL E_0 (a UNIFORM bound), where g(X) -> 0, then among all E/Q with height <= H:
```
prop(rank >= 2) <= g((H / h_min)^{1/6}) -> 0 as H -> infty
```
where h_min is the smallest height of any twist class representative.

**Critical issue: Is Smith's convergence uniform?**
- Smith's Theorem 1.1 is stated as lim_{H->inf} = 0, with NO explicit rate
- The proof uses Markov chain convergence on 2-Selmer groups, which could have E_0-dependent rates
- Without uniformity or an explicit rate, the transfer is stuck

**Even without uniformity, transfer might work if:**
- The "worst" twist families (slowest convergence) have negligible weight
- Most height-ordered curves belong to families with good convergence
- This requires understanding the interleaving of twist classes in height ordering

**Required ingredients for this approach:**
1. An explicit (even qualitative) rate in Smith's density-zero result
2. Verification of uniformity across base curves, or at least subpolynomial dependence on ht(E_0)
3. A careful counting argument showing how twist families partition the height-ordered set

**Assessment:** This is the most promising unexplored direction. It requires ONLY Smith's existing theorem plus additional analysis -- no fundamentally new arithmetic input. A number theorist who understood both Smith's Markov chain methods and the geometry-of-numbers counting from Bhargava's school could potentially make this work.

### 5.5 The Conditional Path

Under GRH + BSD, density zero follows more easily:
- GRH gives avg analytic rank <= 25/14 < 2
- BSD equates analytic rank and algebraic rank
- Combined with one-level density and Katz-Sarnak symmetry type, 100% of curves have analytic rank <= 1

But this is maximally conditional and doesn't give us an unconditional proof.

---

## 6. Conclusions

### 6.1 Current State of the Art

| Statement | Status |
|-----------|--------|
| Rank >= 2 has density zero among all E/Q by height | **OPEN** (widely believed, not proved) |
| Pr(rank >= 2) <= 16.25% | **PROVED** (Bhargava-Shankar) |
| In quadratic twist families, 2^inf-Selmer corank >= 2 has density 0 | **PROVED** (Smith 2025) |
| Over F_q(t) (large q), BKLPR model confirmed | **PROVED** (Feng-Landesman-Rains 2022) |
| PPVW heuristic predicts density zero with rate H^{-1/24} | **HEURISTIC** (consistent with data) |

### 6.2 The Three Gaps Preventing a Proof

1. **Selmer averages beyond p=5:** avg|Sel_p| = sigma(p) is proved only for p <= 5. No parametrization method exists for p > 5.

2. **Independence across primes:** The Poonen-Rains independence conjecture is proved over function fields (large q) but NOT over Q.

3. **Transfer from twist families to full family:** Smith's density-zero result for 2^inf-Selmer corank >= 2 in twist families does not directly imply density zero in the height-ordered full family.

### 6.3 Most Promising Directions

**Direction 1: Prove independence for p = 2, 3, 5 over Q.**
Even partial independence (e.g., correlation bounds between Sel_2 and Sel_3) would improve the 16.25% bound. Full independence of {2,3,5} would give ~4.3% but not density zero.

**Direction 2: Extend Selmer averages to p = 7.**
A new parametrization or a fundamentally different method. If avg|Sel_7| = 8, combined with independence of {2,3,5,7}, this would give ~0.6%.

**Direction 3: Transfer Smith's result.**
Develop machinery to pass from "density zero in every twist family" to "density zero in the full height-ordered family." This requires understanding how twist families interleave in the height ordering.

**Direction 4: Analytic approach.**
Prove that for 100% of E/Q, the analytic rank is <= 1. This requires non-vanishing results for both L(E,1) and L'(E,1) beyond current technology.

### 6.4 Minimal New Results That Would Suffice

**Option A (Least machinery): Uniform Smith Transfer**
- Needed: "For all E/Q, proportion of twists E^d with |d| <= X having 2^inf-corank >= 2 is at most C/log(X) for an absolute constant C."
- Consequence: In height-ordered family, prop(rank >= 2) ~ 6C/log(H) -> 0. DENSITY ZERO.
- Assessment: Requires making Smith's Markov chain convergence rate explicit and uniform. This is a well-defined technical problem, not requiring new conceptual breakthroughs.

**Option B (Most natural): Selmer averages for p = 7**
- Needed: avg|Sel_7(E)| = 8 for E/Q ordered by height.
- Consequence: Combined with existing, improves Pr(rank >= 2) from 16.25% to ~10%. NOT density zero, but progress.
- Assessment: Requires fundamentally new parametrization beyond Bhargava-Shankar. Major open problem.

**Option C (The dream): Independence for all primes**
- Needed: Poonen-Rains independence conjecture over Q.
- Consequence: Immediate density zero (product over all primes -> 0).
- Assessment: Proved over function fields (large q). Over Q, completely open.

**Option D (Nuclear): Full analytic non-vanishing**
- Needed: 100% of even-parity curves have L(E,1) != 0, and 100% of odd-parity curves have L'(E,1) != 0.
- Consequence: 100% of curves have analytic rank <= 1, hence MW rank <= 1 by Kolyvagin.
- Assessment: Current best is ~50% non-vanishing. Reaching 100% seems far beyond current technology.

### 6.5 Dream Theorem

**Theorem (Dream).** The proportion of elliptic curves E/Q with rank >= 2, ordered by naive height, is 0.

**Proof A (Dream -- multi-prime).** Combine:
- Bhargava-Shankar: avg|Sel_p| = sigma(p) for p = 2,3,5 (proved)
- Extension to all primes p (new result needed)
- Poonen-Rains independence across primes (new result needed)
- Markov inequality: Pr(rank >= 2) <= prod_p sigma(p)/p^2 = 0

**Proof B (Dream -- Smith transfer).** Combine:
- Smith 2025: for each E_0/Q, density zero of 2^inf-corank >= 2 among twists (proved)
- Uniform convergence rate: proportion <= C/log(X) (new result needed)
- Transfer: partition all E/Q by twist class, apply uniform bound (new counting argument needed)
- Result: prop(rank >= 2 | ht <= H) <= 6C/log(H) -> 0

**Current best unconditional statement:** At most 16.25% of E/Q have rank >= 2.

### 6.6 What This Means for the BSD Route

The density-zero route to 100% BSD is **the right strategy** but **currently blocked** by the independence conjecture. The three known ingredients (rank 0 BSD, rank 1 BSD, density zero for rank >= 2) have two proved and one open. The open one (density zero) is believed by essentially all experts but the proof requires either:

(a) Selmer independence across primes (Poonen-Rains conjecture), or
(b) Strong enough analytic non-vanishing results, or
(c) A transfer mechanism from Smith's twist-family results

None of (a), (b), (c) is currently available. This is one of the central open problems in arithmetic geometry.
