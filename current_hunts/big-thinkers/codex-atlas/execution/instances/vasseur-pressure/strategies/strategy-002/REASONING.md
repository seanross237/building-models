# Reasoning Log

## Direction Status Tracker

| Direction | Status | Evidence | Exploration |
|---|---|---|---|
| Phase 0: Decomposition Audit | SUCCEEDED | Single improvable step identified (Chebyshev) | 001 |
| Track A: Obstruction/universality (model PDEs) | OPEN | — | — |
| Track B: Chebyshev level-set improvement (analytical) | CLOSED (E003) | NOT independently improvable; flat optimization; circular with regularity problem | 003 |
| Track B: Chebyshev level-set improvement (computational) | CLOSED (E002) | Tightness ~3-5× but k-independent; no U_{k-1}^{-δ} scaling; ABC tight | 002 |
| Track A: Universality formula β = 1+s/n | SUCCEEDED (E003) | Confirmed across Burgers, 2D NS, SQG, MHD, fractional NS | 003 |
| Track B: Commutator / compensated compactness (Route 3) | CLOSED (E004) | 3 independent obstructions: no div-curl, div-error dominates, CRW no gain | 004 |
| Track B: Frequency-localized De Giorgi (LP decomposition) | CLOSED (E005) | 4 independent lines: spectral shift, growing I_hi, Bernstein penalty, analytical chain. CZ is optimal freq-by-freq. | 005 |
| Track B: Div-free truncation existence | OPEN | Likely impossible (topological); closing loophole would be clean | — |
| Track B: Non-CZ pressure handling | CLOSED (E006) | 3 routes: IBP gives β=1 (worse), H¹/BMO gives β=4/3 (same), CRW gives β≤1. Tool-independent. | 006 |
| Track B: Time-frequency analysis | OPEN | NEW from E005: modulation spaces / wave packets — very speculative | — |
| Track B: Wolf harmonic+particular decomposition | OPEN | NEW from E006: genuinely CZ-free, untested for β — speculative | — |
| Track B: Modified functional | CLOSED (Phase 0) | All free parameters optimized; 1/2 is definitional | 001 |
| Track B: Improved Sobolev (div-free) | CLOSED (Phase 0) | H¹→L⁶ sharp even for div-free; step is sharp | 001 |
| Track B: Optimized truncation | CLOSED (Phase 0) | Truncation shape irrelevant to β | 001 |
| Track B: Local Beltrami | OPEN | Not addressed by Phase 0 — still viable as conditional approach | — |
| Open question: div-free level-set | OPEN (publishable) | No paper addresses whether div(u)=0 improves |{|u|>λ}|; genuinely novel. Likely negative for pure div-free (toroidal counterexample); NS-specific version harder | 003, 007 |
| Phase 2: Adversarial review | SUCCEEDED | All 7 closures survive. 3 combination attacks fail. Claims 1-4 publishable. SDP formalization identified. | 007 |
| Track B: SDP Chebyshev sharpness formalization | SUCCEEDED (E008) | Chebyshev PROVABLY tight: constant field u=(c,0,0) achieves ratio→1. All 4 De Giorgi steps tight. β=4/3 SHARP. | 008 |

---

## Exploration 001: Phase 0 Decomposition Audit

### Options considered:
1. **Decomposition audit of Vasseur (2007) Prop 3** — line-by-line extraction of where 1/2 and 5/6 come from, sensitivity table, free parameters. This is prescribed by the strategy as Phase 0 and must happen first.
2. **Skip Phase 0, go straight to Track A/B attacks** — Risky. Strategy-001 already established the 1/2 + 5/6 decomposition at a high level, but we need the line-by-line detail to know WHERE to attack. Without this, Phase 1 explorations would be speculative.
3. **Start with a computational exploration testing modified functionals on DNS** — Tempting given the code infrastructure, but premature without knowing exactly which steps are improvable.

