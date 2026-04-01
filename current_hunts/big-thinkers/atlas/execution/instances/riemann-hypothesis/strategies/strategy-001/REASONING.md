# Strategizer Reasoning Log

## Exploration 001: GUE Pair Correlation and Nearest-Neighbor Spacing

### Planning (pre-launch)

**Options considered:**
1. **Random Matrix Theory — pair correlation + spacing** (CHOSEN): The Montgomery-Odlyzko pair correlation is the foundational GUE-zeta connection. Computing it numerically establishes our baseline tooling and may reveal sub-leading corrections or finite-height deviations. Nearest-neighbor spacing is closely related and can be done in the same computation pass.
2. **Explicit formulas / Weil explicit formula**: More algebraic, harder to make computational. Better for exploration 2 after we have zero data infrastructure.
3. **Quantum chaos / semiclassical**: Requires more theoretical setup. Better after we have the statistical baseline.
4. **Moment conjectures (Keating-Snaith)**: Computationally expensive, requires zeta values on the critical line. Good for later.

**Why pair correlation first:** It's the most computationally concrete starting point. We need code that computes zeta zeros and manipulates them — this will be reused in every subsequent exploration. The pair correlation function has an exact prediction (Montgomery's conjecture) that we can test against, making success criteria unambiguous. Any deviations or sub-leading corrections would be immediately interesting.

**Scope decision:** The meta-learning warns about multi-task overload. I'm keeping this to TWO closely related statistics: pair correlation R2(x) and nearest-neighbor spacing P(s). These come from the same zero data and are conceptually one investigation ("how do zeta zeros compare to GUE at the two-point level?"). Number variance and spectral form factor will be exploration 002.

**Librarian query:** Queried the library. Factual library has zero RH content (all QG). Meta library returned 12+ useful lessons about exploration design. Key lesson: explorers need explicit instructions to write code, and formulas should be provided rather than left for the explorer to research.

### Reflection (post-completion)

**Did the explorer deliver what I asked?** Yes — pair correlation and nearest-neighbor spacing were both computed and compared to GUE predictions with quantitative error measures. The explorer also went beyond the ask by comparing against all four ensembles (Poisson, GOE, GUE, GSE) and performing KS tests.

**Was the scope right?** Slightly overambitious on computation scale. The goal asked for 10,000 zeros and high-height zeros near n=100,000 — both were infeasible with mpmath. The explorer adapted well (reducing to 2,000 low + 500 high), but I should have set more realistic computation targets.

**What would I do differently?**
- Set explicit computation time budgets ("aim for ~5 minutes of computation total")
- Ask for 1,000-2,000 zeros upfront instead of 10,000
- Skip the high-height request or make it optional
- The Wigner surmise approximation issue was predictable — should have mentioned it in the goal

**Key findings to carry forward:**
1. GUE is definitively the right universality class (Poisson 5x worse, GOE 2x worse)
2. Chi-squared/dof = 1.50 is mildly elevated — possible unfolding artifacts
3. Wigner surmise detectable at N=2000 — need exact GUE for tighter tests
4. mpmath tops out at ~2000 zeros practically; large-scale needs Odlyzko-Schonhage
5. The Riemann operator must: act on complex Hilbert space, break T-symmetry, have quadratic level repulsion

## Exploration 002: Number Variance, Spectral Rigidity, and Berry's Saturation

### Planning (pre-launch)

**Options considered:**
1. **Number variance + spectral rigidity** (CHOSEN): These are the long-range spectral statistics, complementing exploration 001's short-range results. Berry (1985) predicts that number variance saturates (deviates from GUE logarithmic growth) at a scale related to the shortest periodic orbit. This saturation IS a deviation from pure GUE and would constrain the periodic orbit structure of the Riemann operator. Most likely to produce a non-trivial finding.
2. **Explicit formulas / Weil explicit formula**: Still an option for exploration 003. Want to complete the RMT constraint catalog first.
3. **Spectral form factor K(tau)**: Closely related to number variance via Fourier transform. Could be combined with number variance, but keeping scope tight.
4. **Exact GUE spacing distribution**: Important computation (from exploration 001 leads) but more of a refinement than a new constraint.

**Why number variance now:** Berry's saturation prediction is one of the few places where we EXPECT a deviation from GUE. Pure GUE number variance grows as log(L). Berry's semiclassical prediction says it saturates at L ~ T_H (the Heisenberg time). Computing this with 2000 zeros is borderline — the saturation may only become visible at large L where we have poor statistics — but even a null result (no saturation detected) is informative.

**Scope:** Number variance + spectral rigidity (Dyson-Mehta Delta_3). Both computed from the same zero data. The spectral form factor is the Fourier transform of pair correlation, which we already have — so including it is minimal extra work. THREE statistics, all closely related long-range measures.

**Lessons applied from exploration 001:**
- Asking for 2000 zeros max (not 10,000)
- Providing all formulas explicitly
- Explicit computation time budget
- Making high-height computation optional

