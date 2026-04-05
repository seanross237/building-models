# Every Rewrite Must Stay Inside The Same Localized LEI Package

Status: `INFERRED`

In this branch, a candidate rewrite only counts if it remains interpretable
before and after localization inside the same suitable-weak local-energy
setting.

That makes the following compatibility violations disqualifying rather than
helpful:

- upgrading the solution class beyond the fixed suitable-weak/Leray-Hopf
  package
- replacing the local energy inequality with a vorticity-only or otherwise
  different closure scheme
- hiding projector, singular-integral, or commutator costs by changing the
  surrounding protocol

This is the branch's non-negotiable compatibility rule: if a rewrite becomes
exact or useful only after an architecture change, it is not a live candidate
for the fixed-protocol audit.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-005-exploration-002-compatibility-localization-protocol.md`
