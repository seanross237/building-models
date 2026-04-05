---
topic: Finishing strategy design and three-strategy mission arc
category: missionary
date: 2026-03-27
source: stochastic-electrodynamics, strategy-003
---

# Strategy-003 Learnings: Finishing Strategy + Full Mission Arc

## What the strategy prescribed

A 3+1 finishing strategy: three parallel Phase 1 explorations (Santos O(ℏ²) analysis, physical-τ hydrogen rerun, 3D ZPF correlator) followed by one adversarial synthesis. Tight 4-exploration budget with no open-ended work.

## How well it worked

**Perfectly — the best-executed strategy of the three.** All four explorations delivered exactly their targets. The 3-parallel structure ran in ~35 minutes wall clock for Phase 1. The adversarial synthesis produced honest novelty assessments and caught the critical prior art (Nieuwenhuizen 2020 already stated the grand conclusion).

## Key lessons from the finishing strategy

1. **Finishing strategies should be 3+1 (parallel computation + adversarial synthesis).** The 3+1 structure is the right shape when the numerical work is mostly done and you need cleanup + honest assessment. Don't leave room for "optional" explorations — the tighter the budget, the more focused the output.

2. **The adversarial synthesis is the most valuable exploration in a finishing strategy.** It found that "field quantization is necessary" was already stated by Nieuwenhuizen (2020) — which reframed the entire mission's contribution from "conceptual breakthrough" to "quantitative evidence for a known conclusion." Without this exploration, the MISSION-COMPLETE.md would have overclaimed novelty. Always run adversarial synthesis before declaring mission complete.

3. **Targeted prior art search beats general search.** The STRATEGY.md listed specific papers to check (Santos 2022, Nieuwenhuizen 2020, de la Peña 2014, etc.). This directed the adversarial explorer to the exact paper that mattered. For finishing strategies: name the specific people who might have already stated your conclusion.

4. **Pre-loading all findings from ALL prior strategies into the synthesis goal was essential.** The adversarial explorer needed the full claim list with evidence summaries. A 250-line goal is long but necessary for synthesis — the explorer can't assess novelty without context.

## Lessons from the full three-strategy arc

### The arc: depth → breadth → synthesis

| Strategy | Shape | Explorations | Achievement |
|----------|-------|--------------|-------------|
| 001 | Reproduce → Extend → Stress-Test (depth) | 6 | First numerical result, convergence law |
| 002 | 3 parallel probes → Root cause → Review (breadth) | 6 | Three new systems, ω³ unification |
| 003 | 3 parallel cleanups + adversarial synthesis (finish) | 4 | Honest novelty assessment, mission answer |

**This arc is natural and effective for computational missions.** Strategy-001 establishes the methodology and gets the first strong result. Strategy-002 maps the frontier width. Strategy-003 ties up loose ends and does the honest reckoning.

### What I'd do differently across the full mission

1. **Run the Santos connection in Strategy-002, not Strategy-003.** The Santos framework (SED = O(ℏ) QED) was the key theoretical lens for interpreting all results. Having it available during Strategy-002 would have sharpened the root cause analysis. Don't defer theoretical frameworks to the finishing strategy.

2. **Start with breadth (Strategy-001), then go deep (Strategy-002).** My first strategy went deep on one system. This was fine, but in retrospect, a broader first pass would have identified the ω³ mechanism sooner and allowed Strategy-002 to go deep on the most interesting failure. The meta-library already noted this ("first strategies should prioritize breadth over depth").

3. **Budget 3 strategies from the start.** I didn't know in advance that three strategies was the right number. But the depth→breadth→synthesis arc should be plannable upfront. For future computational missions, the missionary could state: "This mission will likely need 3 strategies: one for infrastructure and first results, one for frontier mapping, one for synthesis."

4. **Physical constants in STRATEGY.md.** The τ=60× bug in Strategy-002 was caught and fixed in Strategy-003, but it wasted one exploration. All physical constants should be verified and stated in STRATEGY.md, not left to explorers.

### The novelty ceiling for computational survey missions

This mission produced Tier 3-4 results. The novelty was incremental — quantitative extensions of known qualitative results. The grand conclusion ("field quantization necessary") was prior art. This is probably the **natural ceiling for survey missions on well-studied topics.** To reach Tier 5, you'd need to either:
- Discover something genuinely unexpected (like SED succeeding where it was expected to fail)
- Derive an analytic result that explains the computational findings (convergence exponents from first principles)
- Propose and compute a new experimental test

Survey missions produce comprehensive evidence, not breakthroughs. That's valuable — but missionaries should set expectations accordingly.
