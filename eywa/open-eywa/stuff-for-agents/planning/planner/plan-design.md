# Plan Design Guidance

## Plan Format (Strict)

The orchestrator parses your plan mechanically. You MUST follow this exact format:

```markdown
## Plan
Status: draft
Review: low | medium

### Step 1: {short-name}
Goal: {self-contained goal description}
Complexity: {1-10}
Importance: {1-10}
Dependencies: none | step N, step M
Independent: yes | no
Confidence: high | medium | low
Verifiable: yes | partially | no

### Step 2: {short-name}
Goal: {self-contained goal description}
Complexity: {1-10}
Importance: {1-10}
Dependencies: step 1
Independent: no
Confidence: high | medium | low
Verifiable: yes | partially | no
```

## Critical Format Rules

The `Goal` field is extracted verbatim and becomes the child's `input/parent-instructions.md`.

This means:

- each Goal must make sense to a fresh agent with no plan context
- never refer to "the parent's goal", "as discussed above", or "from step 1"
- include enough context that a fresh agent knows what to do, what to produce, and how to judge success

## Routing Logic

Open-Eywa routes children mechanically after depth adjustment:

- adjusted C x I > 30 -> `planner`
- adjusted C x I <= 30 -> `worker`

You do not decide the child role directly. You score honestly and the orchestrator routes.

## Scoring Guidance

### Complexity

- 1-3 -> straightforward lookup, simple computation, or narrow task
- 4-6 -> requires judgment, multiple considerations, or medium investigation
- 7-10 -> deep analysis, multi-part reasoning, or creative problem-solving

### Importance

- 1-3 -> nice to have
- 4-6 -> important but recoverable
- 7-10 -> essential to the mission

## Dependency Labels

- `Dependencies: none` means the step can start immediately
- `Dependencies: step 1, step 3` means those steps must finish first
- `Independent: yes` means the step has no dependencies
- `Independent: no` means the step depends on at least one prior step

## Review Tier

- `low` -> routine plan, low downside if imperfect
- `medium` -> getting this plan wrong would waste significant work or time

## Useful Patterns

### Survey tasks

1. Broad scan
2. Deep dive on promising branches
3. Synthesize and assess

### Verification tasks

1. State or reproduce the claim precisely
2. Test assumptions and edge cases
3. Conclude: confirmed / refuted / inconclusive

### Construction tasks

1. Gather context or tools
2. Build
3. Verify

### Analysis tasks

1-N. Independent sub-analyses
N+1. Synthesis

## Common Mistakes

- too many tiny steps
- vague goals
- goals that depend on hidden plan context
- including a final parent-level synthesis step as a child step
- predetermined conclusions
- plans with no honest failure path
