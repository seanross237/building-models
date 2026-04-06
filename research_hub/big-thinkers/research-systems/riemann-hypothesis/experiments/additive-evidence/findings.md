# Additive Evidence for Zero-Free Regions as an Optimal Statistical Detection Problem

**Date:** 2026-04-06
**Status:** Complete
**Verdict:** The non-trivial version of the proposal is a restricted mollifier
optimization problem; the pointwise version is structurally infeasible for any
convergent per-prime envelope. Either way, no new zero-free region is obtained.

## Executive Summary

The "additive evidence" proposal asks: can we choose per-prime weights
`w_p(sigma, t)`, bounded by an absolutely convergent envelope
`B_p = C (log p)^A / p^{1+eps}`, such that the partial sum
`E_sigma(t) = sum_p w_p(sigma, t)` certifies `zeta(sigma+it) != 0` for all `t`?

We resolved this question in three steps:

1. **Sign correction.** As originally stated the proposal said
   "`E_sigma(t) > 0 ==> zeta(sigma+it) != 0`". Read literally that requires
   `E_sigma(t) <= log|zeta(sigma+it)|`, which forces `|zeta| >= e^{E_sigma(t)} > 1`,
   a condition that fails routinely on the critical strip. The right framing is
   a finite upper bound on `-log|zeta|`:
        `E_sigma(t) >= -log|zeta(sigma+it)|`  =>  `|zeta(sigma+it)| >= exp(-E_sigma(t)) > 0`.
   The objective then becomes `R(sigma) = inf_w sup_t E_sigma(t)` subject to the
   envelope constraint and the pointwise domination above.

2. **LP numerics (sign-corrected).** Using scipy linprog we solved the
   minimax LP on a grid of 71 t-values (including the first 10 zeta-zero
   imaginary parts) for primes `p <= 100` with envelope `1/p^{1+eps}`.
   - At `sigma >= 0.8` the LP is feasible; the optimal value is exactly
     `max_j (-log|zeta(sigma+i t_j)|)`. The prime structure plays no role.
   - At `sigma = 0.55, 0.60, 0.70` the LP is **infeasible**. The envelope
     budget `sum_p B_p` is 1.64 (and 2.74 for all primes at `eps=0.05`),
     while the target `-log|zeta(0.55 + 14.13 i)|` is already 3.25 and grows
     to 10.82 just `10^-6` from the critical line. Expanding the prime set
     to `p <= 5000` only raises the budget to 2.08. No convergent envelope
     can close the gap.

3. **Novelty verdict.** The pointwise minimax LP decouples across t
   (variables `w_{p,j}` are unconstrained across `j`), so it is structurally
   trivial: `tau_opt = max(max_j target_j, -sum_p B_p)`. To make the LP
   non-trivial one must couple the weights across t-values, and the natural
   coupling is `w_p(t) = Re(a_p p^{-sigma-it})` with a fixed coefficient vector
   `{a_p}` — which is exactly a prime-supported mollifier. The non-trivial
   minimax is therefore the classical mollifier optimization problem
   (Selberg, Levinson, Conrey, Conrey-Iwaniec-Soundararajan,
   Bui-Conrey-Young, Radziwill-Soundararajan), solved only in a mean-square
   (averaged) sense and known to yield proportion-of-zeros results, not a
   new zero-free region.

**Bottom line.** The proposal is not new. Its trivial (pointwise) version is
infeasible for convergent envelopes; its non-trivial version is mollifier
optimization, which has been the primary optimization framework in zero-density
theory for fifty years and does not give deterministic zero-free regions
beyond Vinogradov-Korobov.

## 1. Setup (Sign-Corrected)

### 1.1 The correct certification

For `sigma > 1`,
```
-log|zeta(s)| = -Re log zeta(s) = -sum_p sum_{k>=1} cos(k t log p)/(k p^{k sigma}).
```
Near a would-be zero of `zeta`, `-log|zeta|` is large and positive; away from
zeros it is bounded. Ruling out zeros requires an **upper bound** on
`-log|zeta|`, not a lower bound. The proposal as originally stated
("`E_sigma(t) > 0 => zeta != 0`") asked for the wrong inequality direction;
literally applied, it would require `|zeta| > 1` pointwise, which is false
on any vertical line `Re(s) <= 1`.