### Decision: Option 1 — Decomposition Audit
The strategy prescribes this as Phase 0, and the logic is sound. Strategy-001 established that β = 4/3 = 1/2 + 5/6, but at a conceptual level. We need the precise chain of inequalities in Vasseur (2007) Prop 3, step by step, to identify which steps have slack and which are sharp. This directly determines which Track B directions to prioritize.

**Explorer type:** Standard. This is a close reading of a mathematical paper — no computation needed. The output is an analytical map.

**Scope:** One proposition from one paper (Vasseur 2007, Prop 3). Clear, bounded, achievable. The explorer should also check whether Vasseur-Yang (2021) vorticity framework has an analogous decomposition.

### Library query:
Skipped (API error). Proceeding with context from Strategy-001 FINAL-REPORT and COMPUTATIONS-FOR-LATER.

### Reflection (post-exploration):

**Did the explorer deliver?** Yes — exceeded expectations. The goal asked for a sensitivity table and identification of improvable steps. The explorer produced a definitive answer: exactly ONE step (Chebyshev at the truncation level set) is potentially loose; all others are provably sharp. This dramatically narrows the attack surface.

**Was the scope right?** Perfect. One proposition from one paper, with cross-comparison. The explorer handled it in one run.

**What did I learn?** Phase 0 was essential and paid off immediately. Three of the five Track B directions I had listed (modified functional, improved Sobolev, optimized truncation) are now CLOSED — they can't help because the relevant proof steps are sharp. This saves 3+ explorations that would have been wasted.

**Impact on strategy:** Phase 1 is now sharply focused. The ENTIRE constructive attack reduces to one question: can the Chebyshev estimate |{v_{k-1} > 2^{-k}}| ≤ C^k U_{k-1}^{5/3} be improved for NS solutions? This is both the analytical question (does div-free + energy structure help?) and the computational question (what does DNS show?).

**Deviation from strategy budget:** Phase 0 completed in 1 exploration (strategy suggested 1-2). Moving to Phase 1 immediately. Reallocating saved budget to Phase 1 depth.

---

## Explorations 002-003: Phase 1 Parallel Launch — Chebyshev Attack + Model PDE Universality Test

### Options considered:
1. **Chebyshev level-set improvement (analytical) + DNS level-set measurement** — Two explorations attacking the single improvable step from both sides: theory and computation. High synergy.
2. **Track A universality test on model PDEs** — Apply De Giorgi to Burgers/SQG/MHD and check if the same Chebyshev step produces 4/3. If beta ≠ 4/3 on some PDE, the difference reveals which structural feature of NS makes Chebyshev tight.
3. **Local Beltrami conditioning** — Still open but Phase 0 didn't identify it as connected to the Chebyshev step. Lower priority now.
4. **DNS level-set measurement alone** — The computation from the report's "Computations identified" section.

### Decision: Launch 002 (math, DNS level-set measurement) and 003 (standard, analytical Chebyshev improvement + model PDE comparison) in parallel

**Rationale:** Phase 0 identified the Chebyshev step as the single target. Before spending budget on multiple analytical variations, I need TWO things simultaneously:
- **002 (math):** Does the Chebyshev bound actually have numerical slack on NS solutions? Compute |{|u| > λ}| vs λ^{-10/3} from DNS. This is the "compute, don't argue" check — if there's no slack on DNS, the analytical direction may still work (DNS is smooth) but we'd know the improvement is subtle.
- **003 (standard):** Can div-free structure or energy constraints analytically improve the Chebyshev estimate? Also: what happens to the Chebyshev step on model PDEs (Burgers 1D, SQG 2D)? This combines the Track A universality question WITH the Track B analytical attack, focused through the lens of the Chebyshev step.

I'm combining "Track A universality" and "Track B analytical Chebyshev" into one exploration (003) because Phase 0 revealed they're the SAME question: does the Chebyshev step have the same tightness across different quadratic PDEs? This isn't violating "one task per explorer" — it's one question (Chebyshev sharpness) tested on multiple PDEs.

**Explorer types:**
- 002: Math explorer (DNS computation, level-set measurement)
- 003: Standard explorer (literature analysis + analytical argument)

