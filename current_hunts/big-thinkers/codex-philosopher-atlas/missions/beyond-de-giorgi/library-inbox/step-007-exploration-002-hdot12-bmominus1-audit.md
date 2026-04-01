# Exploration 002 Report

## Goal

Audit `\dot H^{1/2}` against the same Step-1 extraction-package checklist used for `L^3`, and decide whether `BMO^{-1}` deserves admission at all under this chain's standard.

## Sources Consulted

- `missions/beyond-de-giorgi/steps/step-007/GOAL.md`
- `missions/beyond-de-giorgi/steps/step-007/REASONING.md`
- `runtime/results/codex-patlas-beyond-de-giorgi-step-007-receptionist.md`
- `runtime/logs/codex-patlas-beyond-de-giorgi-step-007-receptionist-search.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/controller/decisions/decision-010.md`
- `missions/beyond-de-giorgi/planning-runs/run-004/selected/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-004/judgments/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-004/attacks/chain-02.md`
- `missions/beyond-de-giorgi/planning-runs/run-003/refined/chain-03.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
- `missions/navier-stokes/library-inbox/lin-1998-proof-architecture.md`
- `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- `library/factual/exact-rewrite-obstruction-audit/suitable-weak-leray-hopf-with-lei-is-the-fixed-solution-class.md`
- `library/factual/exact-rewrite-obstruction-audit/every-rewrite-must-stay-inside-the-same-localized-lei-package.md`

## Findings

### Architecture Floor And Absence Scan

- `[VERIFIED]` The branch's fixed architecture floor is suitable weak
  Leray-Hopf solutions with the local energy inequality. This is stated
  directly in
  `library/factual/exact-rewrite-obstruction-audit/suitable-weak-leray-hopf-with-lei-is-the-fixed-solution-class.md`
  and is consistent with the CKN / Lin / Vasseur proof-architecture notes.
- `[VERIFIED]` The branch does not allow a host-space route to become viable
  only after changing the surrounding protocol away from the same localized LEI
  package. This is stated in
  `library/factual/exact-rewrite-obstruction-audit/every-rewrite-must-stay-inside-the-same-localized-lei-package.md`.
- `[VERIFIED]` A repository scan over `missions/` and `library/` for
  `\dot H^{1/2}` and `BMO^{-1}` found only planning, governance, and prompt
  references, not a dedicated local theorem packet for either host space.

### `\dot H^{1/2}` Package Audit Table

| Requirement | Known input | Solution-class commitment | Overlap / prior-art note | Missing piece |
| --- | --- | --- | --- | --- |
| local theory | `[VERIFIED]` `run-004/attacks/chain-02.md` states that `\dot H^{1/2}` has cleaner Hilbert-space profile technology than `BMO^{-1}`. `[INFERRED]` That is a comparative compactness remark, not a local theorem packet in the repository. | `[INFERRED]` The local record pushes `\dot H^{1/2}` toward a Hilbert/critical-space program rather than the inherited suitable-weak LEI class. | `[VERIFIED]` Overlap is with generic Hilbert-space critical-space technology, not with a mission-specific theorem packet. | `[VERIFIED]` No local theorem packet establishes `\dot H^{1/2}` local theory in the exact Step-1 sense. |
| large-data perturbation / stability | `[VERIFIED]` `run-004/judgments/chain-02.md` and `decision-010.md` require exact stability inputs as part of the Step-1 gate. `[VERIFIED]` The local repository does not provide any dedicated `\dot H^{1/2}` stability theorem packet. | `[INFERRED]` A viable route would need a stability theorem in the same class as the proposed critical evolution, but that class is not frozen locally. | `[VERIFIED]` The local critique warns against soft "credibility" language here. | `[VERIFIED]` Stability remains part of a diffuse missing stack, not one sharply bounded theorem. |
| profile decomposition / extraction input | `[VERIFIED]` The local record repeatedly names profile decomposition and concentration compactness as required ingredients. `[VERIFIED]` The specific comparative point is only that `\dot H^{1/2}` has cleaner Hilbert-space profile technology than `BMO^{-1}`. | `[INFERRED]` That suggests plausibility for extraction language, but still inside a not-yet-frozen critical-space program. | `[VERIFIED]` Overlap is with the Kenig-Merle-style compactness template rather than a concrete NS host-space packet. | `[VERIFIED]` No dedicated local extraction theorem is supplied. |
| symmetry normalization | `[VERIFIED]` `run-004/attacks/chain-02.md` says symmetry normalization in NS is nontrivial because scaling, translation, Galilean issues, pressure normalization, and solution framework all matter. | `[INFERRED]` The same unresolved normalization burden applies to `\dot H^{1/2}`. | `[VERIFIED]` This is another place where the local record treats the issue as foundational rather than cosmetic. | `[VERIFIED]` No local normalization theorem or convention is fixed for a `\dot H^{1/2}` critical element. |
| pressure / local-energy compatibility | `[VERIFIED]` `run-004/attacks/chain-02.md` explicitly says `\dot H^{1/2}` is less naturally tied to suitable-weak-solution machinery feeding local energy and backward uniqueness. `[VERIFIED]` `suitable-weak-leray-hopf-with-lei-is-the-fixed-solution-class.md` fixes the branch's inherited compatibility floor as suitable weak / Leray-Hopf plus LEI. | `[INFERRED]` A surviving `\dot H^{1/2}` route would need a bridge into that LEI architecture or else a declared architecture change. | `[VERIFIED]` This is the clearest local warning against treating `\dot H^{1/2}` as automatically better because it is Hilbertian. | `[VERIFIED]` Missing LEI-compatibility bridge. |
| compactness usable by later rigidity | `[VERIFIED]` `decision-010.md` and `step-007/GOAL.md` require compactness usable by later rigidity. `[INFERRED]` The local record makes `\dot H^{1/2}` look more plausible than `BMO^{-1}` on compactness language alone, but not as a completed package. | `[INFERRED]` Would require a mild or critical-space maximal-lifespan framework that the local corpus never ties back to LEI. | `[VERIFIED]` Overlap is again with generic critical-space compactness rather than a branch-frozen NS theorem packet. | `[VERIFIED]` No usable compactness theorem is instantiated locally. |

