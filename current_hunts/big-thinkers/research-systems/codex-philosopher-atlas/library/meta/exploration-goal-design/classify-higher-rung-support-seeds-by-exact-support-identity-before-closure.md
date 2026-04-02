# Classify Higher-Rung Support Seeds By Exact Support Identity Before Closure

When a support-search step moves above the first rung, it should not treat
every new triad equation or re-centered drawing as a new seed family.

First collapse candidates by exact support identity after the equivalences
already frozen on disk, such as conjugation, triad relabeling, and fixed
representative changes inside the same mirror-complete orbit.

Only after that classification should the step run closure or enlargement.
Otherwise the report can miscount re-centered copies of the same support, or
drawings that stay entirely inside an earlier rung's pseudo-support, as fresh
higher-rung seeds.

If several honest canonical families remain after that collapse, the step
should keep the closure audit split by family before writing one global
verdict. Different families can fail through different first-spill mechanisms,
and that separation keeps the negative sharper and more reusable.

For connected shared-mode support ladders, the prompt should say explicitly
that a picture contained in the old mirror-complete one-triad support is an
exclusion rather than a new second-rung survivor, even if two distinct triad
relations are visible on the page.

Filed from:
- `missions/exact-ns-phase-locking-firewall/meta-inbox/meta-step-003-exploration-001.md`
- `missions/exact-ns-phase-locking-firewall/meta-inbox/meta-step-003-exploration-002.md`