### Reflection on Exploration 003 (post-completion):

**Did the explorer deliver?** Exceeded expectations. All 4 tasks completed. The ranked route list is exactly what was needed. The universal formula β = 1 + s/n is a potential novel claim that emerged naturally from the model PDE comparison.

**Was the scope right?** Yes — combining "analytical Chebyshev improvement" with "model PDE comparison" in one exploration worked because E001 had already shown they're the same question. The explorer handled both coherently.

**What did I learn?** The single most important insight: **the 4/3 is NOT a proof artifact.** It faithfully encodes the integrability gap between H¹ and the Serrin threshold. This means:
- Direct Chebyshev improvement is circular with the regularity problem itself
- The remaining viable approach is changing HOW the nonlinear term couples (SQG precedent), not improving the distributional estimate
- The universal formula β = 1 + s/n is a clean characterization of when De Giorgi works

**Impact on strategy:** Massive pivot. The entire "improve the Chebyshev step" program (which Phase 0 identified as the single target) is now revealed to be equivalent to the regularity problem itself. We can't improve it without already having the answer. The remaining viable Track B direction is the **commutator / compensated compactness route** — changing how the pressure nonlinearity couples into the iteration, not improving the level-set estimate. This is Route 3 from E003's ranked list.

**Budget assessment:** 3 explorations used (001-003). E002 still running (DNS level-set). The strategy's Phase 1 budget of 3-5 explorations is being well-spent. Next: commutator exploration (004), then reassess after E002 completes.

---

## Exploration 004: Commutator / Compensated Compactness Analysis

### Options considered:
1. **Commutator estimate for P_{k21} via Hardy space** — E003's Route 3. The SQG precedent shows that when the nonlinear term enters as a commutator-like structure, the De Giorgi iteration gains an extra power. Can P_{k21}·div(uv_k/|u|) be reorganized to exploit compensated compactness (CLMS-type div-curl cancellation)?
2. **Wait for E002 results first** — E002 (DNS level-set measurement) is still running. Could inform whether Chebyshev has numerical slack. BUT: E003 already showed Chebyshev improvement is circular, so E002 is now more of a confirmation than a decision point. The commutator direction doesn't depend on E002.
3. **Local Beltrami conditioning** — Still open, but Phase 0/E003 shifted the landscape. The key insight is that the obstruction is in HOW the nonlinearity couples, not in the level-set estimate. Local Beltrami might help with coupling but is a separate direction.
4. **Pursue the β = 1 + s/n formula** — Clean up and formalize the universal formula. Publishable as a negative result / obstruction theorem. But this is synthesis work better suited for Phase 2.

### Decision: Option 1 — Commutator / compensated compactness (math explorer)

**Rationale:** E003 identified this as the single most promising remaining direction. The SQG success mechanism is concrete and analyzable: Caffarelli-Vasseur (2010) gains an extra power because the drift enters as a commutator [(-Δ)^{1/2}, u·] rather than a product. The NS nonlinear term P_{k21} involves a bilinear form of div-free fields — exactly the setting where CLMS compensated compactness gives Hardy space H¹ improvements over L^1.

**Explorer type:** Math. The key deliverable is a symbolic computation: write out the exact bilinear form of P_{k21}·div(uv_k/|u|), test whether it has the div-curl structure needed for CLMS, and if so, compute what improvement in the U-exponent results. This mixes analytical reasoning with verifiable symbolic/numerical checks.

**Why not wait for E002:** The commutator direction attacks the nonlinear COUPLING, not the level-set estimate. E002 measures level-set slack, which E003 already showed is circular. These are independent questions.

### Reflection on Exploration 004 (post-completion):

**Did the explorer deliver?** Exceeded expectations. All 4 tasks completed with 14 computed results and 2 checked. The three-layer obstruction argument is rigorous and definitive. The unexpected finding about the commutator part having good high-frequency behavior (but being negated by the div-error remainder) is genuinely insightful — it points precisely to WHERE the obstruction lives.

