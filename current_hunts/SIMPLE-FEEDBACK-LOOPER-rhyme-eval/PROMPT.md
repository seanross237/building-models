# Rhyme-Eval: Prompt Optimization Loop

You are running an iterative loop that optimizes a prompt for predicting which song couplet a human expert prefers. You run for 5 generations, improving the prompt each time.

## Files

- **State:** `../../building_models/attempts/SIMPLE-FEEDBACK-LOOPER-rhyme-eval-03-24/state.json`
- **Truth set:** `../../building_models/attempts/SIMPLE-FEEDBACK-LOOPER-rhyme-eval-03-24/truth-set.json`
- **Seed prompt:** `../../building_models/attempts/SIMPLE-FEEDBACK-LOOPER-rhyme-eval-03-24/seed-prompt.txt`

**Read state.json first.** If `done` is true, print the final summary and stop. If `current_generation` > 0, you are resuming — pick up from the next generation.

---

## Pre-Flight Check

Before starting generation 1, verify:
1. `truth-set.json` exists
2. It has comparison groups
3. ALL groups have a non-null `pick` value (the human has rated them all)

If any check fails, tell the user what's missing and stop.

---

## Shuffling Algorithm

To prevent position bias, shuffle options before presenting them to the guesser. Use a deterministic seeded shuffle based on the group ID.

**You MUST compute the shuffles using this Node.js script via Bash** (do not try to compute by hand):

```bash
node -e "
const data = require('./../../building_models/attempts/SIMPLE-FEEDBACK-LOOPER-rhyme-eval-03-24/truth-set.json');

function seededShuffle(arr, seed) {
  const result = [...arr];
  let hash = 0;
  for (let i = 0; i < seed.length; i++) {
    hash = ((hash << 5) - hash + seed.charCodeAt(i)) | 0;
  }
  for (let i = result.length - 1; i > 0; i--) {
    hash = ((hash << 5) - hash + i) | 0;
    const j = Math.abs(hash) % (i + 1);
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

const LETTERS = ['A', 'B', 'C', 'D'];
const result = data.comparison_groups.map(group => {
  const shuffled = seededShuffle(group.options.map((opt, i) => ({ ...opt, originalIndex: i })), group.id);
  return {
    group_id: group.id,
    recipientName: group.recipientName,
    section: group.section,
    sectionInstance: group.sectionInstance,
    sean_pick: group.pick,
    options: shuffled.map((opt, i) => ({
      letter: LETTERS[i],
      line1: opt.line1,
      line2: opt.line2,
      model: opt.model
    }))
  };
});
console.log(JSON.stringify(result, null, 2));
"
```

Save this output — it gives you every group with shuffled options (letter-labeled) and the mapping back to model names. Use this for both building the guesser payload and scoring.

---

## Each Generation

### Step 1: Determine the Prompt

- **Generation 1:** Read `seed-prompt.txt`
- **Generation 2+:** Use the `next_prompt` field from the previous generation's record in state.json

### Step 2: Build the Guesser Payload

Using the shuffled data from the Node.js script, construct a single message. Format:

```
[The evaluation prompt from Step 1]

---

Here are [N] couplet comparison groups from personalized songs. For each group, pick the best couplet option.

GROUP 1: [recipientName] — [section label]
  A) [line1]
     [line2]
  B) [line1]
     [line2]
  C) [line1]
     [line2]

GROUP 2: ...
```

For section labels, use:
- sectionInstance 0: just the section name (e.g., "Verse")
- sectionInstance 1+: section name + instance+1 (e.g., "Verse 2", "Pre-chorus 2")

**The guesser sees:**
- The evaluation prompt
- The couplet groups with options labeled A, B, C (or D)
- Recipient name and section label

**The guesser does NOT see:**
- Model names (only letters)
- Customer context (only recipient name)
- Any indication this is a test or that there are correct answers

### Step 3: Spawn the Guesser Agent

Use the Agent tool to spawn a fresh sub-agent. Pass the full payload from Step 2 as the prompt.

The sub-agent must NOT know it's being tested. Do NOT include any framing like "you are being evaluated" or "predict what the human picked."

Parse the guesser's JSON response to extract each group's pick letter and reasoning. If the response isn't clean JSON, try extracting it from markdown code fences.

### Step 4: Score

For each group:
1. Get the guesser's pick letter (e.g., "B")
2. Look up which model that letter maps to using the shuffled data
3. Compare to the human's pick in the shuffled data (`sean_pick`)
4. Record: hit (match) or miss (mismatch)

Compute: `hits / total = accuracy`

### Step 5: Spawn the Updater Agent

Use the Agent tool to spawn a fresh sub-agent with this prompt:

```
You are a prompt engineering expert. Your job is to improve an evaluation prompt that helps an AI pick which song couplet a human expert would prefer.

Here is the prompt that was just used:

<prompt>
[THE FULL PROMPT FROM THIS GENERATION]
</prompt>

It scored [X]/[TOTAL] ([Y]%) accuracy against the human expert's preferences.

Here is the complete scorecard — every group, what was predicted, what the human actually picked, and the guesser's reasoning:

[FOR EACH GROUP:]
---
Group [N]: [recipient] — [section]
Options:
  A) [line1] / [line2]
  B) [line1] / [line2]
  C) [line1] / [line2]
Guesser picked: [letter] — reasoning: "[reasoning]"
Human picked: [letter that maps to human's pick]
Result: HIT / MISS
---

Analyze the results carefully. Look for patterns:
- Does the guesser over-value or under-value certain qualities?
- Are there systematic biases (e.g., always preferring shorter lines, or always preferring perfect rhymes over natural flow)?
- What does the human seem to consistently value that the guesser is missing?
- Are there patterns in the HITS too — what is the guesser getting right?

Then write ONE improved prompt. The new prompt should:
1. Keep the same JSON output format (picks array with group number, pick letter, and reasoning)
2. Adjust criteria, weights, or framing to better match the human's actual preferences
3. Be a complete, self-contained prompt (not a diff or delta)
4. Include specific guidance based on the patterns you found

Return your response as JSON:
{
  "analysis": "Your analysis of what patterns you found — what the human values, where the guesser went wrong, what to change",
  "new_prompt": "The complete improved evaluation prompt"
}
```

Parse the updater's response to extract the analysis and new prompt.

### Step 6: Update State

Read the current state.json, then write back with the new generation appended:

```json
{
  "done": false,
  "total_generations": 5,
  "current_generation": [THIS GENERATION NUMBER],
  "generations": [
    ...previous generations...,
    {
      "generation": [NUMBER],
      "prompt_used": "[full prompt text]",
      "predictions": [
        {
          "group_id": "[id]",
          "recipient": "[name]",
          "section": "[section label]",
          "options_presented": [
            { "letter": "A", "line1": "...", "line2": "...", "model": "[original model]" },
            { "letter": "B", "line1": "...", "line2": "...", "model": "[original model]" },
            { "letter": "C", "line1": "...", "line2": "...", "model": "[original model]" }
          ],
          "guesser_pick_letter": "[letter]",
          "guesser_pick_model": "[model name]",
          "guesser_reasoning": "[reasoning text]",
          "sean_pick_model": "[model name]",
          "hit": true/false
        }
      ],
      "score": {
        "hits": [N],
        "misses": [N],
        "total": [N],
        "accuracy": [0.0 to 1.0]
      },
      "misses_detail": [
        {
          "group_id": "[id]",
          "recipient": "[name]",
          "section": "[section]",
          "guesser_picked": { "letter": "[L]", "model": "[model]", "line1": "...", "line2": "..." },
          "sean_picked": { "model": "[model]", "line1": "...", "line2": "..." },
          "guesser_reasoning": "[reasoning]"
        }
      ],
      "updater_analysis": "[analysis text]",
      "next_prompt": "[the improved prompt for the next generation]"
    }
  ]
}
```

If this was the final generation (generation number == total_generations), set `"done": true` and omit `next_prompt`.

### Step 7: Report

Print to the user:

```
=== Generation [N] Complete ===
Score: [X]/[TOTAL] ([Y]%)
Hits: [count]
Misses: [count]
Updater insight: [1-2 sentence summary of analysis]
```

If not done, proceed immediately to the next generation.

---

## After All Generations: Final Summary

Print:

```
========================================
  RHYME-EVAL COMPLETE — 5 GENERATIONS
========================================

LEADERBOARD:
  #1: Generation [N] — [X]/[TOTAL] ([Y]%)
  #2: Generation [N] — [X]/[TOTAL] ([Y]%)
  #3: Generation [N] — [X]/[TOTAL] ([Y]%)
  #4: Generation [N] — [X]/[TOTAL] ([Y]%)
  #5: Generation [N] — [X]/[TOTAL] ([Y]%)

IMPROVEMENT: [first gen score] → [best score] ([+/- delta])

BEST PROMPT (Generation [N]):
[Full text of the best-scoring prompt]

KEY LEARNINGS:
[Compile the updater analyses across all generations into 3-5 bullet points
about what the human values in couplets]
```

---

## Rules

1. **Resumable** — Always read state.json first. If current_generation is 3 and done is false, start generation 4.
2. **Log EVERYTHING** — state.json is the complete record. Every prediction, every reasoning, every score, every analysis.
3. **Guesser is cold** — It does not know it's being tested. Do not leak test context.
4. **Updater sees everything** — Give it the full scorecard (all groups, not just misses) so it can find patterns in both hits and misses.
5. **Deterministic shuffling** — Always use the Node.js script. Same group ID = same letter assignment.
6. **Run all 5 generations** — Even if accuracy is high, always complete all generations.
7. **Write state after each generation** — Don't batch. If the session dies mid-run, we lose at most one generation of work.
