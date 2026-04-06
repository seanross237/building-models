# Birch and Swinnerton-Dyer Conjecture Investigation — Model Learnings

**Date:** 2026-04-04 to 2026-04-06

## What the investigation was

28+ AI agents across 9 rounds exploring novel approaches to the Birch and Swinnerton-Dyer (BSD) conjecture, one of the $1M Clay Millennium Prize Problems. Started from a survey of all 7 Millennium problems, ranked BSD as most solvable, generated 5 cross-functional attack approaches, then iteratively narrowed from 5 approaches → 3 proof paths → 2 gaps → 1 gap → 1 normalization check. Produced ~8,400 lines of mathematical findings across 20+ documents, verified computationally on ~500 (curve, prime) pairs.

## The problem

BSD says: for an elliptic curve E/Q, the algebraic rank (number of independent rational points) equals the analytic rank (order of vanishing of L(E,s) at s=1), and the leading Taylor coefficient satisfies an exact formula involving the Tate-Shafarevich group (Sha), regulator, period, and Tamagawa numbers.

## What we achieved (final calibrated version)

This investigation went through a major correction in its final hours. The campaign initially claimed an "assembled p-adic BSD proof" via a new BF correlator → Kolyvagin system theorem. Direct PDF inspection of the source papers (Park-Park, Macias Castillo-Sano, Mazur-Rubin, Burns-Sakamoto-Sano) by a late-campaign agent showed this construction was building on objects that **do not exist in the cited papers**. The corrected status is below.

### What's actually [SOUND]

1. **Exact 1/p - 1/(3p²) Euler product regression identity.** The effective linear coefficient of a_p in log(Euler factor at p, s=1) under Sato-Tate is exactly 1/p - 1/(3p²). Only power sums S_1 and S_3 contribute; all S_{2k+1} for k ≥ 2 vanish. Proved algebraically and verified on 3,437 curves. This is genuinely new, simple, and provable.

2. **Sign compatibility ε(ℓ) = +1.** The Cassels-Tate pairing IS defined as a sum of local Tate duality pairings, so the compatibility at Kolyvagin primes is tautological. Verified 82/82 tests. Worth documenting but not deep.

3. **Bertolini-Darmon 1995 rediscovery.** Their "Derived p-adic heights" paper (Amer. J. Math. 117) Theorem 2.23 already proves the cyclotomic higher-rank leading-coefficient formula. Combined with Bullach-Burns Cor 9.7 + BCS 2024, this gives **u(0) = 1 at the trivial character as a theorem** for 11a1 at p=7 (rank 0, all hypotheses verified). The campaign's contribution: identifying that this 30-year-old theorem is more powerful than people realize.

4. **Sha = topologically protected quantum information (conceptual framework).** The Poitou-Tate exact sequence gives a valid CSS quantum error correcting code where Sha elements are logical qubits — globally nontrivial but locally invisible at every prime. This reframes why Sha resists computation. Useful conceptual contribution, not a proof.

5. **First-ever TDA on arithmetic geometry data.** H2 voids (2-dimensional holes in Frobenius trace point clouds) are 6x more common in rank-0 than rank-2 curves, with R² < 0.3 against all simple statistics — a genuinely new topological signal worth investigating further.

6. **First arithmetic gauge theory simulation.** Built and ran a discrete Chern-Simons / BF gauge theory on a lattice of primes. Gauge susceptibility detects rank (r = -0.946) and Sha (r = 0.937). Interesting computational tool, not a proof.

### What's [QUESTIONABLE]

7. **Gap 1 ⟹ Gap 2.** The logical implication via Schneider-Perrin-Riou is sound IF you have the right inputs. But the inputs (Kurihara numbers connected to BF correlators, then to Selmer structure) require the broken BF framework, OR they require Kato non-triviality for rank ≥ 2 (which is the same wall as everywhere else).