**Was the scope right?** Yes. The math explorer was the right choice — the symbolic computation of div(u^below) and the numerical verification of the compressibility ratio were essential. A standard explorer would have produced vague analytical arguments.

**What did I learn?** Route 3 is closed, but the closure is informative. The obstruction is NOT that compensated compactness is irrelevant — it's that **truncation breaks div-free**. The commutator part of P^{21} genuinely does have better regularity. The problem is the divergence-error remainder, which is a HIGH-FREQUENCY phenomenon. This directly motivates the frequency-localized direction: if you could treat low and high modes separately, the low modes would benefit from commutator structure.

**Impact on strategy:** The cumulative picture is now:
- 5 Track B directions CLOSED (modified functional, Sobolev, truncation, direct Chebyshev, commutator)
- 1 Track A direction SUCCEEDED (universality formula β = 1+s/n)
- β = 4/3 is sharp within energy+Sobolev+CZ+Chebyshev methods
- Remaining viable: frequency-localized De Giorgi (strongest lead from E004), local Beltrami, div-free truncation existence
- E002 (DNS level-set) still running

The strategy is converging toward a clean negative result: β = 4/3 cannot be improved by standard techniques. The frequency-localized direction is the last serious constructive avenue. After that, Phase 2 (adversarial review + synthesis) should produce a definitive report.

**Budget assessment:** 4 explorations completed (001, 003, 004) + E002 in progress. Budget used: ~4 of 8-14. Remaining budget: ~4-10. Plan:
- E005: Frequency-localized De Giorgi (the strongest remaining lead)
- E002: Process when complete (DNS confirmation)
- E006 or later: Local Beltrami conditioning (still open) OR adversarial review
- Final synthesis: 1-2 explorations

---

## Exploration 005: Frequency-Localized De Giorgi via Littlewood-Paley

### Options considered:
1. **Frequency-localized De Giorgi (LP decomposition)** — E004's strongest new lead. The divergence error concentrating at high frequencies means low-mode P^{21} has effective commutator structure. A LP decomposition treating low and high modes with different estimates could potentially beat 4/3 on the low modes while accepting 4/3 on the high modes. If the high-mode contribution is subdominant (decays with k), the overall recurrence could improve.
2. **Div-free truncation existence** — Likely impossible (topological argument about degree of u/|u| on level sets). Proving impossibility would be clean but doesn't advance the constructive attack. Lower priority.
3. **Local Beltrami conditioning** — Still open, but E004's findings suggest the frequency-localized direction is more concrete. Local Beltrami helps with the Lamb vector but doesn't address the frequency structure of the divergence error.
4. **Adversarial review now** — Premature. We haven't exhausted the constructive directions yet. The frequency-localized lead is concrete and testable.
5. **Wait for E002** — E002 is a DNS measurement that E003 already showed has limited interpretive value. Don't block on it.

### Decision: Option 1 — Frequency-localized De Giorgi

**Rationale:** This is the direct follow-up to E004's key finding. E004 showed that the commutator part of P^{21} HAS good high-frequency regularity (spectral ratio drops 0.67→0.09), but the divergence-error remainder negates it because it dominates at high frequencies. A frequency-localized approach would split the problem:
- Low modes: commutator structure applies → potentially better exponent
- High modes: standard CZ → 4/3 exponent, but contribution may be subdominant

This is mathematically concrete (Littlewood-Paley is well-established in fluid mechanics) and directly testable (both analytically and on DNS data).

**Explorer type:** Math. Needs both analytical Littlewood-Paley decomposition and numerical verification of the frequency splitting on DNS data.

### Reflection on Exploration 005 (post-completion):

**Did the explorer deliver?** Exceeded expectations. All 4 tasks completed. 8 computed results, 4 conjectured. The four independent lines of evidence make the negative result robust. The unexpected paraproduct transition finding is genuinely interesting.

**Was the scope right?** Perfect. The combination of analytical LP theory + numerical measurement was exactly right for this question. The math explorer handled the Bony paraproduct decomposition and the Bernstein cost computation cleanly.

