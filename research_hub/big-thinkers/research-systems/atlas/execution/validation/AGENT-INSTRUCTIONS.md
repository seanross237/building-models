# Agent Instructions for Validation Suite

How autonomous research agents should use these validation tools. The key principle: **this suite helps you go faster, not slower.**

---

## When to Validate

| Trigger | What to Run |
|---------|-------------|
| You propose a new theory or major revision | QUICK-CHECK.md (5 questions, 2 minutes) |
| You write down an action or partition function | Tier 1 tests (structural sanity) |
| You claim to reproduce known physics | Tier 2 tests (known physics recovery) |
| You compute a specific number or prediction | Tier 3 tests (quantitative checks) |
| The theory is mature and passes Tiers 1-3 | Tier 4 tests (novel predictions) |
| You're building a unification theory | Tier 5 tests (unification checks) |
| You're unsure if a result violates known data | Look up the bound in EXPERIMENTAL-DATA.md |

**Do NOT run the full suite every iteration.** Only run the tests relevant to what you just did.

---

## How to Report Results

After running tests, add a validation section to your working document (CALCULATIONS.md, GRAND-THEORY.md, or equivalent).

### Format

```markdown
## Validation Results (Iteration N)

**Date:** YYYY-MM-DD
**Theory version:** [brief description of current state]

### Quick Check
| # | Question | Result | Notes |
|---|----------|--------|-------|
| 1 | Has Z? | PASS | Z = integral DA exp(-S[A]) |
| 2 | Spin-2? | PASS | Emerges via Goldstone mechanism |
| 3 | Newton's law? | PASS | Shown in Section 4.2 |
| 4 | Experimental bounds? | PASS | All checked, within bounds |
| 5 | Novel prediction? | PASS | Predicts modified dispersion at E > 10^17 GeV |

### Tier 1-2 Tests
| Test | Result | Notes |
|------|--------|-------|
| 1.1 Action exists | PASS | S = integral d^4x sqrt(g) (R + alpha R^2 + ...) |
| 1.2 DOF count | PASS | 2 propagating modes |
| 1.3 Gauge symmetry | PASS | Linearized diffeos preserved |
| 1.4 Ghost freedom | CONDITIONAL | Ghost-free if alpha > 0, proof in Appendix B |
| 2.1 Propagator | PASS | Matches GR at k << M_Pl |
| 2.2 Newton's law | PASS | V(r) = -GM/r + O(l_P^2/r^3) |
| 3.4 BH entropy | SKIP | Not ready — BH solutions not yet derived |
| 3.5 Spectral dimension | SKIP | Not computed yet |
```

### Result Labels

| Label | Meaning |
|-------|---------|
| **PASS** | Test satisfied. Include brief evidence. |
| **CONDITIONAL** | Passes under specific conditions. State the conditions. |
| **FAIL** | Test not satisfied. Explain why and what it means. |
| **SKIP** | Prerequisites not met, or test not applicable. Brief reason. |
| **PARTIAL** | Some aspects pass, others don't. Detail which. |

---

## When to Skip Tests

**It is completely fine to skip tests.** A SKIP is not a failure — it means "not applicable yet."

Skip a test when:
- The **Prerequisites** listed in the test aren't met
- You're at an early structural stage and quantitative tests don't apply yet
- The test is about unification but you're only working on quantum gravity
- The computation is genuinely intractable at this stage
- The test doesn't apply to your theory's framework (e.g., non-perturbative theories skipping propagator tests)

**Never let a skipped test block your progress.** Just note "SKIP — [reason]" and move on.

---

## When to Worry

### Red Flags (act immediately)

| Situation | What It Means | What to Do |
|-----------|---------------|------------|
| Quick Check #4 fails (violates experimental bound) | Theory is ruled out unless you find an error | Recheck your calculation. If correct, the theory needs modification or is dead. |
| Tier 1 tests fail (structural problems) | Foundational issues | Reconsider the theory's construction. Ghost? Wrong DOF? Fix before proceeding. |
| Multiple Tier 2 tests fail | Doesn't reproduce known physics | Major revision needed. The theory may need a different starting point. |

### Yellow Flags (note and continue)

| Situation | What It Means | What to Do |
|-----------|---------------|------------|
| Tier 3 test is borderline | Theory is marginal quantitatively | Refine the calculation. Check for errors. The value might shift with better approximations. |
| All Tier 4 tests are SKIP after many iterations | Not producing predictions | Push harder. Compute something testable, even if approximate. |
| Tier 5 tests fail | Not a unification theory (yet) | That's fine if you're focused on quantum gravity alone. |

### Green Flags (celebrate and push further)

| Situation | What It Means |
|-----------|---------------|
| All Quick Checks pass | Solid foundation. Proceed with confidence. |
| Tier 1-2 all pass | Theory reproduces known physics. |
| Tier 3 tests pass with specific numbers | Quantitatively viable. Time for predictions. |
| Tier 4 tests produce testable predictions | This is real physics. Publish. |

---

## Validation Cadence

A suggested rhythm for long research efforts:

| Phase | Run | Frequency |
|-------|-----|-----------|
| Early exploration | Quick Check | After each major idea |
| Formalization | Tier 1 | Once, when action is written |
| Known physics | Tier 2 | After each limit calculation |
| Quantitative work | Tier 3 | After each numerical result |
| Maturation | Tier 4 | When theory stabilizes |
| Unification | Tier 5 | When scope expands beyond gravity |

---

## Referencing Experimental Data

When you need a specific value:

1. Check EXPERIMENTAL-DATA.md first — it has the most commonly needed values.
2. If the value isn't there, check the PDG (pdg.lbl.gov) for particle physics data.
3. For Lorentz violation: Kostelecky & Russell Data Tables (arXiv:0801.0287, updated annually).
4. For gravitational tests: Will (2014) "The Confrontation between General Relativity and Experiment" (Living Reviews in Relativity).
5. For cosmological data: Planck 2018 results (arXiv:1807.06209).

---

## Tips for Efficient Validation

1. **Run Quick Check early and often.** It takes 2 minutes and catches obvious problems.
2. **Don't gold-plate Tier 1-2.** A clean pass is enough — you don't need to write a paper about why your propagator matches GR.
3. **Spend time on Tier 3.** This is where the real physics happens. Getting numbers right matters.
4. **Don't skip Tier 4 forever.** If you've been working for many iterations and every Tier 4 test is "SKIP", something is wrong — you're perfecting without predicting.
5. **Use EXPERIMENTAL-DATA.md as a cheat sheet.** Don't look up values from scratch every time.
6. **Report results honestly.** A FAIL is more useful than a dishonest PASS — it tells you where to focus.