The sign-corrected proposal is:
```
Find w_p(sigma, t) with |w_p| <= B_p = C (log p)^A / p^{1+eps}
such that E_sigma(t) := sum_p w_p(sigma,t) >= -log|zeta(sigma+it)| for all t.
Minimize R(sigma) := sup_t E_sigma(t).
```
Any finite `R(sigma)` implies the zero-free region `|zeta(sigma+it)| >= exp(-R(sigma))` on that vertical line.

### 1.2 Why this could, a priori, be strong

A convergent-at-the-line envelope (`sum_p B_p < infty`) would give a finite
absolute bound on `R(sigma)`, which would be stronger than any known zero-free
region. That is precisely why the proposal is structurally appealing. The
question is whether any such `w_p` can actually dominate `-log|zeta|`
pointwise.

## 2. Numerical Minimax LP (Corrected Signs)

### 2.1 Setup

- Primes `p <= P` for `P in {100, 200, 500, 1000, 2000, 5000}`.
- Envelope `B_p = C (log p)^A / p^{1+eps}` for `eps in {0.001, ..., 0.5}` and
  `A in {0, 1, 2, 3}`.
- `t`-grid: 61 equi-spaced points in `[0.5, 60]` plus the first 10 Riemann
  zeros' imaginary parts (where `-log|zeta|` spikes).
- Target: `target_j = -log|zeta(sigma + i t_j)|` computed to 30 digits with
  `mpmath`.
- LP variables: per-prime-per-t weights `w_{p,j}` plus scalar
  `tau = sup_j sum_p w_{p,j}`.
- Constraints: `|w_{p,j}| <= B_p`, `sum_p w_{p,j} >= target_j`,
  `sum_p w_{p,j} <= tau`.
- Objective: minimize `tau`.

### 2.2 Envelope budget `sum_p B_p` (for reference)

```
  eps       P=100       P=1000      P=10000     P=Infinity (prime zeta at 1+eps)
 0.001      1.7995      2.1925      2.4752      6.5934
 0.010      1.7696      2.1430      2.4061      4.3027
 0.050      1.6447      1.9426      2.1337      2.7436
 0.100      1.5053      1.7301      1.8584      2.1088
 0.200      1.2726      1.4010      1.4590      1.5198
 0.500      0.8177      0.8422      0.8477      0.8496
```
The limiting budget for `eps -> 0` is `+infty`, but extremely slowly
(`P(1+eps) ~ log(1/eps)`). Practically the budget is `O(1)` for any
`eps >> 0`, and even `eps = 0.001` only yields 6.59.

### 2.3 Primary LP sweep (`P <= 100`, `eps = 0.05`, `sum_p B_p = 1.6447`)

```
sigma = 0.55:  max target = 3.2477 (at t=14.13)   LP INFEASIBLE
                total slack = 10.88, max slack = 1.60, 11/71 t-points infeasible

sigma = 0.60:  max target = 2.5745 (at t=14.13)   LP INFEASIBLE
                total slack =  4.14, max slack = 0.93, 11/71 t-points infeasible

sigma = 0.70:  max target = 1.9210 (at t=14.13)   LP INFEASIBLE
                total slack =  0.28, max slack = 0.28,  1/71 t-points infeasible

sigma = 0.80:  max target = 1.5546                LP FEASIBLE, tau = 1.5546
sigma = 1.00:  max target = 1.1202                LP FEASIBLE, tau = 1.1202
sigma = 1.05:  max target = 1.0436                LP FEASIBLE, tau = 1.0436
```

**Infeasibility is structural, not a discretization artifact.** The max of
`-log|zeta|` over the grid exceeds the *sum of all envelope upper bounds*,
so no choice of `|w_p| <= B_p` can meet the domination constraint at the
peak t.

### 2.4 Growing the prime set does not help

