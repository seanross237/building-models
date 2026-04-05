# Distinguish Launcher Stalls From Research Inconclusiveness

Session monitoring should report launcher-side stalls separately from
research-side inconclusiveness.

If a scheduled launcher fails to complete reliably, that is an operational
workflow fact, not evidence that the underlying branch audit was inconclusive.
Conflating the two weakens both the runtime diagnosis and the resulting
research memo.

The reusable rule is to surface at least two statuses:

- launcher or runtime execution failure
- substantive research outcome from the anchored materials

That separation keeps operational noise from being misfiled as epistemic
weakness.

Filed from:
- `missions/beyond-de-giorgi/meta-inbox/meta-step-004-exploration-003.md`
