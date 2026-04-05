# Library Changelog

## 2026-03-30 (vasseur-pressure S2-E008 + S2-meta-E008)

### Chebyshev provably tight, all 4 De Giorgi steps tight, beta = 4/3 SHARP, analytic extremizer lesson: 1 new factual entry, 4 factual updates, 1 new meta entry, 0 meta updates

**New factual entries (1):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/chebyshev-sharpness-constant-field-extremizer.md` — Chebyshev bound PROVABLY TIGHT for div-free fields: constant field u_n = (lambda+1/n, 0, 0) achieves ratio -> 1. Div-free constrains direction not magnitude (three families: constant, shear, curl). L^2 and H^1 constraints improve by constant factor only (10-200x), never exponent. De Giorgi truncation also tight. All 4 chain steps (energy, Sobolev H^1->L^6, Holder interpolation, Chebyshev) now confirmed individually tight under NS constraints. beta = 4/3 rigorously SHARP within De Giorgi-Vasseur framework. SDP formalization (identified by S2-E007 as top priority) unnecessary — analytic extremizer is elementary. Closes open question from S2-E001 (direction a: structural Chebyshev improvement) and S2-E003 (div-free level-set distribution). Sixth evidence point for universality of 4/3 barrier.

**Updated factual entries (4):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — Added S2-E008 section: Chebyshev provably tight for div-free fields, all 4 chain steps tight, beta = 4/3 SHARP, SDP unnecessary (analytic extremizer), constant factor improvement from L^2/H^1.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/proposition-3-sharpness-audit.md` — Open question (div-free level-set distribution) RESOLVED: no improvement. Direction (a) CLOSED. All three S2-E001 directions (a, b, c) now CLOSED within the De Giorgi-Vasseur framework. Added S2-E008 section.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/chebyshev-universality-and-model-pde-comparison.md` — Open question about div-free level-set distribution RESOLVED by S2-E008: constant field proves no improvement; div-free constrains direction not magnitude; question CLOSED.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/vorticity-degiorgi-universal-barrier.md` — Added S2-E008 as sixth evidence point for universality of 4/3 barrier: Chebyshev step provably tight, all 4 chain steps individually tight. Updated combined 6-line evidence summary.

**New meta entries (1):**
- **Created** `meta/goal-design/allow-analytic-extremizer-over-computation.md` — When designing optimization-based explorations (SDP, LP, numerical), allow explorers to find analytic extremizers instead of over-specifying computational approach. S2-E008: goal described ~100-line CVXPY SDP; explorer found constant field u=(c,0,0) is a one-line extremizer making SDP unnecessary. Protocol: state mathematical question, specify computation as ONE tool, explicitly allow analytic solutions. Distinct from allow-explorer-synthesis (conclusions vs methods), check-bypass (framework choice), specify-computation-parameters (parameters when computation IS needed).

**Skipped meta items (0):**
- All meta items from s2-meta-E008 were filed.

**Updated indexes:** factual root INDEX (341->342), factual/navier-stokes/INDEX (44->45), factual/navier-stokes/vasseur-de-giorgi/INDEX (27->28), meta root INDEX, meta/goal-design/INDEX (39->40), CHANGELOG.

## 2026-03-30 (vasseur-pressure S2-E007 + S2-meta-E007)

### Adversarial review confirms beta = 4/3 obstruction, novel claim rankings, parallel-context lesson: 1 new factual entry, 4 factual updates, 1 new meta entry, 1 meta update

**New factual entries (1):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/s2-adversarial-review-beta-four-thirds.md` — Comprehensive adversarial review of Strategy-002 beta = 4/3 obstruction. 15-paper literature search confirms no published improvement (Vasseur 2025 arXiv:2503.02575 definitive confirmation). All 7 closure arguments survive attack (weakest: Route 1 modified functional, speculative only; strongest challenge: Route 5 DNS representativeness, mitigated by ABC). All 3 combination attacks fail (commutator+LP, modified functional+embedding, truncation+compensated compactness) — structural interlocking of truncation, Sobolev, Chebyshev. Tao (2016) supercritical barrier connection: generic methods cannot resolve NS regularity. Novel claims ranked by publishability: Claim 3 (seven-route obstruction) most significant at 8/10 novelty + 8/10 significance; Claims 1-4 combined publishable as single paper. SDP formalization identified as top priority for upgrading informal sharpness to rigorous result. Six missing directions ranked (SDP first, probabilistic third, geometric fourth).

**Updated factual entries (4):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/post-2007-beta-landscape.md` — Added Vasseur 2025 survey (arXiv:2503.02575) as definitive author confirmation of 4/3 barrier; added Lei-Ren 2024 and Tao 2016 connection; extended from 12 to 15 papers; added S2-E007 section.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — Added S2-E007 adversarial confirmation section: 7 closures survive, 3 combinations fail, Vasseur 2025 confirms, Tao 2016 connection, claim rankings, SDP formalization path.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/chebyshev-universality-and-model-pde-comparison.md` — Added S2-E007 adversarial verdicts on Claims 1 and 2: beta formula (7/10 correctness, 5/10 novelty) and SQG-NS gap (9/10 correctness, 6/10 novelty); both survive.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md` — Added S2-E007 adversarial review of informal sharpness (Claim 3): most significant novel claim; three combination attacks tested against closures; SDP formalization path for rigorous upgrade.

**New meta entries (1):**
- **Created** `meta/goal-design/adversarial-review-needs-complete-parallel-context.md` — Adversarial reviews launched in parallel with constructive explorations may lack findings from parallel work (S2-E007 flagged "non-CZ pressure incomplete" when S2-E006 had already resolved it). Protocol: launch adversarial reviews after constructive explorations complete (preferred), or include summaries of parallel work as supplementary context. Distinct from adversarial-check-between-phases (timing), preload-context (general loading), adversarial-synthesis-goal-structure (output format).

**Updated meta entries (1):**
- **Updated** `meta/goal-design/adversarial-synthesis-goal-structure.md` — Added two new variants from S2-E007: (1) ranked publishability format for novel claims (correctness/novelty/significance/publishability per claim, "fatal flaw?" column, "most publishable combination" assessment); (2) require specific formalization steps per informal claim (SDP approach was most actionable output of entire adversarial review).

**Skipped meta items (0):**
- All meta items from s2-meta-E007 were filed or incorporated into updates.

**Updated indexes:** factual root INDEX (340->341), factual/navier-stokes/INDEX (43->44), factual/navier-stokes/vasseur-de-giorgi/INDEX (26->27), meta root INDEX, meta/goal-design/INDEX (38->39), CHANGELOG.

## 2026-03-30 (vasseur-pressure S2-E006 + S2-meta-E006)

### Non-CZ pressure routes, tool-independence of 4/3, quantitative route comparison: 1 new factual entry, 4 factual updates, 2 new meta entries, 0 meta updates

**New factual entries (1):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/non-cz-pressure-routes-tool-independence.md` — Three non-CZ pressure routes computed: (1) direct IBP gives beta=1 (WORSE by 1/3); (2) H^1/BMO duality gives beta=4/3 (MATCHES CZ via completely different mechanism — U-scaling in ||v_k||_{H^1} not ||P^{21}||_{L^{3/2}}); (3) CRW commutator variant gives beta<=1 (confirms S2-E004). Also tested: W^{-1,q'}/W^{1,q} corrected to beta<=4/3; Lorentz refinement unchanged at 4/3. CZ consolidation gain = exactly 1/3 (maps bilinear product to single L^p, enabling Chebyshev extraction). CZ becomes loose at high k (ratio 0.2->92 from k=2 to k=5). 12 published approaches surveyed, none achieve beta>4/3 (barrier since 2007). DNS confirms CZ 2-3x tighter than direct at low k, both overestimate by 5-20x (consistent with nonlinearity depletion). Effective beta_eff ~ 2-3 in practice. Two genuinely untested approaches: Wolf local pressure decomposition (CZ-free, harmonic+particular), Tran-Yu depletion (unquantified at De Giorgi levels). **KEY CONCLUSION: beta=4/3 is TOOL-INDEPENDENT — locked to NS quadratic structure, not analytical method.** Fifth evidence point for universality of 4/3 barrier.

**Updated factual entries (4):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — Added S2-E006 section: non-CZ routes (IBP beta=1, H^1/BMO beta=4/3, CRW beta<=1), CZ consolidation gain 1/3, 12 approaches surveyed, tool-independence conclusion, two untested approaches.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/vorticity-degiorgi-universal-barrier.md` — Added S2-E006 as fifth evidence point for 4/3 universality: non-CZ methods (especially H^1/BMO) confirm tool-independence. Updated combined 5-line evidence summary.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md` — Added S2-E006 confirmation section: CRW consistently vacuous from test-function side; IBP quantifies consolidation gain; tool-independence established. Added cross-reference to new entry.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/proposition-3-sharpness-audit.md` — Added S2-E006 section: 1/2 + 5/6 chain is tool-independent (H^1/BMO recovers same decomposition via different mechanism); direction (b) closed by five independent routes; IBP gap = exactly 1/3 = Chebyshev extraction value.

**New meta entries (2):**
- **Created** `meta/methodology/tool-independence-stronger-than-single-failure.md` — When multiple independent analytical routes produce the same exponent/barrier, the result upgrades from "method X doesn't work" to "the barrier is intrinsic to the problem structure." Always compute at least two alternative routes when closing a direction. S2-E006: IBP+H^1/BMO+CRW all fail to improve 4/3, with H^1/BMO matching via completely different mechanism establishing tool-independence. Distinct from extract-precise-obstruction (one route), check-bypass (whether to avoid tool), ask-what-replaces-the-bottleneck (new bottleneck after reformulation).
- **Created** `meta/methodology/quantitative-comparison-reveals-why-standard-is-standard.md` — When closing a direction, compute the QUANTITATIVE gap between the closed route and the standard route. The magnitude and mechanism reveal why the standard method became standard, constraining future attempts. S2-E006: IBP beta=1 vs CZ beta=4/3 — gap of exactly 1/3 = CZ consolidation gain. Shows consolidation is ESSENTIAL not just convenient. Distinct from extract-precise-obstruction (what fails vs. why standard is better), distinguish-constant-from-scaling-slack (slack type), tool-independence (structural conclusion vs. mechanism explanation).

**Skipped meta items (1):**
- "Testing multiple variants of one idea in a single exploration was right scope" — already covered by one-task-per-exploration (exception clause for genuinely parallel computations with shared setup)

**Updated indexes:** factual root INDEX (339->340), factual/navier-stokes/INDEX (42->43), factual/navier-stokes/vasseur-de-giorgi/INDEX (25->26), meta root INDEX, meta/methodology/INDEX (49->51), CHANGELOG.

## 2026-03-30 (vasseur-pressure S2-E005 + S2-meta-E005)

### Frequency-localized De Giorgi LP obstruction, Bernstein poison pill, bypass-not-improve: 1 new factual entry, 4 factual updates, 2 new meta entries, 0 meta updates

**New factual entries (1):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/frequency-localized-degiorgi-lp-obstruction.md` — Littlewood-Paley frequency decomposition of P^{21} CANNOT improve beta. Four independent lines of evidence: (1) spectral peak shifts to higher frequencies with k; (2) high-frequency fraction of bottleneck integral grows from ~1% at k=1 to ~20% at k=6; (3) Bernstein inflation makes LP 5-10x worse than direct CZ; (4) all three LP approaches introduce growing 2^{alpha J} penalty. CZ IS the optimal frequency-by-frequency estimate. Bernstein exchange rate 2^{3j/5} is dimensional (Sobolev embedding cost in 3D), structural not technical. Paraproduct transition: resonance dominates low k, paraproduct T dominates high k (exactly CZ exponents). No single technique handles all De Giorgi levels. LP route CLOSED; three remaining directions (nonlinear dissipation, unique continuation, topological/geometric).

**Updated factual entries (4):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md` — Direction 2 (frequency-localized De Giorgi) now CLOSED by S2-E005; struck through in remaining directions list; cross-reference to new entry added.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — Added S2-E005 section: LP route closed, 4 independent lines of evidence, Bernstein exchange rate dimensional, paraproduct transition, 3 remaining directions.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/vorticity-degiorgi-universal-barrier.md` — Added S2-E005 as fourth evidence point for 4/3 universality: LP toolkit also saturates at 4/3.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/proposition-3-sharpness-audit.md` — Added S2-E005 section: LP/frequency-localized route non-viable, Bernstein exchange rate = dimensional cost of Step 3b, direction 2 closed.

**New meta entries (2):**
- **Created** `meta/methodology/bernstein-lp-poison-pill-3d.md` — Bernstein inequality exchange rate 2^{3j/5} per LP block in 3D is dimensional and destroys frequency-localized improvement attempts. General lesson: when target norm is L^p with p > 2, check if Bernstein cost 2^{dj(1/2-1/p)} is comparable to spectral decay. k-dependent character change (resonance -> paraproduct) means no single technique handles all De Giorgi levels, explaining barrier robustness. Distinct from extract-precise-obstruction (structural recognition vs. information extraction) and numerical-spectral-dns-diagnostic (interpretation vs. diagnostic tool).
- **Created** `meta/methodology/check-bypass-not-just-improve-bottleneck.md` — When a bottleneck tool limits progress, ask "can we avoid this tool entirely?" before "can we improve it?" Protocol: (1) bypass tool, (2) different tool for same job, (3) improve within framework. S2-E001 through S2-E005 spent 5 explorations on question 3; should have asked question 1 after S2-E001. Distinct from ask-what-replaces-the-bottleneck (new bottleneck after reformulation) and decomposition-audit (which step is tight vs. whether framework is right).

**Skipped meta items (1):**
- "Math explorer handled Bony paraproduct well" — already covered by parallel-math-explorer-explorations and one-task-per-exploration (three LP variants as one coherent task)

**Updated indexes:** factual root INDEX (338->339), factual/navier-stokes/INDEX (41->42), factual/navier-stokes/vasseur-de-giorgi/INDEX (24->25), meta root INDEX, meta/methodology/INDEX (47->49), CHANGELOG.

## 2026-03-30 (vasseur-pressure S2-E002 + S2-meta-E002)

### DNS level-set distribution and Chebyshev tightness, constant vs scaling slack: 1 new factual entry, 3 factual updates, 1 new meta entry, 0 meta updates

**New factual entries (1):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/dns-levelset-distribution-chebyshev-tightness.md` — DNS measurement of velocity distribution tails mu(lambda) ~ lambda^{-p}: IC-dependent exponents (TG p~10, Random p~8-9, ABC p~2.1 < 10/3 — Chebyshev tight or optimistic for Beltrami tails). De Giorgi Chebyshev tightness ratios ~3-5x across all ICs and k=1..8, k-independent (never growing exponentially; C ~ 0.87-0.89). Constant slack does NOT improve beta — only affects C in recurrence. Numerically confirms S2-E003 analytical circularity. Same-regime caveat (smooth DNS solutions). 7 cases at N=128, verified at N=64.

**Updated factual entries (3):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/chebyshev-universality-and-model-pde-comparison.md` — Added S2-E002 DNS numerical confirmation section: IC-dependent tails, ABC p < 10/3, constant tightness ratios. Added cross-reference.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/proposition-3-sharpness-audit.md` — Added S2-E002 DNS measurement of Chebyshev slack: moderate slack of wrong type (constant per level, not scaling with U_{k-1}).
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/cz-slack-k-independent.md` — Added S2-E002 companion: Chebyshev tightness ratios also k-independent, establishing both CZ and Chebyshev steps have constant-only slack on smooth DNS.

**New meta entries (1):**
- **Created** `meta/methodology/distinguish-constant-from-scaling-slack.md` — When measuring tightness of an inequality in a De Giorgi iteration, the key question is "does the slack scale with U_{k-1}^{-delta}?" not "is there slack?" Constant multiplicative slack (ratio independent of k and U) only affects C, not beta. Design measurement goals with this distinction from the start. S2-E002 tightness ratios were correctly interpreted, but the distinction should have been built into the exploration goal. Distinct from test-improvability (circularity) and decomposition-audit (target identification).

**Skipped meta items (3):**
- "E002 was partially superseded by E003" — already covered by test-improvability-before-pursuing-variations (the lesson that analytical results can deprioritize computational ones)
- "Parallel analytical+computational explorations work well for early Phase 1" — already covered by parallel-math-explorer-explorations
- "Reduce weight on computational confirmation when analytical is definitive" — minor variant of existing parallel-launch guidance

**Updated indexes:** factual root INDEX (337->338), factual/navier-stokes/INDEX (40->41), factual/navier-stokes/vasseur-de-giorgi/INDEX (23->24), meta root INDEX, meta/methodology/INDEX (46->47), CHANGELOG.

## 2026-03-30 (vasseur-pressure S2-E004 + S2-meta-E004)

### Compensated compactness / commutator obstruction, precise obstruction extraction, DNS spectral diagnostic: 1 new factual entry, 4 factual updates, 2 new meta entries, 0 meta updates

**New factual entries (1):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md` — Compensated compactness / commutator route to improving beta DEFINITIVELY CLOSED. Three-layer obstruction: (1) no div-curl structure — truncation breaks div(u)=0 with 0.07-0.14 compressibility error (O(enstrophy)); (2) commutator decomposition of P^{21} has non-commutator remainder dominating (61% of P^{21} in L^2, 18x at high frequencies) because div(u^{above}) != 0 (identically zero in SQG); (3) CRW vacuous for bounded multipliers (||u^{below}||_{BMO} = O(||u^{below}||_{L^infty}), identical to direct CZ). SQG-NS structural gap precisely characterized: scalar vs vector, linear vs quadratic, first-order vs second-order. Div-free truncation topologically impossible (degree theory). Informal theorem: beta = 4/3 sharp within energy+Sobolev+CZ(+commutator/CLMS)+Chebyshev class. Four remaining directions: nonlinear dissipation lower bounds, frequency-localized De Giorgi, quantitative unique continuation, topological/geometric constraints.

**Updated factual entries (4):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — Added S2-E004 cross-reference: compensated compactness / commutator route closed; informal sharpness theorem for energy+Sobolev+CZ+Chebyshev class.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/chebyshev-universality-and-model-pde-comparison.md` — Added S2-E004 SQG-NS gap further characterized section (six-property comparison table, three key differences, DNS verification); added cross-reference to new entry.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/proposition-3-sharpness-audit.md` — Added S2-E004 direction (b) tested via commutator: confirmed non-viable within CZ class; three obstructions; only non-CZ directions remain open.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/vorticity-degiorgi-universal-barrier.md` — Added S2-E004 as third evidence point for universality: entire CZ+commutator analytical toolkit saturates at 4/3.

**New meta entries (2):**
- **Created** `meta/methodology/extract-precise-obstruction-from-failed-route.md` — When a route fails, extract the precise mathematical obstruction (not just "doesn't work"). The precise failure point generates next directions. S2-E004: three independent obstructions each yielded specific leads (frequency-localized De Giorgi from "truncation kills div-free at high frequencies," div-free approximation from "remainder dominates because div(u^{above}) != 0," unbounded-but-BMO multiplier from "CRW vacuous for bounded"). Protocol: identify all layers, state precise condition that fails, state what would need to change, rank leads. Distinct from decisive-negative-pivot (pivot decision vs. information extraction) and useful-failure-extracts-secondary-results (accidental vs. deliberate).
- **Created** `meta/methodology/numerical-spectral-dns-diagnostic.md` — Numerical spectral analysis on DNS data (frequency-resolved energy decomposition) as diagnostic for mathematical PDE questions. Reveals high-frequency vs. low-frequency obstruction character invisible to analytical norms. S2-E004: commutator part had good high-frequency regularity but remainder dominated by 18x at k=20. Protocol: compute decomposition on DNS, spectral energy per component, compare decay rates, identify bottleneck at high frequencies. Distinct from sufficient-ic-diversity (IC selection vs. frequency analysis).

**Updated indexes:** factual root INDEX (336->337), factual/navier-stokes/INDEX (39->40), factual/navier-stokes/vasseur-de-giorgi/INDEX (22->23), meta root INDEX, meta/methodology/INDEX (44->46), CHANGELOG.

## 2026-03-30 (vasseur-pressure S2-E003 + S2-meta-E003)

### Chebyshev universality, model PDE comparison, improvability testing: 1 new factual entry, 3 factual updates, 2 new meta entries, 0 meta updates

**New factual entries (1):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/chebyshev-universality-and-model-pde-comparison.md` — Universal formula beta = 1 + s/n for De Giorgi recursion exponent confirmed across 9 model PDEs (Burgers, 2D NS, 3D NS, 4D NS, MHD, SQG direct, SQG extension, fractional NS alpha=5/4, fractional NS alpha=3/2). Brigati-Mouhot (2025) confirms for scalar equations. Chebyshev step NOT independently improvable — 6 routes ruled out (support-restricted, Holder interpolation, Lorentz, gradient/isoperimetric, L^2 Chebyshev, PDE-based integrability) or circular. SQG Caffarelli-Vasseur 2010 success mechanism: drift is multiplicative (BMO^{-1} constant), not additional U power; commutator structure, not Chebyshev improvement. Open question: does div(u)=0 improve level-set distribution? (genuinely open, no paper addresses). MHD confirmed beta=4/3 (He-Xin 2005). Fractional NS: De Giorgi misses Lions regularity by alpha gap (requires alpha=3/2 vs Lions 5/4).

**Updated factual entries (3):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — Added S2-E003 cross-reference: universal formula beta = 1 + s/n and Chebyshev circularity (improving L^{10/3} to L^4 requires H^{5/4} = Lions threshold).
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/vorticity-degiorgi-universal-barrier.md` — Added S2-E003 universal formula confirmation across 9 model PDEs; SQG extension gives same 4/3 but closes via multiplicative drift.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/proposition-3-sharpness-audit.md` — Added S2-E003 Chebyshev circularity assessment: all 6 improvement routes ruled out; directions (b) and (c) from sharpness audit are the only non-circular options; added open question on div-free level-set distribution.

**New meta entries (2):**
- **Created** `meta/methodology/model-pde-comparison-for-mechanism-identification.md` — Cross-PDE comparison reveals universal formulas and pinpoints exception mechanisms. S2-E003: comparing beta across Burgers/2DNS/SQG/MHD/fractional NS produced two major insights in one exploration (universal formula + SQG exception mechanism). Protocol: 4-6 model PDEs, compute barrier for each, tabulate, identify formula or exceptions. Distinct from comparison-exploration-pattern and gap-finding.
- **Created** `meta/methodology/test-improvability-before-pursuing-variations.md` — Test circularity of identified target step before pursuing variations. S2-E003: 6 Chebyshev improvement routes all ruled out or circular in one exploration; saved 3+ explorations on provably futile Lorentz/interpolation/support tricks. Protocol: enumerate routes, classify as impossible/insufficient/circular/open; if none open, pivot. Distinct from decomposition-audit (target vs. viability) and decisive-negative-pivot (dimensional analysis vs. circularity).

**Updated indexes:** factual root INDEX (335->336), factual/navier-stokes/INDEX (38->39), factual/navier-stokes/vasseur-de-giorgi/INDEX (21->22), meta root INDEX, meta/methodology/INDEX (42->44), CHANGELOG.

## 2026-03-30 (vasseur-pressure S2-E001 + S2-meta-E001)

### Proposition 3 sharpness audit, decomposition audit methodology: 1 new factual entry, 2 factual updates, 2 new meta entries, 0 meta updates

**New factual entries (1):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/proposition-3-sharpness-audit.md` — Line-by-line sharpness audit of Vasseur (2007) Proposition 3. Complete sensitivity table (8 steps with dβ/dδ), 5/6 genealogy (H^1→L^6→L^{10/3}→Chebyshev→L^2 norm), all 5 free parameters assessed and exhausted. Single potentially improvable step: Chebyshev inequality applied to NS solutions (sharp for arbitrary L^{10/3} functions, potentially loose for NS). Three improvement directions ranked. Vorticity cross-comparison confirms identical 1/2 + 5/6 chain.

**Updated factual entries (2):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — Added S2-E001 cross-reference to sharpness audit (complete sensitivity table and free parameter analysis).
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/vorticity-degiorgi-universal-barrier.md` — Added S2-E001 detailed cross-comparison data confirming identical 1/2 + 5/6 chain in both velocity and vorticity formulations, with identical exhausted free parameters.

**New meta entries (2):**
- **Created** `meta/methodology/decomposition-audit-before-attacking-barrier.md` — Always run a line-by-line proof reading + sharpness classification before attacking a mathematical barrier. S2-E001 narrowed 5 open Track B directions to 1, saving 3+ explorations. Distinct from definition-extraction-gates-computation and gap-finding.
- **Created** `meta/goal-design/require-sensitivity-table-for-proof-analysis.md` — Require tabular output format for proof chain analysis: step, tool, exponent, sensitivity, sharpness. Forces per-step assessment. Complementary to decomposition-audit-before-attacking-barrier.

**Updated indexes:** factual root INDEX (334->335), factual/navier-stokes/INDEX (37->38), factual/navier-stokes/vasseur-de-giorgi/INDEX (20->21), meta root INDEX, meta/goal-design/INDEX (37->38), meta/methodology/INDEX (41->42), CHANGELOG.

## 2026-03-30 (vasseur-pressure E009 + meta-E009)

### Strategy-001 adversarial synthesis: 1 new factual entry, 9 factual updates, 0 new meta entries, 2 meta updates

**New factual entries (1):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/strategy-001-adversarial-synthesis.md` — Strategy-001 adversarial review synthesis: claim survival table (6 claims, grades B to C+), novel contributions confirmed (Beltrami-De Giorgi connection, computational De Giorgi methodology, dual-mechanism universality). Strongest finding: Lamb vector -> CZ loss connection. Weakest claim: truncation Beltrami preservation. Strategy-002 recommendations: analytical Beltrami-beta connection, abandon DNS tightness, consider vorticity formulation.

**Updated factual entries (9):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/vorticity-degiorgi-universal-barrier.md` — Added E009 adversarial: "universality" is induction from 2 examples, not theorem. Corrected framing: strong evidence, not proved universal.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/cz-slack-k-independent.md` — Added E009 adversarial: measurement on wrong regime (smooth solutions, not near-singular). Survives as empirical fact, not evidence about analytical bound tightness.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/dns-beta-empirical-results.md` — Added E009 adversarial: smooth-solution tautology. Measurement survives; interpretation does NOT. ABC corroboration is salvageable.
- **Updated** `factual/navier-stokes/beltrami-pressure-analytical.md` — Added E009 adversarial: mechanism correct, practical significance uncertain. Exact Beltrami trivially regular; near-Beltrami needs quantitative ||L|| -> beta bound.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/beltrami-deficit-truncation-survival.md` — Added E009 adversarial: DOES NOT SURVIVE AS STATED. Trivially expected for smooth truncation, near-Beltrami uncharacterized, div(u_below) != 0, missing beta connection. WEAKEST CLAIM in Strategy-001.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/bottleneck-exponent-dns.md` — Added E009 adversarial: DNS evidence cannot diagnose near-singular bounds. Gap genuineness supported by analytical evidence only.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/abc-beltrami-degiorgi-advantage.md` — Added E009 adversarial: strongest surviving finding is the structural Lamb vector -> CZ loss story.
- **Updated** `factual/navier-stokes/near-beltrami-pressure-perturbation.md` — Added E009 adversarial: mechanism discontinuous at analytical level; key open task is quantitative Beltrami-beta connection.
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/pressure-bernoulli-dominance-truncated.md` — Added E009 adversarial: shares Claim 5 limitations.

**Updated meta entries (2):**
- **Updated** `meta/goal-design/adversarial-synthesis-goal-structure.md` — Added four new variants from E009: evidence grading (A/B/C/D/F per claim), weakest-link deliverable, novel claims list by adversarial reviewer (not original explorer), require fix specification per weakness.
- **Updated** `meta/methodology/adversarial-check-between-phases.md` — Added timing refinement: run adversarial after key mechanism identified/tested but before extended test (E009 timing was ideal).

**Updated indexes:** factual root INDEX (332->333), factual/navier-stokes/INDEX (35->36), factual/navier-stokes/vasseur-de-giorgi/INDEX (19->20), meta root INDEX, meta/goal-design/INDEX, meta/methodology/INDEX, CHANGELOG.

## 2026-03-30 (vasseur-pressure E007 + meta-E007)

### Beltrami deficit truncation survival, pressure Bernoulli dominance: 2 new factual entries, 2 factual updates, 0 new meta entries, 2 meta updates

**New factual entries (2):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/beltrami-deficit-truncation-survival.md` — De Giorgi truncation preserves Beltrami structure: B_k = O(2^{-k}), lambda_opt = -1.000 at all k, Re-independent. Controls (TG, RG) show B_k ~ const. Truncation breaks div-free (||div(u_below)|| = O(2^{-k})) but Beltrami deficit still vanishes. Resolves key obstacle from E006.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/pressure-bernoulli-dominance-truncated.md` — Truncated pressure for ABC is Bernoulli-dominated: R_frac = O(2^{-k}) (3.7% at k=4, 0.04% at k=8). Bottleneck remainder I_r/I_t = O(2^{-k}) (4.4% at k=4, 0.2% at k=8). Non-Beltrami controls show R_frac > 1. Effective CZ constant ~ 1.0 for Beltrami. Sign error caught by t=0 sanity check.

**Updated factual entries (2):**
- **Updated** `factual/navier-stokes/near-beltrami-pressure-perturbation.md` — Key obstacle section updated: truncation breaking Beltrami RESOLVED by E007 (B_k = O(2^{-k}), R_frac = O(2^{-k})).
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/abc-beltrami-degiorgi-advantage.md` — Added "Truncation Survival" section referencing E007 results; updated actionable insight to note key obstacle is resolved.

**Updated meta entries (2):**
- **Updated** `meta/methodology/include-trivial-control-checks.md` — Added two new variants: known-answer validation at exact-solution conditions (t=0 Beltrami sanity check caught sign error propagated from prior code); verify mathematical identity before building measurements (div(u_below) != 0 invalidated prescribed Lamb decomposition).
- **Updated** `meta/goal-design/one-task-per-exploration.md` — Added vasseur-pressure E007 as additional evidence for two-linked-tasks corollary (Task A + Task B shared DNS setup, handled cleanly).

**Updated indexes:** factual root INDEX (330->332), factual/navier-stokes/INDEX (33->35), factual/navier-stokes/vasseur-de-giorgi/INDEX (17->19), meta root INDEX, meta/goal-design/INDEX, meta/methodology/INDEX, CHANGELOG.

## 2026-03-30 (vasseur-pressure E008 + meta-E008 + philosopher-atlas H^1 report)

### Vorticity De Giorgi universal barrier, H^1 dead end: 2 new factual entries, 1 new meta entry

