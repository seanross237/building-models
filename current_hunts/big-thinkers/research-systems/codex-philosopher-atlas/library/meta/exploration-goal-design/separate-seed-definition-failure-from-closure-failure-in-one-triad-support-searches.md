# Separate Seed-Definition Failure From Closure Failure In One-Triad Support Searches

When a support-search budget is
`one exact triad orbit`,
the prompt should first separate honest exact active triads from degenerate
wavevector relations before it asks for any closure work.

Repeated-wavevector and collinear relations can already force the exact
projected interaction coefficient to vanish.
Those cases are non-seeds, not closure failures.

If a step skips that screen, later negative evidence mixes two different
claims:
the candidate never met the seed definition, or it met the seed definition
but failed recursive closure or downstream tests.
That makes the resulting obstruction harder to reuse.

So one-triad support-search prompts should force a seed-stage nondegeneracy
screen before any closure or enlargement audit.

Filed from:
- `missions/exact-ns-phase-locking-firewall/meta-inbox/meta-step-002-exploration-001.md`