At `sigma = 0.55`, `t = 14.1347`, target = 3.2477:
```
Pmax        #p     budget    target    result    budget gap
100         25     1.6447    3.2477    INFEAS    1.6029
200         46     1.7589    3.2477    INFEAS    1.4887
500         95     1.8696    3.2477    INFEAS    1.3781
1000       168     1.9426    3.2477    INFEAS    1.3050
2000       303     2.0083    3.2477    INFEAS    1.2393
5000       669     2.0837    3.2477    INFEAS    1.1640
```
The budget converges to `primezeta(1.05) = 2.7436`, which is **still less
than the target**. So even the full infinite-prime envelope at `eps = 0.05`
is insufficient. Nor can we rescue by shrinking `eps`:
```
 eps     budget  target
0.500    0.818   3.248   INFEAS
0.200    1.273   3.248   INFEAS
0.100    1.505   3.248   INFEAS
0.050    1.645   3.248   INFEAS
0.010    1.770   3.248   INFEAS
0.001    1.800   3.248   INFEAS
```
and the `eps -> 0` limit is `primezeta(1+eps) ~ log(1/eps) + C`, which only
reaches 3.25 for `eps` around `e^-3 ~ 0.05`. Under `P = 100` we cannot get
there. With all primes, `eps = 0.001` gives budget 6.59, which finally exceeds
3.25 — but fails the instant we move `sigma` one notch closer to `1/2`: at
`sigma = 0.501`, the target is 7.14; at `sigma = 0.5001`, 9.41;
at `sigma = 0.500001`, 10.82. The target grows without bound while the
budget saturates at a finite (slow-growing) number.

### 2.5 (log p)^A envelope

Increasing `A` does raise the budget, but the resulting envelope is no longer
`o(p^{-1})`:
```
A=0  budget 1.65   INFEAS (target 3.25)
A=1  budget 2.96   INFEAS
A=2  budget 7.48   FEAS,   tau = 3.25 = target
A=3  budget 23.1   FEAS,   tau = 3.25 = target
```
Once feasible, `tau` is literally the target: the LP has enough slack to
meet the largest target value but nothing further. It does not shave off any
buffer.

### 2.6 The LP is structurally trivial (decoupling lemma)

**Claim.** For any envelope `B_p >= 0`, any finite primes set, and any t-grid,
the sign-corrected LP has optimal value
```
tau* = max( max_j target_j,  -sum_p B_p )
```
and this value depends on the envelope only through its total mass `sum_p B_p`.

**Proof.** Variables `w_{p,j}` for different `j` share no constraints: the
envelope is per-prime box constraints, not per-prime sum constraints across t.
Hence for each `j` the sub-problem is
```
min_{|w_{p,j}|<=B_p} sum_p w_{p,j}   s.t.   sum_p w_{p,j} >= target_j.
```
The unconstrained minimum is `-sum_p B_p` (all weights at lower bound);
the constrained minimum is `max(target_j, -sum_p B_p)`. Feasibility requires
`sum_p B_p >= target_j`, i.e. `target_j <= sum_p B_p`. Taking the sup over `j`
gives the claim.

**Verified numerically (lp_structural_check.py):** at `sigma = 0.8`, the LP
solution has `tau = 1.5546 = max target`. Reshuffling `B_p` across primes,
or replacing with a random Dirichlet partition of the same total mass, gives
identical `tau`. The per-prime distribution of `B_p` is **irrelevant**.

### 2.7 What this LP reveals

1. The sign-corrected LP has no interesting optimization structure: each t is
   independent, and "solving" it is just reading off `max_j target_j`. It
   gives no new information about `-log|zeta|`.
2. Feasibility is controlled purely by whether `sum_p B_p` (a prime-zeta-like
   constant) exceeds the pointwise max of `-log|zeta|` on the vertical line.
   For any convergent envelope (in particular, any `B_p = O(p^{-1-eps})`),
   the total mass is finite and hence bounded — while
   `sup_t -log|zeta(sigma+it)|` is unbounded as `sigma -> 1/2` (and in
   fact grows as large as the smallest gap to a zero allows at any fixed
   `sigma > 1/2`).
3. Therefore no absolutely-convergent per-prime envelope can produce a
   pointwise certificate `E_sigma(t) >= -log|zeta(sigma+it)|` for all `t` on
   any vertical line `sigma > 1/2`.

## 3. Why the LP Is Trivial: The Missing Coupling

The decoupling lemma above says the pointwise LP is uninteresting because the
weights `w_{p,j}` can be chosen independently at each `t_j`. Any **non-trivial**
version of the proposal must couple the weights across `t`. The natural
couplings are:

- `w_p(t) = Re(a_p p^{-sigma-it})` for a fixed coefficient vector `a_p`
  (one coefficient per prime, not per `(p,t)` pair). This reduces to
  choosing a short prime-supported Dirichlet polynomial
  `M(s) = sum_{p <= P} a_p p^{-s}`.
