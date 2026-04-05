---
topic: Require theorem-facing observables to survive harmless representative and refinement changes
category: goal-design
date: 2026-04-01
source: "exact-ns-helical-sign-bottleneck strategy-001 meta-exploration-001"
---

## Lesson

Before authorizing Phase 1 computation on a refined observable, ask whether that observable is invariant under the natural harmless changes that leave the underlying exact object unchanged.

Typical harmless changes include:

- conjugate-pair representative relabeling,
- quotient conventions for real mode pairs,
- harmless packet/support refinement with the same union support,
- and witness-set choices that should not change the underlying exact object.

If the observable moves under any of those, the mission is still at the canonization gate rather than at a quantitative phase.

## Evidence

- **exact-ns-helical-sign-bottleneck exploration-001** — The proposed packet sign statistic `SD_part` required choosing one representative from each conjugate pair `{(k,sigma), (-k,-sigma)}`. Flipping that representative changed the sign balance while leaving the exact support, exact solution segment, and exact triad magnitudes unchanged.
- Counting both members of each conjugate pair did not fix the problem. It trivialized the global sign statistic instead of making it canonical.
- The same exploration showed that `SD_part` also moved under harmless packet refinement, because participation mass was redistributed across a different family list with the same union support.
- `SD_target` and `Leak` still depended on which exact target triads were declared "desired" inside the packets. If all role-compatible triads counted, refinement changed the desired set; if only a witness subset counted, the object depended on an extra convention.

## Goal Pattern

1. List the harmless changes that should leave the proposed object unchanged.
2. For each candidate observable, run an explicit invariance screen against those changes before any optimization or scan.
3. If invariance fails, either supply and defend a canonical convention up front or stop and record canonicity failure.
4. Only after the observable passes the harmless-change screen should the goal authorize thresholds, parameter scans, or extremization work.

## Why This Matters

Quantitative work on a moving observable can look productive while measuring only bookkeeping choices. A cheap invariance screen prevents a long Phase 1 from confusing object selection with theorem-facing evidence.

## Distinction from Related Entries

- `check-faithful-support-shrinkage-before-narrowing.md` asks whether the follow-on mission changed the object at all. This entry asks whether new observables actually live on that object without extra choices.
- `fix-observability-conventions-before-precursor-search.md` is about freezing one physical-space event and region geometry. This entry is about quotient/refinement invariance inside an already proposed object family.
- `build-adversarial-suppression-into-first-audit.md` assumes a fixed audit object already exists. This entry decides whether there is a fixed object to audit.
