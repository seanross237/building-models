# Executive verdict

[CHECKED] The definition gate passes. A "near-closed Tao circuit" can be made precise enough to be true or false in exact Navier-Stokes if it is formulated in the exact helical Fourier basis and tested through a finite directed hypergraph of desired monomials plus a computable leakage ratio.

[VERIFIED] In the helical basis,

```text
u(k) = u_+(k) h_+(k) + u_-(k) h_-(k),
ik × h_s(k) = s |k| h_s(k),
```

and the exact Navier-Stokes evolution becomes

```text
(∂t + ν|k|^2) u_{s_k}(k)
  = -1/4 ∑_{k+p+q=0} ∑_{s_p,s_q}
      (s_p |p| - s_q |q|)
      (h_{s_p}(p) × h_{s_q}(q) · h_{s_k}(k))̄
      u_{s_p}(p) u_{s_q}(q).
```

[VERIFIED] This is an exact reformulation of incompressible Fourier NS, not a toy model. The key local-library gap was not the interaction law itself but the absence of a precise circuit definition stated in this exact language.

# Tao mechanism map to candidate circuit object

[VERIFIED] Tao's five mechanism roles are:

- `a`: current carrier
- `b`: slow clock
- `c`: tiny trigger
- `d`: conduit / rotor leg
- `ã`: next carrier

[CHECKED] The right exact analogue is therefore a directed hypergraph of quadratic monomials, not a plain five-node graph. The minimal desired monomial pattern is:

```text
a1^2  -> a2   weak pump
a1^2  -> a3   tiny seed
a2a3  -> a3   amplifier
a1a3  -> a4   rotor activation
a3a4  -> a1   rotor feedback / exchange leg
a4^2  -> a5   handoff
```

[CHECKED] Real-valuedness forces conjugate bookkeeping. If `k` is active then `-k` is active with linked amplitude, so an honest exact support already includes the mirror modes.

# Preferred definition

## Preferred object: exact five-role helical-mode circuit

Choose distinct representative wavevectors and helicities

```text
K = {k1, k2, k3, k4, k5} ⊂ Z^3 \ {0},
σ = (σ1, σ2, σ3, σ4, σ5) ∈ {±1}^5.
```

Define the exact active helical support

```text
S(K,σ) := {(k_j, σ_j), (-k_j, -σ_j) : j = 1,...,5},
```

and the distinguished amplitudes

```text
aj(t) := u_{σ_j}(k_j,t),   j = 1,...,5.
```

Let the desired hypergraph `G_target` be the monomial sets

```text
D1 = {(3,4)}
D2 = {(1,1)}
D3 = {(1,1), (2,3)}
D4 = {(1,3)}
D5 = {(4,4)}.
```

For each `aj`, split the exact evolution into

```text
∂t aj = Fj^des(a) + Fj^int-leak(a) + Fj^ext-leak(u) - ν|kj|^2 aj,
```

where:

- `Fj^des` is the sum of exact helical-triad terms whose ordered source pair lies in `Dj`,
- `Fj^int-leak` is the sum of all other exact triad contributions built entirely from `S`,
- `Fj^ext-leak` is the sum of exact triad contributions hitting `aj` with at least one leg outside `S`.

Define the leakage functional on a time interval `I` by

```text
Leak_I(S,G_target;u)
  := max_j sup_{t∈I}
     ( |Fj^int-leak(a(t))| + |Fj^ext-leak(u(t))| )
     / max(|Fj^des(a(t))|, ε_floor),
```

with a bookkeeping floor `ε_floor > 0`.

A solution segment `u|_I` is an `(η, λ, Θ)`-near-closed Tao circuit on `(S,G_target)` if:

1. the total helical energy outside `S` is at most `η_act` times the energy on `S` throughout `I`,
2. `Leak_I(S,G_target;u) ≤ η`,
3. on prescribed windows `I_seed, I_amp, I_rot, I_hand`, the intended desired term dominates every individual leakage term by a factor at least `λ > 1`,
4. there exist thresholds `Θ = (θ_clock, θ_seed, θ_trigger, θ_handoff)` and times `t0 < t1 < t2 < t3` such that:
   - `|a3| ≤ θ_seed` on `[t0,t1]`,
   - the amplifier term in `∂t a3` dominates on `[t1,t2]`,
   - rotor terms dominate the `a1/a4` exchange on `[t2,t3]`,
   - the `a4^2 -> a5` handoff dominates on a terminal subwindow of `[t2,t3]`.