- `w_p(t) = Re( (sum_{k<=K} a_{p,k} p^{-k(sigma+it)} ) )` — equivalently, a
  short Dirichlet polynomial `M(s) = sum_{n <= P^K, n squarefree-prime-power} a_n n^{-s}`
  with coefficients supported on prime powers.

Either way, the "additive evidence with convergent envelope" proposal becomes:
optimize a Dirichlet polynomial (mollifier) so that its real part on the line
`sigma + it` dominates `-log|zeta(sigma+it)|`. This is **precisely** a
prime-supported mollifier optimization problem.

## 4. Connection to Mollifiers (Investigation 1)

### 4.1 What mollifiers optimize

The standard mollifier setup (Levinson 1974; Conrey 1989; Bui-Conrey-Young 2011;
Conrey-Iwaniec-Soundararajan 2012; Pratt-Robles-Zaharescu-Zeindler 2020;
Radziwill-Soundararajan ongoing) introduces a Dirichlet polynomial
`M(s) = sum_{n <= N} mu(n) P(log(N/n)/log N) n^{-s}` and computes
asymptotics for the mean square `int_T^{2T} |zeta(s) M(s)|^2 dt` on vertical
lines or on the critical line. The aim is to obtain upper bounds on mean
squares that imply *either* lower bounds on the proportion of zeros on the
line (Levinson method) *or* mean-value estimates that feed into zero-density
theorems (Halasz-Montgomery).

**No mollifier method is known to produce a pointwise deterministic
zero-free region strictly larger than Vinogradov-Korobov.** The best zero-free
regions (VK, plus its refinements by Heath-Brown, Ford, Kulas, etc.) come
from a completely different technique: bounding exponential sums
`sum_{n <= N} n^{-it}` via Weyl/Vinogradov differencing and Van der Corput.

### 4.2 Why mollifiers cannot yield a pointwise certificate

The mean-square input to mollifier methods is
```
(1/T) int_T^{2T} |zeta(sigma+it)|^2 |M(sigma+it)|^2 dt
```
which is averaged in `t`. Averaging in `t` erases the spikes of
`-log|zeta|` near zeros. One cannot unaverage: Bohr-Jessen theory
(Jessen-Wintner 1935, Laurincikas 1996) shows `log|zeta(sigma+it)|` is
almost-periodic with a continuous distribution function for `sigma > 1/2`,
and its pointwise supremum on long intervals grows like
`(log log T)^{1/2}` (Soundararajan 2009; Bondarenko-Seip 2018). No finite
mollifier controls that supremum pointwise.

### 4.3 Explicit match between the LP and a mollifier objective

If one parametrizes `w_p(t) = Re(a_p p^{-sigma-it})` with real `a_p`, then
```
sum_p w_p(t) = Re ( sum_p a_p p^{-sigma-it} ) = Re M(sigma+it)
```
for the prime-supported mollifier `M(s) = sum_p a_p p^{-s}`. The envelope
constraint `|w_p(t)| <= B_p` pointwise becomes `|a_p| p^{-sigma} <= B_p`,
i.e. `|a_p| <= B_p p^{sigma}`. For `B_p = p^{-1-eps}` and `sigma = 1/2` this
is `|a_p| <= p^{-1/2-eps}`, which is **much faster decay than the standard
mollifier coefficient size `|a_p| ~ 1`**. Standard mollifiers use coefficients
of size `|mu(p)| = 1`, not shrinking with `p`.

So under the convergent-envelope hypothesis, the additive proposal corresponds
to a **highly restricted** sub-class of mollifiers, strictly weaker than the
mollifiers already in the literature. The problem is not that mollifiers are
insufficient for the task — it's that our proposed class is even more
constrained.

### 4.4 Novelty verdict for Investigation 1

**The proposal is a proper sub-class of the existing mollifier optimization
framework. Known mollifiers already subsume and dominate it.**
Specifically:
- Levinson (1974), Conrey (1989) mollifiers give proportion-of-zeros on
  the critical line.
- Conrey-Iwaniec-Soundararajan (2012) asymptotic large sieve gives optimal
  mean-square control.
- Guth-Maynard (2024) large-value estimates for Dirichlet polynomials
  improve zero-density theorems, but still via mean-square, not pointwise.

None of these produce a zero-free region better than VK, and the
more-restricted additive-evidence class cannot either.

## 5. Neyman-Pearson Formulation (Investigation 2)

### 5.1 Null and alternative

