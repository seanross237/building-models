# Chain 03 - Tensor-Stretching Audit with Early Tao Screen and Degeneracy Discipline

## Central Premise

Tensor structure around strain, vorticity, and the pressure Hessian is worth
auditing only if it can do more than repackage known geometric criteria. The
refined chain therefore treats "exact but non-coercive" as the default baseline
and asks whether any tensor observable can survive three tests at once:
full nonlocal coupling, instability near spectral degeneracy, and a concrete
Tao discriminator.

## Verifiable Result Target

Either:

- a theorem-grade conditional criterion, tensor control lemma, or sharply
  reduced model with a rigorous error bridge that controls the full stretching
  term in a way not obviously preserved by Tao-style averaging; or
- a calibrated obstruction memo showing exactly why candidate tensor observables
  fail: prior-art redundancy, nonlocal freedom, eigenframe degeneracy,
  representation dependence, or collapse to a known open criterion.

## Why This Chain Is Still Worth Keeping

This branch still targets the real nonlinear mechanism, `S\omega \cdot \omega`,
instead of moving to a generic norm surrogate. Its value is no longer the hope
that tensor language itself solves the problem, but the chance to determine
precisely whether any NS-specific tensor feature carries genuine control.

## Ordered Steps

### Step 1 - Build an exact tensor ledger with adversarial nonlocal accounting

- Depends on: none.
- Action: assemble the exact identities relating `S`, `\omega`, and
  `\nabla^2 p`, including the local-plus-harmonic pressure split.
- Action: mark, for each identity, what is exact NS structure, what is generic
  Calderon-Zygmund repackaging, and what nonlocal freedom remains in the
  harmonic far-field Hessian.
- Action: fix one or two canonical stretching representations up front so later
  steps cannot switch coordinates opportunistically.
- Expected output: a tensor ledger separating exact identities, nonlocal debt,
  and representation choices.
- Kill condition: if the ledger already shows that every candidate representation
  differs only cosmetically from generic singular-integral structure with no
  one-sided leverage target, stop and record a direct obstruction.

### Step 2 - Run a prior-art and admissibility screen before choosing observables

- Depends on: Step 1.
- Action: list the nearest prior-art families the chain could accidentally
  rediscover: strain-eigenvalue criteria, vorticity alignment, geometric
  depletion, pressure-Hessian closures, and restricted-Euler-style reductions.
- Action: define admissibility filters for candidate observables. Each candidate
  must have:
  - a concrete role in controlling the full stretching term;
  - an explicit Tao discriminator stated in advance;
  - resistance to eigenvalue-degeneracy pathologies or a plan to avoid them;
  - dynamic meaning beyond static geometry;
  - and assumptions that are at least in principle monitorable.
- Action: shortlist only the observables that survive this filter.
- Expected output: an observable audit table with prior-art adjacency, scaling,
  Tao discriminator, degeneracy exposure, and intended leverage point.
- Kill condition: if no observable survives the admissibility screen, close the
  branch negatively rather than proceeding with attractive but non-operational
  diagnostics.

### Step 3 - Stress-test Tao sensitivity and eigenframe stability before estimates

- Depends on: Step 2.
- Action: for each shortlisted observable, state exactly what feature should fail
  in Tao's averaged model: sign coupling, frame coherence, cancellation,
  commutator structure, or another named mechanism.
- Action: test whether that feature is genuinely specific or merely a formal
  rephrasing of exact NS identities that averaging could preserve in spirit.
- Action: if the observable uses eigenvectors or alignment, analyze failure near
  repeated eigenvalues and decide whether the route can be reformulated in a
  frame-invariant way.
- Expected output: a Tao-and-degeneracy memo that either licenses or rejects
  each observable before detailed control claims.
- Kill condition: if the Tao discriminator is post hoc, or if the route depends
  on unstable eigenframe hypotheses with no invariant substitute, stop.

### Step 4 - Test whether any observable controls the full stretching mechanism

- Depends on: Step 3.
- Action: using the canonical representation fixed in Step 1, test whether the
  lead observable controls the full `S\omega \cdot \omega` term rather than a
  self-induced, local, or reduced-model fragment.
- Action: charge all nonlocal pressure-Hessian debt explicitly, including any
  far-field contribution that can rotate or amplify strain independently of the
  local geometry.
- Action: classify the outcome into one of four buckets:
  - restatement of a known open criterion;
  - reduced-model-only control;
  - faithful NS statement with unverifiable or unpreserved hypotheses;
  - genuine new leverage on full stretching.
- Expected output: a control-or-obstruction table saying exactly which bucket
  each candidate lands in and why.
- Kill condition: if every candidate falls into one of the first three buckets,
  terminate with an obstruction memo and do not promote the branch.

### Step 5 - Promote only a non-circular survivor into proposition scale

- Depends on: Step 4.
- Action: if one candidate reaches the fourth bucket, translate it into a
  conditional criterion, control lemma, or reduced-model proposition only with
  explicit assumptions, preservation requirements, and the first missing theorem.
- Action: reject any output that is merely a renamed alignment criterion, a
  reduced model with no rigorous error bridge, or a pointwise hypothesis not
  known to be dynamically meaningful.
- Action: benchmark the candidate against nearby literature so novelty and
  hardness are stated honestly.
- Expected output: one proposition-scale target with one precise bottleneck
  theorem and one next execution step.
- Kill condition: if the bottleneck is effectively equivalent to solving the
  original blowup problem, downgrade the result back to obstruction.

### Step 6 - Close with a calibrated tensor verdict

- Depends on: Step 5, or directly on Step 4 if the chain dies there.
- Action: state whether the final outcome is:
  - a genuine NS-specific tensor mechanism with plausible theorem path;
  - a faithful but nonclosing conditional criterion;
  - or a negative diagnosis showing why tensor structure stays informative but
    non-coercive.
- Action: make the verdict explicitly Tao-sensitive and prior-art-sensitive,
  with no claims broader than the audited observables and representations.
- Expected output: either a live tensor route or a sharp tensor-obstruction memo
  ready for final comparison.
- Kill condition: if the claimed mechanism still works unchanged in the averaged
  model or differs from known criteria only cosmetically, close the branch
  negatively.

## Probability Assessment

- Probability this refined chain yields a presentable result: **0.72**
- Most likely presentable result: a calibrated tensor-obstruction memo.
- Less likely presentable result: a live full-stretching control mechanism.