**New factual entries (2):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/vorticity-degiorgi-universal-barrier.md` — Vasseur-Yang (2021) vorticity-based De Giorgi: pressure-free variable v, iteration CLOSES (beta=4/3 > 1 with small U_0), but universal 4/3 barrier from trilinear form (1/2 + 5/6), NOT pressure. Full local bootstrap to C^infinity under local smallness. Beltrami connection: omega x u = 0 gives heat equation.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/h1-pressure-dead-end.md` — Three H^1 routes (H^1-BMO, atomic decomposition, interpolation) all fail at the W^{1,3} wall. Far-field pressure is the sole obstruction. Bogovskii correction strictly worse. ||p||_{H^1} is a fixed constant. Structural dead end.

**New meta entries (1):**
- **Created** `meta/goal-design/ask-what-replaces-the-bottleneck.md` — When testing alternative formulations against a known barrier, always ask "what is the NEW bottleneck?" Same value from different mechanism = structural obstruction.

**Updated indexes:** factual root INDEX (328->330), factual/navier-stokes/INDEX (31->33), factual/navier-stokes/vasseur-de-giorgi/INDEX (15->17), meta root INDEX, meta/goal-design/INDEX (36->37), CHANGELOG.

## 2026-03-30 (vasseur-pressure E005 + meta-E005 + E006 + meta-E006)

### Post-2007 De Giorgi landscape, Choi-Vasseur 2014, Beltrami analytical: 6 new factual entries, 1 factual update, 1 new meta entry, 3 meta updates

**New factual entries (6):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/choi-vasseur-2014-decomposition.md` — CV14 three-way decomposition P = P_{1,k} + P_{2,k} + P_3 with P_3 absorption into time-dependent truncation level. Achieves beta = 7/6 (weaker than 4/3, sufficient for their goal). Does NOT bypass P_k^{21} bottleneck.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/post-2007-beta-landscape.md` — Comprehensive survey: NO paper since 2007 has improved beta beyond 4/3. Community moved orthogonally (higher derivatives, epsilon-regularity, other equations). 12-paper table.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/fernandez-dalgo-2025-dynamic-pressure.md` — arXiv:2501.18402v2, dynamic pressure decomposition in paraboloid geometry. Gronwall methods, NOT De Giorgi iteration. About epsilon-regularity, not beta.
- **Created** `factual/navier-stokes/geometric-regularity-criteria.md` — Survey of Constantin-Fefferman (1993), Beirao da Veiga-Berselli (2002), Vasseur (2007), etc. Smoothness of vorticity/velocity direction implies regularity. For Beltrami: vorticity direction = velocity direction.
- **Created** `factual/navier-stokes/beltrami-pressure-analytical.md` — Exact derivation: Beltrami L = omega x u = 0, p = -|u|^2/2 + const, CZ loss = 0, u(t) = u_0 exp(-nu lambda^2 t). Verified to machine precision on ABC.
- **Created** `factual/navier-stokes/near-beltrami-pressure-perturbation.md` — Perturbation analysis: bad pressure O(eps), continuous linear degradation. Key obstacle: truncation breaks Beltrami. Conditional regularity conjecture via Beltrami deficit. Grade B.

**Updated factual entries (1):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/abc-beltrami-degiorgi-advantage.md` — Physical mechanism section expanded with E006 analytical derivation (Lamb vector = 0, Bernoulli pressure, zero CZ loss).

**New meta entries (1):**
- **Created** `meta/goal-design/flag-cross-framework-connections.md` — When two independently well-studied frameworks haven't been connected in the literature, flag the intersection as potential novel territory.

**Updated meta entries (3):**
- **Updated** `meta/methodology/gap-finding-in-existing-programs.md` — Added "landscape of attempts" variant: survey what the community has TRIED (including failures), not just achieved. Table format forces completeness and makes negative results visible.
- **Updated** `meta/goal-design/request-equations-for-construction.md` — Added "derive WHY" variant: when a follow-up literature survey investigates a computationally identified mechanism, always include a derivation request.
- **Updated** `meta/methodology/standard-explorer-for-literature-surveys.md` — Added "when NOT to apply" case: when survey includes perturbation analysis or computational verification, consider math explorer instead.

**Updated indexes:** factual root INDEX (322->328), factual/navier-stokes/INDEX (25->31), factual/navier-stokes/vasseur-de-giorgi/INDEX (12->15), meta root INDEX, meta/goal-design/INDEX (35->36), meta/methodology/INDEX, CHANGELOG.

## 2026-03-30 (vasseur-pressure E002 + meta-E002)

### DNS beta measurement: 3 new factual entries, 1 factual update, 1 new meta entry, 1 meta update

**New factual entries (3):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/dns-beta-empirical-results.md` — Full DNS measurement of beta_eff across 5 ICs x 4 Re x 2 resolutions. All beta_eff < 4/3 (max 1.01 for ABC at Re=1000). Strong IC dependence. L^inf normalization required. Critical caveat: beta_eff != beta_p.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/bottleneck-exponent-dns.md` — Bottleneck exponent gamma (P_k^{21} pressure integral scaling) DECREASES with Re for all ICs. At Re>=500, most show gamma < 1. The 4/3 bound is NOT loose — the gap between 4/3 and 3/2 is genuine.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/abc-beltrami-degiorgi-advantage.md` — ABC (Beltrami) flow uniquely favorable: highest beta_eff (1.01), best R^2 (0.999), most stable gamma (1.10-1.22), beta_eff increases with Re. Suggests conditional regularity via Beltrami-like structure.

**Updated factual entries (1):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/dns-beta-measurement.md` — Approaches A (direct iteration) and B (bottleneck term) marked as TESTED with E002 results. Answer: empirical beta does NOT exceed 4/3.

**New meta entries (1):**
- **Created** `meta/methodology/sufficient-ic-diversity-for-outliers.md` — For measurement campaigns, use 5+ ICs covering different structural classes. ABC was the 5th IC and produced the most important finding. Fewer ICs would have missed it.

**Updated meta entries (1):**
- **Updated** `meta/goal-design/distinguish-typical-vs-worst-case-bounds.md` — Added "empirical analogue vs analytical quantity" variant: when computing empirical analogues of analytical bounds, require explicit statement of what the empirical quantity IS and ISN'T (beta_eff != beta_p).

**Updated indexes:** factual root INDEX (319->322), factual/navier-stokes/INDEX (22->25), factual/navier-stokes/vasseur-de-giorgi/INDEX (9->12), meta root INDEX, meta/goal-design/INDEX, meta/methodology/INDEX (39->40), CHANGELOG.

## 2026-03-30 (vasseur-pressure E003 + meta-E003)

### Tran-Yu Galilean invariance assessment: 2 new factual entries, 2 meta updates

**New factual entries (2):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/tran-yu-galilean-invariance-orthogonal.md` — Tran-Yu 5-paper program (2015-2021) on pressure moderation and Galilean invariance is ORTHOGONAL to De Giorgi bottleneck. Different energy functionals (global L^q vs level-set), different pressure objects (full p vs P_k^{21}), Galilean boost doesn't help P_k^{21}. Grade C (not applicable). Two potentially useful ideas noted.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/pressure-galilean-invariance.md` — Pressure Poisson equation is exactly Galilean-invariant for incompressible flow (div u = 0 kills cross-terms). CZ bound unchanged by any constant-velocity frame shift.

