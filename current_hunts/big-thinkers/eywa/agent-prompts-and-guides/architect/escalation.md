# Escalation Guidance

When a child node completes (or fails/escalates), you are re-spawned to decide what happens next. You have three options.

## Continue

The plan is on track. Proceed to the next step.

**Signals:**
- Child succeeded and produced the expected type of output
- Next step's preconditions are met
- No new information that invalidates remaining steps
- The results are roughly what you anticipated when you made the plan

**Action:** Write "continue" to for-orchestrator/eval-decision (just the word, nothing else). If the next step in the plan depends on completed steps, also write output/context-for-next-step.md — a concise summary of relevant findings from completed children that the next step will need. Don't dump raw outputs; summarize what matters. If the next step is independent, skip this file. Update output/state.md with your reasoning.

## Replan

The goal is still achievable, but the approach needs to change.

**Signals:**
- Child succeeded but revealed information that changes what the remaining steps should be
- Child failed, but the failure suggests a different approach that could still achieve your goal
- An assumption in your plan turned out to be wrong, but the overall objective is still reachable
- You can see a concrete alternative path forward

**Action:** Write an updated output/plan.md (Status: draft). Write "replan" to for-orchestrator/eval-decision (just the word). Update output/state.md with what changed and why. The orchestrator will cancel unstarted children and route the new plan through review if needed.

**Important:** Preserve completed work. If steps 1-2 are done and valid, your new plan should build on their results, not redo them. Only replan the remaining steps.

## Escalate

You cannot produce what your parent expects from you.

**Signals:**
- Child failure reveals that your goal itself is wrong, impossible, or based on a false premise
- Multiple children have failed in ways that suggest a fundamental misunderstanding of the problem
- You've already replanned once and the replan also failed — you're in a loop
- You've learned something that changes the broader picture in a way your parent needs to know about

**Action:** Write output/escalation.md explaining: what you attempted, what you learned, why you can't continue, and what you recommend. Write "escalate" to for-orchestrator/eval-decision (just the word). Update output/state.md.

## The Core Question

> "Can I still produce what my parent expects from me, given what I now know?"

- **Yes, and the plan still works** → Continue
- **Yes, but I need a different approach** → Replan
- **No** → Escalate

## Anti-Patterns

- **Mechanical continuing:** A child produces a result that clearly contradicts the premise of later steps, and you continue anyway because "that's what the plan says." Read the results. Think about what they mean for the remaining work.
- **Infinite replanning:** If you've replanned twice and are about to replan again, escalate instead. You don't have a good enough model of the problem to plan your way out of it.
- **Premature escalation:** A single child failure doesn't mean the goal is impossible. Consider whether a different approach (replan) could work before giving up.
- **Escalating without useful information:** "I couldn't do it" is a worthless escalation. Your parent needs to know: what did you try, what did you learn, and what does that imply?

## What to Capture

Include your reasoning in output/state.md:
- Which option you chose and why
- What in the child's result drove the decision
- What you considered and rejected
- If continuing: any concerns about remaining steps
- If replanning: what specifically changed and what you're preserving
- If escalating: what you recommend your parent do
