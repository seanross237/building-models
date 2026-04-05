---
description: "Start a Usain Bolt sprint - lightweight autonomous development"
argument-hint: "[description of what to build]"
allowed-tools: ["Bash(./scripts/usain-bolt/usain-bolt-setup.sh:*)", "Bash(mkdir:*)"]
---

# Usain Bolt Sprint

You are starting a **Usain Bolt** sprint — a lightweight autonomous development workflow. Faster planning than Big Build, same stop-hook execution loop.

## Phase 1: Quick Planning (You Are Here)

### 1. Clarifying Questions (ONE Round Only)

The user's goal: **$ARGUMENTS**

Ask ONE message of clarifying questions. Cover all of these in a single shot — do NOT go back and forth:

- **Scope**: What's in, what's out? Any edge cases to handle or skip?
- **Testing**: Specific test scenarios, or test as you see fit?
- **Open questions**: Ambiguities, architectural choices, or trade-offs to resolve NOW (you can't ask later)
- **Constraints**: Files not to touch, patterns to follow, dependencies?

Keep it concise — bullet points, not paragraphs. This is a sprint, not an interrogation.

### 2. Write Plan & Activate

Once the user answers:

1. **Derive a slug** — lowercase, hyphenated, 2-4 words (e.g., `lyrics-page`, `payment-fix`, `love-fund-ui`)
2. Create the `.usain-bolt/` directory and write these files:

#### `.usain-bolt/USAIN-BOLT-{slug}-PLAN.md`
Concise plan including:
- What's being built (1-2 paragraph overview)
- Work items with clear acceptance criteria
- Testing approach
- Key decisions made during planning
- Constraints

#### `.usain-bolt/USAIN-BOLT-{slug}-PROGRESS.md`
```
# {Feature Name} Progress

## Status: IN PROGRESS

### Work Items
- [ ] Item 1 (0 attempts)
- [ ] Item 2 (0 attempts)
...

### Testing
- [ ] Test 1 (0 attempts)
- [ ] Test 2 (0 attempts)
...
```

#### `.usain-bolt/USAIN-BOLT-{slug}-HANDOFF.md`
```
# {Feature Name} Handoff

## Current Status
Starting execution.

## Last Completed
(none yet)

## Next Up
(first work item)

## Notes
(none)
```

### 3. Activate the Loop

After writing all files, run:
```!
./scripts/usain-bolt/usain-bolt-setup.sh --slug {slug} --max-iterations 30
```

Then **immediately begin working on the first item** in `USAIN-BOLT-{slug}-PROGRESS.md`.

## Critical Notes

- The plan files MUST be thorough — they survive context window compression, your conversation memory does not
- For fully autonomous operation, the user should be running with `--dangerously-skip-permissions`
- Once the loop is active, every time you finish a turn, you'll receive a meta-prompt to continue
- You MUST update `USAIN-BOLT-{slug}-HANDOFF.md` before each turn ends — it's your memory across context compressions
- To cancel: `/cancel-usain-bolt`