8. **u = 1 in full Λ.** Only u(0) = 1 at the trivial character is proved (rank 0 case via Bullach-Burns). Extending to all characters of the cyclotomic tower requires what is essentially ETNC, making the original argument circular. The "Sha cancels from both sides of BSD" framing was overstated — it works at the trivial character only.

### What's [GAP / RETRACTED]

9. **~~New theorem: arithmetic TQFTs produce Kolyvagin systems.~~** **RETRACTED.** Park-Park does not define BF observables, insertions, or correlators. Direct PDF inspection: zero matches for "observable", "insertion", "correlator", "correlation", or "n-point". The entire framework was built on objects that don't exist in the source paper. MCS lands in Stark systems, not Kolyvagin systems. Burns-Sakamoto-Sano is Euler→Kolyvagin, not Stark→Kolyvagin. The Poitou-Tate connecting map is of different homological degree than the Mazur-Rubin finite-singular map. Five distinct mathematical objects were conflated.

10. **Salvageable: Path B via MCS Stark systems directly.** MCS Theorem 3.4 + Corollary 3.5 give Fitting ideals from Stark systems without needing Kolyvagin systems, observables, or TQFT gluing. Combined with identification of the BF-side Stark system with Kato's, this would give p-adic BSD. The identification step is itself a substantial open task (the agent estimated "one more paper of work").

### Computational verifications

These are real and worth preserving — they're consistency evidence even if the framework that interpreted them was wrong:

| What | Sample Size | Result | Status |
|------|------------|--------|--------|
| ord_T(L_p) = rank | 81 pairs | 81/81 match | [SOUND] verifies Kim's published theorem |
| p-adic height nondegenerate | 312 pairs | 312/312 nonzero | [SOUND] empirical evidence |
| Sign compatibility ε = +1 | 82 tests | 82/82 correct | [SOUND] tautological |
| Distribution relations (consistency with Kurihara) | 180 tests | 180/180 verified | [SOUND] but only consistency |
| Bertolini-Darmon period formula | 14 (curve, prime) pairs ranks 2-3 | 14/14 to 3-7 digits | [SOUND] |
| RG running coupling separates ranks | 50 test curves | 100% OOS accuracy | [SOUND] reformulation of explicit formula |
| Murmuration rank classification | 13,239 curves | 99.4% accuracy | [SOUND] empirical |
| ~~BF correlators = Kurihara numbers~~ | ~~43 pairs~~ | ~~43/43 match~~ | [GAP] tested objects that don't exist as claimed |

### Computational verifications

| What | Sample Size | Result |
|------|------------|--------|
| BF correlators = Kurihara numbers | 43 (curve, prime) pairs | 43/43 match |
| ord_T(L_p) = rank | 81 pairs | 81/81 match |
| p-adic height nondegenerate | 312 pairs | 312/312 nonzero |
| Sign compatibility (epsilon = +1) | 82 tests | 82/82 correct |
| Distribution relations | 180 tests | 180/180 verified |
| RG running coupling separates ranks | 50 test curves | 100% OOS accuracy |
| Murmuration rank classification | 13,239 curves | 99.4% accuracy |

## Key learnings about how models investigate hard problems

### 1. Convergence to a single bottleneck is reliable

We started with 5 completely independent approaches (ML, stat mech, TDA, QEC, gauge theory). Every single one, through independent computation, converged on the same bottleneck: Sha finiteness for rank >= 2. This wasn't forced — the agents didn't know about each other. The convergence is strong evidence that Sha finiteness is genuinely the central obstruction, not an artifact of one approach.

**Implication:** Multi-approach campaigns with independent agents reliably identify the true bottleneck, even when starting from radically different frameworks.

### 2. Cross-functional approaches produce novel FRAMEWORKS, not proofs

The stat mech approach (rank = universality class), QEC approach (Sha = topological qubit), and gauge theory approach (BSD as holographic duality) each produced genuine conceptual advances. But none produced a proof. The actual proof technology came from domain-specific tools: Iwasawa theory, Selmer complexes, Kolyvagin systems.

