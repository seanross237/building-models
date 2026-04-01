# Anatomy of Averaged NS Blowup Firewall

Source filter: local factual library, meta library, and mission meta-inbox only.
Scope: Phase 1 intervention-map briefing for Tao-style blowup mechanism tracing.

## Bottom Line

The strongest local material says the next exploration should treat the Tao shell cascade as a question of missing exact-NS structure, not missing estimates.

The main live candidates are:

1. a decomposition mismatch around the pressure split, not a weakness in the harmonic far-field term itself;
2. exact pressure/Leray/incompressibility couplings that remain rigid under boosts and truncation;
3. structural, not quantitative, obstructions in the quadratic NS couplings;
4. measure-zero symmetry cases like exact Beltrami that look decisive but do not generalize;
5. already-closed estimate routes that should be preloaded as dead ends.

## Candidate Firewall Types

### 1) Triadic coefficient rigidity or sign constraints in exact NS

Most useful material:

- `factual/navier-stokes/vasseur-de-giorgi/vorticity-degiorgi-universal-barrier.md`
- `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md`
- `factual/navier-stokes/vasseur-de-giorgi/proposition-3-sharpness-audit.md`

Usable content:

- The exact NS bottleneck survives a formulation change from pressure-based to vorticity-based De Giorgi.
- The same `1/2 + 5/6` exponent split reappears in the trilinear term `T_∇[alpha_k v, rho_k beta_k v, beta_k v]`.
- The 4/3 barrier is presented as intrinsic to the quadratic structure, not to one proof packaging.
- The exact obstruction is not a free coefficient sign choice; it is the non-divergence quadratic coupling.

Status:

- `potentially load-bearing` if the next exploration can identify a sign/asymmetry that exact NS has and the toy circuit averaged away.
- `already closed` for ordinary estimate-level coefficient tuning.

### 2) Unavoidable extra same-scale or cross-scale couplings in exact NS

Most useful material:

- `factual/navier-stokes/vasseur-de-giorgi/frequency-localized-degiorgi-lp-obstruction.md`
- `factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md`
- `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md`

Usable content:

- Littlewood-Paley decomposition exposes resonance at low k and paraproduct dominance at high k.
- The Bernstein exchange rate `2^{3j/5}` is dimensional, not a tunable artifact.
- The surviving far-field lead is a decomposition mismatch: `P_{k1}` is already favorable, while the load-bearing term is `P_{k21}`.
- The pressure-side obstruction is about which coupling carries the level-set scaling, not about the existence of any harmonic piece.

Status:

- `already closed` for frequency-localized or LP-paraproduct bypasses.
- `potentially load-bearing` only if a different exact-NS near/far split moves the dangerous pairing into a genuinely `U_k`-dependent harmonic piece.

### 3) Pressure / Leray / incompressibility couplings that destroy Tao-style trigger isolation

Most useful material:

- `factual/navier-stokes/vasseur-de-giorgi/pressure-galilean-invariance.md`
- `factual/navier-stokes/vasseur-de-giorgi/pressure-bernoulli-dominance-truncated.md`
- `factual/navier-stokes/near-beltrami-negative-result.md`
- `factual/navier-stokes/beltrami-pressure-analytical.md`

Usable content:

- Pressure Poisson is Galilean-invariant for incompressible flow, so boosts do not change the source term or the CZ bound.
- Exact Beltrami flows satisfy `L = omega x u = 0` and `p = -|u|^2/2 + const`.
- Truncated Beltrami flows can be Bernoulli-dominated, but only in the exact Beltrami setting.
- Perturbed ABC flows break the Beltrami decay immediately; `B_k` stops decaying for any `eps > 0` and Leray projection is minor.

Status:

- `already closed` for generic pressure-shift or frame-shift arguments.
- `potentially load-bearing` only for exact-symmetry special cases, but E010 says these are measure-zero and do not generalize.

### 4) Dynamically decisive but energetically negligible modes / structural obstructions

Most useful material:

- `factual/navier-stokes/vorticity-intermittency-measures.md`
- `factual/navier-stokes/vortex-stretching-structural-slack.md`
- `factual/navier-stokes/beltrami-zero-vortex-stretching.md`
- `factual/navier-stokes/adversarial-minimum-vs-slack.md`

Usable content:

- Vorticity can be highly intermittent: 1-2.4% of the domain carries `|omega| > 0.5 * omega_max`.
- The effective Ladyzhenskaya constant varies much less than the raw vorticity concentration.
- Exact symmetry classes can make the decisive term identically zero: ABC Beltrami and z-invariant vortex tubes have zero vortex stretching.
- The minimum observed vortex-stretching slack is still huge, so the bottleneck is geometric and not just energetic.

Status:

- `potentially load-bearing` as a warning sign: tiny support or tiny remainder terms can still control the mechanism.
- `cosmetic` if used only as a smoothness/flatness proxy without a causal link to the Tao cascade.

### 5) Prior closures to preload so the exploration does not drift back to estimate-level routes

Preload these as dead ends:

- `factual/navier-stokes/vasseur-de-giorgi/chebyshev-sharpness-constant-field-extremizer.md` - div-free Chebyshev improvement is closed; constant field extremizer hits ratio 1
- `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md` - commutator / CLMS route closed
- `factual/navier-stokes/vasseur-de-giorgi/frequency-localized-degiorgi-lp-obstruction.md` - LP / Bernstein route closed
- `factual/navier-stokes/vasseur-de-giorgi/non-cz-pressure-routes-tool-independence.md` - non-CZ pressure routes do not beat 4/3
- `factual/navier-stokes/near-beltrami-negative-result.md` - near-Beltrami generalization fails
- `factual/navier-stokes/vasseur-de-giorgi/beltrami-deficit-truncation-survival.md` - exact Beltrami truncation survives only as a special-case phenomenon
- `factual/navier-stokes/vasseur-de-giorgi/pressure-bernoulli-dominance-truncated.md` - Bernoulli dominance is exact-symmetry-only
- `factual/navier-stokes/vasseur-de-giorgi/pressure-galilean-invariance.md` - frame shifts do not help

Status:

- These are `already closed` for the kind of estimate-level route that only improves constants or rearranges the same pressure bound.

## Meta Guidance That Actually Helps

Most relevant meta notes:

- `meta/methodology/model-pde-comparison-for-mechanism-identification.md`
- `meta/goal-design/distinguish-identity-from-mechanism.md`
- `meta/methodology/structural-vs-quantitative-discrepancy.md`
- `meta/methodology/distinguish-constant-from-scaling-slack.md`
- `meta/methodology/check-bypass-not-just-improve-bottleneck.md`
- `meta/methodology/comparison-exploration-pattern.md`
- `meta/goal-design/preload-context-from-prior-work.md`
- `meta/goal-design/adversarial-synthesis-goal-structure.md`
- `meta/goal-design/include-predecessor-comparison-for-reformulations.md`
- `meta/INDEX.md` updates: `reconcile-notation-before-falsification`, `allow-analytic-extremizer-over-computation`

What they imply for Phase 1:

- Compare exact NS against the toy mechanism with explicit dimensions, not just analogies.
- Treat algebraic identities separately from actual mechanisms.
- Ask whether the discrepancy is structural or merely a constant-factor slack issue.
- Preload all already-closed routes so the next exploration cannot quietly rediscover them.
- Let the exploration search for an analytic extremizer if the route is really about structure, not computation.

## Concise Table-Ready Mapping

| Tao cascade step | Exact NS structure missing after averaging | Concrete mathematical form | Causal role in cascade | Status |
|---|---|---|---|---|
| pressure trigger isolation | Galilean/pressure invariance does not create a `U_k`-dependent gain | `-Δp = ∂_i∂_j(u_i u_j)`; boosts leave source unchanged | prevents frame-shift escape | already closed |
| far-field pressure replacement | harmonic piece already favorable; mismatch is local vs harmonic decomposition | `P = P_{k1} + P_{k2}`, with bad term `P_{k21}` | only live route is a different near/far split | potentially load-bearing |
| cross-scale cleanup | LP/paraproduct still leaves dimensional Bernstein cost | `2^{3j/5}` exchange rate | same-scale/cross-scale couplings reappear | already closed |
| exact symmetry trigger | exact Beltrami / zero Lamb vector | `omega x u = 0`, `p = -|u|^2/2 + const` | isolates decisive but special-case cancellation | potentially load-bearing, but measure-zero |
| level-set improvement | div-free does not improve Chebyshev distribution | constant div-free field hits ratio 1 | no hidden exponent gain from incompressibility | already closed |

## Confidence

High confidence on the closure stack and pressure/Leray points. Moderate confidence that the exact far-field decomposition mismatch is the live phase-1 question worth testing next.