[CHECKED] This is narrow enough to test. Every ingredient is exact or explicitly parameterized, and Phase 1 can now build a literal desired-vs-leakage interaction ledger.

## Exact objects vs user-chosen tolerances

[VERIFIED] Exact NS objects:

- wavevectors `k_j`,
- helicity signs `σ_j`,
- exact helical basis vectors `h_σ(k)`,
- exact coefficients `C(k,p,q;s_k,s_p,s_q)`,
- triad constraint `k+p+q=0`,
- reality constraint coupling `k` and `-k`,
- the exact solution `u(t)`.

[CHECKED] User-chosen tolerances:

- support concentration `η_act`,
- leakage budget `η`,
- dominance gap `λ`,
- thresholds `Θ`,
- activation windows,
- bookkeeping floor `ε_floor`.

## Obstruction vs counterexample

[CHECKED] A positive obstruction would show:

```text
For every admissible (K,σ) and every candidate interval I,
either Leak_I has a fixed lower bound c0 > 0, or the delayed-trigger
dominance conditions cannot all hold simultaneously.
```

[CHECKED] A counterexample would exhibit explicit `(K,σ)`, explicit tolerances `(η, λ, Θ)`, and an exact solution segment `u|_I` satisfying all four conditions.

# Backup definition or rejection of alternatives

## Backup: finite helical-packet circuit

[CHECKED] A backup definition replaces each singleton helical mode by a finite packet `P_j` and defines one projected packet amplitude or packet energy per Tao role. This remains exact if the packets are finite exact subsets of helical Fourier space.

## Why it is only the backup

[CHECKED] The packet version is weaker at the gate because projected packet amplitudes are basis-dependent, packet energies lose phase information, and the leakage scalarization becomes less canonical. Phase 1 would first need a packetization convention before it could even write the ledger.

## Rejected alternatives

[CHECKED] Reject "five active Fourier magnitudes with small spectator energy" as the primary definition: it is too coarse for Tao's monomial-level mechanism.

[CHECKED] Reject combinatorial triad counts as the primary definition: counting desired and undesired triads without weighting by exact coefficients and amplitudes does not measure the actual leakage threat.

[CHECKED] Reject a pure packet-energy leakage measure with no exact amplitude decomposition: that simply restates the original vagueness in different notation.

# Precision gate analysis

[VERIFIED] The exact helical basis supplies the missing exact-language layer. The definition problem is no longer blocked on Leray projection, incompressibility, or the absence of a precise exact interaction law.

[CHECKED] The real choice is between:

- an amplitude-level definition that preserves exact monomials and phase-sensitive leakage bookkeeping,
- and a packet-energy definition that is more Tao-like but less sharp.

[CHECKED] The amplitude-level singleton definition is preferable because the next exploration needs a coefficient-by-coefficient interaction ledger. The helical triad law already packages Leray projection, incompressibility, and helicity into exact coefficients, so it is the cleanest Phase 1 interface.

[CHECKED] The remaining arbitrariness is now explicit and acceptable: the tolerances `(η, λ, Θ)` and the choice of activation windows are user-imposed parameters, not hidden pieces of the exact law.

[CHECKED] Therefore the idea does not fail the precision gate. What remains open is quantitative: whether any admissible support can make leakage genuinely subordinate to the desired Tao-like channels.

# Phase 1 recommendation or stop verdict

[CHECKED] Gate verdict: `pass`.

[CHECKED] Phase 1 should use the preferred singleton helical-mode definition, not the packet backup.

[CHECKED] The exact interaction audit should now do exactly three things:

1. choose the smallest candidate five-role support `(K,σ)`,
2. write the full exact helical interaction ledger for `a1,...,a5`, including conjugate-forced companions,
3. classify each term as desired, internal leakage, or external leakage, with tunable-vs-rigid status.

[CHECKED] The cheapest adversarial screen should be embedded immediately: try at least one helicity/sign arrangement designed to suppress leakage before accepting any impossibility story.

## Sources used

- Local Atlas factual notes on Tao's five-stage circuit, coefficient rigidity, and unavoidable spectator couplings.
- Exact helical decomposition and triad equations as restated in Biferale, Musacchio, Toschi, *J. Fluid Mech.* 730 (2013), section 2, following Constantin-Majda and Waleffe.