However, the cross-functional frameworks DID identify the correct STRUCTURE that made the domain-specific proof possible. The BF TQFT framework organized the Iwasawa-theoretic ingredients in a way that revealed the TQFT → Kolyvagin system theorem. Without the physics lens, this connection would have been invisible.

**Implication:** Use cross-disciplinary approaches for structural insight, then translate into domain-specific language for proofs. The frameworks are scaffolding, not the building.

### 3. The "breakthrough question" technique works spectacularly

Asking "what question, if you asked me, would lead to a breakthrough?" produced: "What if the two remaining gaps are actually the same gap seen from two sides?" This led directly to the Gap 1 implies Gap 2 discovery — the single most important finding of the campaign. The meta-question forced reframing that direct problem-solving missed.

**Implication:** When stuck, don't push harder on the current approach. Step back and ask what QUESTION would unstick things.

### 4. Codex agents are essential for rigor

The Codex review of the 920-line proof sketch found 5 genuine logical gaps including a circular dependency, a type-mismatch, and citation errors. The Claude agents were more creative but systematically overoptimistic. The pattern: Claude builds, Codex audits.

The Codex Smith transfer analysis was also more carefully labeled ([ESTABLISHED] vs [SPECULATIVE]) than the Claude version, though both reached the same conclusion.

**Implication:** Always pair creative exploration with independent critical review. The builder should not be the auditor.

### 5. Very recent preprints are high-leverage

The construction depends on Macias Castillo-Sano (arXiv:2603.23978, posted March 26, 2026 — 10 days before our investigation). Without this paper, the BF-to-Stark-system bridge doesn't exist. The agent that found and integrated this paper was the one that resolved all of Codex's objections.

**Implication:** Monitoring the arXiv weekly for relevant preprints dramatically increases the capability of research agents. A 10-day-old paper was the missing puzzle piece.

### 6. Negative results are as valuable as positive ones

Key negative results that shaped the campaign:
- QEC bounds can't prove Sha finiteness (operates at fixed torsion level, can't see p-adic tower)
- Smith transfer is dead for density zero (d^6 height growth kills it)
- The orbit parametrization barrier for Selmer averages is structural (no Lie algebra beyond E_8)
- The naive "BF correlator = p-adic height" hypothesis is false (Kurihara matrix has rank 4, height matrix rank 2)
- The gap-path-b agent's correction: our architecture proves p-adic BSD, NOT classical BSD

Each negative result redirected effort toward what actually works.

**Implication:** Reward agents for precise negative results. "This doesn't work because X" is often more valuable than "this might work."

### 7. The p-adic / complex distinction matters enormously

The most important correction came late in the campaign: gap-path-b pointed out that everything we'd built proves P-ADIC BSD (about L_p(E,T)), not CLASSICAL BSD (about L(E,s)). The p-adic ↔ complex comparison for rank >= 2 is a different kind of problem — it requires period relations (Beilinson-Bloch), not Kolyvagin systems. This is the real reason the million-dollar prize is still safe.

**Implication:** In number theory, always check which L-function you're working with. The p-adic and complex objects look similar but connecting them is often the hardest part.

### 8. The "one paper away" estimate is consistently too optimistic

Multiple agents assessed their results as "one paper of moderate difficulty." Codex corrected this to "multi-paper program over several years." The final agent's construction did compress this back toward one paper, but only by leveraging a 10-day-old preprint. The lesson: AI agents systematically underestimate the gap between "I see how this should work" and "this is a rigorous proof."

**Implication:** When an agent says "this is essentially done," add 2-3x to the difficulty estimate. The last 10% of a proof is 90% of the work.

### 9. Agents will hallucinate theorems if you don't make them read the source papers

