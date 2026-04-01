---
topic: Exact Navier-Stokes admits a testable near-closed Tao-circuit definition in the helical Fourier basis
confidence: checked
date: 2026-03-31
source: "exact-ns-no-near-closed-tao-circuit strategy-001 exploration-001 report"
---

## Finding

The "near-closed Tao circuit" idea passes the definition gate in exact Navier-Stokes if it is stated at the amplitude level in the exact helical Fourier basis. The right object is not a vague five-node isolation slogan and not a packet-energy surrogate. It is a finite sign-closed helical support, a five-role directed hypergraph of desired quadratic monomials, and a coefficient-weighted leakage ratio computed from the exact triad law.

## Exact Definition

Choose distinct wavevectors and helicities

```text
K = {k1, k2, k3, k4, k5} subset Z^3 \ {0},
sigma = (sigma1, ..., sigma5) in {+,-}^5,
```

and define the exact active support

```text
S(K,sigma) = {(kj, sigmaj), (-kj, -sigmaj) : j = 1,...,5}.
```

Let

```text
aj(t) = u_{sigmaj}(kj,t)
```

represent Tao's five roles

- `a1`: current carrier
- `a2`: slow clock
- `a3`: tiny trigger
- `a4`: conduit / rotor leg
- `a5`: next carrier

and encode the intended Tao mechanism as a directed hypergraph of desired source pairs

```text
D1 = {(3,4)}
D2 = {(1,1)}
D3 = {(1,1), (2,3)}
D4 = {(1,3)}
D5 = {(4,4)}.
```

For each target amplitude, split the exact helical evolution into desired, internal-leakage, and external-leakage pieces:

```text
dt aj = Fj^des(a) + Fj^int-leak(a) + Fj^ext-leak(u) - nu |kj|^2 aj.
```

The scalar leakage budget on an interval `I` is

```text
Leak_I(S,G_target;u)
  = max_j sup_{t in I}
      (|Fj^int-leak(a(t))| + |Fj^ext-leak(u(t))|)
      / max(|Fj^des(a(t))|, eps_floor).
```

This makes the definition testable: every term comes from the exact triad law, and every tolerance is exposed as an explicit user choice rather than hidden inside words like "mostly isolated."

## Exact Data Versus Tolerances

Exact NS data:

- wavevectors `kj`
- helicities `sigmaj`
- helical basis vectors `h_sigma(k)`
- exact triad coefficients
- triad constraint `k + p + q = 0`
- reality constraint linking `k` and `-k`
- the exact solution segment `u|_I`

User-chosen tolerances:

- support-concentration budget `eta_act`
- leakage budget `eta`
- dominance gap `lambda`
- threshold vector `Theta`
- activation windows
- bookkeeping floor `eps_floor`

This separation is part of the result: the exact law is now fixed, and the remaining freedom is an explicit theorem parameter list.

## Why The Singleton Definition Is Primary

The preferred Phase 1 object is the singleton helical-mode version above. A packet version remains available as a backup, but only as a weaker formulation.

- The singleton form preserves exact monomials and phase-sensitive bookkeeping.
- Packet amplitudes depend on packetization choices.
- Packet energies lose the phase information needed for Tao's gate logic.
- Triad counts alone are too coarse because they ignore exact coefficients and amplitudes.

So the real choice is not "mode versus packet" in the abstract. It is exact amplitude-level bookkeeping versus coarse packet-energy bookkeeping, and only the former is sharp enough for the first exact ledger.

## Phase 1 Consequence

The next exact audit should:

1. choose the smallest candidate support `(K,sigma)`,
2. write the full helical interaction ledger for `a1,...,a5` including conjugate-forced companions,
3. classify every term as desired, internal leakage, or external leakage,
4. test whether desired terms dominate on the seed, amplifier, rotor, and handoff windows,
5. include at least one helicity/sign arrangement chosen specifically to suppress leakage before accepting any impossibility claim.

## Relationship to Other Entries

- `tao-averaged-ns-delayed-transfer-circuit.md` gives the reduced five-role circuit this exact definition is meant to realize or obstruct.
- `exact-ns-triadic-coefficient-rigidity.md` is the coefficient-level firewall question once the test object is fixed.
- `exact-ns-unavoidable-spectator-couplings.md` is the network-isolation firewall question once desired and leakage terms are separated exactly.
