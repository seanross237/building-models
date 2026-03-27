# Curator Log

## 2026-03-27 Processing: exploration-001-balaban-rg-program.md (yang-mills strategy-001)

### Report Summary

Precision technical map of Balaban's 14-paper renormalization group program for lattice Yang-Mills theory in 4D. Paper-by-paper inventory across four phases, precise UV stability theorem statement, 12-step reconstruction chain toward the Millennium Problem, two-tier gap structure (4 specific gaps with mathematical formulations), and comprehensive survey of modern developments (Dimock, Chatterjee, Chandra-Hairer stochastic quantization, Faria da Veiga-O'Carroll, MRS, Charalambous-Gross, Federbush). 462 lines.

### Findings extracted:

- Balaban's UV stability theorem (14 papers, 4 phases, precise bound) → filed at `yang-mills/balaban-uv-stability.md` (NEW)
- Two-tier gap structure + 12-step chain + 4 gaps with formulations → filed at `yang-mills/gap-structure-overview.md` (NEW)
- Dimock's expository revisitation (2011-2022) + QED/NLSM extensions → filed at `yang-mills/dimock-expository-program.md` (NEW)
- Chatterjee's probabilistic program (2018-2024) + Wilson loops + trivial YMH limit → filed at `yang-mills/chatterjee-probabilistic-program.md` (NEW)
- Chandra-Hairer-Chevyrev-Shen stochastic quantization (2024) → filed at `yang-mills/stochastic-quantization-chandra-hairer.md` (NEW)
- Other modern approaches (Faria da Veiga, MRS, Charalambous-Gross, Federbush) → filed at `yang-mills/other-modern-approaches.md` (NEW)
- Completed gauge constructions (BFS, King, Gross/Driver) → filed at `yang-mills/completed-gauge-constructions.md` (NEW)

### Summary: Added 7 new entries (all new — no prior yang-mills content in library), updated 0 existing, skipped 0 duplicates, resolved 0 conflicts. Created new top-level `yang-mills/` folder.

---

## 2026-03-27 Processing: meta-exploration-001.md (yang-mills strategy-001)

### Report Summary

Meta-learning note from first yang-mills exploration. Lessons about naming authors, classification schemes, rigor-level specification, and technical mapping stall patterns.

### Findings extracted:

- "Specify rigor level (theorem-level precision)" → filed at `meta/goal-design/specify-rigor-level.md` (NEW)
- "Naming specific authors led to independent discovery of Dimock, Chandra-Hairer" → updated existing `meta/goal-design/name-specific-authors-and-papers.md` (added yang-mills evidence)
- "Classification scheme (COMPLETED/NOT ATTEMPTED) produced two-tier gap structure" → updated existing `meta/goal-design/use-classification-schemes.md` (added progress stratification use case)
- "Explorer needs web search time before writing for technical mapping" → updated existing `meta/system-behavior/explorer-stalling-and-nudge-pattern.md` (added technical mapping nuance)
- "Naming 5+ papers plus 'any others you find' is the right balance" → SKIPPED (already covered by `name-specific-authors-and-papers.md` — this is the exact same lesson with cumulative evidence)
- "Report at ~460 lines, upper end of target" → SKIPPED (already covered by `use-line-count-targets.md` — minor data point, no new insight)
- "Explorer went beyond named authors — good divergent behavior" → SKIPPED (folded into the name-specific-authors-and-papers.md update as evidence)

### Summary: Added 1 new entry, updated 3 existing, skipped 3 (duplicates/already covered).

---

## 2026-03-26 Processing: exploration-s4-007-complete-theory.md (quantum-gravity-2 strategy-004)

### Report Summary

Final consolidated theory document of the Atlas QG research program. A 451-line complete theory document presenting the Unified QG+F–AS Framework with: abstract, core insight for non-specialists, theory statement (action, two descriptions, QCD analogy, regime table, phase transition, 5 bridge mechanisms), evidence for/against (6 supporting, 3 unresolved, 3 against including QCD analogy breakdowns and H₀ null hypothesis), honest prediction catalog (4 tiers: inherited-QG+F, inherited-AS, novel-unconfirmed, promising-leads), three critical computations (C²-extended FRG propagator, g̃₃*→δ₃ mapping, AF→NGFP trajectory), comparison to alternatives, open problems, and conclusion.

### Findings extracted:

- **Post-adversarial overall assessment: "structural conjecture — organizational, not predictive"** → updated existing `cross-cutting/unified-qgf-as-framework/framework-conjecture.md` (MAJOR REVISION to Overall Assessment section). New framing: zero novel discriminating predictions survive adversarial scrutiny, H₀ is simpler and equally explanatory, QCD analogy breaks at 3 load-bearing joints, practically unfalsifiable on current timescales. Added "what would change this assessment" (3 conditions). Added comparison to alternatives. Cross-reference to mission validation.

- **Consolidated post-adversarial prediction survival table (11 predictions, pre/post status, testability)** → updated existing `cross-cutting/unified-qgf-as-framework/novel-predictions.md` (added survival table section). Key downgrades: P-UNI-1 ghost dissolution DISCRIMINATING→CONSISTENCY CHECK (circularity), P-UNI-2 BH phase transition NOVEL→DEAD (Planck-scale, self-undermined, analogy-dependent). Added b parameter cautionary tale for δ₃ lead. Bottom line: every testable prediction inherited from one standalone component.

- **Theory statement (action, two descriptions, QCD analogy, regime table, bridges)** → SKIPPED. Already comprehensively covered in existing `framework-conjecture.md` (created from earlier explorations).

- **Supporting evidence S1–S6** → SKIPPED. Already covered across `framework-conjecture.md`, `qgf-vs-as-cmb-discrimination.md`, `qgf-vs-as-bh-compatibility.md`, `qgf-vs-as-analyticity-compatibility.md`.

- **Evidence Against A1 (QCD analogy breaks at 3 joints)** → SKIPPED as standalone. Already in `open-problems.md` Section #2 "Where the QCD Analogy Breaks Down" and `qcd-analogy-ghost-confinement.md`. Added to framework-conjecture.md assessment.

- **Evidence Against A2 (H₀ null hypothesis scorecard)** → SKIPPED as standalone. Already comprehensively in `discriminating-predictions.md`. Referenced in framework-conjecture.md update.

- **Evidence Against A3 (practical unfalsifiability)** → SKIPPED as standalone. Already in `discriminating-predictions.md` ("falsifiable in principle but not within 5 years"). Captured in framework-conjecture.md update.

- **Three Critical Computations (detailed outcomes tables)** → SKIPPED as standalone update. Content is already distributed between `open-problems.md` (resolving calculations) and `discriminating-predictions.md` (outcome tables and amplitude equivalence test). The theory document's presentation is cleaner but adds no new factual content.

- **Comparison to alternatives (vs. String Theory, LQG)** → folded into `framework-conjecture.md` update (not standalone file — brief and generic, no deep findings).

- **Individual prediction details (P-QGF-1 through L2)** → SKIPPED. Each prediction already has its own detailed coverage in existing entries.

- **Key references appendix** → SKIPPED. References already captured in source lines of existing entries.

### Summary: Added 0 new entries, updated 2 existing entries (framework-conjecture MAJOR REVISION, novel-predictions added survival table), updated 4 INDEX files (unified-qgf-as-framework, cross-cutting, root × 2 edits), skipped 9 items (theory statement, supporting evidence, evidence against A1/A2/A3, three critical computations, comparison to alternatives, individual predictions, references — all already covered in existing library entries).

---

## 2026-03-26 Processing: exploration-s4-008-mission-validation.md (quantum-gravity-2 strategy-004)

### Report Summary

Formal 5-tier mission validation assessment of the Unified QG+F–AS Framework. Scores: Novelty MARGINAL (novel synthesis but not genuinely new theory — every equation borrowed), Logical Consistency PASS (strongest tier — survived by honest retreat), Explanatory Power MARGINAL (meta-theoretical not physical — explains formalism relationships not nature), Compatibility with Reality PASS (no contradictions, inherited predictions testable, but no prediction REQUIRES unification), Depth PASS (rich internal structure, honest edge cases, valuable open questions). Overall 3 PASS / 2 MARGINAL / 0 FAIL. Mission comparison: partially satisfies — falls short on "something genuinely new," "novel explanations," and "predictions that differ." Four-strategy retrospective arc. Three Strategy 005 options (compute, new angle, pivot). Honest bottom line: "sophisticated literature synthesis, empirically vacuous."

### Findings extracted:

- **Full 5-tier mission validation assessment (scorecard, mission comparison, 4-strategy arc, Strategy 005 options, honest bottom line)** → filed at `cross-cutting/unified-qgf-as-framework/mission-validation-assessment.md` (NEW). Core new content: formal tier-by-tier scoring with detailed justifications; mission goal comparison (4 shortfalls identified); four-strategy retrospective (S1: axiom-breaking → too ambitious; S2: QG+F gaps → point to AS; S3: unification conjecture → plausible but unproven; S4: prediction forge → all discriminating claims killed); three options for Strategy 005; honest bottom line.

- **Individual tier justifications (Novelty reasoning, "survived by retreat" insight, "meta-theoretical not physical" distinction)** → SKIPPED as standalone entries. Fully captured in the mission validation assessment entry.

- **4-strategy retrospective** → SKIPPED as standalone. Captured in mission validation assessment. This is program history, not a factual finding about QG.

- **Strategy 005 options** → SKIPPED as standalone. Strategic guidance, not factual finding. Captured in mission validation assessment.

### Summary: Added 1 new entry (mission-validation-assessment), updated 0 existing entries (INDEX updates were done during s4-007 processing), skipped 3 items (tier justifications, retrospective, strategy options — all captured in new entry).

---

## 2026-03-26 Processing: exploration-006-stress-test-synthesis.md (nature-of-time strategy-002)

### Report Summary

Five maximum-strength adversarial attacks on the "Time as Irreversible Determination" meta-interpretation (E005, originally 57.0/65). Attacks: (1) "determination" as synonym vs. primitive — PARTIALLY SURVIVED; (2) score inflation via max-function — WOUNDED; (3) "natural initial condition" = PH renamed — WOUNDED; (4) real potentialities dependency (every improvement traces to one commitment) — WOUNDED but survivable; (5) circularity / QRF-process tension — PARTIALLY SURVIVED. Revised score 52.5/65. Six mandatory modifications proposed. Structural insight: synthesis = "CI + ontological upgrade." CI-CP structural isomorphism identified as most important standalone discovery.

### Findings extracted:

- **Full adversarial stress-test (5 attacks, verdicts, revised score table, QRF-process tension, QM compatibility matrix, 6 mandatory modifications, final assessment)** → filed at `cross-cutting/meta-interpretation-stress-test.md` (NEW). Core new content: Attack-by-attack verdicts with best defense and wounds; revised 13-criterion score table (57.0→52.5, every criterion with change rationale); QRF-process tension as critical unresolved internal incoherence (2 repair options, process-primary recommended); QM compatibility matrix (compatible/incompatible/unclear); 6 mandatory modifications ranked by priority; "CI with ontological upgrade" architectural framing; most important discovery = CI-CP structural isomorphism (stands regardless of synthesis).

- **Score downgrade 57.0→52.5, revised score table, "determination" as bridging concept, QRF-process tension, QM compatibility, PH reframing downgraded, architecture reframed, expanded honest limits** → updated existing `cross-cutting/meta-interpretation-determination.md` (MAJOR REVISION). Score table now shows original + revised + change + notes. "Determination" section rewritten: bridging concept, not primitive. Tension 2 (PH) rewritten: honest about verbal nature. New QRF-Process Tension section. New QM Compatibility Matrix section. Honest limits expanded 6→8. Self-Critique replaced with Post-Stress-Test Assessment. Summary reframed with "CI + ontological upgrade" architecture and conditional scoring.

- **Synthesis outcome score revision (57.0→52.5), stress-test context** → updated existing `cross-cutting/ci-vs-cp-tournament.md` (Synthesis Outcome section rewritten, cross-reference added).

- **Cross-reference score update (57.0→52.5)** → updated existing `cross-cutting/three-layer-time-synthesis.md` (cross-reference updated, stress-test link added).

- **Landauer = possibility-extinguishing identification claim** → SKIPPED as standalone. Already captured comprehensively in the stress-test entry (Attack 1 defense) and the updated meta-interpretation's Determination section.

- **Camilleri's critique of Heisenberg's potentia** → SKIPPED as standalone. Mentioned in Attack 4 but as a secondary point within the broader real-potentialities dependency analysis. Captured in stress-test entry.

- **McTaggart parallel for processual circularity** → SKIPPED as standalone. Standard philosophical reference deployed within Attack 5; fully captured in stress-test entry.

- **Callender/Earman PH criticisms** → SKIPPED as standalone. Referenced in Attack 3 as contextual philosophy-of-physics literature; captured in stress-test entry's Attack 3 description.

- **Six mandatory modifications** → SKIPPED as standalone entries. These are repair recommendations, not factual findings. Fully captured in stress-test entry's Mandatory Modifications section.

- **Process-primary vs. QRF-primary options** → SKIPPED as standalone. These are proposed repair paths for the QRF-process tension, not independent findings. Captured in stress-test entry and in the meta-interpretation's new QRF-Process Tension section.

### Summary: Added 1 new entry (meta-interpretation-stress-test), updated 4 existing entries (meta-interpretation-determination MAJOR REVISION, ci-vs-cp-tournament, three-layer-time-synthesis, cross-cutting/INDEX), updated root INDEX (161→162), skipped 6 items (Landauer identification, Camilleri critique, McTaggart parallel, Callender/Earman, mandatory modifications, repair options — all captured within new/updated entries).

---

## 2026-03-26 Processing: exploration-003-adversarial-attack-cp.md (nature-of-time strategy-002)

### Report Summary

Four-dimensional adversarial attack on the Causal-Processual (CP) interpretation of time: (1) convergence with CI — near-total structural isomorphism but one clear fork (ontological potentia) saves CP; (2) physics vacuum — CP's physics content is thinner than packaging suggests (1 unconfirmed framework + 1 contested position + 3 philosophies); (3) block universe — causal-order Rietdijk-Putnam response is strong, deeper growth-vs-construction stalemate is inherent; (4) panexperientialism — full flow advantage requires panexperientialism, three-level framework proposed as repair. Overall verdict: "wounded but competitive," scores 26→25.

### Findings extracted:

- **Full adversarial assessment (4 attacks, verdicts, structural isomorphism table, three genuine forks, physics inventory, block universe defense, three-level flow framework, revised scores, repairs, meta-assessment)** → filed at `cross-cutting/cp-adversarial-assessment.md` (NEW). Core new content: 8-row CP-CI structural isomorphism table demonstrating near-total convergence; three genuine forks identified and ranked (potentia ontology STRONG, direction of explanation MODERATE, subject nature WEAK); component-by-component physics inventory with status table; Prigogine reception (Bricmont 1996, Drouet-Lippens 2025: "the rest of the profession versus Prigogine"); causal-order response to Rietdijk-Putnam (EXCELLENT — becoming structured by causal order, not simultaneity, dissolves the argument); growth-vs-construction genuine stalemate; three-level flow framework (minimal/moderate/panexperientialist); revised post-attack scores (26→25); five proposed repairs; honest meta-assessment.

- **Post-attack score revision (26→25), three-level flow framework, strengthened honest weaknesses, precise CP-CI forks** → updated existing `cross-cutting/causal-processual-interpretation.md` (significant revision). Flow section rewritten with three-level framework and score downgrade (4→3.5). Score history table expanded to include E003 post-attack column. Honest weaknesses section completely reorganized around attack results (5 weaknesses rewritten with attack numbers and verdicts). Cross-reference to adversarial assessment added.

- **Post-attack grand total revision (39→38), updated feature/meta scores** → updated existing `cross-cutting/time-interpretation-challenger-survey.md` (added post-attack scores). Feature total 26→25, meta scores adjusted (vulnerability increased, novelty decreased). Cross-reference to adversarial assessment added.

- **Swerves observational constraint k ≤ 10⁻⁵⁶ kg²m²s⁻³, cosmic ray swerves ruled out** → updated existing `causal-set-theory/swerves-phenomenology.md` (added quantitative constraint). Previously had only qualitative statement ("extremely small, challenging with current technology"); now has specific bound from spontaneous heating bounds on hydrogen gas, and explicit statement that cosmic ray attribution is ruled out.

- **CP-CI detailed structural isomorphism (8-row mapping table)** → SKIPPED as standalone entry. Captured comprehensively in the new adversarial assessment file. Not a standalone finding — it's an analytical tool within the adversarial attack.

- **Rietdijk-Putnam dissolution via causal order** → SKIPPED as standalone entry. This is an argument within the block universe attack, not a standalone finding. The key insight (becoming structured by causal order, not simultaneity) is captured in the adversarial assessment's Attack 3 section.

