# Attack on Selected Chain 03 - Exact `F_SL(rho)` Template Frontier

`selected/chain-03.md` is internally titled `Chain 01`. That is minor compared
with the mathematical issues, but it is still a real traceability problem in a
branch whose main risk is packaging drift.

## Bottom line

This is a real branch, and it is not obviously foolish. Step 6 really did hand
off the next theorem-facing question to repaired `G_tmpl` on `F_SL(rho)`, so a
family-local audit is the cleanest positive route still alive.

But the chain is unstable in exactly the place where it claims to become exact.
The local record already contains draft family arithmetic from Step 4:

- `Delta_tmpl = 1/4`
- `Delta_spec = 3 rho + rho^2`

on `F_SL(rho)` in the fallback Step-4 pro dossier and its check script.
At the same time, the Step-6 promoted-object memo still lists the
`rho`-dependent defect ledger as missing exact data. So this chain is caught in
a binary trap:

- if it accepts the Step-4 draft arithmetic, most of Step 3 collapses to a
  nearly trivial algebra exercise, and the main remaining work is provenance
  control;
- if it does not accept that draft arithmetic, the chain dies at Step 2.

That means the real unresolved issue is not "solve a deep five-step family
theorem." It is "can the repository honestly promote the existing `F_SL(rho)`
draft ledger into repaired same-currency theorem data?"

## Step-by-step critique

### Step 1 - Freeze The Family, Authority Sheet, And Allowed Scope

This step looks disciplined, but it already blurs two different jobs.

- Freezing the canonical packet semantics, repaired `G_tmpl`, thresholds
  `(1/4, 49/256)`, and fixed window `I = [0, 1]` is mostly duplicate work.
  Step 6 already froze those objects on the promoted ledger. Re-freezing them
  here risks producing a new memo that sounds foundational without adding any
  new authority.
- The step says Step-4/5 arithmetic "suggests a larger possible endpoint."
  That is dangerous shorthand. The recorded `sqrt(10)` endpoint lead comes from
  the old Step-4 spectator threshold `1/4`, not the repaired Step-5 threshold
  `49/256`. Carrying that old lead into the repaired branch invites stale
  arithmetic contamination.
- The scope is ambiguous in exactly the wrong place. Step 4 originally used the
  family range `0 < rho <= 1/12`. Step 6 then handed off the first exact
  theorem question on the carried range `0 < rho <= 1/16`. This chain wants
  the "true admissible interval" but never states whether it means the original
  Step-4 family or the already-carried subfamily. If it means the former, the
  branch is quietly reopening pre-Step-6 scope. If it means the latter, the
  interval question is partly pre-answered by the handoff.
- The kill condition is miscalibrated. The repo can recover an exact frozen
  definition of `F_SL(rho)` as a family on the canonical sheet. The real debt
  is not family definition. It is promoted same-currency formula authority for
  `Delta_tmpl(rho)` and `Delta_spec(rho)`. Step 1 can therefore "pass" while
  leaving the actual theorem bottleneck untouched.

Fair point in its favor: the refusal to infer closure from the template pass is
the right instinct. But that guardrail should be a premise, not a Step-1
deliverable.

### Step 2 - Derive The Exact `rho`-Dependent Defect Ledger

This is the real crux of the whole chain.

- The branch treats this as one normal derivation step. It is not. The local
  record already has candidate formulas in the Step-4 fallback dossier and in
  `pro_circuit_dossier_check.py`, but those formulas were not promoted at Step
  6. Step 6 explicitly says the exact `rho`-ledger is still missing. So Step 2
  is really a source-basis audit: are those formulas theorem-grade, or are they
  only draft arithmetic?
- The provenance is weaker than the chain admits. The Step-4 pro dossier says
  the only concrete pro-family ledgers on disk were family-level `O(mu)` /
  `O(rho)` descriptions plus a stalled draft in a runtime log, then a local
  recheck with a reproducible script. That is useful evidence, but it is not
  the same thing as a clean promoted family proof artifact.