**Updated meta entries (2):**
- **Updated** `meta/goal-design/name-specific-authors-and-papers.md` — Added "also survey related approaches by same group/school" variant. Source: vasseur-pressure E003 (most valuable finding was incidental Choi-Vasseur discovery).
- **Updated** `meta/goal-design/verify-goal-claims-before-delegating.md` — Added "verify paper existence before citing" variant. Source: vasseur-pressure E003 ("Tran-Yu (2014, AIHP)" doesn't exist; actual program is 5 papers 2015-2021).

**Updated indexes:** factual root INDEX (317→319), factual/navier-stokes/INDEX (20→22), factual/navier-stokes/vasseur-de-giorgi/INDEX (7→9), meta root INDEX, meta/goal-design/INDEX, CHANGELOG.

## 2026-03-30 (vasseur-pressure E004 + meta-E004)

### CZ slack k-independence: 2 new factual entries, 1 factual update, 1 meta update

**New factual entries (2):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/cz-slack-k-independent.md` — CZ tightness ratio for P_k^{21} converges to k-independent constant by k~3-4. FALSIFIES hypothesis that CZ slack could improve beta beyond 4/3. Slack ranges 1.7-3.9x (q=2) to 5.5-18.4x (q=8), all constant in k.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/p21-tighter-than-full-pressure.md` — P_k^{21} has LESS CZ slack than full pressure (1.7-3.9x vs 7.6-17.5x at q=2). Bottleneck piece's tensor is smoother/more structured.

**Updated factual entries (1):**
- **Updated** `factual/navier-stokes/vasseur-de-giorgi/dns-beta-measurement.md` — Approach C (CZ slack proxy) marked as TESTED and ELIMINATED. P21 CZ slack is k-independent and less than full pressure.

**Updated meta entries (1):**
- **Updated** `meta/goal-design/specify-failure-paths.md` — Added "quantitative falsification criterion" variant for hypothesis-testing computations + "seed alternative paths" extension. Source: vasseur-pressure E004.

## 2026-03-30 (vasseur-pressure E001 + meta-E001)

### Vasseur De Giorgi Framework: 5 new factual entries in new subfolder; meta: definition-extraction gates computation + specify-rigor-level evidence

**New factual entries (5):**
- **Created** `factual/navier-stokes/vasseur-de-giorgi/beta-definition-recurrence-exponent.md` — Beta is the nonlinear recurrence exponent in De Giorgi iteration (NOT a pressure integrability exponent). Defined via Proposition 3, eq. (5).
- **Created** `factual/navier-stokes/vasseur-de-giorgi/beta-threshold-three-halves.md` — Beta > 3/2 implies all suitable weak solutions are regular. Proved in Vasseur's Appendix. Conjecture 14 states this is achievable.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — Current beta < 4/3 from single bottleneck: non-divergence local pressure P_k^{21}. Term-by-term exponent table. Gap of 1/6 is qualitative.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/de-giorgi-iteration-structure.md` — 7-step iteration procedure. Beta enters at Step 4 (Sobolev + Chebyshev power raising). Beta_p = minimum over all term exponents.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/dns-beta-measurement.md` — Three DNS measurement approaches (direct iteration, bottleneck term, CZ slack proxy). Partially computable: ~10-15 useful De Giorgi levels.
- **Created** `factual/navier-stokes/vasseur-de-giorgi/INDEX.md` — Subfolder index for the 5 entries.

**New meta entries (1):**
- **Created** `meta/methodology/definition-extraction-gates-computation.md` — Phase 0 definition-extraction prevents computing the wrong thing. Vasseur-pressure: team assumed beta = pressure integrability; reading the paper revealed beta = De Giorgi recurrence exponent.

**Updated meta entries (1):**
- **Updated** `meta/goal-design/specify-rigor-level.md` — Added vasseur-pressure evidence for "What EXACTLY is...?" pattern: can force discovery of incorrect assumptions, not just extract precise definitions.

**Updated indexes:** factual root INDEX (310→315), factual/navier-stokes/INDEX (13→18), meta root INDEX, meta/methodology/INDEX (38→39), meta/goal-design/INDEX, CHANGELOG.

## 2026-03-30 (navier-stokes E008 adversarial review + meta-E008)

### Navier-Stokes: Adversarial review weakens/downgrades 6 entries; meta: pre-specify attack vectors + dual-mode adversarial

**Updated factual entries (7):**
- **Updated** `factual/navier-stokes/bkm-near-tightness-226x-advantage.md` — MAJOR REVISION: downgraded confidence verified→provisional. "226x advantage" weakened to ~80x with theoretical constants. Added 4 adversarial attacks: (1) comparison is apples-to-oranges (BKM bounds ||nabla u||_{L^inf}, Ladyzhenskaya bounds VS — different mathematical quantities), (2) 1.05x slack is circular from empirical C_BKM calibration (with theoretical C, slack is ~3x), (3) BKM tightness is CZ theory not NS-specific, (4) doesn't transfer to regularity theory (requires L^inf control). Direction correct, headline number misleading.
- **Updated** `factual/navier-stokes/vortex-stretching-structural-slack.md` — softened "irreducible" to "lower bound over tested ICs"; added Protas (2020, JFM 893) as untested adversarial IC type; added 3-factor decomposition tautology caveat.
- **Updated** `factual/navier-stokes/adversarial-minimum-vs-slack.md` — added Protas (2020) reference as strongest untested challenge.
- **Updated** `factual/navier-stokes/bmo-kozono-taniuchi-criterion.md` — downgraded confidence verified→provisional; added 5 adversarial caveats (ball sampling underestimates, single IC, limited Re, universality unsupported).
- **Updated** `factual/navier-stokes/divergence-free-flatness-reduction.md` — KEY CORRECTION: (5/9)^{1/4} factor is NOT about div-free constraint, is purely vector-vs-scalar Gaussian effect. Confirmed numerically (div-free vs non-div-free identical). Misattributed. Applies only to Gaussian, not actual NS.
- **Updated** `factual/navier-stokes/conditional-vortex-stretching-bound.md` — added 4 adversarial caveats (narrow F₄ range, no F₄ boundedness proof, TGV symmetry bias, no theoretical justification).
- **Updated** `factual/navier-stokes/spectral-ladyzhenskaya-negative-result.md` — added local optima concern for phase optimization; added Bernstein alternative interpolation path.

**Updated meta entries (1):**
- **Updated** `meta/goal-design/adversarial-proof-review-structure.md` — Added "pre-specify 3-4 attack vectors per claim" variant (NS E008: directed reviewer to productive criticisms, caught apples-to-oranges and (5/9)^{1/4} misattribution). Added "dual-mode adversarial: standard + math explorer" variant (standard-only missed opportunity for independent numerical recomputation).

**Updated indexes:** factual root INDEX, factual/navier-stokes/INDEX, meta root INDEX, meta/goal-design/INDEX, CHANGELOG.

## 2026-03-30 (navier-stokes E007 BKM advantage + intermittency + meta-E007)

### Navier-Stokes: BKM near-tight (1.05x slack, 226x advantage over Ladyzhenskaya); BMO criterion; intermittency measures; conditional bound; meta: quantitative proof approach comparison

**New factual entries (4):**
- **Created** `factual/navier-stokes/bkm-near-tightness-226x-advantage.md` — BKM bound has 1.05x slack (near-tight), 226x advantage over Ladyzhenskaya. Calibrated C_BKM ≈ 0.68 (2.7x over R³ theoretical). Agmon intermediate at 12.4x. Re-independent minimum slack. Headline finding: 237x slack is artifact of Ladyzhenskaya interpolation chain.
- **Created** `factual/navier-stokes/bmo-kozono-taniuchi-criterion.md` — BMO/L^inf ratio ~0.25-0.27 across Re=100-5000. Kozono-Taniuchi criterion ~4x tighter. Remarkably Re-stable (universal structure). BMO peaks at intermediate radii.
- **Created** `factual/navier-stokes/vorticity-intermittency-measures.md` — Flatness F4 = 2-12x Gaussian. Only 1-2.4% of domain has |omega| > 0.5*omega_max. C_{L,eff}/C_L ~ F4^{-0.30}. 4x residual from geometric alignment.
- **Created** `factual/navier-stokes/conditional-vortex-stretching-bound.md` — Conjectured: C(F4) ≈ 0.003/F4 (global), envelope 0.0035*F4^{-0.85}. Improvement 237-1659x. Not verified on other ICs.

**Updated meta entries (1):**
- **Updated** `meta/methodology/comparison-exploration-pattern.md` — Added "quantitative proof approach comparison" variant: comparing existing proof approaches head-to-head on shared computational data is underexploited methodology. NS E007 BKM vs Ladyzhenskaya comparison was the most valuable finding.

**Updated indexes:** factual root INDEX (306→310), factual/navier-stokes/INDEX (6→10), meta root INDEX, meta/methodology/INDEX, CHANGELOG.

## 2026-03-30 (navier-stokes E006 spectral Ladyzhenskaya + meta-E006)

### Navier-Stokes: Spectral Ladyzhenskaya NEGATIVE RESULT — cannot tighten sharp constant; Gaussian typical-case formula; div-free factor; meta: typical vs worst-case bounds

**New factual entries (3):**
- **Created** `factual/navier-stokes/spectral-ladyzhenskaya-negative-result.md` — Spectral support alone CANNOT improve sharp Ladyzhenskaya constant as worst-case bound. LP cross terms dominate (63% for Kolmogorov). Phase-optimized fields achieve near-sharp constants. Most promising direction: flatness bounds.
- **Created** `factual/navier-stokes/gaussian-effective-ladyzhenskaya.md` — Gaussian CLT regime: C_{L,eff} = 3^{1/4}(||f||/||∇f||)^{3/4} → 1.707 × Re^{-3/8} for Kolmogorov. At Re=1000: 0.125 (632× slack reduction). TYPICAL only, not worst-case bound. Measured NS ~18% above Gaussian.
- **Created** `factual/navier-stokes/divergence-free-flatness-reduction.md` — (5/9)^{1/4} ≈ 0.8633 uniform reduction from vector vs scalar Gaussian flatness. Analytically derived, numerically verified to 4 sig figs.

**New meta entries (1):**
- **Created** `meta/goal-design/distinguish-typical-vs-worst-case-bounds.md` — Bound-tightening goals must require typical/worst-case classification. Prompted by C_{L,eff} ~ Re^{-3/8} being impressive but unusable as proof tool.

**Updated meta entries (1):**
- **Updated** `meta/methodology/decisive-negative-pivot.md` — Added "direction-eliminating negatives as high-value Phase 3 outputs" section with navier-stokes E006 evidence.

**Updated indexes:** factual root INDEX (303→306), factual/navier-stokes/INDEX (3→6), meta root INDEX, meta/goal-design/INDEX (34→35), meta/methodology/INDEX, CHANGELOG.

## 2026-03-30 (navier-stokes E003 adversarial IC search + meta-E003)

### Navier-Stokes: NEW domain folder — adversarial minimum VS slack 157.70x, structural gap 158x, Beltrami zero-VS; meta: anticipate symmetry degeneracies

**New factual entries (3):**
- **Created** `factual/navier-stokes/` folder (NEW domain)
- **Created** `factual/navier-stokes/adversarial-minimum-vs-slack.md` — Anti-parallel tubes sigma=2.5 achieve 157.70x (N=128 converged), 34% below TGV's 236.90x. Bowl-shaped sigma-dependence. Five-IC comparison. Re-independent.
- **Created** `factual/navier-stokes/vortex-stretching-structural-slack.md` — 158x irreducible structural gap in VS bound proof chain. Holder + Ladyzhenskaya decomposition. VS bound not regularity bottleneck. Geometric universality conjecture.
- **Created** `factual/navier-stokes/beltrami-zero-vortex-stretching.md` — ABC (Beltrami) and z-invariant flows have VS=0 identically by symmetry.

**New meta entries (1):**
- **Created** `meta/goal-design/anticipate-symmetry-degeneracies-in-ics.md` — Anticipate symmetry degeneracies (z-invariance, Beltrami) that make measured quantities vanish identically; flag or exclude in goal.

**Cross-references added:**
- `factual/navier-stokes/INDEX.md` → `factual/yang-mills/szz-lemma-4-1-hessian-slack.md` (analogous structural slack in proof bounds)
- `factual/yang-mills/INDEX.md` → `factual/navier-stokes/adversarial-minimum-vs-slack.md` (reciprocal)

**Updated indexes:** factual root INDEX (300→303, 20→21 categories), factual/yang-mills/INDEX (cross-reference), meta root INDEX (navier-stokes mission added), meta/goal-design/INDEX (33→34), CHANGELOG.

## 2026-03-29 (yang-mills-validation E001-E007 bulk processing — 8 factual reports + 7 meta notes)

### YM Validation: Adversarial proof review (β < 1/6 proof chain INVALID), CNS novelty confirmed, SU(3) extension, d=5 anomaly resolved, formula corrections, meta updates

**New factual entries (4):**
- **Created** `factual/yang-mills/adversarial-review-proof-chain.md` — β < 1/6 proof chain INVALID at Step 2: HessS ≠ (β/2N)Σ|B_□|² at general Q (exact only at flat connections). Commutator cross terms unbounded. SZZ citation correction (Cor 1.6 not "Thm 1.3"). Mass gap = lattice spectral gap clarification.
- **Created** `factual/yang-mills/cns-novelty-assessment.md` — β < 1/6 NOT in CNS papers, NOT trivially derivable. CNS vertex bound TIGHT in their formulation. Equation-level comparison table. CNS proves area law not mass gap.
- **Created** `factual/yang-mills/su3-extension-hnorm.md` — SU(3) H_norm(I) = 1/27. General formula d/(4(d-1)N²) with N² not N. 120+ configs tested. CS threshold β < 3/8 for SU(3).
- **Created** `factual/yang-mills/d5-anomaly-eigenstructure.md` — λ_max(M(I)) = 4d for ALL d. Even/odd dichotomy: staggered mode maximizer only for even d. Corrects prior formula ⌈d/2⌉⌊d/2⌋ to d/(4(d-1)N²). Pascal-triangle multiplicities.

**Updated factual entries (3):**
- **CRITICAL CORRECTION** `factual/yang-mills/fourier-hessian-proof-q-identity.md` — H_norm ≤ 1/8 changed from [PROVED] to [CONJECTURED — proof incomplete] (commutator cross terms not bounded by Lemma 5.1). Formula corrected from ⌈d/2⌉⌊d/2⌋ to d/(4(d-1)N²). Threshold table rows marked [CONJECTURED].
- **Updated** `factual/yang-mills/hnorm-conjecture-numerical-resolution.md` — Added L=4 (21 configs), L=6 (11 configs), SU(3) (120+ configs) verification data. ARPACK artifact warning.
- **Updated** `factual/yang-mills/INDEX.md` — Count 24→28, new Extensions and Verification subsection.

**Updated meta entries (3):**
- **Updated** `meta/methodology/include-trivial-control-checks.md` — Non-trivial control variant: for convention verification, test at non-identity config (e.g., iσ₃) because Q=I hides formula differences.
- **Updated** `meta/goal-design/prioritize-novelty-assessment.md` — Equation-level comparison variant for novelty assessment.
- **Updated** `meta/goal-design/verify-goal-claims-before-delegating.md` — Verify analytical predictions independently variant (don't trust GOAL.md formulas without re-deriving).

**Updated indexes:** factual root INDEX (296→300), factual/yang-mills/INDEX (24→28), meta root INDEX, meta/methodology/INDEX, meta/goal-design/INDEX, CHANGELOG.

## 2026-03-29 (yang-mills-conjecture S003-exploration-004-lambda-min-adversarial + S003-meta-004)

### YM Conjecture: Adversarial characterization of sup|λ_min(HessS)|; β < 1/4 ruled out; conditional β < 1/8 via decoherence; meta: domain-specific structured starts

**New factual entries:**
- **Created** `factual/yang-mills/hessian-lambda-min-adversarial.md` — Adversarial optimization (35+ starts, 2000+ configs) finds empirical sup|λ_min(HessS)| = 14.73 (d=4, L=2, SU(2)); GD-optimized anti-instanton (axes (0,0,2,1)) is extremal. β < 1/4 RULED OUT (|λ_min| = 14.73 >> 2d = 8). Decoherence conjecture (||C(Q)|| ≤ 2(d+1), numerically supported for all 2000+ configs) gives conditional β < 1/8 if proved. D/C anti-correlation mechanism identified. Dimension scaling |λ_min|/4d ≈ 0.85–0.92. L=2 worst case.

**Updated factual entries:**
- **Updated** `factual/yang-mills/shen-zhu-zhu-stochastic-analysis.md` — Added pointer in Extension Strategies Option 1 to the new conditional β < 1/8 result via D+C decoherence approach.

**Updated meta entries:**
- **Updated** `meta/methodology/budget-adversarial-for-high-dim.md` — Added "domain-specific structured starts" variant: physics-motivated extremal configurations (anti-instantons) as GD seeds found 63% more negative eigenvalue than random-start GD.

**Updated indexes:** factual root INDEX (295→296), factual/yang-mills/INDEX (23→24), meta/INDEX, meta/methodology/INDEX, CHANGELOG.

## 2026-03-29 (yang-mills-validation S002-exploration-002 + S002-meta-exploration-002)

### YM Validation: Complete analytical Hessian formula with commutator cross terms; C = C_curv + C_comm decomposition; meta: decompose corrections into PSD + indefinite

**New factual entries:**
- **Created** `factual/yang-mills/hessian-analytical-formula-c-decomposition.md` — Complete analytical second derivative formula for SU(2) Wilson action including commutator cross terms (mean |comm/w²U| = 3.12, often dominant). SU(2) cross-product simplification. C = C_curv (PSD) + C_comm (indefinite) decomposition. C has 41 negative eigenvalues but λ_max(H_actual) ≤ λ_max(H_formula) holds (ratio 0.61–0.74). Three proof strategies identified.

**Updated factual entries:**
- **Updated** `factual/yang-mills/b-square-inequality-proof-progress.md` — Expanded M(Q) ≠ Hessian section with analytical details from yang-mills-validation S002-E002: C = C_curv + C_comm decomposition, 41 negative eigenvalues, λ_max ratio 0.61–0.74, reference to new entry.

**New meta entries:**
- **Created** `meta/methodology/decompose-correction-into-psd-and-indefinite.md` — For matrix inequality analysis, decompose C into PSD + indefinite components; reveals mechanism and margins; includes 4-step protocol.

**Updated indexes:** factual root INDEX (294→295), factual/yang-mills/INDEX (22→23), meta root INDEX (37→38 methodology), meta/methodology/INDEX (37→38), CHANGELOG.

## 2026-03-29 (yang-mills-conjecture S002-exploration-007 + S002-meta-exploration-007)

### YM Conjecture: M(Q) ≠ Hessian structural distinction; UNRESOLVED potential counterexample (formula verification needed); Gershgorin/projection dead ends; meta: verify counterexample before investigating, define objects at MISSION level

**Updated factual entries:**
- **Updated** `factual/yang-mills/b-square-inequality-proof-progress.md` — Added M(Q) ≠ Hessian structural distinction: H(Q) = M(Q) − C(Q), C not PSD, O(1) eigenvalue discrepancy. Added UNRESOLVED potential counterexample section: S002-E007 gradient ascent found λ_max ≈ 16.08, but B_p formula (left multiplication) likely differs from verified adjoint formula (Ad_Q(v) = QvQ⁻¹) — flagged as unresolved, consistent with known "wrong formula → spurious violations" pattern. Added two new dead ends: Gershgorin (36+) and projection decomposition (equivalent to original problem).

**New meta entries:**
- **Created** `meta/methodology/verify-counterexample-before-investigating.md` — When finding a potential counterexample, FIRST verify it against the exact problem statement before investigating consequences; check representation/convention/normalization match.

**Updated meta entries:**
- **Updated** `meta/goal-design/verify-goal-claims-before-delegating.md` — Added "define key mathematical objects at MISSION level" variant: specify target operator with exact formula, not just by name. M(Q) vs Hessian distinction discovered in 7th exploration; should have been pinned down at MISSION level.

**Updated indexes:** factual root INDEX, factual/yang-mills/INDEX, meta root INDEX, meta/methodology/INDEX, meta/goal-design/INDEX, CHANGELOG.

## 2026-03-29 (yang-mills-conjecture S002-exploration-006 + S002-meta-exploration-006)

### YM Conjecture: Independent adversarial review confirms Gap 1 (CLOSED); momentum decomposition, L=3 eigenvalue formula, SZZ normalization convention; meta: structure-first adversarial sequencing

**Updated factual entries:**
- **Updated** `factual/yang-mills/cube-face-reduction-adversarial-review.md` — Added S002-E006 independent adversarial confirmation: momentum decomposition formula (eigenvalue = 4·(# of π-components) at Q=I), L=3 Q=I eigenvalue structure {0,3,6,9,12} with formula 4d·sin²(π/L) = 12, quantitative non-staggered vs staggered eigenvalue data (non-stag max 14.6, stag max 9.5, stag projection 0.19-0.48 for random Q). Gap 1 independently found and confirmed CLOSED.
- **Updated** `factual/yang-mills/b-square-inequality-proof-progress.md` — Added SZZ normalization convention note: SU(2) N=2 gives H_norm=4β (β < 1/4); SO(3) N=3 gives H_norm=8β/3 (β < 3/8). Convention ambiguity flagged for resolution against exact SZZ theorem statement.

**Updated meta entries:**
- **Updated** `meta/goal-design/adversarial-proof-review-structure.md` — Added "structure first, computation second" sequencing variant: check logical chain (proved ⇒ claimed?) before computational verification of individual steps. S002-E006 found all B1-B9 computationally correct but the structural gap was the critical finding.

**Updated indexes:** factual root INDEX, factual/yang-mills/INDEX, meta root INDEX, meta/goal-design/INDEX, CHANGELOG.

## 2026-03-29 (yang-mills-conjecture S002-exploration-005 + S002-meta-exploration-005)

### YM Conjecture: sum_S ≥ 0 PROVED (contraction bound), Gap 1 CLOSED, B_□ PROVED for even L; meta: affine structure check, don't prescribe tight-bound technique

**Updated factual entries:**
- **Updated** `factual/yang-mills/lemma-d-rdr-false-sum-s-nonneg.md` — MAJOR: **sum_S ≥ 0 PROVED** via contraction bound (M9 affine in D + per-pair Cauchy-Schwarz + combinatorial cancellation → F = 2Σf + Σ(||u||−||v||)² ≥ 0). Extends to all contractions ||D|| ≤ 1 (not just SO(3)). Tightness: F = 0 iff T on rotation axes. Full verification scorecard (25K random + adversarial, 0 violations). Polarization approach FAILS (37%/65% negative). Was: "full algebraic proof open."
- **Updated** `factual/yang-mills/b-square-inequality-proof-progress.md` — sum_S route (#5) upgraded from OPEN to PROVED; Gap 1 investigation section updated to CLOSED; Remaining Gap section updated (B_□ inequality PROVED for even L); Per-Component Lemmas section updated.
- **Updated** `factual/yang-mills/full-eigenspace-gap1-investigation.md` — Confidence upgraded to verified; overview updated (Gap 1 CLOSED by E005); proof strategy section replaced with resolution note.
- **Updated** `factual/yang-mills/cube-face-reduction-adversarial-review.md` — Gap 1 section updated from MODERATE to CLOSED; combined with cube-face reduction proves B_□ for even L.

**New meta entries:**
- **Created** `meta/methodology/check-affine-structure-before-bounding.md` — Before attempting bounds, check whether quantity is linear/affine in parameters; enables per-parameter independent minimization with closed-form bounds.

**Updated meta entries:**
- **Updated** `meta/goal-design/allow-explorer-synthesis.md` — Added "don't prescribe proof technique for tight bounds" variant: prescribed polarization failed; explorer succeeded by discovering affine structure.

**Updated indexes:** factual root INDEX, factual/yang-mills/INDEX, meta root INDEX, meta/methodology/INDEX, meta/goal-design/INDEX, CHANGELOG.

## 2026-03-29 (yang-mills-conjecture S002-exploration-004 + S002-meta-exploration-004)

### YM Conjecture: D=I base case PROVED, Critical T theorem PROVED, master identity, 7 dead ends; meta: special-case-proof generalization

**Updated factual entries:**
- **Updated** `factual/yang-mills/lemma-d-rdr-false-sum-s-nonneg.md` — Major update with E004 results: D=I base case PROVED algebraically (sum_S = 6Σf + |ΣR^T T|² ≥ 0), Critical T theorem PROVED (T on rotation axes: u=v → quadratic ≥ 0, most dangerous direction), master identity decomposition (baseline + bilinear correction), Delta_S factoring identity, E003 claim CORRECTED (sum_S(D=I) ≠ 0, actually ≥ 0 with min eig = 0), 7 dead-end approaches cataloged, adversarial evidence expanded from 200 to 67K. Full algebraic proof remains open.
- **Updated** `factual/yang-mills/b-square-inequality-proof-progress.md` — Updated sum_S proof route (#5) with Critical T theorem, master identity, and dead-end catalog; updated source.

**New meta entries:**
- **Created** `meta/methodology/special-case-proof-guides-generalization.md` — When a proof works for a special case, analyze WHY (the structural property that made it easy), then frame the general case as "restore that property + bound the deviation." From E004: on-axis proof works because u=v; deviation has same structure as baseline.

**Updated meta entries:**
- **Updated** `meta/methodology/verify-identity-generalization-before-extending.md` — Added "verify predecessor exploration claims" variant: E004 corrected E003's claim that sum_S(D=I) = 0 (actually ≥ 0); the correction enabled the master identity and Critical T theorem.

**Overwrites:**
- **Corrected** `factual/yang-mills/lemma-d-rdr-false-sum-s-nonneg.md` — E003 claimed "sum_S(D=I) = 0 for all R, T." E004 proved this FALSE; correct statement: sum_S(D=I) ≥ 0 with min eigenvalue = 0 (tight). Reason: E004 algebraic proof revealed two non-negative terms, the second (|Σ R^T T|²) is generically positive.

**Updated indexes:** factual root INDEX (description updated), factual/yang-mills/INDEX (description + entry updated), meta root INDEX (description updated), meta/methodology/INDEX (34→35, new entry + update)

## 2026-03-29 (yang-mills-conjecture S002-exploration-003 + S002-meta-exploration-003)

### YM Conjecture: LEMMA_D/LEMMA_RDR FALSE, sum_S ≥ 0 correct target; meta: adversarial for high-dim, tight-bound variant

**New factual entries:**
- **Created** `factual/yang-mills/lemma-d-rdr-false-sum-s-nonneg.md` — LEMMA_D and LEMMA_RDR individually FALSE (adversarial: -2.13 and -1.45; 200K random missed both). sum_S = LEMMA_D + LEMMA_RDR ≥ 0 is correct target (200 adversarial opts → 0). Zero-set: D=I for any R. VCBL at R=I; rank-3 obstruction for general R.

**Updated factual entries:**
- **Updated** `factual/yang-mills/b-square-inequality-proof-progress.md` — Added LEMMA_D/RDR failure under "What Failed" + sum_S interpolation as proof route #5; updated source.

**New meta entries:**
- **Created** `meta/methodology/budget-adversarial-for-high-dim.md` — Budget adversarial optimization from the start in ≥20D parameter spaces; random testing has poor coverage (200K samples missed counterexample in 30D).

**Updated meta entries:**
- **Updated** `meta/methodology/verify-identity-generalization-before-extending.md` — Added "verify conjectures adversarially before proving them" variant (LEMMA_D evidence); updated source.
- **Updated** `meta/methodology/consider-sdp-sos-for-constrained-proofs.md` — Added "tight bound" variant: when infimum = 0, loose inequalities (Cauchy-Schwarz, AM-GM) are ruled out; prefer SDP/SOS or exact algebraic decomposition.

**Updated indexes:** factual root INDEX (293→294, description updated), factual/yang-mills/INDEX (21→22, new entry + update), meta root INDEX (description updated), meta/methodology/INDEX (33→34, new entry + 2 updates)

## 2026-03-28 (yang-mills-conjecture exploration-008 + meta-exploration-008)

### YM Conjecture: Full 9D eigenspace bound (Gap 1) investigation; meta: identity generalization check, SDP/SOS for constrained proofs

**New factual entries:**
- **Created** `factual/yang-mills/full-eigenspace-gap1-investigation.md` — Full 9D eigenspace bound investigation (Gap 1 from cube-face reduction): per-vertex 12×12 reduction, 0 violations across 110K+ configs, gap decomposition (f_same + cross, harmful cross ≤ 8.2%), constraint essential, maximizer mixed-rank, algebraic proof open.

**Updated factual entries:**
- **Updated** `factual/yang-mills/b-square-inequality-proof-progress.md` — Added Gap 1 investigation section with cross-reference to new entry; updated source.
- **Updated** `factual/yang-mills/cube-face-reduction-adversarial-review.md` — Updated Gap 1 section with E008 investigation results and cross-reference.

**New meta entries:**
- **Created** `meta/methodology/verify-identity-generalization-before-extending.md` — Check key identities still hold before extending proof to larger space (trace identity failure for general patterns).
- **Created** `meta/methodology/consider-sdp-sos-for-constrained-proofs.md` — SDP/SOS formulations from the start for matrix-inequality proofs over constrained spaces.

**Updated meta entries:**
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — Added yang-mills-conjecture E008 as evidence (75+ min stall, 119 lines, needed nudge).

**Updated indexes:** factual root INDEX (292→293, description updated), factual/yang-mills/INDEX (20→21, new entry + updates), meta root INDEX (description updated), meta/methodology/INDEX (31→33, two new entries), meta/system-behavior/INDEX (description updated)

## 2026-03-28 (yang-mills-conjecture exploration-007 + meta-exploration-007)

### YM Conjecture: Cube-face reduction proof CONDITIONAL PASS; meta: check full logical chain, CONDITIONAL PASS verdict

**New factual entries:**
- **Created** `factual/yang-mills/cube-face-reduction-adversarial-review.md` — Adversarial review of 5-step cube-face reduction proof for Conjecture 1 (λ_max(M(Q)) ≤ 4d): CONDITIONAL PASS. Core algebra correct (13 VERIFIED, 5 COMPUTED). Two gaps: staggered mode ≠ full operator (9-dim top eigenspace: 3 staggered + 6 non-staggered), even-L only. Full M(Q) spectrum at identity {0,4,8,12,16}. Three paths to close Gap 1.

**Updated factual entries:**
- **Updated** `factual/yang-mills/b-square-inequality-proof-progress.md` — Added cube-face reduction proof section (cross-reference to new entry) and updated source.

**Updated meta entries:**
- **Updated** `meta/goal-design/adversarial-proof-review-structure.md` — Added "check full logical chain" variant (Step 5: verify reduction chain from proved statement to claimed conclusion; operator-vs-quadratic-form sub-lesson for matrix inequality proofs). Source updated.
- **Updated** `meta/goal-design/use-classification-schemes.md` — Added "Proof Review Verdicts (CONDITIONAL PASS)" variant: PASS / CONDITIONAL PASS / FAIL scale for proof reviews. Source updated.

**Updated indexes:** factual root INDEX (291→292, description updated), factual/yang-mills/INDEX (19→20, new entry listed), meta root INDEX (description updated, yang-mills-conjecture added to missions list), meta/goal-design INDEX (descriptions updated for both entries)

## 2026-03-28 (barandes-stochastic exploration-005 + meta-exploration-005)

### Barandes ISP: Tsirelson circularity CONFIRMED, steelman graded, Level 2→2+; meta: adversarial proof review structure

**New factual entries:**
- **Created** `factual/barandes-stochastic/steelman-and-level-3-paths.md` — Four steelman arguments graded (measurement problem SUBSTANTIVE, Lagrangian analogy APT BUT INCOMPLETE, open systems MOST PLAUSIBLE, causal locality PHILOSOPHICALLY STRONGEST); three Level 2→3 transition conditions (non-unistochastic proof, stochastic variational principle, operational channel result); none exist yet

**Updated factual entries:**
- **Updated** `factual/barandes-stochastic/chsh-tsirelson-causal-locality.md` — Circularity upgraded from "concern" to CONFIRMED; added detailed proof trace showing unistochastic = Born rule QM; added paper's own Section 5 acknowledgment; added prior art table (Tsirelson 1980, Buhrman-Massar 2005, Pawłowski 2009, NPA); added critical open question (non-unistochastic ISPs); added causal locality vs no-signaling confirmation. Source updated.
- **Updated** `factual/barandes-stochastic/physical-content-verdict.md` — Level 2 → Level 2+ refinement; added Level 2→3 transition conditions; cross-reference to steelman entry

**New meta entries:**
- **Created** `meta/goal-design/adversarial-proof-review-structure.md` — 4-step structure (trace proof, identify key assumption, check derived vs imported, check prior art); steelman requirement for likely-negative reviews; "does the paper acknowledge limitations?" variant

**Updated indexes:** factual root INDEX (290→291, description updated), factual/barandes-stochastic/INDEX (5→6, circularity confirmed, Level 2+), meta root INDEX (description updated), meta/goal-design INDEX (32→33)

## 2026-03-28 (barandes-stochastic exploration-004 + meta-exploration-004)

### Barandes ISP: Physical content assessment (Level 2 reformulation); meta: predecessor comparison for reformulations

**New factual entries:**
- **Created** `factual/barandes-stochastic/` folder with INDEX.md and 5 entries:
  - `chsh-tsirelson-causal-locality.md` — Causal local ISP -> Tsirelson bound (2sqrt(2)); strongest claim in Feb 2026 cluster; circularity concern noted
  - `complex-numbers-from-indivisibility.md` — Complex numbers needed for N>2 (Markovian embedding argument); pseudo-quaternion observation; prior art: Stueckelberg 1960
  - `physical-content-verdict.md` — Tests A/B/C (NEGATIVE/NEGATIVE/POSITIVE); amplituhedron comparison (significantly weaker); Level 2 reformulation verdict; pilot-wave/HMM minor finding
  - `fundamental-gaps-phase-erasure.md` — 4 fundamental gaps (entanglement, generators, QFT, superposition) from phase erasure
  - `feb-2026-paper-cluster.md` — 7 papers ranked: CHSH strongest, Deflationary Account moderate, Pilot-Wave minor, 2 critiques add nothing
- **Updated** `factual/gravitize-the-quantum/barandes-verlinde-stochastic-emergence.md` — Added cross-reference to new barandes-stochastic/ folder

**New meta entries:**
- **Created** `meta/goal-design/include-predecessor-comparison-for-reformulations.md` — Provide successful predecessor reformulation (e.g., amplituhedron) as structured comparison framework; "one paragraph answer" variant; "rank papers by importance" variant

**Updated meta entries:**
- **Updated** `meta/goal-design/require-gap-analysis-in-formal-mappings.md` — Added "require novel gaps not already identified in prior explorations" variant

**Updated indexes:** factual root INDEX (285->290, 19->20 categories), factual/barandes-stochastic/INDEX, factual/gravitize-the-quantum/barandes-verlinde entry, meta root INDEX, meta/goal-design INDEX (31->32)

## 2026-03-28 (yang-mills s003-exploration-006/007 + meta-exploration-s003-006)

### YM: Pure gauge isometry proof, abelian saturation, expanded P^T R P verification, structural properties; meta: gradient ascent on projection, multiple background scripts

**Updated factual entries:**
- **Updated** `factual/yang-mills/b-square-inequality-proof-progress.md` — Added pure gauge isometry proof (E006: M(Q)=Ad_G^T M(I) Ad_G, 15 configs verified to 4e-14), staggered mode single-link bound (E007: Δ=14(cosε−1)≤0 PROVED), expanded operator domination failure (E006: 50 configs across 8 classes, all violate), abelian saturation characterization (λ_max=4d iff fixed color direction — corrects "iff pure gauge"), SO(3)/triangle inequality approach (E007: gives 8(d-1), too weak), Schur/Haar average (E007: E[M]=2(d-1)I, average only), P^T R P expanded 20→42, structural properties section (trace conservation analytical proof, Tr(M²) decoherence, abelian block decomposition, Haar average). Source updated.
- **Updated** `factual/yang-mills/weitzenbock-exact-formula.md` — P^T R P verification count 20→42 configs, gradient ascent on P^T R P (stays at -8 to -11, 3 trials). Source updated.
- **Updated** `factual/yang-mills/hnorm-conjecture-numerical-resolution.md` — Added 95-config λ_max verification from E006 (including abelian configs, gradient ascent on λ_max). Source updated.

**New meta entries:**
- **Created** `meta/methodology/gradient-ascent-on-projected-quantity.md` — Run gradient ascent on projected matrix (P^T R P) not full matrix for subspace bound testing. Cheaper, tests correct target, shows cleaner margin.

**Updated meta entries:**
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — NEW "multiple simultaneous background scripts" caution: don't start two long-running background computations at once; causes 30+ min "Forming" stall.

**Updated indexes:** factual/yang-mills INDEX, factual root INDEX, meta root INDEX, meta/methodology INDEX (30→31), meta/system-behavior INDEX

## 2026-03-28 (yang-mills s003-exploration-005 + meta-exploration-005 + meta-exploration-s003-007)

### YM: Weitzenböck exact formula R(Q)|_P = −(1/12)W(Q); meta: verify goal claims, useful failure, proof sanity check, standard explorer computation

**New factual entries:**
- **Created** `factual/yang-mills/weitzenbock-exact-formula.md` — Exact formula max λ[R(Q)|_P] = −(1/12)W(Q) for single-link excitations (R²=1.000000); bound ≤ −W(Q)/12 for general Q (20/20 verified, random Q 1.7-2× tighter); −1/12 coefficient matches H_norm threshold; parallel transport decoherence mechanism; R(Q) globally mixed signs but R(Q)|_P always NSD; Jiang (2022) structural decomposition (no sign proof); SZZ non-usage confirmed; M(Q)=M(I)+R(Q) framework original.

**Updated factual entries:**
- **Updated** `factual/yang-mills/b-square-inequality-proof-progress.md` — Added Weitzenböck Exact Formula section (E005) with reference to new entry; updated Remaining Gap with 20/20 verification note; expanded Most Promising Proof Routes (Jiang F + SU(2) algebra as Avenue 1, spectral radius concavity as Avenue 2); added Forman (2003) reference; expanded Jiang reference with explicit formula details. Source updated.

**New meta entries:**
- **Created** `meta/goal-design/verify-goal-claims-before-delegating.md` — Verify cited prior results before writing GOAL.md; two-level fix (strategizer re-reads REPORT.md; GOAL.md includes numerical pre-screening). Evidence: two yang-mills s003 explorations wasted on false M(Q)≼M(I) goal.
- **Created** `meta/methodology/useful-failure-extracts-secondary-results.md` — Even when main goal fails, secondary results (algebraic invariants, special-case proofs, structural constants) are valuable. Evidence: yang-mills s003-E007 found B_□ B_□^T = 4I₃, Haar average, single-link analytical proof despite false main goal.

**Updated meta entries:**
- **Updated** `meta/methodology/include-trivial-control-checks.md` — NEW "numerical sanity check for proof targets" variant: compute the claim for 3-5 random configs before attempting to prove it. Evidence: yang-mills E007 could have caught false M(Q)≼M(I) in 5 lines.
- **Updated** `meta/system-behavior/computation-vs-reasoning-limits.md` — NEW "standard explorers can compute too" section: standard explorers can run Python eigenvalue computations (192×192 matrices, subspace projections, R²=1.000). Evidence: yang-mills s003-E005.

**Updated indexes:** factual/yang-mills INDEX (18→19), factual root INDEX (284→285), meta root INDEX, meta/goal-design INDEX (30→31), meta/methodology INDEX (29→30), meta/system-behavior INDEX

## 2026-03-28 (yang-mills strategy-003 explorations 001-004 + s003-meta-explorations 001-004)

### YM: B_□ inequality proof progress, per-plaquette inequality FALSE, L=4 confirmation, d=5 eigenvector; meta: characterize-maximizers, stalling variant, control checks, formula verification

**New factual entries:**
- **Created** `factual/yang-mills/b-square-inequality-proof-progress.md` — Comprehensive status of Σ|B_□|² ≤ 4d|v|² proof: B_□ formula correction (GOAL.md wrong for backward edges), partial proofs (uniform Q [PROVED], flat connections [PROVED], single-link [PROVED], Q=I local max [PROVED]), failed approaches (operator domination FALSE, geodesic concavity FAILS globally, Coulomb gauge blocked by Gribov, covariant Fourier equivalent), structural insights (B_□ B_□^T = 4I₃, cos(ε) suppression, Weitzenböck decomposition), remaining gap, key references (Jiang 2022, Liu-Peyerimhoff 2024).
- **Created** `factual/yang-mills/per-plaquette-inequality-false.md` — Per-plaquette bound H_P ≤ (β/2N)|B_P|² DEFINITIVELY FALSE for Q≠I: ratios up to 8383× per-plaquette, 1.936 global sum. B_P proof chain dead. Q=I equality is flat-vacuum coincidence.

**Updated factual entries:**
- **Updated** `factual/yang-mills/fourier-hessian-proof-q-identity.md` — Added S003-E004 analytical K_curl theorem (Fourier block-diagonalization → λ_max(K_curl) = 4d for all d, all L). Updated Open Conjecture A' with L=4 evidence, proof progress pointers, per-plaquette dead end. Source updated.
- **Updated** `factual/yang-mills/hnorm-conjecture-numerical-resolution.md` — Added L=4 confirmation (50+ configs including gradient adversarial search, zero violations). Corrected: directional staggered mode eigenvalue is 3β not 4β. Source updated.
- **Updated** `factual/yang-mills/eigenvalue-verification-d5-departure.md` — Added complete d=5 eigenvector characterization: v = (−1)^|x| × f(μ) with Σf=0 (zero-sum traceless); Mode C fails at odd d; general pattern λ_max=dβ for all d. Source updated.

**New meta entries:**
- **Created** `meta/goal-design/characterize-maximizers-not-just-bounds.md` — Frame goals as "characterize the maximizers" not just "is the bound tight"; structural characterization (F=4d ↔ pure gauge) was the most valuable finding.

**Updated meta entries:**
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — NEW "math-heavy standard explorer context exhaustion" variant: 70%+ context on long derivations → compaction → "queued messages" dead state; fix: kill and relaunch; preventive: nudge at 40% context.
- **Updated** `meta/methodology/include-trivial-control-checks.md` — NEW "Q=I sanity check for Hessian computations" variant: compute λ_max at Q=I and verify against analytical value before main scan.
- **Updated** `meta/goal-design/require-matrix-sanity-checks.md` — NEW "verify derived formulas against finite differences" variant: finite-difference check catches formula transcription errors invisible at Q=I.

**Updated indexes:** factual/yang-mills INDEX, factual root INDEX, meta root INDEX, meta/goal-design INDEX, meta/methodology INDEX, meta/system-behavior INDEX

## 2026-03-28 (riemann-hypothesis strategy-003 exploration-009 lambda-convergence + s003-meta-exploration-009)

### RH: Li-GUE crossover RESOLVED as truncation artifact; meta: write-during-long-computation, emergency nudge with numbers

**Updated factual entries:**
- **Updated** `factual/riemann-hypothesis/li-gue-comparison-super-rigidity.md` — MAJOR UPDATE: CRITICAL CAVEAT from E008 → **RESOLVED: TRUNCATION ARTIFACT** (E009). Added matched K=N convergence test data (500/1000/2000/3000/5000): ratio at n=500 monotonically increases 0.888→1.090, crossing 1.0 between K=2000-3000. Root cause: linear GUE scaling density mismatch (semicircle vs log-density). Novelty for comparison methodology remains 4/5; specific crossover claim RETRACTED. Verification Requirements → Verification Status (2 RESOLVED, 2 OPEN). Added full ratio table across all n. Source updated to include E009.
- **Updated** `factual/riemann-hypothesis/li-coefficients-verified-n500.md` — Added E009 multi-K confirmation note (monotonic growth at all n across K=500..5000, consistent with geometric convergence model). Source updated.

**Updated meta entries:**
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — NEW data point: context pressure at 33 min (E009, vs 52 min E008) for large-matrix computations; **key technique: pre-supply numerical results in emergency nudge** enables immediate summary writing without recomputation. Source updated.
- **Updated** `meta/goal-design/instruct-incremental-writing.md` — Eleventh confirmation: **write-during-long-computation variant** — for computations >15 min, submit as background job and write intermediate results first; decouples writing from computation to prevent context-pressure loss. Source updated.

**Updated indexes:** factual/riemann-hypothesis INDEX, factual root INDEX, meta root INDEX, meta/goal-design INDEX, meta/system-behavior INDEX

## 2026-03-28 (riemann-hypothesis strategy-003 exploration-008 lambda-truncation + s003-meta-exploration-008)

### RH: Li-GUE truncation validation; meta: scope computations, source data re-reading, Math Explorer context pressure

**Updated factual entries:**
- **Updated** `factual/riemann-hypothesis/li-gue-comparison-super-rigidity.md` — Major update: replaced 5-realization GUE table with 100-realization data (7.3σ at n=500); added Truncation Analysis section (λ_n NOT converged at 2000 zeros for n≥300, +6.1% at n=500 with 5k zeros); added N-dependence study (GUE λ_n scales linearly with N); added truncation artifact concern (crossover may approach 1 at larger K=N); updated verification requirements (matched K=N scaling test as priority). Added CRITICAL CAVEAT to finding summary. Source updated to include E008.
- **Updated** `factual/riemann-hypothesis/li-coefficients-verified-n500.md` — Added 5000-zero convergence section (slow convergence confirms r≈0.646 model but many zeros needed; positivity unaffected). Source updated.

**New meta entries:**
- **Created** `meta/goal-design/scope-computations-to-minimum-diagnostic.md` — Specify minimum computation path for intensive explorations; "compute ratio at K=N=500..5000" beats "validate with 5000 zeros"

**Updated meta entries:**
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — NEW "Context Pressure Emergency at 50+ Minutes (Math Explorer)" variant: 12.2k tokens at 52 min; shorten polling to 5 min for sessions >45 min
- **Updated** `meta/goal-design/preload-context-from-prior-work.md` — NEW "Re-Read Source Data, Not Strategizer Summaries" variant: have explorer load actual .npz data files, not rely on strategizer's (potentially wrong) summaries

**Updated indexes:** factual/riemann-hypothesis INDEX, factual root INDEX, meta root INDEX, meta/goal-design INDEX, meta/system-behavior INDEX

## 2026-03-28 (thermal-time strategy-003 exploration-003 distance-from-Gibbs + s003-meta-exploration-003)

### TTH distance-from-Gibbs characterization: relative entropy ≠ TTH discrepancy; spectrum preservation discriminant

- **Created** `factual/thermal-time/distance-from-gibbs-characterization.md` — 22-point survey: relative entropy does NOT determine TTH discrepancy; discriminant is spectrum preservation (unitary deformations → quantitative only; non-unitary → immediate structural failure); at comparable S_rel ~0.05, squeezed 0% vs quench ~140%
- **Updated** `factual/thermal-time/nonequilibrium-tth-post-quench.md` — Added cross-reference to distance-from-gibbs-characterization.md (extends single squeezed data point r=0.3 to 11-point systematic survey)
- **Updated** all INDEX.md files — thermal-time factual (9→10 findings), root factual (281→282)
- **No meta updates** — s003-meta-exploration-003 was already fully processed (all source fields already reference it); file deleted from inbox

## 2026-03-28 (thermal-time strategy-003 exploration-002 adversarial review + s003-meta-exploration-002)

### TTH adversarial claims assessment: novelty ratings, prior art, attack verdicts; meta: adversarial per-claim checkpoint, prior art discovery value

- **Created** `factual/thermal-time/tth-adversarial-claims-assessment.md` — Consolidated adversarial review of 5 TTH claims: novelty ratings (2.5/1/4/3/4), prior art for each (Cardy-Tonni 2016/2018, Takesaki IX.4.2, Lashkari-Liu-Rajagopal 2021), three conceptual attacks tested, null hypothesis assessments, claim priority ranking
- **Updated** `factual/thermal-time/nonequilibrium-tth-post-quench.md` — Added adversarial review section with novelty ratings and prior art references
- **Updated** `factual/thermal-time/excited-state-modular-flow.md` — Added adversarial review section (novelty 4/5, Lashkari-Liu-Rajagopal 2021 as closest prior art, attack verdicts), added verification status line
- **Updated** `meta/goal-design/instruct-incremental-writing.md` — 10th confirmation: adversarial per-claim checkpoint variant (write each claim's section after its prior art search, before moving to next claim)
- **Updated** `meta/goal-design/adversarial-synthesis-goal-structure.md` — Added "Prior Art Discovery as Primary Outcome" section (Lashkari-Liu-Rajagopal 2021 discovery was most important outcome of thermal-time adversarial review)
- **Updated** all INDEX.md files — thermal-time factual (8→9 findings), root factual (280→281), goal-design meta, root meta

## 2026-03-28 (riemann-hypothesis strategy-003 exploration-007 + s003-meta-exploration-007)

### RH: Li-GUE novelty confirmed, Berry formula artifact assessment; meta: deadline nudge, pre-settled claims, research-buffering nudge exception

**Updated factual entries:**
- **Updated** `factual/riemann-hypothesis/li-gue-comparison-super-rigidity.md` — Added Novelty Assessment section: 4/5 (literature-confirmed). Zero prior papers compare λ_n^zeta to λ_n^GUE. Searched Li (1997), Keiper (1992), Bombieri-Lagarias (1999), Schumayer-Hutchinson (2011). BL asymptotic provides growth rate but not the ratio. Added Verification Requirements section (≥10k zeros, larger GUE ensemble, mechanism cross-check, GUE dimension caveat at 17σ).
- **Updated** `factual/riemann-hypothesis/berry-formula-quantitative-test.md` — Added sparse-sampling artifact assessment for growing high-T error (0.2%→12.5%). Three hypotheses analyzed; sparse sampling at N=2000 is most likely. Novelty 1-2/5.

**Updated meta entries:**
- **Updated** `meta/goal-design/instruct-incremental-writing.md` — NEW "Literature Search Deadline Nudge with [INCOMPLETE] Markers" variant: add time-based writing trigger for web research explorations ("if searching >20 min without writing, STOP and write partial section with [INCOMPLETE]"). From RH s003-E007 (45-min stall broken by specific nudge).
- **Updated** `meta/goal-design/preload-context-from-prior-work.md` — NEW "Pre-Settle Resolved Claims" variant: record prior verdicts in goal to close off investigation paths. From RH s003-E007 (3 pre-settled claims freed explorer to focus on 2 live claims).
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — Research-buffering stall partial exception: highly specific nudges CAN work (RH s003-E007 — "STOP RESEARCHING" + format-specific follow-up produced 141 lines). Revised guidance: try specific nudge before killing. Planning assumption: first write after ~45 min for web research.

**Updated indexes:**
- All 5 INDEX.md files updated (factual/riemann-hypothesis, factual root, meta root, meta/goal-design, meta/system-behavior).

**Nuance conflict resolved:**
- `explorer-stalling-and-nudge-pattern.md`: existing "nudges don't fix research-buffering stalls" nuanced with partial exception. General assessment retained; conditions for exception documented.

## 2026-03-28 (riemann-hypothesis strategy-003 exploration-006 + s003-meta-exploration-006)

### RH: Super-rigidity mechanism, integral chain update; meta: analytical cross-check routes, normalization convention check

**New factual entries:**
- **Created** `factual/riemann-hypothesis/super-rigidity-mechanism-berry-formula.md` — Super-rigidity (Δ₃_sat ≈ 0.155 vs GUE 0.294) arises from saturation mechanism (K(τ) failing to sustain K=1 for τ>1), not from tau<1 differences. K_primes(cap) only 3.3% above GUE through integral transform. Berry's direct formula works; integral chain fails. Correct Berry weight: (log p)²/p^m.

**Updated factual entries:**
- **Updated** `factual/riemann-hypothesis/integral-chain-unreliable-n2000.md` — Added K(τ) → Σ₂ → Δ₃ as second unreliable integral route. Different failure mode: systematic ~2× normalization error from Fourier convention mismatch (vs R₂ route's 43% noise amplification). Relative comparisons remain valid.

**Updated meta entries:**
- **Updated** `meta/methodology/include-trivial-control-checks.md` — NEW "Analytical Cross-Check Route for Multi-Step Integral Chains" variant (include independent formula + GUE control with pass/fail threshold); NEW "Multiple Computation Variants for Relative Comparison" variant (nocap/cap/GUE design pattern).
- **Updated** `meta/goal-design/preload-context-from-prior-work.md` — Strengthened "Verify Formulas Before Preloading" with normalization convention check: always verify semiclassical weights against original paper (Berry weight missing 1/p^m factor caused K_primes to be ~183 instead of ~1).

**Updated indexes:**
- **Updated** all INDEX.md files — RH factual (23 → 24 findings), root factual (278 → 279), meta INDEX, methodology INDEX, goal-design INDEX.

## 2026-03-28 (thermal-time strategy-002 explorations 001-003 + s002-meta-exploration-001)

### Thermal Time: Rindler BW verification, non-equilibrium TTH, excited-state modular flow; meta: lattice convergence, Gaussian control, symmetry generator, parallel explorations, adversarial timing

**New factual entries:**
- **Created** `factual/thermal-time/rindler-bw-lattice-verification.md` — Lattice BW verification (N=50/100/200): BW profile 0.1% at d<=1.5 (lattice artifact beyond); modular-boost correlator converges at d=1.5; KMS exact to machine precision; Calabrese-Cardy entropy 1.5% match; modular flow = boost != time translation.
- **Created** `factual/thermal-time/nonequilibrium-tth-post-quench.md` — Non-equilibrium TTH: post-quench state 102% structural discrepancy (disjoint frequency content); modular time = pre-quench time; product-state identity (C_global = C_local for product states); squeezed state contrast (7.8% quantitative vs 102% structural); exact analytical formulas verified to 3e-13.
- **Created** `factual/thermal-time/excited-state-modular-flow.md` — One-particle excitation: modular flow at entanglement frequencies, physical frequency absent (amplitude ratio 0.0001); discrepancy GROWS ~N^{+0.33}; mode-0 convergence is IR artifact; Gaussian approximation caveat (PROVISIONAL).

**Updated factual indexes:**
- **Updated** `factual/thermal-time/INDEX.md` — Count 4 → 7; added 3 new entries; updated header.
- **Updated** `factual/INDEX.md` — Count 275 → 278; updated header and thermal-time entry description.

**New meta entries:**
- **Created** `meta/methodology/lattice-convergence-fixed-frequency.md` — Use fixed physical frequency (not fixed mode index) for lattice QFT convergence; multi-angle convergence reveals artifacts; E003 mode-0 fake convergence N^{-0.46} vs true divergence N^{+0.33}.
- **Created** `meta/goal-design/require-gaussian-control-for-non-gaussian-states.md` — For non-Gaussian states under Gaussian approximation, always request parallel Gaussian control computation (coherent state) to isolate approximation artifacts.

**Updated meta entries:**
- **Updated** `meta/methodology/parallel-math-explorer-explorations.md` — Broadened from math-explorer-only to general explorations; added thermal-time s002 evidence (3 Phase 1 probes in parallel); updated title in frontmatter.
- **Updated** `meta/goal-design/specify-rigor-level.md` — Broadened "Request Analytic Derivation of Power-Law Coefficient" to "Request Analytical Formulas Alongside Numerics"; added E002 evidence (exact closed-form correlators verified to 3e-13).
- **Updated** `meta/goal-design/specify-computation-parameters.md` — NEW "Specify Which Symmetry Generator" variant (QFT: boost vs translation vs rotation); NEW "Specify Williamson for Bosonic" variant; added source.
- **Updated** `meta/methodology/adversarial-check-between-phases.md` — Added thermal-time s002 confirmation (3 of 10 budget used, no adversarial, Gaussian caveat unflagged); updated source.

**Updated meta indexes:**
- **Updated** `meta/INDEX.md` — Updated header with thermal-time s002-meta-001 contributions.
- **Updated** `meta/goal-design/INDEX.md` — Count 27 → 28; added new entry; updated header.
- **Updated** `meta/methodology/INDEX.md` — Count 28 → 29; added new entry; updated header.

---

## 2026-03-28 (riemann-hypothesis strategy-003 exploration-005 + s003-meta-exploration-005)

### Riemann Hypothesis: Gauss Δ₃ rigidity hierarchy; meta: CWD drift fix

**New factual entries:**
- **Created** `factual/riemann-hypothesis/gauss-delta3-rigidity-hierarchy.md` — Gauss Δ₃ spectral rigidity computed for 6 primes (p=97 to 9973): Δ₃_sat ranges 0.415–0.559, all less rigid than random-phase N=500 ensembles (0.23–0.29). Complete rigidity hierarchy: zeta(0.155) < C1/GUE_N500(0.23–0.29) < Gauss-best(0.415) < GUE∞(0.581). β and Δ₃ decouple. Random phases produce stronger long-range correlations than arithmetic Gauss phases. Gauss pair correlation MRD (15–18%) worse than C1 (7.9%).

**Updated factual indexes:**
- **Updated** `factual/riemann-hypothesis/INDEX.md` — Count 22 → 23; added new entry; updated header with S003-E005 summary.
- **Updated** `factual/INDEX.md` — Count 274 → 275; updated header and RH entry with Gauss Δ₃ hierarchy.

**Updated meta entries:**
- **Updated** `meta/system-behavior/explorer-crashes-and-path-confusion.md` — NEW "CWD Drift During Computation" variant: explorer's working directory silently drifted from strategy-003/exploration-005 to strategy-002/exploration-005, executing entirely different task. Fix: add Task 0 "confirm working directory" (pwd + ls + expected path) to every GOAL.md.

**Updated meta indexes:**
- **Updated** `meta/INDEX.md` — Updated header with RH s003-meta-005 contribution.
- **Updated** `meta/system-behavior/INDEX.md` — Updated entry description and header with CWD drift variant.

---

## 2026-03-28 (riemann-hypothesis strategy-003 exploration-004 + s003-meta-exploration-004)

### Riemann Hypothesis: N²/p scaling universality REJECTED; meta: row-level writing, fitting method specification, trend tabulation, computation-buffering stall

**New factual entries:**
- **Created** `factual/riemann-hypothesis/n2p-scaling-universality-rejected.md` — N²/p ≈ 275 universal scaling hypothesis REJECTED by multi-N testing (N=250, 500, 1000). Peak N²/p_opt varies from 200 to 309 (1.5× range); peak β_max decreases with N (1.318→1.154→1.019); fitting method matters (Wigner vs Brody); weaker claim (Brody MLE peaks near N²/p≈290–310 for N≥500) partially supported; p≈N anomaly (β→0 at p≈N) documented.

**Updated factual entries:**
- **Updated** `factual/riemann-hypothesis/gauss-sum-phases-permanently-goe.md` — Resolved universality caveat: "TESTED AND REJECTED" replaces "premature — only N=500 tested." Points to new n2p-scaling-universality-rejected.md.
- **Updated** `factual/riemann-hypothesis/novelty-verdicts-synthesis.md` — Claim 1 verdict qualified from "SUPPORTED" to "SUPPORTED (N=500 observation); UNIVERSAL claim REJECTED." Detail section updated with S003-E004 multi-N results. Strategy 003 Q#2 marked as ANSWERED.

**Updated factual indexes:**
- **Updated** `factual/riemann-hypothesis/INDEX.md` — Count 21 → 22; added new entry; updated gauss-sum entry description; updated header.
- **Updated** `factual/INDEX.md` — Count 273 → 274; updated header and RH entry with S003-E004 summary.

**New meta entries:**
- **Created** `meta/methodology/require-trend-tabulation-for-negative-results.md` — Tabulate metric at each parameter value + test for monotone trend; makes negative results decisive ("β_max decreasing" vs "results vary").

**Updated meta entries:**
- **Updated** `meta/goal-design/instruct-incremental-writing.md` — Added 9th confirmation: E004 computation-buffering stall (results in tmux but not in REPORT.md); NEW row-level writing template for parameter sweeps.
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — Added E004 evidence to "Extended Between-Task Computation Stall" variant: computation-buffering detail (tmux showed results); specific prime list in nudge effective.
- **Updated** `meta/goal-design/specify-computation-parameters.md` — NEW "Specify Fitting Method When Comparing to Prior Explorations" variant: Wigner vs Brody gives different β by 0.1–0.2; always name the method.

**Updated meta indexes:**
- **Updated** `meta/INDEX.md` — Updated header with RH s003-meta-004 contributions (4 updates including 1 new methodology entry).
- **Updated** `meta/goal-design/INDEX.md` — Updated header with 2 entry updates.
- **Updated** `meta/methodology/INDEX.md` — Count 27 → 28; added new entry; updated header.
- **Updated** `meta/system-behavior/INDEX.md` — Updated header with E004 computation-buffering evidence.

---

## 2026-03-28 (riemann-hypothesis strategy-003 exploration-003 + s003-meta-exploration-003)

### Riemann Hypothesis: R₂→Δ₃ integral chain unreliability; meta: stalling variant, incremental writing, task prioritization, fallback methods

**New factual entries:**
- **Created** `factual/riemann-hypothesis/integral-chain-unreliable-n2000.md` — R₂ → Σ₂ → Δ₃ integral chain overestimates Δ₃_sat by 43% at N=2000 zeros (0.220 vs 0.155); root cause: R₂ statistical noise amplified through double integration + r_max=30 truncation; direct sliding-window method is reliable; K(τ) from R₂ Fourier transform qualitatively correct but quantitatively noisy with Gibbs artifact at τ=1; empirical R₂ anti-bunching at r=1 (0.92 vs GUE 1.00) consistent with super-rigidity

**Updated factual indexes:**
- **Updated** `factual/riemann-hypothesis/INDEX.md` — Count 20 → 21; added Computation Methods section with new entry; updated header description
- **Updated** `factual/INDEX.md` — Count 272 → 273; updated header and RH entry with S003-E003 integral chain unreliability

**Updated meta entries:**
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — Added "Extended Between-Task Computation Stall" variant: 3.5-hour stall between Tasks 1→2 in S003-E003; nudge with saved-data reference + task-skip instructions effective in 15 min; recommend 15-minute threshold for multi-task computation explorations
- **Updated** `meta/goal-design/instruct-incremental-writing.md` — Added 8th confirmation: S003-E003 wrote sections incrementally (positive example) but incremental writing doesn't prevent computation-initiation stall
- **Updated** `meta/goal-design/one-task-per-exploration.md` — Added "Mark Optional Tasks as Explicitly Skippable" corollary: S003-E003 had 5 tasks, explorer correctly skipped 2; goals should label required vs. optional tasks with priority template
- **Updated** `meta/goal-design/specify-failure-paths.md` — Added "Include Brute-Force Fallback Alongside Elegant Indirect Methods" variant: S003-E003 R₂→Δ₃ chain failed but direct sliding-window fallback succeeded; include both methods in goal

**Updated meta indexes:**
- **Updated** `meta/INDEX.md` — Updated header with RH s003-meta-003 contributions (4 updates)
- **Updated** `meta/goal-design/INDEX.md` — Updated header with 3 entry updates
- **Updated** `meta/system-behavior/INDEX.md` — Updated header with new stalling variant

---

## 2026-03-27 (riemann-hypothesis strategy-003 exploration-002 + s003-meta-exploration-002)

### Riemann Hypothesis: Li's criterion computation + phase cancellation + GUE comparison; meta: incremental writing + timeout

**New factual entries:**
- **Created** `factual/riemann-hypothesis/li-coefficients-verified-n500.md` — All 500 Li coefficients positive (n=1..500, 2000 zeros, 50-digit precision); truncation convergence ratio r ≈ 0.646 uniform across n; Coffey asymptotic 2.44× better than BL; no prime correlation (t = −1.33) or FFT structure
- **Created** `factual/riemann-hypothesis/li-phase-cancellation-structure.md` — |1−1/ρ| = 1 for critical-line zeros (verified by computation); Li series converges by phase cancellation not amplitude decay; λ_n = Σ 2(1 − cos(n·θ_k)); algebraically trivial but interpretively useful framing
- **Created** `factual/riemann-hypothesis/li-gue-comparison-super-rigidity.md` — 97.1% Coffey residual correlation between zeta and GUE Li coefficients; systematic divergence for large n (GUE overshoots, crossover n ≈ 300); super-rigidity (Δ₃ ≈ 0.16 vs GUE 0.31) → tighter phase cancellation; zeta residual 5× more variable than GUE

**Updated factual indexes:**
- **Updated** `factual/riemann-hypothesis/INDEX.md` — Count 17 → 20; added Li's Criterion section with 3 entries; updated header description
- **Updated** `factual/INDEX.md` — Count 269 → 272; updated RH description with S003-E002 Li's criterion summary

**Updated meta entries:**
- **Updated** `meta/goal-design/instruct-incremental-writing.md` — Added 7th Confirmation: [SECTION COMPLETE] markers insufficient for computation-heavy explorations; report stayed at 33 lines for 20 min despite fast computation; write-then-proceed temporal ordering is critical
- **Updated** `meta/goal-design/specify-computation-parameters.md` — Added "Variant: Specify Computation Timeout for Long Pre-Computations" (569s zero pre-computation barely fit in 10-min timeout; use 2× safety margin) and "Pre-compute shared data pattern" (compute once, save, iterate)

**Updated meta indexes:**
- **Updated** `meta/goal-design/INDEX.md` — Updated header with RH s003-meta-002 contributions
- **Updated** `meta/INDEX.md` — Updated header summary with RH s003-meta-002 contributions

---

## 2026-03-27 (thermal-time strategy-001 exploration-003 + meta-explorations 001-002-003 + conflict corrections)

### Thermal Time: E003 structural result, baseline correction to E002 finding, fabricated-entry removals

**New factual:**
- **Created** `factual/thermal-time/tth-full-qm-vs-local-tth.md` — direct C_full_QM vs. C_local_TTH; control check at machine zero; structural discrepancy (2-peak vs. 1-peak); 82.7% L² norm at λ=0.3; global TTH = QM (trivially); local TTH fails structurally

**Corrected factual:**
- **Corrected** `factual/thermal-time/tth-deltaK-and-period-shift.md` — "6.4% period shift vs. standard QM" was wrong baseline (was vs. C_free, should be vs. C_full). Against C_full: shift ~1.3% at λ=0.3. L² norm is better figure of merit. Reason: E003 established correct QM baseline is H_AB, not H_A.

**New meta (from actual meta-003):**
- **Created** `meta/methodology/include-trivial-control-checks.md` — include a trivial "should equal X by construction" check; thermal-time E003 control confirmed 83% discrepancy was physical
- **Created** `meta/methodology/structural-vs-quantitative-discrepancy.md` — diagnose type before investing in repair; structural (different signal topology) cannot be fixed by parameter tuning

**Updated meta (from actual meta-001/002 content, previously unprocessed):**
- **Updated** `meta/goal-design/one-task-per-exploration.md` — new "Separate Literature/Convention Questions from Computation" corollary
- **Updated** `meta/goal-design/specify-computation-parameters.md` — new "Specify Exact Comparison Baseline" variant: write full dynamics equations, not just "standard QM"
- **Updated** `meta/goal-design/specify-rigor-level.md` — new "Request Analytic Coefficient for Power-Law Corrections" variant
- **Updated** `meta/goal-design/specify-failure-paths.md` — new "Resolve Interpretation Ambiguity Before Computing Consequences" variant

**Conflict corrections (fabricated entries removed from prior run):**
- **Overwrote** `meta/goal-design/instruct-incremental-writing.md` — REMOVED fabricated "Sixth Confirmation" (thermal-time E001 nudge stall) and "Seventh Observation" (thermal-time E002 prevention). These were invented in the prior run; the actual meta-001/002 files do not mention write stalls. The legitimate subsequent observations from RH s002-meta-008 are preserved.
- **Overwrote** `meta/goal-design/prioritize-novelty-assessment.md` — REMOVED fabricated thermal-time meta-002 entry from "Embed Verdict on Novelty" variant. Actual meta-002 does not contain this lesson.

---

## 2026-03-27 (riemann-hypothesis strategy-002 exploration-009 + s002-meta-exploration-009)

### Riemann Hypothesis: Flat-amplitude test + C1 rigidity retraction; meta: finite-N sanity check, .npz saving, usage-limit recovery

**New factual entries:**
- **Created** `factual/riemann-hypothesis/von-mangoldt-amplitude-irrelevant-to-delta3.md` — H_flat (flat amplitude) ≈ C1 (Von Mangoldt) ≈ GUE control at N=500 (Δ₃_sat: 0.256, 0.243, 0.227; <1σ difference). Von Mangoldt amplitude does not cause spectral rigidity. Finite-size N=500 GUE Δ₃_sat = 0.23–0.26 (not infinite-N theory ~0.566). Formula bug: residuals-only formula underestimates Δ₃ by ~50×; correct formula = staircase integration. 40% gap to zeta zeros (0.155) confirmed and unresolved.

**Updated factual entries:**
- **Updated** `factual/riemann-hypothesis/c1-constraint-scorecard.md` — Added "E009 Update" section. Old claim: Δ₃_sat = 0.285 is "anomalous rigidity" (50% of GUE). Corrected: C1 Δ₃_sat = 0.243 ± 0.017 is generic finite-size GUE, indistinguishable from H_flat (0.256) at 1σ; Von Mangoldt amplitude irrelevant; prior comparison was against infinite-N theory. Constraint #7 reclassified from PARTIAL to NOT MEANINGFUL.
- **Updated** `factual/riemann-hypothesis/novelty-verdicts-synthesis.md` — C1 anomalous rigidity verdict changed from WEAK to NOT NOVEL (E009 retraction). Strategy 003 Q#1 marked ANSWERED (H_flat ≈ C1 within noise). Exploration count updated 17 → 18. Central open problem updated with E009 findings.

**Updated factual indexes:**
- **Updated** `factual/riemann-hypothesis/INDEX.md` — Count 16 → 17; updated header description to include E009; added von-mangoldt-amplitude-irrelevant-to-delta3.md entry; updated novelty-verdicts-synthesis description.
- **Updated** `factual/INDEX.md` — Count 265 → 266; updated riemann-hypothesis description to include flat-amplitude test result and C1 retraction.

**Updated meta entries:**
- **Updated** `meta/goal-design/require-matrix-sanity-checks.md` — Added "Variant: Verify Spectral Statistics Formula Against the Correct Finite-N GUE Range." Key: N=500 GUE Δ₃_sat ≈ 0.22–0.26 (NOT infinite-N theory ~0.566); ~2.3× difference; include GUE-control sanity check in every goal; explorers can self-diagnose formula bugs from expected-output context. C1 anomalous rigidity was infinite-N baseline artifact.
- **Updated** `meta/goal-design/specify-computation-parameters.md` — Added "Variant: Save Intermediate Results to .npz After Each Computation Block." Motivation: usage-limit deaths unrecoverable without saved files; template for per-block saves; companion instruction + strategizer recovery workflow.
- **Updated** `meta/system-behavior/explorer-crashes-and-path-confusion.md` — Added "Variant: Usage-Limit Death with Intermediate Files." Recovery workflow: check .npz/.pkl files immediately; load and write report manually; distinction from context-exhaustion crash.

**Updated meta indexes:**
- **Updated** `meta/goal-design/INDEX.md` — Added RH s002-meta-009 updates to header.
- **Updated** `meta/system-behavior/INDEX.md` — Added RH s002-meta-009 explorer-crashes update to header.
- **Updated** `meta/INDEX.md` — Added RH s002-meta-009 contributions to header summary; updated system-behavior section description.

---

## 2026-03-27 (SED strategy-003 explorations 001-002 + meta-exploration-s003-001)

### SED: physical-τ hydrogen data + Santos Moyal hierarchy + tunneling resolution

**Updated (adds significant new data):**
- **Updated** `factual/stochastic-electrodynamics/hydrogen-self-ionization.md` — added full physical-τ = 2.591×10⁻⁷ a.u. scan (7 L values, 140 trajectories; T_ion = 37,527×L^6.44; T_ion(L=1.0) = 19,223 periods ≈ 2.9 ps; ⟨r⟩(L=1.0) = 1.509 a₀ = QM ±0.6%); replaces the τ-extrapolation estimates that were the only prior reference.
- **Updated** `factual/stochastic-electrodynamics/sed-double-well-tunneling.md` — resolved open question: slope=1.049 is a finite-τ/ω_max simulation artifact (NOT an O(ħ²) effect); added analytic WKB action S=2√2/(3λ) (verified numerically); confirmed Faria-França slope=1.000 as exact algebraic identity, not an approximation.

**New:**
- **Created** `factual/stochastic-electrodynamics/sed-santos-moyal-hierarchy.md` — Santos (2022) Moyal bracket formalism + quantified ħ-expansion hierarchy (classical 0.183 < QM 0.258 < ALD 0.303 at β=1) + novel symmetry argument (O(ħ²) correction to ⟨x²⟩ is zero at O(β), explaining P&C's O(β²) onset).

**Meta:**
- **Updated** `meta/goal-design/specify-computation-parameters.md` — added "hierarchy-of-approximations" variant for theory/synthesis explorations
- **Updated** `meta/goal-design/allow-explorer-synthesis.md` — added "explain WHY this agrees" variant that elicits novel bonus derivations

## 2026-03-27 (thermal-time strategy-001 explorations 001-002 + meta-explorations 001-002)

### Thermal Time Hypothesis: new topic added to factual library

**New factual topic:**
- **Created** `factual/thermal-time/` folder — new top-level topic: Connes-Rovelli Thermal Time Hypothesis (TTH)
- **Created** `factual/thermal-time/modular-hamiltonian-catalog.md` — 4-system catalog (Rindler/BW theorem, Bell state, HO thermal, CFT interval/Casini-Huerta) with explicit K formulas and modular flow expressions
- **Created** `factual/thermal-time/tth-normalization-and-discriminating-observable.md` — normalization τ=β·t confirmed by BW + 3 papers; when TTH=QM (iff ρ_A is Gibbs); position autocorrelation as best discriminating observable
- **Created** `factual/thermal-time/tth-deltaK-and-period-shift.md` — ΔK_A ≠ 0 for λ≠0; O(λ²) with analytic proof; band-2 structure (β_eff renormalization + squeezing); period shift table (0% at λ=0 to 20.3% at λ=0.5); Δτ/τ ≈ 0.71λ²
- **Created** `factual/thermal-time/INDEX.md`

**Updated factual indexes:**
- **Updated** `factual/INDEX.md` — count 259→262; added Thermal Time Hypothesis section; updated description to include thermal-time

**New meta entry:**
- **Created** `meta/methodology/work-backward-from-constraint.md` — constructive exploration framing: "what satisfies this constraint?" produces definitive answers and unexpected no-go theorems; contrast with forward framing; evidence from thermal-time E002

**Updated meta entries:**
- **Updated** `meta/goal-design/instruct-incremental-writing.md` — sixth confirmation (thermal-time E001 reactive nudge); seventh partial observation (thermal-time E002 — prevention reduced but didn't eliminate batch write)
- **Updated** `meta/goal-design/use-classification-schemes.md` — added thermal-time E001 as third confirmation of Category Labels variant
- **Updated** `meta/goal-design/one-task-per-exploration.md` — added thermal-time E001 to "Trust Well-Scoped Comprehensive Survey" corollary
- **Updated** `meta/goal-design/allow-explorer-synthesis.md` — added two new evidence items (thermal-time E001 underexploited constraints; E002 no-go theorem); added "What Would Be a Breakthrough?" variant
- **Updated** `meta/goal-design/prioritize-novelty-assessment.md` — added thermal-time E002 to embed-verdict-on-novelty variant

**Updated meta indexes:**
- **Updated** `meta/goal-design/INDEX.md` — header updated; instruct-incremental-writing and allow-explorer-synthesis descriptions updated
- **Updated** `meta/methodology/INDEX.md` — count 23→24; added work-backward-from-constraint entry
- **Updated** `meta/INDEX.md` — added thermal-time mission; updated goal-design and methodology counts

---

## 2026-03-27 (yang-mills strategy-002 explorations-003 through 006 + meta-explorations-s002-003 through s002-006)

### Yang-Mills: CNS master loop ceiling, Hessian slack MAJOR FINDING, meta lessons

**New factual entries:**
- **Created** `factual/yang-mills/master-loop-optimized-ceiling.md` — CNS May 2025 Prop 3.23 exact analysis. Optimized ceiling β₀(4)_max = 1/(32e) ≈ 1/87 [DERIVED]. Parameters: λ=1/N optimal (proven), ρ=1/e required (proof necessity), γ=1 achievable ceiling. Gap to BE threshold = 4e/3 ≈ 3.6×. Critical correction: Remark 1.4 is about signed cancellations in merger term (NOT curvature). Curvature is structurally absent from master loop proof; quantitative impossibility for SU(2)/SU(3).
- **Created** `factual/yang-mills/szz-lemma-4-1-hessian-slack.md` — **MAJOR FINDING.** SZZ Lemma 4.1 Hessian bound is 12-170× loose. 3D: 12-45×. 4D: 29-138× (counter-intuitive: 4D tighter than 3D due to more plaquette cancellations). Adversarial search (gradient ascent, aligned configs, eigenvalue search): ≥176× slack. Mechanism: random-phase plaquette destructive interference. Implied threshold if proven analytically: β < 0.25-0.93 (12-45× improvement over 1/48).

**Updated factual entries:**
- **Updated** `factual/yang-mills/cao-nissim-sheffield-area-law-extension.md` — Major expansion: added Optimized Threshold section (β₀(4)_max = 1/(32e), parameter analysis), N-independence vs. β-range tradeoff table, Remark 1.4 critical correction (signed cancellations not curvature), expanded Open Questions including combination strategies A-D and Remark 1.4 path, updated Current State of the Field table with master loop optimized row.

**New meta entries:**
- **Created** `meta/methodology/verify-unexpected-findings-immediately.md` — When unexpected major finding emerges, design immediate stress-test exploration targeting most plausible failure mode. Include comparison table, treat outcome as decisive. Protocol, what to include, what NOT to do.

**Updated meta entries:**
- **Updated** `meta/goal-design/specify-rigor-level.md` — Added "Is X better than Y?" comparative question pattern; paper directly answers comparative questions in Remarks. Source updated.
- **Updated** `meta/goal-design/specify-computation-parameters.md` — Added "Specify Physical Dimension Separately from Lattice Geometry" variant (d=4 physics ≠ 4³ lattice); added "Include Both Typical-Config and Worst-Case Search for Bound Measurements" variant with template and three adversarial strategy recommendations. Source updated.
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — Added "Pre-Computation Coding Stall" variant: nudge must include (a) "code NOW", (b) output file path, (c) starting code file path. Source updated.
- **Updated** `meta/system-behavior/computation-vs-reasoning-limits.md` — Added formula optimization ~2 min floor (pure calculus); added 4D lattice ~3× slower than 3D dimension scaling guidance. Source updated.

---

## 2026-03-27 (riemann-hypothesis strategy-002 exploration-007 + s002-meta-exploration-007)

### Riemann Hypothesis: Adversarial review of C1 pair correlation claim

**Updated factual entries:**
- **Updated** `factual/riemann-hypothesis/c1-constraint-scorecard.md` — Added "Adversarial Review (S002-E007)" section. Key findings: (1) pair correlation ≤10% MRD is generic to all GUE-class matrices (GUE control: 7.8%, flat-amplitude: 6.8%, GOE-class Toeplitz: 9.0%); (2) per-realization C1 MRD mean = 15.5% ± 1.9%, 0/20 pass; (3) Von Mangoldt amplitude not necessary; (4) pair correlation PASS restated as SUPPORTED not ESTABLISHED. Source updated to include E007.

**New factual entries:**
- **Created** `factual/riemann-hypothesis/pair-correlation-discriminating-power.md` — The 10% MRD pair correlation test at N=500 with 5-realization averaging is insufficiently discriminating: cannot distinguish GOE from GUE. All GUE-class matrices pass; even GOE-class Toeplitz passes (9.0%). Meaningful discrimination requires N>2,000 or ≥20 realizations pooled.

**Updated factual indexes:**
- **Updated** `factual/riemann-hypothesis/INDEX.md` — Count 14 → 15; updated c1-constraint-scorecard description; added pair-correlation-discriminating-power.md entry.
- **Updated** `factual/INDEX.md` — Updated riemann-hypothesis summary to include adversarial review result.

**Updated meta entries:**
- **Updated** `meta/goal-design/instruct-incremental-writing.md` — Added "Fifth Confirmation" from RH s002-E007 (30-min thinking loop without writing in multi-test exploration); added section-specific checkpoint form ("after Test N, write Test N section before Test N+1"); added >15 min intervention threshold. Source updated.
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — Added RH s002-E007 evidence to Post-Computation Thinking Stall variant: stall can last ~30 min (extends prior ~10 min estimate); for multi-test explorations, use >15 min as intervention threshold. Source updated.

**Updated meta indexes:**
- **Updated** `meta/INDEX.md` — Added RH s002-meta-007 contributions to header summary; updated system-behavior section description.
- **Updated** `meta/goal-design/INDEX.md` — Updated instruct-incremental-writing description; updated header.
- **Updated** `meta/system-behavior/INDEX.md` — Updated entry description with 30-min stall duration and >15 min threshold.

---

## 2026-03-27 (riemann-hypothesis strategy-002 exploration-006 + s002-meta-exploration-006)

### Riemann Hypothesis: Berry diagonal approximation + Dirichlet character impossibility proof

**New factual entry:**
- **Created** `factual/riemann-hypothesis/prime-sum-form-factor-ramp.md` — Berry's diagonal approximation (prime sums) reproduces K(τ) ramp with MAD=14.5%; fails for τ>1 (plateau requires off-diagonal orbits). Resolves E003/E005 failures: cosine formula ≠ form factor; correct normalization is K_primes = K_density/(2πρ̄)².

**Updated factual entries:**
- **Updated** `factual/riemann-hypothesis/complex-phase-matrices-gue-approach.md` — Added "Extended Failure: Dirichlet Character Constructions (Algebraic Proof)" section: all Dirichlet character constructions (multiplicative χ(j)χ(k) route + factorizable χ(j)χ*(k) route) provably collapse to real symmetric matrices → permanently GOE. Numerical confirmation: β ≤ 0.281 for all tested constructions (χ₅, χ₁₃). Source updated to include E006.
- **Updated** `factual/riemann-hypothesis/riemann-operator-constraints.md` — Added nuance distinguishing two uses of primes: (1) prime corrections to zero positions → destroys level repulsion [prior finding, correct]; (2) Berry diagonal prime orbit formula → predicts K(τ) ramp with 14.5% accuracy [new E006 finding]. These are not contradictory — they measure different things. Source updated.

**Updated factual indexes:**
- **Updated** `factual/riemann-hypothesis/INDEX.md` — Count 13 → 14; added prime-sum-form-factor-ramp.md entry; updated complex-phase-matrices-gue-approach description (Dirichlet proof); updated riemann-operator-constraints description (Berry diagonal nuance).
- **Updated** `factual/INDEX.md` — Updated riemann-hypothesis summary to include Berry diagonal confirmation and Dirichlet impossibility proof.

**Updated meta entries:**
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — Added "Computation-Done-But-Still-Debugging Stall" variant: explorer has saved data file but stuck fixing scipy.optimize failure; direct nudge must name the file. Source updated.
- **Updated** `meta/goal-design/specify-computation-parameters.md` — Added two variants: (1) "Startup Diagnostics for Fragile Imports" — `python3 -c "import scipy.optimize"` check before computation, paired with explicit fallback formula; (2) "Specify Expected Output File Keys" — include exact .npz key names so explorer reads saved data, not re-computes. Source updated.
- **Updated** `meta/goal-design/specify-failure-paths.md` — Added "Request Structural Explanation When Construction May Fail" variant: ask "if the construction fails, determine if failure is empirical or structural; if structural, provide the proof" — elicits algebraic impossibility proofs that close entire construction classes. Source updated.

**Updated meta indexes:**
- **Updated** `meta/goal-design/INDEX.md` — Updated specify-computation-parameters and specify-failure-paths entries; updated header.
- **Updated** `meta/system-behavior/INDEX.md` — Updated explorer-stalling-and-nudge-pattern entry.
- **Updated** `meta/INDEX.md` — Updated header and section descriptions.

## 2026-03-27 (amplituhedron strategy-001, exploration-007 + meta-exploration-007)

### Amplituhedron: Surfaceology program survey + yang-mills-scattering-forms update

**Updated factual entry:**
- **Updated** `factual/amplituhedron/yang-mills-scattering-forms.md` — "Loop-level general ❌ UV divergences prohibit" framing clarified: this obstruction is specific to the *amplituhedron approach* (twistor space). Surface kinematics (arXiv:2408.11891, PRL 2025) resolved the canonical loop integrand for non-SUSY YM via a different geometric framework (kinematic space). Status table updated to show both approaches. Cross-reference to new surfaceology/surfaceology-yang-mills-integrand.md added.

**New factual subfolder:**
- **Created** `factual/amplituhedron/surfaceology/` — 5 new findings covering the surfaceology program (curves on surfaces for scattering amplitudes):
  - `surfaceology-framework-and-amplitude-formula.md` — Fatgraphs, u-variables, amplitude formula, first miracle
  - `surfaceology-amplituhedron-distinction.md` — Parallel frameworks (not nested); unification map
  - `surfaceology-yang-mills-integrand.md` — Scalar scaffolding, PRL 2025 canonical YM integrand
  - `surfaceology-new-results-2023-2026.md` — Cut equation, NLSM, Yukawa, strings, cosmohedra, Monte Carlo, inverse KLT
  - `surfaceology-open-problems.md` — Momentum-space bridge (central open problem) + field assessment

**Updated factual indexes:**
- **Updated** `factual/amplituhedron/INDEX.md` — 19 → 24 findings; added surfaceology/ subfolder section; updated yang-mills-scattering-forms description.
- **Updated** `factual/INDEX.md` — 251 → 256 findings; updated amplituhedron description to include surfaceology.

**Updated meta entries:**
- **Updated** `meta/methodology/standard-explorer-for-literature-surveys.md` — Added amplituhedron E007 evidence (466 lines, 15+ papers, ~15 min, 4th consecutive successful standard exploration; explorer independently identified critical parallel-not-nested distinction). Added E007 timing to timing reference table.
- **Updated** `meta/methodology/INDEX.md` — Noted E007 confirmation of standard-explorer pattern.
- **Updated** `meta/INDEX.md` — Header note updated with amplituhedron E007 contribution.

## 2026-03-27 (yang-mills strategy-002, explorations 001-002 + meta s002-001, s002-002)

### Yang-Mills: SZZ technique deep extraction + CNS area law extension + spectral gap numerics

**Overwrote/corrected existing factual entries:**
- **Corrected** `factual/yang-mills/chatterjee-probabilistic-program.md` — Item 6 (arXiv:2509.04688) was attributed to "Adhikari-Suzuki-Zhou-Zhuang" with description "Area law in 't Hooft limit". Corrected to "Cao-Nissim-Sheffield" with description "Area law at β < 1/24 via σ-model on vertices". Added CNS May 2025 (arXiv:2505.16585) to timeline. Reason: exploration-001 fetched the paper directly and identified the correct authors and result.
- **Updated** `factual/yang-mills/shen-zhu-zhu-stochastic-analysis.md` — Added exact K_S = N/2 − 8N(d-1)β formula with derivation; failure analysis at β = 1/48; five extension strategies; Chatterjee strong mass gap analysis; updated "Role in Area Law" section to remove wrong ASZT attribution and replace with correct CNS reference.

**New factual entries:**
- **Created** `factual/yang-mills/cao-nissim-sheffield-area-law-extension.md` — CNS Sept 2025 (β < 1/24 via vertex σ-model) + CNS May 2025 (N-independent via master loop equations); field state table; open questions.
- **Created** `factual/yang-mills/szz-spectral-gap-numerical-evidence.md` — MCMC spectral gap scan on 4^4 SU(2) lattice; γ > 0 throughout β ∈ [0.02, 3.0]; SZZ bound conservative by ~100×; τ_int peak = critical slowing down not gap closure.

**Updated indexes:**
- **Updated** `factual/yang-mills/INDEX.md` — 12 → 14 findings; added entries for both new files; expanded shen-zhu-zhu description.
- **Updated** `factual/INDEX.md` — 249 → 251 findings; updated yang-mills description.

## 2026-03-27 (riemann-hypothesis strategy-002, exploration-005 + s002-meta-exploration-005)

### Riemann Hypothesis: C1 constraint rescoring + Gauss prime sweep

**Overwrote factual entry:**
- **Overwrote** `factual/riemann-hypothesis/c1-constraint-scorecard.md` — Old scorecard (S002-E001): 4 PASS, 2 PARTIAL, 2 NOT COMPUTED, 2 N/A. New corrected scorecard (S002-E005): 3 PASS, 4 PARTIAL, 2 NOT COMPUTED, 1 N/A. Key changes: pair correlation upgraded NOT COMPUTED→PASS (normalization bug fixed, MRD=7.9%); Δ₃ upgraded NOT COMPUTED→PARTIAL (integral formula bug fixed, saturation=0.285≈50% GUE); β downgraded PASS→PARTIAL (5-realization average 1.18 vs prior single-realization outlier 1.675). Reason: S002-E005 recomputed all constraints with corrected code.

**Updated factual entries:**
- **Updated** `factual/riemann-hypothesis/complex-phase-matrices-gue-approach.md` — (1) Corrected C1 β note: 5-realization average gives 1.182 ± 0.219 (vs original S002-E001 estimate of 1.675 which was likely a high-realization outlier). (2) Added: Gauss sum GOE ceiling confirmed — β DECREASES for large p (non-monotone); β=0.086 at p=99991; optimal N²/p ≈ 250–310. (3) Updated Implications: Gauss sum direction ruled out; random-phase is the way forward. (4) Source updated to include S002-E005.

**New factual entry:**
- **Created** `factual/riemann-hypothesis/gauss-sum-phases-permanently-goe.md` — Gauss sum phases exp(2πi·jk/p) are permanently GOE-class; β→2 hypothesis REFUTED; max β=1.154 at p=809; non-monotone β vs p (decreases for large p); N²/p ≈ 250–310 optimal ratio; physical interpretation as chirp function; GUE structurally inaccessible.

**Updated factual indexes:**
- **Updated** `factual/riemann-hypothesis/INDEX.md` — 12 → 13 findings; updated descriptions for c1-constraint-scorecard.md and complex-phase-matrices-gue-approach.md; added gauss-sum-phases-permanently-goe.md entry.
- **Updated** `factual/INDEX.md` — updated riemann-hypothesis description (13 findings, added Gauss sweep refutation, corrected β range for random phases).

---

## 2026-03-27 (riemann-hypothesis strategy-002, exploration-004 + meta-exploration-004)

### Riemann Hypothesis: Berry formula quantitative test + meta lessons

**Updated factual entry:**
- **Updated** `factual/riemann-hypothesis/berry-saturation-confirmed.md` — Δ₃_sat value updated from 0.156 to 0.1550 ± 0.0008 (more precise measurement using integral formula, 300 windows per L value). Saturation onset for Δ₃ corrected to L≈10–12. Added formula note (Dyson-Mehta integral required; sum formula gives ~half). Added cross-reference to new berry-formula-quantitative-test.md. Source updated to include s002 exploration-004.

**New factual entry:**
- **Created** `factual/riemann-hypothesis/berry-formula-quantitative-test.md` — Berry's specific formula Δ₃_sat = (1/π²)·log(log(T/2π)) confirmed to 7.6% overall, 0.2% for low-T bin (T_geo=383). Three alternative formula variants fail by 2.5–3.4×. Height-resolved analysis: Δ₃_sat = 0.1435→0.1545→0.1569→0.1595 (strictly monotone). Critical: Dyson-Mehta integral formula is correct; sum formula gives ~half the value (resolves Δ₃ bug from c1-constraint-scorecard.md).

**Updated factual indexes:**
- **Updated** `factual/riemann-hypothesis/INDEX.md` — 11 → 12 findings; updated berry-saturation-confirmed.md description; added berry-formula-quantitative-test.md entry.
- **Updated** `factual/INDEX.md` — 248 → 249 findings; updated riemann-hypothesis description.

**Updated meta entries:**
- **Updated** `meta/goal-design/specify-computation-parameters.md` — (1) Extended "Provide Exact Implementation Formula" variant: also provide a known numerical value as second anchor (s002 E004 evidence). (2) Added new variant: "Build Formula Disambiguation Into the Goal When Implementations Disagree." (3) Added new variant: "Specify Parameter Bins for Testing Scaling Predictions." Updated "When to apply" section.
- **Updated** `meta/goal-design/specify-failure-paths.md` — Added new variant: "Give Explicit Skip Permission for Ambiguous Sub-Tasks" (silent omission prevention).
- **Updated** `meta/goal-design/INDEX.md` — Updated entry descriptions; noted new variants added.
- **Updated** `meta/INDEX.md` — Updated header to note RH s002 E004 contributions.

## 2026-03-27 (amplituhedron strategy-001, exploration-004)

### Amplituhedron: Locality/unitarity emergence, physical assessment, EFT-hedron, hidden zeros

**New factual entries:**
- **Created** `factual/amplituhedron/locality-unitarity-emergence-mechanism.md` — Precise mechanism of locality/unitarity emergence: canonical form has log singularities only on boundaries (= physical poles); unitarity = boundary factorization proved all n,L,k (JHEP 2020) + ABJM (2023); binary code / sign-flip perspective; concrete 4-pt example; planarity derived not assumed; deformed amplituhedron (relaxed positivity) gains non-local poles; UV finiteness connection.
- **Created** `factual/amplituhedron/bcfw-triangulation-proof-2025.md` — Even-Zohar, Lakrec, Tessler, Inventiones Math. 239(2025)1009-1138; BCFW cells tile amplituhedron exactly (injectivity + surjectivity via topological argument); amplituhedron homeomorphic to open ball; spurious poles cancel via opposite orientation on internal boundaries; 12-year gap from conjecture (2013) to proof.
- **Created** `factual/amplituhedron/eft-hedron-positivity-constraints.md` — Arkani-Hamed, T.-C. Huang, Y.-T. Huang JHEP 2021; real-world bounds on Wilson coefficients; amplitude growth > E^6 → not UV-completable; photon-photon and graviton EFT bounds; upper bound on new physics mass; most practically relevant output of the positive geometry program.
- **Created** `factual/amplituhedron/hidden-zeros-inter-theory-structure.md` — arXiv:2312.16282 JHEP 2024: ϕ³/pions/gluons share hidden zeros + kinematic-shift structure; ABHY associahedron collapses at zero kinematics; 2025 extension (arXiv:2503.03805): one-loop Tr(φ³) integrand fixed by hidden zeros, locality/unitarity emerge in non-SUSY theory.
- **Created** `factual/amplituhedron/amplituhedron-physical-assessment.md` — Honest physical status: identical predictions to Feynman for N=4 SYM; 3 genuine contributions; 12-claim assessment table (ESTABLISHED/SUPPORTED/SPECULATIVE/REFUTED); comparison table of emergent locality programs vs. string theory, NCG, causal sets.

**Updates to existing factual entries:**
- **Updated** `factual/amplituhedron/INDEX.md` — 13 → 18 findings; added 5 new entries with descriptions; updated header.
- **Updated** `factual/INDEX.md` — 237 → 247 findings (237 + 5 amplituhedron + 5 RH from concurrent update); updated amplituhedron description.

**New meta entries (no new files — updates to existing):**
- **Updated** `meta/goal-design/use-classification-schemes.md` — Added amplituhedron E004 evidence to "Explicit Honesty Language" variant; added new "Claim Evaluation Tables" variant (Claim | Evidence For | Evidence Against | Status format).
- **Updated** `meta/methodology/standard-explorer-for-literature-surveys.md` — Added amplituhedron E004 evidence: standard explorer handles multi-part analysis (not just surveys); 362 lines, 16 papers, ~25 min.
- **Updated** `meta/goal-design/allow-explorer-synthesis.md` — Added amplituhedron E004 evidence: synthesis separating genuine contributions from reformulation was the most valuable output.
- **Updated** `meta/goal-design/INDEX.md` — noted new updates to use-classification-schemes and allow-explorer-synthesis.
- **Updated** `meta/methodology/INDEX.md` — noted update to standard-explorer-for-literature-surveys.
- **Updated** `meta/INDEX.md` — noted amplituhedron E004 contributions.

## 2026-03-27 (riemann-hypothesis strategy-002, exploration-001)

### Riemann Hypothesis: Complex-phase matrix screening + index repair

**New factual entries:**
- **Created** `factual/riemann-hypothesis/complex-phase-matrices-gue-approach.md` — C1 (random phases) achieves β=1.675 ± 0.085 (GUE-class, primary success criterion β>1.5 met); C3b (Gauss p=997) achieves β=1.092 (GOE); C2 fails (odd Dirichlet characters → antisymmetric → zero matrix); C4 fails (Toeplitz zeta phases → Poisson). Non-factorizability principle: phase φ(j,k) must depend jointly on j,k to break time-reversal symmetry.
- **Created** `factual/riemann-hypothesis/c1-constraint-scorecard.md` — 10-constraint RMT evaluation of C1: 4 PASS, 2 PARTIAL, 2 NOT COMPUTED (pair correlation normalization bug, Δ₃ formula bug), 2 N/A; detailed tables for number variance and form factor.

**Updated factual entries:**
- **Updated** `factual/riemann-hypothesis/arithmetic-matrix-operators-poisson-failure.md` — Added forward reference: prediction of complex-phase extension confirmed; pointer to complex-phase-matrices-gue-approach.md and c1-constraint-scorecard.md.
- **Updated** `factual/riemann-hypothesis/INDEX.md` — Added 5 files (3 previously missing: individual-zero-reconstruction-impossible, prime-corrections-statistical-partial-success, trace-formula-gibbs-phenomenon; 2 new: complex-phase-matrices-gue-approach, c1-constraint-scorecard); count updated 6 → 11.
- **Updated** `factual/INDEX.md` — Updated riemann-hypothesis description to include trace formula findings and complex-phase results; count unchanged at 242 (already correct after prior session).

**New meta entries:**
- **Created** `meta/goal-design/require-matrix-sanity-checks.md` — Require pre-analysis sanity checks in matrix construction goals; from C2 construction failure (odd characters → zero matrix → meaningless stats).

**Updated meta entries:**
- **Updated** `meta/goal-design/specify-computation-parameters.md` — Added variant: provide exact implementation formula for normalization-sensitive statistics (pair correlation R₂, spectral rigidity Δ₃); from two bug failures in s002 E001.
- **Updated** `meta/goal-design/specify-failure-paths.md` — Extended domain-constraints variant: added non-factorizability constraint for complex matrix GUE goals (factorizable phases g(j)−g(k) are unitarily equivalent to real symmetric matrices, also capped at β≤1).
- **Updated** `meta/methodology/multi-ansatz-sweep-pattern.md` — Added s002 E001 as third evidence item: 7-construction sweep with clear β>1.5 threshold; note on sanity-check limitation.
- **Updated** `meta/goal-design/INDEX.md` — 24 → 25 entries.
- **Updated** `meta/INDEX.md` — Updated goal-design count and description.

## 2026-03-27 (compton-unruh strategy-001, explorations 007-008)

### Compton-Unruh: free-fall resolution + adversarial stress test

**OVERWRITES / Conflict resolution:**
- **Rewrote** `factual/compton-unruh/free-fall-objection-analysis.md` — Old claim: "de Sitter geodesic deviation approach is potentially valid but unproven; Jacobson 1995 is NOT a resolution for T_U/T_dS." New finding (COMPUTED E007): de Sitter-relative acceleration = g_N exactly (Λ cancels — proven by Sympy + 3 numerical test cases to machine precision); Jacobson local Rindler IS a valid equivalent resolution (κ_local = g_N by definition of surface gravity); both give identical formula. Free-fall objection RESOLVED. Confidence upgraded from provisional → verified. Reason: E007 provided the missing computation.
- **Updated** `factual/compton-unruh/tu-tds-mond-identity.md` — "Updates from Later Explorations" section: changed "de Sitter-relative approach potentially valid but not yet rigorously derived (E005)" → "free-fall objection RESOLVED (E007) via de Sitter-relative acceleration and Jacobson local Rindler."

**New factual entries:**
- **Created** `factual/compton-unruh/factor-of-2pi-obstruction.md` — Four independent approaches to deriving 1/(2π) from T_U/T_dS all fail (algebraically inevitable — 2π cancels in ratio); must import from Verlinde's area-volume entropy competition; genuine gap.
- **Created** `factual/compton-unruh/modified-inertia-lensing-falsification.md` — Bullet Cluster: 5.7× amplitude deficit + wrong morphology (lensing at stars, predicted at gas). General cluster lensing: 5–10× mass deficit. Intrinsic to modified inertia (Poisson equation unchanged). Decisive observational falsification.
- **Created** `factual/compton-unruh/tu-tds-acceleration-ambiguity.md` — Three cases for which "a" enters μ: Case A (proper) → m_i = 0 for free fall; Case B (centripetal) → correct rotation curves; Case C (g_N, formula notation) → v ∝ √r (wrong). Rotation curve fits used Case B; GOAL.md implies Case C. Internal inconsistency undetected for 7 explorations.
- **Created** `factual/compton-unruh/tu-tds-cosmological-failure.md` — Evolving a₀ catastrophic (BBN + CMB in deep MOND). Fixed a₀: CMB 3rd peak wrong by 2× (no CDM). No mechanism to freeze a₀.
- **Created** `factual/compton-unruh/tu-tds-momentum-non-conservation.md` — No action principle → momentum not conserved. Spurious impulse ~10⁶³ kg·m/s over merger timescale. Cannot embed in QFT.
- **Created** `factual/compton-unruh/tu-tds-viability-scorecard.md` — 14-criterion adversarial scorecard: 3.6/10 average. Observationally falsified by lensing. Genuine: T_U/T_dS = μ_MOND identity, solar system, WEP, H₀–a₀ connection.

**Updates to existing factual entries:**
- **Updated** `factual/compton-unruh/galaxy-rotation-curve-fits.md` — Added E007 NGC 3198 re-analysis: corrected v_flat = 150 km/s (not 120 km/s); best-fit a₀ = 1.175×10⁻¹⁰ m/s² (within 2% of MOND); cH₀/(2π) indistinguishable from MOND (χ²/dof ratio = 1.02).
- **Updated** `factual/compton-unruh/INDEX.md` — 15 → 21 findings; added 6 new entries; updated descriptions for free-fall, tu-tds-identity, galaxy fits.
- **Updated** `factual/INDEX.md` — 231 → 237 findings; updated compton-unruh description.

**New meta entries:**
- **Created** `meta/methodology/check-algebra-before-multi-approach.md` — Pre-screen for algebraic inevitability (factor cancellation in ratios) before committing to multiple exploration approaches; from E007 where 4 approaches to restore 1/(2π) all failed predictably.
- **Created** `meta/goal-design/specify-modified-inertia-vs-gravity.md` — Require modified-dynamics explorations to specify inertia vs. gravity upfront; decisive for lensing predictions; failure to specify costs 5–7 explorations before fatal test is run.

**Updates to existing meta entries:**
- **Updated** `meta/methodology/adversarial-check-between-phases.md` — Added E008 upgrade: run full standard-test adversarial exploration early (not just lightweight novelty check); Bullet Cluster objection is a canonical test for modified gravity/inertia that should have been run at E003–E004.
- **Updated** `meta/methodology/INDEX.md` — 18 → 19 entries; added check-algebra-before-multi-approach; updated adversarial-check-between-phases description.
- **Updated** `meta/goal-design/INDEX.md` — 23 → 24 entries; added specify-modified-inertia-vs-gravity.
- **Updated** `meta/INDEX.md` — Updated goal-design (23→24) and methodology (18→19) counts; added new entries to descriptions.

## 2026-03-27 (stochastic-electrodynamics strategy-001, explorations 005-006)

### SED: UV-cutoff parameter scan + adversarial novelty review

**OVERWRITE / Conflict resolution:**
- **Corrected** `factual/stochastic-electrodynamics/anharmonic-ald-landau-lifshitz.md` — "Residual Failure at β > 0.2: UV Cutoff Conjecture [CONJECTURED]" section replaced with confirmed E005 findings. Old claim: "Most likely explanation: the finite UV cutoff ω_max=10 creates an imperfect FDT balance... Testing with ω_max=20 would confirm or refute this." New finding (COMPUTED): Tripling ω_max reduces Δe by only 18% (p≈0.18 vs expected p≥1 for UV artifact); quintupling 1/τ reduces Δe by only 31% (τ^0.23 vs P&C τ^1); **UV cutoff hypothesis REFUTED**. P&C regime requires τ<10^-4, ω_max>10^6. Reason: E005 directly tested ω_max∈{10,20,30} and τ∈{0.01,0.005,0.002}.

**New factual entries:**
- **Created** `factual/stochastic-electrodynamics/uv-cutoff-parameter-scan.md` — E005 ω_max and τ parameter scans; β^0.40 NOT a UV artifact; Δe ~ τ^0.23 × ω_max^(-0.18); convergence extrapolation; dt stability issue (dt=π/ω_max causes runaway).
- **Created** `factual/stochastic-electrodynamics/sed-novelty-assessment.md` — E006 adversarial review; finding-by-finding novelty/robustness verdicts; F3 = lead finding; F4 (linearity boundary) NOT novel (Boyer 1975/2019); significance correction at β=0.01; Moore & Ramirez (1981) found; full bibliography.

**Updates to existing factual entries:**
- **Updated** `factual/stochastic-electrodynamics/anharmonic-ald-landau-lifshitz.md` — Implications and Future Work sections updated to reflect E005 confirmation.
- **Updated** `factual/stochastic-electrodynamics/anharmonic-oscillator-failure.md` — Added significance correction note (5.4σ absolute → ~2.5σ for O(β) trend at β=0.01).
- **Updated** `factual/stochastic-electrodynamics/linearity-boundary-pattern.md` — Added Novelty Assessment section: concept known since Boyer 1975/2019, NOT novel.
- **Updated** `factual/stochastic-electrodynamics/anharmonic-langevin-o-beta-failure.md` — Added Framing Note: "approximation failure, NOT a SED fundamental failure."
- **Updated** `factual/stochastic-electrodynamics/INDEX.md` — 12 → 14 findings; updated ALD entry description; added 2 new entries.
- **Updated** `factual/INDEX.md` — 229 → 231 findings; updated SED description.

**New meta entries:**
- **Created** `meta/goal-design/separate-numerical-from-physics-parameters.md` — Fix numerical method parameters (dt) separately from physics parameters (ω_max) in scan goals; co-variation causes instability and confounding.
- **Created** `meta/methodology/adversarial-check-between-phases.md` — Lightweight adversarial check between Phase 2 and Phase 3; early reframing on novelty/approximation-artifacts is more valuable than late correction.
- **Created** `meta/goal-design/require-baseline-adjusted-significance.md` — Require baseline-adjusted (trend) significance alongside raw (absolute) significance for parameter-dependent measurements.

**Updates to existing meta entries:**
- **Updated** `meta/methodology/adversarial-explorations-need-null-hypothesis.md` — Added SED E006 evidence: "findings are known or wrong" framing caused genuine downgrade of F4 from novel to known.
- **Updated** `meta/goal-design/INDEX.md` — 20 → 22 entries.
- **Updated** `meta/methodology/INDEX.md` — 17 → 18 entries.
- **Updated** `meta/INDEX.md` — counts updated.

---

## 2026-03-27 (classicality-budget strategy-002, explorations 003-004)

### Classicality budget: experimental regime survey + ion trap protocol + island formula page curve

**New factual entries:**
- **Created** `factual/classicality-budget/experimental-testable-systems-survey.md` — 8-system R_max survey using actual thermodynamic entropy; 3 TIGHT systems; inflation Hubble patch as BH analog.
- **Created** `factual/classicality-budget/ion-trap-classicality-transition-protocol.md` — Ion trap phase transition at n̄_c ≈ 0.003; experimental protocol; feasibility assessment.
- **Created** `factual/classicality-budget/island-formula-page-curve-classicality.md` — Quantitative R_δ(t) via island formula; two-stage classicality structure; novelty verdict = HQEC restatement.

**Conflict/correction:**
- **Upgraded** `factual/classicality-budget/holographic-classicality-budget.md` (INDEX reference) — E007 conjectured "R_collective just barely ≥ 1 after Page time." E004 computed the actual jump: R_δ_int → S_BH/2 − 1 ≈ 5×10^76 for solar mass BH. New file captures the quantitative result; INDEX cross-reference updated.

**Updated meta entries (new variants added):**
- **Updated** `meta/goal-design/specify-computation-parameters.md` — Added variants: Python code templates as strongest parameter specification; threshold-finding scanning questions.
- **Updated** `meta/goal-design/specify-failure-paths.md` — Added variant: "No-go argument counts as success" framing for experimental prediction goals.
- **Updated** `meta/goal-design/prioritize-novelty-assessment.md` — Added variant: Embed "verdict on novelty" as mandatory section in any mathematical exploration goal.

## 2026-03-27

### SED: ALD/Landau-Lifshitz anharmonic oscillator result (E004, stochastic-electrodynamics strategy-001)

**New entries:**
- **Created** `factual/stochastic-electrodynamics/anharmonic-ald-landau-lifshitz.md` — ALD with LL order reduction eliminates O(β) Langevin failure for β ≤ 0.1; full 3-way comparison table; β^0.40 residual; physical mechanism (Γ_eff table); sign correctness.
- **Created** `meta/methodology/investigate-why-on-discrepancies.md` — When results disagree with predictions, investigate the WHY; the explanation is often the main finding.

**Updates:**
- **Updated** `factual/stochastic-electrodynamics/anharmonic-oscillator-failure.md` — Added UPDATE note in Significance section pointing to ALD fix.
- **Updated** `factual/stochastic-electrodynamics/anharmonic-langevin-o-beta-failure.md` — Added UPDATE note in Context section noting ALD eliminates the O(β) failure.
- **Updated** `factual/stochastic-electrodynamics/linearity-boundary-pattern.md` — Updated anharmonic oscillator scorecard row; updated Open Computations entry to reflect E004 ALD result.
- **Updated** `factual/stochastic-electrodynamics/INDEX.md` — 11 → 12 findings; added anharmonic-ald-landau-lifshitz.md entry.
- **Updated** `factual/INDEX.md` — 224 → 225 findings; updated SED description with ALD/LL fix note.
- **Updated** `meta/goal-design/preload-context-from-prior-work.md` — Added "Variant: Pre-Loading Specific Formulas and Numerical Values" with SED E004 evidence (36 min → 14 min).
- **Updated** `meta/methodology/INDEX.md` — 16 → 17 entries.
- **Updated** `meta/goal-design/INDEX.md` — noted preload update.
- **Updated** `meta/INDEX.md` — methodology count 16 → 17.

### Classicality Budget: BH Horizon Implications + Holographic Reformulation (E006–007, classicality-budget strategy-001)

**Overwrites / Corrections:**
- **Corrected** `factual/classicality-budget/blackhole-hawking-classicality-impossible.md` —
  "Contrast with Planck-Mass BH" section contained an incorrect conjecture: "At the Planck mass,
  the Hawking photon wavelength becomes comparable to the Schwarzschild radius. Photons fit in the
  near-horizon volume. The Hawking environment might have significant entropy at Planck scale."
  This is FALSE. E006 proves T_H × r_s = ℏc/(4πk_B) is universal, so λ_Hawking = 4π r_s ALWAYS,
  meaning the photon is 12.57× larger than r_s at ALL masses including Planck. S_Hawking = 1/(540 ln2)
  at Planck mass, identical to any other mass. Corrected to state this explicitly and mark the
  old conjecture as disproved.
- Also updated Core Result in same file to explicitly state the mass-independence (was implicitly
  solar-mass only before; is now stated as universal).

**Major additions:**
- **Created** `factual/classicality-budget/blackhole-universal-constants.md`
- **Created** `factual/classicality-budget/holographic-classicality-budget.md`
- **Created** `factual/classicality-budget/qd-hqec-mapping.md`
- **Updated** `factual/classicality-budget/adversarial-objections-assessment.md` — added UPDATE note
  to Objection 4 (catch-22) that the structural component is PARTIALLY RESOLVED by E007
- **Updated** `factual/classicality-budget/INDEX.md` — 8 → 11 findings
- **Updated** `factual/INDEX.md` — 211 → 214 findings

**Meta additions:**
- **Created** `meta/goal-design/provide-specific-tools-for-reformulation.md`
- **Created** `meta/methodology/dual-mechanism-robustness.md`
- **Updated** `meta/goal-design/specify-failure-paths.md` — added variant for physical implication explorations
- **Updated** `meta/goal-design/prioritize-novelty-assessment.md` — added variant for universal constants
- **Updated** `meta/goal-design/one-task-per-exploration.md` — added corollary about splitting conceptual + computational explorations by explorer type
- **Updated** `meta/goal-design/INDEX.md` — 16 → 17 entries
- **Updated** `meta/methodology/INDEX.md` — 13 → 14 entries
- **Updated** `meta/INDEX.md` — updated counts

### Unruh-Inertia Survey + No-Go Landscape (Exploration 003, compton-unruh strategy-001)

Comprehensive survey of all major Unruh-based inertia proposals and systematic no-go analysis.

- **Created** `compton-unruh/mcculloch-qi-negative-mass.md` — McCulloch QI: mode truncation mechanism, critical negative mass problem (m_i/m ≈ −0.70 at a₀), Renda (2019) derivation errors; conceptual mode-counting insight survives
- **Created** `compton-unruh/hrp-sed-inertia-dead.md` — HRP SED vacuum inertia: ZPF Lorentz force mechanism definitively refuted by Levin (2009); DEAD
- **Created** `compton-unruh/mond-phenomenology-coincidences.md` — MOND formula, a₀ cosmological coincidences table, EFE, observational scorecard (galaxies ✓, clusters ✗, CMB ✗), solar system constraints
- **Created** `compton-unruh/verlinde-emergent-gravity-a0.md` — Verlinde derives a₀ = cH₀/6 from area-volume entropy in de Sitter; within 8% of observed; most theoretically grounded surviving proposal
- **Created** `compton-unruh/unruh-inertia-no-go-landscape.md` — Verdict table (thermal/HRP/McCulloch/resonance DEAD; mode-counting/entropic/crossover open); freely-falling observer paradox as key unsolved objection
- **Updated** `compton-unruh/INDEX.md` — 3 → 8 findings (after Exploration 003)
- **Updated** `factual/INDEX.md` — 195 → 203 findings

### De Sitter Crossover Mechanism Investigation (Exploration 004, compton-unruh strategy-001)

Wightman function analysis, force mechanism sweep, T_U/T_dS = μ_MOND algebraic identity.

- **Created** `compton-unruh/desitter-wightman-crossover-structure.md` — De Sitter Wightman function same sinh⁻² form; spectrum Planckian in all regimes; temperature crossover table (T_dS/T_U = 5.6 at MOND scale)
- **Created** `compton-unruh/tu-tds-mond-identity.md` — KEY: T_U/T_dS = a/√(a²+c²H₀²) = standard MOND interpolation function μ(x) = x/√(1+x²); rotation curves; BTFR; a₀ = cH₀ is 5.5× too large; solar system consistent
- **Created** `compton-unruh/desitter-force-mechanisms-assessment.md` — Three mechanisms tested: naive entropic (wrong sign), ALD self-force (vanishes), ratio ansatz (exact MOND but physically unjustified); rigorous path = DeWitt-Brehme in de Sitter
- **Updated** `compton-unruh/INDEX.md` — 8 → 11 findings (after Exploration 004)
- **Updated** `factual/INDEX.md` — 203 → 203 findings (count captured above; compton-unruh entry updated)

### Meta-Learning: Compton-Unruh Explorations 003-004

- **Created** `meta/goal-design/distinguish-identity-from-mechanism.md` — Require explorers to label algebraic identities vs. physical derivations; prevents conflating T_U/T_dS = μ_MOND (identity) with a mechanism
- **Created** `meta/methodology/multi-ansatz-sweep-pattern.md` — When N similar ansatze exist, test all in one pass; rules out N-1 candidates with diagnostic comparison table
- **Updated** `meta/goal-design/preload-context-from-prior-work.md` — Added "retrying a failed exploration" variant: repeat mission name, directory, and prior negative results explicitly
- **Updated** `meta/goal-design/specify-failure-paths.md` — Added "rate each assumption's weakness" variant (CRITICAL/MODERATE/LOW ratings); proved essential for catching that ratio ansatz is unjustified
- **Updated** `meta/goal-design/INDEX.md` — 13 → 14 entries
- **Updated** `meta/methodology/INDEX.md` — 12 → 13 entries
- **Updated** `meta/INDEX.md` — goal-design 13→14, methodology 12→13; added stochastic-electrodynamics to mission list

### Classicality Budget Prior Art Search (Exploration 003, classicality-budget strategy-001)

Comprehensive prior art search: 29 queries, 17 papers, 8 author groups. Refined novelty from "novel" to "PARTIALLY KNOWN (Novel Synthesis)."

- **Created** `classicality-budget/prior-art-literature-search.md` — Tank (2025) structural precursor, two-community gap, Hayden-Wang conceptual neighbor, comprehensive search audit, refined verdict
- **Updated** `classicality-budget/zurek-saturation-and-novelty.md` — Novelty assessment refined from unqualified "novel" to "PARTIALLY KNOWN (Novel Synthesis)" with Tank (2025) caveat and structural-vs-physical distinction
- **Updated** `classicality-budget/INDEX.md` — 4 → 5 findings, added novelty verdict to description
- **Updated** `factual/INDEX.md` — 194 → 195 findings, updated classicality-budget description

### Meta-Learning: Classicality Budget Exploration 003

- **Created** `meta/goal-design/prioritize-novelty-assessment.md` — Make novelty assessment Task 1 when a specific theory is identified
- **Updated** `meta/goal-design/use-classification-schemes.md` — Added "Prior Art Comparison Tables" variant with classicality-budget evidence
- **Created** `meta/methodology/gap-finding-in-existing-programs.md` — Identifying gaps in existing programs is as valuable as inventing new theories

### SED Extension Landscape (Exploration 002, stochastic-electrodynamics strategy-001)

Comprehensive survey of SED computations across 5 domains, establishing the "linearity boundary" pattern.

- **Created** `stochastic-electrodynamics/` folder with INDEX.md — new top-level category in factual library (17th category)
- **Created** `stochastic-electrodynamics/established-successes.md` — 4+3 systems where SED = QM, all linear
- **Created** `stochastic-electrodynamics/hydrogen-self-ionization.md` — Three-phase history ending in decisive failure
- **Created** `stochastic-electrodynamics/anharmonic-oscillator-failure.md` — Pesquera & Claverie 1982 O(beta^2) disagreement, numerically unverified
- **Created** `stochastic-electrodynamics/quantum-coherence-failure.md` — Huang & Batelaan 2019 no-interference result
- **Created** `stochastic-electrodynamics/entanglement-bell-contested.md` — LSED/Stochastic Optics contested program
- **Created** `stochastic-electrodynamics/spin-anomalous-moment-status.md` — No spin in pure SED, SEDS claims unreliable
- **Created** `stochastic-electrodynamics/linearity-boundary-pattern.md` — Overarching pattern + open computations
- **Updated** `factual/INDEX.md` — 187 → 194 findings, added SED section

### Meta-Learning: SED Exploration 002

- **Updated** `meta/methodology/divergent-survey-pattern.md` — Expanded from 4-part to 5-part pattern: added "concrete next-computation recommendation" as Part (e)
- **Updated** `meta/goal-design/name-specific-authors-and-papers.md` — Added SED evidence for "cite specifically" producing well-sourced reports
- **Updated** `meta/goal-design/specify-rigor-level.md` — Added "what is the exact coefficient?" prompt pattern for extracting specific numerical values

### Modern Rigorous Frontier (Exploration 006, yang-mills strategy-001)

Deep technical analysis of Adhikari-Cao, Chatterjee, Shen-Zhu-Zhu and the path forward.

- **Created** `yang-mills/adhikari-cao-technique-and-obstruction.md` — Swapping map technique (4 steps) and four-layer structural obstruction preventing extension to continuous groups
- **Created** `yang-mills/shen-zhu-zhu-stochastic-analysis.md` — Bakry-Émery / Langevin mass gap for SU(N) at strong coupling (β < 1/48); complementarity table with Adhikari-Cao
- **Updated** `yang-mills/chatterjee-probabilistic-program.md` — Added results 7-9 (Cao U(N) 2025, Chatterjee 3D confinement 2026, Rajasekaran-Yakir-Zhou 2026), complete 12-paper timeline, Chatterjee's own October 2025 assessment
- **Updated** `yang-mills/proof-strategies-comparison.md` — Added timeline assessment (20-50+ years), breakthrough tier classification (Tier 1-3), wild cards
- **Updated** `yang-mills/gap-structure-overview.md` — Added explicit negative status list (6 items still NOT proved as of March 2026)
- **Updated** `yang-mills/INDEX.md` — 9 → 11 findings
- **Updated** `factual/INDEX.md` — 185 → 187 findings

### Meta-Learning: Yang-Mills Exploration 006

- **Updated** `meta/goal-design/specify-rigor-level.md` — Added "what EXACTLY do they prove" prompt pattern; precise questions enable emergent structure discovery
- **Updated** `meta/goal-design/specify-failure-paths.md` — Added "Pessimistic Assessments as High-Value Outcomes" variant
- **Updated** `meta/goal-design/use-classification-schemes.md` — Added "Structural vs. Technical Obstruction Classification" variant

### Classicality Budget Derivation (Exploration 001, classicality-budget strategy-001)

Gap-free derivation of the classicality budget inequality R_delta <= (S_max/S_T - 1)/(1-delta) from five standard axioms, plus Zurek saturation analysis and novelty assessment.

- **Created** `classicality-budget/` folder with INDEX.md — new top-level category in factual library (16th category)
- **Created** `classicality-budget/derivation-from-five-axioms.md` — Derivation chain from 5 axioms, multi-fact trade-off, boundary cases, rigor assessment
- **Created** `classicality-budget/zurek-saturation-and-novelty.md` — Zurek's R~N saturates the bound; connecting QD to Bekenstein bounds is novel
- **Updated** root `factual/INDEX.md` — added classicality-budget section, updated count

### Classicality Budget Numerical Computation (Exploration 002, classicality-budget strategy-001)

Numerical computation of the budget across 7 physical systems from Planck to cosmological scales.

- **Created** `classicality-budget/numerical-results-across-scales.md` — Summary table, Bekenstein vs holographic dominance, key physical insights
- **Created** `classicality-budget/planck-scale-classicality-breakdown.md` — S_max ~ 4.5 bits at Planck scale; classicality impossible for facts > ~2 bits
- **Updated** root `factual/INDEX.md` — updated count

### Meta-Learning: Classicality-Budget Explorations 001-002

- **Created** `meta/methodology/scale-spread-in-numerical-surveys.md` — Spread of scales more important than many similar-scale systems
- **Updated** `meta/goal-design/specify-computation-parameters.md` — Added classicality-budget evidence (providing all formulas + constants enables ~8 min completion)
- **Updated** `meta/goal-design/use-classification-schemes.md` — Added classicality-budget evidence for COMPUTED/ESTIMATED/CHECKED tagging
- **Updated** `meta/system-behavior/computation-vs-reasoning-limits.md` — Added "computation reveals non-obvious insights" section
- **Updated** `meta/methodology/INDEX.md` — 10 → 11 entries
- **Updated** `meta/INDEX.md` — added classicality-budget mission, methodology 10 → 11
- **Duplicate detected**: meta-exploration-001 lessons on Math Explorer and decisive negative results already filed from compton-unruh curator run — skipped

### Compton-Unruh Dimensional Analysis (Exploration 001, compton-unruh strategy-001)

Decisive negative result: the Compton-Unruh resonance hypothesis fails by 43 orders of magnitude.

- **Created** `compton-unruh/` folder with INDEX.md and 3 findings
- **Created** `compton-unruh/dimensional-inconsistency.md` — Matching acceleration a* ~ 10^33 m/s^2 vs. target a_0 ~ 10^-10 m/s^2; mass-dependent; no cosmological parameter; de Sitter modification negligible
- **Created** `compton-unruh/unruh-dewitt-no-resonance.md` — UDW detector response smooth Planckian, no peaks/poles; Boltzmann suppression exp(-10^42); Compton frequency enters only as Van Hove zero
- **Created** `compton-unruh/gibbons-hawking-crossover.md` — Physical crossover at a ~ cH_0 from acceleration to cosmological-horizon thermal dominance; at the right scale but no resonance or inertia modification
- **Updated** `factual/INDEX.md` — 178 → 181 findings, 14 → 15 categories, added Compton-Unruh section

### Meta-Learning: Compton-Unruh Exploration 001

- **Created** `meta/methodology/math-explorer-dimensional-analysis.md` — Math Explorer + dimensional analysis is an excellent pattern for quantitative feasibility checks
- **Created** `meta/methodology/decisive-negative-pivot.md` — Discrepancies > 10 orders of magnitude are hard kills; pivot immediately
- **Updated** `meta/system-behavior/explorer-crashes-and-path-confusion.md` — Added context contamination variant for parallel explorer launches
- **Updated** `meta/methodology/INDEX.md` — 8 → 10 entries
- **Updated** `meta/INDEX.md` — methodology count 8 → 10, added compton-unruh to mission list

### SU(2) Lattice Computation Verification (Exploration 003, yang-mills strategy-001)

First-principles SU(2) lattice Monte Carlo reproducing known results; practical lattice size requirements.

- **Updated** `yang-mills/lattice-numerical-evidence.md` — Added Atlas SU(2) verification section (exploration-003 reproduces literature within 1-2σ on 4⁴-8⁴) and practical lattice size requirements table (glueball mass needs ≥16⁴, scaling needs β ≥ 2.4 on ≥16⁴)
- **Updated** `yang-mills/INDEX.md` — description updated with verification note

### Meta-Learning: Yang-Mills Exploration 003

- **Created** `meta/goal-design/specify-computation-parameters.md` — Specify exact simulation parameters (β values, lattice sizes) for reproducible, comparable results
- **Updated** `meta/system-behavior/computation-vs-reasoning-limits.md` — Explorers CAN implement full Monte Carlo simulations from scratch; added practical lattice limits
- **Updated** `meta/goal-design/use-classification-schemes.md` — Added verification scorecard variant (VERIFIED/COMPUTED/CHECKED/CONJECTURED)
- **Updated** `meta/goal-design/specify-failure-paths.md` — Added diagnostic outputs recommendation
- **Updated** `meta/system-behavior/explorer-crashes-and-path-confusion.md` — Added tmux paste-then-Enter requirement
- **Updated** `meta/goal-design/INDEX.md` — count 11 → 12
- **Updated** `meta/INDEX.md` — goal-design count 11 → 12

### Number Variance, Spectral Rigidity, and Berry's Saturation (Exploration 002, riemann-hypothesis strategy-001)

Long-range spectral statistics of zeta zeros confirming Berry's 1985 saturation prediction.

- **Created** `riemann-hypothesis/berry-saturation-confirmed.md` — Σ²(L) saturates at ~0.3–0.5 for L>2, Δ₃(L) saturates at 0.156 for L>15; zeta zeros 30–50% more rigid than finite-size GUE; prime periodic orbits cause saturation
- **Created** `riemann-hypothesis/spectral-form-factor-gue.md` — K(τ) matches GUE within 1–4% (ramp slope 1.010, plateau 1.043); confirms GUE universality class
- **Updated** `riemann-hypothesis/riemann-operator-constraints.md` — Added periodic orbit constraints (chaotic classical limit, periods ~ log p, super-rigidity beyond GUE, no missing structure)
- **Updated** `riemann-hypothesis/INDEX.md` — 3→5 findings, reorganized into Short-Range / Long-Range / Operator Constraints sections
- **Updated** root `factual/INDEX.md` — 174→176 findings

### Meta-Learning: QG-2 Exploration 002

- **Updated** `meta/goal-design/use-classification-schemes.md` — Added constraint-checklist variant (provide explicit list of constraints to check proposals against)

### Balaban's RG Program for Yang-Mills (Exploration 001, yang-mills strategy-001)

First entries for the yang-mills mission. Precision map of Balaban's renormalization group program, gap structure toward Millennium Problem, and modern developments.

- **Created** `yang-mills/` folder with INDEX.md — new top-level category in factual library (14th category)
- **Created** `yang-mills/balaban-uv-stability.md` — 14-paper program (1983-1989), four phases, precise UV stability theorem, what it does/doesn't achieve
- **Created** `yang-mills/gap-structure-overview.md` — Two-tier gap structure (tractable vs. fundamental), 12-step chain with status, 4 gaps with mathematical formulations
- **Created** `yang-mills/dimock-expository-program.md` — Dimock's 2011-2022 revisitation, φ⁴₃ expository series, QED in 3D, NLSM extensions
- **Created** `yang-mills/chatterjee-probabilistic-program.md` — Probabilistic approach, Wilson loops for finite groups, mass gap ⟹ confinement, trivial SU(2) YMH limit
- **Created** `yang-mills/stochastic-quantization-chandra-hairer.md` — Regularity structures approach to 3D YMH (2024), dynamics vs. measure difference
- **Created** `yang-mills/other-modern-approaches.md` — Faria da Veiga-O'Carroll, MRS continuum, Charalambous-Gross heat flow, Federbush phase cell
- **Created** `yang-mills/completed-gauge-constructions.md` — BFS 2D abelian Higgs (only complete OS construction), King 3D Higgs, Gross/Driver abelian
- **Updated** root `factual/INDEX.md` — 167→174 findings, 13→14 top-level categories

### Meta-Learning: Yang-Mills Exploration 001

- **Created** `meta/goal-design/specify-rigor-level.md` — Explicitly requesting rigor level gets detailed technical tracking
- **Updated** `meta/goal-design/name-specific-authors-and-papers.md` — Added yang-mills evidence (Balaban targets led to Dimock, Chandra-Hairer, Faria da Veiga discovery)
- **Updated** `meta/goal-design/use-classification-schemes.md` — Added progress stratification use case (COMPLETED/NOT ATTEMPTED scheme)
- **Updated** `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` — Added technical mapping nuance (web research time ≠ stalling, check tmux not just line count)
- **Updated** `meta/goal-design/INDEX.md` — 10→11 entries
- **Updated** `meta/INDEX.md` — Added yang-mills mission to scope description

### Riemann Hypothesis GUE Statistics (Exploration 001, riemann-hypothesis strategy-001)

First entries for the Riemann hypothesis mission. Computational study of 2,000+ zeta zeros confirming GUE statistics.

- **Created** `riemann-hypothesis/` folder with INDEX.md — new top-level category in factual library
- **Created** `riemann-hypothesis/gue-pair-correlation.md` — Montgomery's conjecture confirmed to 9.1% mean relative deviation (STRONG MATCH); chi-squared/dof = 1.50; 68% within 1-sigma; no height dependence; full methodology
- **Created** `riemann-hypothesis/gue-nearest-neighbor-spacing.md` — GUE Wigner surmise match at 4.1% mean abs dev; ensemble discrimination (GUE > GSE > GOE >> Poisson); KS marginal failure = Wigner surmise approximation; quadratic level repulsion confirmed
- **Created** `riemann-hypothesis/riemann-operator-constraints.md` — Rules out Poisson (integrable), GOE (real symmetric), disfavors GSE; requires complex Hilbert space + broken time-reversal symmetry
- **Updated** root `factual/INDEX.md` — 164→167 findings, 12→13 top-level categories

### Meta-Learning: Goal Design (meta-exploration-001)

Three new goal-design lessons from divergent survey meta-learning.

- **Created** `meta/goal-design/specify-temporal-recency.md` — Explicit time windows get genuinely current results
- **Created** `meta/goal-design/request-equations-for-construction.md` — Construction tasks need explicit equation/derivation requests
- **Created** `meta/goal-design/require-claim-attribution.md` — Ask explorers to distinguish sourced vs. own reasoning
- **Updated** `meta/goal-design/INDEX.md` — 7→10 entries
- **Updated** `meta/INDEX.md` — Updated mission scope description and entry count

## 2026-03-26

### Complete Theory Document + Mission Validation (Explorations s4-007 & s4-008, strategy-004)

Processed exploration-s4-007-complete-theory.md and exploration-s4-008-mission-validation.md. The complete theory document is the final consolidated deliverable of the Atlas QG research program across 4 strategies and 38+ explorations. The mission validation provides a formal 5-tier assessment.

- **Created** `cross-cutting/unified-qgf-as-framework/mission-validation-assessment.md` — Formal 5-tier mission validation: Novelty MARGINAL, Logical Consistency PASS, Explanatory Power MARGINAL, Compatibility with Reality PASS, Depth PASS (3/2/0); mission comparison (partially satisfies — falls short on "genuinely new" and "novel explanations"); 4-strategy retrospective arc; Strategy 005 options; honest bottom line ("sophisticated literature synthesis, empirically vacuous")
- **Updated** `cross-cutting/unified-qgf-as-framework/framework-conjecture.md` — Major revision to Overall Assessment section: reframed from "most parsimonious interpretation" to "structural conjecture — organizational, not predictive"; added post-adversarial findings (zero novel discriminating predictions, H₀ simpler and equally explanatory, QCD analogy breaks at 3 load-bearing joints); added "what would change this assessment" (3 specific conditions); added comparison to alternatives (vs. String Theory, LQG, standalone components); cross-reference to mission validation
- **Updated** `cross-cutting/unified-qgf-as-framework/novel-predictions.md` — Added consolidated post-adversarial prediction survival table (11 predictions with pre/post-adversarial status, testability); key downgrades documented (P-UNI-1 → CONSISTENCY CHECK, P-UNI-2 → DEAD); b parameter cautionary tale for δ₃ lead (12-order-of-magnitude RG suppression precedent); bottom line statement
- **Updated** all INDEX.md files — unified-qgf-as-framework (7 → 8 findings, description updated with post-adversarial status), cross-cutting (40 → 41), root (162 → 163), descriptions updated throughout with final assessment framing

### Meta-Interpretation Stress-Test (Exploration 006, nature-of-time strategy-002)

Processed exploration-006-stress-test-synthesis.md. Five maximum-strength adversarial attacks on "Time as Irreversible Determination" synthesis. Revised score from 57.0 to 52.5/65. Key finding: synthesis is "CI with ontological upgrade," not transcendent meta-interpretation. QRF-process tension identified as unresolved internal incoherence.

- **Created** `cross-cutting/meta-interpretation-stress-test.md` — Full adversarial stress-test: 5 attacks with verdicts (2 PARTIALLY SURVIVED: synonym and circularity; 3 WOUNDED: score inflation, PH reframing, potentialities dependency), revised 13-criterion score table (57.0→52.5), QRF-process tension (timeless WDW vs. processual ontology), QM compatibility matrix (incompatible with Everettian, pilot wave, strict Copenhagen), 6 mandatory modifications, final assessment ("CI + ontological upgrade"), CI-CP structural isomorphism as most important standalone discovery
- **Updated** `cross-cutting/meta-interpretation-determination.md` — Major revision: score downgrade (57.0→52.5) with full revised score table; "determination" reframed from primitive to bridging concept; Tension 2 (PH) rewritten to acknowledge verbal nature of "natural initial condition" claim; new QRF-Process Tension section; new QM Compatibility Matrix; honest limits expanded from 6 to 8 (added QRF tension, determination-as-label); Self-Critique Assessment replaced with Post-Stress-Test Assessment; architecture reframed as "CI with ontological upgrade"; cross-reference to stress-test added
- **Updated** `cross-cutting/ci-vs-cp-tournament.md` — Synthesis Outcome section updated (57.0→52.5, post-stress-test context, architectural insight); cross-reference to stress-test added
- **Updated** `cross-cutting/three-layer-time-synthesis.md` — Cross-reference updated (57.0→52.5, stress-test link added)
- **Updated** all INDEX.md files — cross-cutting (39→40 findings), root (161→162), descriptions updated with post-stress-test score and key findings

### Higgs Mass Consistency Check (Exploration s4-004, strategy-004)

Processed exploration-s4-004-higgs-mass-consistency.md (quantum-gravity-2 strategy-004). Fakeon prescription does NOT affect the Shaposhnikov-Wetterich Higgs mass prediction; three independent arguments; |Δm_H| < 10⁻⁷ GeV.

- **Created** `cross-cutting/unified-qgf-as-framework/higgs-mass-consistency.md` — Full consistency check: three independent arguments (prescription-independent UV divergences/beta functions, Euclidean FRG prescription-indistinguishable, absorptive part vanishes below M₂ threshold); conservative bound |Δm_H| < 10⁻⁷ GeV; uncertainty comparison table; "topological" SW structural robustness; C² ghost already implicit in AS; Eichhorn-Held + dark portal extensions unaffected; residual open calc: A_λ in C²-extended FRG
- **Updated** `cross-cutting/unified-qgf-as-framework/novel-predictions.md` — Prediction #7 marked RESOLVED ✓ (from open questions to answered: fakeon does not affect prediction, |Δm_H| < 10⁻⁷ GeV, three-argument summary, classified as non-novel consistency check)
- **Updated** `asymptotic-safety/standard-model.md` — Added detailed uncertainty budget (m_top ±3 GeV dominant, δm_H ≈ 1 per 1 shift, α_s ±1, higher-loop ±0.5), "topological" prediction robustness, Einstein-Hilbert truncation limitation, full fakeon compatibility paragraph with cross-reference
- **Updated** all INDEX.md files — unified-qgf-as-framework (6 → 7 findings), cross-cutting (36 → 37), root (158 → 159), descriptions updated

### CP Adversarial Assessment (Exploration 003, nature-of-time strategy-002)

Processed exploration-003-adversarial-attack-cp.md. Four-dimensional adversarial attack on the Causal-Processual interpretation of time: convergence with CI, physics vacuum, block universe response, panexperientialism dependency.

- **Created** `cross-cutting/cp-adversarial-assessment.md` — Full adversarial assessment: 4 attacks with verdicts (2 PARTIALLY SURVIVED, 2 WOUNDED), CP-CI 8-row structural isomorphism table, three genuine forks identified (potentia ontology STRONG, direction of explanation MODERATE, subject nature WEAK), physics component inventory (1 unconfirmed framework + 3 philosophies), Prigogine reception (Bricmont 1996, Drouet-Lippens 2025), causal-order Rietdijk-Putnam response (EXCELLENT), growth-vs-construction stalemate, three-level flow framework repair (Level 1-3), revised scores 26→25, post-attack formulation, honest meta-assessment
- **Updated** `cross-cutting/causal-processual-interpretation.md` — Post-attack score revision (26→25), flow section rewritten with three-level framework, honest weaknesses section revised and strengthened (5 weaknesses reorganized around attack results), cross-reference to adversarial assessment added
- **Updated** `cross-cutting/time-interpretation-challenger-survey.md` — CP grand total 39→38 (post-attack), post-attack feature scores added, meta-criteria vulnerability and novelty adjusted, cross-reference to adversarial assessment
- **Updated** `causal-set-theory/swerves-phenomenology.md` — Added specific observational constraint k ≤ 10⁻⁵⁶ kg²m²s⁻³ from spontaneous heating bounds; cosmic ray swerves ruled out
- **Updated** all INDEX.md files — cross-cutting (35 → 36 findings), root (157 → 158), descriptions updated

### BH Phase Transition Quantitative Predictions (Exploration s4-002, strategy-004)

Processed exploration-s4-002-bh-phase-transition.md (quantum-gravity-2 strategy-004). Quantitative predictions for the BH evaporation phase transition: M_crit, T_crit, transition order, classification of 12 predictions, honest assessment.

- **Created** `cross-cutting/unified-qgf-as-framework/bh-phase-transition-predictions.md` — M_crit = 0.308 M_P (convention-dependent: 1.55 M_P if reduced Planck mass); T_crit = 0.03–0.13 M_P; transition order (first-order pure gravity, crossover gravity+SM, by QCD analogy); gravitational Polyakov loop analog; latent heat ~7 kJ; M_rem vs M_crit ordering; 12-prediction classification table (6 NOVEL, 5 INHERITED, 1 DISCRIMINATING); honest verdict: "AS predictions + ghost trigger"
- **Updated** `cross-cutting/unified-qgf-as-framework/novel-predictions.md` — Expanded prediction #3 with specific M_crit values (both conventions), convention uncertainty, transition order prediction, M_rem vs M_crit ordering, corrected PBH DM statement, honest caveat (7/12 inherited), cross-reference to detailed entry
- **Corrected** `asymptotic-safety/black-holes-and-singularity-resolution.md` — PBH DM: "could dominate" replaced with "cannot be ALL of dark matter" (γ-ray constraints β < 10⁻²⁵ vs. needed β ~ 10⁻¹⁸); added specific remnant properties and very-light-PBH caveat
- **Updated** all INDEX.md files — unified-qgf-as-framework (5 → 6 findings), cross-cutting (34 → 35), root (156 → 157)

### Ghost Propagator Specification (Exploration s4-001, strategy-004)

Processed exploration-s4-001-ghost-propagator-specification.md (quantum-gravity-2 strategy-004). Detailed quantitative specification of the ghost propagator prediction: numerical NGFP values, pole migration pattern, amplitude equivalence test.

- **Created** `cross-cutting/unified-qgf-as-framework/ghost-propagator-prediction.md` — Quantitative ghost propagator prediction: m₂/k ≈ 1.42 at NGFP (from Benedetti et al. g₁*/g₃* = 2.02), predicted pole migration pattern (real → complex → tower), mathematical form (tanh form factor interpolation), transition scale ~2M̄_P², BH instability scale r_H ≈ 0.63 l_P, amplitude equivalence test as sharpest criterion, three unknowns (c_C, trajectory, form factor), honest assessment (consistency check not sharp prediction), 5-step FRG computational specification
- **Updated** `asymptotic-safety/ghost-fate-strong-coupling.md` — Added specific Benedetti et al. 2009 NGFP numerical values (g₀*–g₃*, critical exponents θ₀–θ₃, universal product), derived ghost mass ratio m₂/k ≈ 1.42, explicit statement that mass-divergence mechanism is structurally excluded for spin-2
- **Updated** `cross-cutting/unified-qgf-as-framework/discriminating-predictions.md` — Added amplitude equivalence test as sharpest discriminating criterion and honest assessment ("consistency check, not sharp prediction")
- **Updated** `quadratic-gravity-fakeon/black-hole-predictions.md` — Added specific numerical BH instability scale r_H ≈ 0.63 l_P using m₂ ≈ 1.42 M_P
- **Updated** all INDEX.md files — unified-qgf-as-framework (4 → 5 findings), cross-cutting (31 → 32), root (153 → 154)

### Discriminating Predictions for the Unified Framework (Exploration 009, strategy-003)

Processed exploration-009-discriminating-predictions.md (quantum-gravity-2 strategy-003). Systematic identification of what discriminates the unified QG+F–AS framework from the "compatible-but-separate" null hypothesis.

- **Created** `cross-cutting/unified-qgf-as-framework/discriminating-predictions.md` — Null hypothesis H₀ formulated, three discriminators ranked (ghost dissolution STRONG, average continuation MODERATE, coupling unification WEAK), near-term experimental assessment (NO discriminating prediction before 2030), falsifiability verdict, computational roadmap
- **Updated** `asymptotic-safety/ghost-fate-strong-coupling.md` — Added Knorr & Saueressig (2022) spectral reconstruction reference under Critical Gap section (new: background vs. dynamical graviton spectral functions, Einstein-Hilbert truncation only)
- **Updated** `cross-cutting/unified-qgf-as-framework/novel-predictions.md` — Added Baldazzi et al. 2025 caveat to prediction #1 (average continuation may be rendered moot by Lorentzian AS); added critical exponent values and b ~ θ/(16π²) quantitative estimate to prediction #4
- **Updated** `cross-cutting/unified-qgf-as-framework/open-problems.md` — Enhanced #2 with feasibility estimate and cross-reference to discrimination analysis
- **Updated** all INDEX.md files — unified-qgf-as-framework (3 → 4 findings), cross-cutting (30 → 31), root (152 → 153)

### Unified QG+F--AS Framework (Exploration 007, strategy-003)

Processed exploration-007-unified-framework.md (quantum-gravity-2 strategy-003). Synthesis document constructing a coherent unified theory treating QG+F and AS as perturbative/non-perturbative descriptions of one UV-complete quantum gravity theory, analogous to QCD.

- **Created** `cross-cutting/unified-qgf-as-framework/` subfolder with INDEX.md and 3 findings:
  - `framework-conjecture.md` — Formal theory statement: conjecture, precise QCD analogy (11-row mapping table), master regime table (8 regimes from trans-Planckian to cosmological IR), Planck-scale phase transition (3 independent lines of evidence), 5 bridge mechanisms summary with cross-references to existing detailed entries, comparison table (what unification adds vs. standalone QG+F and AS), overall strengths/weaknesses assessment
  - `novel-predictions.md` — 7 novel predictions unique to unification: (1) average continuation resolves AS Wick rotation, (2) ghost confinement scale = M_P dynamically generated, (3) BH evaporation phase transition with 3 phases and PBH remnant observables, (4) unified r formula combining QG+F alpha/beta with AS b parameter, (5) spectral dimension profile matching as consistency check, (6) six-derivative extension from NGFP truncation hierarchy, (7) Higgs mass as UV boundary consistency check
  - `open-problems.md` — Prioritized open problems: #1 AF->NGFP trajectory (most important, specific resolving calculation defined), #2 spin-2 ghost confinement (second most important, specific resolving calculation defined), plus 5 additional issues (non-perturbative uncertainty, n_s tension, matter sector, CC problem, experimental falsification conditions)
- **Updated** `cross-cutting/INDEX.md` — added unified-qgf-as-framework subfolder entry; count 27 → 30
- **Updated** `factual/INDEX.md` — added unified framework to cross-cutting description; count 149 → 152; count in cross-cutting section 27 → 30

### Analyticity Reconciliation (Exploration 006, strategy-003)

Processed exploration-006-analyticity-reconciliation.md (quantum-gravity-2 strategy-003). Systematic analysis of whether QG+F's analyticity sacrifice is compatible with AS's Euclidean FRG framework. Verdict: SUPPORTS — analyticity sacrifice is not a barrier to QG+F = AS.

- **Created** `cross-cutting/qgf-vs-as-analyticity-compatibility.md` — Three-step argument: (1) AS FRG doesn't require analyticity, (2) AS already has non-standard analytic structure (Donoghue Wick rotation obstruction, Draper complex pole towers, Bonanno assumption), (3) Lorentzian AS bypasses analyticity entirely (D'Angelo et al. 2024); fakeon average continuation may solve AS's Wick rotation problem; evidence strength table; verdict: SUPPORTS
- **Overwrote** `quadratic-gravity-fakeon/analyticity-sacrifice.md` — "Comparison with Other Approaches" AS entry: old claim "Standard analytic structure at the UV fixed point" replaced with "Also has non-standard analytic structure" with details. Reason: exploration-006 demonstrated AS doesn't have standard analyticity either. Also added "Average Continuation" section explaining the fakeon's nonanalytic Euclidean→Lorentzian mechanism.
- **Updated** `asymptotic-safety/graviton-propagator.md` — Added "Wick Rotation Obstruction" section (Donoghue ghost pole, Draper imaginary-p² towers, Bonanno assumption) and new open issue; cross-reference to analyticity compatibility analysis
- **Updated** `asymptotic-safety/limitations.md` — Expanded "Lorentzian vs. Euclidean" section with D'Angelo et al. 2024 (NGFP in Lorentzian), Manrique causal FRG, foliated AS 2025; cross-reference to analyticity compatibility analysis
- **Updated** all INDEX.md files — cross-cutting (26 → 27 findings), root (148 → 149 findings), descriptions updated

### BH Compatibility Analysis (Exploration 005, strategy-003)

Processed exploration-005-bh-compatibility.md (quantum-gravity-2 strategy-003). Systematic analysis of whether QG+F and AS black hole predictions are compatible. Verdict: SUPPORTS — perturbative vs. non-perturbative regime complementarity, analogous to QCD.

- **Created** `cross-cutting/qgf-vs-as-bh-compatibility.md` — Systematic five-argument compatibility analysis: (1) QG+F admits non-perturbative blindness, (2) perturbative breakdown at AS takeover, (3) branch crossing phase transition, (4) large-r quantitative agreement, (5) Holdom-Ren phase transition; domain-of-validity regime table; spontaneous ghostification 3-possibility analysis; 4 incompatibility conditions (none met); verdict: SUPPORTS
- **Updated** `quadratic-gravity-fakeon/black-hole-predictions.md` — Conclusion reframed from "highlights the tension" to "compatible, not contradictory" with cross-reference to compatibility analysis
- **Updated** `asymptotic-safety/black-holes-and-singularity-resolution.md` — Added explicit BR metric large-r formula matching and SUPPORTS verdict cross-reference
- **Updated** all INDEX.md files — cross-cutting (25 → 26), root (147 → 148), descriptions updated

### Inflation Prediction Reconciliation (Exploration 004, strategy-003)

Processed exploration-004-inflation-prediction-reconciliation.md (quantum-gravity-2 strategy-003). Systematic comparison of AS and QG+F inflationary predictions, revealing both frameworks predict Starobinsky inflation and correcting the misleading "inflaton-free" characterization of AS.

- **Overwrote** `asymptotic-safety/cosmology.md` — "Inflation Without an Inflaton" section replaced with "AS Inflation: Four Distinct Classes." Old claim: AS inflation is inflaton-free with r up to 0.01. New claim: Only Bonanno-Reuter 2002 is inflaton-free; most AS models (Codello 2014, Gubitosi 2018, Bonanno-Platania 2015/18, Pawlowski 2024) produce Starobinsky inflation with r ≈ 0.003. Reason: exploration-004 systematically reviewed 6 AS inflation models and found the inflaton-free characterization applies only to the most primitive.
- **Overwrote** `cross-cutting/qgf-vs-as-cmb-discrimination.md` — AS inflation characterization corrected from "no inflaton needed" to "most models: yes (R² scalaron from NGFP flow)." Added reconciliation analysis, missing R²+C² calculation gap, corrected discrimination table. Reason: same exploration.
- **Updated** `quadratic-gravity-fakeon/inflationary-predictions.md` — Added Bianchi-Gamonal 2025 precision W² correction formula and Anselmi 2023 causality bound on inflationary models.
- **Updated** all INDEX.md files — asymptotic-safety, cross-cutting, quadratic-gravity-fakeon, root factual (descriptions updated, no count changes)

### Ghost Fate at Strong Coupling (Exploration 003, strategy-003)

Processed exploration-003-ghost-fate-strong-coupling.md (quantum-gravity-2 strategy-003). Comprehensive survey of spin-2 ghost fate in the AS literature.

- **Created** `asymptotic-safety/ghost-fate-strong-coupling.md` — 4 proposed mechanisms (Holdom-Ren confinement, Becker et al. scalar ghost decoupling, Platania-Wetterich fictitious ghosts, Draper et al. complex pole tower); critical gap (no spin-2 ghost propagator computed); Benedetti et al. 2009 (f₂ finite at NGFP → ghost mass stays finite); CDT non-resolution; verdict: INCONCLUSIVE leaning SUPPORTS; QG+F = AS bridge at ghost level unbuilt
- **Updated** `asymptotic-safety/graviton-propagator.md` — Added "Critical Caveat" section noting ghost absent from Einstein-Hilbert truncation; added ghost propagator as open issue; cross-reference to ghost-fate entry
- **Updated** `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` — Added Holdom-Ren Case A/B mechanisms, 5 author-acknowledged limitations, Frasca 2025 scope limitation (scalar sector only), cross-reference to ghost-fate entry
- **Updated** all INDEX.md files — asymptotic-safety (13 → 14 findings), root (146 → 147 findings)

### Causal Fakeon Theory Deep Build (Exploration 006)

Processed exploration-006-causal-fakeon-theory.md (quantum-gravity-2 strategy-002). Major upgrade of causal-order fakeon interpretation concept into full formal theory framework (CFT) with axioms, physical consequences, comparison table, novel predictions, and open problems.

- **Updated** `quadratic-gravity-fakeon/causal-order-fakeon-interpretation.md` — Upgraded from concept sketch to full CFT framework: 4 axioms (causal foundation, spectral causal compatibility, Wheeler exclusion, perturbative self-consistency) + 1 conjecture (loop extension); self-consistency resolution for circularity concern (Axiom 4); detailed loop-level analysis with 3 specific technical requirements; CFT vs QG+F comparison table; 4 physical consequences; 3 novel predictions including structural prediction (CST → quadratic gravity); 5 formalized open problems; expanded devil's advocate; additional references (Belenchia et al. 2016, Afshordi-Aslanbeigi-Sorkin 2012, Anselmi 2021 diagrammar)
- **Updated** `quadratic-gravity-fakeon/INDEX.md` — Updated entry description to reflect CFT formalization
- **Updated** `factual/INDEX.md` — Updated QG+F entry to mention CFT framework

### Three Novel Fakeon Interpretation Concepts (Explorations 003-005)

Processed three exploration reports from quantum-gravity-2 strategy-002: full concept developments of three novel interpretations of the fakeon prescription targeting QG+F's Gap #1 (fakeon interpretation + analyticity sacrifice).

- **Created** `quadratic-gravity-fakeon/causal-order-fakeon-interpretation.md` — Causal order as physical origin of fakeon; Wheeler propagator = fakeon at tree level; Belenchia et al. (2015) causal set bridge; SJ vacuum mechanism; loop-level gap; devil's advocate
- **Created** `quadratic-gravity-fakeon/indivisibility-fakeon-interpretation.md` — Fakeon as gravitational indivisibility (Barandes-Doukas); explains analyticity sacrifice via irreducible multi-time information; measurement problem connection; non-perturbative criterion; devil's advocate
- **Created** `quadratic-gravity-fakeon/entanglement-structure-fakeon-interpretation.md` — Entanglement structure requires fakeon; ghost entanglement pathology (Jatkar-Narayan 2017); MVEH self-consistency loop; analyticity as informational area law; structural prediction; devil's advocate
- **Updated** `gravitize-the-quantum/scg-viable-moves-for-qgf.md` — Added cross-references from Moves 2, 5, and 7 to their full developments
- **Updated** all INDEX.md files — quadratic-gravity-fakeon (15 → 18 findings), root (142 → 145 findings)

### SCG Viable Moves for QG+F Theory Construction

Processed exploration-002-scg-conceptual-moves.md (quantum-gravity-2 strategy-002). Systematic extraction of 7 conceptual moves from SCG v2.0 targeting QG+F's explanatory gaps, with viability and novelty rankings.

- **Created** `gravitize-the-quantum/scg-viable-moves-for-qgf.md` — New finding: 7 conceptual moves (computational cost → fakeon, indivisibility → fakeon, noise → microcausality, finite config → regulator, causal order → fakeon, complexity → singularity, entanglement-theoretic fakeon); viability rankings; critical classical → quantum constraint
- **Updated** `gravitize-the-quantum/scg-theory-construction.md` — Added cross-reference to viable moves catalog
- **Updated** `quadratic-gravity-fakeon/explanatory-debts-catalog.md` — Added section linking top gaps to viable conceptual moves
- **Updated** all INDEX.md files — gravitize-the-quantum (14 → 15 findings), root (141 → 142 findings)

### QG+F Explanatory Debts Catalog

Processed exploration-001-qgf-explanatory-debts.md (quantum-gravity-2 strategy-002). Comprehensive catalog of 23 explanatory debts of QG+F with severity/specificity ratings and ranked top-5 fertile gaps for novel theory construction.

- **Created** `quadratic-gravity-fakeon/analyticity-sacrifice.md` — New finding: fakeon prescription sacrifices S-matrix analyticity; 4-prescription trade-off table (Anselmi et al. JHEP 2025); Anselmi's 2026 radical position on causality abandonment
- **Created** `quadratic-gravity-fakeon/explanatory-debts-catalog.md` — Comprehensive ranked catalog of 23 debts (4 CRITICAL, 7 MAJOR, 12 MODERATE); TOP 5 fertile gaps; community blind spots; comparative framework analysis
- **Updated** `quadratic-gravity-fakeon/research-program-status.md` — Added substance to 2025 and 2026 milestone entries (amplitude prescriptions paper details, Anselmi causality paper)
- **Updated** all INDEX.md files — quadratic-gravity-fakeon (13 → 15 findings), root (139 → 141 findings)

### SCG v2.0: Causal Order Rewrite

Processed exploration-007-scg-v2-causal-order.md (quantum-gravity-2 strategy-001). Major rewrite of SCG Axiom 3 to fix the fatal Lorentzian signature problem. Replaces symmetric cost function with causal partial order + directed cost + volume measure.

- **Created** `gravitize-the-quantum/scg-v2-causal-order-rewrite.md` — Full v2.0 axiom set, derivation chain survival analysis, scorecard (v1.0 → v2.0), what's fixed (Lorentzian signature, hyperbolic operators, Jacobson alignment), what remains broken (QM reformulation, continuum limit, Pedraza 2D, no unique predictions), two new moderate gaps (volume measure origin, partial order justification), verdict: "alive but wounded"
- **Updated** `gravitize-the-quantum/scg-theory-construction.md` — Status upgraded from "fatally flawed" to "alive but wounded" with v2.0 reference; Lorentzian signature gap marked as resolved; added v2.0 cross-reference
- **Updated** `gravitize-the-quantum/scg-adversarial-assessment.md` — FATAL flaw marked as addressed in v2.0; overall verdict updated to note v2.0 response; "What Would Elevate SCG" item #1 marked as addressed
- **Updated** all INDEX.md files — gravitize-the-quantum (13 → 14 findings), root (138 → 139 findings)

### SCG Adversarial Assessment: Devil's Advocate Attack

Processed exploration-005-devils-advocate-scg.md (quantum-gravity-2 strategy-001). Systematic 7-vector attack on SCG. Verdict: SCG does NOT survive in current form — FATAL Lorentzian signature flaw, near-fatal derivation gaps, no unique predictions.

- **Created** `gravitize-the-quantum/scg-adversarial-assessment.md` — Comprehensive adversarial review: 7 attacks, 11 ranked weaknesses (1 FATAL, 3 near-fatal, 4 serious, 3 moderate); FATAL: Lorentzian signature structural incompatibility (positive-definite cost → Riemannian only); QM emergence is reformulation not derivation; continuum limit unproven (Gromov-Hausdorff); Pedraza only 2D; no unique predictions; overall verdict: valuable synthesis but not a theory
- **Updated** `gravitize-the-quantum/scg-theory-construction.md` — Status downgraded from "research program" to "fatally flawed in current form"; added Adversarial Assessment section with cross-reference and key findings
- **Updated** `gravitize-the-quantum/barandes-verlinde-stochastic-emergence.md` — Added adversarial findings section: isomorphism not derivation, Born rule definitional, phase dilemma, Aaronson critique, Nelson multi-time problem
- **Updated** `gravitize-the-quantum/nelson-stochastic-mechanics.md` — Added multi-time correlation problem (Blanchard et al. 1986): single-time OK but multi-time wrong; inherited by SCG
- **Updated** all INDEX.md files — gravitize-the-quantum (12 → 13 findings), root (137 → 138 findings)

## 2026-03-25

### Cost Function Ghost-Selection Negative Result

Processed exploration-004-cost-function-ghost-freedom.md (quantum-gravity-2 strategy-001). Investigation of whether Pedraza et al. spacetime complexity cost function constraints can select ghost-free higher-derivative gravity (QG+F). Clear negative result with four reasons.

- **Created** `cross-cutting/cost-function-ghost-selection-negative.md` — Pedraza framework, complexity=anything freedom, four reasons cost functions can't select QG+F (too much freedom, wrong inference direction, classical vs. quantum, IR vs. UV), Flory et al. 2026 positive-definiteness lead (incomplete), alternative holographic constraints (conformal collider bounds, Caron-Huot swampland)
- **Updated** `gravitize-the-quantum/scg-theory-construction.md` — Prediction #6 marked as BLOCKED; "Most promising next direction" updated with negative result and redirect to quantum cost function or entanglement-gravity bootstrap; added cross-reference
- **Updated** all INDEX.md files — cross-cutting (24 → 25 findings), root (136 → 137 findings)

### Three-Layer Time Synthesis: Construction and Stress Test

Processed exploration-005-synthesis-stress-test.md (nature-of-time strategy-001). Fifth report from the nature-of-time mission — combines all three time theses (entanglement, computational irreducibility, becoming) into a unified three-layer architecture, stress-tests it with four systematic attacks, and compares it to three alternative syntheses. Key achievement: resolves the kinematic/dynamic entanglement tension identified by exploration-004's adversarial assessment, via the computational irreducibility layer. Supported by computational deep thermalization research (PRL November 2025).

- **Created** `cross-cutting/three-layer-time-synthesis.md` — Full synthesis: three-layer architecture (static ontology + CI + becoming), layer connections, static/dynamic tension resolution via CI, weakness scorecard (7 fixed, 1 unfixed, 2 partial), five hardest questions answered with quality ratings, four attacks (circularity HIGH, factorization HIGH, unfalsifiability MEDIUM-HIGH, homunculus MEDIUM), four alternative syntheses compared (three-layer 28/40, relational 27/40, becoming-first 24/40, pure-computational 22/40), recommended hybrid development path, key references
- **Updated** `cross-cutting/time-from-entanglement-synthesis.md` — Added "The Three-Layer Synthesis" section with cross-reference and key results
- **Updated** `cross-cutting/computational-irreducibility-thesis.md` — Added "The Three-Layer Synthesis" section noting this thesis forms Layer 2 and resolves kinematic/dynamic tension
- **Updated** `cross-cutting/entanglement-thesis-adversarial-assessment.md` — Added "Subsequent Development" section noting proposed resolution of kinematic/dynamic incoherence via three-layer synthesis
- **Updated** all INDEX.md files — cross-cutting (23 → 24 findings), root (135 → 136 findings)

### SCG Theory Construction: Full Axiomatic Framework

Processed exploration-003-scg-theory-construction.md (quantum-gravity-2 strategy-001). Third report from the quantum-gravity-2 mission — constructs "Stochastic Computational Gravity" (SCG), a unified axiomatic framework that derives both QM and spacetime geometry from a stochastic computation on a finite configuration space with a cost function. Extends the earlier stochastic-spacetime-qm-synthesis pipeline into a concrete theory with five axioms, two derivation chains, two independent routes to Einstein equations, and six testable predictions.

- **Created** `gravitize-the-quantum/scg-theory-construction.md` — Full SCG construction: 5 axioms (configuration space, indivisible stochastic dynamics, cost function, optimization, irreducible noise), QM emergence via Barandes-Doukas lifting (ℏ = 2mσ²), geometry emergence from cost function continuum limit, two routes to Einstein equations (Pedraza cost optimization + Jacobson thermodynamic), Diósi-Penrose collapse from cost optimization, self-consistency fixed-point condition, 6 predictions (no graviton, spacetime diffusion, decoherence-diffusion trade-off, complexity plateau, modified dispersion, higher-derivative gravity with predicted coefficients), 3 circularities addressed, 7 honest gaps (dimensionality, Lorentzian signature, continuum limit, N, no SM, indivisibility, quantitative ℏ-G), comparison to 6 existing programs, assessment as research program
- **Updated** `gravitize-the-quantum/stochastic-spacetime-qm-synthesis.md` — Added "Axiomatic Development: SCG" section cross-referencing the full theory construction
- **Updated** `gravitize-the-quantum/barandes-verlinde-stochastic-emergence.md` — Added cross-reference to SCG as most developed application of Barandes-Doukas lifting
- **Updated** all INDEX.md files — gravitize-the-quantum (11 → 12 findings), root (134 → 135 findings)

### Adversarial Assessment of the Entanglement Thesis

Processed exploration-004-attack-entanglement-thesis.md (nature-of-time strategy-001). Fourth report from the nature-of-time mission — a systematic devil's advocate attack on the time-from-entanglement thesis (exploration-001). Five attack vectors (circularity, explanatory weakness, unfalsifiability, physics foundations, phenomenology) plus a novel kinematic/dynamic entanglement incoherence attack. Verdict: "wounded but viable" — thesis downgraded from explanation to reformulation/consistency.

- **Created** `cross-cutting/entanglement-thesis-adversarial-assessment.md` — Comprehensive adversarial review: ranked severity table (10 attacks, 2 VERY HIGH, 4 HIGH), novel kinematic vs. dynamic entanglement incoherence (PW static ≠ arrow dynamic), what survives (math sound, convergence real, entanglement necessary, parsimony), what collapses (derivation claim, "explains our time," arrow from entanglement, experimental support, universality), honest reassessment (reformulation not explanation), upgrade conditions
- **Updated** `cross-cutting/time-from-entanglement-synthesis.md` — Added "Adversarial Assessment" section with cross-reference, key downgrades, and what survives
- **Updated** `cross-cutting/page-wootters-mechanism.md` — Added Unruh-Wald (1989) objections, ideal clock assumption, conditional probability problem, interaction problem (expanded); changed "Experimental Confirmation" to "Experimental Illustration" with caveats; added adversarial assessment cross-reference
- **Updated** `cross-cutting/arrow-of-time-from-entanglement.md` — Added "Critical Caveat: Kinematic vs. Dynamic Entanglement Tension" section explaining that the arrow is not derivable from PW's static framework
- **Updated** all INDEX.md files — cross-cutting (22 → 23 findings), root (133 → 134 findings)

### Computational Irreducibility Thesis: Time as Computation

Processed exploration-003-computational-irreducibility-time.md (nature-of-time strategy-001). Third report from the nature-of-time mission — the **computational thesis** complementing the entanglement thesis (exploration-001) and becoming thesis (exploration-002). Comprehensive case that time is the computational irreducibility of the universe, grounded in the Landauer-Bennett-Bekenstein triad and Lloyd's universe-as-quantum-computer. Filed as one new cross-cutting finding, updated three existing entries with cross-references.

- **Created** `cross-cutting/computational-irreducibility-thesis.md` — Full computational thesis: Landauer-Bennett-Bekenstein triad (information is physical, reversible computation requires complete records, finite information density), Wolfram computational irreducibility and Principle of Computational Equivalence, Lloyd's universe-as-quantum-computer (10^120 operations, Margolus-Levitin bound), Wolfram Physics Project (strengths and criticisms), explanatory strengths (one-dimensionality as sequential computation, three-layer arrow via Landauer/Bennett/CI, future openness, time-complexity link via logical depth), seven difficulties (epistemic-ontological ambiguity, quantum non-sequentiality, time dilation mechanism gap, "now" problem, is-it-really-computation question, regress, initial conditions), three-thesis comparison table, key thinkers and historical lineage
- **Updated** `cross-cutting/time-from-entanglement-synthesis.md` — Added "The Competing View: Computational Irreducibility" section with key tension description
- **Updated** `cross-cutting/temporal-realism-irreducible-becoming.md` — Added cross-reference to computational thesis in Cross-References section
- **Updated** `cross-cutting/problem-of-time.md` — Added cross-reference to computational thesis (novel framing where frozen formalism dissolves because computation is inherently sequential)
- **Updated** all INDEX.md files — cross-cutting (21 → 22 findings), root (132 → 133 findings)

### Temporal Realism: The Case for Irreducible Becoming

Processed exploration-002-irreducible-time-becoming.md (nature-of-time strategy-001). Second report from the nature-of-time mission — the **counter-thesis** to the first report's time-from-entanglement synthesis. Comprehensive case for irreducible time/becoming drawing on Bergson, Whitehead, Prigogine, causal set theory, QM measurement, cosmological history, Smolin-Cortês temporal naturalism, Ellis evolving block, and Maudlin directed topology. Filed as one new cross-cutting finding, updated three existing entries with cross-references.

- **Created** `cross-cutting/temporal-realism-irreducible-becoming.md` — Full case for irreducible becoming: philosophical foundations (Bergson's durée vs. temps, Whitehead's process philosophy/actual occasions), physical arguments (Prigogine's fundamental irreversibility, CST sequential growth as becoming, QM collapse as genuine becoming, cosmological history), key programs (Smolin-Cortês temporal naturalism, Ellis evolving block, Maudlin Theory of Linear Structures), self-defeating eliminativism argument, explanatory strengths (flow, arrow, "now", time-space distinction), difficulties (relativity of simultaneity with three responses, mechanism problem, mathematical elegance, retrocausation)
- **Updated** `cross-cutting/problem-of-time.md` — Added cross-reference to temporal realism entry
- **Updated** `cross-cutting/time-from-entanglement-synthesis.md` — Added "The Competing View: Temporal Realism" section with cross-reference and key tension description
- **Updated** `cross-cutting/arrow-of-time-from-entanglement.md` — Added cross-reference noting Prigogine's alternative (dynamical irreversibility vs. entanglement growth)
- **Updated** all INDEX.md files — cross-cutting (20 → 21 findings), root (120 → 121 findings)

### Time from Entanglement: Page-Wootters, Arrow of Time, and Unified Thesis

Processed exploration-001-time-from-entanglement.md (nature-of-time strategy-001). First report from the nature-of-time mission. Comprehensive exploration of the thesis that time is emergent from quantum entanglement. Filed three new cross-cutting findings (Page-Wootters mechanism with full math and experimental confirmation, arrow of time from entanglement growth, unified time-from-entanglement synthesis), updated problem-of-time with cross-references, updated holographic-entanglement-spacetime with 2024-2025 de Sitter progress.

- **Created** `cross-cutting/page-wootters-mechanism.md` — Full Page-Wootters mechanism: mathematical formulation (|ψ_S(t)⟩ = ⟨t|_C |Ψ⟩), three critical assumptions, Moreva et al. 2014 experimental confirmation, Smith-Ahmadi 2019 interacting extension (time-nonlocal corrections), Giovannetti-Lloyd-Maccone 2015 (resolves Kuchar objections), Hoehn quantum reference frame program, open problems (clock ambiguity, factorization, Lorentz recovery)
- **Created** `cross-cutting/arrow-of-time-from-entanglement.md` — Entanglement growth as arrow of time mechanism: Linden-Popescu-Short-Winter 2009 (equilibration), Short-Farrelly 2012 (finite time), Lloyd (decoherence), Deutsch-Marletto + Scandolo-Chiribella (second law from QI), Past Hypothesis as low initial entanglement, advantage over classical thermodynamics
- **Created** `cross-cutting/time-from-entanglement-synthesis.md` — Unified thesis: WDW → PW → gravity-from-entanglement → arrow = "time IS entanglement viewed from inside"; what it explains (flow, irreversibility, arrow, observer question); 7 open problems (Lorentz recovery biggest gap, dS dependence, "now" problem, factorization, regress, time dilation derivation gap, cosmological initial condition); assessment: provisional confidence
- **Updated** `cross-cutting/problem-of-time.md` — Added cross-references to the three new entries
- **Updated** `emergent-gravity/entanglement-and-holography/holographic-entanglement-spacetime.md` — Added 2024-2025 de Sitter progress section (static patch holography, island formula extension, time from dS holography 2025, naive RT fails strong subadditivity in dS)
- **Updated** all INDEX.md files — cross-cutting (17 → 20 findings), root (117 → 120 findings)

### Agravity CC Analysis and Comprehensive Non-CMB Experimental Catalog

Processed exploration-013-agravity-CC.md and exploration-014-non-CMB-signatures.md (strategy-002). Agravity CC analysis: detailed CW mechanism for M_P, cascading transmutation explored and found to fail, old CC solved (unimodular) but new CC NOT solved. Non-CMB experimental catalog: systematic assessment of all 19 QG+F signatures outside CMB — every one undetectable. QG+F is effectively a one-prediction theory (r). First LVK ringdown constraints on quadratic gravity (2025). Microcausality non-propagation result (Anselmi & Marino 2020).

- **Created** `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` — Complete 19-signature catalog with detectability verdicts, quantitative suppression factors, priority ranking, "one-prediction theory" conclusion
- **Updated** `quadratic-gravity-fakeon/standard-model-and-agravity.md` — Added scalar field content, detailed CW mechanism for M_P (V_E formula, vacuum conditions, mass spectrum), f₂ AF as dynamical explanation for hierarchy; massively expanded CC section (tree Λ=0, one-loop 10⁸⁸ too large, Kugo theorem, Weinberg no-go, cascading transmutation explored and FAILS, Maggiore nonlocal gravity, three approaches with verdicts)
- **Updated** `quadratic-gravity-fakeon/microcausality-and-novel-signatures.md` — Added non-propagation result (Anselmi & Marino 2020: "universe conspires"), violation range (~10⁻²⁹ m), "missing resonance" signature distinct from "pair of bumps"; corrected experimental accessibility table (GQuEST not relevant, BMV not discriminating, GW ringdown 40 orders too weak)
- **Updated** `cross-cutting/cosmological-constant-problem.md` — Added QG+F/agravity-specific analysis section with cross-reference
- **Updated** `cross-cutting/experimental-constraints.md` — Added GQuEST irrelevance to QG+F, BMV non-discrimination, first LVK ringdown constraints (ℓ < 34-49 km, arXiv:2506.14695)
- **Updated** all INDEX.md files — quadratic-gravity-fakeon (12 → 13 findings), root (116 → 117 findings), updated descriptions

### Black Hole Predictions and Standard Model Connections

Processed exploration-011-BH-predictions.md and exploration-012-SM-connections.md (strategy-002). Comprehensive QG+F black hole catalog: fakeon selects Schwarzschild, no testable BH prediction for astrophysical BHs, Wald entropy resolved. SM connections: agravity program, f₂ AF for any matter, baryogenesis/leptogenesis, dark matter, strong CP, enhanced AS-GUT predictions, near-criticality.

- **Created** `quadratic-gravity-fakeon/black-hole-predictions.md` — Full BH catalog: Lü-Perkins-Pope-Stelle nonlinear solutions, Lichnerowicz theorem, 3 solution families, fakeon = Schwarzschild, singularity NOT resolved, spontaneous ghostification (Bonanno 2025), Wald entropy O(l_P²/r_H²), Hawking radiation = GR, QNMs (virtual massive spin-2), BH shadows exponentially suppressed, evaporation endpoint open, QG+F vs AS vs GR comparison, experimental prospects
- **Created** `quadratic-gravity-fakeon/standard-model-and-agravity.md` — SM coupling (f₂ AF for any matter, f₀ not AF), gauge group NOT predicted, TAF constraints, agravity program (Salvio-Strumia), hierarchy problem, fakeon collider phenomenology (peak uncertainty, fake inert doublet, muon g-2), baryogenesis via scalaron, DM connections, strong CP (indirect), SM near-criticality
- **Updated** `quadratic-gravity-fakeon/core-idea.md` — BH entropy question #4 partially resolved (Wald formula gives correct result)
- **Updated** `quadratic-gravity-fakeon/newtonian-potential-and-ir-recovery.md` — Validation scorecard: BH entropy ⚠️ Open → ✅ Pass (7/7 GR tests passed)
- **Updated** `quadratic-gravity-fakeon/microcausality-and-novel-signatures.md` — Added peak uncertainty (Anselmi 2022), enhanced collider phenomenology (fake doublet details, muon g-2), BH information leak cross-reference
- **Updated** `asymptotic-safety/standard-model.md` — Enhanced Shaposhnikov-Wetterich mechanism (A_λ anomalous dimension, boundary condition, robustness, QG+F connection), added AS grand unification (Eichhorn-Held: α_em calculable, predictive GUT quartics), SM near-criticality section
- **Updated** `cross-cutting/bekenstein-hawking-entropy.md` — Added QG+F Wald entropy result
- **Updated** `cross-cutting/information-paradox.md` — Added QG+F microcausality leak channel and spontaneous ghostification alternative
- **Updated** all INDEX.md files — quadratic-gravity-fakeon (10 → 12 findings), root (114 → 116 findings), updated descriptions for AS, cross-cutting

### IHO Ghost Assessment, Full CMB Catalog, AS vs QG+F Discrimination, Experimental Timeline

Processed exploration-010-IHO-CMB-predictions.md (strategy-002). Full assessment of the March 2026 IHO ghost paper, complete QG+F CMB predictions catalog (beyond n_s and r), systematic AS vs QG+F discrimination table, and experimental timeline including CMB-S4 cancellation.

- **Created** `quadratic-gravity-fakeon/iho-ghost-interpretation.md` — Full critical assessment: IHO mechanism, comparison to fakeon (competing not compatible), CMB anomaly connection (50-650× Bayes factor, not robust), unitarity argued not proven, verdict: interesting but not credible
- **Created** `cross-cutting/qgf-vs-as-cmb-discrimination.md` — Systematic discrimination table: r is sole realistic discriminator (QG+F < 0.005, AS up to 0.01); all other observables (α_s, n_T, f_NL) indistinguishable; discrimination windows; Bonanno-Platania AS framework
- **Created** `cross-cutting/cmb-experimental-timeline.md` — Full timeline: SO (3 SATs operational 2024), BICEP Array, LiteBIRD (launch 2032), CMB-S4 CANCELLED (July 2025), LISA, DECIGO; earliest discrimination ~2030, definitive ~2036-2037
- **Updated** `quadratic-gravity-fakeon/inflationary-predictions.md` — Added complete CMB predictions catalog: α_s, β_s, n_T, f_NL, isocurvature, spectral features, summary table; updated experiment table (CMB-S4 cancelled)
- **Updated** `cross-cutting/experimental-constraints.md` — CMB-S4 CANCELLED; expanded primordial GW section with SO, BICEP Array, LiteBIRD details
- **Updated** `cross-cutting/cmb-spectral-index-tension.md` — CMB-S4 cancelled; resolution timeline shifted to ~2034-2037
- **Updated** `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` — IHO section expanded with verdict and cross-reference
- **Updated** all INDEX.md files — quadratic-gravity-fakeon (9 → 10 findings), cross-cutting (14 → 17 findings), root (110 → 114 findings)

### Entanglement-Gravity Bootstrap: MVEH Constructively Explored → Produces QG+F

Processed exploration-009-entanglement-UV-construction.md (strategy-002). The MVEH axiom has now been used constructively to build a UV-complete theory. Result: uniquely produces QG+F through the self-consistency bootstrap. Novel insights: QG+F as unique entanglement-gravity fixed point, modular flow unitarity as independent argument for fakeon, linearization barrier for higher-derivative gravity.

- **Created** `cross-cutting/entanglement-gravity-bootstrap.md` — Full construction: UV divergence structure, Susskind-Uglum renormalization, entanglement-coupling Rosetta Stone, Nesterov-Solodukhin no-go, Bueno et al. extension, linearization barrier, 6-step self-consistency bootstrap, spectral dimension route, modular flow unitarity argument, fundamental obstacle to novelty
- **Updated** `cross-cutting/information-theoretic-constructive-axioms.md` — MVEH axiom marked as NOW EXPLORED (produces QG+F); added axiom #5 (modular flow unitarity); "What's Missing" replaced with "What's Been Explored and What Remains"
- **Updated** `emergent-gravity/thermodynamic-derivations/jacobson-entanglement-2015.md` — Added mathematical machinery (modular Hamiltonian formulas, first law of entanglement, area variation), structural features (5 key properties), what Jacobson does NOT address (4 gaps), cross-reference to bootstrap

### Six-Derivative Full Validation: d_s CORRECTED to 4/3, Tier 1-4 PASS

Processed exploration-008-six-derivative-validation.md (strategy-002). Full Tier 1-4 validation of the six-derivative QG+F extension. Major conflict resolved: spectral dimension corrected from d_s = 2 to d_s = 4/3. Comprehensive update with propagator pole analysis, Lee-Wick complex mass pairs, validation scorecards, and comparison table.

- **Overwrote** `quadratic-gravity-fakeon/six-derivative-extension.md` — [OLD: d_s = 4 -> 2 in UV] replaced with [NEW: d_s = 4 -> 4/3 in UV (from 1/p^6 propagator, z=3)]. Reason: The 1/p^6 propagator gives z=3 and d_s = D/z = 4/3, not 2. The old value incorrectly applied the QG+F (1/p^4) result. Added: full propagator analysis (14 DOF, mass eigenvalue formulas, alternating residues theorem), Lee-Wick complex mass pairs as preferred approach, super-renormalizability (one-loop only, not 1-3 loops), full Tier 1-4 validation tables, GR vs QG+F vs six-derivative comparison, novelty assessment, research status.

### Non-Perturbative QG+F: QCD Analogy, AS Black Holes, Bound States, CDT Phases

Processed exploration-007-nonperturbative-QGF.md (strategy-002). Major new content on the non-perturbative sector complementing perturbative QG+F: the QCD-gravity analogy and ghost confinement conjecture, Bonanno-Reuter black holes with singularity resolution, gravitational bound states, and CDT phase structure.

- **Created** `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` — Holdom-Ren (2015/2024) structural analogy, ghost confinement conjecture, fakeon as perturbative shadow, IHO interpretation (March 2026, arXiv:2603.07150), mass gap via Dyson-Schwinger (Jan 2025, arXiv:2501.16445), gravitational "hadrons", 7 breakdown points
- **Created** `asymptotic-safety/black-holes-and-singularity-resolution.md` — Bonanno-Reuter metric, singularity resolution via anti-screening (G->0), two-horizon structure, Planck-mass remnants (T->0), parameterized collapse (alpha>1 required), dark matter implications, comparison with perturbative QG+F
- **Created** `cross-cutting/gravitational-bound-states.md` — Graviballs (Guiot et al. 2020), Dvali-Gomez N-portrait (BEC of N gravitons), dark matter candidates, Hamber vacuum condensate (nu~1/3, xi~1/sqrt(Lambda)), gap in lattice evidence
- **Created** `cross-cutting/cdt-phase-diagram.md` — Three phases (A/branched polymer, B/crumpled, C/de Sitter) plus C_b; B-C second-order transition as UV continuum limit candidate; CDT-FRG comparison tension (2024); spectral dimension phase transition
- **Updated** `asymptotic-safety/cosmology.md` — Major expansion: inflaton-free inflation mechanism details, running G model (Bonanno 2024, epsilon_c encoding), vacuum condensate (Hamber lattice), power-law running G at cosmic scales, non-perturbative predictions table
- **Updated** `asymptotic-safety/swy-two-fixed-points.md` — Added "QG+F as perturbative sector of AS" hypothesis with supporting evidence from QCD analogy
- **Updated** `quadratic-gravity-fakeon/core-idea.md` — Open question #8 expanded with mass gap (arXiv:2501.16445), IHO interpretation (arXiv:2603.07150), cross-reference to qcd-analogy-ghost-confinement.md
- **Updated** all INDEX.md files — quadratic-gravity-fakeon (8 -> 9 findings), asymptotic-safety (11 -> 12 findings), cross-cutting (12 -> 14 findings), root (106 -> 112 findings)

## 2026-03-24

### Physical Beta Functions and Six-Derivative Extension: RG Running RULED OUT, R³ Wins

Processed exploration-005-ns-beta-functions-six-derivative.md (strategy-002). The "critical next calculation" from the previous report has been completed: RG running of R² gives Δn_s ~ 10⁻¹⁴, 12 orders of magnitude too small. Path 1 (RG running) is definitively ruled out. Path 2 (R³ correction from six-derivative extension) is now the definitive resolution. Major updates to resolution paths (priority reversal) and six-derivative extension (massively expanded with action inventory, predictions, naturalness analysis).

- **Created** `quadratic-gravity-fakeon/physical-beta-functions.md` — Branchina et al. PRL 2024 gauge-invariant beta functions vs. Fradkin-Tseytlin 1982; notation mapping (λ=f₂², ξ=−6/f₀²); coupling values during inflation (θ ≈ 1.8×10⁸, ξ ≈ −6.4×10⁸); separatrix structure (s₂: ξ ≈ −3.53λ enables AF + healthy Starobinsky); fakeon does not modify one-loop beta functions
- **Updated** `quadratic-gravity-fakeon/ns-tension-resolution-paths.md` — **MAJOR**: Path 1 (RG running) changed from "most natural, critical next calculation" to "RULED OUT (Δn_s ~ 10⁻¹⁴)"; Path 2 (R³) promoted to #1; added definitive calculation details (β_θ, two independent suppression reasons, three cross-checks); added comparison table of distinguishing predictions; added "What this means for QG+F" section; confidence upgraded to verified
- **Updated** `quadratic-gravity-fakeon/six-derivative-extension.md` — **MAJOR expansion**: added complete 17-term inventory of six-derivative invariants; reduction chain 17→10→3; super-renormalizability details (finite beyond 3 loops, 1/p⁶ propagator); fakeon requirement for complex conjugate mass pairs; modified slow-roll parameters (εᵥ, ηᵥ); naturalness comparison table (EFT vs. loop-generated vs. free parameter); tachyonic instability caveat; active research groups (~20+ papers 2024-2025); confidence upgraded to verified
- **Updated** `quadratic-gravity-fakeon/inflationary-predictions.md` — added definitive RG running result (Δn_s ~ 10⁻¹⁴) to running note
- **Updated** `cross-cutting/inflationary-model-selection-post-act.md` — corrected RG-improved Starobinsky entry (QG+F perturbative running negligible; requires AS non-perturbative effects or six-derivative R³); corrected UV completion exceptions list
- **Updated** all INDEX.md files — quadratic-gravity-fakeon (7 → 8 findings, added physical-beta-functions, updated descriptions for ruled-out RG running), root (105 → 106 findings, updated QG+F description)

### n_s Tension Analysis: New Observational Constraint on QG+F and Inflation

Processed exploration-004-ns-tension-analysis.md (strategy-002). Comprehensive analysis of the CMB spectral index tension (n_s = 0.974 ± 0.003 from ACT DR6 + DESI vs. QG+F/Starobinsky prediction of 0.967). Filed observational status, resolution paths for QG+F, six-derivative extension as fallback, and inflationary model selection landscape. Key finding: the fakeon (C² term) does NOT shift n_s — only the R² sector matters.

- **Created** `cross-cutting/cmb-spectral-index-tension.md` — full observational picture: ACT DR6, Planck PR4, SPT-3G D1, DESI combination, combined analyses table, systematic effects, inter-experiment tensions, EDE wild card, future experiments timeline
- **Created** `quadratic-gravity-fakeon/ns-tension-resolution-paths.md` — four resolution paths ranked by naturalness: (1) RG running of R² with γ ≈ 0.007, (2) R³ correction δ₃ ≈ −10⁻⁴, (3) matter radiative corrections, (4) high e-folds; includes Branchina et al. 2024 physical beta functions and the critical next calculation
- **Created** `quadratic-gravity-fakeon/six-derivative-extension.md` — super-renormalizable six-derivative gravity as QG+F extension; naturally includes R³; property comparison table; tier 1 checks
- **Created** `cross-cutting/inflationary-model-selection-post-act.md` — favored models (monomial φ^(2/3), RG-improved Starobinsky, R²+R³), disfavored models (pure Starobinsky, Higgs, standard α-attractors), UV completion challenge
- **Updated** `quadratic-gravity-fakeon/inflationary-predictions.md` — expanded from r-only to include full n_s analysis: Starobinsky refined formula, fakeon does NOT shift n_s (Anselmi-Bianchi-Piva 2020), tension significance, falsification criteria, cross-references to resolution paths
- **Updated** all INDEX.md files — quadratic-gravity-fakeon (5 → 7 findings, added n_s status note), cross-cutting (10 → 12 findings), root (101 → 105 findings)

### Lee-Wick QG Assessment: Major Corrections — CLOP Prescription Fails, Program Dead

Processed exploration-003-lee-wick-qg-assessment.md (strategy-002). **Major conflict resolution**: the existing `lee-wick-gravity/core-idea.md` claimed CLOP was ghost-free, LW was genuinely distinct from QG+F, and unitarity was "debated." The new report provides five independent lines of evidence that the CLOP prescription definitively FAILS (unitarity violation + Lorentz invariance breaking), and Modesto (the creator of LW QG) co-authored the 2025 paper concluding only the fakeon prescription is viable.

- **Overwrote** `lee-wick-gravity/core-idea.md` — [OLD: "Ghost-free via CLOP, genuinely distinct from QG+F, unitarity debated, 2nd most promising escape route"] replaced with [NEW: CLOP fails unitarity and Lorentz invariance; 4-deriv + fakeon = QG+F; 6-deriv + fakeon = super-renorm variant; not viable as independent program]. Reason: 5 independent evidence lines, including Modesto's own co-authored 2025 paper.
- **Created** `lee-wick-gravity/unitarity-resolution.md` — 5 evidence lines (Kubo-Kugo 2023, Anselmi 2022, Anselmi+Modesto 2025, Oda 2026, Buoninfante 2025), ghost confinement failure, research program trajectory 2015-2026, key researchers
- **Created** `lee-wick-gravity/prescription-comparison.md` — 4 prescriptions (by-the-book, LWN/CLOP, fakeon/AP, direct Minkowski), property comparison table, CLOP Lorentz violation mechanism, fakeon average continuation formula
- **Updated** `constraints/escape-routes-from-no-go.md` — Route 4 changed from "OPEN, high potential" to "CLOSED (collapses to QG+F)"; novel candidate #2 marked as ELIMINATED; cross-cutting insight #1 corrected
- **Updated** `constraints/structural/ghost-spectral-dimension-no-go.md` — Escape route (E) marked as CLOSED; theory table corrected
- **Updated** `constraints/INDEX.md` — escape-routes description corrected (Route 4 CLOSED, 3 surviving candidates)
- **Updated** `lee-wick-gravity/INDEX.md` — rewritten to reflect corrected status, now lists 3 findings
- **Updated** `factual/INDEX.md` — lee-wick-gravity description corrected, finding count 1 → 3, total 99 → 101

### Bianconi Entropic Action Assessment

Processed exploration-002-bianconi-entropic-action-assessment.md (strategy-002). Comprehensive critical assessment of Bianconi's "Gravity from entropy" (Phys. Rev. D 111, 066001, 2025). Verdict: NOT viable as quantum gravity theory — fails Tier 1 validation (entirely classical, ghost concerns from fourth-order equations, no UV completion, phenomenological construction). Filed detailed assessment, updated info-theoretic axioms entry to reflect completed scrutiny, added shared UV completion failure pattern to emergent gravity limitations.

- **Created** `emergent-gravity/bianconi-entropic-action.md` — full assessment: paper identity, mechanism, novelty (genuine in form but engineered output), Tier 1 FAIL table, Tier 2 partial, predictive claims (CC empty, DM speculative, inflation testable, BH entropy approximate), comparison table to all entropic programs, verdict MOVE ON
- **Updated** `cross-cutting/information-theoretic-constructive-axioms.md` — axiom #4 (Bianconi) updated from "not yet widely scrutinized" to detailed verdict with cross-reference to assessment
- **Updated** `emergent-gravity/criticisms-and-limitations/limitations-overview.md` — added "The Shared UV Completion Failure" section: all entropic programs (Jacobson/Verlinde/Padmanabhan/Bianconi) share the same failure mode
- **Updated** all INDEX.md files — emergent-gravity (added bianconi file, 17 → 18 findings), criticisms-and-limitations (updated limitations-overview description), root (98 → 99 findings)

### Escape Routes Survey: Two New Approaches, Info-Theoretic Axioms, and Meta-Analysis

Processed exploration-001-escape-routes-survey.md (strategy-002). Systematic survey of all 5 escape routes from the ghost/d_s=2 no-go theorem. Added 2 new approach folders (Horava-Lifshitz, Lee-Wick gravity), a new AS finding (SWY two fixed points), a new cross-cutting finding (information-theoretic constructive axioms), and the meta-survey itself.

- **Created** `constraints/escape-routes-from-no-go.md` — ranked survey of all 5 routes with verdicts, cross-cutting insights, and 4 novel theory candidates
- **Created** `horava-lifshitz/` folder with INDEX.md and `core-idea.md` — anisotropic scaling z=3, scalar mode problem, U(1) extension fix, LIV constraints, current status
- **Created** `lee-wick-gravity/` folder with INDEX.md and `core-idea.md` — meromorphic propagator loophole, CLOP prescription, super-renormalizability, distinction from QG+F, unitarity debate
- **Created** `asymptotic-safety/swy-two-fixed-points.md` — SWY 2022 two distinct fixed points, AS-QG+F SINGLETON risk, Swampland tension (Bonanno 2025)
- **Created** `cross-cutting/information-theoretic-constructive-axioms.md` — four info-theoretic axioms as alternative QG foundations: positivity of relative entropy, maximal vacuum entanglement, QFC, entropic action
- **Updated** `cross-cutting/spectral-dimension-running.md` — added non-universality analysis (CDT ~1.80, LQG 1 or 2, CST 2.38), multiple d_s definitions, physical consequences of d_s = 2 + epsilon
- **Updated** `constraints/theory-construction-implications.md` — added info-theoretic axioms to underexploited constraints list (#5), updated references
- **Updated** `constraints/structural/ghost-spectral-dimension-no-go.md` — cross-references to detailed escape routes survey and new approach folders
- **Updated** all INDEX.md files — root (92 → 98 findings, 9 → 11 categories), constraints, asymptotic-safety, cross-cutting, plus 2 new INDEX files

### Quadratic Gravity Fakeon: Validation, Predictions, and Research Program Status

Processed exploration-003-quadratic-gravity-fakeon-validation.md. Expanded the `quadratic-gravity-fakeon/` folder from 1 to 5 findings, covering research program status, IR recovery with the explicit Stelle potential, inflationary tensor-to-scalar ratio prediction, and microcausality/scattering signatures.

- **Created** `quadratic-gravity-fakeon/research-program-status.md` — Anselmi-Piva program milestones (2017-2026), 6 active research groups, computation status table, Quanta Magazine feature
- **Created** `quadratic-gravity-fakeon/newtonian-potential-and-ir-recovery.md` — Stelle potential, propagator 3-sector decomposition, r→0 singularity resolution, validation scorecard (6/7 GR tests passed)
- **Created** `quadratic-gravity-fakeon/inflationary-predictions.md` — tensor-to-scalar ratio 0.0004 ≲ r ≲ 0.0035, LiteBIRD/CMB-S4 testability
- **Created** `quadratic-gravity-fakeon/microcausality-and-novel-signatures.md` — microcausality violation details, "pair of bumps" scattering signature, experimental accessibility ranking
- **Updated** `quadratic-gravity-fakeon/core-idea.md` — expanded open questions from 7 to 10 (added spectral dimension gap, non-perturbative completion, unimodular extension)
- **Updated** `quadratic-gravity-fakeon/INDEX.md` — now lists all 5 findings
- **Updated** `factual/INDEX.md` — quadratic-gravity-fakeon count 1 → 5, total 88 → 92

### Spectral Dimension as Constructive Axiom — New Approach and Key Results

Processed exploration-002-spectral-dimension-constructive-axiom.md. Created new `quadratic-gravity-fakeon/` approach folder and filed key mathematical results about spectral dimension's power as a constructive tool.

- **Created** `cross-cutting/spectral-dimension-propagator-constraint.md` — mathematical derivation that d_s = 2 forces propagator ~ 1/p^4
- **Created** `constraints/structural/ghost-spectral-dimension-no-go.md` — no-go theorem: ghost freedom + Lorentz invariance incompatible with d_s = 2
- **Created** `quadratic-gravity-fakeon/` folder with INDEX.md and `core-idea.md` — Stelle action + Anselmi-Piva fakeon as new QG approach
- **Updated** `constraints/theory-construction-implications.md` — noted d_s = 2 axiom program has been carried out (was listed as "underexploited")
- **Updated** `cross-cutting/spectral-dimension-running.md` — added section on constructive use as axiom with cross-references
- **Updated** `factual/INDEX.md` — added quadratic-gravity-fakeon and bmeg (previously unlisted) to root index (81 → 88 total findings)

### New Category: Constraints on Viable Quantum Gravity Theories

Processed exploration-001-structural-recovery-constraints.md. Created new top-level `constraints/` folder with 14 findings organized into structural, recovery, and precision-bounds subcategories, plus two cross-cutting analysis files (constraint rankings/dependencies and theory construction implications).

- **Created** `constraints/` hierarchy with 3 subfolders, 4 INDEX files, and 14 finding files
- **Updated** `cross-cutting/holographic-principle.md` — added mathematical forms of entropy bounds (Bekenstein, spherical, Bousso) and the 2025 proof for higher-derivative theories
- **Updated** `cross-cutting/experimental-constraints.md` — added specific tensor-to-scalar ratio bound r < 0.036 (BICEP/Keck 2021) and LiteBIRD target
- **Updated** `factual/INDEX.md` — added constraints category (67 → 81 total findings)

## 2026-03-22

### Initial Organization of Factual Library

Processed ~79 research finding files from `factual/inbox/` into a 6-category hierarchical structure.

### Merges (duplicates combined into single authoritative files)

- **Merged** `asymptotic-safety-core-idea.md` + `asymptotic-safety-overview.md` into `asymptotic-safety/core-idea.md` -- both covered the same foundational material from the same source; combined version includes evidence from multiple frameworks
- **Merged** `asymptotic-safety-reuter-fixed-point.md` + `reuter-fixed-point.md` into `asymptotic-safety/reuter-fixed-point.md` -- one had fixed point values and critical exponents, the other had historical context; combined both
- **Merged** `asymptotic-safety-sm-compatibility.md` + `asymptotic-safety-standard-model.md` into `asymptotic-safety/standard-model.md` -- one focused on matter field bounds, the other on Higgs/top predictions; combined into comprehensive file
- **Merged** `string-ads-cft.md` + `string-theory-ads-cft.md` into `string-theory/ads-cft.md` -- one had technical detail ('t Hooft limit, AdS limitation), the other had accessible overview; combined
- **Merged** `string-black-hole-entropy.md` + `string-theory-black-hole-entropy.md` into `string-theory/black-hole-entropy.md` -- both covered Strominger-Vafa from same source with complementary details
- **Merged** `string-extra-dimensions.md` + `string-theory-extra-dimensions.md` into `string-theory/extra-dimensions.md` -- one had critical dimension derivation, the other had compactification details; combined
- **Merged** `string-graviton-mechanism.md` + `string-theory-graviton.md` into `string-theory/graviton-mechanism.md` -- complementary coverage of the same topic from different sources
- **Merged** `string-landscape-problem.md` + `string-theory-landscape-problem.md` into `string-theory/landscape-problem.md` -- one had KKLT and swampland detail, the other had accessible vacuum explanation; combined
- **Merged** `string-testable-predictions.md` + `string-theory-predictions.md` into `string-theory/predictions.md` -- one focused on swampland conjectures, the other on SUEP and cosmological tests; combined
- **Merged** `emergent-padmanabhan-equipartition.md` + `emergent-padmanabhan-thermodynamic-paradigm.md` into `emergent-gravity/thermodynamic-derivations/padmanabhan-program.md` -- same source, overlapping content with complementary emphasis
- **Merged** `emergent-lensing-test-brouwer-2017.md` + `emergent-dark-matter-claims-tests.md` into `emergent-gravity/verlinde-entropic-gravity/observational-tests.md` -- the lensing test was a subset of the broader observational tests file

### Overwrites (2026 updates replacing earlier versions)

- **Overwrote** `cross-cutting/bekenstein-hawking-entropy.md` with 2026 update -- added LQG LIGO-VIRGO-KAGRA verification, entanglement area law results, and Carlip CFT approach
- **Overwrote** `cross-cutting/cosmological-constant-problem.md` with 2026 update -- added running vacuum model, gravitized quantum theory (April 2025), spacetime foam mechanisms
- **Overwrote** `cross-cutting/experimental-constraints.md` with 2026 update -- added GQuEST experiment, unified spacetime fluctuation framework (Jan 2026), gravity-induced entanglement analysis
- **Overwrote** `cross-cutting/holographic-principle.md` with 2026 update -- added swampland constraints from holographic principles, Takayanagi 2025, Universal Holographic Principle beyond AdS/CFT
- **Overwrote** `cross-cutting/information-paradox.md` with 2026 update -- added island formula in asymptotic safety, LQG resolution via Sun Yat-sen group, remaining challenges
- **Overwrote** `cross-cutting/spectral-dimension-running.md` with 2026 update -- much more comprehensive: detailed evidence from 7+ approaches, common mechanisms, observational signatures

### Structure Created

```
factual/
  INDEX.md
  asymptotic-safety/     (10 files)
  causal-set-theory/     (15 files)
  loop-quantum-gravity/  (9 files)
  string-theory/         (8 files)
  emergent-gravity/      (17 files across 5 subfolders)
    thermodynamic-derivations/
    verlinde-entropic-gravity/
    entanglement-and-holography/
    analogue-gravity/
    criticisms-and-limitations/
  cross-cutting/         (8 files)
```

### Challenger Survey and Causal-Processual Interpretation (Exploration 001, nature-of-time strategy-002)

Processed exploration-001-challenger-survey-selection.md (nature-of-time strategy-002). Systematic comparison of five time interpretations; selection of causal-processual hybrid as strongest challenger to the computational interpretation.

- **Created** `cross-cutting/time-interpretation-challenger-survey.md` — Systematic six-feature scored comparison of five non-computational time interpretations (causal fundamentalism 35/40, thermodynamic realism 26/40, experience-first 30/40, causal-processual hybrid 36/40, Smolin 27/40); six-feature benchmark formalized; Husserl temporal phenomenology and IIT temporal structure assessments; retrocausal rejected (9/30), Rovellian rejected as CI-adjacent; selection rationale
- **Created** `cross-cutting/causal-processual-interpretation.md` — Selected challenger: synthesizes Maudlin/CST + Whitehead + Prigogine + Smolin; core claim (time is irreversible causal process of becoming); six-feature explanations; triple-grounded directionality without Past Hypothesis; five advantages over CI; five honest weaknesses (coherence, formalization, "now," flow, phenomenology gap); development roadmap (actualization as unifying principle, Baron-Le Bihan 2025)
- **Updated** `cross-cutting/temporal-realism-irreducible-becoming.md` — Added cross-references to survey and causal-processual hybrid
- **Updated** all INDEX.md files — cross-cutting (32 → 34 findings), root (154 → 156 findings)

### Causal-Processual Interpretation Full Construction (Exploration 002, nature-of-time strategy-002)

Processed exploration-002-causal-processual-construction.md. Deep construction of the Causal-Processual Interpretation: actualization as unifying principle, upgraded feature scores, perspectival "now" account, head-to-head CI comparison.

- **Updated** `cross-cutting/causal-processual-interpretation.md` — MAJOR UPGRADE: "Initial Sketch" → "Full Construction"; actualization as single unifying primitive (irreversible, creative, relational, constitutive of time); four-tradition mapping; Heisenberg potentia / Kastner-Kauffman 2017 quantum connection; irreversibility upgraded 4→5 (generalized second law, Baron-Le Bihan actual causation); flow upgraded 3→4 (Husserl retention-protention structure, Bergson durée, concrescence = specious present bridge); dilation upgraded 3→4 (CST chain-length-as-proper-time, hauptvermutung); new perspectival-processual "now" account; head-to-head CI comparison tables; convergence risk as new weakness; final formulation replacing development roadmap; total 23/30 → 26/30
- **Updated** `cross-cutting/time-interpretation-challenger-survey.md` — Revised D section scores (23→26), scoring matrix (irreversibility 4→5, flow 3→4, dilation 3→4), grand total (36→39)
- **Updated** all INDEX.md descriptions — cross-cutting and root INDEX updated to reflect full construction

### CI vs. CP Head-to-Head Tournament (Exploration 004, nature-of-time strategy-002)

Processed exploration-004-tournament-ci-vs-cp.md. Formal 13-criterion tournament: CP wins 48.5–47.5 (near-draw). CI advantages: physics grounding (+2.5), LBB engine (+1.0). CP advantages: directionality (+1.5), "now" (+1.5), explanatory depth (+1.0).

- **Created** `cross-cutting/ci-vs-cp-tournament.md` — Full tournament: 13-criterion scoring table, category subtotals, verdict (CP +1.0 near-draw), three reasons each side nearly wins, fundamental trade-off (safer/rigorous vs deeper/ambitious), convergence insight (both point to same irreversible-novelty-generating structure), key round highlights, four honest caveats, scoring methodology note
- **Updated** `cross-cutting/computational-irreducibility-thesis.md` — Added tournament results section: CI feature scores (21.5/30), strengths (physics grounding 5.0, LBB 4.5), weakness ("now" 2.5), convergence insight, cross-reference
- **Updated** `cross-cutting/causal-processual-interpretation.md` — Score history table expanded with E004 tournament column (22.5/30 features, 48.5/65 grand total), tournament methodology note, cross-reference
- **Updated** `cross-cutting/time-interpretation-challenger-survey.md` — Tournament result paragraph added under CP section
- **Updated** all INDEX.md files — cross-cutting (37 → 38 findings), root (159 → 160), descriptions updated

### Meta-Interpretation: Time as Irreversible Determination (Exploration 005, nature-of-time strategy-002)

Processed exploration-005-meta-interpretation-determination.md. CI+CP synthesis: "Time is irreversible determination." Scores 57.0/65 on same 13 criteria (+8.5 over best parent).

- **Created** `cross-cutting/meta-interpretation-determination.md` — Full CI+CP meta-interpretation: "determination" subsumes computation and actualization; potentialities-are-real fork resolution; three tension resolutions; 13-criterion score table (57.0/65); feature constructions (irreversibility 5.0, directionality 4.5, flow 4.0); 6 honest limits; self-critique; final statement
- **Updated** `cross-cutting/ci-vs-cp-tournament.md` — Added Synthesis Outcome section (57.0/65 result, complementary weakness structure) and cross-reference to meta-interpretation
- **Updated** `cross-cutting/computational-irreducibility-thesis.md` — Added cross-reference to meta-interpretation (CI subsumed as constraint-level description)
- **Updated** `cross-cutting/causal-processual-interpretation.md` — Added cross-reference to meta-interpretation (CP subsumed as ontological-level description)
- **Updated** `cross-cutting/three-layer-time-synthesis.md` — Added cross-reference to meta-interpretation as alternative Strategy 002 synthesis
- **Updated** all INDEX.md files — cross-cutting (38 → 39 findings), root (160 → 161), descriptions updated

## 2026-03-27 (SED strategy-002 exploration-006 adversarial review)

- **Overwrote (interpretation)** `factual/stochastic-electrodynamics/entanglement-bell-contested.md` — E002 Status block implied Bell S ≤ 2 contrasted SED with QM. E006 adversarial review showed this comparison is INVALID: two uncoupled QM oscillators in vacuum are SEPARABLE, so QM also gives S ≤ 2. The Bell S ≤ 2 result is a tautology, not a distinguishing finding. Corrected framing: the true distinction is C_xx oscillating (SED) vs C_xx=0 (QM). Status block updated with new ADVERSARIAL CORRECTION section. The numerical computation (S ≤ 2) itself stands. Reason: adversarial review found a logical error in the prior claim's interpretation.
