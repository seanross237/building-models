# Rhyme-Eval: Summary, Learnings & Review

## Learnings

### About the Loop System

1. **The guesser→score→updater→new prompt loop works.** 43% → 73% over 5 generations. The pattern is reusable for any preference prediction task with ground truth.

2. **Exploration includes regression — that's fine.** Gen 2 hit 63%, Gen 3 dropped back to 43%, then Gen 5 climbed to 73%. The dip wasn't a failure — the system was exploring different prompt strategies. Some explorations don't pan out, and that's how you find the right direction. The loop self-corrected by Gen 5.

3. **The updater only sees failures — future versions should also analyze hits.** It examines misses but never asks WHY the 19 hits were hits. Analyzing both would let it preserve winning patterns while fixing losing ones, making exploration more efficient.

4. **30 samples is too small for confident signal.** A few lucky/unlucky calls swing the score by 10%. Multi-run scoring (3x per prompt, use median) and larger truth sets would give more reliable signal about whether a prompt change actually helped.

5. **Blind evaluation with deterministic shuffling was essential.** Seeded Fisher-Yates shuffle (same algo as the RhymePreferencesPage UI) eliminated position bias. Model names stripped from the guesser's view. Without this, the results would be contaminated.

### About Sean's Couplet Preferences

6. **Sincerity over cleverness, always.** The seed prompt valued "naturalness & flow" and "emotional specificity" — craft-centric evaluator values. Sean values warmth, devotion, and feeling like the song is truly about the person. A straightforward "you're everything I need" beats a clever metaphor.

7. **Direct character praise is the #1 signal.** Lines that name and admire WHO the person IS — "patient, kind, brilliant" — win almost every time. This was the single most powerful insight the updater discovered.

8. **Using the recipient's name is a major advantage.** When one couplet uses the person's name and another doesn't, the named one has a strong edge.

9. **Fuller narrative beats tidy summary.** More of the couple's story > a clean poetic moment. The seed prompt penalized "overstuffed lines" — but Sean actually prefers lines packed with story.

10. **Warm metaphor is good. Cleverness is bad.** "Like the sunrise through the pines" serves tenderness — that's welcome. "Your greatest work's been building up this heart" is showing off — that loses. The line between them is whether the imagery serves the person or serves the poet.

11. **Warm ending > dramatic ending > funny ending.** The last impression matters. "You're home to me" beats "our baby will never know that pain" beats a punchline. Celebrate, don't devastate.

12. **Rhonda was easiest, James was hardest.** By Gen 5: Rhonda 10/10, Dillon 7/10, James 5/10. Rhonda's song had clear personality markers (5 feet, hoodie, Bud Light, off-grid). James's options were more similar to each other, making the distinctions subtler.

### About Prompt Evolution

13. **The seed prompt's values were wrong.** It prioritized naturalness, singability, rhyme quality, and "both lines carry weight." The winning prompt prioritized narrative completeness, sincerity, direct character praise, and warm emotional resolution. The evaluator's instinct for what makes a "good" couplet ≠ what makes a human choose one as a gift.

14. **Gen 2 was the breakthrough generation.** It discovered the core insight: sincerity over cleverness, narrative over brevity. Every subsequent improvement built on that foundation. Gen 3-4 were detours caused by overcorrection.

15. **The best prompt reframes the task.** Seed prompt: "you are an expert songwriter evaluating couplets." Best prompt: "you are picking which couplet will make the recipient cry happy tears." Same task, totally different frame — and the frame matters more than the evaluation criteria.

---

## Experiment Overview

**What:** Can an AI predict which song couplet Sean prefers, and can we iteratively improve that prediction?

**Truth set:** 30 couplet comparison groups from 3 real customer songs (Dillon, Rhonda, James). Each group has 3 options from different models (haiku, sonnet, opus), blind-labeled A/B/C. Sean picked his favorite for each.

**Loop:** 5 generations. Each generation: spawn a guesser agent with a prompt → score against Sean's picks → spawn an updater agent to analyze errors → produce improved prompt → repeat.

---

## Generation-by-Generation Results

### Gen 1: 13/30 (43%)
**Prompt approach:** Craft-centric — naturalness, emotional specificity, singability, rhyme quality, conversational warmth.

**Per-song:** Dillon 2/10, Rhonda 7/10, James 4/10

**What went wrong:** Brevity bias (preferred short clean couplets over story-packed ones), cleverness bias (chose poetic/artistic over sincere), edge bias (picked gut-punch moments over warm celebration).

**Updater diagnosis:** Brevity bias, cleverness over sincerity, edge over warmth, undervaluing names, undervaluing narrative completeness.

### Gen 2: 19/30 (63%) — +6 from Gen 1
**Prompt approach:** Shifted to narrative completeness, sincerity, and warm conventional resolution. Added "using the recipient's name is a strong positive signal."

