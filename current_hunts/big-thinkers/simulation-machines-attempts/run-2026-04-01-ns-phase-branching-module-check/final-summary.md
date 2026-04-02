# Final Summary

## Answer

The first honest branching module above the surviving exact core triad does
not show immediate phase frustration. It shows the opposite:

- an exact three-phase quadrature-locked sector exists on the reduced internal
  dynamics, and
- the first serious obstruction is recursive support spill, not a finite
  incompatibility of constructive phase windows.

So this round weakens the original Route 3 story in one specific way:

```text
first-branch phase frustration is not the right lead object
```

If the phase/coherence route survives, it should now be reframed as a
`recursive closure / spectator-overload against would-be locking` route.

## Minimal Branching Module

Take the surviving exact core triad from the earlier helical audit

```text
a1 : (1,0,0), sigma = +1
a3 : (0,1,0), sigma = -1
a4 : (1,1,0), sigma = +1
```

and adjoin the first two exact emissions already identified there:

```text
b : (1,2,0), sigma = +1
c : (2,1,0), sigma = +1.
```

With conjugates included for reality, the exact internal Waleffe-helical
equations on this five-mode branch are

```text
dot z1 = -i alpha conj(z3) z4 - i beta conj(z4) zc + F1^ext
dot z3 = -i alpha conj(z1) z4 - i delta zb conj(z4) + F3^ext
dot z4 =  2i alpha z1 z3 - i eps zb conj(z3) + i zeta conj(z1) zc + F4^ext
dot zb =  i eta z3 z4 + Fb^ext
dot zc = -i kappa z1 z4 + Fc^ext
```

with numerical coefficients

```text
alpha = 0.176776695297
beta  = 0.371762039816
delta = 0.036351843192
eps   = 0.321326551542
zeta  = 0.479440434550
eta   = 0.357678394734
kappa = 0.107678394734.
```

Here `F^ext` denotes the still-present emissions outside this five-mode branch.

## Gauge-Invariant Phase Variables

Write

```text
zj = rj exp(i theta_j).
```

Modulo the two translation gauges, the natural exact phase variables are

```text
phi   = theta1 + theta3 - theta4
phi_b = theta3 + theta4 - theta_b
phi_c = theta1 + theta4 - theta_c.
```

Ignoring viscosity and external spill for the internal phase test, the
amplitude equations become

```text
dot r1 = -alpha r3 r4 sin(phi) - beta  r4 rc sin(phi_c)
dot r3 = -alpha r1 r4 sin(phi) - delta rb r4 sin(phi_b)
dot r4 = -2alpha r1 r3 sin(phi) - eps  rb r3 sin(phi_b)
         + zeta r1 rc sin(phi_c)
dot rb = -eta   r3 r4 sin(phi_b)
dot rc =  kappa r1 r4 sin(phi_c).
```

The corresponding phase drifts depend only on cosines:

```text
dot phi   = -(alpha r3 r4 / r1 + alpha r1 r4 / r3 + 2alpha r1 r3 / r4) cos(phi)
            + (-delta rb r4 / r3 + eps rb r3 / r4) cos(phi_b)
            + (-beta r4 rc / r1 - zeta r1 rc / r4) cos(phi_c)

dot phi_b = alpha(-r1 r4 / r3 + 2r1 r3 / r4) cos(phi)
            - (delta rb r4 / r3 + eps rb r3 / r4 + eta r3 r4 / rb) cos(phi_b)
            + zeta r1 rc / r4 cos(phi_c)

dot phi_c = alpha(-r3 r4 / r1 + 2r1 r3 / r4) cos(phi)
            - eps rb r3 / r4 cos(phi_b)
            + (-beta r4 rc / r1 + zeta r1 rc / r4 + kappa r1 r4 / rc) cos(phi_c).
```

## Main Structural Finding

There is an exact constant-phase sector

```text
phi   = -pi/2
phi_b = -pi/2
phi_c = +pi/2
```

because all three phase drifts vanish there identically.

On that sector,

```text
dot r4 = 2alpha r1 r3 + eps rb r3 + zeta r1 rc
dot rb = eta r3 r4
dot rc = kappa r1 r4
```

so the core transfer and both first-branch emissions are simultaneously
constructive. The first branching layer therefore does not produce the finite
"incompatible constructive windows" obstruction that the earlier Route 3 hope
was targeting.

## What Actually Breaks First

This five-mode branch is not recursively closed. The same exact audit gives 72
ordered external emissions immediately outside the branch. The strongest new
families are:

- `(0, 2, 0)` from `a1 * conj(b)` with coefficient magnitude `0.413947519809`,
- `(2, 2, 0)` from `a3 * c` with coefficient magnitude `0.367637035676`,
- `(2, 0, 0)` from `conj(a3) * c` with coefficient magnitude `0.255833636801`,
- `(-1, 1, 0)` and `(1, -1, 0)` from `b * conj(c)` with coefficient magnitude
  `0.237170824513`,
- `(2, 2, 0)` again from `a1 * b` with coefficient magnitude `0.209523152667`.

So the first honest obstruction candidate is no longer "phase frustration on a
small closed branch." It is:

```text
can any quadrature-locked constructive sector survive the recursively forced
spectator and companion spill?
```

## Verdict For Route 3

- `finite first-branch phase frustration`: downgraded
- `small exact phase-locked branch exists at reduced level`: yes
- `recursive closure / spectator-overload against locking`: still live

This means Route 3 remains the best intrinsic line only in a narrowed form. The
next clean theorem-or-kill task is:

```text
test whether the quadrature-locked sector above can persist once the first
forced external families are added recursively, or whether exact closure
explodes too fast for any genuine delayed-transfer locking window to survive
```