**What did I learn?** CZ is not just "good enough" — it's OPTIMAL in the frequency-by-frequency sense. LP reveals the structure that CZ handles implicitly. This is a deeper understanding than "LP doesn't help." The Bernstein exchange rate is fixed by dimensional analysis (d=3 gives 2^{3j/5} per block), which means ANY frequency-localized approach in 3D will face this penalty.

The paraproduct transition is notable: at low k (close to the L^∞ threshold), same-frequency interactions dominate via the resonance term. At high k (deep in the iteration), the paraproduct T_{u^below}u^above dominates. This means the mathematical structure of the bottleneck changes character across the De Giorgi iteration. No single technique handles both regimes optimally — this may be why the 4/3 is so robust.

**Impact on strategy:** ALL standard analytical improvement routes are now CLOSED:
1. Modified energy functional (E001)
2. Improved Sobolev (E001)
3. Optimized truncation (E001)
4. Direct Chebyshev analytical (E003)
5. Direct Chebyshev computational (E002)
6. Commutator / compensated compactness (E004)
7. Frequency-localized LP (E005)

This is a comprehensive negative result. The remaining constructive directions (non-CZ pressure, local Beltrami, time-frequency) are increasingly speculative. I should transition to Phase 2: one more constructive probe (non-CZ pressure — the only genuinely new class of approach) + adversarial review + synthesis.

**Budget assessment:** 5 explorations complete (001-005). Budget: 5 of up to 20 used. Plan for remaining budget:
- E006: Non-CZ pressure handling (the last genuinely new constructive direction — bypasses CZ entirely)
- E007: Adversarial review of the comprehensive obstruction result + novel claims evaluation
- E008: Final synthesis and write-up
- Reserve 1-2 for follow-ups if adversarial review identifies gaps

---

## Explorations 006-007: Phase 2 — Last Constructive Probe + Adversarial Review (Parallel)

### Options considered:
1. **Non-CZ pressure handling + Adversarial review (parallel)** — E005 identified "bypass CZ entirely" as a genuinely new direction. All previous explorations accepted CZ as the tool for pressure and tried to improve other steps or the CZ application itself. Estimating the pressure contribution DIRECTLY through the Poisson equation is a different class of approach. Pair with adversarial review to transition to Phase 2.
2. **Local Beltrami conditioning** — Still open from original strategy, but Strategy-001 already found Beltrami conditioning doesn't generalize (β > 1 requires >98% Beltrami). Not promising.
3. **Div-free truncation existence proof** — Clean mathematical question but negative result is expected and doesn't advance the constructive attack.
4. **Time-frequency analysis** — Very speculative. Modulation spaces for NS pressure is uncharted territory. Low probability of payoff in one exploration.
5. **Skip to adversarial review + synthesis** — Could do this, but we'd miss the non-CZ direction, which is the one remaining approach that's genuinely different from everything tried.

### Decision: Launch E006 (non-CZ pressure, math) and E007 (adversarial review, standard) in parallel

**Rationale for E006:** Every exploration so far has accepted the CZ framework for handling pressure: bound P^{21} in some L^p space, then use that L^p bound in the De Giorgi iteration. The CZ bound is sharp (E001, E005). But what if we don't use CZ at all? The pressure satisfies Δp = -∂_i∂_j(u_iu_j). Direct energy estimates on this Poisson equation might produce a bound on ∫P·∇v_k that doesn't go through L^p of P. This is genuinely orthogonal to all previous approaches.

**Rationale for E007:** We've accumulated enough evidence for a comprehensive obstruction claim. An adversarial review should stress-test: (1) the "β = 4/3 sharp within standard tools" claim, (2) whether any published post-2007 result beats 4/3, (3) the novel claims (β = 1+s/n formula, SQG-NS gap, div-free level-set question), and (4) whether any COMBINATION of the closed routes could work.

**Explorer types:**
- E006: Math explorer (direct energy estimate computation + numerical test)
- E007: Standard explorer (literature survey + adversarial analysis)

### Reflection on Exploration 007 (post-completion):