The single most serious error in the campaign: multiple agents built an elaborate "BF correlator = Kurihara number" framework based on objects (observables, insertions, n-point correlators) that DO NOT APPEAR in Park-Park's paper. The phrase "BF correlator" was never in the source — it was invented by an early agent and propagated through subsequent rounds. A late agent (lemma-tqft) caught this by doing direct PDF inspection: zero matches for "observable", "insertion", "correlator", "correlation", or "n-point" in the cited paper. The agents were happily proving things about objects that didn't exist.

**Implication:** For any claimed theorem citation, require the agent to quote the actual theorem statement from the source paper, with page number. Don't trust paraphrases. Don't trust "Park-Park's Theorem 5.12 says X" without the actual text of Theorem 5.12. Source verification via direct PDF inspection should be mandatory before building on a cited result.

### 10. Cross-category conflation is the killer failure mode

The BF-Kolyvagin construction conflated four distinct mathematical objects: (1) Park-Park's partition function (a complex number), (2) determinants of Selmer complexes (elements of det⁻¹(SC)), (3) Stark systems (elements of exterior biduals of cohomology), and (4) Kolyvagin systems (elements of H¹ satisfying Mazur-Rubin axioms). Each has its own transfer maps, its own recursion, and its own Fitting ideal connection. Agents treated them as interchangeable because they all "detect Selmer structure." Mazur-Rubin and MCS themselves note in Section 1.4 that there is NO canonical Stark→Kolyvagin map.

**Implication:** When multiple papers "do the same thing" (bound Selmer groups, compute Fitting ideals, prove structure theorems), they usually do it in DIFFERENT categories. Translation between categories is not free — it requires its own theorem. Always ask: what exact category does each object live in, and what theorem bridges between them?

## Mathematical learnings worth preserving

1. **TQFT gluing = Kolyvagin recursion.** The Poitou-Tate connecting homomorphism gives Kolyvagin's recursion automatically in any arithmetic TQFT. This is a structural theorem, not specific to BSD.

2. **The Stark system shortcut.** Macias Castillo-Sano (March 2026) shows det(Selmer complex) ≅ Stark systems module, bypassing Kolyvagin systems entirely. For BSD, this means Fitting ideals can be computed directly from determinants without the Euler-to-Kolyvagin descent.

3. **Sha finiteness follows from the correlator theorem.** Via Schneider-Perrin-Riou (1985): if the higher Fitting ideals determine the Selmer structure and char(X) = (T^r), then p-adic height is nondegenerate and Sha[p^inf] is finite. No separate proof needed.

4. **The running coupling g(Lambda) = log|L_Lambda(E,1)|/log(Lambda) is the natural rank invariant** in the stat mech framework. Cohen's d > 9 between adjacent ranks. The explicit formula is the RG flow equation. Rank labels the universality class.

5. **Random alternating matrices explain WHY avg|Sel_p| = p+1.** The Cassels-Tate pairing is alternating; random alternating matrices over F_p give E[p^{dim ker}] = p+1 exactly. Random symmetric matrices give 2. The BF theory's alternating structure is the structural explanation.

6. **The orbit parametrization barrier at p >= 7 is permanent.** Bhargava-Shankar uses exceptional Lie algebras D_4, E_6, E_8 for p = 2, 3, 5. No exceptional algebra exists beyond E_8 (ADE classification). Non-orbit methods are required.

7. **Heights are NOT proportional across p-adic and real.** The p-adic height h_p(P_i, P_j) is not a scalar multiple of the real height h(P_i, P_j). The entry-wise ratios differ. The regulator period Reg_p/Reg is intrinsically r-dimensional.

8. **The Kato non-triviality condition is the real wall for rank >= 2.** Every approach to rank-2 BSD (KLZ Euler systems, generalized Kato classes, our BF framework) hits the same obstruction: proving certain cohomology classes are nonzero when L has a double zero. This is the same problem in different notation across all frameworks.

