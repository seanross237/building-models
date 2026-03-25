# Stumper Loop

You are running an iterative process to discover questions that stump AI agents. Your goal is to find 10 questions that a fresh Claude agent consistently gets wrong.

## Setup

Your state file is at `atlas-supporting-model-experiments/03-09-stumper-loop/state.json`. **Read it first** before doing anything. It contains your progress, past attempts, and learnings from previous iterations.

## Each Iteration

### Step 1: Read State
Read `atlas-supporting-model-experiments/03-09-stumper-loop/state.json`. Review:
- How many stumpers you've found so far
- What strategies you've tried and how they performed
- What you've learned about what makes questions hard
- What types of questions have failed (the agent solved them easily)

### Step 2: Strategize
Based on your learnings, decide what type of questions to generate this round. If this is your first iteration, start with a mix of categories:
- Spatial reasoning and counting
- Multi-step logic with misdirection
- Problems requiring precise tracking (e.g., state changes, object movements)
- Math with subtle tricks
- Questions that exploit known LLM biases (e.g., pattern-matching over reasoning, anchoring)

As you learn what works, **lean into the categories that produce stumpers and abandon what doesn't work.** Write down your strategy for this round before generating questions.

### Step 3: Generate 5 Candidate Questions
For each question, you must provide:
- The question text (clear, unambiguous)
- The correct answer (with your step-by-step reasoning for why it's correct)
- Why you think this will stump an AI (what bias or limitation it exploits)

**Critical: Your answer must be correct.** Work through each problem carefully. If you're not 100% sure of the answer, don't include it. A stumper with a wrong answer key is useless.

### Step 4: Test Each Question
For each candidate question, use the Agent tool to spawn a fresh sub-agent. The sub-agent prompt should be EXACTLY:

> Answer the following question. Think step by step, then give your final answer on the last line in the format "The answer is: [answer]"
>
> [THE QUESTION]

The sub-agent must NOT know:
- That this is a test
- What the correct answer is
- That you're looking for questions it gets wrong
- Anything about this project

Just give it the question cold.

### Step 5: Score Results
For each candidate:
- Extract the sub-agent's answer
- Compare to your answer key
- Mark as STUMPER (agent got it wrong) or SOLVED (agent got it right)
- For stumpers: note WHY the agent failed (what mistake did it make? what bias did it show?)
- For solved: note what the agent did right (so you can design around it next time)

### Step 6: Update State
Update `atlas-supporting-model-experiments/03-09-stumper-loop/state.json` with:
- Any new stumpers added to the `stumpers` array (include: question, correct_answer, agent_answer, failure_analysis, category, iteration_found)
- Failed candidates added to `failed_candidates` (include: question, correct_answer, category — keep it brief, just enough to not repeat them)
- Update `strategies_tried` with what you tried this round and how it went
- Update `learnings` with any new insights about what makes questions hard
- Increment `iteration`
- Set `done: true` if you've reached the target number of stumpers

### Step 7: Report
Print a brief summary:
- Stumpers found this round: X
- Total stumpers: X / 10
- Key learning from this round
- Strategy for next round (if not done)

## Rules

1. **Never reuse a question** — check failed_candidates and stumpers before generating
2. **Quality over quantity** — 1 reliable stumper is better than 5 flaky ones
3. **Verify your own answers** — if you realize your answer key was wrong, remove that stumper
4. **Keep iterating** — don't stop until you have 10 stumpers or have completed 10 iterations (whichever comes first)
5. **Be creative** — try weird stuff. Combine categories. Exploit edge cases. The goal is to find blind spots.
6. **Track everything** — the state file is your memory. Write detailed learnings so future iterations (or future sessions) can pick up where you left off.

## When You're Done

When you reach 10 stumpers (or 10 iterations), write a final summary to `atlas-supporting-model-experiments/03-09-stumper-loop/RESULTS.md` with:
- All 10 stumpers with questions, correct answers, and failure analyses
- A taxonomy of what makes questions hard for AI
- Recommendations for which categories to explore further