### `\dot H^{1/2}` Verdict

- `[VERIFIED]` Classification: `not viable because extraction package is diffuse`.
- `[INFERRED]` The attractive part of `\dot H^{1/2}` in the local corpus is its
  Hilbert-space flavor, but the exact Step-1 burden still fails because local
  theory, stability, normalization, and LEI compatibility are not frozen into
  one theorem stack.
- `[VERIFIED]` There is no single sharply isolated local missing theorem. The
  gap remains diffuse across local theory, stability, extraction,
  normalization, and LEI / pressure compatibility.

### `BMO^{-1}` Admission Decision

- `[VERIFIED]` `run-004/attacks/chain-02.md` states that `BMO^{-1}` is the
  weakest candidate in this menu for a compactness-rigidity program.
- `[VERIFIED]` The same source says it is excellent for small-data mild theory,
  but a poor default host for large-data minimal blowup extraction unless one
  can point to a concrete nonlinear profile decomposition and a robust
  stability theory in exactly that setting.
- `[VERIFIED]` The receptionist result confirms that no local source packet
  provides that replacement large-data compactness package.
- `[VERIFIED]` `planning-runs/run-003/refined/chain-03.md` states the sharper
  admission rule: a weaker candidate such as `BMO^{-1}` is to be included only
  if an explicit replacement compactness package is stated.
- `[VERIFIED]` The inherited branch floor remains suitable weak / Leray-Hopf
  plus LEI, while `BMO^{-1}` is only locally supported in small-data mild
  language.
- `[VERIFIED]` Classification: `not admitted for this chain`.
- `[INFERRED]` The sharpest exclusion reason is:
  the local repository does not supply the replacement compactness-plus-
  stability structure that would justify moving from the inherited LEI
  architecture to a large-data `BMO^{-1}` minimal-blowup program.

### Exact Exclusion Reason For `BMO^{-1}`

- `[VERIFIED]` The clean local obstruction is not a generic dislike of the
  space. It is failure of the entry condition named in
  `planning-runs/run-003/refined/chain-03.md`: no explicit replacement
  compactness package is stated locally for large-data extraction in
  `BMO^{-1}`.
- `[VERIFIED]` `run-004/attacks/chain-02.md` makes that missing package
  concrete: one would need a nonlinear profile decomposition and robust
  stability theory in exactly the `BMO^{-1}` setting.
- `[INFERRED]` The LEI / local-energy mismatch is therefore a reinforcing
  architecture objection, not the first admission-level obstruction. The first
  obstruction is earlier and sharper: the replacement extraction package is
  absent.

## Dead Ends / Failed Attempts

- Initial `rg` pattern for mixed TeX strings failed due to regex escaping; switched to direct file reads and simpler searches.
- Search for a dedicated local `\dot H^{1/2}` or `BMO^{-1}` theorem packet in
  `missions/` and `library/` came back empty apart from planning/governance
  files.

## Conclusion

`\dot H^{1/2}` does not clear Step 1 because its package gap is still diffuse,
especially at the LEI-compatibility interface. `BMO^{-1}` should be excluded
up front: the local record supports it only as small-data mild theory and
provides no large-data nonlinear profile decomposition or replacement
compactness package. The correct Step-1 outcome is therefore negative on both
fronts.