- **Null model `H_0`**: there is no zero at `sigma + i t_0`. Under Bohr-Jessen
  theory, for `sigma > 1/2`, `log|zeta(sigma+it)|` as a function of `t` is
  a real-analytic almost-periodic function with a continuous value
  distribution `F_sigma`, which is absolutely continuous w.r.t. Lebesgue
  measure on `R` (Jessen-Wintner 1935). In particular `{t : log|zeta| < -M}`
  has Lebesgue measure decaying faster than any polynomial in `1/M`.

- **Alternative model `H_1(t_0)`**: there is a zero at `sigma + i t_0`. Then
  `log|zeta(sigma+it)| -> -infty` as `t -> t_0`, and at that one point
  `-log|zeta| = +infty`.

### 5.2 Log-likelihood ratio is degenerate

`H_1(t_0)` differs from `H_0` only at a single point `t_0` (a Lebesgue null
set). As measures on the function space `C(R)` (or more precisely on a
suitable subspace of almost-periodic functions), `H_0` and `H_1(t_0)` are
**mutually singular**: `H_0` gives measure one to "log|zeta| is everywhere
finite", while `H_1(t_0)` gives measure one to "log|zeta| is `-infty` at
`t_0`". The log-likelihood ratio
```
dH_1(t_0)/dH_0
```
is therefore **not an `L^1` function** — it is a singular measure (Dirac
density times `+infty`), and no detector based on an `L^1`-convergent sum
`sum_p f_p(t)` can separate them.

### 5.3 Consequence for any convergent-envelope detector

Any additive detector with absolutely convergent envelope is a continuous
function of `t` on every vertical line `sigma > 1/2`. A continuous detector
cannot resolve a single-point singularity of the alternative — at best it
resolves the neighborhood `|t - t_0| < delta` by integrating against a smooth
kernel, which is the mollifier/averaging approach again.

### 5.4 Where the singularity is hiding

The "information about a zero at `t_0`" is carried by the **divergent tail**
of the prime sum `sum_p p^{-sigma-it_0}`, whose partial sums oscillate but
do not converge absolutely for `sigma <= 1`. Absolute convergence — the
hypothesis of the additive-evidence proposal — **exactly kills this
information**, since it forces the detector to be continuous in `t`.
In detection-theory terms, passing to the absolutely-convergent regime is
equivalent to a band-limited / low-pass filter applied to `log|zeta|`, and
zeros live in the high-frequency tail.

### 5.5 Novelty verdict for Investigation 2

**The Neyman-Pearson formulation is mathematically well-defined but confirms
the previous (convolution-invariant) finding:** the distinction "zero at `t_0`
vs no zero at `t_0`" is a singular distinction between probability measures,
so any detector built on a convergent `L^1` sum of per-prime statistics is
measuring the wrong object. This is the same probabilistic-to-deterministic
gap observed in the convolution-invariant experiment, now cast in hypothesis-
testing language.

## 6. Minimax Optimization (Investigation 3)

### 6.1 Numerical minimax

See section 2. Infeasible for `sigma <= 0.70`, trivially feasible for
`sigma >= 0.80` with `tau = max target`, with zero dependence on the
per-prime distribution of the envelope.

### 6.2 Coupled (mollifier) minimax

When the variables are coupled via `w_p(t) = Re(a_p p^{-sigma-it})`, the
minimax becomes
```
inf_a  sup_t  Re ( sum_p a_p p^{-sigma-it} )   s.t.   |a_p| p^{-sigma} <= B_p
                                                    and   domination constraint.
```
This problem has no closed form but is equivalent to well-studied Dirichlet
polynomial sup-norm minimization subject to a pointwise domination. The
Beurling-Selberg extremal function theory (Selberg 1940s unpublished;
Vaaler 1985; Graham-Vaaler 1981; Carneiro-Vaaler 2010) provides the sharp
bounds for problems of this form, and they are **always** of the same order
as classical zero-density and zero-detection estimates — never stronger.

### 6.3 Novelty verdict for Investigation 3

**The minimax LP does not outperform its existing analytic solutions.**
The pointwise LP is trivial (max of target). The coupled LP reduces to a
Beurling-Selberg-type extremal problem whose solutions are already optimized
in the literature.

## 7. Comparison to Vinogradov-Korobov (Investigation 4)

### 7.1 The existing deterministic zero-free region

