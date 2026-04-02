# Architecture — m001-vasseur-pressure

## Hierarchy

**Depth: 2** — Planner + Workers

```
Planner (forge-planner-m001-vasseur-pressure)
  ├── Code Worker(s)        — DNS solver setup, simulation runs, data extraction
  ├── Math Worker(s)        — Vasseur framework, De Giorgi theory, proof attempts
  ├── Research Worker(s)    — Literature (Tran-Yu, Brandolini et al., Vasseur-Yu)
  ├── Analysis Worker(s)    — beta_effective measurement, CZ decomposition, synthesis
  ├── Adversarial Worker(s) — Stress-test claims, check circular reasoning
  └── Librarian/Curator     — Knowledge retrieval and organization
```

## Rationale

Depth 2 despite complex goal because:
1. Single workstream — serial chain with branching, not parallel independent fronts
2. Well-specified strategy — the mission doc prescribes exact branching logic with numeric kill conditions
3. Quantitative measurability — beta_effective is a number, kill thresholds are explicit
4. Conductor would add overhead without strategic value — there's nothing ambiguous to resolve at the strategic level

## Agent Roles

### Planner
- **CWD:** `.../missions/m001-vasseur-pressure/plan`
- **Responsibility:** Execute the 4-step chain. Design tasks for each step. Evaluate results against kill conditions. Branch to 2A/2B/2C based on Step 1 measurements. Synthesize findings into FINAL-REPORT.md.
- **Task budget:** 12 tasks (expandable to 15 if needed)
- **Critical instruction:** Do NOT skip Step 1 measurement. Do not assume beta_effective > 4/3 — measure it first. The entire chain depends on this measurement being rigorous.

### Code Workers
- DNS solver: pseudospectral on T^3. Can reuse prior Atlas code or build fresh.
- Simulations: Taylor-Green vortex, anti-parallel tubes, random IC. Re = 100-5000. N=64 and N=128.
- Data extraction: compute De Giorgi iteration quantities, level-set measurements.

### Math Workers
- Step 2A: structural property isolation (div-free, quadratic, Poisson)
- Step 3: proof construction — div-free CZ theory, quadratic cancellation, Galilean covariance
- Tran-Yu verification: read paper carefully, assess whether Galilean invariance actually improves beta

### Research Workers
- Literature survey on post-2007 De Giorgi approaches
- Brandolini-Chiacchio-Trombetti div-free CZ theory

### Analysis Workers
- beta_effective computation from DNS data
- CZ pressure decomposition (harmonic + particular)
- Cross-IC, cross-Re comparison tables

### Adversarial Workers
- Review beta_effective measurements for numerical artifacts
- Check if proof attempts contain circular reasoning
- Stress-test whether "slack" is real or an artifact of insufficient resolution

## Communication Flow

1. Planner designs task → spawns Worker
2. Worker writes REPORT.md to `plan/reports/task-NNN-report.md`
3. Planner reads report, updates state, designs next task
4. Library: Librarian retrieves before each task; Curator processes inbox after significant findings
5. Kill conditions evaluated by Planner after each phase-ending task

## Task Budget Breakdown

| Phase | Tasks | Workers |
|---|---|---|
| Step 1: DNS setup + validation | 2-3 | Code |
| Step 1: beta_effective measurement | 2-3 | Code + Analysis |
| Step 1: CZ decomposition | 1 | Analysis |
| Step 2 (whichever branch) | 2-3 | Math + Research + Analysis |
| Step 3 (if reached) | 2-3 | Math + Adversarial |
| Step 4 (if reached) | 1 | Math |
| **Total** | **10-15** | |

## Considered Alternatives

**Depth 3 (Conductor + Planner):** Rejected. The branching logic (2A/2B/2C) is well-specified with numeric thresholds. A Conductor evaluating "should we pivot?" adds no value when the pivot criteria are already defined. The Planner can evaluate beta_effective against 4/3 and 3/2 itself.

**Depth 4 (Multiple Planners):** Rejected. No parallel independent workstreams. Steps 2A/2B/2C are mutually exclusive branches, not parallel efforts.