- "Use existing checked arithmetic or scripts" is too permissive. The current
  script is a small arithmetic checker using hand-entered formulas, and it even
  prints the old unrepaired root `(-3 + sqrt(10)) / 2`. Treating that as
  family-proof authority would be exactly the kind of packaging inflation this
  branch is supposed to avoid.
- The step says to keep desired-channel and spectator contributions separate so
  the later boundary computation is exact. Fine. But if the current draft
  formulas are right, `Delta_tmpl` is identically `1/4` across the family and
  all the nontrivial `rho` dependence sits in `Delta_spec`. In that case the
  hard question is not "can the ledger be separated?" It is "why is this
  constant template defect genuinely structural rather than an artifact of the
  chosen normalization?"
- The kill condition is still too weak. Failing to get a family-level ledger is
  not the only danger. A family-level ledger copied from stale Step-4 draft
  arithmetic without upgraded authority is also not honest theorem input.

This step is strong only if it is treated as an adversarial validation pass on
already-suggested formulas. If it is treated as a routine derivation step, the
branch is underestimating its own hardest dependency.

### Step 3 - Solve The Admissible Interval And Identify The Sharp Boundary

This step is much weaker than it looks.

- If Step 2 validates the existing draft formulas, the interval computation is
  almost immediate:
  `Delta_tmpl = 1/4` contributes no interior restriction, and
  `3 rho + rho^2 <= 49/256`
  gives the boundary `rho = 1/16` exactly. So Step 3 is not a deep frontier
  analysis. It is algebra plus packaging.
- If Step 2 does not validate those formulas, Step 3 has nothing to solve.
  That means this is not really an independent theorem stage. It is completely
  hostage to Step 2 provenance.
- The explicit instruction to test
  `rho_* = (-3 + sqrt(10)) / 2`
  is a red flag. That root belongs to the old spectator threshold `1/4`. Under
  the repaired Step-5 sheet, it is not the live endpoint unless the family
  formula itself changes. Keeping it psychologically active makes it too easy
  to smuggle pre-repair arithmetic into a repaired family theorem.
- The phrase "identify the true admissible interval" still overreaches. If the
  branch stays inside the Step-6 carried range `0 < rho <= 1/16`, then it can
  prove uniform admissibility on that carried subfamily and maybe show
  sharpness at its endpoint. That is not automatically the same thing as
  identifying the full admissible interval of the original Step-4 family.
- The kill condition misses the most likely failure mode: not threshold retuning
  or asymptotic error terms, but false exactness created by elevating a draft
  family ansatz into a proved repaired ledger.

If the branch lands honestly, this step likely reduces to "the repaired
boundary is exactly the carried witness `1/16`." Useful, but much smaller than
the chain's wording suggests.

### Step 4 - Audit What The Family Theorem Does Not Say About Closure

This guardrail is necessary, but it arrives too late.

- Step 8 already established that static admissibility on repaired gates does
  not by itself yield honest finite closure on the frozen ledger for the
  carried witness `F_SS(1/12)`. That is not a theorem about `F_SL(rho)`, but
  it is enough to make closure non-implication a front-loaded warning rather
  than a late-stage audit.
- The comparison target is awkward. This chain is family-local and
  template-facing on `F_SL(rho)`. Step 8 is witness-local and closure-facing on
  `F_SS(1/12)`. Comparing them is useful for rhetoric control, but it is not
  likely to produce new structure. The likely honest result is just a scope
  memo saying "template admissibility remains template admissibility."
- The line about whether "one extra exact hypothesis" could turn the family
  theorem into a closure-relevant statement is too loose. That invites the
  branch to reopen Chain 02 or Chain 03 territory under a nicer label.
- The kill condition is fair, but again it is staged too late. If the branch
  needs a closure assumption to sound important, that should be caught before
  theorem packaging begins.

This step is good as a brake. It is weak as a source of new mathematical
content.

### Step 5 - Package The Family-Level Verdict

This step is where the branch's positive bias can leak into the writeup.

- The central premise already frames this as the "cleanest surviving positive
  theorem route." That makes Step 5 vulnerable to overpackaging a bookkeeping
  cleanup as a theorem.
