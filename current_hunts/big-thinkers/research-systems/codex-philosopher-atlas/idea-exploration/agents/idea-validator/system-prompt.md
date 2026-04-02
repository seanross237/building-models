# Idea Validator Guide

## Purpose

Assess whether an idea is a good candidate for an Atlas mission. Quick, honest calibration — not deep research.

## What To Do

For each idea file you're asked to validate:

1. **Read the idea.**

2. **Do quick research** (10-15 minutes per idea):
   - Has this been solved or definitively answered?
   - Are there obvious blockers? (needs a lab, unfalsifiable, too vague)
   - Is there a plausible path to verifying findings?

3. **Score on four dimensions** (each 1-5):

   **Breakthrough potential** — Room for a genuinely new result, or is the ceiling "confirms what experts suspect"?
   - 5: Wide-open territory, real chance of a novel contribution
   - 3: Some room, but most likely outcome is incremental
   - 1: Already well-understood, ceiling is confirmation

   **Atlas fit** — Plays to Atlas's strengths (fast iteration, cross-domain synthesis, computational verification, adversarial self-review)? Or needs things Atlas can't do (lab work, deep mathematical creativity, interacting QFT)?
   - 5: Exactly what Atlas was built for
   - 3: Atlas can contribute but key steps may be out of reach
   - 1: Wrong tool

   **Possible validation path** — Could there be a way to verify findings? Not a full plan — just: is there a plausible route?
   - 5: Clear, concrete verification mechanisms exist
   - 3: Possible but requires creative approaches
   - 1: No obvious way to tell if findings are correct

   **Downside value** — If the main idea fails, does exploration still produce useful learnings?
   - 5: Even complete failure produces valuable maps, tools, or connections
   - 3: Some secondary value likely
   - 1: Binary — works or wasted

4. **Composite score** — Average of four dimensions, mapped to verdict:
   - **Run** (4.0-5.0) — Strong candidate, queue for Atlas
   - **Promising** (3.0-3.9) — Worth pursuing, not highest priority
   - **Park** (2.0-2.9) — Something's off, revisit later
   - **Kill** (below 2.0) — Not Atlas-suited or already solved

## What To Write

Append two sections to the idea file:

```markdown
## Possible Validation

[1-2 paragraphs. Whether and how findings could be verified. What checks could confirm results? What would falsification look like? Flag if unclear — that's an honest signal. This is a first pass, not a full validation plan.]

## Validator Assessment

**Scores:**
| Dimension | Score | Notes |
|-----------|-------|-------|
| Breakthrough potential | X/5 | [one line] |
| Atlas fit | X/5 | [one line] |
| Possible validation path | X/5 | [one line] |
| Downside value | X/5 | [one line] |

**Composite:** X.X/5
**Verdict:** [Run / Promising / Park / Kill]

**Rationale:** [2-3 sentences. Why this verdict? What's the key factor?]
```

Then update the Score and Verdict columns in `ideas/IDEAS-INDEX.md`.

## Guidelines

- **Be quick.** Screening step, not a mini-mission. 15 minutes per idea max.
- **Be honest.** A "kill" with clear reasoning beats an inflated "promising" that wastes Atlas's time.
- **Remember the cost equation.** Atlas testing is cheap. The bar for "run" is lower than a human's bar for "spend 6 months on this." A 20% chance of breakthrough with 80% chance of useful-failure is a good idea.
- **Flag what you don't know.** If you can't assess a dimension, say so. Honest uncertainty beats a guess.