```
sigma > 1 - c / ( (log|t|)^{2/3} (log log|t|)^{1/3} )      (VK, 1958)
```
At `t ~ 14` this gives `sigma > 1 - c/(log 14)^{2/3} ~ 1 - 0.5c`. With the
best known `c ~ 0.0521` (Ford 2002 explicit form) this is `sigma > 0.974`.

### 7.2 What the LP achieves

In section 2.3 the LP is feasible at `sigma = 0.8`, with `tau = 1.5546`, i.e.
`|zeta(0.8 + it)| >= 0.211` on the grid. For `sigma = 0.7` the LP is
**infeasible** (it cannot certify `|zeta(0.7+it)| > 0` at `t = 14.13`), and
the same is true for `sigma = 0.6, 0.55`.

So the additive-evidence LP does not reach as far as VK in any region: VK
gives an (admittedly only effective for `|t| >= 3`) zero-free certification
for `sigma > 0.974` at `t = 14`, whereas the LP can at best confirm
`|zeta| > 0.21` at `sigma = 0.8`, `t = 14` — which is strictly weaker because
(a) it requires the numerical value of `zeta` in advance, and (b) it doesn't
extend to `sigma in (0.5, 0.8)`.

### 7.3 Novelty verdict for Investigation 4

**The LP produces a strictly weaker result than VK**, and in the critical
regime `sigma < 0.8` it produces no zero-free statement at all. The proposal
offers no improvement.

## 8. Probabilistic → Deterministic Gap (Investigation 5)

### 8.1 The t-average picture

```
Mean of -log|zeta(sigma+it)| over t in [10, 200]:
  sigma=0.55: mean=-0.0002, min=-1.71, max= 2.77, std=0.95
  sigma=0.60: mean=-0.0027, min=-1.63, max= 2.11, std=0.85
  sigma=0.70: mean=-0.0034, min=-1.47, max= 1.71, std=0.72
  sigma=0.80: mean=-0.0033, min=-1.33, max= 1.45, std=0.62
  sigma=1.00: mean=-0.0027, min=-1.09, max= 1.07, std=0.49
```
The t-average of `-log|zeta|` is essentially 0 on every vertical line
`sigma > 1/2` (Bohr-Jessen centering). **The envelope budget 1.64 easily
dominates the mean** at every `sigma`. So averaged estimates are trivial.

### 8.2 The pointwise picture

But the pointwise max grows with the t-window, and as `sigma -> 1/2` it
grows without bound near each Riemann zero. Concretely at `t = 14.1347`:
```
sigma    -log|zeta|
1.00     1.12
0.80     1.55
0.60     2.57
0.55     3.25
0.51     4.84
0.501    7.14
0.5001   9.41
0.50001 10.75
```
The value diverges logarithmically in the distance to the zero, exactly as
`-log|s - zero|` would. Any bounded budget loses.

### 8.3 Novelty verdict for Investigation 5

**Optimization of bounded prime weights does NOT upgrade the averaged
estimate to a pointwise one.** This is the same probabilistic-to-deterministic
gap identified by the convolution-invariant experiment (`promising-findings.md`
entry from Wave 6) and by every prior analytic approach to RH through
concentration-of-measure. The numerical experiment gives the clearest possible
quantification: the pointwise max exceeds the averaged mean by several orders
of magnitude near any zero, and the gap is exactly the `-log|s-rho|`
singularity at the zero.

## 9. Halasz-Montgomery Connection (Investigation 6)

### 9.1 What HM optimizes

Halasz-Montgomery method (Halasz 1968, Montgomery 1971; used in
Iwaniec-Kowalski, *Analytic Number Theory*, ch. 9) bounds the number of
"large values" of a Dirichlet polynomial:
```
N(V; T) = #{ t in [-T, T] : |sum_{n<=N} a_n n^{-it}| >= V }.
```
For a_n normalized to `||a||_2 = 1`, HM gives
`N(V; T) << V^{-2} (N + T log N)`. This is the foundation of zero-density
theorems. The optimization is *over the set of large-value points*, not over
the coefficients.

### 9.2 Relation to additive evidence

The additive-evidence LP optimizes the coefficients (prime weights) to produce
a lower envelope for `-log|zeta|`, which is a **dual** problem to
large-value estimation. Duality here means: HM gives an upper bound on
`|sum a_n n^{-it}|` of the form `<< V`, and asks how often it exceeds `V`;
additive evidence asks for a *lower* bound `sum_p w_p(t) >= -log|zeta|`
pointwise. But by log-conjugation the two are the same object: a lower
bound on `-log|zeta|` (or equivalently a lower bound on `log|zeta|^{-1}`)
is an upper bound on `|zeta|`, which is in the same functional class as
Dirichlet polynomial large-value bounds.

