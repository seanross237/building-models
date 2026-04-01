---
topic: In toy-mechanism vs exact-PDE comparisons, test subsystem isolation inside the exact interaction network
date: 2026-03-31
source: "anatomy-of-averaged-ns-blowup-firewall strategy-001 meta-exploration-002"
---

## Lesson

When a paper embeds or motivates a toy mechanism inside an exact PDE, the decisive comparison is usually not "does the PDE contain an analogous local interaction?" but "can the toy subsystem remain isolated once the full exact interaction network is restored?" The sharp diagnostic is leakage and isolation, not slogan-level resemblance.

## Evidence

- **anatomy-of-averaged-ns-blowup-firewall exploration-002** — Exact NS obviously has triads and pressure/Leray structure, so generic resemblance was never the issue. The live candidates became (1) coefficient rigidity and (2) unavoidable spectator couplings only after the comparison table was tied to Tao's literal gate chain `X1,n -> X2,n -> X3,n -> X4,n -> X1,n+1`.
- The same exploration showed that tiny or low-energy variables are not a firewall by themselves. The real question is whether exact dynamics can keep `X2,n` and `X3,n` in their intended isolated roles without activating comparable companion channels.
- Pressure/Leray worked best as an enforcement mechanism for rigidity/leakage rather than as a standalone candidate. That classification prevented the exploration from re-opening the already-closed generic "pressure is nonlocal" route.

## Protocol

1. Write the toy subsystem as a literal channel graph or intervention table.
2. Restore the exact PDE interaction law on the same target modes.
3. Enumerate all forced companion interactions, not just the desired ones.
4. Separate standalone obstruction candidates from mechanisms that enforce them.
5. Ask whether the desired channels dominate every forced spectator by a genuine small parameter.

## When to Apply

- toy-model vs exact-PDE firewall questions
- shell/cascade reductions
- exact-support realization problems
- any exploration where generic objections are already closed and only mechanism-level discrepancies remain

## Relationship to Other Lessons

Distinct from `goal-design/require-mechanism-layer-maps.md`, which identifies the layers and variable roles. This entry governs what to test after that map exists.

Complementary to `ask-what-replaces-the-bottleneck.md` and `model-pde-comparison-for-mechanism-identification.md`: those isolate replacement mechanisms or cross-PDE structure; this one tests whether a reduced subsystem can survive inside the exact network at all.
