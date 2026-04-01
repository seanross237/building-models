# Meta-Learning: Exploration 003

## What worked well
- **Multiple approaches in one exploration** worked here because they share the same constraint catalog testing framework. The three-way comparison was valuable.
- **Providing the constraint catalog as a reference table** made scoring straightforward and systematic.
- **The explorer correctly identified that Approach C was tautological** ("somewhat circular") rather than enthusiastically claiming success. The honesty instruction seems to be internalizing.

## What didn't work well
- **The BBM approach used the wrong basis** (harmonic oscillator), which the goal didn't prevent. The goal should have either (a) specified position-space discretization, or (b) warned that HO basis is poorly suited to xp-type operators.
- **N=200 zeros for Approach C** was too few for number variance and spectral rigidity, degrading 4 constraint tests to PARTIAL. The goal should have specified using the 2000 zeros already available from Phase 1 (or saving/reloading them).

## Lessons for future explorations
1. **When testing an operator, specify the discretization basis explicitly.** Different bases give wildly different results for truncated operators. The HO basis is only good for operators with HO-like potentials.
2. **When reusing Phase 1 data, either provide it as files or tell the explorer to recompute at the same N.** Phase 1 used 2000 zeros; Phase 2 dropping to 200 was a step backward for statistical power.
3. **The scorecard format worked well** — having a table of PASS/FAIL/PARTIAL with quantitative measures made the comparison clear. Use this format in future operator testing explorations.
4. **Key insight for future work:** Simple regularizations of xp all fail because they only capture the smooth (Weyl) density. The fluctuations require prime input. The trace formula reconstruction is the right next step.