**Did the explorer deliver?** Yes — thorough adversarial review. 15-paper literature search, all 7 closure arguments attacked, 3 combination attacks tested, all 5 novel claims evaluated with correctness/novelty/significance ratings. The Tao (2016) connection is a valuable unexpected finding.

**Was the scope right?** Good. The standard explorer handled the breadth well. The literature search was comprehensive (15 papers), the attacks were genuine, and the claim evaluations were specific.

**What did I learn?** Three things:
1. The obstruction is robust — no genuine weakness found in any closure argument, and no published improvement exists.
2. Claim 3 (seven-route obstruction) is the most significant novel result and could be formalized via SDP. This is actionable.
3. The adversarial reviewer flagged "non-CZ pressure handling incomplete" but we already completed it in E006. This is a context gap in the reviewer's information — the parallel launch meant E006 wasn't in the goal context.
4. Tao (2016) provides independent theoretical support: energy identity + harmonic analysis cannot resolve NS regularity. Our β = 4/3 barrier is an instance of Tao's broader supercritical obstruction.

**Impact on strategy:** The adversarial review confirms we're ready for finalization, with one actionable step remaining: the SDP formalization of Chebyshev sharpness. This would upgrade Claim 3 from "informal" to "rigorous" — the difference between a survey result and a theorem.

**Budget assessment:** 7 explorations complete (001-007). Budget: 7 of up to 20 used. Plan:
- E008: SDP formalization of Chebyshev sharpness (math explorer) — upgrades the strongest novel claim
- Then: write FINAL-REPORT.md myself

This is efficient: 8 explorations total, well within the 8-14 suggested budget. Early stopping is appropriate because:
- All constructive directions are closed (8 routes)
- Adversarial review confirms the obstruction
- One clear formalization step remains (SDP)
- The remaining open directions (time-frequency, Wolf, probabilistic) are speculative and unlikely to change the verdict

---

## Exploration 008: SDP Formalization of Chebyshev Sharpness Under NS Constraints

