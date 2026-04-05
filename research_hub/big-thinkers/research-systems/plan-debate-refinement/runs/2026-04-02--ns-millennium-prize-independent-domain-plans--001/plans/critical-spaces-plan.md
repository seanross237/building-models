# Critical Spaces / Compactness-Rigidity / Minimal-Element Plan

## Core Judgment

There is no honest prize-facing compactness-rigidity mainline right now.

The status file closes the generic version of this domain: standard retries in
`L^3`, `\dot H^{1/2}`, `BMO^{-1}`, or equivalent critical host spaces do not
currently produce a Navier-Stokes-specific extraction package, and "assume a
minimal blowup element and hope compactness-rigidity finishes the job" is not a
live program.

The only domain-serious route left in this lens is much narrower:

1. work in one defensible critical space, most likely `L^3`;
2. assume a minimal blowup element exists at the threshold;
3. prove a canonical concentration/extraction theorem that is stable under
critical symmetries, subsequences, and harmless refinement;
4. only then attempt a rigidity contradiction.

If Step 3 cannot be done, then the correct output of this lens is a no-go
theorem explaining why compactness-rigidity cannot currently feed a
prize-facing Navier-Stokes argument.

## Main Theorem Target

### Theorem Target M

Let

`A_c = inf { A : every Leray-Hopf solution with sup_t ||u(t)||_{L^3} <= A is global and smooth }`.

Assume `A_c < infinity` and blowup occurs at the threshold. Then there exists a
symmetry-normalized minimal blowup element `u_c` together with a **canonical
critical concentration tree**

`C(u_c) = { (t_n, x_n, N_n, mu_n) }`

such that:

1. `u_c` is almost periodic modulo scaling and translation in the standard
critical-element sense;
2. the extracted windows are canonical, meaning invariant under admissible
relabeling, stable under compactness limits, and unchanged by harmless
refinement of the concentration windows;
3. at least one persistent branch of `C(u_c)` carries a fixed positive fraction
of the critical `L^3` mass and of the localized nonlinear flux on every bad
time sequence;
4. every such persistent branch obeys a dichotomy:
   - either it asymptotically enters a known rigidity class
     (self-similar / Type I-like / locally perturbative),
   - or it exhibits forced multi-branch splitting incompatible with minimality.

The real point is not the final contradiction in one jump. The point is to
replace the current non-canonical "there is some concentration profile" with a
theorem-quality object that can actually support rigidity.

## Fallback Theorem Target

### Theorem Target F

Prove a **critical-space no-canonical-finite-reduction theorem**:

for an `L^3`-minimal blowup element, no extraction rule based on finitely many
profiles, finitely many packets, or finitely many concentration windows can be
simultaneously:

1. invariant under the critical symmetries;
2. stable under profile decomposition and subsequence passage;
3. robust under harmless refinement;
4. rich enough to support a finite-dimensional rigidity contradiction.

This is a bounded no-go result, not a prize route. But it would be genuine
progress because it would explain, in theorem form, why the compactness-rigidity
program keeps stalling at the object-definition stage.

## Route Structure

### Route 1: Canonical extraction in `L^3` for a hypothetical minimal element

This is the only route in this lens worth promoting.

The problem is not existence of a minimal element in the abstract; the problem
is producing a canonical descriptor of its concentration geometry that survives
all the usual compactness ambiguities. Without that, rigidity has nothing solid
to act on.

### Route 2: Rigidity after extraction, not before

If Route 1 works, the next move is not a generic host-space contradiction. It
is a sharply localized rigidity statement for the extracted persistent branch:
single-branch concentration must either collapse into a known rigid regime or
split in a way that contradicts minimality.

This route is secondary because it depends completely on Route 1.

### Route 3: No-go theorem if canonical extraction fails

If repeated attempts at Route 1 fail for structural reasons, stop pretending a
compactness-rigidity proof is nearby and prove the obstruction. In this lens,
an honest obstruction theorem is preferable to another soft restart.

## First 2-3 Concrete Theorem Steps