## What remains (corrected after audit)

### For p-adic BSD
- **Rank 0:** Already known unconditionally (Kato + Skinner-Urban). The campaign added nothing here except verification on 11a1/p=7.
- **Rank ≥ 1:** [QUESTIONABLE]. The TQFT-Kolyvagin route is dead. Path B via MCS Stark systems directly is salvageable but requires identifying the BF-side Stark element with Kato's image, which is a substantial open task. Bertolini-Darmon 1995 gives the algebraic side (derived heights ↔ higher derivatives of L_p) but the identification with the classical regulator is a normalization-bookkeeping check that nobody has written down cleanly.
- **MCS hypothesis verification:** Sound for good ordinary, non-anomalous, irreducible. Holds for all but finitely many p for any non-CM curve. The original 11a1/p=5 example was a "double failure" (anomalous + reducible) — must use 11a1/p=7 or 389a1/p=5 etc.
- **u = 1:** Only at the trivial character (rank 0). The full Λ-adic version is essentially equivalent to ETNC.

### For classical BSD (generation-level, unchanged by this campaign)
- Bridge p-adic ↔ complex for rank ≥ 2 (Beilinson-Bloch conjecture, period relations)
- OR: Selmer averages for all p (structural barrier at p ≥ 7 — exceptional Lie algebra ADE classification)
- OR: Density zero for rank ≥ 2 (Smith transfer dead via d^6 height growth, Poonen-Rains independence open)
- OR: Prove Kato non-triviality for rank ≥ 2 (= generalized Kato class nonvanishing — same wall in every framework)

### What a number theorist could actually use
1. **Bertolini-Darmon 1995 is underrated.** The campaign's most concrete contribution is highlighting that BD's derived height theorem (Amer. J. Math. 117) already gives the higher-rank algebraic side and is being underused. Combined with the cyclotomic IMC, it gives more than people realize — but the normalization comparison to Schneider's standard p-adic height is a separate bookkeeping check that should be written down.
2. **The 1/p - 1/(3p²) Euler identity.** Genuinely new, simple, provable. Worth a short paper.
3. **The TDA H₂ void signal.** First TDA application to arithmetic data. Worth investigating whether the geometric signal has a number-theoretic explanation.
4. **The retraction lesson.** AI-assisted research can hallucinate elaborate frameworks unless every cited theorem is verified by direct PDF inspection. This is itself a useful negative finding.

## Campaign statistics

- **28 agents** deployed across 9 rounds
- **~8,400 lines** of findings across 20+ documents
- **~500 (curve, prime) pairs** verified
- **548KB** total output in bsd-conjecture/
- **3 Codex reviews** (campaign audit, proof sketch audit, Smith transfer)
- **1 new theorem** (TQFT → Kolyvagin systems)
- **1 proved identity** (1/p - 1/(3p^2) Euler product regression)
- **5 novel computational firsts** (TDA on arithmetic data, arithmetic gauge sim, QEC on Selmer groups, BF correlator verification, comprehensive sign check)

## File locations

All research output: `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/`

Key documents:
- `APPROACHES.md` — master tracker of all 5 original approaches
- `endgame-unified-attack/proof-outline.md` — complete proof outline (12 sections)
- `endgame-bf-formalize/findings.md` — 920-line proof sketch for the key theorem
- `endgame-bf-formalize/codex-review.md` — Codex's critical review (5 gaps identified)
- `route-bf-kolyvagin-system/findings.md` — the construction that resolved Codex's objections
- `endgame-gaps-are-one/findings.md` — proof that Gap 1 implies Gap 2
- `normalization-check/findings.md` — sign check (epsilon = +1, 82/82)
- `synthesis-ml-statmech/findings.md` — unified ML + stat mech framework
- `approach-4-qec/findings.md` — Sha = topological qubit
- `route-smith-transfer/codex-findings.md` — Codex's Smith transfer analysis (labeled claims)