### Options considered:
1. **SDP formalization** — E007 identified this as the most actionable remaining step. Use semidefinite programming to bound |{|u|>λ}| under NS constraints (div-free, energy bound, Sobolev bound). If the SDP shows Chebyshev is tight even under these constraints, Claim 3 upgrades to rigorous.
2. **Wolf's local pressure decomposition** — E006 identified this as a remaining CZ-free direction. But E006 already established tool-independence, and Wolf's approach is unlikely to break it. Lower priority.
3. **Probabilistic regularization** — E007 identified this. Very speculative. The connection between noise and De Giorgi iteration is unclear.
4. **Final synthesis without SDP** — Could skip SDP and write the report with informal sharpness. But the SDP would be a significant quality improvement with modest effort (~100 lines CVXPY per E007's estimate).
5. **Tao (2016) connection exploration** — Understand how our β = 1+s/n relates to Tao's supercritical barrier. Valuable for framing but doesn't produce new results.

### Decision: Option 1 — SDP formalization

### Reflection on Exploration 008 (post-completion):

**Did the explorer deliver?** Exceeded expectations. The result is even cleaner than anticipated: instead of a complex SDP relaxation, the explorer found a one-line extremizer — the constant vector field u(x) = (c, 0, 0). This is simultaneously divergence-free, in H¹, and achieves the Chebyshev bound with ratio → 1 as λ → c⁻. The simplicity of the construction makes the result unassailable.

**Was the scope right?** Yes. The explorer correctly identified that the full SDP machinery wasn't needed — the pointwise dual + constant field construction resolves the question completely. The additional verifications (Fourier field survey, DNS comparison, truncation analysis) provide robustness.

**What did I learn?** The sharpness result is elementary once you look for it. The constant field is the simplest possible extremizer and it works because div-free doesn't constrain the MAGNITUDE of u, only its direction variation. This is the deep reason div-free can't help: the Chebyshev bound depends on ||u||_{L^p} which is a scalar quantity, and div-free constrains the vector structure.

**Impact on strategy:** This is the final piece. Combined with E001-E007, we now have:
- EIGHT routes to improving β tested and all closed (E001-E006)
- Adversarial review confirming all closures (E007)
- Rigorous sharpness proof for the Chebyshev step (E008)
- Universal formula β = 1+s/n (E003)
- Tool-independence of β = 4/3 (E006)

The strategy is COMPLETE. Time to write FINAL-REPORT.md.

**Rationale:** This is the single highest-value remaining action. The adversarial review (E007) identified Claim 3 (seven-route obstruction) as the most significant novel result AND identified SDP as the path to formalization. An SDP showing that under NS constraints (div-free + energy + Sobolev), the Chebyshev bound |{|u|>λ}| ≤ λ^{-10/3}||u||_{L^{10/3}}^{10/3} cannot be improved would transform our comprehensive-but-informal obstruction into a rigorous sharpness result.

**Explorer type:** Math. This is a computation: formulate the SDP, implement in CVXPY, solve, verify.

### Reflection on Exploration 006 (post-completion):

**Did the explorer deliver?** Yes — clean result with 12 computed claims. All three non-CZ routes computed explicitly with exponent analysis. The DNS comparison and literature survey add robustness. The "tool-independence" framing is the key insight.

**Was the scope right?** Perfect. The math explorer handled analytical route computation + DNS verification + literature survey coherently. The three routes are variations of one idea (bypass CZ), so combining them is appropriate.

**What did I learn?** The most important new insight: **β = 4/3 is tool-independent.** The CZ consolidation gain of 1/3 is exactly what H¹/BMO duality reproduces via a different mechanism. This means the 4/3 is locked to the NS quadratic structure itself, not to any particular analytical tool. This is stronger than "sharp within standard tools" — it's "invariant across tools."

The IBP route giving β = 1 (WORSE) is particularly informative: CZ consolidation is not just convenient, it's essential. Without it, you lose 1/3 of the exponent. This explains why CZ became standard in the first place.

**Impact on strategy:** 8 routes now closed. Combined with E003's β = 1+s/n and E006's tool-independence, the obstruction picture is nearly complete. E007 (adversarial review) will determine if any gaps remain. No new exploration launched — waiting for E007 before deciding on follow-ups vs final synthesis.

**Novel claim update:** The "tool-independence" result strengthens Claim 3 from an informal sharpness theorem to a near-theorem: β = 4/3 is not just sharp within one class of tools but invariant across IBP, CZ, H¹/BMO, and CRW approaches.

### Reflection on Exploration 002 (post-completion):

**Did the explorer deliver?** Yes — clean computational result. 7 DNS cases, resolution-checked, tightness ratios computed across k=1..10. The IC-dependent tail exponents (p ≈ 10 for TG vs p ≈ 2.1 for ABC) are interesting and the k-independence of tightness ratios is the key negative finding.

**Was the scope right?** Yes. One focused computation, well-scoped, using existing infrastructure.

**What did I learn?** E003 (analytical) already predicted this: Chebyshev improvement is circular with the regularity problem. E002 confirms numerically that the slack is constant (doesn't scale with U_{k-1}), which is exactly what "circular" means computationally. The analytical and numerical results are fully consistent.

The ABC result is notable: p ≈ 2.1 < 10/3 means Chebyshev is actually TIGHT (or even optimistic) for exact Beltrami flows in the tail. This is consistent with the known result that Beltrami flows have exponential mode concentration — heavy tails, not light tails.

**Impact on strategy:** Confirmation of E003's analytical verdict. The Chebyshev direction is now closed from both analytical and computational sides. No new directions opened. E005 (frequency-localized De Giorgi) remains the active exploration.

**Budget assessment:** 4 explorations complete (001-004), E005 in progress. Budget used: 5 of 8-14. Remaining: 3-9. After E005:
- If E005 finds improvement → lead pursuit + adversarial review (2-3 more)
- If E005 closes → only local Beltrami remains as constructive direction. Should then move to adversarial review + final synthesis (2-3 explorations). May also formalize the β = 1+s/n obstruction result.