### Step 1: Freeze the threshold setting in one critical space and rule out fake alternatives

Work only in `L^3`. Do not split effort across `L^3`, `\dot H^{1/2}`,
`BMO^{-1}`, and related spaces.

Prove or restate in the exact form needed:

1. threshold existence and symmetry-normalized minimal blowup element;
2. quantitative almost periodicity modulo translation and scaling;
3. a no-vanishing / no-low-frequency-evacuation / no-high-frequency-evacuation
package along bad times strong enough to force genuine one-scale concentration
rather than an arbitrary profile cloud.

If even this cannot be organized cleanly in `L^3`, the route should already be
downgraded.

### Step 2: Prove a canonical concentration-window extraction lemma

This is the load-bearing step.

Construct, from `u_c` alone, a sequence of bad-time parabolic windows
`Q_n = Q(t_n, x_n, N_n^{-1})` and a branch-selection rule such that:

1. the selected windows maximize a critical concentration functional;
2. ties are resolved intrinsically, not by coordinates or ad hoc packet labels;
3. the rule commutes with subsequence limits and profile decomposition;
4. the extracted branch carries a fixed positive proportion of the local
critical mass/flux.

If no intrinsic tie-breaker exists, that is already evidence for the fallback
no-go theorem.

### Step 3: Turn the canonical branch into a rigidity dichotomy

For the extracted branch, prove a theorem of the form:

either

1. the branch becomes asymptotically self-similar / Type I-like / perturbative
in a quantified way that places it inside an existing rigidity class,

or

2. the branch must split into two asymptotically disjoint critical subbranches,
which contradicts minimality of `u_c`.

This is the first point where a real contradiction could appear. Before this
step, the program is still only infrastructure.

## Hard Stop Conditions

Stop the mainline immediately if any of the following happens:

1. the extraction rule depends on non-intrinsic choices of representatives,
subsequence, packetization, or coordinate frame;
2. the only surviving descriptor is an infinite soft profile decomposition with
no canonical persistent branch;
3. the rigidity step requires importing exactly the sort of packet ledger or
desired-channel annotation that the status file already says is non-canonical;
4. the contradiction reduces to generic critical-space folklore with no
Navier-Stokes-specific one-sided gain;
5. the route quietly reopens closed host-space retries under new notation.

If any of these occurs, switch from "proof route" to "obstruction theorem"
mode.

## What Counts as Genuine Progress

The following would count as real progress in this lens:

1. a theorem-quality canonical extraction lemma for `L^3` minimal elements;
2. a proof that every persistent concentration branch satisfies a sharp
single-branch versus splitting dichotomy;
3. a rigidity theorem excluding one side of that dichotomy by accepted PDE
arguments, not by speculative packet heuristics;
4. failing that, a no-go theorem proving that no finite canonical reduction of
the critical element can survive the symmetry/compactness/refinement demands.

By contrast, another abstract profile decomposition, another host-space survey,
or another "assume minimality and hope" note is not progress.

## What I Refuse To Spend Time On Because The Status File Closes It

I will not spend time on:

1. generic restarts of compactness-rigidity in `L^3`, `\dot H^{1/2}`,
`BMO^{-1}`, or equivalent critical spaces without a new extraction object;
2. attempts to rescue the route by exact reformulation alone;
3. epsilon-regularity, De Giorgi, pressure-improvement, or `H^1` pressure
patches glued onto a critical-space argument;
4. packet or hypergraph objects that require post hoc desired-channel
annotation, since this lens only helps if the extracted object is canonical;
5. vague claims that a minimal element "should look like Tao's mechanism"
without a theorem-level extraction rule.

## Bottom Line

For this domain lens, the honest plan is not "prove regularity from critical
spaces." It is:

1. either prove a canonical `L^3` minimal-element concentration theorem that
gives rigidity something concrete to attack,
2. or prove that no such finite canonical reduction exists and formally park
compactness-rigidity as a prize route for now.

Until Step 2 is achieved, this domain should be treated as a bounded
prerequisite/no-go campaign, not as an active prize-facing mainline.
