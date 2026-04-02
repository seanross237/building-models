---
topic: Run adversarial check between Phase 2 and Phase 3, not just after Phase 3
category: methodology
date: 2026-03-27
source: "stochastic-electrodynamics strategy-001 meta-exploration-006, thermal-time strategy-002 meta-exploration-001"
---

## Lesson

Run a **lightweight adversarial check after Phase 2** (numerical/construction phase) and **before committing to Phase 3** (extended computation phase). Early reframing is far more valuable than corrections after the long computation is done. Specifically: after the first quantitative findings are in, have an explorer ask "which of these findings are genuinely novel vs. known?" and "which are artifacts of the approximation vs. fundamental physics?" before designing the next expensive explorations.

## Evidence

- **SED strategy-001 exploration-006** — Adversarial review at Phase 3 reframed Finding 2 (Langevin failure) as "approximation artifact, not SED fundamental failure." This reframing would have sharpened E004's goal significantly if known before E004 was run. Similarly, downgrading Finding 4 (linearity boundary) from "novel" to "known since Boyer 1975" should have happened before designing the full E005 scan — the key novelty question is about F3 (ALD result), not F4.

## When the Cost Is Highest

The cost of late adversarial reframing scales with how much Phase 3 computation has already been committed:
- If reframing happens after 1 computation exploration: saves 1 misdirected exploration
- If reframing happens before Phase 3: saves potentially 3-5 misdirected explorations

## Lightweight Adversarial Format

For the between-phases adversarial check, a focused prompt works better than a full adversarial review:

1. "For each finding so far, is this known in the literature or genuinely new?"
2. "Which findings are artifacts of the approximation used vs. intrinsic to the physics?"
3. "What is the single most important remaining check that would change the narrative?"

This takes ~1 exploration instead of the ~3 explorations a full adversarial review requires.

## Strong Upgrade: Run Full Adversarial EARLY (E008)

**compton-unruh strategy-001 exploration-008** strengthens this lesson substantially. The full
adversarial exploration (E008) at exploration 8 revealed:
- The Bullet Cluster objection is **the standard observational test** for any modified gravity/inertia
  proposal — and it decisively falsifies the modified inertia interpretation
- This objection would have been caught at exploration 3 or 4, saving 4–5 explorations of
  construction and refinement on a model that is observationally falsified at cluster scales

The lesson upgrade: **a standard-test adversarial check** (listing the 5–10 canonical tests for the
model class and computing each one) is MORE valuable than the lightweight "novelty + approximation"
check described above. For any model in a well-studied domain (MOND, dark matter alternatives,
modified gravity), a known checklist of standard observational tests exists. Run that checklist
as an adversarial exploration before Phase 3.

**The Compton-Unruh sequence should have been:**
1. E001–003: build and identify the T_U/T_dS identity
2. E004 (adversarial, standard MOND tests): Bullet Cluster, CMB 3rd peak, cluster lensing → catch
   the fatal lensing falsification early
3. E005+: pivot to Verlinde reformulation or modified-gravity version

Instead, the standard test was run as E008 after 7 constructive explorations.

## Additional Confirmation: Missing Adversarial in Thermal-Time s002

- **thermal-time strategy-002** — Ran only 3 of 10 budgeted explorations, all constructive (Rindler verification, post-quench test, excited-state test). Results are strong but unverified by adversarial review. The Gaussian approximation caveat in E003 (non-Gaussian state with quadratic K_R) is exactly the kind of issue an adversarial exploration would flag. The meta note explicitly identified this gap: "Should have launched at least an adversarial probe."

## Confirmation: Adversarial Before FINAL-REPORT Catches Embarrassments

- **navier-stokes strategy-002 exploration-004** — Adversarial review of all strategy-002 claims caught the BGW C ≤ 0.81 claim as a DNS resolution artifact (BGW fails in 3D for H^1 fields). This would have been embarrassing in a final report. Also properly calibrated novelty: "modest but real" for the BKM enstrophy theorem, "trivially known" for the C_Leff^4=F4*R^3 identity, "genuinely novel" for the 237x slack. This honest calibration is exactly what adversarial review is for. **The adversarial review should always come BEFORE the FINAL-REPORT, never after.**

## Timing Refinement: After Key Mechanism, Before Extended Test

**[vasseur-pressure E009]** Running the adversarial review AFTER the key mechanism was identified and computationally tested (Beltrami-De Giorgi connection, E006-E007) but BEFORE the extended near-Beltrami test was ideal timing. Earlier would have missed the strongest finding; later would have wasted budget on extended tests whose foundations needed correction. The adversarial review correctly identified that the DNS tightness program should be ABANDONED (smooth-solution limitation is fundamental) and that the remaining budget should focus on ANALYTICAL work (quantitative Beltrami-beta connection). This saved potential Strategy-002 explorations from pursuing DNS-based approaches.

## Variant: Adversarial -> Targeted Follow-Up on Weakest Link

**[vasseur-pressure E010]** The "adversarial review -> targeted follow-up" sequence is the optimal pattern for closing out a strategy. E009 identified Claim 5 (truncation preserves Beltrami) as the weakest claim and recommended testing near-Beltrami behavior. E010 ran exactly that test: perturbed-ABC sweep showing the mechanism is measure-zero specific. Without E010, the final report would have overclaimed the Beltrami connection. The adversarial review surfaces the weakest point; the targeted follow-up provides the definitive answer.

**Pattern:** (1) Run adversarial review. (2) Identify the weakest claim / most uncertain finding. (3) Design a single targeted exploration to definitively test that claim. (4) Use the result to correctly scope the final conclusions.

## Relationship to Other Entries

- `devils-advocate-after-construction.md` — The canonical post-Phase-3 adversarial check. That lesson remains valid; this is an ADDITIONAL check earlier in the sequence.
- `adversarial-explorations-need-null-hypothesis.md` — What adversarial explorations should contain; applies at both Phase 2→3 and post-Phase-3 checks.
- `decisive-negative-pivot.md` — When adversarial early review finds a fatal flaw, pivot before wasting Phase 3 compute.
- `specify-modified-inertia-vs-gravity.md` — The Compton-Unruh specific lesson: specify the inertia/gravity distinction upfront, as it is decisive for lensing.