### 9.3 Guth-Maynard (2024)

The Guth-Maynard large-value estimate (arXiv 2405.20552) gives the first
improvement on Montgomery's 1971 bound in 50 years. It directly improves
zero-density theorems for `zeta`. Importantly: Guth-Maynard is still an
**averaged** (mean-square over `t`) estimate, not pointwise. It improves
the constants in `N(sigma, T)` but does not yield a new deterministic
zero-free region. In particular it does **not** produce `sum_p w_p(t) >=
-log|zeta(sigma+it)|` pointwise for any `sigma < 1`.

### 9.4 Novelty verdict for Investigation 6

**The HM / Guth-Maynard optimization already is the decision-theoretic
limit of the proposal, in an averaged sense.** No new ingredient is
provided by the additive-evidence framing: the convergent envelope
hypothesis forces averaging (section 5.4), and once we're averaging we are
in the HM/Guth-Maynard regime. Guth-Maynard 2024 is the state of the art
in this regime. The proposal adds nothing.

## 10. Final Verdict

### 10.1 Novelty assessment (all 6 investigations)

| # | Question | Verdict |
|---|----------|---------|
| 1 | Equivalent to mollifiers? | Yes; in fact a restricted sub-class (with coefficients decaying faster than standard mollifiers). |
| 2 | Neyman-Pearson formulation summable? | No; the alternative is singular w.r.t. Bohr-Jessen, so any `L^1`-convergent detector is band-limited and cannot resolve zeros. |
| 3 | Minimax LP feasible? | Pointwise LP is trivial (decouples, equals `max target`). Coupled LP reduces to Beurling-Selberg, already optimized in the literature. |
| 4 | Beats Vinogradov-Korobov? | No; produces strictly weaker bounds on `\|zeta\|` and no new zero-free region. |
| 5 | Optimization upgrades probabilistic to deterministic? | No; pointwise max exceeds averaged mean by `-log|s-rho|` near each zero, unbounded. |
| 6 | New relative to Halasz-Montgomery? | No; same regime, Guth-Maynard 2024 is the state of the art. |

### 10.2 One-paragraph summary

The sign-corrected additive-evidence proposal asks whether one can dominate
`-log|zeta(sigma+it)|` pointwise in `t` by an absolutely convergent sum of
per-prime weights. **This is impossible in two different ways.** First,
quantitatively: any convergent envelope of the form `C(log p)^A / p^{1+eps}`
has total mass bounded by a constant (`primezeta(1+eps)` up to (log p)^A
correction), whereas `sup_t -log|zeta(sigma+it)|` diverges as `sigma -> 1/2`,
so no convergent envelope can dominate. Second, structurally: if we allow the
weights to depend arbitrarily on `t`, the minimax LP decouples and becomes
the trivial observation `tau = max_j target_j`; if we force the weights into
a mollifier form `w_p(t) = Re(a_p p^{-sigma-it})`, we recover the classical
(already-optimized) mollifier problem, whose best known instance
(Guth-Maynard 2024) does not produce a new zero-free region. The proposal
therefore sits strictly inside the well-explored mollifier / Halasz-Montgomery
optimization landscape, and it is strictly weaker than Vinogradov-Korobov as
a source of deterministic zero-free regions.

### 10.3 The precise reason the approach fails

The fatal ingredient is the **absolute-convergence-at-1/2** requirement
`|w_p| <= C(log p)^A / p^{1+eps}`. This is exactly what makes
`E_sigma(t) = sum_p w_p(t)` a continuous, bounded, band-limited function of
`t`. But the object we want to dominate — `-log|zeta(sigma+it)|` — has
logarithmic singularities wherever `zeta` has zeros, and no bounded continuous
function can dominate a logarithmic singularity. Dropping absolute convergence
returns us to conditionally-convergent sums like `log zeta(s) = sum_p log(1-p^{-s})^{-1}`,
which do carry the zeros' information but require exactly the kind of
oscillatory-cancellation analysis that is RH. **The convergent envelope is
the feature that makes the problem tractable; it is also what makes the
problem uninformative.**