- The allowed endpoints are not equally demanding. An exact admissible-interval
  theorem, a corrected witness-only memo, and a bounded negative do not have
  the same burden of proof. Because the chain never narrows that burden early,
  Step 5 can end up naming the best-looking partial result rather than the most
  honestly earned one.
- The final kill condition protects against illicit generalization from
  `F_SL(rho)` to the whole one-bridge class. Good. But it does not protect
  against a different overclaim: presenting repaired packaging of Step-4 draft
  arithmetic as if it were a genuinely new family theorem.

The strongest honest package may well be modest:
a same-currency family admissibility memo with exact endpoint `rho = 1/16` and
an explicit statement that nothing closure-level follows.

## Structural weaknesses of the whole chain

### 1. The branch's real bottleneck is provenance, not algebra

The family formulas are already suggested on disk. Step 6 still refuses to
promote them. So the actual question is whether the repo can certify those
formulas on the repaired ledger. The chain disguises that source-basis problem
as a five-step theorem arc.

### 2. It risks mixing unrepaired and repaired arithmetic

The chain explicitly carries a Step-4 lead about a larger endpoint while
working on the repaired Step-5 defect sheet. That is exactly how stale
pre-repair numerics get smuggled into a supposedly repaired theorem branch.

### 3. The interval question is scope-ambiguous

The chain talks about the "true admissible interval" without fixing whether the
domain is the original Step-4 family `0 < rho <= 1/12` or the Step-6 carried
family `0 < rho <= 1/16`. That ambiguity matters:

- on the smaller carried range, the endpoint problem is largely predetermined;
- on the larger original range, the chain is reopening earlier scope.

### 4. The middle of the chain is either trivial or blocked

If the draft formulas are valid, Step 3 becomes almost automatic and Step 4 is
mostly a scope disclaimer. If the draft formulas are not valid, the chain fails
at Step 2. That is not a robust five-stage program.

### 5. The guardrails are staged too late

The anti-overclaim discipline about closure should be frozen before the family
theorem work starts. Waiting until Step 4 lets the branch do theorem-flavored
work under a scope illusion that the repo has already warned against.

### 6. It is more redundant with the Step-6 handoff than advertised

Step 6 already says:

- the next exact theorem question is on `F_SL(rho)`,
- the carried range is `0 < rho <= 1/16`,
- the exact `rho`-ledger is still missing,
- boundary-sharpness is still unproved,
- and any later use beyond family-level admissibility needs a clearly stated
  transfer scope.

This chain adds some sequencing language, but very little new strategic
content.

### 7. The label mismatch is a small but real workflow warning

`selected/chain-03.md` being titled `Chain 01` is not mathematically fatal.
But it is exactly the kind of bookkeeping slippage that makes theorem-packaging
drift harder to detect.

## What is genuinely strong

- The chain stays inside the Step-6 promoted object instead of reopening the
  whole mission.
- It keeps the claim family-local and refuses whole-class closure rhetoric.
- It correctly identifies `F_SL(1/16)` as the carried witness that must either
  be promoted into a family theorem or downgraded to a witness-local memo.
- Its instinct to include an explicit no-overclaim scope audit is good, even if
  badly timed.

## Fair verdict

This chain is real, and it may still be worth doing. But it is not five hard
steps. It is one hard step and several packaging consequences.

The one hard step is:
can the repository honestly upgrade the existing Step-4 `F_SL(rho)` arithmetic
into repaired same-currency theorem data?

If yes, the repaired boundary likely collapses to the already-carried witness
`rho = 1/16`, and the rest of the chain is mostly scope control plus honest
statement of limits.

If no, the chain should fail fast as a source-basis failure instead of
pretending to be a fresh derivation program.

So the ruthless but fair judgment is:

- good choice of object,
- good instinct about scope,
- but too much hidden dependence on fallback Step-4 draft arithmetic,
- too much room for stale unrepaired endpoint lore to leak back in,
- and too much theatrical sequencing around what is really a provenance audit.
