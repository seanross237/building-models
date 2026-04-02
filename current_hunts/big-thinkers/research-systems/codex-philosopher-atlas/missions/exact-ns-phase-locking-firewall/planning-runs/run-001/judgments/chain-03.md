# Judgment on Selected Chain 03

## Selection note

`selected/chain-03.md` is internally titled "Chain 04." That is a real
bookkeeping defect in the handoff artifact. It does not invalidate the branch's
mathematical premise, but it should be recorded as a process weakness.

## Overall judgment

The attacker is right about the main issue: as written, this branch can support
only a scoped intrinsicity audit, not a universal negative such as "no
intrinsic phase object survives." The core branch is still worth keeping. Its
distinctive value is as an early guardrail that can either promote a genuinely
intrinsic object or close a precisely defined subfamily. The refined version
should therefore narrow the claim scope, formalize the equivalence test, and
separate intrinsicity from downstream usefulness.

## Major critique rulings

### 1. The search scope is too narrow to justify the advertised negative

Label: `valid`

The original "at most three" candidate rule and first-pass kill condition are
far too thin to support a branch-closing nonexistence claim. At most they can
support a negative result over a declared candidate class. The refined chain
must define that class explicitly before any kill memo is allowed.

### 2. Candidate generation is biased by preferred semantics and theorem use

Label: `partially valid`

The criticism is correct that the original examples lean toward delayed-transfer
language and that "intended theorem use" should not be an admissibility gate.
But the examples were illustrative rather than logically binding. The right fix
is not to ban examples; it is to replace planner-picked examples with a neutral
candidate grammar or basis and move theorem relevance to a later, non-gating
step.

### 3. The intrinsicity screen is underformalized and too permissive

Label: `valid`

This is the strongest technical objection. The original chain names several
symmetries and conventions but never states the actual equivalence relation. It
also leaves too much room in the "canonical-but-honest" bucket. Any object that
depends on a packet sheet, desired channel, or similarly external bookkeeping
cannot count as an intrinsic survivor for this mission. The refined chain must
state the invariance criterion explicitly and treat canonically representable
but non-intrinsic objects as side notes, not promoted wins.

### 4. The dynamics step changes the target from existence to tractability

Label: `valid`

An object can be intrinsic even if its exact evolution law is messy, open, or
not immediately theorem-ready. The original chain incorrectly lets dynamic
convenience act as a survival criterion. In the refined chain, dynamics should
classify the usefulness of intrinsic survivors, not determine whether they are
real.

### 5. The fixture audit is being asked to do too much

Label: `partially valid`

The attacker is right that the original fixture step is too thin and too strong
if used as a kill gate. But it would be an overcorrection to remove fixtures
entirely. Inherited fixtures can still serve as diagnostics, provided they are
not treated as exhaustive validators and provided failure there does not, by
itself, disqualify an otherwise intrinsic object.

### 6. The final fork overreaches relative to the evidence gathered

Label: `valid`

The original closing memo promises more than the branch could honestly earn. A
defensible negative must be scoped to a declared candidate class and formal
equivalence test. A survivor can be promoted only as an intrinsic object within
that same scope.

### 7. The chain conflates definability, invariance, usefulness, and diagnostics

Label: `valid`

This conflation is real and materially weakens the branch. Those are four
different questions. The refined chain must evaluate them in sequence and avoid
treating failure on a later usefulness or diagnostic step as proof of
nonexistence.

### 8. The branch is structurally biased toward a predetermined negative

Label: `partially valid`

The original version leans too hard toward a kill memo because the search is
narrow, the intrinsicity bucket is vague, and the fixture step is too punitive.
Still, the branch is not inherently invalid as a negative-audit branch. With a
neutral candidate class and scoped conclusions, it becomes a fair guardrail
rather than a stacked prosecution.

### 9. The selection artifact mismatch matters

Label: `valid`

This is a process critique, not a mathematical refutation. It remains worth
recording because a branch that aims to issue decision-grade closure memos
should not already contain chain-identity ambiguity in its own handoff file.

## Resulting disposition

Keep the branch, but narrow it sharply. Its honest output space is:

- a promoted intrinsic object within a formally declared candidate class and
  equivalence relation; or
- a scoped negative memo saying no intrinsic survivor exists within that class
  under that equivalence test.

It should not claim a universal mission-level nonexistence result.

## Probability assessment

Probability that the refined chain can yield a presentable result: `0.74`

Rationale: this branch has a fairly good chance of producing a presentable
output once the conclusion is scoped correctly, because even a negative result
can be valuable if it is tied to an explicit candidate class and invariance
test. The main remaining risk is not total failure; it is ending with a class
definition that is still too vague to support a clean memo.
