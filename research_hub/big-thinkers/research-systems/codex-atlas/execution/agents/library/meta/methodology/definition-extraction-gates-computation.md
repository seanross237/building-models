---
topic: Definition-extraction explorations gate computation phases
category: methodology
date: 2026-04-01
source: "vasseur-pressure strategy-001 meta-exploration-001; anatomy-of-averaged-ns-blowup-firewall strategy-001 meta-exploration-001; exact-ns-no-near-closed-tao-circuit strategy-001 meta-exploration-001; exact-ns-hidden-precursor-firewall strategy-001 meta-exploration-001; exact-ns-phase-locking-firewall strategy-001 meta-exploration-001"
---

## Lesson

Before committing to a computation phase, run a definition-extraction exploration ("Phase 0") that reads the primary source and extracts the exact mathematical definition of the quantity, event, or theorem object to be measured or proved. This prevents the most wasteful failure mode: computing the wrong thing because the team's mental model of the target object was incorrect.

## Evidence

- **vasseur-pressure exploration-001** — The team assumed beta was a pressure integrability exponent. The Phase 0 exploration (reading Vasseur 2007) revealed that beta is actually a De Giorgi recurrence exponent with a completely different mathematical structure. If the team had skipped to DNS computation, they would have measured pressure integrability indices (a well-defined but irrelevant quantity) rather than the recurrence exponent that actually controls regularity. The entire computational strategy would have been wasted.
- **anatomy-of-averaged-ns-blowup-firewall exploration-001** — Full PDF access was unavailable, but primary-source AMS snippets were still enough for Phase 0 because the target was the **mechanism architecture**: averaged operator -> reduced five-mode circuit -> final blowup induction. The mission did not need every auxiliary bootstrap estimate before proceeding.
- **exact-ns-no-near-closed-tao-circuit exploration-001** — The local library already had the mechanism map and the candidate exact-NS objections. What it lacked was the exact amplitude-level interaction language. Pulling one precise helical-triad law from primary sources was enough to close the definition gap and produce a testable exact-support object. The computation phase was blocked on the missing exact law, not on a full literature survey.
- **exact-ns-hidden-precursor-firewall exploration-001** — The helical singleton and packet definitions were already exhausted. The successful Phase 0 move was different: exact coarse-grained forward flux `Pi_ell` plus a local subscale witness `W_{ell,rho,r}` gave a faithful physical-space event directly on exact Navier-Stokes. The missing layer was an observability-convention ledger, not a new reduced dynamical model.
- **exact-ns-phase-locking-firewall exploration-001** — The packet/sign line was already closed locally, and the physical-space delayed-transfer event already existed. The useful Phase 0 move was to reuse only the surviving interface logic while returning to the exact signed helical transfer ledger itself: each triad term carries an intrinsic phase, and the preferred observable had to live on that exact ledger rather than on packet bookkeeping or a localized cutoff that scrambles the clean triad population.

## Pattern

1. Before any computation-heavy phase, allocate one exploration to read the primary source(s) and extract exact definitions.
2. Frame the key question as "What EXACTLY is X?" (see `goal-design/specify-rigor-level.md` for prompt pattern).
3. Require the exploration to identify which claims are from the source vs. interpretation (see `goal-design/require-claim-attribution.md`).
4. If the extracted definition differs from the team's working assumption, redesign the computation phase before proceeding.
5. If source access is partial but the Phase 0 target is an architecture-level mechanism map, recover the operator / reduced model / theorem interface first; full lemma-by-lemma reconstruction is unnecessary at this stage.
6. If the local library already fixes the architecture and objections, ask whether a single exact law or definition from the primary source is the only missing ingredient. Often that one missing exact-language layer is enough to unlock the whole next phase.
7. If the Phase 0 target is a physical-space event, ask whether exact-PDE post-processing plus explicit observability conventions already defines it. If yes, prefer that exact observable pair over inventing a surrogate reduced model.
8. If you inherit a useful predecessor scaffold, separate the parts that preserve the new exact ledger from the parts that destroy it. Reuse the surviving interface/event shape, but drop localization or packet layers that erase the exact variable now under audit.
9. If multiple exact candidates survive, prefer the first one that stays coupled to the load-bearing ledger. A raw concentration statistic that forgets the sign of the actual transfer is a backup summary, not the main theorem object.

## When to Apply

Any mission that targets a quantity, event, or theorem object defined in a specific paper or framework, especially when the name is suggestive of a different (more familiar) mathematical object. High-risk cases: quantities named after common objects (e.g., "beta" could be a dozen things), event concepts inherited from reduced models, quantities from papers not yet read by the team, and objects known only through secondary sources.

## Distinction from Existing Entries

Distinct from `benchmark-comparison-early` (comparing to external benchmarks) and `verify-goal-claims-before-delegating` (checking cited results). This is about verifying the team's understanding of the target definition itself, not about benchmarks or prior results.