### Reflection (post-completion)

**Did the explorer deliver?** Yes — all three statistics computed with quantitative results. The explorer also went beyond the ask by generating a GUE simulation as a finite-size control, which was extremely valuable for separating real saturation from finite-N artifacts.

**Was the scope right?** Borderline. Three statistics in one exploration is a lot, but they're closely related enough that it worked. The report is dense but complete.

**Key findings:**
1. Berry's saturation confirmed — Sigma^2 and Delta_3 both saturate well below GUE
2. Delta_3 saturation at 0.156 is the cleanest signal (flat from L=15 to L=100)
3. Form factor ramp slope = 1.010 — GUE short-range confirmed
4. Zeta zeros are 30-50% more rigid than finite-size GUE at large L
5. Saturation onset at L~2-5 is earlier than Berry's L_max~100 estimate

**Phase pivot decision:** I'm moving to Phase 2 after just 2 Phase 1 explorations (strategy suggested 3). Rationale: We now have 10 quantitative constraints from 2 independent domains (short-range RMT and long-range RMT). The constraint catalog is rich enough to meaningfully test operator candidates. A third Phase 1 exploration on the Weil explicit formula would add one more constraint type, but Phase 2 candidate testing is likely to be more productive now. Saving the exploration budget for more Phase 2 testing (4→5 explorations) or Phase 3 adversarial checks.

## Exploration 003: Berry-Keating xp Operator — Spectrum Computation and Constraint Testing

### Planning (pre-launch)

**Options considered for first Phase 2 exploration:**
1. **Berry-Keating xp and regularizations** (CHOSEN): The most famous specific candidate for the Riemann operator. H = xp (or its regularizations) is motivated by semiclassical arguments. The spectrum can be computed for specific regularizations. Testing against our 10-constraint catalog would be the first comprehensive numerical check.
2. **Laplacians on hyperbolic surfaces**: Connected to Selberg zeta function. More technically demanding to compute spectra. Better for exploration 004.
3. **Random matrix realizations**: Generate GUE matrices and compare individual eigenvalue patterns to zeta zeros. Interesting but less specific than testing a named candidate.
4. **Toeplitz/Hankel operators from arithmetic functions**: Novel but underspecified. Need to choose which arithmetic function.

**Why Berry-Keating first:** It's the most cited candidate. If it passes our constraint catalog, that's a strong signal. If it fails specific constraints, identifying WHICH constraints it fails and by HOW MUCH would be a concrete contribution. The Sierra-Townsend and Bender-Brody-Mueller regularizations have explicit spectra that can be computed.

**Key challenge:** The raw H = xp operator doesn't have a discrete spectrum on the real line. Regularizations (boundary conditions, truncation, PT-symmetric modifications) are needed to get a discrete spectrum. The exploration needs to handle multiple regularization approaches and compare their spectra to zeta zeros.

**Scope:** ONE operator family (Berry-Keating xp), but testing MULTIPLE regularizations. Focus on getting at least one regularization's spectrum computed and tested against the full constraint catalog.

### Reflection (post-completion)

**Did the explorer deliver?** Yes — all three approaches attempted with full scorecard. The comparative table at the end is exactly what was needed. The BBM result, while a failure, is informative (HO basis is fundamentally wrong).

**Was the scope right?** Good. Three approaches was the right number because two of them (A and B) are quick, and the third (C) is the interesting one.

**Key insight for strategy:** The exploration confirmed what Berry-Keating always implied but we hadn't computationally verified: the xp operator is only the smooth part. The fluctuations (ALL the interesting statistics) require primes. This means the most promising next step is the **trace formula reconstruction** — can we start from equally-spaced E_n = n and add prime corrections to reconstruct the zeta zero statistics?

**What would I do differently?**
- For Approach B, should have specified position-space discretization instead of leaving basis choice to the explorer
- For Approach C, should have specified N=2000 zeros (recompute) instead of accepting the explorer's choice of N=200
- The goal was well-designed for a survey; next explorations should be deeper on a single approach

## Exploration 004: Trace Formula Reconstruction — Can xp + Primes = Zeta Zeros?

### Planning (pre-launch)

**Options considered:**
1. **Trace formula reconstruction** (CHOSEN): Start from E_n = n (Sierra-Townsend) and add oscillatory prime corrections from the Weil explicit formula. This directly tests the Berry-Keating hypothesis that the Riemann operator = xp + prime arithmetic. This is the highest-value computation identified in exploration 003.
2. **BBM in position-space basis**: Would determine if BBM's failure was basis-dependent. Lower value than trace formula because even if it works, it just gives the BBM spectrum without explaining the prime connection.
3. **Laplacian on hyperbolic surfaces**: Interesting but separate from the Berry-Keating program. Better for exploration 005 or later.
4. **Toeplitz operators from arithmetic functions**: Novel but speculative. Less grounded than the trace formula approach.