**Per-song:** Dillon 7/10, Rhonda 8/10, James 4/10

**What went wrong:** Remaining misses concentrated in James (still 4/10). Over-valued detail-stuffing in James's song. Missed that warm poetic imagery is NOT cleverness.

**Updater diagnosis:** Detail-stuffing loses to cleaner emotional delivery. Warm poetic imagery is welcome. Gentle admiration beats dramatic intensity.

### Gen 3: 13/30 (43%) — Exploration dip, -6 from Gen 2
**Prompt approach:** Explored a different direction — added guardrails: "Detail Sweet Spot" warning, "Warm Embrace Over Dramatic Impact", "The Intensity Trap."

**Per-song:** Dillon 4/10, Rhonda 6/10, James 3/10

**What happened:** This exploration path didn't pan out. The anti-detail and anti-intensity framing made the guesser too cautious. But it taught the system what NOT to do, which informed the recovery in Gen 4-5.

**Updater diagnosis:** Correctly identified the overcorrection. Proposed: direct character praise as #1, recipient name advantage, warm emotional resolution, distinguish good intensity from bad intensity.

### Gen 4: 16/30 (53%) — Partial recovery, +3 from Gen 3
**Prompt approach:** Emphasized direct character praise, recipient names, emotional vulnerability.

**Per-song:** Dillon 5/10, Rhonda 8/10, James 3/10

**What went wrong:** Recovered Rhonda but James stayed stuck at 3/10. Over-relied on "most personal detail = best" for James. The Dillon bridge miss persisted (kept picking the "break the chain" gut-punch).

**Updater diagnosis:** Direct character praise helped but James section remains a problem. Subtle model preference distinctions.

### Gen 5: 22/30 (73%) — Best score, +6 from Gen 4
**Prompt approach:** Used refined Gen 2 base (the peak before regression) with character praise and warm metaphor additions. Reframed task as "which makes recipient cry happy tears?"

**Per-song:** Dillon 7/10, Rhonda 10/10, James 5/10

**Remaining misses (8):**
- **Dillon (3):** verse-0 (haiku preferred over sonnet), chorus-0 (opus preferred — "steady in my storm" warmth), bridge-0 (sonnet preferred — persists across all 5 gens, guesser always picks the "break the chain" gut-punch)
- **James (5):** Consistently picks wrong on verse-0 line 2 (detail-packed vs warm), chorus-0 (both lines), verse-1 (both lines). The James options are genuinely closer in quality, making distinctions harder.

---

## Persistent Misses (Wrong All 5 Generations)

These couplet groups were NEVER correctly predicted:

1. **dillon-bridge-0-c0** — Every generation picks the "two troubled hearts / break the chain / baby girl won't know that pain" opus option. Sean always picks the sonnet "we came from the hard roads / look at this life and this love." The guesser can't resist the dramatic intensity of the chain-breaking line, but Sean consistently prefers the warm celebration.

2. **james-verse-1-c1** — Every generation picks opus ("carpenter hands" / "I come runnin' straight to you") or sonnet. Sean picks the simpler sonnet "calloused hands all day / pull up in that F-150, handsome as can be." The guesser overvalues the dramatic imagery and undervalues the simple, adoring observation.

---

## Prompt Evolution: Seed vs Best

| Dimension | Seed Prompt (Gen 1, 43%) | Best Prompt (Gen 5, 73%) |
|-----------|-------------------------|--------------------------|
| Frame | "Expert songwriter evaluating" | "Pick what makes recipient cry happy tears" |
| #1 Priority | Naturalness & flow | Narrative completeness & personal detail |
| #2 Priority | Emotional specificity | Warmth, sincerity & gratitude |
| #3 Priority | Both lines carry weight | Direct character praise |
| Cleverness | Valued as craft | Explicitly warned against |
| Names | Not mentioned | Called out as strong positive |
| Length | Penalized overstuffing | "Don't over-penalize longer lines" |
| Ending | Not addressed | Warm resolution > dramatic > funny |

---

## Files in This Experiment

| File | What It Is |
|------|-----------|
| `state.json` | Complete loop state — all 5 generations, every prediction, reasoning, score, updater analysis |
| `truth-set.json` | Sean's 30 picks (ground truth) |
| `seed-prompt.txt` | Generation 1 prompt |
| `PROMPT.md` | Loop execution instructions |
| `dashboard.html` | Live visualization dashboard |
| `dashboard.py` | Python server for dashboard (port 8877) |
| `summary_learnings_and_review.md` | This file |

---

## V2 Improvements (If We Run This Again)

1. **Hit analysis** — Updater should analyze what's working, not just what's failing
2. **Multi-run scoring** — 3 runs per prompt, use median to reduce noise
3. **Larger truth set** — More couplet groups or cross-validation splits
4. **Best-prompt anchoring** — Updater could optionally work from the highest-scoring prompt, not just the latest, to explore more efficiently