This is the same barrier identified in every previous probabilistic approach
to RH in this investigation (Jensen-concentration wrong-arrow, almost-periodic
growth mismatch, concentration-invariant probabilistic-to-deterministic gap).
The additive-evidence proposal is a new presentation of the same barrier, not
a new technique for breaching it.

## 11. Connection to Prior Experiments

| Experiment | Relation |
|------------|----------|
| `convolution-invariant/` | Wave 6 showed the probabilistic concentration inequality can't be upgraded to deterministic. This experiment specializes that lesson to a minimax LP formulation. |
| `mobius-martingale/` | Wave 6 showed prime-by-prime detectors are circular. This LP is a linear version of the same detector, with the same issue. |
| `almost-periodic-concentration/` | Wave 7 showed AP growth and concentration growth are mismatched. This LP exhibits the same mismatch at the level of `sum_p 1/p^{1+eps}` vs `sup_t -log|zeta|`. |
| `jensen-concentration/` | Wave 7: wrong arrow. Here too: our LP bounds averaged quantities, we want pointwise. |
| `gmc-repulsion/` | `sigma = 1/2` is the GMC critical point. Our envelope budget is precisely the integral test for `eta`-scale GMC, and it diverges as `sigma -> 1/2`. |

The proposal is the same wall under new lighting.

## 12. Files Produced

- `findings.md` — this document
- `code/lp_experiment.py` — main minimax LP solver (sign-corrected), sweeps
  over `sigma`, envelope `eps`, prime cutoff, and `(log p)^A` factors.
- `code/lp_structural_check.py` — proof-by-numerical-demonstration that the
  LP decouples across `t` and depends only on `sum_p B_p`.
- `code/mollifier_reduction.py` — computes `t`-averages of `-log|zeta|` to
  illustrate the averaged-vs-pointwise gap.

## 13. Key References

1. **Selberg, A.** (1942). "On the zeros of Riemann's zeta-function." *Skr. Norske Vid. Akad. Oslo*. Original mollifier construction.
2. **Levinson, N.** (1974). "More than one third of zeros of Riemann's zeta-function are on sigma = 1/2." *Adv. Math.* 13.
3. **Conrey, J. B.** (1989). "More than two fifths of the zeros of the Riemann zeta function are on the critical line." *J. Reine Angew. Math.* 399.
4. **Bui-Conrey-Young** (2011). "More than 41% of zeros of zeta..." *Acta Arith.* 150.
5. **Conrey-Iwaniec-Soundararajan** (2012). "Asymptotic large sieve." *Acta Arith.*
6. **Guth-Maynard** (2024). "New large value estimates for Dirichlet polynomials." arXiv 2405.20552.
7. **Halasz-Montgomery** large-value method, as in Iwaniec-Kowalski *Analytic Number Theory*, chapter 9.
8. **Vinogradov** (1958), **Korobov** (1958), **Ford** (2002) — zero-free region constants.
9. **Jessen-Wintner** (1935), **Laurincikas** (1996) — Bohr-Jessen distribution of `log|zeta|`.
10. **Soundararajan** (2009), **Bondarenko-Seip** (2018) — large values of `|zeta|`.
11. **Beurling-Selberg** extremal functions: Vaaler (1985), Graham-Vaaler (1981), Carneiro-Vaaler (2010).
12. **Prior experiments in this investigation:**
    - `convolution-invariant/findings.md` (Wave 6)
    - `mobius-martingale/findings.md` (Wave 6)
    - `jensen-concentration/findings.md` (Wave 7)
    - `almost-periodic-concentration/findings.md` (Wave 7)

## 14. Honest Rating

**Mathematical depth: 5/10.** The sign correction, decoupling lemma, and
envelope-budget analysis are all elementary (once correctly framed). The
novelty verdict relies on mapping the proposal into the mollifier /
Halasz-Montgomery landscape, which is a literature-identification exercise.

**RH proximity: 1/10.** The proposal does not produce a new zero-free region
or any new structural insight into `zeta`. It sits strictly inside territory
already covered (and outperformed) by classical mollifier methods.

**Utility of the finding: high.** The result is a clean "door closed":
any future proposal phrased as "convergent sum of per-prime weights
dominating `-log|zeta|`" can be rejected on sight via the decoupling lemma
and envelope-budget argument. This adds one more approach to the "doors
definitively closed" list in the Riemann hypothesis investigation synthesis.