**Why trace formula reconstruction:** Exploration 003 showed xp alone = 0/10 constraints. The explicit formula says the fluctuations in the zero-counting function come from sum over primes. If we can computationally reconstruct the zeta zero statistics by adding prime corrections to the equally-spaced spectrum, we've demonstrated that the Berry-Keating decomposition works. If there's a residual that can't be explained by a finite number of prime corrections, that's a new constraint on the operator.

**Scope:** ONE focused computation. Start with equally-spaced E_n = n, add prime corrections, compute the resulting spectrum's statistics, compare to zeta zeros. Deep exploration of ONE approach.

### Reflection (post-completion)

**Did the explorer deliver?** Exceptionally. This is the most insightful exploration so far. The negative result — individual zero reconstruction fails fundamentally due to the Gibbs phenomenon — is clean, well-supported, and produces a clear new understanding.

**Unexpected value:** The explorer corrected a formula error in the goal (ln(p) factor), discovered the ±0.5 Gibbs offset as a mathematical identity, and identified a deep structural insight: the trace formula determines spectral density but not spectral correlations.

**Key strategic insight:** The Berry-Keating operator contains more information than the trace formula. Its eigenvectors/matrix elements determine GUE statistics, which can't be extracted from the prime sum alone. This means:
- Future Phase 2 explorations should focus on the TWO-POINT trace formula (which might encode correlations)
- Or on operator construction from constraints (reverse engineering)
- Or on arithmetic geometry approaches that encode primes in the operator itself

**Remaining budget:** 6 explorations left. Phase 2 needs 2-3 more (operator candidates and correlation analysis). Phase 3 needs 2-3 (synthesis + adversarial).

## Exploration 005: Two-Point Correlation from Prime Pairs — Montgomery's Formula

### Planning (pre-launch)

**Options considered:**
1. **Two-point trace formula / pair correlation from prime pairs** (CHOSEN): Montgomery (1973) proved that the pair correlation of zeta zeros is determined by a sum over prime pairs. This is the TWO-POINT version of the trace formula — if it works, it means primes DO determine correlations, contradicting exploration 004's conclusion. Critical test.
2. **Arithmetic operators (Toeplitz/Hankel)**: Build operators from arithmetic functions with primes built in. Novel but speculative.
3. **Reverse-engineer operator from constraints**: Use the 10-constraint catalog to narrow the operator space. Interesting synthesis but may be premature.
4. **Laplacian on modular surface**: Connected to Selberg zeta function. A different operator candidate.

**Why pair correlation from prime pairs:** This directly addresses exploration 004's key insight ("primes determine density, not correlations"). Montgomery's proof shows the pair correlation IS determined by sums over prime pairs — so there IS a connection between primes and correlations. The question is whether this connection can be computed explicitly. If so, the insight from exploration 004 needs refinement: primes determine correlations through the TWO-POINT formula, not through the one-point counting function.

**Scope:** Compute Montgomery's pair correlation formula explicitly from primes and compare to the numerical pair correlation from exploration 001.

### Reflection (post-completion)

**Explorer crashed/timed out.** The tmux session was lost during the zero computation + prime analysis phase. The explorer had written code files and computed some data (part1_results.npz exists at 189KB) but never finished writing the report. Only a 33-line skeleton remains.

**What went wrong:** The computation was too heavy — computing 2000 zeros (5+ min) plus complex prime sums with normalization issues. The explorer also got briefly confused with the Yang-Mills mission, wasting time.

**Decision:** Not retrying. The two-point question is important but not essential for the synthesis phase. We have enough from explorations 001-004 to produce a meaningful final report. Moving to Phase 3.

## Exploration 006: Novel Arithmetic Operator Construction

### Planning (pre-launch)

**Remaining budget:** 5 explorations (006-010). Allocating:
- 006: One more Phase 2 operator candidate (arithmetic construction)
- 007: Synthesis of all findings
- 008: Adversarial review
- 009-010: Follow-up or additional synthesis

**Options for 006:**
1. **Arithmetic Toeplitz operator** (CHOSEN): Construct a Toeplitz matrix whose entries are values of the von Mangoldt function Lambda(n) (which is ln(p) when n = p^k, and 0 otherwise). This naturally encodes primes in the operator. Test against the constraint catalog.
2. **Retry exploration 005**: Two-point correlation from primes. Lower value because of prior failure.
3. **Selberg zeta function / hyperbolic Laplacian**: Different family of operators connected to trace formulas. More abstract.

**Why the arithmetic Toeplitz operator:** This is a genuinely novel computation. Toeplitz matrices T_{ij} = a(i-j) where a(n) = Lambda(n) (von Mangoldt) have arithmetic structure built in. Their spectra are related to the Fourier transform of Lambda, which connects to the zeta function via the explicit formula. If the eigenvalue statistics of this matrix are GUE-like, it would be a concrete connection between arithmetic and spectral statistics.

### Reflection (post-completion)
*[To be filled after exploration completes]*