- **Baron & Le Bihan (2025) actual causation strengthens growth-is-not-gauge argument** → SKIPPED. Already cited in existing `causal-processual-interpretation.md` (E002). The adversarial assessment adds context (how it's deployed in the growth-vs-construction debate) but no new factual content.

- **Prigogine reception details (Bricmont 1996, Drouet-Lippens 2025)** → SKIPPED as standalone entry. Captured in adversarial assessment's Attack 2 and in updated CP interpretation's honest weakness #1. Not enough standalone value for a separate entry.

- **Three-level flow framework (Level 1-3)** → SKIPPED as standalone entry. This is a repair strategy, not a factual finding. Fully captured in both the adversarial assessment and the updated CP interpretation flow section.

- **Revised post-attack formulation of CP** → SKIPPED as standalone entry. Captured in the adversarial assessment's Repairs section and the updated CP interpretation.

- **CP's directionality advantage survived all attacks, confirmed as strongest feature** → SKIPPED. Already stated in E002; the adversarial assessment confirms without adding new content.

- **CST swerves parameter bound (k ≤ 10⁻⁵⁶)** → Updated existing `causal-set-theory/swerves-phenomenology.md` (see above). Not a new entry — quantitative detail added to existing entry.

### Summary: Added 1 new entry (cp-adversarial-assessment), updated 3 existing entries (causal-processual-interpretation with major revision, time-interpretation-challenger-survey with post-attack scores, swerves-phenomenology with quantitative constraint), updated all INDEX files (3 levels: cross-cutting 35→36, root 157→158), skipped 7 findings (structural isomorphism table, Rietdijk-Putnam argument, Baron & Le Bihan, Prigogine reception, three-level framework, revised formulation, directionality confirmation — all captured within new/updated entries).

---

## 2026-03-26 Processing: exploration-s4-002-bh-phase-transition.md (quantum-gravity-2 strategy-004)

### Report Summary

Quantitative predictions for the BH evaporation phase transition in the unified QG+F–AS framework. Derives M_crit from combining Bonanno et al. instability threshold (r_H ≈ 0.876/m₂) with Benedetti et al. NGFP ghost mass (m₂/k ≈ 1.42). Covers: critical mass, transition temperature, transition order via QCD analogy (first-order pure gravity / crossover with SM), gravitational Polyakov loop analog, latent heat estimate, M_rem vs M_crit ordering and implications, heat capacity signature, PBH dark matter constraints, observability assessment, 12-prediction classification table, and honest assessment. Key meta-finding: 7 of 12 BH predictions are inherited from AS alone; novelty is real but narrow.

### Findings extracted:

- **Quantitative BH phase transition predictions (M_crit, T_crit, convention uncertainty, transition order, M_rem vs M_crit ordering, latent heat, classification table, observability, honest assessment)** → filed at `cross-cutting/unified-qgf-as-framework/bh-phase-transition-predictions.md` (NEW). Core new content: M_crit = 0.308 M_P (or 1.55 M_P — convention dependence is largest systematic); T_crit = 0.03–0.13 M_P; transition order prediction unique to unified framework (first-order pure gravity via CDT + QCD, crossover with SM by flavor analogy); gravitational Polyakov loop concept; latent heat ~7 kJ; M_rem vs M_crit ordering determines whether ghost trigger is operative or preempted; 12-prediction classification (6 NOVEL, 5 INHERITED, 1 DISCRIMINATING); honest verdict: "AS predictions dressed up with ghost confinement trigger."

- **BH evaporation phase transition (prediction #3) — specific M_crit, convention uncertainty, transition order, honest caveat** → updated existing `cross-cutting/unified-qgf-as-framework/novel-predictions.md` (significant expansion of prediction #3). Previously had only qualitative description ("M ~ 0.876 M_P/m_2"); now has specific numerical M_crit for both conventions, transition order prediction, M_rem vs M_crit ordering implications, sharpened PBH DM statement (γ-ray constraints rule out all-DM), honest caveat (7/12 inherited from AS), and cross-reference to detailed entry.

- **PBH remnant DM: γ-ray constraints → can't be all of dark matter** → updated existing `asymptotic-safety/black-holes-and-singularity-resolution.md` (CORRECTED). Previously said "Remnants could dominate dark matter density if enough primordial BHs formed." Now corrected: γ-ray constraints (β < 10⁻²⁵) are 7 orders of magnitude tighter than needed for all-DM (β ~ 10⁻¹⁸); added specific remnant properties (M, charge, T, σ, S); added very-light-PBH caveat.

- **QCD deconfinement lattice data (pure SU(3) first-order at 270 MeV, physical quarks crossover at 156.5 MeV, critical endpoint, latent heat values)** → SKIPPED as standalone entry. Technical background used to justify the transition order prediction; captured adequately within the new bh-phase-transition-predictions.md entry's transition order section. These are well-established QCD results, not QG findings.

- **Heat capacity sign change and divergence (C: −∞ → +∞ → 0⁺, burst then cooling)** → SKIPPED as standalone entry. Classified as INHERITED from AS in the report. The qualitative behavior is already noted in `black-holes-and-singularity-resolution.md` ("Modified thermodynamics"). The specific pattern is captured in the new entry's heat capacity section. Not enough standalone value.

- **Remnant mass M_rem ≈ 0.46 M_P, T → 0, O(1) entropy** → SKIPPED. Already covered in `black-holes-and-singularity-resolution.md` ("Planckian remnant" and "T -> 0"). Remnant entropy (S ~ π ≈ 3) is new but too minor for a standalone entry; captured in new entry and in updated AS BH entry (remnant properties).

- **PBH evaporation time calculation and abundance analysis** → SKIPPED. Standard physics (Hawking evaporation time formula). The conclusion (γ-ray constraints rule out all-DM) is captured in the AS BH update.

- **Observable signatures table (7 predictions assessed)** → SKIPPED as standalone entry. Useful synthesis but no new information — individual observability assessments already noted across existing entries. Captured in the new entry's observability section.

- **Ghost confinement trigger as sole DISCRIMINATING prediction (#12)** → SKIPPED. Already captured in `discriminating-predictions.md` (ghost dissolution = "ONE genuine discriminator"). The report confirms this without adding new content.

- **Sharpened M_rem under unification (M_rem(g*, 1.42) constraint)** → SKIPPED as standalone entry. Classified as CONSISTENCY CHECK in the report. The constraint (m₂/k = 1.42 fixed → reduces from 2 parameters to 1) narrows M_rem to 0.3–0.7 M_P; captured in new entry.

- **QCD comparison table (T_c ratios)** → SKIPPED. Contextual detail supporting the QCD analogy; captured in new entry.

### Summary: Added 1 new entry (bh-phase-transition-predictions), updated 2 existing entries (novel-predictions #3, black-holes-and-singularity-resolution PBH DM correction), updated all INDEX files (4 levels: unified-framework 5→6, cross-cutting 34→35, root 156→157), skipped 8 findings (inherited from AS, technical background, or already covered), resolved 1 correction (PBH DM "could dominate" → "cannot be all").

---

## 2026-03-26 Processing: exploration-s4-001-ghost-propagator-specification.md (quantum-gravity-2 strategy-004)

### Report Summary

Detailed derivation of the ghost propagator prediction for the unified QG+F–AS framework. Covers: Benedetti et al. 2009 NGFP fixed-point values, ghost mass at NGFP (m₂/k ≈ 1.42), Draper et al. 2020 complex pole tower structure with form factor and pole formulas, ghost mass formula and BH instability scale, predicted pole migration pattern, computational specification for C²-extended FRG, classification as partially discriminating/novel, and honest assessment.

### Findings extracted:

- **Quantitative ghost propagator prediction (pole migration pattern, mathematical form, transition scale, amplitude equivalence test, honest assessment)** → filed at `cross-cutting/unified-qgf-as-framework/ghost-propagator-prediction.md` (NEW). Core new content: the specific predicted form of how the ghost pole dissolves — real pole at p²=-m₂² splits into complex conjugate pairs migrating to imaginary p², building infinite tower; tanh form factor interpolation between IR (Stelle) and UV (complex tower); transition scale ~2M̄_P²; the amplitude equivalence test (fakeon amplitudes = complex-pole-tower amplitudes) as the single sharpest discriminating criterion; honest verdict: "consistency check, not sharp prediction"; 5-step FRG computational specification with available parameters; three blocking unknowns (c_C, trajectory, form factor).

- **Benedetti et al. 2009 specific numerical NGFP values (g₀*–g₃*, critical exponents, universal product) and derived ghost mass ratio m₂/k ≈ 1.42** → updated existing `asymptotic-safety/ghost-fate-strong-coupling.md` (added quantitative detail). Previously had qualitative statement only ("higher-derivative couplings are finite and non-zero"); now has the specific numerical table plus derived ghost mass ratio and explicit statement that mass-divergence is structurally excluded.

- **Amplitude equivalence test as sharpest criterion + honest assessment** → updated existing `cross-cutting/unified-qgf-as-framework/discriminating-predictions.md` (added nuance). Previously described ghost dissolution as "STRONG" discriminator; now clarifies that the real test is amplitude equivalence, not mere pole dissolution, and adds honest assessment.

- **BH instability scale r_H ≈ 0.63 l_P** → updated existing `quadratic-gravity-fakeon/black-hole-predictions.md` (added specific numerical value). Previously had formula r_H^cross ≈ 0.876/m₂ without plugging in m₂; now has explicit sub-Planckian value.

- **Benedetti et al. 2009 action ansatz and coupling definitions** → SKIPPED (technical detail, captured adequately in the new entry and the ghost-fate update)

- **Draper et al. 2020 form factor parametrization and pole positions** → SKIPPED as standalone entry. Already qualitatively covered in `ghost-fate-strong-coupling.md` Mechanism 4. Quantitative details (tanh form, pole formula, partial wave results, unitarity bounds) captured in the new ghost-propagator-prediction entry.

- **Ghost mass formula m₂² = u₁/u₃ and physical mass range** → SKIPPED as standalone entry. Captured in the new entry. The formula and its implications are adequately covered.

- **Why residue vanishing is unlikely for spin-2** → SKIPPED as standalone entry. Already qualitatively covered in `ghost-fate-strong-coupling.md` Mechanism 3. The additional argument (finite coupling works against vanishing) is captured in the new entry.

- **Computational specification (5-step FRG program)** → SKIPPED as standalone entry. More detailed than what was in `discriminating-predictions.md` and `open-problems.md`, but captured in the new entry. Not enough standalone value for a separate file.

- **Classification as partially discriminating + novel** → SKIPPED. Already fully covered by `discriminating-predictions.md`. The report's classification table adds no content beyond what was already captured.

- **Key limitation of Draper et al. (EH truncation, tanh is ansatz)** → SKIPPED. Already noted in `ghost-fate-strong-coupling.md` ("General truncation, not Stelle ghost specifically") and captured in the new entry's "Three Unknowns" section.

- **Knorr-Saueressig 2022 parameters** → SKIPPED. Already referenced in `discriminating-predictions.md` and `graviton-propagator.md`. Captured in new entry.

- **Source references survey** → SKIPPED. All sources already in library. No new papers identified.

### Summary: Added 1 new entry (ghost-propagator-prediction), updated 3 existing entries (ghost-fate-strong-coupling, discriminating-predictions, black-hole-predictions), updated all INDEX files (3 levels), skipped 9 findings already covered or captured in new entry, resolved 0 conflicts.

---

## 2026-03-26 Processing: exploration-009-discriminating-predictions.md (quantum-gravity-2 strategy-003)

### Report Summary

Systematic search for predictions that discriminate the unified QG+F–AS framework from: (1) standalone QG+F or AS, and (2) the "compatible-but-separate" null hypothesis. Covers: the spin-2 ghost propagator computation as the key discriminator, the b parameter from NGFP, fakeon average continuation applied to FRG, near-term experimental prospects (none before 2030), the null hypothesis H₀ with explicit predictions, and an overall falsifiability verdict.

### Findings extracted:

- **Null hypothesis H₀ + three discriminators + falsifiability verdict + near-term experimental assessment** → filed at `cross-cutting/unified-qgf-as-framework/discriminating-predictions.md` (NEW). The core new contribution: formal H₀ ("compatible-but-separate") with explicit differing predictions; three discriminators ranked (A: ghost dissolution STRONG, B: average continuation MODERATE, C: coupling unification WEAK); "Only Discriminator A is genuinely novel to unification"; near-term assessment (NO discriminating experimental prediction before 2030); verdict: "falsifiable in principle but not in practice within 5 years"; computational roadmap for the ghost propagator calculation.

- **Knorr & Saueressig (2022) spectral reconstruction** → updated existing `asymptotic-safety/ghost-fate-strong-coupling.md` (added new subsection). New reference: background graviton spectral function has negative parts, dynamical graviton positive; Einstein-Hilbert truncation only (no C²). This is the closest existing computation to what the unified framework needs but doesn't include the Stelle ghost term.

- **Baldazzi et al. 2025 Foliated AS result** → updated existing `cross-cutting/unified-qgf-as-framework/novel-predictions.md` prediction #1 (added caveat). Key finding: Lorentzian two-point function has causal structure of **Feynman propagator** (not fakeon), which means the average continuation prediction may be rendered moot if Lorentzian AS works independently. Reference already in `qgf-vs-as-analyticity-compatibility.md` but the "rendered moot" implication for the prediction was not captured.

- **Critical exponent values for b parameter** → updated existing `cross-cutting/unified-qgf-as-framework/novel-predictions.md` prediction #4 (added specificity). New: b ~ θ/(16π²) ~ O(10⁻²); θ₁,₂ = 1.48 ± 3.04i (EH), θ₁ = 2.38 (R²); precise relation not yet derived from first principles.

- **Discrimination feasibility for ghost propagator** → updated existing `cross-cutting/unified-qgf-as-framework/open-problems.md` #2 (added feasibility estimate and cross-reference).

- **Ghost propagator literature survey (Section 1 details)** → SKIPPED as standalone entries. Draper et al. 2020 already in `ghost-fate-strong-coupling.md`. Platania-Wetterich 2020 already there. Antoniou et al. 2024 QNM paper already covered in `quadratic-gravity-fakeon/black-hole-predictions.md` (as "Tattersall & Silveravalle" — **NOTE: possible author attribution discrepancy for arXiv:2412.15037**, report says Antoniou-Gualtieri-Pani, library says Tattersall-Silveravalle; same arXiv number). All captured in the new discriminating-predictions entry.

- **b parameter general discussion (Section 2)** → SKIPPED as standalone. Already covered by `novel-predictions.md` prediction #4 (updated with new specificity). The "WEAKLY DISCRIMINATING" assessment is captured in the discriminating-predictions entry.

- **Fakeon average continuation applied to FRG (Section 3)** → SKIPPED as standalone. Already covered by `novel-predictions.md` prediction #1 (updated with caveat) and `qgf-vs-as-analyticity-compatibility.md`. D'Angelo et al. 2024 already referenced in analyticity entry. Captured in discriminating-predictions entry.

- **Near-term QNM suppression prediction** → SKIPPED as standalone. Both unified and standalone QG+F agree massive spin-2 QNMs are unobservable (mass ~ M_P). Captured in discriminating-predictions entry.

- **CMB σ(r) ~ 0.003 at detection threshold** → SKIPPED. Already in `experimental-constraints.md` and `cmb-experimental-timeline.md`.

- **LIGO O4/O5 corrections suppressed by 10⁻⁷⁶** → SKIPPED. Already in `quadratic-gravity-fakeon/black-hole-predictions.md`.

- **n_s tension resolution paths** → SKIPPED. Already covered in `novel-predictions.md` prediction #4, `cmb-spectral-index-tension.md`, and `quadratic-gravity-fakeon/ns-tension-resolution-paths.md`.

- **"What would make framework more falsifiable" (Section 6)** → SKIPPED as standalone items. AF→NGFP trajectory already in `open-problems.md` #1. Ghost confinement scale already in `novel-predictions.md` #2. Matter-sector prediction (Higgs + fakeon) already in `novel-predictions.md` #7. Captured in the discriminating-predictions entry.

### Summary: Added 1 new entry (discriminating-predictions), updated 4 existing entries (ghost-fate-strong-coupling, novel-predictions, open-problems, all INDEX files), skipped 9 findings already covered by existing entries, resolved 0 conflicts. Noted 1 possible author attribution discrepancy (arXiv:2412.15037).

---

## 2026-03-26 Processing: exploration-007-unified-framework.md (quantum-gravity-2 strategy-003)

### Report Summary

Major synthesis document constructing a unified QG+F--AS framework. Ties together the sector-by-sector compatibility analyses from explorations 002-006 into a single coherent theory: QG+F and AS are perturbative/non-perturbative descriptions of one UV-complete quantum gravity theory, in direct analogy with perturbative QCD and lattice QCD. Contains: formal conjecture with four-derivative action, precise QCD analogy mapping table (11 rows), master regime table (8 regimes), Planck-scale phase transition, 5 bridge mechanisms, 7 novel predictions unique to unification, prioritized open problems with specific resolving calculations, and overall assessment.

### Findings extracted:

- **Unified theory conjecture + QCD analogy (expanded) + regime structure + phase diagram** → filed at `cross-cutting/unified-qgf-as-framework/framework-conjecture.md` (NEW). The core theory statement with the formal conjecture, 11-row QCD mapping (extends existing 8-row table in `qcd-analogy-ghost-confinement.md` with rows for fixed points, hadronization, and Draper et al. realization), master regime table covering 8 energy regimes (genuinely new artifact — no existing entry has a comprehensive regime table), phase transition characterization, and value-add comparison table.

- **Ghost bridge mechanism (§3.1)** → SKIPPED. Already thoroughly covered by `asymptotic-safety/ghost-fate-strong-coupling.md` (4 mechanisms, critical gap, verdict) and `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` (analogy, confinement conjecture, breakdown points). The report's bridge framing ("fakeon is the perturbative avatar of ghost confinement") is captured as part of the framework conjecture entry.

- **Fixed point bridge mechanism (§3.2)** → SKIPPED. Already covered by `asymptotic-safety/af-ngfp-fixed-point-connection.md` (two interpretations, known flow structure, literature gaps). The unified interpretation (AF→NGFP crossover→GR flow) is captured in the framework conjecture entry.

- **Inflation bridge mechanism (§3.3)** → SKIPPED. Already covered by `cross-cutting/qgf-vs-as-cmb-discrimination.md` (corrected AS inflation taxonomy, SUPPORTS MODERATE verdict, discrimination table, experimental timeline).

- **BH bridge mechanism (§3.4)** → SKIPPED. Already thoroughly covered by `cross-cutting/qgf-vs-as-bh-compatibility.md` (5 arguments, domain-of-validity table, spontaneous ghostification analysis, SUPPORTS verdict).

- **Analyticity bridge mechanism (§3.5)** → SKIPPED. Already covered by `cross-cutting/qgf-vs-as-analyticity-compatibility.md` (three-step argument, SUPPORTS verdict).

- **7 novel predictions unique to unification (§4)** → filed at `cross-cutting/unified-qgf-as-framework/novel-predictions.md` (NEW). These emerge ONLY from combining QG+F and AS: (1) average continuation as AS Wick rotation solution (extends the "suggestive" note in analyticity entry to a concrete methodological prediction with specific test), (2) ghost confinement scale = M_P as dynamically generated (extends the Holdom-Ren conjecture from QCD analogy entry into a specific unified prediction where m_2 is fixed by RG flow, not free), (3) BH evaporation 3-phase transition with PBH remnant observables (extends BH compatibility analysis into specific observational predictions: GW signals at f~100 Hz, modified PBH mass spectrum, LISA-era targets), (4) unified r formula combining QG+F α,β with AS b (genuinely new formula not in any existing entry), (5) spectral dimension profile matching (extends d_s=2 from consistency check to quantitative matching requirement), (6) six-derivative from NGFP hierarchy (links existing six-derivative entry to NGFP truncation), (7) Higgs mass fakeon compatibility check (links AS Higgs prediction to fakeon quantization).

- **Prioritized open problems (§5)** → filed at `cross-cutting/unified-qgf-as-framework/open-problems.md` (NEW). While #1 (AF→NGFP trajectory) and #2 (spin-2 confinement) are already noted as gaps in their respective entries, this is the first comprehensive prioritized catalog with specific resolving calculations defined, QCD analogy breakdown analysis (4 points from the unified perspective), and experimental falsification conditions table.

- **Comparison table: what unification adds (§6)** → filed as part of `framework-conjecture.md`. 8-row table showing what QG+F alone, AS alone, and the unified theory predict for each of 8 questions. New synthesis artifact.

- **Phase transition characterization (§2.2)** → SKIPPED as standalone. The 3 lines of evidence are already spread across existing entries: coupling strength (QCD analogy), ghost mass threshold (QG+F core-idea), BH branch crossing (BH compatibility). Captured in the framework conjecture entry's phase transition section.

- **Overall assessment: strengths/weaknesses/verdict (§6.2)** → filed as part of `framework-conjecture.md`. "Most parsimonious interpretation" verdict is new overall judgment.

- **Individual technical details already in library:**
  - Draper et al. complex pole tower → in `ghost-fate-strong-coupling.md`
  - Becker et al. scalar ghost mass divergence → in `ghost-fate-strong-coupling.md`
  - Bonanno-Reuter metric and remnants → in `asymptotic-safety/black-holes-and-singularity-resolution.md`
  - Bonanno et al. 2025 instability at r_H ≈ 0.876/m_2 → in `qgf-vs-as-bh-compatibility.md`
  - SWY two fixed points → in `swy-two-fixed-points.md`
  - Falls et al. 4D critical surface → in `af-ngfp-fixed-point-connection.md`
  - Bianchi-Gamonal precision formula → in `inflationary-predictions.md`
  - n_s tension details → in `cmb-spectral-index-tension.md`
  - CC problem → in `cosmological-constant-problem.md`
  - All SKIPPED — already present with equivalent or better detail.

### Summary: Added 3 new entries (framework-conjecture, novel-predictions, open-problems in new unified-qgf-as-framework subfolder), updated 2 INDEX files, skipped 12+ findings already covered by existing library entries from explorations 002-006, resolved 0 conflicts.

---

## 2026-03-26 Processing: exploration-006-analyticity-reconciliation.md (quantum-gravity-2 strategy-003)

### Report Summary

Systematic investigation of whether QG+F's sacrifice of S-matrix analyticity is reconcilable with AS's Euclidean functional RG framework. Central finding: the apparent tension dissolves entirely — AS doesn't require analyticity, AS already has non-standard analytic structure (complex poles obstruct Wick rotation), and Lorentzian AS formulations bypass the issue. The fakeon "average continuation" may be the solution to AS's own Wick rotation problem. Verdict: SUPPORTS.

### Findings extracted:

- **QG+F 4-prescription table and analyticity sacrifice details** → SKIPPED (already thoroughly covered by `quadratic-gravity-fakeon/analyticity-sacrifice.md` — same table, same consequences list)

- **"Average continuation" mechanism (Anselmi JHEP 2018)** → updated existing `quadratic-gravity-fakeon/analyticity-sacrifice.md` (added new "Average Continuation" section explaining nonanalytic Euclidean→Lorentzian extraction via averaging limits from different directions)

- **AS does NOT require S-matrix analyticity (Wetterich equation is computational tool, Osterwalder-Schrader sufficient not necessary)** → filed as part of new `cross-cutting/qgf-vs-as-analyticity-compatibility.md` (NEW — Step 1 of three-step argument)

- **AS's own Wick rotation obstruction (Donoghue ghost pole, Draper pole towers, Bonanno assumption)** → filed at two locations:
  - New `cross-cutting/qgf-vs-as-analyticity-compatibility.md` (Step 2 of three-step argument)
  - Updated existing `asymptotic-safety/graviton-propagator.md` (added "Wick Rotation Obstruction" section — these are propagator-specific findings that belong there too)

- **"AS: Standard analytic structure at the UV fixed point" claim in analyticity-sacrifice.md** → CONFLICT with exploration findings — **OVERWRITTEN**. Old claim directly contradicted by Donoghue (2020), Draper et al. (2020), Bonanno et al. (2022). Replaced with accurate characterization and cross-reference.

- **Lorentzian AS exists (D'Angelo et al. 2024, Manrique et al. 2011, Foliated AS 2025)** → filed at two locations:
  - New `cross-cutting/qgf-vs-as-analyticity-compatibility.md` (Step 3 of three-step argument)
  - Updated existing `asymptotic-safety/limitations.md` (expanded Lorentzian vs. Euclidean section with specific results and references)

- **Fakeon + FRG operate at different levels (compatible operations)** → filed as part of new `cross-cutting/qgf-vs-as-analyticity-compatibility.md` (compatibility table showing FRG computation vs. physics extraction levels)

- **Platania-Wetterich ghost mechanism orthogonal to analyticity** → SKIPPED as standalone. Already covered in `asymptotic-safety/ghost-fate-strong-coupling.md`. The minor point about analyticity orthogonality is noted briefly in the new compatibility entry.

- **Overall verdict: SUPPORTS** → filed as part of new `cross-cutting/qgf-vs-as-analyticity-compatibility.md` (verdict section with evidence strength table; noted as third SUPPORTS in QG+F = AS reconciliation program)

### Summary: Added 1 new entry, updated 4 existing (2 overwrites: analyticity-sacrifice AS comparison, limitations Lorentzian section; 2 additions: graviton-propagator Wick obstruction, analyticity-sacrifice average continuation), skipped 2 duplicates, resolved 1 conflict.

---

## 2026-03-26 Processing: exploration-004-inflation-prediction-reconciliation.md (quantum-gravity-2 strategy-003)

### Report Summary

Systematic comparison of AS and QG+F inflationary predictions across 6 AS models and QG+F literature. Central finding: both frameworks predict Starobinsky inflation, and the common characterization of AS inflation as "inflaton-free" is incorrect for all but the most primitive model. The "r up to 0.01" attributed to AS comes from one model (Bonanno-Platania with maximal b). Most AS models predict r ≈ 0.003, indistinguishable from QG+F. Verdict: inflationary predictions are reconcilable (MODERATE strength). Also reports new QG+F results (Bianchi-Gamonal 2025 W² precision formula, Anselmi 2023 causality bound).

### Findings extracted:

- **AS inflation taxonomy (6 models across 4 classes)** → updated existing `asymptotic-safety/cosmology.md` (MAJOR OVERWRITE — "Inflation Without an Inflaton" section replaced with "AS Inflation: Four Distinct Classes"). Added: Bonanno-Platania 2015/18 detailed model with L_eff formula and b-dependence, Codello et al. 2014 (Starobinsky from NGFP), Gubitosi et al. 2018 (f(R) RG flow → Starobinsky), Pawlowski et al. 2024 (emergent potential, r ≈ 0.005), summary table. Corrected inflaton-free framing.

- **"Most AS inflation IS Starobinsky" + reconciliation verdict** → updated existing `cross-cutting/qgf-vs-as-cmb-discrimination.md` (MAJOR UPDATE). Added reconciliation analysis with SUPPORTS (MODERATE) verdict, corrected AS characterization in Key Distinction and discrimination table, added missing R²+C² calculation gap, added full AS landscape section with all 6 models, added compatibility scenario.

- **"r up to 0.01" correction** → updated both `asymptotic-safety/cosmology.md` and `cross-cutting/qgf-vs-as-cmb-discrimination.md`. CONFLICT with prior entries that treated this as representative AS prediction. Resolved: it comes from one model (Bonanno-Platania with maximal b ~ 10⁻²); majority predict r ≈ 0.003.

- **Bianchi-Gamonal 2025 precision W² corrections (arXiv:2506.10081)** → updated existing `quadratic-gravity-fakeon/inflationary-predictions.md` (added specificity). New: N³LO precision formula r ≈ 3(1−β/6α)(n_s−1)², W² pushes r DOWN from Starobinsky, c_t/c_s ratio formula.

- **Anselmi 2023 causality bound (PRD 108, 083526)** → updated existing `quadratic-gravity-fakeon/inflationary-predictions.md` (added new result). Pure quadratic inflation ruled out by causality; only Starobinsky-type viable within QG+F.

- **No direct AS vs QG+F inflation comparison paper** → SKIPPED as standalone entry. Noted as literature gap within the updated discrimination entry. Metadata, not a finding warranting its own file.

- **Missing calculation: AS with full R²+C² truncation** → captured in updated `cross-cutting/qgf-vs-as-cmb-discrimination.md` (new "Missing Calculation" section). Not a standalone finding — it's context for the reconciliation.

- **QG+F r predictions cross-check (Anselmi-Piva 2020)** → SKIPPED. Already thoroughly covered in `quadratic-gravity-fakeon/inflationary-predictions.md` (tensor-to-scalar ratio section with full r range and table).

- **Observational discrimination scenarios** → SKIPPED as standalone. Existing `qgf-vs-as-cmb-discrimination.md` already had discrimination windows; minor refinements captured in the update.

- **Bonanno-Reuter 2002 mechanism** → SKIPPED. Already in `asymptotic-safety/cosmology.md` (was Class 1 in old version, retained in updated version).

- **Bonanno et al. 2024 emergent cosmology** → SKIPPED. Already in `asymptotic-safety/cosmology.md` (retained in updated version).

### Summary: Added 0 new entries, updated 3 existing (2 major overwrites: cosmology.md and qgf-vs-as-cmb-discrimination.md; 1 addition: inflationary-predictions.md), skipped 5 duplicates/metadata, resolved 1 conflict (inflaton-free characterization corrected). All INDEX files updated.

---

## 2026-03-26 Processing: exploration-002-fixed-point-compatibility.md (quantum-gravity-2 strategy-003)

### Report Summary

Systematic literature review addressing whether the asymptotically free (AF) UV fixed point of quadratic gravity connects to the non-Gaussian fixed point (NGFP, Reuter) of asymptotic safety via RG flow. Reviews 6 key papers (SWY 2022/2023, Codello-Percacci 2006, Niedermaier 2009/2010, Ohta-Percacci 2014, Falls et al. 2023) plus the QQG claim. Identifies two competing interpretations (same FP vs. distinct FPs) and reaches an INCONCLUSIVE verdict with 4 specific literature gaps.

### Findings extracted:

- **AF–NGFP connection question (full synthesis)** → filed at `asymptotic-safety/af-ngfp-fixed-point-connection.md` (NEW). Genuinely new content: systematic two-interpretation framing, 4 previously uncatalogued papers (Codello-Percacci 2006, Niedermaier 2009/2010, Ohta-Percacci 2014, Falls et al. 2023), INCONCLUSIVE verdict with 4 specific literature gaps (no AF→NGFP trajectory computed, no systematic critical exponent comparison, no separatrix study, no universality class analysis). The existing `swy-two-fixed-points.md` had the SINGLETON risk concept and QQG claim, but lacked these supporting papers and the systematic analysis.

- **SWY 2023 scaling solutions (AF → IR viable)** → updated existing `asymptotic-safety/swy-two-fixed-points.md` (added specificity). New: SWY follow-up paper (JHEP 02 (2023) 054) showing AF has its own viable IR completion via scaling solutions, independent of the NGFP. Cross-reference added to new af-ngfp entry.

- **SWY 2022 two fixed points** → SKIPPED. Already comprehensively covered by `asymptotic-safety/swy-two-fixed-points.md` (critical exponents, SINGLETON risk, d_s = 2 robustness, QG+F as perturbative sector hypothesis). Report adds the specific quote ("may exist a critical trajectory") but the substance is already there.

- **QQG as "concrete realization of AS"** → SKIPPED. Already in `swy-two-fixed-points.md` (SINGLETON risk section).

- **Flow topology synthesis (Section 8)** → captured in af-ngfp entry. New as systematic catalog but individual flow directions partially covered in existing entries.

- **Verdict and literature gaps (Section 10)** → captured in af-ngfp entry. The 4 specific gaps are genuinely new — no existing entry catalogued what calculations are missing.

### Summary: Added 1 new entry, updated 1 existing (SWY entry with 2023 scaling solutions + cross-reference), skipped 2 duplicates (SWY 2022, QQG claim already covered). No conflicts. Index files updated (asymptotic-safety: 12 → 13, root: 145 → 146).

---

## 2026-03-26 Processing: exploration-006-causal-fakeon-theory.md (quantum-gravity-2 strategy-002)

### Report Summary

Deep build report developing the causal-order fakeon concept (from exploration-003) into a full formal theory: "Causal Fakeon Theory (CFT)." Presents 4 axioms + 1 conjecture, derives physical consequences, provides systematic CFT vs QG+F comparison table, identifies 3 novel predictions (including structural prediction: CST continuum limit should produce quadratic gravity), gives detailed loop-level analysis with 3 specific technical requirements, and formulates 5 key open problems.

### Findings extracted:

- **CFT formal axiom structure (4 axioms + 1 conjecture)** → updated existing `quadratic-gravity-fakeon/causal-order-fakeon-interpretation.md` (added substantial depth). Existing file had the basic concept (Wheeler = fakeon, Belenchia et al., SJ mechanism, loop-level gap, predictions, devil's advocate). New report adds: formal axiom structure, spectral causal compatibility condition (positive/negative spectral weight → Feynman/Wheeler), Axiom 4 self-consistency resolution of circularity within perturbation theory, and the loop extension conjecture formalized with Anselmi's threshold-dropping procedure.
- **Detailed loop-level analysis with 3 technical requirements** → updated existing file (added specificity). Three requirements: (1) interacting SJ construction (Dowker et al. 2024 preliminary), (2) causal-set spectral optical theorem (not formalized), (3) spin-2 SJ construction (unexplored). Plus tractability assessment.
- **CFT vs QG+F comparison table** → updated existing file (NEW content). Systematic 11-row comparison covering action, fakeon origin, propagators, microcausality, analyticity, d_s, microstructure, predictions, conceptual economy.
- **Physical consequences section** → updated existing file (added depth). Expanded microcausality reinterpretation (stochastic fluctuations from Poisson sprinkling), d_s unification with Belenchia et al. 2016 (universal d_s = 2 in all dimensions), analyticity explanation (S-matrix encoding of causally forbidden states).
- **Structural prediction: CST continuum limit → quadratic gravity** → updated existing file (GENUINELY NEW prediction). Existing file noted "causal sets don't produce quadratic gravity" as an objection; new report reframes this as a falsifiable prediction: CFT requires higher-order causal set operators to produce R² + C² terms.
- **5 formalized open problems** → updated existing file (added formalization). Upgraded from existing objections to well-posed open problems.
- **Recovery of QG+F at tree level (Stelle potential, GR tests)** → SKIPPED. Already covered in `quadratic-gravity-fakeon/newtonian-potential-and-ir-recovery.md` and `core-idea.md`.
- **Anselmi 2020 loop-level comparison** → SKIPPED as standalone. Already in existing file.
- **Anselmi 2026 causality position** → SKIPPED. Already in `quadratic-gravity-fakeon/analyticity-sacrifice.md`.
- **Belenchia et al. 2015 Wheeler result** → SKIPPED as standalone. Already in existing file and `causal-set-theory/qft-sorkin-johnston.md`.
- **Additional references** → updated existing file. Added: Belenchia et al. (2016), Afshordi-Aslanbeigi-Sorkin (2012), Anselmi (2021 diagrammar), Dowker et al. (2024). Added cross-references to `causal-set-theory/qft-sorkin-johnston.md` and `causal-set-theory/benincasa-dowker-action.md`.

### Summary: Updated 1 existing entry (major upgrade from concept sketch to full theory framework), skipped 4 duplicates. No new entries, no conflicts. Index files updated (quadratic-gravity-fakeon, root factual).

---

## 2026-03-26 Processing: exploration-005-entanglement-fakeon.md (quantum-gravity-2 strategy-002)

### Report Summary

Third of three concept development reports. Develops the concept that the fakeon prescription is uniquely selected by the requirement of finite, well-defined entanglement entropy (MVEH construction). Ghost with Feynman prescription → pathological entanglement (Jatkar-Narayan 2017: negative eigenvalues, complex entropy). Fakeon restores consistency. Self-consistency loop: gravity from entanglement requires fakeon to preserve entanglement. Structural prediction about Wald entropy ↔ MVEH matching.

### Findings extracted:

- **Entanglement-structure fakeon interpretation (full concept)** → filed at `quadratic-gravity-fakeon/entanglement-structure-fakeon-interpretation.md` (NEW). The 1-paragraph Move 7 in `gravitize-the-quantum/scg-viable-moves-for-qgf.md` already proposed this direction; this report contains substantial new content: Jatkar-Narayan (2017) ghost entanglement pathology result, full 5-step mechanism, analyticity sacrifice as informational area law manifestation, structural prediction (Wald entropy should maintain MVEH with fakeon), research direction (nonlinear MVEH as prescription selector), devil's advocate with 6 objections. This warrants its own entry.
- **MVEH program status / Jacobson, Bueno et al., Speranza, Faulkner et al.** → SKIPPED. Already thoroughly covered in `cross-cutting/entanglement-gravity-bootstrap.md` (MVEH construction, linearization barrier, Bueno et al. extension, Susskind-Uglum identification).
- **Susskind-Uglum renormalization of entanglement entropy** → SKIPPED. Already in `cross-cutting/entanglement-gravity-bootstrap.md` (UV divergence structure section).
- **Analyticity sacrifice context** → SKIPPED. Already in `quadratic-gravity-fakeon/analyticity-sacrifice.md`.
- **Cross-references** → updated `gravitize-the-quantum/scg-viable-moves-for-qgf.md` Move 7 with link to full development.

### Summary: Added 1 new entry, updated 1 existing (cross-reference in moves catalog), skipped 3 duplicates.

---

## 2026-03-26 Processing: exploration-004-indivisibility-fakeon.md (quantum-gravity-2 strategy-002)

### Report Summary

Second of three concept development reports. Develops the concept that the fakeon prescription is the gravitational manifestation of stochastic indivisibility (Barandes-Doukas framework). Negative residue = negative intermediate probability = process indivisible through ghost = fakeon forced. Three distinguishing consequences: (1) explains analyticity sacrifice via irreducible multi-time information, (2) connects to measurement problem, (3) suggests non-perturbative criterion. Devil's advocate finds it primarily interpretive.

### Findings extracted:

- **Indivisibility fakeon interpretation (full concept)** → filed at `quadratic-gravity-fakeon/indivisibility-fakeon-interpretation.md` (NEW). The 1-paragraph Move 2 in `gravitize-the-quantum/scg-viable-moves-for-qgf.md` already proposed this direction; this report contains substantial new content: full 5-step mechanism, Doukas Feb 2026 CK-divisibility result applied, analyticity sacrifice explanation (strongest unique contribution), measurement problem connection, non-perturbative criterion, devil's advocate with 5 objections (isomorphism problem, Aaronson test), self-assessment. Warrants its own entry.
- **Doukas (Feb 2026) CK-divisibility result** → SKIPPED as standalone. Already covered in `gravitize-the-quantum/barandes-verlinde-stochastic-emergence.md` (Doukas 2025 [sic] lifting procedure). The specific application to fakeon is new and captured in the new entry.
- **CP-divisibility in open quantum systems** → SKIPPED. Background context, not a finding. Noted in the new entry's mechanism section.
- **Cross-references** → updated `gravitize-the-quantum/scg-viable-moves-for-qgf.md` Move 2 with link to full development.

### Summary: Added 1 new entry, updated 1 existing (cross-reference in moves catalog), skipped 2 duplicates.

---

## 2026-03-26 Processing: exploration-003-causal-order-fakeon.md (quantum-gravity-2 strategy-002)

### Report Summary

First of three concept development reports from strategy-002's concept sprint targeting QG+F's Gap #1 (fakeon interpretation). Develops the concept that the fakeon prescription arises from spacetime's causal partial order. Key discovery: the fakeon propagator (Cauchy principal value) = Wheeler propagator = (G_R + G_A)/2, and Belenchia et al. (2015) independently showed causal set dynamics produces the Wheeler propagator for unstable modes. Nobody has connected these two results.

### Findings extracted:

- **Causal-order fakeon interpretation (full concept)** → filed at `quadratic-gravity-fakeon/causal-order-fakeon-interpretation.md` (NEW). The 1-paragraph Move 5 in `gravitize-the-quantum/scg-viable-moves-for-qgf.md` already proposed this direction; this report contains substantial new content: Wheeler propagator mathematical identity, Belenchia-Benincasa-Liberati (2015) causal set result with direct quotes, Anselmi (2020) explicit loop-level comparison showing Wheeler ≠ fakeon, Sorkin-Johnston vacuum construction mechanism for ghost modes, Emond-Moynihan-Roest (2024) and Ali-Suneeta (2025) classical causal structure results, Donoghue (2019) ghost backward-time propagation, Epstein-Glaser framework, dimensional reduction prediction, devil's advocate with 4 major objections + 4 additional. Substantial new factual and analytical content warranting its own entry.
- **Anselmi 2026 causality position** → SKIPPED. Already thoroughly covered in `quadratic-gravity-fakeon/analyticity-sacrifice.md` (Anselmi's Radical Position on Causality section).
- **Anselmi 2018 microcausality violation** → SKIPPED. Already in `quadratic-gravity-fakeon/core-idea.md` and `microcausality-and-novel-signatures.md`.
- **Cross-references** → updated `gravitize-the-quantum/scg-viable-moves-for-qgf.md` Move 5 with link to full development.

### Summary: Added 1 new entry, updated 1 existing (cross-reference in moves catalog), skipped 2 duplicates.

---

## 2026-03-26 Processing: exploration-002-scg-conceptual-moves.md (quantum-gravity-2 strategy-002)

### Report Summary

Second report from quantum-gravity-2 strategy-002. Extracts conceptual raw materials from SCG v2.0 (strategy-001) that could power novel theory construction targeting QG+F's explanatory gaps. Contains: (A) 6 viable conceptual moves with viability/novelty assessments, (B) 5 technical constraints from strategy-001 negative results, (C) 5 failure anti-patterns, (D) design brief with 3 recommended concept sprint targets (including 1 new move not from SCG).

### Findings extracted:

- **Conceptual moves catalog (Section A + Sprint 3 from Section D)** → filed at `gravitize-the-quantum/scg-viable-moves-for-qgf.md` (NEW). Novel analytical contribution: systematic extraction of 7 viable research directions from SCG targeting QG+F gaps. Individual component concepts (Pedraza, Barandes-Doukas, Malament, MVEH) already in library, but the specific mappings to fakeon interpretation (fakeon as computationally forbidden mode, as gravitational indivisibility, as encoding of causal order, as entanglement consistency requirement) and the viability/novelty rankings are new. Sprint 3's "analyticity sacrifice = entanglement area law" claim included as Move 7.

- **Technical constraint #1: Classical cost functions can't select QG+F (Section B.1)** → SKIPPED (already covered by `cross-cutting/cost-function-ghost-selection-negative.md`, Reason 3)

- **Technical constraint #2: Complexity = Anything (Section B.2)** → SKIPPED (already covered by `cross-cutting/cost-function-ghost-selection-negative.md`, Complexity = Anything section)

- **Technical constraint #3: Barandes lifting is isomorphism (Section B.3)** → SKIPPED (already covered by `gravitize-the-quantum/scg-adversarial-assessment.md`, Attack 1)

- **Technical constraint #4: Causal structure mandatory (Section B.4)** → SKIPPED (already covered by `gravitize-the-quantum/scg-v2-causal-order-rewrite.md`, the entire point of v2.0)

- **Technical constraint #5: Pedraza is 2D only (Section B.5)** → SKIPPED (already covered by `gravitize-the-quantum/scg-adversarial-assessment.md`, Attack 4 and `cross-cutting/cost-function-ghost-selection-negative.md`)

- **Five anti-patterns (Section C)** → SKIPPED (meta-methodology lessons, not factual findings; belong in meta library, not factual library). Content: over-ambitious synthesis, claiming inherited predictions, classical→quantum leap, late devil's advocate, multi-task explorations.

- **Design brief / sprint recommendations (Section D)** → SKIPPED (strategic planning content, not factual findings). Sprint 3's novel conceptual connection captured in Move 7 of the catalog.

- **Cross-references** → updated `gravitize-the-quantum/scg-theory-construction.md` (added link to moves catalog) and `quadratic-gravity-fakeon/explanatory-debts-catalog.md` (added section linking gaps to viable moves).

### Summary: Added 1 new entry, updated 2 existing (cross-references), skipped 8 (5 duplicate constraints, 1 meta-methodology section, 1 strategic planning section, 1 incorporated into new entry).

## 2026-03-25 Processing: exploration-001-time-from-entanglement.md (nature-of-time strategy-001)

### Report Summary

First report from the nature-of-time mission (distinct from the quantum-gravity mission that produced all prior reports). Comprehensive exploration arguing that time is emergent from quantum entanglement. Covers the problem of time / Wheeler-DeWitt, the Page-Wootters mechanism in detail, the gravity-from-entanglement program (Ryu-Takayanagi, Van Raamsdonk, ER=EPR, Jacobson), entanglement-based arrow of time, and a unified synthesis with assessment of strengths and weaknesses.

### Findings extracted:

- **Page-Wootters mechanism (detailed)** → filed at `cross-cutting/page-wootters-mechanism.md` (NEW). Existing `problem-of-time.md` mentioned Page-Wootters in one line as a Type III resolution. The report provides full mathematical formulation, three critical assumptions, Moreva et al. 2014 experimental confirmation, three extensions (Smith-Ahmadi, Giovannetti-Lloyd-Maccone, Hoehn), and three open problems. This is substantial new content warranting its own entry.

- **Arrow of time from entanglement growth** → filed at `cross-cutting/arrow-of-time-from-entanglement.md` (NEW). Not previously covered in the library. The only prior mention of "arrow of time" was a one-liner in `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` about H₀ positivity in the fakeon framework, which is a different topic. This entry covers Linden et al. 2009, Short & Farrelly 2012, Lloyd, Deutsch-Marletto, Scandolo-Chiribella — all new to the library.

- **Time-from-entanglement unified thesis** → filed at `cross-cutting/time-from-entanglement-synthesis.md` (NEW). The synthesis connecting WDW → PW → gravity-from-entanglement → arrow into a single thesis is not in the library. Marked as provisional confidence because while individual pieces are verified, the full chain has important gaps (Lorentz recovery, dS generalization). Includes 7 categorized open problems and a balanced assessment.

- **Problem of time / Wheeler-DeWitt / frozen formalism (§1.1-1.2)** → SKIPPED. Already covered by `cross-cutting/problem-of-time.md` with equivalent detail (Isham-Kuchar classification, WDW equation, frozen formalism, resolution strategies). Added cross-references to new entries.

- **Ryu-Takayanagi formula (§1.4)** → SKIPPED. Already thoroughly covered by `emergent-gravity/entanglement-and-holography/ryu-takayanagi.md` (formula, validation, implications, modern status).

- **Van Raamsdonk / ER=EPR / Lashkari et al. (§1.4)** → SKIPPED. Already covered by `emergent-gravity/entanglement-and-holography/holographic-entanglement-spacetime.md` (Van Raamsdonk, ER=EPR, linearized Einstein from entanglement).

- **Jacobson entanglement equilibrium (§1.4)** → SKIPPED. Already thoroughly covered by `emergent-gravity/thermodynamic-derivations/jacobson-entanglement-2015.md` with full mathematical machinery.

- **De Sitter holography progress (§3.5)** → updated existing `emergent-gravity/entanglement-and-holography/holographic-entanglement-spacetime.md` (added specificity). The existing "Critical Limitation" section noted the AdS restriction; added 2024-2025 developments (static patch holography, island formula extensions, time from dS 2025, naive RT fails strong subadditivity in dS).

### Summary: Added 3 new entries, updated 2 existing (problem-of-time cross-refs, holographic-entanglement-spacetime dS progress), skipped 4 duplicates (problem-of-time, Ryu-Takayanagi, Van Raamsdonk/ER=EPR, Jacobson), resolved 0 conflicts.

## 2026-03-25 Processing: exploration-013-agravity-CC.md (strategy-002)

### Report Summary
Detailed investigation of whether agravity (classically scale-invariant QG+F) can generate the cosmological constant Λ through dimensional transmutation. Covers the Coleman-Weinberg mechanism for M_P, the CC problem within agravity, a novel "cascading dimensional transmutation" mechanism, and assessment of all approaches.

### Findings extracted:
- Agravity framework (Salvio-Strumia 2014): classically scale-invariant action with R²/f₀² and W²/f₂² → SKIPPED (basic framework already in `standard-model-and-agravity.md`)
- Scalar field content (gravitational Higgs S, scalar potential, non-minimal coupling) → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (added specificity: ℒ_BSM formula, key scalars)
- Detailed CW mechanism for M_P (V_E formula, vacuum conditions λ_S=0/β_{λ_S}=0/ξ_S⟨S⟩²=M̄_Pl², CW form of λ_S) → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (added specificity: complete derivation)
- Critical difference from non-gravitational CW (V_E can vanish at minimum) → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (added specificity)
- Mass spectrum (M₂=f₂M̄_Pl/√2, M₀=f₀M̄_Pl/√2, M_s≈1.4×10¹³ GeV) → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (added specificity: mass table)
- f₂ AF beta function as dynamical explanation for small f₂ → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (added specificity: explicit beta function, naturalness argument)
- Tree-level CC = 0 from CW condition λ_S(s)=0 → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (expanded CC section)
- One-loop CC ~ f₂⁴M_Pl⁴/(16π²) ~ 10⁻³⁴ M_Pl⁴ (88 orders too large) → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (added specificity: quantitative failure)
- Salvio-Strumia's own assessment ("at least 60 orders of magnitude too large") → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (added specificity)
- Kugo 2020 theorem: scale invariance necessary but insufficient for CC → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW information); updated `cross-cutting/cosmological-constant-problem.md`
- Weinberg no-go generalization: no continuous symmetry protects CC → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- Cascading dimensional transmutation mechanism (4-stage and 2-stage explored) → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW — novel mechanism explored, found to FAIL)
- Failure mechanism: no IR coupling in QG+F confines at meV → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- Maggiore nonlocal gravity as closest existing CC-from-transmutation idea → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW cross-reference)
- Agravity up to infinite energy (2018): f₀→∞ limit, accidental SUSY → updated existing `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- Unimodular QG+F (Salvio 2024): old CC solved, anthropic for new CC → SKIPPED (basic fact already in library; expanded description)
- Zeldovich formula, seesaw formula, other numerological coincidences → SKIPPED (interesting numerology but not new knowledge about QG+F)
- Connection to Exploration 006 conclusions → SKIPPED (meta-reference, not a finding)

### Summary: Added 0 new entries, updated 2 existing (standard-model-and-agravity.md substantially expanded with CW mechanism detail and CC analysis; cosmological-constant-problem.md with QG+F section), skipped 3 duplicates/meta, resolved 0 conflicts.

---

## 2026-03-25 Processing: exploration-014-non-CMB-signatures.md (strategy-002)

### Report Summary
Systematic assessment of all QG+F experimental signatures beyond the CMB sector: gravitational waves, table-top experiments, cosmological signatures, microcausality violation, and DM candidates. Comprehensive 19-signature catalog with detectability verdicts and priority ranking.

### Findings extracted:
- All GW signatures undetectable: scalar mode (M₀ too high), dispersion (10⁻⁸⁰ suppressed), polarizations (no extra at observable f), QNMs (Planck suppressed), stochastic (f ~ 10⁸-10¹⁰ Hz) → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW — comprehensive catalog)
- First LVK ringdown constraints on quadratic gravity (arXiv:2506.14695, June 2025): ℓ < 34-49 km, 40 orders too weak → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW); updated `cross-cutting/experimental-constraints.md` (NEW experimental data)
- LVK modified dispersion tests (arXiv:2511.00497, 2025) → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW)
- Graviton-fakeon oscillation length L_osc ~ 10⁻⁶⁰ m → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW quantitative)
- GQuEST not relevant to QG+F (tests holographic, not perturbative QFT) → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW); updated `cross-cutting/experimental-constraints.md`
- BMV not discriminating for QG+F (all QG theories predict entanglement) → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW); updated `cross-cutting/experimental-constraints.md`
- Yukawa ranges 25 orders below experimental reach → SKIPPED (quantitative detail already implied by `newtonian-potential-and-ir-recovery.md`; added to new catalog)
- 21-cm signal: modifications 10⁻¹¹⁰ suppressed → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW)
- Matter power spectrum: identical to GR at all cosmological scales → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW)
- Scalaron DM: M₀ too heavy for viable DM window → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW); SKIPPED as standalone (brief mention already in `standard-model-and-agravity.md`)
- Planck remnant DM: non-perturbative, no abundance prediction → SKIPPED (already in `asymptotic-safety/black-holes-and-singularity-resolution.md`)
- Agravity DM (right-handed ν): model-dependent → SKIPPED (already in `standard-model-and-agravity.md`)
- Microcausality violation does NOT propagate (Anselmi & Marino 2020): "universe conspires" → updated existing `quadratic-gravity-fakeon/microcausality-and-novel-signatures.md` (NEW significant result)
- Violation range extends to ~10⁻²⁹ m (6 orders above Planck) → updated existing `quadratic-gravity-fakeon/microcausality-and-novel-signatures.md` (added specificity)
- "Missing resonance" as distinct from "pair of bumps" (4-deriv vs 6-deriv) → updated existing `quadratic-gravity-fakeon/microcausality-and-novel-signatures.md` (added specificity)
- Dressed propagator: peak region "outside convergence domain" → updated existing `quadratic-gravity-fakeon/microcausality-and-novel-signatures.md` (added specificity)
- Six-derivative Lee-Wick GW signatures: also undetectable → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW)
- Complete 19-signature catalog with priority ranking → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW — the main deliverable)
- "QG+F is a one-prediction theory (r)" conclusion → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW)
- Why CMB is special: inflation amplified quantum fluctuations → filed at `quadratic-gravity-fakeon/experimental-signatures-beyond-cmb.md` (NEW explanatory)
- BH QNMs virtual under fakeon, all BH corrections exp(-10⁵⁰) → SKIPPED (already in `black-hole-predictions.md`)
- r prediction and CMB testability → SKIPPED (already in `inflationary-predictions.md`)
- CMB-S4 cancelled → SKIPPED (already in `cmb-experimental-timeline.md`)
- Higgs mass prediction confirmed → SKIPPED (already in `asymptotic-safety/standard-model.md`)

### Summary: Added 1 new entry (comprehensive catalog), updated 3 existing (microcausality signatures, experimental constraints, cosmological constant), skipped 6 duplicates, resolved 0 conflicts.

---

## 2026-03-25 Processing: exploration-011-BH-predictions.md (strategy-002)

### Report Summary
Comprehensive investigation of QG+F black hole physics: nonlinear solutions, singularity resolution, Wald entropy, Hawking radiation, quasi-normal modes, BH shadows, information paradox, remnants, and experimental prospects. Comparison with GR and AS.

### Findings extracted:
- Lü-Perkins-Pope-Stelle nonlinear solutions (Lichnerowicz theorem, 3 families, phase diagram) → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW — comprehensive BH catalog)
- Fakeon prescription selects Schwarzschild at classical level → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW)
- Singularity NOT resolved perturbatively in QG+F → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW)
- Spontaneous ghostification (Bonanno et al. May 2025) → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW)
- Wald entropy S = A/(4G) + O(l_P²/r_H²) → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW); updated `core-idea.md` question #4; updated `newtonian-potential-and-ir-recovery.md` scorecard (7/7 pass); updated `cross-cutting/bekenstein-hawking-entropy.md`
- QG+F Hawking radiation indistinguishable from GR → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW)
- Massive spin-2 QNMs (Tattersall-Silveravalle 2024) — virtual under fakeon → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW)
- BH shadow exponentially suppressed (Held-Gold-Sen 2023) → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW)
- Microcausality and information paradox implications → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW); updated `cross-cutting/information-paradox.md`
- Evaporation endpoint open; remnant comparison (QG+F vs AS vs ghost-as-physical) → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW)
- QG+F vs AS vs GR BH comparison table → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW)
- Experimental prospects table → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (NEW)
- Stelle potential details (V(r)→0, Yukawa charge) → SKIPPED (already covered by `newtonian-potential-and-ir-recovery.md`)
- AS singularity resolution, Planck remnants → SKIPPED (already covered by `asymptotic-safety/black-holes-and-singularity-resolution.md`)
- Six-derivative extension BH predictions even more suppressed → filed at `quadratic-gravity-fakeon/black-hole-predictions.md` (brief mention, not separate entry — already covered in `six-derivative-extension.md`)

### Summary: Added 1 new entry (comprehensive), updated 5 existing files, skipped 3 duplicates, resolved 0 conflicts.

---

## 2026-03-25 Processing: exploration-012-SM-connections.md (strategy-002)

### Report Summary
How QG+F connects to the Standard Model: coupling structure, beta functions with matter, Shaposhnikov-Wetterich Higgs mass, agravity program (Salvio-Strumia), fakeon collider phenomenology, baryogenesis, dark matter, strong CP, AS grand unification.

### Findings extracted:
- f₂ AF for any matter content (all species same-sign contributions) → filed at `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- f₀ NOT AF; resolution via conformal gravity flow → filed at `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- Gauge group SU(3)×SU(2)×U(1) NOT predicted → filed at `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- TAF constraints (SM not TAF-compatible, needs BSM extensions) → filed at `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- Agravity program (Salvio-Strumia): scale invariance, hierarchy, CC, predictions → filed at `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW — first library entry)
- Fakeon collider phenomenology (peak uncertainty, fake inert doublet, muon g-2) → filed at `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW); updated `microcausality-and-novel-signatures.md` (added peak uncertainty, enhanced fake doublet details)
- Baryogenesis via scalaron decay/gravitational baryogenesis → filed at `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- Dark matter connections (scalaron mediator, sterile neutrino DM, BH remnants, fakeon is NOT DM) → filed at `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- Strong CP (indirect via agravity scale invariance) → filed at `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- SM near-criticality as prediction → filed at `quadratic-gravity-fakeon/standard-model-and-agravity.md` (NEW)
- Shaposhnikov-Wetterich mechanism detail (A_λ anomalous dimension, boundary condition, robustness) → updated existing `asymptotic-safety/standard-model.md` (added specificity: mechanism, robustness, connection to QG+F)
- AS grand unification: α_em calculable, predictive GUT quartics (Eichhorn-Held 2018/2020) → updated existing `asymptotic-safety/standard-model.md` (added specificity: AS-GUT section, SO(10) 2025)
- SM near-criticality → updated existing `asymptotic-safety/standard-model.md` (added section)
- Higgs mass prediction 126 GeV → SKIPPED (already in `asymptotic-safety/standard-model.md`; enhanced mechanism detail instead)
- Top quark mass prediction → SKIPPED (already in `asymptotic-safety/standard-model.md`)
- Conformal SM extension predictions → SKIPPED (already in `asymptotic-safety/standard-model.md`)
- Spin-2 fakeon mass constraints → SKIPPED (already covered in `inflationary-predictions.md` via r bounds)

### Summary: Added 1 new entry (comprehensive), updated 3 existing files, skipped 4 duplicates, resolved 0 conflicts.

---

## 2026-03-25 Processing: exploration-010-IHO-CMB-predictions.md (strategy-002)

### Report Summary
Four tasks: (1) Full assessment of IHO ghost paper (arXiv:2603.07150), (2) Complete QG+F CMB predictions catalog beyond n_s and r, (3) AS vs QG+F discrimination table, (4) Experimental timeline for testing.

### Findings extracted:

**New entries (3):**
- IHO ghost interpretation → filed at `quadratic-gravity-fakeon/iho-ghost-interpretation.md` (NEW) — full mechanism (IHO vs ghost vs dual IHO), comparison to fakeon (competing frameworks), geometric superselection sectors, CMB anomaly connection (50-650× Bayes factor, methodology-dependent), unitarity argued not proven, Riemann zeta connection, critical assessment with verdict: interesting but not credible as breakthrough
- QG+F vs AS discrimination → filed at `cross-cutting/qgf-vs-as-cmb-discrimination.md` (NEW) — full observable comparison table, r as sole realistic discriminator (QG+F < 0.005, AS up to 0.01), discrimination windows, Bonanno-Platania AS framework details, experimental timeline reference
- CMB experimental timeline → filed at `cross-cutting/cmb-experimental-timeline.md` (NEW) — SO operational status, BICEP Array, LiteBIRD, **CMB-S4 CANCELLED July 2025**, LISA, DECIGO; "first testable prediction" timeline with 3 opportunities; observable-by-observable precision requirements

**Updated existing (4):**
- Full CMB predictions → updated `quadratic-gravity-fakeon/inflationary-predictions.md` (added α_s, β_s, n_T, f_NL, isocurvature, spectral features, summary table, CMB-S4 cancellation in experiment table)
- CMB-S4 cancellation → updated `cross-cutting/experimental-constraints.md` (expanded primordial GW section, marked CMB-S4 as CANCELLED)
- CMB-S4 cancellation → updated `cross-cutting/cmb-spectral-index-tension.md` (CMB-S4 cancelled, resolution timeline shifted)
- IHO cross-reference → updated `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` (expanded IHO section with verdict, cross-reference to full assessment)

**Skipped (many):**
- QG+F action and propagator structure → already in `core-idea.md`
- Starobinsky inflation mechanism → already in `inflationary-predictions.md`
- r prediction range (0.0004-0.004) → already covered
- n_s prediction and tension → already in `inflationary-predictions.md` and `cmb-spectral-index-tension.md`
- AS inflation predictions (qualitative) → already in `asymptotic-safety/cosmology.md`
- Lee-Wick unitarity failure → already in `lee-wick-gravity/unitarity-resolution.md`
- Fakeon mass constraint m_χ > m_φ/4 → already in `inflationary-predictions.md`
- CMB anomalies at 2-3σ → noted in IHO assessment but not separate finding

**Conflicts resolved (1):**
- **CMB-S4 status**: Multiple existing entries reference CMB-S4 as operational/upcoming. **Resolved**: CMB-S4 was CANCELLED in July 2025 (DOE + NSF withdrew support). Updated all affected entries: `inflationary-predictions.md`, `experimental-constraints.md`, `cmb-spectral-index-tension.md`. Discrimination timeline shifted from "definitive by 2035" to "~2034-2037" via SO + LiteBIRD.

### Summary: Added 3 new entries, updated 4 existing, skipped ~8 duplicates, resolved 1 conflict (CMB-S4 cancellation).

---

## 2026-03-25 Processing: exploration-009-entanglement-UV-construction.md (strategy-002)

### Report Summary
Attempt to construct UV-complete quantum gravity from Jacobson's MVEH as constructive axiom. Reconstructs Jacobson's framework, analyzes UV cutoff behavior, constructs the entanglement-gravity bootstrap, evaluates alternative info-theoretic constructions. Result: MVEH + renormalizability + unitarity uniquely produces QG+F.

### Findings extracted:

**New entries (1):**
- Entanglement-gravity bootstrap → filed at `cross-cutting/entanglement-gravity-bootstrap.md` (NEW) — UV divergence structure of S_EE (Solodukhin 2011), Susskind-Uglum renormalization principle, entanglement-coupling Rosetta Stone (4D mapping table), Nesterov-Solodukhin no-go theorem, Bueno et al. extension to higher-derivative gravity, the linearization barrier, 6-step self-consistency bootstrap construction, spectral dimension alternative route, modular flow unitarity argument for fakeon, six-derivative assessment (permitted but not required), fundamental obstacle to novelty, what would enable genuine novelty, QFC and relative entropy assessments

**Updated existing (3):**
- Info-theoretic axioms → updated `cross-cutting/information-theoretic-constructive-axioms.md` (MVEH axiom marked as NOW EXPLORED constructively with result QG+F; added axiom #5: modular flow unitarity; replaced "What's Missing" with "What's Been Explored and What Remains" reflecting that MVEH is done, QFC shown insufficient alone, others remain open)
- Jacobson 2015 → updated `emergent-gravity/thermodynamic-derivations/jacobson-entanglement-2015.md` (added mathematical machinery: first law of entanglement, modular Hamiltonian formulas, constant stress-energy result, total entropy variation, area variation at fixed volume, derivation of Einstein equations with G = 1/(4ℏη); added 5 structural features; added 4 gaps Jacobson doesn't address; cross-reference to bootstrap)
- IHO cross-reference via qcd-analogy → already handled above in exploration-010 processing

**Skipped (many):**
- Jacobson's core result (MVEH → Einstein equations) → already in `jacobson-entanglement-2015.md` (added mathematical detail as update above)
- QG+F action and uniqueness → already in `quadratic-gravity-fakeon/core-idea.md`
- Fakeon prescription → already in `core-idea.md`
- Lee-Wick failure → already in `lee-wick-gravity/unitarity-resolution.md`
- d_s = 2 → propagator 1/p^4 → already in `spectral-dimension-propagator-constraint.md`
- Six-derivative extension properties → already in `six-derivative-extension.md`
- Entanglement wedge reconstruction (too vague for filing) → not actionable
- Lashkari et al. linearized Einstein from relative entropy → already in `holographic-entanglement-spacetime.md`
- Pagani-Reuter finite S_EE in AS → mentioned in bootstrap entry, not separate finding

### Summary: Added 1 new entry, updated 3 existing, skipped ~9 duplicates, resolved 0 conflicts.

---

## 2026-03-25 Processing: exploration-008-six-derivative-validation.md (strategy-002)

### Report Summary
Comprehensive Tier 1-4 validation of the six-derivative extension of QG+F. Reconstructs the full action, analyzes the propagator (14 DOF, alternating residues), validates through all tiers (structural sanity, known physics recovery, precision tests, novel predictions). Key finding: d_s = 4/3 in UV (not 2), and it passes all validation tiers.

### Findings extracted:

**Conflicts resolved (1):**
- d_s = 4 -> 2 in six-derivative theory → CONFLICT with report finding d_s = 4 -> 4/3. **Resolved**: the report is correct. The 1/p^6 propagator gives z=3, d_s = D/z = 4/3. The old entry incorrectly applied the QG+F (1/p^4) result. This is already acknowledged in `core-idea.md` which says "R^3 ~ partial^6 g would give 1/p^6 propagator and d_s = 4/3." Overwrote `six-derivative-extension.md` with corrected value.

**Updated existing (1):**
- Six-derivative extension → MAJOR UPDATE to `quadratic-gravity-fakeon/six-derivative-extension.md`: added full propagator analysis (spin-2 and spin-0 sectors, mass eigenvalue formulas, alternating residues theorem), 14 DOF particle content, Lee-Wick complex mass pairs as preferred ghost resolution, super-renormalizability stronger than power counting (one-loop only, couplings don't run), full Tier 1-4 validation tables, GR vs QG+F vs six-derivative comparison table, novelty assessment ("not novel theory, but legitimate extension"), research status (~20-30 direct papers)

**Skipped (many):**
- 17 -> 10 -> 3 reduction → already in existing entry
- R^3 inflationary predictions (n_s ~ 0.974, r ~ 0.0045) → already in existing entry
- Naturalness of delta_3 → already in existing entry
- GR recovery at low energies → already covered in `newtonian-potential-and-ir-recovery.md`
- Newtonian potential (Stelle) → already covered; six-derivative modifications are Planck-suppressed
- PPN parameters → already implicit (identical to GR)
- GW speed = c → already implicit
- Graviton mass bounds → trivially satisfied
- Asymptotic freedom → already in existing entry
- Microcausality violation → already in `microcausality-and-novel-signatures.md`
- Research groups → already listed, minor additions absorbed into update

### Summary: Added 0 new entries, updated 1 existing (major), skipped ~12 duplicates, resolved 1 conflict (d_s corrected from 2 to 4/3).

---

## 2026-03-25 Processing: exploration-007-nonperturbative-QGF.md (strategy-002)

### Report Summary
Investigation of the non-perturbative structure of QG+F/AS: the QCD analogy and ghost confinement conjecture (Holdom-Ren), non-perturbative AS predictions (BR black holes, singularity resolution, Planck remnants, vacuum condensate, inflaton-free inflation), gravitational bound states (graviballs, N-portrait), CDT phase diagram and phase transitions, and the QG+F-AS relationship.

### Findings extracted:

**New entries (4):**
- QCD-gravity analogy and ghost confinement → filed at `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` (NEW) — Holdom-Ren structural analogy, ghost confinement conjecture, fakeon as perturbative shadow, IHO interpretation (March 2026), mass gap via Dyson-Schwinger, gravitational "hadrons", 7 breakdown points
- AS black holes and singularity resolution → filed at `asymptotic-safety/black-holes-and-singularity-resolution.md` (NEW) — Bonanno-Reuter metric, singularity resolution via anti-screening, Planck-mass remnants, parameterized collapse, dark matter implications
- Gravitational bound states → filed at `cross-cutting/gravitational-bound-states.md` (NEW) — graviballs, Dvali-Gomez N-portrait, dark matter candidates, Hamber vacuum condensate, lattice evidence gap
- CDT phase diagram → filed at `cross-cutting/cdt-phase-diagram.md` (NEW) — three-phase structure, B-C second-order transition, spectral dimension phase transition, CDT-FRG comparison tension

**Updated existing (3):**
- AS cosmology → MAJOR UPDATE to `asymptotic-safety/cosmology.md` (expanded from thin overview to comprehensive: inflaton-free inflation mechanism, running G model with epsilon_c, vacuum condensate, power-law running, non-perturbative predictions table)
- SWY two fixed points → updated `asymptotic-safety/swy-two-fixed-points.md` (added "QG+F as perturbative sector of AS" hypothesis)
- QG+F core idea → updated `quadratic-gravity-fakeon/core-idea.md` (expanded open question #8 with mass gap and IHO cross-references)

**Skipped (3):**
- Shaposhnikov-Wetterich Higgs mass prediction → already well-covered in `asymptotic-safety/standard-model.md` (report adds "invisible to QG+F" perspective but no new factual content)
- Spectral dimension universality details → already covered in `cross-cutting/spectral-dimension-running.md`
- d_s = 4 -> 2 universality across approaches → already covered

### Summary: Added 4 new entries, updated 3 existing (1 major), skipped 3 duplicates, resolved 0 conflicts.

---

## 2026-03-24 Processing: exploration-005-ns-beta-functions-six-derivative.md (strategy-002)

### Report Summary
Detailed computation of n_s shift from RG running of R² coupling in QG+F using physical (Branchina 2024) beta functions, plus comprehensive analysis of the six-derivative gravitational extension with R³ correction. Three-part structure: (A) physical beta functions and definitive RG running calculation → Δn_s ~ 10⁻¹⁴ (ruled out), (B) six-derivative action inventory and R³ inflationary predictions (δ₃ ≈ −10⁻⁴ → n_s ≈ 0.974), (C) synthesis comparing approaches and implications for QG+F program.

### Findings extracted:

**New entries (1):**
- Physical beta functions of quadratic gravity → filed at `quadratic-gravity-fakeon/physical-beta-functions.md` (NEW) — Branchina et al. PRL 2024 gauge-invariant beta functions vs. Fradkin-Tseytlin 1982, full comparison table (5 coefficient differences), notation mapping (λ=f₂², ξ=−6/f₀²), QG+F coupling values during inflation (f₀² ≈ 9.4×10⁻⁹, θ ≈ 1.8×10⁸, ξ ≈ −6.4×10⁸), two separatrices (s₁: ξ ≈ 79.4λ tachyonic, s₂: ξ ≈ −3.53λ healthy), crucial result: AF compatible with healthy Starobinsky scalar via s₂, fakeon does not modify one-loop beta functions, running of f₂

**Updated existing (5):**
- n_s resolution paths → updated `quadratic-gravity-fakeon/ns-tension-resolution-paths.md` (MAJOR UPDATE — Path 1 RG running changed from "most natural, critical next calculation" to "RULED OUT (Δn_s ~ 10⁻¹⁴)"; added definitive calculation: β_θ ≈ −1.76×10⁻⁴, Δθ/θ ≈ 10⁻¹⁴, two independent reasons for suppression; three cross-checks (Coleman-Weinberg, Anselmi cosmic RG, radiative corrections literature); Path 2 R³ promoted to #1 with expanded mechanism/slow-roll/naturalness; added distinguishing predictions table; added "What this means for QG+F" section; confidence → verified)
- Six-derivative extension → updated `quadratic-gravity-fakeon/six-derivative-extension.md` (MAJOR UPDATE — added complete 17-term inventory of six-derivative invariants with all 8 pure cubic and 9 derivative-on-curvature terms; reduction chain 17→10→3 via integration by parts, Xu identity, Lovelock constraint; super-renormalizability: finite beyond 3 loops, propagator 1/p⁶; fakeon for complex conjugate mass pairs; modified slow-roll parameters εᵥ and ηᵥ; naturalness comparison table for δ₃; tachyonic instability caveat; research groups and ~20+ papers 2024-2025; confidence → verified)
- Inflationary predictions → updated `quadratic-gravity-fakeon/inflationary-predictions.md` (minor — added definitive Δn_s ~ 10⁻¹⁴ result to running note)
- Inflationary model selection → updated `cross-cutting/inflationary-model-selection-post-act.md` (minor — corrected RG-improved Starobinsky note: QG+F perturbative running negligible; requires AS non-perturbative effects or six-derivative R³; corrected UV completion exceptions)

**Skipped (duplicates/already covered):**
- Starobinsky inflation mechanism → SKIPPED (already in `inflationary-predictions.md`)
- Basic n_s tension numbers (0.974 vs 0.967) → SKIPPED (already in `cmb-spectral-index-tension.md` and `inflationary-predictions.md`)
- R³ basic prediction (δ₃ ≈ −10⁻⁴ → n_s ≈ 0.974) → SKIPPED as standalone (already in `ns-tension-resolution-paths.md` from exploration-004; expanded in-place)
- Anselmi r prediction (4/3 < N²r < 12) → SKIPPED (already in `inflationary-predictions.md`)
- Literature confirmations from arXiv:2511.06640 and arXiv:2504.20757 → SKIPPED as standalone (folded into updated resolution paths)
- Active research groups list → SKIPPED as standalone (folded into six-derivative-extension.md update)
- Six-derivative theory genuinely different from QG+F → SKIPPED as standalone (folded into six-derivative-extension.md update)
- Synthesis comparison table → SKIPPED as standalone (folded into ns-tension-resolution-paths.md update as distinguishing predictions)

### Summary: Added 1 new entry, updated 5 existing (2 major, 3 minor), skipped 8 (duplicates or folded in). No conflicts — new results are additive (ruling out Path 1 doesn't contradict prior entries, it answers their open question).

---

## 2026-03-24 Processing: exploration-004-ns-tension-analysis.md (strategy-002)

### Report Summary
Comprehensive analysis of the CMB spectral index (n_s) tension between ACT DR6 + DESI data (n_s ≈ 0.974) and the Starobinsky/QG+F prediction (n_s ≈ 0.967). Covers: (1) current experimental status across ACT, Planck PR4, SPT-3G, DESI, (2) modifications to QG+F that could resolve the tension, (3) alternative inflationary theories predicting n_s ≈ 0.974, (4) what confirmation would rule out, (5) candidate theory identification (RG-improved QG+F and six-derivative extension).

### Findings extracted:

**New entries (4):**
- CMB spectral index tension observational status → filed at `cross-cutting/cmb-spectral-index-tension.md` (NEW) — ACT DR6 n_s = 0.974 ± 0.003, Planck PR4 n_s = 0.9638, SPT-3G n_s = 0.951, DESI shifts n_s upward, combined analyses table, systematic effects (DESI degeneracy, lensing anomaly, foreground contamination, inter-experiment tension), EDE wild card (n_s → 0.98-1.00), future experiments timeline (CMB-S4 definitive ~2028-2030)
- QG+F n_s resolution paths → filed at `quadratic-gravity-fakeon/ns-tension-resolution-paths.md` (NEW) — four ranked paths: (1) RG running of R² with γ ≈ 0.007 (most natural, includes Branchina et al. PRL 2024 physical beta functions), (2) R³ correction δ₃ ≈ −10⁻⁴, (3) matter radiative corrections (Yukawa/Higgs portal), (4) high e-folds; critical next calculation defined
- Six-derivative super-renormalizable gravity → filed at `quadratic-gravity-fakeon/six-derivative-extension.md` (NEW) — QG+F extension with R³ naturally present at tree level, super-renormalizable (finite from 2-loop), property comparison table, tier 1 checks, Modesto's work, research status
- Inflationary model selection post-ACT → filed at `cross-cutting/inflationary-model-selection-post-act.md` (NEW) — favored models (monomial φ^(2/3), RG-improved Starobinsky, R²+R³), disfavored (pure Starobinsky >3σ, Higgs inflation, standard α-attractors), UV completion challenge, spectral index running

**Updated existing (1):**
- QG+F inflationary predictions → updated `quadratic-gravity-fakeon/inflationary-predictions.md` (UPDATED — major expansion: added n_s analysis section with Starobinsky refined formula, proof that fakeon/C² does NOT shift n_s, 2.3σ tension significance, falsification criteria combining r and n_s, cross-references to resolution paths; updated significance section)

**Skipped (duplicates/already covered):**
- Starobinsky inflation basic mechanism → SKIPPED — already covered by `quadratic-gravity-fakeon/inflationary-predictions.md` and `quadratic-gravity-fakeon/core-idea.md`
- AS RG-improved inflation basics → SKIPPED — already covered by `asymptotic-safety/cosmology.md`; new AS-specific details (RG improvement formula, β parameter effects) are cross-referenced from the QG+F resolution paths entry
- Fakeon mass constraint m_χ > m_φ/4 → SKIPPED — already in `quadratic-gravity-fakeon/inflationary-predictions.md` (now moved to more logical position)
- Connection to cosmological constant problem → SKIPPED — the report acknowledges this is speculative; the CC involves 10¹²⁰ hierarchy while n_s shift is O(1%); not enough substance to file separately
- QG+F parameter space discussion → SKIPPED — folded into the inflationary-predictions update (f₀ fixed by A_s, f₂ affects r not n_s)
- Models with running spectral index → SKIPPED — folded into inflationary-model-selection-post-act.md (running too small to explain tension)

### Summary: Added 4 new entries, updated 1 existing, skipped 6 (duplicates or folded in). No conflicts.

---

## 2026-03-24 Processing: exploration-003-lee-wick-qg-assessment.md (strategy-002)

### Report Summary
Comprehensive assessment of Lee-Wick quantum gravity as a complete theory. Seven tasks: reconstruct the theory (action, propagator, 12 key papers), definitively resolve unitarity status (5 independent evidence lines: FAILS with CLOP), Tier 1 validation (FAILS with CLOP, passes with fakeon = QG+F), Tier 2 validation (Newtonian potential, GR recovery, PPN), comparison to QG+F (same action, different prescription; 4-deriv + fakeon = QG+F exactly), novelty assessment (~15-25 papers, ~5-10 researchers, program absorbed into fakeon), overall verdict (not viable as independent construction target). The definitive finding: Modesto (the creator of LW QG) co-authored a 2025 paper with Anselmi concluding only the fakeon prescription is physically viable.

### Findings extracted:

**New entries (2):**
- Unitarity resolution: 5 evidence lines → filed at `lee-wick-gravity/unitarity-resolution.md` (NEW) — Kubo-Kugo 2023 direct unitarity violation above threshold, Anselmi 2022 structural problems (non-Hermitian classical limit, unbounded Hamiltonian), Anselmi+Modesto 2025 definitive co-authored verdict, Oda 2026 bound state impossibility, Buoninfante 2025 ghost resonance in first Riemann sheet; ghost confinement strategy fails; research program trajectory 2015-2026; key researchers
- Four prescriptions comparison → filed at `lee-wick-gravity/prescription-comparison.md` (NEW) — by-the-book, LWN/CLOP, fakeon/AP, direct Minkowski; property table (Lorentz inv., optical theorem, power-counting, analyticity); CLOP Lorentz violation mechanism (Nakanishi 1971: loop energy complex contour vs real spatial momenta under boost); fakeon average continuation formula ℳ_AP = ½[ℳ(p²−iε) + ℳ(p²+iε)]; from definitive 2025 paper arXiv:2503.01841

**Overwrites/major updates (1):**
- Lee-Wick core theory description → OVERWROTE `lee-wick-gravity/core-idea.md` — CONFLICT with existing entry which claimed "ghost-free via CLOP, genuinely distinct from QG+F, unitarity debated, 2nd most promising escape route." Resolved by overwriting: CLOP fails unitarity and Lorentz invariance; 4-deriv + fakeon = QG+F; 6-deriv = super-renorm variant; not viable as independent program. Reason: 5 independent evidence lines including Modesto's own 2025 co-authored paper.

**Updated existing (4):**
- Escape routes survey → updated `constraints/escape-routes-from-no-go.md` (UPDATED — Route 4 changed from "OPEN, Moderate theory space, High novelty potential" to "CLOSED, None (collapses to QG+F)"; novel candidate #2 Lee-Wick QG marked as ELIMINATED; cross-cutting insight #1 corrected to remove Route 4 combination suggestion)
- Ghost/d_s no-go theorem → updated `constraints/structural/ghost-spectral-dimension-no-go.md` (UPDATED — escape route (E) marked as CLOSED with explanation; Lee-Wick row in theory comparison table corrected from "~(complex poles)" to "✗ (CLOP fails; fakeon → QG+F)")
- Constraints INDEX → updated `constraints/INDEX.md` (UPDATED — escape-routes description corrected: Route 4 CLOSED, 3 surviving candidates instead of 4)
- Root factual INDEX → updated `factual/INDEX.md` (UPDATED — lee-wick-gravity description corrected from "genuinely distinct from QG+F; higher-loop unitarity debated" to "CLOP definitively fails; not viable as independent program"; finding count 1 → 3; total 99 → 101)

**Skipped (duplicates/already covered):**
- QG+F action structure (S = ∫√-g [M²_P R/2 - C²/2f₂² + R²/6f₀²]) → SKIPPED — already comprehensively in `quadratic-gravity-fakeon/core-idea.md`. The report confirms same action; no new information.
- QG+F propagator decomposition (spin-2, spin-0 sectors) → SKIPPED — already in `quadratic-gravity-fakeon/core-idea.md`
- Fakeon prescription mechanism and unitarity proof → SKIPPED — already in `quadratic-gravity-fakeon/core-idea.md`
- QG+F inflationary predictions (r ∈ [0.0004, 0.0035]) → SKIPPED — already in `quadratic-gravity-fakeon/inflationary-predictions.md`
- Newtonian potential singularity-free at r=0 → SKIPPED — already in `quadratic-gravity-fakeon/newtonian-potential-and-ir-recovery.md` (Stelle potential). The complex-pole version's oscillating correction is noted in core-idea but not worth a separate file since LW is not viable.
- GR recovery at low energies → SKIPPED — already covered in QG+F validation scorecard
- PPN parameters (γ=β=1 at r >> 1/M) → SKIPPED — already in `constraints/recovery/post-newtonian-ppn.md` and QG+F validation scorecard
- GW speed = c → SKIPPED — already in `constraints/precision-bounds/gw-speed.md`
- Spectral dimension d_s = 2 for 4-derivative theory → SKIPPED — already across multiple files (cross-cutting/spectral-dimension-running.md, cross-cutting/spectral-dimension-propagator-constraint.md, quadratic-gravity-fakeon/core-idea.md)
- Ghost/d_s no-go theorem basics → SKIPPED — already in `constraints/structural/ghost-spectral-dimension-no-go.md`
- Stelle gravity ghost problem → SKIPPED — already in `constraints/structural/unitarity-and-ghost-freedom.md` and `quadratic-gravity-fakeon/core-idea.md`
- QG+F microcausality violation → SKIPPED — already in `quadratic-gravity-fakeon/microcausality-and-novel-signatures.md`
- Graviton multiplet (h_μν + φ + χ_μν) → SKIPPED — already in `quadratic-gravity-fakeon/core-idea.md`
- RG flow of six-derivative LW QG (Modesto, Rachwał & Shapiro 2018) → SKIPPED — incremental detail about a non-viable theory; beta function specifics not worth filing
- Super-renormalizable vs renormalizable distinction → SKIPPED — already noted in existing escape routes survey; updated in core-idea overwrite

**Housekeeping:**
- Updated `lee-wick-gravity/INDEX.md` — rewritten to reflect 3 findings and corrected viability status
- Updated `factual/INDEX.md` — lee-wick-gravity description corrected, count 1 → 3, total 99 → 101
- Updated `constraints/INDEX.md` — escape-routes description corrected
- Updated `CHANGELOG.md` — logged all overwrites and significant updates

### Summary: Added 2 new entries, overwrote 1 existing (major conflict resolution), updated 4 existing, skipped 16 duplicates, resolved 1 conflict (unitarity status of LW/CLOP: "debated" → "definitively fails").

---

## 2026-03-24 Processing: exploration-002-bianconi-entropic-action-assessment.md (strategy-002)

### Report Summary
Comprehensive critical assessment of Bianconi's "Gravity from entropy" (Phys. Rev. D 111, 066001, 2025). Six tasks: reconstruct the proposal, assess novelty, Tier 1 validation (structural sanity), Tier 2 validation (known physics recovery), assess predictive claims, overall verdict. Author is a network scientist, not a QG researcher. Theory proposes gravitational action = quantum relative entropy between spacetime metric and matter-induced metric, using Dirac-Kähler formalism. Verdict: NOT viable as QG theory — entirely classical, fails Tier 1, serious ghost concerns. Recommendation: MOVE ON, but retain two lessons (entropic action idea and inflationary predictions).

### Findings extracted:

**New entries (1):**
- Bianconi "Gravity from Entropy" full critical assessment → filed at `emergent-gravity/bianconi-entropic-action.md` (NEW) — paper identity and author background (network scientist), core mechanism (ℒ = −Tr ln(G̃ g̃⁻¹) with Dirac-Kähler matter), novelty verdict (genuine in form but engineered to reproduce GR), Tier 1 FAIL (no spin-2 graviton, no unitarity, 4th-order ghost concern, no UV completion, formal diffeo only), Tier 2 partial (GR by construction, PPN/GW speed not computed), predictive claims assessment (CC mostly empty, G-field DM speculative, inflation n_s∈[0.962,0.964] r∈[0.010,0.012] testable but caveated, BH entropy approximate), comparison table to Jacobson/Verlinde/Padmanabhan/Sakharov, follow-up papers, minimal community response, verdict MOVE ON, generalizable lessons

**Updated existing (3):**
- Info-theoretic constructive axioms, axiom #4 → updated `cross-cutting/information-theoretic-constructive-axioms.md` (UPDATED — changed "Very new, not yet widely scrutinized" to detailed verdict: FAILS Tier 1, entirely classical, ghost concerns, phenomenological construction; added cross-reference to full assessment; noted inflationary predictions testable by CMB-S4)
- Emergent gravity limitations overview → updated `emergent-gravity/criticisms-and-limitations/limitations-overview.md` (UPDATED — added "The Shared UV Completion Failure" section: all entropic programs share the failure mode of deriving classical Einstein equations without providing UV completion; Bianconi as latest case study)
- Criticisms-and-limitations INDEX → updated `emergent-gravity/criticisms-and-limitations/INDEX.md` (UPDATED — expanded limitations-overview description to mention shared UV completion failure)

**Skipped (duplicates/already covered):**
- Jacobson (1995) thermodynamic derivation (δQ = TdS → Einstein eqs) → SKIPPED — already in `emergent-gravity/thermodynamic-derivations/jacobson-thermodynamic.md`. Comparison to Bianconi embedded in assessment.
- Jacobson (2015) entanglement equilibrium → SKIPPED — already in `emergent-gravity/thermodynamic-derivations/jacobson-entanglement-2015.md` and `cross-cutting/information-theoretic-constructive-axioms.md`
- Verlinde (2010) entropic gravity mechanism → SKIPPED — already comprehensively in `emergent-gravity/verlinde-entropic-gravity/`
- Padmanabhan's thermodynamic program → SKIPPED — already in `emergent-gravity/thermodynamic-derivations/padmanabhan-program.md`
- Sakharev (1967) induced gravity → SKIPPED — already in `emergent-gravity/thermodynamic-derivations/sakharov-induced-gravity.md`
- Weinberg-Witten theorem details → SKIPPED — already in `constraints/structural/weinberg-witten-theorem.md`. Bianconi's WW status noted in assessment.
- Ostrogradsky theorem / ghost instability from higher derivatives → SKIPPED — already comprehensively in `constraints/structural/unitarity-and-ghost-freedom.md`. Bianconi's specific ghost issue noted in assessment.
- Diffeomorphism invariance requirements → SKIPPED — already in `constraints/structural/diffeomorphism-invariance.md`
- UV completion requirements → SKIPPED — already in `constraints/structural/uv-completion.md`
- Carlip's challenges for emergent gravity → SKIPPED — already in `emergent-gravity/criticisms-and-limitations/carlip-challenges.md`
- Stelle gravity ghost problem (4th-order → massive spin-2 ghost) → SKIPPED — already detailed in `quadratic-gravity-fakeon/core-idea.md` and `constraints/structural/unitarity-and-ghost-freedom.md`
- GW170817 speed constraint |c_gw/c − 1| < 10⁻¹⁵ → SKIPPED — already in `constraints/precision-bounds/gw-speed.md`
- Planck CMB data (n_s = 0.9649 ± 0.0042, r < 0.036) → SKIPPED — already in `cross-cutting/experimental-constraints.md`
- QG+F inflationary predictions (r ∈ [0.0004, 0.0035]) → SKIPPED as update — comparison included in the Bianconi assessment table; source predictions already in `quadratic-gravity-fakeon/inflationary-predictions.md`

**Housekeeping:**
- Updated `emergent-gravity/INDEX.md` — added bianconi-entropic-action.md under new "Specific Proposals" section; updated criticisms description
- Updated `emergent-gravity/criticisms-and-limitations/INDEX.md` — expanded limitations-overview description
- Updated `factual/INDEX.md` — emergent-gravity description expanded (added "Bianconi entropic action assessment (fails Tier 1)"), finding count 17 → 18, total 98 → 99

### Summary: Added 1 new entry, updated 3 existing, skipped 14 duplicates, resolved 0 conflicts.

---

## 2026-03-24 Processing: exploration-001-escape-routes-survey.md (strategy-002)

### Report Summary
Systematic survey of all 5 "escape routes" from the no-go theorem that {d_s = 2, Lorentz invariance, diffeomorphism invariance, renormalizability} uniquely selects QG+F. For each route (relax LI, relax renormalizability, relax d_s=2, relax locality, replace axioms), determines whether the theory space is EMPTY, SINGLETON, or OPEN. All 5 are OPEN. Ranked by novelty potential: Route 5 (info-theoretic axioms) > Route 4 (Lee-Wick) > Route 2 (AS) > Route 3 (relax d_s) > Route 1 (HL). Identifies 4 specific novel theory candidates.

### Findings extracted:

**New entries (5):**
- Escape routes ranked meta-survey → filed at `constraints/escape-routes-from-no-go.md` (NEW) — all 5 routes OPEN; ranked verdicts table; cross-cutting insights (d_s should be prediction not axiom, combine routes, info-theoretic frontier); 4 novel theory candidates (entropic-action QG, Lee-Wick QG, info-theoretic QG from Holographic Emergence Bound, thermodynamic UV completion from Jacobson)
- Horava-Lifshitz gravity detailed status → filed at `horava-lifshitz/core-idea.md` (NEW, new folder) — anisotropic scaling z=3 giving d_s=2, scalar mode strong coupling at ~10^{-3} eV, ghost behavior for 1/3 < lambda < 1, U(1) extension (Horava-Melby-Thompson 2010) as accepted fix, Bargmann extension geometric origin, detailed balance reducing 70+ couplings to 15, post-Newtonian success, theory space essentially HL-only for z=3 gravity, tropological Yang-Mills (2025), no convincing emergent LI mechanism, verdict OPEN but NARROW
- Lee-Wick quantum gravity → filed at `lee-wick-gravity/core-idea.md` (NEW, new folder) — meromorphic propagator loophole in no-go (complex poles not entire), CLOP prescription for ghost freedom, super-renormalizability (better than QG+F), d_s = 2(N+1) for N complex pole pairs, genuinely different S-matrix from QG+F at loop level, discrete theory family parameterized by N and complex masses, unitarity debate at higher loops (2023 PTEP vs 2024 anti-instability), verdict: 2nd most promising escape route
- SWY two distinct fixed points → filed at `asymptotic-safety/swy-two-fixed-points.md` (NEW) — Sen-Wetterich-Yamada 2022 finding of AF + NGFP fixed points in full fourth-order truncation, different critical exponents and relevant directions, d_s=2 robust across ALL truncations (depends only on eta_N = -2), SINGLETON risk that AS and QG+F are same theory, QQG as "concrete realization of AS", Swampland tension (Bonanno et al. SciPost 2025): AS may violate positivity bounds, de Sitter vacua allowed in AS but possibly forbidden in string theory
- Information-theoretic constructive axioms → filed at `cross-cutting/information-theoretic-constructive-axioms.md` (NEW) — four axioms: (1) positivity of relative entropy from Upadhyay et al. 2025 unified holographic bound, (2) maximal vacuum entanglement hypothesis (Jacobson 2015) with UV extension potential and 2026 non-Riemannian extension, (3) quantum focusing condition (Bousso et al.), (4) entropic action principle (Bianconi 2025 Phys. Rev. D, gravity = S(rho_metric || rho_matter), predicts emergent Lambda + G-field dark matter); also gravity as thermodynamic deformation (2025 Otto cycle)

**Updated existing (3):**
- Spectral dimension non-universality → updated `cross-cutting/spectral-dimension-running.md` (UPDATED — added "Universality: Approximate, Not Exact" section: CDT ~1.80±0.25 or ~3/2, LQG 1 or 2, CST d_mm ~2.38; four different d_s definitions; physical consequences of d_s = 2 + epsilon for renormalizability)
- Theory construction implications → updated `constraints/theory-construction-implications.md` (UPDATED — expanded item #2 with Jacobson UV extension idea, added item #5 on information-theoretic axioms with cross-reference, added escape routes survey reference to item #1)
- No-go theorem escape routes → updated `constraints/structural/ghost-spectral-dimension-no-go.md` (UPDATED — added cross-references from each escape route to its detailed file/folder; corrected eta_N sign in Route C; updated Route E description from "d_s = 4/3" to "d_s = 2(N+1), super-renormalizable")

**Skipped (duplicates/already covered):**
- GRB 221009A LIV bounds (E_QG > 5.9-6.2 E_Pl for n=1; >5.8×10^{-8} E_Pl for n=2; constancy of c confirmed 2025) → SKIPPED — identical numbers already in `constraints/recovery/lorentz-invariance-bounds.md`
- IDG gives d_s → 0 (entire function argument) → SKIPPED — already detailed in `constraints/structural/ghost-spectral-dimension-no-go.md` (Hadamard factorization, saddle-point formula, IDG section)
- Jacobson 1995 thermodynamic derivation (delta Q = TdS) → SKIPPED — already in `emergent-gravity/thermodynamic-derivations/jacobson-thermodynamic.md`
- Jacobson 2015 entanglement equilibrium → SKIPPED — already in `emergent-gravity/thermodynamic-derivations/jacobson-entanglement-2015.md`. The UV extension *idea* is new and filed in the info-theoretic axioms file.
- Holographic entropy bounds (Bekenstein, spherical, Bousso) → SKIPPED — already in `cross-cutting/holographic-principle.md` with mathematical forms and 2025 proof
- 2025 unified holographic Swampland condition (Upadhyay et al.) → SKIPPED as standalone — already in `cross-cutting/holographic-principle.md`. The *use as constructive axiom* is new and filed in the info-theoretic axioms file.
- CST everpresent Lambda (Sorkin 1987, Lambda ~ 1/sqrt(N) ~ H_0^2) → SKIPPED — already comprehensively in `causal-set-theory/cosmological-constant.md`
- Unimodular gravity (Salvio 2024) → SKIPPED — already mentioned in `quadratic-gravity-fakeon/core-idea.md` open question #9
- Cosmological constant problem basics and running vacuum model → SKIPPED — already in `cross-cutting/cosmological-constant-problem.md`
- Carlip's two mechanisms (scale invariance + asymptotic silence) → SKIPPED — already in `cross-cutting/spectral-dimension-running.md`
- BMEG bimetric structure basics → SKIPPED — already in `bmeg/` folder (4 files)
- d_s = 2 robust across truncations in AS → SKIPPED as standalone — already in `asymptotic-safety/spectral-dimension.md`. Integrated into the SWY file for context.
- Basic spectral dimension definitions (heat kernel, return probability) → SKIPPED — already across multiple files
- Partially nonlocal theories / scale-dependent locality analysis (Route 4a-b) → SKIPPED as standalone — the general conclusion (no escape from entire/pole dichotomy in Lorentz-invariant theories) is captured in the no-go theorem file. The Deser-Woodard models are IR modifications, not UV completions.
- Multi-fractional spacetimes (Calcagni) → SKIPPED as standalone — ad hoc (d_s is adjustable parameter, not predicted). Mentioned in escape routes summary under Route 3.
- Condensed matter emergent LI analogues → SKIPPED — incremental detail beyond what's already noted in the HL core-idea file

**Housekeeping:**
- Created `horava-lifshitz/` folder with INDEX.md
- Created `lee-wick-gravity/` folder with INDEX.md
- Updated `constraints/INDEX.md` — added escape routes file
- Updated `asymptotic-safety/INDEX.md` — added SWY file (10 → 11 findings)
- Updated `cross-cutting/INDEX.md` — added info-theoretic axioms file (9 → 10 findings)
- Updated `factual/INDEX.md` — added horava-lifshitz and lee-wick-gravity folders; updated counts: constraints 15 → 16, AS 10 → 11, cross-cutting 9 → 10; total 92 → 98; categories 9 → 11

### Summary: Added 5 new entries, updated 3 existing, skipped 15 duplicates, resolved 0 conflicts.

---

## 2026-03-24 Processing: exploration-003-quadratic-gravity-fakeon-validation.md

### Report Summary
Comprehensive validation of quadratic gravity + Anselmi-Piva fakeon quantization. Three tasks: (1) novelty assessment — confirms this is a well-developed program (25+ papers, multiple groups, Quanta feature) with our constraint-driven derivation as the genuinely novel contribution; (2) Tier 2-3 validation against GR recovery tests — passes 6/7 with BH entropy open; (3) novel predictions — inflationary tensor-to-scalar ratio 0.0004 ≲ r ≲ 0.0035 (testable by LiteBIRD/CMB-S4), microcausality violation, scattering signatures, experimental prospects.

### Findings extracted:

**New entries (4):**
- Research program status (milestones, groups, computation status, public attention) → filed at `quadratic-gravity-fakeon/research-program-status.md` (NEW) — Anselmi 25+ papers, Salvio/Donoghue/Holdom/Buoninfante/Platania groups, computation status table, Stelle >150 cit/yr, Quanta Magazine Nov 2025
- IR recovery and Stelle potential → filed at `quadratic-gravity-fakeon/newtonian-potential-and-ir-recovery.md` (NEW) — propagator 3-sector decomposition, Stelle potential V(r) = -GM/r × [1 + (1/3)e^{-M₀r} - (4/3)e^{-M₂r}], singularity resolution (V→0 at r→0), fakeon classicized potential note, experimental bounds (Eöt-Wash), full validation scorecard (6/7 passed)
- Inflationary predictions → filed at `quadratic-gravity-fakeon/inflationary-predictions.md` (NEW) — tensor-to-scalar ratio 0.0004 ≲ r ≲ 0.0035, Starobinsky mechanism + fakeon modification, fakeon mass constraint m_χ > m_φ/4, LiteBIRD δr < 10⁻³ and CMB-S4 σ(r) ≤ 5×10⁻⁴ testability, falsification criterion
- Microcausality and novel signatures → filed at `quadratic-gravity-fakeon/microcausality-and-novel-signatures.md` (NEW) — microcausality violation Δt ~ 1/M₂ (survives classical limit), tree-level scattering = GR but loop/resummation differ, "pair of bumps" signature at E ~ M₂ (smoking gun), scalar GW polarization, GQuEST open calculation, fake doublet collider phenomenology, experimental priority ranking

**Updated existing (1):**
- Open questions → updated `quadratic-gravity-fakeon/core-idea.md` (UPDATED — expanded from 7 to 10 open questions; added: spectral dimension not computed by Anselmi's group (#7), non-perturbative completion/QCD analogy (#8), unimodular extension Salvio 2024 (#9); also enriched existing items with specifics: BH entropy Wald formula detail, AS/asymptotic-freedom relationship detail, microcausality timescale correction 10⁻⁴³ s)

**Skipped (duplicates/already covered):**
- §1.3-1.4 (novelty of our derivation) → SKIPPED — the constraint-driven derivation path, no-go theorem, and uniqueness argument are already comprehensively covered in `quadratic-gravity-fakeon/core-idea.md` (from exploration-002). The report's novelty assessment is meta-commentary, not a new finding.
- §2.3 (PPN γ=1, β=1 verification) → SKIPPED — trivial pass ("corrections ~ e^{-10^{38}}"); the PPN constraint itself is in `constraints/recovery/post-newtonian-ppn.md`. The specific QG verification is noted in the validation scorecard within `newtonian-potential-and-ir-recovery.md`.
- §2.4 (GW speed = c) → SKIPPED — trivial pass (Lorentz invariant by construction); constraint in `constraints/precision-bounds/gw-speed.md`. Noted in validation scorecard.
- §2.5 (graviton mass = 0) → SKIPPED — trivial pass (massless by construction); constraint in `constraints/precision-bounds/graviton-mass.md`. Noted in validation scorecard.
- §2.7 (Lorentz invariance) → SKIPPED — trivial pass (exact by construction); constraint in `constraints/recovery/lorentz-invariance-bounds.md`. Noted in validation scorecard.
- §3.3 (cosmological constant) → SKIPPED as standalone — the CC problem is already in `cross-cutting/cosmological-constant-problem.md`; the renormalizability advantage and unimodular extension specifics are added to `core-idea.md` open questions (#9).
- §3.6 (experimental signatures priority list) → SKIPPED as standalone — the key info is distributed into `inflationary-predictions.md` (CMB tests) and `microcausality-and-novel-signatures.md` (experimental accessibility table). The general experimental infrastructure (GQuEST, LIGO, EHT) is in `cross-cutting/experimental-constraints.md`.

**Housekeeping:**
- Updated `quadratic-gravity-fakeon/INDEX.md` — now lists all 5 findings with one-line descriptions
- Updated `factual/INDEX.md` — quadratic-gravity-fakeon description expanded, finding count 1 → 5, total 88 → 92

### Summary: Added 4 new entries, updated 1 existing, skipped 7 duplicates, resolved 0 conflicts.

---

## 2026-03-24 Processing: exploration-002-spectral-dimension-constructive-axiom.md

### Report Summary
Uses spectral dimension d_s = 4 → 2 as a constructive axiom to derive what propagator, dispersion relation, and action are forced. Derives the d_s = d/n formula and saddle-point formula. Proves a no-go theorem (ghost freedom + Lorentz invariance incompatible with d_s = 2 via Hadamard factorization). Shows IDG gives d_s → 0, not 2. Demonstrates the constraint stack uniquely selects Stelle quadratic gravity with Anselmi-Piva fakeon quantization — only 2 new parameters beyond GR. Covers Carlip's two mechanisms (scale invariance vs. asymptotic silence).

### Findings extracted:

**New entries (3):**
- Mathematical framework: d_s = 2 forces f(p²) ~ (p²)² and propagator ~ 1/p⁴ → filed at `cross-cutting/spectral-dimension-propagator-constraint.md` (NEW) — d_s = d/n formula, saddle-point formula, differential equation characterization, quartic upper bound, interpolating form, Sotiriou-Visser-Weinfurtner framework
- No-go theorem: ghost freedom + Lorentz invariance + d_s = 2 incompatible → filed at `constraints/structural/ghost-spectral-dimension-no-go.md` (NEW) — Hadamard factorization proof, Källén-Lehmann supporting argument, IDG gives d_s → 0, theory comparison table (GR/Stelle/IDG/Lee-Wick/Hořava), five escape routes (fakeon/LV/AS/IDG/Lee-Wick)
- Stelle quadratic gravity + fakeon quantization as candidate QG theory → filed at `quadratic-gravity-fakeon/core-idea.md` (NEW) — explicit action, spin-2/spin-0 propagator decomposition, fakeon prescription, uniqueness from constraint stack (step-by-step elimination), 4 parameters (2 new), established properties (renormalizable/unitary/d_s=2/GR recovery/asymptotically free), costs (microcausality violation, no classical fakeon limit), open questions (BH entropy, AS relationship, predicting M₂)

**Updated existing (2):**
- d_s = 2 as underexploited starting axiom → updated `constraints/theory-construction-implications.md` (UPDATED — changed from "could be used" to noting it has been carried out, with results cross-referenced)
- Spectral dimension running phenomenon → updated `cross-cutting/spectral-dimension-running.md` (UPDATED — added "Constructive Use as Axiom" section with cross-references to new files)

**Skipped (duplicates/already covered):**
- Section 1.1-1.2 (basic definitions of spectral dimension, heat kernel, return probability) → SKIPPED — already covered by `cross-cutting/spectral-dimension-running.md` and `asymptotic-safety/spectral-dimension.md` at equivalent detail. New mathematical formulas (d_s = d/n, saddle-point) filed in the new propagator constraint file.
- Section 6 (Carlip's two mechanisms: scale invariance and asymptotic silence) → SKIPPED — already comprehensively covered in `cross-cutting/spectral-dimension-running.md` (same two mechanisms, same classification). The additional detail (Kasner exponents, Wheeler-DeWitt scaling) is incremental. The insight that quadratic gravity incorporates both mechanisms is noted in `quadratic-gravity-fakeon/core-idea.md`.
- Section 2.2 (Hořava-Lifshitz z=3 giving d_s = 2) → SKIPPED as standalone file — already mentioned in `cross-cutting/spectral-dimension-running.md` and `constraints/recovery/lorentz-invariance-bounds.md`. The specific formula d_s = 1 + d_spatial/z is included in the no-go theorem file as an escape route.
- Section 4.2 (Gauss-Bonnet identity) — included as step in the uniqueness argument in `quadratic-gravity-fakeon/core-idea.md`, not filed separately (standard textbook result, not a research finding).

**Housekeeping:**
- Added `bmeg/` to root `factual/INDEX.md` — it existed with 4 findings but was not listed in the root index. Not from this report but noticed during index verification.
- Created `quadratic-gravity-fakeon/INDEX.md` for the new approach folder.
- Updated finding counts: constraints 14→15, cross-cutting 8→9, total 81→88 (includes 4 pre-existing bmeg findings now listed).

### Summary: Added 3 new entries, updated 2 existing, skipped 4 duplicates, resolved 0 conflicts.

---

## 2026-03-24 Processing: exploration-001-structural-recovery-constraints.md

### Report Summary
Catalogs 32 distinct constraints any viable quantum gravity theory must satisfy, organized into structural (A1-A7), recovery (B1-B7), cross-framework convergences (C1-C6), and precision bounds (D1-D9). Each constraint has mathematical form, restrictiveness ranking, and status across major approaches. Includes constraint dependency map and implications for novel theory construction.

### Findings extracted:

**New entries (14):**
- A1+A2 (Unitarity + Ghost freedom) → filed at `constraints/structural/unitarity-and-ghost-freedom.md` (NEW) — comprehensive treatment of S-matrix unitarity, Ostrogradsky instability, IDG escape route, kinetic positivity constraints (2024), status across ST/LQG/AS
- A4+A3 (Diffeomorphism invariance + correct DOF) → filed at `constraints/structural/diffeomorphism-invariance.md` (NEW) — Weinberg soft graviton theorem uniquely selecting Einstein gravity, derived DOF counting
- A5 (UV completion) → filed at `constraints/structural/uv-completion.md` (NEW) — four escape routes (string, AS, LQG, IDG), Goroff-Sagnotti 1986 divergence, why this is the fundamental obstacle
- A6 (Causality preservation) → filed at `constraints/structural/causality-preservation.md` (NEW) — retarded Green's function, modified dispersion, characteristic surfaces vs metric null cones
- A7 (Weinberg-Witten theorem) → filed at `constraints/structural/weinberg-witten-theorem.md` (NEW) — no composite massless j>1 with T^μν, holographic/broken-Lorentz/gauge escape routes
- B3 (Graviton propagator IR matching) → filed at `constraints/recovery/graviton-propagator-ir-matching.md` (NEW) — full tensor structure P^(2)-½P^(0), subsumes B1/B2, verification in AS (Bonanno 2022) and LQG spin foams
- B4 (Three-graviton vertex) → filed at `constraints/recovery/three-graviton-vertex.md` (NEW) — cubic EH expansion, self-coupling test, uniquely fixed by Weinberg's theorem
- B5/D5 (Equivalence principle) → filed at `constraints/recovery/equivalence-principle.md` (NEW) — MICROSCOPE η < 2.3×10⁻¹⁵ (2022), Nordtvedt η_N < 4.4×10⁻⁴
- B6/D6 (Lorentz invariance bounds) → filed at `constraints/recovery/lorentz-invariance-bounds.md` (NEW) — GRB 221009A/LHAASO E_QG > 5.9 E_Pl, Hausdorff dimension bounds, DisCan algorithm
- B7/D3/D4 (Post-Newtonian PPN) → filed at `constraints/recovery/post-newtonian-ppn.md` (NEW) — Cassini γ = 1 ± 2.3×10⁻⁵, β < 8×10⁻⁵, 1PN metric form, ω_BD > 40,000
- D1 (Graviton mass) → filed at `constraints/precision-bounds/graviton-mass.md` (NEW) — CMB m_g < 5×10⁻³² eV, LIGO m_g < 1.27×10⁻²³ eV, vDVZ discontinuity
- D2 (GW speed) → filed at `constraints/precision-bounds/gw-speed.md` (NEW) — |c_gw/c-1| < 6×10⁻¹⁵ from GW170817, eliminated Horndeski/f(R)/massive gravity classes
- Section E (Constraint rankings/dependencies) → filed at `constraints/constraint-rankings-and-dependencies.md` (NEW) — top-5 most restrictive, unitarity-renormalizability tension, full dependency map, 15 independent constraints
- Section G (Theory construction implications) → filed at `constraints/theory-construction-implications.md` (NEW) — constraint funnel methodology, narrowest bottleneck, 4 underexploited constraints as potential starting axioms

**Updated existing (2):**
- C5 (Holographic entropy bounds) → updated `cross-cutting/holographic-principle.md` (UPDATED — added mathematical forms: Bekenstein bound, spherical bound, Bousso covariant bound, plus 2025 proof for higher-derivative theories)
- D8 (Tensor-to-scalar ratio) → updated `cross-cutting/experimental-constraints.md` (UPDATED — added specific bound r < 0.036 BICEP/Keck 2021, LiteBIRD σ(r) ~ 0.001 target)

**Skipped (duplicates already in library):**
- C1 (Spectral dimension d_s → 2) → SKIPPED — already comprehensively covered by `cross-cutting/spectral-dimension-running.md` (same 7 approaches, same mechanisms, same Carlip quote, same observational bounds)
- C2 (Bekenstein-Hawking entropy S=A/4G) → SKIPPED — already comprehensively covered by `cross-cutting/bekenstein-hawking-entropy.md` (same 5 derivation frameworks, same cross-cutting significance)
- C3 (Entanglement area law) → SKIPPED — already covered by `cross-cutting/entanglement-area-law.md` (Ryu-Takayanagi, graviton entanglement, collapse dynamics)
- C4 (Jacobson thermodynamic derivation) → SKIPPED — already covered across `emergent-gravity/thermodynamic-derivations/` and `cross-cutting/bekenstein-hawking-entropy.md`; the report's assessment ("deep consistency requirement, not independent constraint") is captured in the dependency map
- C6 (Page curve / information conservation) → SKIPPED — already covered by `cross-cutting/information-paradox.md` (island formula, Page time, LQG resolution)
- D5 (Eötvös parameter) → SKIPPED — same content as B5, filed in `constraints/recovery/equivalence-principle.md`
- D6 (LIV time-of-flight) → SKIPPED — same content as B6, filed in `constraints/recovery/lorentz-invariance-bounds.md`
- D7 (GW dispersion) → SKIPPED — low additional value beyond D1 (graviton mass) and D2 (GW speed); no specific new numerical bounds beyond those already filed
- D9 (Spacetime fluctuation searches) → SKIPPED — already covered by `cross-cutting/experimental-constraints.md` (GQuEST, unified framework, QUEST)

**Structure created:**
```
constraints/
  INDEX.md
  constraint-rankings-and-dependencies.md
  theory-construction-implications.md
  structural/
    INDEX.md
    unitarity-and-ghost-freedom.md
    diffeomorphism-invariance.md
    uv-completion.md
    causality-preservation.md
    weinberg-witten-theorem.md
  recovery/
    INDEX.md
    graviton-propagator-ir-matching.md
    three-graviton-vertex.md
    equivalence-principle.md
    lorentz-invariance-bounds.md
    post-newtonian-ppn.md
  precision-bounds/
    INDEX.md
    graviton-mass.md
    gw-speed.md
```

### Summary: Added 14 new entries, updated 2 existing, skipped 9 duplicates, resolved 0 conflicts.

## 2026-03-25 Processing: exploration-003-computational-irreducibility-time.md (nature-of-time strategy-001)

### Report Summary

Third report from the nature-of-time mission. Comprehensive exploration of the thesis that time is the computational irreducibility of the universe — the third perspective alongside the entanglement thesis (exploration-001) and becoming thesis (exploration-002). The report covers four pillars (Wolfram's computational irreducibility, Lloyd's universe-as-quantum-computer, the Landauer-Bennett-Bekenstein thermodynamics-of-computation triad, and Wolfram's Physics Project), with detailed assessment of what the thesis explains well (one-dimensionality of time, arrow, openness of future, time-complexity relationship) and what it struggles with (epistemic vs. ontological ambiguity, quantum non-sequentiality, time dilation, the "now," whether the universe is really a computation, regress, initial conditions). Includes a three-way comparison table with the other two theses.

### Findings extracted:

- **The computational irreducibility thesis** → filed at `cross-cutting/computational-irreducibility-thesis.md` (NEW) — Complete thesis covering: Landauer-Bennett-Bekenstein triad (information is physical, reversible computation requires complete records, finite information density/Bekenstein bound), Wolfram computational irreducibility and Principle of Computational Equivalence (with Israeli-Goldenfeld nuance on coarse-graining), Lloyd's universe-as-quantum-computer (10^120 operations, 10^90-10^120 bits, Margolus-Levitin speed limit), Wolfram Physics Project (hypergraph model, ruliad, multicomputational paradigm, causal graphs — genuine strengths and genuine problems including Harlow and Aaronson criticisms), explanatory strengths (one-dimensionality as strongest achievement, three-layer arrow via Landauer/Bennett/CI, determinism+openness reconciliation, time-complexity via Bennett's logical depth), seven difficulties with honest assessments, full three-thesis comparison table, key thinkers table (Zuse through Margolus-Levitin), historical lineage.

- **Cross-reference: entanglement thesis** → updated existing `cross-cutting/time-from-entanglement-synthesis.md` (added "Competing View: Computational Irreducibility" section noting the key tension: computational thesis explains one-dimensionality better but lacks quantum-gravitational integration)

- **Cross-reference: becoming thesis** → updated existing `cross-cutting/temporal-realism-irreducible-becoming.md` (added computational thesis to Cross-References section with note on conceptual proximity: both emphasize irreversibility and directedness, but grounded in information theory vs. process metaphysics)

- **Cross-reference: problem of time** → updated existing `cross-cutting/problem-of-time.md` (added computational thesis cross-reference: offers novel framing where frozen formalism dissolves because computation is inherently sequential)

### Duplicate/conflict check:

No duplicates found. The library had no existing entries on computational irreducibility, Landauer's principle as it relates to time, Lloyd's universe-as-quantum-computer, Bennett's logical depth, or Wolfram's Physics Project. The Bekenstein bound is referenced in `cross-cutting/holographic-principle.md` but in a different context (entropy bounds for spacetime regions, not computational capacity); no update needed — the new entry covers the computational framing without duplicating the holographic context.

No conflicts. The computational thesis is presented as a third perspective alongside the existing entanglement and becoming theses, not as a replacement for either.

### Summary: Added 1 new entry, updated 3 existing (cross-references), skipped 0 duplicates, resolved 0 conflicts.

---

## 2026-03-25 Processing: exploration-004-attack-entanglement-thesis.md (nature-of-time strategy-001)

### Report Summary

Fourth report from the nature-of-time mission. A systematic devil's advocate attack on the time-from-entanglement thesis (exploration-001's unified thesis). Deploys five attack vectors: (A) circularity — WDW/PW/gravity-from-entanglement all presuppose temporal structures; (B) explanatory weakness — can't explain one-dimensionality, Lorentzian signature, passage, merely transfers arrow; (C) unfalsifiability — empirically equivalent to standard QM, may just be block universe repackaged; (D) physics foundations — WDW may not be fundamental, PW has Unruh-Wald objections and ideal clock/interaction/conditional probability problems, Moreva experiment is modest, AdS dependence severe, factorization vicious circle; (E) phenomenological — "from inside" is a consciousness claim, temporal realist's self-defeating argument. Plus a NOVEL attack (F): kinematic vs. dynamic entanglement incoherence — PW's static entanglement cannot ground the dynamic entanglement growth that produces the arrow. Final verdict: thesis is "wounded but viable" — a reformulation, not an explanation.

### Findings extracted:

- **Comprehensive adversarial assessment of entanglement thesis** → filed at `cross-cutting/entanglement-thesis-adversarial-assessment.md` (NEW). No existing entry covered this. The synthesis entry (`time-from-entanglement-synthesis.md`) had a brief self-assessment with open problems, but nothing like this systematic multi-vector adversarial review with severity rankings, novel attacks, and a clear verdict. Includes the ranked severity table (10 attacks), the novel kinematic/dynamic incoherence argument, what survives (5 items), what collapses (5 items), and the honest reassessment (reformulation, not explanation).

- **Adversarial verdict and downgrades** → updated existing `cross-cutting/time-from-entanglement-synthesis.md` (added "Adversarial Assessment" section with cross-reference, key downgrades, and summary of what survives). This is significant new content — the synthesis entry previously presented the thesis positively with caveats; now it has a formal adversarial counterweight.

- **Unruh-Wald objections (1989) to Page-Wootters** → updated existing `cross-cutting/page-wootters-mechanism.md` (NEW information). Not previously in the library. Added under Open Problems: preferred time variable issue, semi-bounded Hamiltonian difficulty, dormancy period.

- **Moreva experiment critique** → updated existing `cross-cutting/page-wootters-mechanism.md` (added specificity). Changed section header from "Experimental Confirmation" to "Experimental Illustration." Added caveat: result predicted by standard QM, paper uses "illustration" not "confirmation" in title, experiment confirms basic entanglement physics not PW ontology specifically, no unique test.

- **Ideal clock assumption, conditional probability problem, interaction problem (expanded)** → updated existing `cross-cutting/page-wootters-mechanism.md` (NEW subsections). Added three new Open Problems entries with detail from the report. The interaction problem partially existed via Smith-Ahmadi mention but now has the deeper analysis (universal gravitational coupling, perturbation theory vs. fundamental derivation).

- **Kinematic vs. dynamic entanglement tension** → updated existing `cross-cutting/arrow-of-time-from-entanglement.md` (NEW critical caveat). Added "Critical Caveat" section explaining that PW's static entanglement cannot ground dynamic entanglement growth, the standard response papers over a logical gap, and the arrow is not derivable from PW.

- **Circularity of WDW derivation via 3+1 decomposition (A1)** → SKIPPED as standalone entry. The core point (WDW derived from ADM 3+1 split) is already in `problem-of-time.md` and `temporal-realism-irreducible-becoming.md`. The elaborated version is captured in the adversarial assessment entry.

- **Can't explain one-dimensionality (B1)** → SKIPPED. Already in `time-from-entanglement-synthesis.md` §1 and `page-wootters-mechanism.md` open problems. The adversarial assessment captures the severity ranking.

- **Can't explain Lorentzian signature (B2)** → SKIPPED. Already covered in synthesis §1 and PW open problems.

- **Arrow only transfers mystery (B3)** → SKIPPED. Already in synthesis §7 and arrow-of-time "Important limitation." The adversarial assessment captures the stronger framing.

- **Can't explain temporal passage (B4)** → SKIPPED. Already in synthesis §4 ("The 'Now' Problem").

- **Empirical equivalence / unfalsifiability (C1)** → captured in adversarial assessment entry rather than standalone.

- **Block universe comparison (C2)** → captured in adversarial assessment entry rather than standalone.

- **Interpretive underdetermination (C3)** → captured in adversarial assessment entry rather than standalone.

- **WDW non-fundamentality (D1)** → captured in adversarial assessment entry. The specific problems (operator ordering, inner product, alternative approaches) overlap partially with `problem-of-time.md` facets #2 (Hilbert space problem) and #5 (multiple choice problem). The Bamonti-Cinti-Sanchioni (2024) reference is new but not worth a standalone entry.

- **AdS/CFT dependence (D4)** → SKIPPED. Already in synthesis §5.

- **Factorization problem (D5)** → SKIPPED as standalone. Already in synthesis §6 and PW open problems. The Carroll-Singh quantum mereology framing and vicious circle argument are captured in the adversarial assessment.

- **Temporal realist's self-defeating argument and retreat (E2)** → SKIPPED. The self-defeating argument is already in `temporal-realism-irreducible-becoming.md`. The entanglement thesis's response ("time is emergent not illusory") is captured in the adversarial assessment.

- **What survives (S1-S5)** → captured in adversarial assessment entry.

- **Severity rankings** → captured in adversarial assessment entry.

### Summary: Added 1 new entry, updated 3 existing (synthesis with adversarial section, PW with Unruh-Wald/Moreva critique/3 new open problems, arrow-of-time with kinematic/dynamic caveat), skipped 12+ findings already covered by existing entries or captured within the adversarial assessment entry, resolved 0 conflicts.

---

## 2026-03-25 Processing: exploration-003-scg-theory-construction.md (quantum-gravity-2 strategy-001)

### Report Summary

Third report from the quantum-gravity-2 mission. Constructs "Stochastic Computational Gravity" (SCG) — a unified axiomatic framework combining stochastic spacetime → QM emergence (exploration-001) and circuit complexity → geometry emergence (exploration-002) into a single coherent theory with five axioms, two derivation chains (QM from Barandes-Doukas lifting, geometry from cost function), two independent routes to Einstein equations, Diósi-Penrose collapse, six predictions, and seven honest gaps. Includes extensive internal consistency analysis addressing three potential circularities.

### Findings extracted:

- **SCG theory construction (full)** → filed at `gravitize-the-quantum/scg-theory-construction.md` (NEW). This is genuinely new content — a specific axiomatic construction with five axioms, derivation chains, predictions, and gap analysis. The existing `stochastic-spacetime-qm-synthesis.md` covers the general pipeline but NOT the cost function formalism, NOT the geometry emergence from cost optimization, NOT the specific predictions and gap analysis. SCG is a substantial extension warranting its own entry.

- **Barandes-Doukas lifting theorem (§3.2)** → SKIPPED. Already covered by `gravitize-the-quantum/barandes-verlinde-stochastic-emergence.md` (Doukas 2025 lifting, phase as multi-time memory, CPTP maps). Updated with cross-reference to SCG.

- **Nelson stochastic mechanics (§3.4)** → SKIPPED. Already covered by `gravitize-the-quantum/nelson-stochastic-mechanics.md`.

- **ℏ = 2mσ² derivation (§3.4)** → captured in SCG entry. This specific derivation chain (noise amplitude → diffusion coefficient → Nelson → ℏ) goes beyond what's in the existing stochastic-spacetime-qm-synthesis entry.

- **Pedraza et al. complexity → Einstein equations (§4.4)** → captured in SCG entry. New to the library — Pedraza's JHEP result was not previously filed.

- **Jacobson thermodynamic derivation with SCG reinterpretation (§5.2)** → captured in SCG entry. Jacobson's derivation is already in `emergent-gravity/thermodynamic-derivations/jacobson-entanglement-2015.md` but the SCG reinterpretation (each ingredient has stochastic-computational origin) is new.

- **Diósi-Penrose collapse from cost optimization (§5.3)** → captured in SCG entry. The mechanism itself is in `gravitize-the-quantum/diosi-penrose-gravitational-collapse.md` but the derivation from cost optimization (Axiom 4) is new.

- **Oppenheim decoherence-diffusion trade-off in SCG (§5.3)** → captured in SCG entry. Already in `gravitize-the-quantum/oppenheim-postquantum-classical-gravity.md` as a standalone result; the SCG embedding is new.

- **Black hole picture — complexity plateau, singularity resolution (§6.4)** → captured in SCG entry. Novel SCG-specific interpretation.

- **Cosmological constant Λ ~ πG/ln(C_max) (§6.5)** → captured in SCG entry. Novel SCG-specific interpretation.

- **Six predictions (§8)** → captured in SCG entry. No graviton, spacetime diffusion, decoherence-diffusion trade-off, complexity plateau, modified dispersion, higher-derivative gravity — all novel as an ensemble.

- **Seven honest gaps (§7.4)** → captured in SCG entry. Key gaps: dimensionality, Lorentzian signature, continuum limit, N, no SM, indivisibility derivation, quantitative ℏ-G.

- **Three circularities analyzed (§7.1-7.3)** → captured in SCG entry. Novel analysis of QM-complexity circularity, time-complexity circularity, and "which complexity?" ambiguity.

- **Continuum limit mechanism (§4.2)** → captured in SCG entry. SKIPPED as standalone — standard metric geometry technique.

- **Equivalence principle from cost function universality (§6.2)** → captured in SCG entry. SKIPPED as standalone — standard GR result, SCG just reinterprets.

- **Stochastic-spacetime-qm-synthesis pipeline** → updated existing `gravitize-the-quantum/stochastic-spacetime-qm-synthesis.md` with cross-reference to SCG as its axiomatic development.

- **Barandes-Verlinde stochastic emergence** → updated existing `gravitize-the-quantum/barandes-verlinde-stochastic-emergence.md` with cross-reference to SCG.

### Summary: Added 1 new entry (comprehensive SCG theory construction), updated 2 existing (stochastic-spacetime-qm-synthesis and barandes-verlinde with cross-references), skipped 10+ individual findings captured within the comprehensive entry or already covered, resolved 0 conflicts.

---

## 2026-03-25 Processing: exploration-005-synthesis-stress-test.md (nature-of-time strategy-001)

### Report Summary

Fifth report from the nature-of-time mission. Constructs the strongest version of the three-thesis synthesis ("The universe is a static entangled state. Time is the computationally irreducible unfolding of entanglement. What this feels like from inside is becoming."), then systematically attacks it. Key achievement: resolves the kinematic/dynamic entanglement tension identified by exploration-004. Compares the three-layer synthesis to three alternative syntheses (becoming-first, pure computational, relational/QRF). Recommends hybrid development with relational alternative.

### Findings extracted:

- **Three-layer time synthesis (full)** → filed at `cross-cutting/three-layer-time-synthesis.md` (NEW). This is genuinely new content — first attempt to combine all three time theses into a single architecture with precise layer connections, a resolution of the static/dynamic tension, systematic attacks, and comparison to alternatives. Not covered by any existing entry (existing entries cover individual theses and adversarial assessment of entanglement thesis alone).

- **Resolution of static/dynamic tension via computational irreducibility (§1.2)** → captured in three-layer synthesis entry. This directly addresses the HIGH-severity kinematic/dynamic incoherence attack identified in exploration-004's adversarial assessment. The computational deep thermalization result (PRL November 2025) is new supporting evidence.

- **Computational deep thermalization (PRL Nov 2025)** → captured in three-layer synthesis entry. New evidence: quantum systems with low entanglement/complexity can appear fully random to computationally bounded observers. Supports the claim that "dynamic" entanglement growth is an artifact of computational boundedness.

- **Individual weakness scorecard (§1.3)** → captured in three-layer synthesis entry. Novel systematic analysis of how thesis combination patches individual gaps.

- **Five hardest questions answered (§1.4)** → captured in three-layer synthesis entry. Quality ratings: flow (★4), irreversibility (★5, strongest), "now" (★4), observers (★4), time dilation (★4 with circularity caveat).

- **Susskind's second law of quantum complexity (§1.1)** → SKIPPED as standalone. Already implied by `cross-cutting/entanglement-gravity-bootstrap.md` complexity discussion. Brief mention captured in synthesis entry.

- **Attack 1: circularity (§2.1)** → captured in synthesis entry. Overlaps with but goes deeper than the circularity noted in the adversarial assessment (exploration-004). The specific three-layer version (each layer presupposes time) is new.

- **Attack 2: factorization problem (§2.2)** → captured in synthesis entry. Overlaps with factorization problem already in `time-from-entanglement-synthesis.md` §6 and adversarial assessment. The specific damage to the three-layer architecture is new.

- **Attack 3: unfalsifiability (§2.3)** → captured in synthesis entry. Overlaps with adversarial assessment. The synthesis-specific version (explains everything about time, predicts nothing) is new.

- **Attack 4: homunculus problem (§2.4)** → captured in synthesis entry. New attack not in adversarial assessment — targets Layer 3's "from inside" claim.

- **Becoming-first synthesis (§3.1)** → SKIPPED as standalone. Already covered by `temporal-realism-irreducible-becoming.md`. Comparison captured in synthesis entry.

- **Pure computational synthesis (§3.2)** → SKIPPED as standalone. Already covered by `computational-irreducibility-thesis.md`. Comparison captured in synthesis entry.

- **Relational synthesis / Hoehn QRF (§3.3)** → captured in synthesis entry. Novel alternative — using QRF program to avoid factorization problem and soften circularity. Not worth standalone entry yet (proposal stage), but the recommendation to develop a hybrid is significant.

- **Comparison matrix (§3.4)** → captured in synthesis entry. Novel systematic quantitative comparison of four syntheses across eight dimensions.

- **Hybrid recommendation (§Part IV)** → captured in synthesis entry. The resulting formula is a key output of the stress test.

- **Updated existing entries with cross-references:**
  - `time-from-entanglement-synthesis.md` — Added "The Three-Layer Synthesis" section
  - `computational-irreducibility-thesis.md` — Added "The Three-Layer Synthesis" section
  - `entanglement-thesis-adversarial-assessment.md` — Added "Subsequent Development" section noting proposed resolution of kinematic/dynamic incoherence

### Summary: Added 1 new entry (comprehensive three-layer synthesis), updated 3 existing (time-from-entanglement-synthesis, computational-irreducibility-thesis, entanglement-thesis-adversarial-assessment with cross-references and synthesis sections), skipped 5 findings already covered or captured within comprehensive entry, resolved 0 conflicts.

---

## 2026-03-25 Processing: exploration-004-cost-function-ghost-freedom.md (quantum-gravity-2 strategy-001)

### Report Summary

Technical investigation from the quantum-gravity-2 mission: can cost function constraints in the Pedraza et al. (2023) spacetime complexity framework select ghost-free higher-derivative gravity — specifically QG+F (quadratic gravity with fakeon quantization)? The report provides a detailed deep dive into the Pedraza framework (CV complexity, cost function F₁, covariant phase space formalism, modified cost functions → higher-derivative gravity), the "complexity = anything" generalization (Belin, Jorstad-Myers-Ruan 2025), the QG+F propagator structure and fakeon prescription, and then systematically analyzes whether cost function constraints can select QG+F. Clear negative result with four precise reasons.

### Findings extracted:

- **Main negative result: cost function constraints cannot select QG+F** → filed at `cross-cutting/cost-function-ghost-selection-negative.md` (NEW). This is the core deliverable. Four reasons: (1) "complexity = anything" gives too much freedom — infinite class of valid functionals, constraints are IR/macroscopic, (2) wrong direction of inference — framework maps gravity → complexity, reverse is degenerate, (3) cost function is classical, fakeon prescription is quantum (Stelle and QG+F have identical Lagrangians), (4) IR complexity constraints vs. UV ghost-freedom — no mapping. Includes the Pedraza framework mechanism (CV functional, covariant phase space formalism, cost function → higher-derivative gravity mapping), positive-definiteness lead from Flory et al. 2026 JHEP (structurally analogous to ghost-freedom but level mismatch, object mismatch, freedom absorbs it), and alternative holographic constraints (Hofman-Maldacena conformal collider bounds, Caron-Huot swampland conditions — give ranges not unique values).

- **Pedraza et al. spacetime complexity framework detailed mechanism (§1)** → captured within main entry. The CV complexity functional C_gen formula, covariant phase space formalism mechanism, bidirectional coupling, 2D dilaton gravity proof, modified cost functions F₁ → higher-derivative theories. This detail was not in the library (SCG entry only mentioned "Pedraza cost optimization" in one line). Filed as context within the negative result entry rather than standalone — the framework is a tool used to pose the question.

- **"Complexity = anything" framework (§1.5-1.6)** → captured within main entry. Belin et al. 2021, Jorstad-Myers-Ruan 2025 (arXiv: 2503.20943). Infinite class of valid complexity functionals, scheme dependence, F₁ ≠ F₂, five constraints (linear growth, switchback, diffeo invariance, positivity, finite at horizons). Not previously in library.

- **Cost function → higher-derivative gravity mapping (§1.4, §2.5)** → captured within main entry. F₁ ~ C² → spin-2 fakeon sector, F₁ ~ R² → spin-0 sector. Direct mapping to QG+F particle content. New detail not in library.

- **QG+F propagator structure and fakeon prescription (§2)** → SKIPPED. Already thoroughly covered by `quadratic-gravity-fakeon/core-idea.md` (action, propagator decomposition, mass relations, fakeon prescription, uniqueness). Report recapitulates for self-containedness.

- **The positive-definiteness lead from Flory et al. 2026 (§3.4.1)** → captured within main entry. Nielsen complexity penalty factor matrix I_IJ must be positive-definite for viable complexity; landscape/swampland structure; analogy to ghost-freedom; three reasons analogy fails (level mismatch, object mismatch, freedom absorbs it). New to library (Flory et al. not previously referenced).

- **Alternative holographic mechanisms: conformal collider bounds, causality constraints, conformal bootstrap (§3.4.3, §5.3)** → captured within main entry. Hofman-Maldacena 2008, Buchel et al. 2010 (energy flux positivity → a/c bounds → coupling constraints), Caron-Huot et al. 2022 (bootstrap → positivity/monotonicity/log-convexity of couplings). New references not previously in library. Filed as section within main entry rather than standalone — they're contextual for understanding what holography CAN vs. CANNOT do.

- **What would be needed for cost functions to select QG+F (§4.4, §5.5)** → captured within main entry. Four requirements: UV-sensitive complexity constraint, holographic propagator-complexity dictionary, quantization-sensitive boundary observable, positive-definiteness theorem. Concept of "quantum cost function." Filed within main entry as forward-looking section.

- **SCG fundamental obstacle identification (§5.4)** → updated `gravitize-the-quantum/scg-theory-construction.md` (updated "Most promising next direction" from open to BLOCKED; updated prediction #6 table entry; added cross-reference). The cost function determines classical geometry; the fakeon prescription determines quantization. These are distinct layers. This directly answers the SCG entry's identified next direction.

### Summary: Added 1 new entry (comprehensive negative result with embedded Pedraza framework, complexity=anything, positive-definiteness lead, holographic alternatives), updated 1 existing (SCG theory construction — prediction #6 blocked, most promising direction updated, cross-reference added), skipped 1 duplicate (QG+F propagator/fakeon basics), resolved 0 conflicts.

---

## 2026-03-26 Processing: exploration-005-devils-advocate-scg.md (quantum-gravity-2 strategy-001)

### Report Summary

Systematic devil's advocate attack on Stochastic Computational Gravity (SCG) across seven vectors: (1) QM emergence validity, (2) continuum limit, (3) ℏ derivation, (4) Pedraza derivation, (5) novelty, (6) internal contradictions, (7) ontological coherence. 11 ranked weaknesses from FATAL to MODERATE. Overall verdict: SCG does NOT survive in its current form — one fatal structural flaw (Lorentzian signature), three near-fatal derivation gaps, no unique predictions. SCG is a valuable synthesis/repackaging but not a theory.

### Findings extracted:

- **Comprehensive adversarial assessment of SCG (all 7 attacks, severity ranking, overall verdict)** → filed at `gravitize-the-quantum/scg-adversarial-assessment.md` (NEW). No prior adversarial analysis of SCG existed. The existing `scg-theory-construction.md` listed 7 "honest gaps" but did not systematically attack the claims. This report provides: FATAL Lorentzian signature incompatibility argument (positive-definite cost → Riemannian, not Lorentzian; elliptic vs hyperbolic operators), QM emergence as reformulation (Barandes-Doukas isomorphism not derivation, Born rule definitional, phase non-uniqueness dilemma, indivisibility smuggling), continuum limit Gromov-Hausdorff argument, Pedraza 2D-only limitation, novelty assessment (every component borrowed, no unique predictions), self-consistency loop potentially impossible, and ontological coherence critique.

- **SCG status downgrade** → updated `gravitize-the-quantum/scg-theory-construction.md` (MAJOR UPDATE). Status changed from "Research program, not completed theory" to "Research program with fatal structural flaw." Added full "Adversarial Assessment" section with cross-reference, key findings, and what would elevate SCG.

- **Barandes-Doukas adversarial findings** → updated `gravitize-the-quantum/barandes-verlinde-stochastic-emergence.md` (added specificity). Added "Adversarial Findings" section: isomorphism vs. derivation, Born rule definitional, phase non-uniqueness dilemma, indivisibility smuggling QM, Aaronson's "what does it buy me?" critique, Nelson multi-time correlation inheritance, publication status concern.

- **Nelson multi-time correlation problem (Blanchard et al. 1986)** → updated `gravitize-the-quantum/nelson-stochastic-mechanics.md` (NEW information). The library's Nelson entry listed 5 known problems but not this specific one. Added: single-time probabilities agree with QM but multi-time joint probabilities give wrong answers; fix requires wave function collapse (reintroduces measurement postulate); inherited by Barandes-Doukas and SCG.

- **Lorentzian signature as structural incompatibility (not just a gap)** → captured in new adversarial entry. The existing SCG entry listed this as an "honest gap" — the report upgrades it to FATAL: positive-definite cost + metric axioms → Riemannian manifold → elliptic operators → no causality structure. This is not fixable without changing Axiom 3 or adding new axioms.

- **CV conjecture only proven in 2D (Attack 4.3)** → captured in new adversarial entry. The existing cost-function-ghost-selection-negative.md covers the wrong-direction and complexity=anything problems, but not the 2D-only limitation. The report adds: Pedraza et al.'s proof is rigorous only for JT gravity; 2D Einstein tensor vanishes identically; no published 4D proof exists.

- **AdS/CFT circularity for SCG (Attack 4.5)** → captured in new adversarial entry. SCG claims to derive spacetime from scratch but relies on AdS/CFT framework presupposing specific spacetime background.

- **SCG vs QG+F no-graviton conflict (Attack 6.1)** → SKIPPED as standalone finding. QG+F graviton uniqueness already thoroughly covered in `quadratic-gravity-fakeon/core-idea.md`. The specific tension noted in adversarial entry.

- **Oppenheim prediction claimed without derivation (Attack 6.3)** → captured in new adversarial entry. SCG doesn't entail Oppenheim's specific assumptions (classical stochastic metric + quantum matter + Lindblad coupling); both gravity and matter emergent in SCG vs. fundamental split in Oppenheim. Already noted in Oppenheim entry's cross-reference; adversarial entry adds specificity.

- **Diósi-Penrose R₀ constraints (Attack 6.4)** → SKIPPED. Already covered in `gravitize-the-quantum/diosi-penrose-gravitational-collapse.md` with R₀ ≳ 4 × 10⁻¹⁰ m.

- **Self-consistency loop potentially impossible (Attack 6.5)** → captured in new adversarial entry. Pedraza and Jacobson routes make independent assumptions (CV vs. Unruh temperature + BH entropy); no proof of compatibility. Already partially noted as gap in SCG entry; adversarial entry adds argument for potential impossibility.

- **Ontological coherence issues (Attack 7)** → captured in new adversarial entry. "Computation" metaphorical, configurations undefined, optimization ad hoc, prescriptive/descriptive ambiguity. These are new philosophical critiques not in prior library entries.

- **ℏ = 2mσ² as renaming (Attack 3)** → captured in new adversarial entry. Nelson's D = ℏ/2m rearranged; σ free parameter; no information gain. Not filed separately since it's an attack on an existing claim, not a new finding.

- **"No unique predictions" conclusion (Attack 5)** → captured in new adversarial entry. Every prediction traced to source: no graviton (Oppenheim, Jacobson/Verlinde), diffusion (Oppenheim), decoherence-diffusion (Oppenheim), plateau (CDT, causal sets, LQG), dispersion (LQG, DSR), coefficients (can't compute without cost function).

### Summary: Added 1 new entry (comprehensive adversarial assessment), updated 3 existing (SCG theory construction status downgraded, Barandes adversarial findings, Nelson multi-time correlation problem), skipped 2 duplicates (Diósi-Penrose constraints, QG+F graviton uniqueness), resolved 0 conflicts.

## 2026-03-26 Processing: exploration-007-scg-v2-causal-order.md (quantum-gravity-2 strategy-001)

### Report Summary

Seventh report from the quantum-gravity-2 mission. Major rewrite of SCG's axioms to fix the fatal Lorentzian signature problem identified by the adversarial assessment (exploration-005). Replaces the symmetric cost function (Axiom 3) with a causal partial order + directed cost + volume measure, drawing on causal set theory's "Order + Number = Geometry" principle and the Malament-Hawking-King-McCarthy theorem. Includes complete v2.0 axiom set, derivation chain survival analysis, itemized fixes, itemized remaining problems, two new gaps, and an honest overall assessment. Verdict: SCG moves from "dead on arrival" to "alive but wounded."

### Findings extracted:

- **SCG v2.0 complete axiom rewrite and assessment** → filed at `gravitize-the-quantum/scg-v2-causal-order-rewrite.md` (NEW). Genuinely new content: full v2.0 axiom set (Axiom 3 rewritten with 3 components: partial order, directed cost, volume measure), derivation chain survival check (QM survives, geometry improved, Jacobson strengthened, Diósi-Penrose unaffected), fixes scorecard (4 issues resolved/improved), remaining problems scorecard (11 issues including 2 new), overall verdict. No existing entry covers v2.0.

- **SCG theory construction status upgrade** → updated existing `gravitize-the-quantum/scg-theory-construction.md` (status change). Status upgraded from "fatally flawed in current form" to "alive but wounded" with explicit v2.0 cross-reference. Lorentzian signature gap marked as resolved. Added v2.0 to cross-references list.

- **SCG adversarial assessment v2.0 response** → updated existing `gravitize-the-quantum/scg-adversarial-assessment.md` (added v2.0 response). The FATAL flaw (Lorentzian signature) is now marked as "addressed in v2.0." Overall verdict updated to note v2.0 progress. "What Would Elevate SCG" item #1 struck through and marked as addressed, with note on two new moderate gaps introduced.

- **Malament-Hawking-King-McCarthy theorem** → SKIPPED (theorem is referenced but its role is specific to SCG v2.0, already captured in the new entry; the general theorem is covered contextually in `causal-set-theory/core-idea.md`)

- **Sorkin "Order + Number = Geometry" principle** → SKIPPED (already covered in `causal-set-theory/core-idea.md`; the new entry cross-references it)

- **Barandes lifting compatibility with causal order** → SKIPPED (folded into v2.0 entry's derivation chain survival section; not enough new content beyond "it still works" to warrant a separate update to the Barandes entry)

- **Jacobson derivation strengthened by causal structure** → SKIPPED (already well-documented that Jacobson requires causal/Lorentzian structure; the improvement is noted in the v2.0 entry)

- **CDT-like dimension selection possibility** → SKIPPED (only noted as "possible, not proven"; already covered in `cross-cutting/cdt-phase-diagram.md`; too speculative for its own entry)

- **Two new gaps (volume measure, partial order origin)** → captured in new v2.0 entry. Not filed separately since they are assessments of SCG v2.0, not standalone findings.

### Summary: Added 1 new entry (SCG v2.0 causal order rewrite and assessment), updated 2 existing (SCG theory construction status upgrade, SCG adversarial assessment v2.0 response), skipped 5 (Malament theorem, Sorkin principle, Barandes compatibility, Jacobson strengthening, CDT dimension selection — all either already covered or folded into v2.0 entry), resolved 0 conflicts.

---

## 2026-03-26 Processing: exploration-001-qgf-explanatory-debts.md (quantum-gravity-2 strategy-002)

### Report Summary

Comprehensive catalog of 23 explanatory debts (gaps/limitations) of QG+F, each rated by severity (CRITICAL/MAJOR/MODERATE), QG+F-specificity, and explanatory opportunity. Includes comparative analysis against other QG frameworks, 2025-2026 literature findings, and a ranked TOP 5 of most fertile gaps for novel theory construction. The report synthesizes information from across the library into a strategic assessment, with some genuinely new findings (particularly the analyticity sacrifice and the ranked gap catalog).

### Findings extracted:

- **Sacrifice of S-matrix analyticity (Debt 21)** → filed at `quadratic-gravity-fakeon/analyticity-sacrifice.md` (NEW). Genuinely new content: the 2025 paper (Anselmi et al., JHEP 05, 2025, 145; arXiv:2503.01841) explicitly catalogs four inequivalent amplitude prescriptions and what each forfeits — only the fakeon preserves both unitarity and Lorentz invariance, at the cost of analyticity. Consequences enumerated (no dispersion relations, no bootstrap, no standard Euclidean-Lorentzian connection). Anselmi's radical 2026 position (arXiv:2601.06346): causality should be abandoned, "delayed prepostdictions" as maximum. While `research-program-status.md` mentioned these papers as milestones and `microcausality-and-novel-signatures.md` noted the peak being "outside the convergence domain," neither contained the systematic 4-prescription trade-off or the philosophical implications.

- **Comprehensive ranked debt catalog (all 23 debts + TOP 5)** → filed at `quadratic-gravity-fakeon/explanatory-debts-catalog.md` (NEW). The catalog as a whole is the finding — individual debts are largely covered across existing entries, but the systematic severity/specificity rating system, the identification of debt clusters, the TOP 5 ranked for novel theory construction with key leads, the "dark corners the community avoids" meta-analysis, and the comparative framework advantages table are all new. Marked as provisional confidence because the ranking is an assessment, not a verified fact.

- **Research program milestones (2025/2026)** → updated existing `quadratic-gravity-fakeon/research-program-status.md` (added specificity). The 2025 and 2026 milestone entries previously had only paper numbers; added the substance (4-prescription catalog, analyticity sacrifice, causality abandonment position, arXiv numbers).

- **Debt 1: Fakeon's physical interpretation** → SKIPPED. Already covered by `core-idea.md` (open problem #2: "No classical limit for the fakeon"), `iho-ghost-interpretation.md` (competing IHO interpretation), `qcd-analogy-ghost-confinement.md` (confinement picture, mass gap result). The three competing interpretations (Anselmi fakeon, IHO/DQFT, Holdom-Ren confinement) are all documented.

- **Debt 2: Why 4D?** → SKIPPED. Already covered by `core-idea.md` (uniqueness from constraint stack: "dimensionlessness of f_2 and f_0 in 4D is precisely why the theory is renormalizable"). The comparative analysis (string 10D, LQG any d, CDT d-dependent) is partially in various approach entries.

- **Debt 3: SM origin** → SKIPPED. Already in `standard-model-and-agravity.md` (f₂ AF for any matter, gauge group NOT predicted, TAF constraints).

- **Debt 4: BH singularity** → SKIPPED. Thoroughly covered by `black-hole-predictions.md` (Lichnerowicz theorem, fakeon selects Schwarzschild, singularity NOT resolved, spontaneous ghostification, comparison with AS/LQG).

- **Debt 5: CC** → SKIPPED. Already in `standard-model-and-agravity.md` (old CC solved, new CC NOT solved, cascading transmutation fails, Kugo theorem, Weinberg no-go) and `cross-cutting/cosmological-constant-problem.md`.

- **Debt 6: Microcausality** → SKIPPED. Already in `microcausality-and-novel-signatures.md` (violation properties, non-propagation proof, information paradox connection, experimental inaccessibility).

- **Debt 7: One-prediction theory** → SKIPPED. Already in `experimental-signatures-beyond-cmb.md` (all 19 signatures assessed, all undetectable, "one-prediction theory" framing).

- **Debt 8: Non-perturbative completion** → SKIPPED. Already in `core-idea.md` (open problem #8: QCD analogy, mass gap, non-perturbative completion unknown) and `qcd-analogy-ghost-confinement.md` (7 breakdown points, gravitational "hadrons").

- **Debt 9: QG+F ↔ AS** → SKIPPED. Already in `core-idea.md` (open problem #5) and `cross-cutting/qgf-vs-as-cmb-discrimination.md` (r is sole discriminator).

- **Debt 10: Information paradox** → SKIPPED. Already in `cross-cutting/information-paradox.md` (microcausality leak channel, no quantitative calculation) and `microcausality-and-novel-signatures.md`.

- **Debt 11: n_s tension** → SKIPPED. Already in `ns-tension-resolution-paths.md` (4 paths, RG ruled out, R³ works) and `cmb-spectral-index-tension.md`.

- **Debt 12: d_s uncomputed** → SKIPPED. Already in `core-idea.md` (open problem #7) and `research-program-status.md` (computation status: ❌ Not computed).

- **Debt 13: Spacetime microstructure** → SKIPPED as standalone. The spacetime microstructure gap is a restatement of the non-perturbative problem through an ontological lens. Captured as part of the debt catalog (TOP 5 #2). The comparison to LQG spin networks, CDT simplices, CST atoms is partially scattered across those approach entries.

- **Debt 14: Why QM?** → SKIPPED. Shared by all QG approaches. The gravitize-the-quantum folder covers this landscape. Not a QG+F-specific debt.

- **Debt 15: No DM candidate** → SKIPPED. Already in `standard-model-and-agravity.md` (dark matter connections, fakeon excluded as DM, gravitational DM production model-dependent).

- **Debt 16: Problem of time** → SKIPPED. Already in `cross-cutting/problem-of-time.md`. QG+F sidesteps it (perturbative QFT on fixed background) — this is the generic perturbative-approach situation, not unique content.

- **Debt 17: Why fakeon selects unitarity** → SKIPPED. The modular flow unitarity argument is already in `cross-cutting/entanglement-gravity-bootstrap.md`. The question of "why unitarity?" is philosophical rather than factual. Captured in the debt catalog.

- **Debt 18: No cosmological dynamics** → SKIPPED. The DESI hints and Λ = const assumption are noted in `standard-model-and-agravity.md` and `cosmological-constant-problem.md`. Too speculative/uncertain to file as standalone.

- **Debt 19: Classical limit of fakeon** → SKIPPED. Already in `core-idea.md` (open problem #2: "No classical limit for the fakeon — the massive spin-2 mode does not correspond to any classical field. Classical equations use averaged (retarded + advanced) Green's functions."). Exact same content.

- **Debt 20: Vacuum structure** → SKIPPED. Already in `core-idea.md` (open problem #6: "Predicting M_2 and M_0 — from BH entropy, spectral dimension matching, inflation, or cosmological constant constraints").

- **Debt 22: No holography** → SKIPPED. The linearization barrier and AdS/CFT incompatibility are partially in `cross-cutting/entanglement-gravity-bootstrap.md`. The Fursaev et al. reference (PRD 104, 2021) adds a minor detail but not enough for a standalone entry. Captured in debt catalog.

- **Debt 23: No gravitational thermodynamics explanation** → SKIPPED. Already covered by `cross-cutting/bekenstein-hawking-entropy.md` (QG+F Wald entropy) and `black-hole-predictions.md` (Wald correction details). The gap (QG+F computes but doesn't explain) is implicit in these entries.

- **Q-desics reference (March 2026)** → SKIPPED. Too peripheral — "potentially relevant for QG+F but developed outside the QG+F framework." Not actionable.

- **Pre-geometric gravity reference (2025)** → SKIPPED. A competing approach mentioned in passing, not enough detail for a standalone entry.

- **Comparative framework analysis** → Captured in the debt catalog entry. The individual framework advantages are mostly documented in their respective approach folders.

### Summary: Added 2 new entries (analyticity sacrifice, explanatory debts catalog), updated 1 existing (research program status — added milestone substance), skipped 21 (Debts 1-20 and 22-23 all individually covered by existing entries; Q-desics and pre-geometric gravity too peripheral), resolved 0 conflicts.

---

## 2026-03-26 Processing: exploration-003-ghost-fate-strong-coupling.md (quantum-gravity-2 strategy-003)

### Report Summary

Comprehensive literature review asking: what does the non-perturbative / Asymptotic Safety literature say about the fate of the massive spin-2 ghost at strong coupling? Reviews 8 papers/programs (Bonanno et al. 2022, Benedetti et al. 2009, Becker et al. 2017, Platania & Wetterich 2020, Draper et al. 2020, CDT program, Frasca 2025, Holdom-Ren 2016). Identifies 4 proposed mechanisms with zero confirmations for the spin-2 ghost specifically. Reaches INCONCLUSIVE verdict leaning SUPPORTS. Identifies the spin-2 ghost as a "blind spot" in AS literature and the ghost-level QG+F = AS bridge as the single most important open calculation.

### Findings extracted:

- **Ghost fate synthesis (4 mechanisms, critical gap, verdict)** → filed at `asymptotic-safety/ghost-fate-strong-coupling.md` (NEW). Genuinely new: no existing entry surveyed the AS literature specifically for the spin-2 ghost's fate. Covers all four proposed mechanisms (confinement, mass → ∞, fictitious ghosts, complex pole tower) with evidence/status table. Includes Benedetti et al. 2009 (f₂ finite at NGFP → ghost mass stays finite), Becker et al. 2017 (scalar ghost decoupling proof-of-principle), Platania & Wetterich 2020 (fictitious ghost methodology), Draper et al. 2020 (complex pole tower — most concrete). CDT non-resolution. Identifies the spin-2 ghost as a blind spot. Verdict: INCONCLUSIVE leaning SUPPORTS. Bridge unbuilt.

- **Bonanno et al. 2022 ghost absence caveat** → updated existing `asymptotic-safety/graviton-propagator.md` (added critical specificity). Existing entry covered the paper but did NOT note that the ghost is entirely absent from the Einstein-Hilbert truncation used. Added "Critical Caveat" section and cross-reference to ghost-fate entry. Also added ghost propagator as open issue.

- **Holdom-Ren Case A/B mechanisms and author-acknowledged limitations** → updated existing `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` (added specificity). Existing entry had the conjecture and structural mapping but lacked the two specific scenarios (softening vs. confinement) and the 5 limitations acknowledged by the authors. Added cross-reference to new AS ghost-fate entry.

- **Frasca 2025 scope limitation** → updated existing `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` (added critical context). Existing entry described the result without noting it's irrelevant to the spin-2 ghost. Added "Scope limitation" note.

- **Holdom-Ren basic conjecture** → SKIPPED. Already comprehensively covered by `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` (structural mapping table, conjecture, fakeon as perturbative shadow, analogy breakdown points). Only the two specific mechanisms (Case A/B) and limitations were new.

- **CDT d_s = 2 consistency** → SKIPPED as standalone. Already in `cross-cutting/spectral-dimension-and-propagator-constraint.md` and other entries. The specific point about CDT not resolving ghost modes is captured in the new synthesis entry.

- **IHO interpretation** → SKIPPED. Already covered in `quadratic-gravity-fakeon/iho-ghost-interpretation.md` and referenced from `qcd-analogy-ghost-confinement.md`.

- **Mass gap in R² gravity (Frasca 2025)** → SKIPPED as standalone. Already in `qcd-analogy-ghost-confinement.md`. Only added the scope limitation note.

### Summary: Added 1 new entry (ghost-fate-strong-coupling synthesis), updated 2 existing (graviton-propagator: ghost absence caveat; qcd-analogy-ghost-confinement: Case A/B mechanisms, limitations, scope note, cross-references), skipped 4 duplicates (Holdom-Ren basic, CDT d_s, IHO, Frasca standalone). No conflicts. Index files updated (asymptotic-safety: 13 → 14, root: 146 → 147).

---

## 2026-03-26 Processing: exploration-005-bh-compatibility.md (quantum-gravity-2 strategy-003)

### Report Summary

Systematic compatibility analysis of QG+F and AS black hole predictions. The report frames the apparent contradiction (QG+F: Schwarzschild, singular, no remnant vs. AS: modified metric, regular core, Planck remnant) and resolves it via the QCD analogy: these are perturbative vs. non-perturbative descriptions of the same physics. Presents five structured arguments for compatibility, a domain-of-validity regime table, analysis of spontaneous ghostification as non-obstacle, four incompatibility conditions (none met), and caveats. Verdict: SUPPORTS.

### Findings extracted:

- **BH compatibility verdict (SUPPORTS) with five-argument analysis** → filed at `cross-cutting/qgf-vs-as-bh-compatibility.md` (NEW). Genuinely new content: the systematic compatibility synthesis with structured arguments, domain-of-validity regime table, spontaneous ghostification 3-possibility analysis for QG+F=AS, four incompatibility conditions framework, and explicit large-r formula matching verification. Individual BH facts (QG+F predictions, AS predictions, QCD analogy, ghost fate) were already well-catalogued in separate entries, but this cross-cutting compatibility verdict did not exist. Parallels `qgf-vs-as-cmb-discrimination.md` for the CMB sector.

- **"QG+F BHs are Schwarzschild" as perturbative claim** → updated existing `quadratic-gravity-fakeon/black-hole-predictions.md` (conclusion updated). Old text characterized the QG+F vs AS BH situation as "tension" — replaced with cross-reference to the compatibility analysis and SUPPORTS verdict. The conclusion now correctly frames it as regime complementarity rather than tension.

- **AS BR metric large-r agreement + compatibility cross-reference** → updated existing `asymptotic-safety/black-holes-and-singularity-resolution.md` (added specificity). Added explicit formula matching (f(r) → Schwarzschild at large r) and SUPPORTS verdict cross-reference to comparison section.

- **QG+F BH predictions (Lichnerowicz, solution families, fakeon selects Schwarzschild, Wald entropy, QNMs, etc.)** → SKIPPED. Already comprehensively covered by `quadratic-gravity-fakeon/black-hole-predictions.md`.

- **AS BH predictions (Bonanno-Reuter, singularity resolution, de Sitter core, Planck remnants, α > 1)** → SKIPPED. Already comprehensively covered by `asymptotic-safety/black-holes-and-singularity-resolution.md`.

- **QCD analogy structural mapping table** → SKIPPED. Already in `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md` with even more detail (7 breakdown points, IHO interpretation, mass gap).

- **Holdom-Ren phase transition conjecture** → SKIPPED. Already in `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md`.

- **Branch crossing at r_H ≈ 0.876/m₂** → SKIPPED as standalone fact. Already in `quadratic-gravity-fakeon/black-hole-predictions.md` line 26 and Silveravalle-Zuccotti phase diagram (line 28-30). The three-scenario instability analysis (EXCLUDED/EXCLUDED/only viable) is captured in the new compatibility file as Argument 3.

- **Anselmi 2026 non-perturbative uncertainty** → SKIPPED. Already in `quadratic-gravity-fakeon/black-hole-predictions.md` line 40.

- **Bonanno 2025 spontaneous ghostification** → SKIPPED as standalone. Already in `quadratic-gravity-fakeon/black-hole-predictions.md` lines 53-55 and `cross-cutting/information-paradox.md`. The 3-possibility analysis for QG+F=AS implications is captured in the new compatibility file.

- **Ghost fate mechanisms (4 mechanisms, INCONCLUSIVE)** → SKIPPED. Already in `asymptotic-safety/ghost-fate-strong-coupling.md`.

- **Draper complex pole tower** → SKIPPED. Already in `asymptotic-safety/ghost-fate-strong-coupling.md`.

- **Planck remnant consistency argument** → captured in new compatibility file (section "Planck Remnants: No Internal Inconsistency"). Not a standalone finding — it's an argument within the compatibility analysis.

- **Perturbative expansion breaks down at M ~ M_P** → SKIPPED. Already in `quadratic-gravity-fakeon/black-hole-predictions.md` line 10 and `asymptotic-safety/black-holes-and-singularity-resolution.md` lines 62-66.

### Summary: Added 1 new entry (qgf-vs-as-bh-compatibility: systematic SUPPORTS verdict with five-argument structure), updated 2 existing (black-hole-predictions: conclusion reframed from "tension" to "compatible"; black-holes-and-singularity-resolution: large-r agreement + cross-ref), skipped 10 duplicates (all individual BH facts already well-catalogued across 5 existing files). No conflicts. Index files updated (cross-cutting: 25 → 26, root: 147 → 148).

---

## 2026-03-26 Processing: exploration-001-challenger-survey-selection.md (nature-of-time strategy-002)

### Report Summary

Systematic survey and scored comparison of five non-computational interpretations of time against a six-feature benchmark (one-dimensionality, irreversibility, directionality, open future, flow, dilation), to select the strongest challenger to the computational interpretation. Candidates: (A) Causal Fundamentalism (Maudlin/Sorkin/CST), (B) Thermodynamic Realism (Prigogine), (C) Experience-First (Bergson/Husserl/IIT), (D) Causal-Processual Hybrid, (E1) Smolin temporal naturalism, (E2) Retrocausal (rejected), (E3) Rovellian (rejected). Winner: Causal-Processual Hybrid (36/40). Includes detailed initial sketch of the selected challenger.

### Findings extracted:

- **Systematic comparative survey: six-feature benchmark + five candidate scored assessments + selection rationale** → filed at `cross-cutting/time-interpretation-challenger-survey.md` (NEW). Core new content: the six-feature benchmark formalized; five candidate interpretations scored on features (1-5) and four meta-criteria; comparative scoring matrix; Husserl's temporal phenomenology (retention/protention structure) and IIT's temporal structure — both genuinely new to library; retrocausal rejected (9/30), Rovellian rejected as CI-adjacent; selection of causal-processual hybrid with justification.

- **Causal-Processual Interpretation of Time: initial sketch** → filed at `cross-cutting/causal-processual-interpretation.md` (NEW). Core new content: a constructed synthesis of causal fundamentalism + process metaphysics + thermodynamic irreversibility + temporal naturalism; core claim (time is irreversible causal process of becoming); six-feature explanations at detail (one-dimensionality from seriality of concrescence, irreversibility at causal and processual levels, triple-grounded directionality without Past Hypothesis, Whiteheadian creativity + CST stochasticity + Smolin law evolution for open future, flow as concrescence, dilation from causal event density); five advantages over CI; five honest weaknesses (coherence risk, formalization, "now" still weak, flow partly assertive, phenomenology gap); development roadmap (actualization as unifying principle, Baron-Le Bihan 2025 CST-Whitehead bridge, category theory formalization).

- **Causal Fundamentalism assessment with six-feature scores (20/30 features, 35/40 grand total)** → SKIPPED as standalone entry. Substance (Maudlin, CST sequential growth, Sorkin) already well-covered in `cross-cutting/temporal-realism-irreducible-becoming.md`. The formal scoring is new but captured in the survey file. Cross-reference added to temporal-realism entry.

- **Thermodynamic Realism standalone assessment (16/30 features, 26/40 grand total)** → SKIPPED as standalone entry. Prigogine content (non-unitary transformations, Poincare resonances, dissipative structures) already covered in `cross-cutting/temporal-realism-irreducible-becoming.md`. The formal scoring and standalone evaluation are captured in the survey file.

- **Smolin Temporal Naturalism standalone assessment (16/30 features, 27/40 grand total)** → SKIPPED as standalone entry. Already covered in `cross-cutting/temporal-realism-irreducible-becoming.md`. Scores captured in survey.

- **Retrocausal / Two-State Vector assessment (9/30 features, rejected)** → SKIPPED as standalone entry. Brief assessment, verdict "not viable," captured in survey file.

- **Relational / Rovellian assessment (rejected as CI-adjacent)** → SKIPPED as standalone entry. Already covered in `cross-cutting/three-layer-time-synthesis.md` relational alternative section. The verdict that it's too close to CI's Layer 1 is captured in survey file.

- **CI benchmark (five weaknesses of computational interpretation)** → SKIPPED. Already fully covered in `cross-cutting/computational-irreducibility-thesis.md` under "What the Thesis Struggles With." The six-feature scoring is implicit throughout that entry.

### Summary: Added 2 new entries (time-interpretation-challenger-survey, causal-processual-interpretation), updated 1 existing entry (temporal-realism-irreducible-becoming: added cross-references to survey and hybrid), updated all INDEX files (cross-cutting 32 → 34, root 154 → 156), skipped 6 findings already covered or captured in new entries, resolved 0 conflicts.

---

## 2026-03-26 Processing: exploration-002-causal-processual-construction.md (nature-of-time strategy-002)

### Report Summary

Deep construction of the Causal-Processual Interpretation of Time. Fulfills the development roadmap from E001: finds the unifying principle (actualization), develops all six feature-explanations to full depth with physics grounding, strengthens flow (Husserlian-Whiteheadian bridge) and dilation (CST chain-length-as-proper-time), builds a perspectival-processual account of the "now," provides detailed head-to-head CI comparison. Total score upgraded from 23/30 to 26/30.

### Findings extracted:

- **Actualization as unifying principle (definition, four-tradition mapping, Heisenberg potentia connection, Kastner-Kauffman 2017)** → updated existing `cross-cutting/causal-processual-interpretation.md` (MAJOR UPGRADE — "Initial Sketch" → "Full Construction"). The central new content: actualization formally defined (irreversible, creative, relational, constitutive of time); each tradition mapped onto it; quantum connection via Heisenberg's potentia and Kastner-Kauffman (2017).

- **Irreversibility upgrade (4→5): ontological, causal-structural, Prigoginian, generalized second law arguments** → updated existing `cross-cutting/causal-processual-interpretation.md` (deepened feature explanation). Key new content: Baron & Le Bihan (2025) actual causation argument, generalized second law (actualization as monotonically non-decreasing definiteness), explicit argument that LBB is a consequence not a source.

- **Flow upgrade (3→4): Husserl's retention-primal impression-protention structure, Bergson's durée, concrescence = specious present bridge** → updated existing `cross-cutting/causal-processual-interpretation.md` (substantially expanded). Key new content: four-part mapping (prehension→retention, concrescence→primal impression, subjective aim→protention, perishing→fading), self-defeating argument, Bergson's durée as qualitative character.

- **Dilation upgrade (3→4): CST chain-length-as-proper-time, hauptvermutung, processual interpretation** → updated existing `cross-cutting/causal-processual-interpretation.md` (substantially expanded). Key new content: Myrheim's proper-time conjecture (confirmed in flat spacetime), gravitational dilation as sparser timelike elements, ontological interpretation (real variation in rate of becoming).

- **The "Now" — perspectival-processual account** → updated existing `cross-cutting/causal-processual-interpretation.md` (NEW SECTION). Each actualization event IS a now; no global now (compatible with SR); "why THIS now?" answered via indexicality; ontological past/present/future distinction as advantage over CI.

- **Head-to-head CI comparison (feature table, meta-criteria table, where each wins)** → updated existing `cross-cutting/causal-processual-interpretation.md` (NEW SECTION). CP wins: directionality, flow, "now", novel predictions. CI wins: physics grounding, safety, parsimony. Roughly even: one-dimensionality, dilation.

- **Convergence risk with CI (new weakness: is actualization just computation?)** → updated existing `cross-cutting/causal-processual-interpretation.md` (added to weaknesses). Key new content: if actualization is information-processing, it might collapse to CI in metaphysical language; claimed difference: creative vs. mechanical.

- **Final formulation (one-paragraph statement)** → updated existing `cross-cutting/causal-processual-interpretation.md` (replaced development roadmap). The interpretation's core claim in polished form.

- **Revised scores in challenger survey (23/30→26/30, grand total 36→39)** → updated existing `cross-cutting/time-interpretation-challenger-survey.md` (updated D section and scoring matrix).

- **Detailed one-dimensionality arguments (topological, processual, information-theoretic)** → SKIPPED as standalone entry. Deepens E001's explanation but doesn't change the score (still 4/5). Captured in updated main entry.

- **Detailed open future arguments (processual creativity, CST stochastic, law evolution, quantum connection)** → SKIPPED as standalone entry. Deepens E001's explanation but doesn't change the score (still 4/5). Captured in updated main entry.

- **Detailed directionality arguments (triple-grounding expansion, no Past Hypothesis argument)** → SKIPPED as standalone entry. Deepens E001's explanation but doesn't change the score (still 5/5). Captured in updated main entry.

- **CST sequential growth dynamics details (Rideout-Sorkin, general covariance, Bell causality)** → SKIPPED. Already covered in `causal-set-theory/dynamics.md`. The report's use of these is captured in the updated main entry's physics anchors.

- **Whiteheadian concrescence detailed mechanics (prehension, subjective aim, satisfaction, perishing)** → SKIPPED as standalone entry. Philosophical framework rather than a physics finding; captured in the main entry's feature explanations. Not suitable for the factual library as a standalone.

- **Prigogine's non-unitary transformation theory details** → SKIPPED as standalone entry. Already referenced in `temporal-realism-irreducible-becoming.md`. The specific physics (Poincaré resonances, semigroup evolution) is captured in the updated main entry.

- **Baron & Le Bihan (2025) actual causation analysis** → SKIPPED as standalone entry. Already cited in E001 entry's development roadmap. Now fully incorporated into the updated main entry's actualization section and irreversibility argument.

- **Honest assessment: mixed physics grounding, panexperientialism tension, formalization gap, block universe commitment** → SKIPPED as standalone entries. These are weaknesses of the interpretation itself, not independent findings. Captured in the updated main entry's weaknesses section.

### Summary: Added 0 new entries, updated 2 existing entries (causal-processual-interpretation.md — major upgrade from "Initial Sketch" to "Full Construction" with actualization as unifying principle, upgraded scores, new sections on "the now" and CI comparison; time-interpretation-challenger-survey.md — revised scores 23→26, grand total 36→39), updated all INDEX files (cross-cutting description updated, root description updated, no count changes), skipped 8 findings already covered or captured in updated entries, resolved 0 conflicts.

---

## 2026-03-26 Processing: exploration-s4-004-higgs-mass-consistency.md (quantum-gravity-2 strategy-004)

### Report Summary

Determines whether the fakeon prescription for the gravitational ghost affects the Shaposhnikov-Wetterich (SW) Higgs mass prediction (m_H ≈ 126 GeV). Analyzes three channels of potential influence (perturbative beta functions, NGFP boundary condition, threshold corrections), derives quantitative upper bound |Δm_H| < 10⁻⁷ GeV, and classifies the result as a CONSISTENCY CHECK — inherited from AS, not a novel prediction. Also covers the Eichhorn-Held top mass refinements (also unaffected) and identifies the key residual open calculation (A_λ in C²-extended FRG truncation).

### Findings extracted:

- **Full Higgs mass consistency check (three independent arguments, quantitative bound, uncertainty comparison table, structural robustness, Eichhorn-Held extension, residual questions)** → filed at `cross-cutting/unified-qgf-as-framework/higgs-mass-consistency.md` (NEW). Core new content: (1) UV divergences / beta functions prescription-independent (Anselmi 2022 explicit confirmation); (2) NGFP is Euclidean → prescription-indistinguishable (D'Angelo et al. 2025 Euclidean-Lorentzian universality class); (3) absorptive part vanishes below M₂ threshold (kinematic suppression by (m_H/M_Pl)²); conservative bound |Δm_H| < 10⁻⁷ GeV; uncertainty comparison table showing fakeon is smallest of all corrections; "topological" nature of SW prediction (depends on SIGN of A_λ only); C² ghost already implicit in AS via Benedetti et al. NGFP; Eichhorn-Held and dark portal extensions also unaffected; residual: A_λ in C²-extended FRG. Classification: CONSISTENCY CHECK, not novel.

- **Prediction #7 (Higgs mass consistency) RESOLVED** → updated existing `cross-cutting/unified-qgf-as-framework/novel-predictions.md` (significant revision). Previously posed two open questions ("Does the fakeon affect λ_H running?" and "Do NGFP boundary conditions survive?"). Now marked RESOLVED ✓ with answers (No and Yes), quantitative bound, three-argument summary, classification as non-novel, and cross-reference to detailed analysis.

- **SW prediction uncertainty budget (m_top ±3 GeV dominant, α_s ±1 GeV, higher-loop ±0.5 GeV) and "topological" robustness** → updated existing `asymptotic-safety/standard-model.md` (added specificity). Previously had "only a few GeV uncertainty (from M_top uncertainty)"; now has detailed breakdown with δm_H ≈ 1 GeV per 1 GeV shift in m_top, original m_top ≈ 171 GeV, current world average, α_s and higher-loop contributions. Added "topological" structural robustness note. Added Einstein-Hilbert truncation limitation (C² not included). Added full fakeon compatibility paragraph with cross-reference to detailed analysis.

- **SW mechanism detailed reconstruction (β_λ = β_λ^SM + A_λ·λ, metastability boundary correspondence, sensitivity analysis)** → SKIPPED as standalone entry. The mechanism is already covered in `asymptotic-safety/standard-model.md` with the key formula and logic. The report adds pedagogical detail but no new factual content beyond the uncertainty budget (which was captured in the update above).

- **Perturbative one-loop ghost correction to β_λ from agravity (Salvio-Strumia 2014)** → SKIPPED as standalone entry. Technical detail supporting the prescription-independence argument. The conclusion (fakeon doesn't change beta functions) is the library-worthy fact, and it's captured in the new higgs-mass-consistency entry. The specific agravity RGE formula (5f₂⁴M̄_Pl²/6) is supporting detail, not a standalone finding.

- **Euclidean FRG prescription-independence argument** → SKIPPED as standalone entry. This is one of the three pillars of the consistency check, fully captured in the new entry. Not a standalone finding — it's a specific application of the general fact that Euclidean computations are prescription-independent, which is standard QFT.

- **Threshold correction analysis at M₂ ~ M_Pl** → SKIPPED as standalone entry. Third pillar of the consistency check. Fully captured in the new entry. The key physics (θ(p² − 4M₂²) = 0 below threshold) is standard.

- **Two-loop absorptive suppression estimate ((m_H/M₂)² ≈ 10⁻³²)** → SKIPPED as standalone entry. Quantitative detail within the bound derivation, captured in the new entry.

- **Eichhorn-Held top mass prediction unaffected** → SKIPPED as standalone entry. The conclusion is captured in the new higgs-mass-consistency entry. No new information about the Eichhorn-Held mechanism itself — just the application of the same three arguments.

- **Dark portal extension (Eichhorn et al. JHEP 10, 2021) unaffected** → SKIPPED as standalone entry. Same reasoning as Eichhorn-Held above. Captured in new entry.

- **"What would make this novel" (if fakeon shifted λ(M_Pl) from 0 to ε > 0)** → SKIPPED. Counterfactual analysis with pedagogical value but no factual content. The conclusion (shift is effectively zero) is the library fact.

- **Three residual open questions (Lorentzian NGFP, higher-loop thresholds, A_λ in C²-extended truncation)** → SKIPPED as standalone entries. Captured in the new entry's Residual Open Questions section. The key open calculation (A_λ in C²-extended FRG) is noted there and could be added to `open-problems.md` in a future curation pass if deemed important enough.

- **Detailed source list (Shaposhnikov-Wetterich, Eichhorn-Held, Anselmi, Benedetti et al., D'Angelo et al., Salvio-Strumia, Dona-Eichhorn-Percacci, Baldazzi-Percacci-Skrinjar, Manrique-Reuter-Saueressig)** → SKIPPED. All sources already in library. No new papers identified.

### Summary: Added 1 new entry (higgs-mass-consistency), updated 2 existing entries (novel-predictions #7 → RESOLVED, standard-model uncertainty budget + fakeon compatibility), updated all INDEX files (3 levels: unified-framework 6→7, cross-cutting 36→37, root 158→159), skipped 10 findings (mechanism reconstruction, technical argument pillars, two-loop estimate, Eichhorn-Held/dark portal extensions, counterfactual, residual questions, sources — all captured in new/updated entries), resolved 0 conflicts.

---

## 2026-03-26 Processing: exploration-004-tournament-ci-vs-cp.md (nature-of-time strategy-002)

### Report Summary

Formal 13-criterion head-to-head tournament between the Computational Interpretation (CI) and the Causal-Processual Interpretation (CP) of time. Six feature rounds (one-dimensionality, irreversibility, directionality, open future, flow, dilation), four "hardest questions" rounds (why does time flow, why can't we go back, what is "now," does time exist without observers), three meta-criteria (physics grounding, explanatory depth, boldness with honesty). Result: CP wins 48.5–47.5, a near-draw (1.0 margin out of 65). CP advantages: directionality (+1.5), "now" (+1.5), explanatory depth (+1.0). CI advantages: physics grounding (+2.5), irreversibility/LBB engine (+1.0). Key convergence insight: both interpretations point to "an irreversible, one-way process that generates novelty and cannot be shortcut."

### Findings extracted:

- **Full tournament results (13-criterion scoring, grand totals, verdict, convergence insight, honest caveats, round highlights)** → filed at `cross-cutting/ci-vs-cp-tournament.md` (NEW). Core new content: complete 13×2 scoring table, category subtotals (P1: CI 21.5 vs CP 22.5, P2: CI 13.5 vs CP 15.0, P3: CI 12.5 vs CP 11.0), three reasons CP edges ahead, three reasons CI nearly ties, the fundamental trade-off (safer/rigorous vs deeper/ambitious), convergence insight (both point to same deep structure), four honest caveats (fragile margin, vocabulary effect, CI more likely correct, CP more fragile), scoring methodology note (tournament vs self-assessment).

- **CI tournament scores (first formal scoring of CI on all six features + four questions + three meta-criteria)** → updated existing `cross-cutting/computational-irreducibility-thesis.md` (added tournament results section). New content: CI feature scores (21.5/30), strengths (physics grounding 5.0/5, LBB engine 4.5/5), weakness ("now" 2.5/5), convergence insight, cross-reference to tournament.

- **CP tournament scores (E004 column in score history)** → updated existing `cross-cutting/causal-processual-interpretation.md` (expanded score history table). New content: E004 tournament column with scores (3.5, 4.0, 4.5, 3.5, 3.5, 3.5 = 22.5/30), tournament note explaining methodology difference and grand total (CP 48.5 vs CI 47.5), cross-reference to tournament.

- **Tournament result summary for challenger survey** → updated existing `cross-cutting/time-interpretation-challenger-survey.md` (added tournament result paragraph under CP section). New content: 1-paragraph summary of E004 tournament result with key gaps and verdict.

- **CI's LBB engine as "most compelling single argument" in tournament** → SKIPPED as standalone entry. Already fully captured in computational-irreducibility-thesis.md. The tournament confirms without adding new mechanistic content.

- **CI's "now" acknowledged as weakest point (2.5/5)** → SKIPPED as standalone entry. Already noted in computational-irreducibility-thesis.md ("Moderate — current computational state"). Tournament confirms and provides quantitative score, captured in tournament file and CI thesis update.

- **CP's directionality as strongest feature (4.5/5 in tournament, +1.5 over CI)** → SKIPPED as standalone entry. Already captured in causal-processual-interpretation.md and cp-adversarial-assessment.md. Tournament confirms with quantitative comparison; captured in tournament file.

- **Individual round-by-round arguments (6 feature rounds + 4 question rounds)** → SKIPPED as standalone entries. These are detailed argumentation supporting the scores, not independent findings. The key arguments are already captured in existing CI and CP thesis files. The tournament file captures the scoring and highlights.

- **"CP's advantage is partly vocabulary" caveat** → SKIPPED as standalone entry. This refines the E003 convergence finding (structural isomorphism) without adding new content. Captured in tournament file's honest caveats section.

- **"CI more likely correct" assessment** → SKIPPED as standalone entry. This is a meta-judgment on scoring, not a factual finding. Captured in tournament file's honest caveats.

- **Ness et al. 2021 experimental confirmation of ML bound** → SKIPPED. Already cited in computational-irreducibility-thesis.md ("Margolus-Levitin theorem... a fundamental physical limit"). Tournament cites it as established confirmation; no new information.

- **Aimet et al. 2025 Landauer confirmation** → SKIPPED. Already cited in computational-irreducibility-thesis.md ("Bérut et al. 2012, Landauer experimental confirmation"). The 2025 citation adds a second confirmation but no new physical content beyond "also confirmed."

- **Wolpert's impossibility theorem (2008)** → SKIPPED. Already captured in computational-irreducibility-thesis.md via the "computational irreducibility" discussion. Mentioned in tournament CI arguments but no new content.

### Summary: Added 1 new entry (ci-vs-cp-tournament), updated 3 existing entries (computational-irreducibility-thesis with tournament results section, causal-processual-interpretation with E004 score history column and tournament note, time-interpretation-challenger-survey with tournament result paragraph), updated all INDEX files (2 levels: cross-cutting 37→38, root 159→160), skipped 9 findings (LBB engine, "now" weakness, directionality strength, round arguments, vocabulary caveat, CI-more-likely, Ness 2021, Aimet 2025, Wolpert — all confirmatory or captured within new/updated entries), resolved 0 conflicts.

---

## 2026-03-26 Processing: exploration-005-meta-interpretation-determination.md (nature-of-time strategy-002)

### Report Summary

CI+CP meta-interpretation: "Time as Irreversible Determination." Synthesizes the Computational Interpretation and the Causal-Processual Interpretation into a single framework. Core claim: "Time is irreversible determination — the ongoing, physically constrained process by which the indeterminate becomes determinate, as encountered from within." Identification of "determination" as a unified concept subsuming CI's "computation" and CP's "actualization." Takes CP's position on the convergence fork (potentialities are ontologically real). Resolves three tensions (computation vs. actualization, Past Hypothesis, the "now"). Feature-by-feature construction scoring 57.0/65 on same 13 tournament criteria (+8.5 over CP's 48.5, +9.5 over CI's 47.5). Six honest limits. No novel predictions.

### Findings extracted:

- **Full meta-interpretation "Time as Irreversible Determination" (core claim, determination concept, convergence fork resolution, 3 tension resolutions, 13-criterion score table, feature constructions, honest limits, self-critique, final statement)** → filed at `cross-cutting/meta-interpretation-determination.md` (NEW). Core new content: "determination" as unified concept subsuming computation and actualization; potentialities-are-real position with explicit cost analysis; three tension resolutions (computation/actualization as two aspects, PH reframed as minimal initial determination, "now" as locus of active determination); full 13-criterion score table (57.0/65); feature constructions for irreversibility (5.0), flow (4.0 via retention-impression-protention), directionality (4.5); 6 honest limits; self-critique assessment; final statement with 6-element unpacking.

- **Synthesis outcome for tournament (57.0/65, +8.5 over best parent)** → updated existing `cross-cutting/ci-vs-cp-tournament.md` (added Synthesis Outcome section and cross-reference). New content: paragraph summarizing that convergence insight motivated the synthesis, 57.0/65 score, complementary weakness structure, link to full construction.

- **CI subsumed as constraint-level description of determination** → updated existing `cross-cutting/computational-irreducibility-thesis.md` (added cross-reference to meta-interpretation). No content change to CI thesis itself — cross-reference only.

- **CP subsumed as ontological-level description of determination** → updated existing `cross-cutting/causal-processual-interpretation.md` (added cross-reference to meta-interpretation). No content change to CP thesis itself — cross-reference only.

- **Three-layer synthesis related as alternative approach** → updated existing `cross-cutting/three-layer-time-synthesis.md` (added cross-reference to meta-interpretation as alternative synthesis from Strategy 002).

- **Individual feature-by-feature constructions (one-dimensionality, irreversibility, directionality, open future, flow, dilation)** → SKIPPED as standalone entries. These are constituent parts of the meta-interpretation, not independent findings. All captured comprehensively in the new entry.

- **Three tension resolutions (computation vs. actualization, Past Hypothesis, the "now")** → SKIPPED as standalone entries. These are structural elements of the synthesis, not standalone findings. Captured in the new entry.

- **The convergence fork resolution (potentialities are real)** → SKIPPED as standalone entry. This is a position taken within the synthesis, not an independent finding. Captured in the new entry's dedicated section.

- **The "natural initial condition" Past Hypothesis reframing** → SKIPPED as standalone entry. Part of Tension 2 resolution. Not a standalone finding — a philosophical argument within the synthesis.

- **The self-critique and score validation** → SKIPPED as standalone entry. Meta-reasoning about the synthesis, not an independent finding. Captured in new entry's self-critique section.

- **CI's tournament scores, CP's tournament scores (already in ci-vs-cp-tournament.md)** → SKIPPED. Already captured in existing entry. The synthesis reproduces the same scores — no new information about CI or CP individually.

- **Retention-impression-protention mapping to inheritance-determination-openness** → SKIPPED as standalone entry. This is the flow construction within the synthesis. Captured in new entry's flow section. Not new — extends the CP Husserlian mapping already in causal-processual-interpretation.md.

- **"No novel predictions" honest limit** → SKIPPED as standalone entry. Captured in new entry's honest limits section.

- **Prigogine dependency weakening** → SKIPPED as standalone entry. Part of the synthesis's honest limits. The CP entry already notes Prigogine's contested status; the synthesis's repositioning is captured in the new entry.

### Summary: Added 1 new entry (meta-interpretation-determination), updated 4 existing entries (ci-vs-cp-tournament with synthesis outcome section, computational-irreducibility-thesis with cross-reference, causal-processual-interpretation with cross-reference, three-layer-time-synthesis with cross-reference), updated all INDEX files (2 levels: cross-cutting 38→39, root 160→161), skipped 9 findings (feature constructions, tension resolutions, convergence fork, PH reframing, self-critique, CI/CP scores, retention mapping, no-novel-predictions, Prigogine — all captured within new/updated entries), resolved 0 conflicts.

---

## 2026-03-27 Processing: exploration-001-gue-pair-correlation-spacing.md (riemann-hypothesis strategy-001)

### Report Summary

Computational study of the first 2,000 non-trivial Riemann zeta zeros and 500 zeros near n=10,000. Tests pair correlation against Montgomery's conjecture and nearest-neighbor spacing against GUE Wigner surmise. Performs ensemble discrimination (GUE vs. GOE vs. GSE vs. Poisson). Extracts constraints on the hypothetical Riemann operator. Both statistics confirm GUE at high precision. This is the first entry in the library for the Riemann hypothesis mission — entirely new domain.

### Findings extracted:

- **GUE pair correlation match (Montgomery's conjecture)** → filed at `riemann-hypothesis/gue-pair-correlation.md` (NEW). 9.1% mean relative deviation for first 2,000 zeros (STRONG MATCH); 17.2% at high height (MODERATE, sample-limited); chi-squared/dof = 1.50 (slightly elevated, possibly unfolding inaccuracy); 68% of bins within 1-sigma (exactly Gaussian); no height dependence detected; Odlyzko confirms strengthening at t~10^20; full methodology (mpmath, unfolding formula, bin width, computation rates).

- **GUE nearest-neighbor spacing and ensemble discrimination** → filed at `riemann-hypothesis/gue-nearest-neighbor-spacing.md` (NEW). 4.1% mean absolute deviation from Wigner surmise (STRONG MATCH); KS test marginally fails at 5% but this reflects Wigner surmise approximation error, not GUE departure; ensemble discrimination: GUE definitively beats GOE (2x) and Poisson (5x), suggestively beats GSE (1.2x); ordering consistent at both heights; quadratic level repulsion confirmed.

- **Constraints on hypothetical Riemann operator** → filed at `riemann-hypothesis/riemann-operator-constraints.md` (NEW). Definitively rules out Poisson (integrable/diagonal systems), GOE (real symmetric operators with time-reversal symmetry); disfavors GSE (Kramers degeneracy); operator must act on complex Hilbert space, break time-reversal symmetry, have complex matrix elements, exhibit quadratic level repulsion; no systematic deviations from GUE detected.

- **Computation of 2,000 low-height + 500 high-height zeros** → SKIPPED as standalone entry. Methodology details folded into pair-correlation entry. The raw computation is infrastructure, not a finding.

- **Height dependence analysis** → SKIPPED as standalone entry. Folded into pair-correlation entry. No evidence of height dependence; increased deviations at high height fully explained by 4x smaller sample.

- **Point-by-point comparison tables** → SKIPPED as standalone entries. Detailed bin-by-bin data captured within the relevant finding entries.

### Summary: Added 3 new entries (gue-pair-correlation, gue-nearest-neighbor-spacing, riemann-operator-constraints), created 1 new folder (riemann-hypothesis/), updated 1 INDEX file (root factual — 164→167, new top-level category), skipped 3 items (computation setup, height dependence, detailed tables — all folded into new entries), resolved 0 conflicts.

---

## 2026-03-27 Processing: meta-exploration-001.md (riemann-hypothesis strategy-001, meta-learning)

### Report Summary

Meta-learning note from a divergent conceptual survey exploration. Reports on what worked (survey+deep dive+synthesis scope, honest novelty assessment, naming specific programs, temporal recency specification) and what could be improved (schematic synthesis, lack of claim attribution). The note appears to describe quantum-gravity exploration 001 (references "7 named programs," Oppenheim, Barandes, etc.) but was filed in the riemann-hypothesis meta-inbox.

### Findings extracted:

- **Divergent survey four-part pattern (survey + deep dive + synthesis + novelty assessment)** → SKIPPED. Already comprehensively captured in `meta/methodology/divergent-survey-pattern.md` (source: strategy-001 meta-001, meta-002). Same lesson, same evidence (strategy-001 exploration 001). No new information.

- **"Honestly assess novelty" produces quality critical analysis** → SKIPPED. Already captured in `meta/methodology/divergent-survey-pattern.md` ("ask for honesty explicitly"). No new information.

- **Name specific programs + "any others you find"** → SKIPPED. Already captured in `meta/goal-design/name-specific-authors-and-papers.md` (source includes strategy-001 meta-001 with identical evidence: "7 named programs," finding Oppenheim, Barandes, Doukas, etc.). No new information.

- **"Focus on recent (2024-2026)" temporal specification** → filed at `meta/goal-design/specify-temporal-recency.md` (NEW). Explicit time windows in goals produce genuinely current results rather than established older references. Single-observation evidence.

- **Ask for equations/derivations for construction tasks** → filed at `meta/goal-design/request-equations-for-construction.md` (NEW). Without explicit request for mathematical specificity, synthesis output is "compelling but schematic." Single-observation evidence.

- **Require claim attribution (sourced vs. own reasoning)** → filed at `meta/goal-design/require-claim-attribution.md` (NEW). Explorer reports blend literature findings and original analysis without distinction unless explicitly instructed. Single-observation evidence.

- **Don't add construction on top of survey** → SKIPPED. Already captured in `meta/methodology/divergent-survey-pattern.md` ("Do NOT add construction on top -- that needs its own exploration"). No new information.

### Summary: Added 3 new meta entries (specify-temporal-recency, request-equations-for-construction, require-claim-attribution), updated 2 INDEX files (goal-design 7→10, meta root), skipped 4 lessons (divergent survey pattern, honest novelty, name specific targets, no construction on survey — all already in existing entries), resolved 0 conflicts.

---

## 2026-03-27 Processing: exploration-002-number-variance-spectral-rigidity.md (riemann-hypothesis strategy-001)

### Report Summary

Long-range spectral statistics of the first 2,000 Riemann zeta zeros: number variance Σ²(L), spectral rigidity Δ₃(L), and spectral form factor K(τ). Three-way comparison (zeta vs. GUE simulation vs. GUE theory) definitively confirming Berry's (1985) saturation prediction. Full data tables for all three statistics. Updated constraint catalog combining explorations 001 and 002 (10 total constraints). 372 lines.

### Findings extracted:

- **Berry's saturation confirmed (Σ² and Δ₃)** → filed at `riemann-hypothesis/berry-saturation-confirmed.md` (NEW). Number variance saturates at ~0.3–0.5 for L>2 (growth rate 12× below GUE sim, 34× below GUE theory). Spectral rigidity saturates at 0.156 for L>15 (constant to L=100). Both statistics show zeta zeros are 30–50% more rigid than GUE at large scales. Prime periodic orbits cause the saturation.

- **Spectral form factor K(τ) GUE match** → filed at `riemann-hypothesis/spectral-form-factor-gue.md` (NEW). Ramp slope = 1.010 (1% of GUE), plateau = 1.043 ± 0.077 (4.3% of GUE). Indistinguishable from GUE simulation. Confirms GUE universality class through Fourier-space statistics.

- **Periodic orbit constraints on Riemann operator** → updated existing `riemann-hypothesis/riemann-operator-constraints.md` (added periodic orbit structure: chaotic classical dynamics, shortest periods ~ log p, super-rigidity, no missing structure detected).

- **Combined 10-constraint catalog (explorations 001+002)** → SKIPPED as separate file. Constraints 1–4 already in `riemann-operator-constraints.md`, constraints 5–10 now added to same file. The numbered list in the report is a summary, not a new finding.

- **Saturation scale analysis (L_max prediction vs. observation)** → INCORPORATED into `berry-saturation-confirmed.md` rather than separate file (it's a detail of the Berry saturation finding, not an independent finding).

- **Methodology details (computation times, statistical adequacy, systematic errors)** → SKIPPED. Methodological notes, not findings. Useful context preserved in the source report.

### Summary: Added 2 new entries, updated 1 existing, skipped 2 (combined catalog = summary of filed findings; methodology = not a finding), resolved 0 conflicts.

---

## 2026-03-27 Processing: meta-exploration-002.md (riemann-hypothesis meta-inbox, QG-2 content)

### Report Summary

Meta-learning note from QG-2 exploration 002. Confirms divergent-survey pattern, notes constraint checklist effectiveness, reinforces equations-for-construction lesson, and introduces the "separate leads into dedicated explorations" principle.

### Findings extracted:

- **"Confirmed this is the right pattern for Phase 1 divergent explorations"** → SKIPPED. Already fully captured in `meta/methodology/divergent-survey-pattern.md` with the same lesson and evidence from strategy-001 meta-002. No new information.

- **"Checking against specific constraints produced structured, useful assessment"** → updated existing `meta/goal-design/use-classification-schemes.md` (added "Variant: Constraint Checklists" section — providing an explicit list of constraints to check proposals against produces structured point-by-point assessment, distinct from severity/type classification).

- **"Asking 'is this genuinely new or repackaging?' got honest, nuanced answer"** → SKIPPED. Already captured in `meta/methodology/divergent-survey-pattern.md` evidence section ("Asking 'is this genuinely new or repackaging?' got a nuanced answer").

- **"Construction explorations need specific calculations or derivations"** → SKIPPED. Already fully captured in `meta/goal-design/request-equations-for-construction.md`.

- **"Most intriguing lead should be FOCUS of dedicated construction exploration"** → SKIPPED. Already captured in `meta/methodology/divergent-survey-pattern.md` ("Do NOT add construction on top — that needs its own exploration").

- **"Explorer could have been more specific about Pedraza cost function lead"** → SKIPPED. Data point reinforcing the "separate leads" lesson already captured. No new actionable insight.

### Summary: Added 0 new entries, updated 1 existing (use-classification-schemes +constraint checklist variant), skipped 5 (all already covered by existing entries), resolved 0 conflicts.
