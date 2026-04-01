# Attack on Chain 01 - Local Harmonic Pressure Localization

## Bottom Line

This chain is pointed at the right leftover object: the prior `vasseur-pressure` mission really did isolate the far-field pressure as the only surviving pressure-side obstruction. That is the strongest thing about it.

But the chain is still too optimistic and too loose. It mostly formalizes a future-work note that already existed in the prior mission rather than introducing a new discriminating lemma, model calculation, or early Tao-compatible kill test. The main risk is that it spends budget renorming a harmonic function whose size is still dictated by the same remote shell energy `E_0`.

The prior mission already had the key formula:

`I_p^far <= C_far 2^{12k/5} U_k^{6/5}`, with `C_far ~ ||u||_{L^2}^2 / r_k^3`.

So the issue is not the `U_k` exponent anymore. The issue is coefficient smallness. Any successful version of this chain has to make `C_far` genuinely better than a fixed energy-class constant. Harmonic smoothness alone does not obviously do that.

## Step 1 - Reconstruct the exact obstruction

This step is partly redundant as written. The exact obstruction has already been reconstructed in the prior mission: local pressure closes, far-field pressure is harmonic on `Q_k`, and the bad point is that its coefficient is a fixed constant rather than something that shrinks with `U_k`. If Step 1 just rewrites that in a cleaner memo, it is bookkeeping, not progress.

The hidden assumption is that the relevant quantity is some local oscillation norm of `p_far`, not the absolute size entering the pressure pairing. That is not automatic. If constants, affine modes, or low-order harmonic modes are already killed by the test structure, Step 1 must say exactly which modes survive in the error term. If they are not killed, then replacing `L^\infty` by an oscillation norm is cosmetic.

The kill condition is also underpowered. "If every local harmonic candidate collapses to the same fixed constant" is too vague because it does not say what counts as a candidate or how one proves collapse. A sharper Step 1 would demand an explicit countermodel: take a remote shell source with admissible energy, compute the induced harmonic field on the inner cylinder, and check whether the local norm is still comparable to shell energy. If yes, most of the chain dies immediately.

## Step 2 - Test truly local harmonic norms

This is the weakest step. It reads like norm-shopping: local `H^1`, local `BMO`, Campanato, Carleson, annular energy, Harnack, mean-value, interior gradient. That is too many analytic wrappers around the same object without a reason to expect any one of them to insert new smallness.

The core mathematical problem is simple: harmonicity gives interior regularity from boundary control, but it does not create boundary control. If the boundary data seen by the inner cylinder is already `O(E_0)`, then mean-value, interior-gradient, and Campanato estimates just propagate `O(E_0)` in smoother language. Without a moment cancellation or sign cancellation in the remote source `u_i u_j`, there is no reason for locality alone to beat the shell-energy bound.

Harnack is especially suspect here. `p_far` is not positive, so a raw Harnack principle is not the right object. The usable quantity would be oscillation, derivative decay, or harmonic polynomial approximation. The chain does not say which one actually enters the pressure error term.

The annular-energy idea also risks quietly reintroducing the already-killed localization problem. If the plan starts partitioning the outer region into shells with cutoffs, it is walking back toward the Bogovskii/cutoff minefield that the prior mission explicitly ruled out. The chain never explains how it will harvest annular information without paying localization costs.

There is also no explicit falsification test. Before running through five function spaces, the chain should force one toy computation: a remote annulus carrying coherent quadratic source can induce a nontrivial harmonic polynomial inside the local cylinder. If the local norm of that polynomial is still proportional to the outer-shell energy, then most candidate norms are dead on arrival.

## Step 3 - Convert the best surviving estimate into a non-De-Giorgi criterion

This step claims to stay outside De Giorgi, but its outputs are "conditional epsilon-regularity," "local energy improvement," or "annular-flux control." That is dangerously close to rebuilding the same recursive architecture under different labels. If the only thing produced is another pressure estimate that still has to be inserted into a threshold/iteration scheme, then the chain has not really escaped the known barrier.

More importantly, the quantitative success condition is missing. Since the prior formula already gives a superlinear `U_k^{6/5}` once `C_far` is small, Step 3 is only meaningful if Step 2 produced a bound that makes `C_far` small from admissible NS data. Anything weaker is irrelevant. A proposition of the form "some local norm of `p_far` is controlled by annular energy" does not matter unless that annular energy is summable, decaying, or otherwise tied to the critical obstruction.

This is also where the chain quietly assumes that a harmonic estimate can be "non-De-Giorgi" while still proving something Tao-relevant. That is not convincing. If the gain uses only elliptic regularity of a harmonic tail, it is almost certainly available in averaged NS too.

## Step 4 - Apply the Tao filter and close the chain

The Tao filter is placed too late. That is a structural mistake.

Everything in Step 2 is generic elliptic/harmonic analysis: local `H^1`, `BMO`, Campanato, Carleson, mean-value, interior gradient, Harnack-type decay. Tao's averaged model is designed to survive exactly this level of analysis. If a candidate route does not use an NS-specific identity before the norm-testing phase, it should be presumed guilty immediately, not checked at the end.

The comparison criterion is also too weak. "Does the argument use exact NS pressure structure or only generic elliptic harmonicity?" is the right question, but the chain gives no mechanism for answering it. A real filter would force the route to identify the specific NS-only ingredient up front, for example some exploitable fact about `\partial_i \partial_j p = R_i R_j(u_i u_j)` that is not preserved by Tao's averaging. If the route cannot name that ingredient by the end of Step 1, it is probably dead already.

## Structural Weaknesses of the Whole Chain

The claimed novelty is overstated. This is not a fresh route discovered from scratch; it is the explicit "lead for future work" already recorded in the prior `vasseur-pressure` mission. That is fine as a follow-up, but it weakens the claim that the chain is "meaningfully different." It is meaningfully narrower, not clearly meaningfully newer.

The chain also sits too close to the mission's forbidden framing. The mission context explicitly says "Do NOT approach this as find a better bound for the pressure term." But Chain 01 is, in substance, exactly a search for a better bound on the far-field pressure coefficient, with harmonicity as the hoped-for lever. Saying "outside De Giorgi" does not fix that by itself.

There is a hidden structural bias toward the conclusion that the one surviving pressure loophole must be the next thing to try. That inference is too strong. "Far-field pressure is the sole obstruction" was proved inside the pressure-based architecture. It does not follow that the best beyond-De-Giorgi attack should continue orbiting pressure.

The kill conditions are not calibrated tightly enough. "Every natural local norm" is open-ended and invites budget drift. A ruthless version of this chain would precommit to a short list of norms, a model-shell falsification test, and an NS-specificity requirement before allowing any step to continue.

## Fair Assessment

The chain is not nonsense. It is a legitimate cleanup target because the prior mission left this harmonic-locality loophole explicitly open, and a solid negative result would be genuinely useful.

But as a planning object it is still too soft. It needs an earlier Tao filter, an explicit shell-source countermodel, and a quantitative definition of success tied to the bad coefficient `C_far`, not just "stronger than `O(E_0)`." Without those upgrades, the most likely outcome is a polished restatement of why harmonicity gives smoothness but not the kind of NS-specific smallness the problem actually needs.
