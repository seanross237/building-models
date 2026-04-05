# Helical Sign-Defect Prototype

## Goal

Test whether the favored

```text
canonical helical packet + homochiral bottleneck
```

route shows any real signal on the exact singleton-support audit machinery that
already exists in the repo.

This is **not** a new packet theorem. It is a small follow-up check on the
existing exact helical support audit from

- `codex-atlas/.../exploration-002/code/helical_support_audit.py`

The narrow question is:

```text
if we define a few candidate sign-defect functionals in exact helical-ledger
language, do lower-leakage sign patterns look more near-homochiral?
```

## Setup

Work on the existing five-role singleton test support

```text
k1 = (1,0,0)
k2 = (2,0,0)
k3 = (0,1,0)
k4 = (1,1,0)
k5 = (2,2,0)
```

and scan all `32` helicity sign assignments already used by the exact audit.

Use the existing exact Waleffe-helical coefficient law and define three simple
prototype sign-defect quantities:

1. `SignDefect_count`
   - minority-sign fraction among the five distinguished roles.

2. `SignDefect_mode`
   - exact-ledger-weighted minority-sign fraction, where each role is weighted
     by the sum of absolute exact coefficient contributions of all triads in
     which it participates.

3. `SignDefect_triad`
   - exact-ledger-weighted fraction of contributions whose three helical signs
     are not all equal.

For the old singleton support, use the same leakage scalarization as the audit:

```text
LeakRatio = (internal_leak + external_leak) / desired_drive.
```

## Main Findings

### 1. Lowest leakage among nonzero desired patterns occurs at smallest minority-sign count

Among the sign patterns with nonzero desired drive, the best leak ratio occurs
when exactly one of the five roles has the minority sign:

```text
SignDefect_count = 1/5 = 0.2
best LeakRatio ≈ 92.09
```

The next tier has

```text
SignDefect_count = 2/5 = 0.4
LeakRatio ≈ 94.31 to 97.43
```

So on this exact support, lower leakage does line up with more globally
near-homochiral organization.

### 2. The desired activation triad is necessarily heterochiral

For the only surviving desired singleton channel

```text
a1 + a3 -> a4
```

the exact helical coefficient is nonzero only when the source signs are
opposite:

```text
s1 = -s3
```

and it vanishes in the same-sign cases.

So the desired activation channel itself is never homochiral on this support.
In the prototype metric restricted to desired drive,

```text
SignDefect_triad_desired = 1
```

for every sign pattern with nonzero desired drive.

### 3. Fully homochiral sign assignments kill the desired drive

The two all-same-sign patterns

```text
(+,+,+,+,+), (-,-,-,-,-)
```

have

```text
desired_drive = 0.
```

So the pure homochiral limit does not realize the desired Tao-like activation
edge even before packet issues enter.

### 4. The global squeeze appears real, but still only at the killed singleton level

The support shows a clean local tension:

- move toward more global sign coherence and the leak ratio improves slightly;
- push all the way to homochiral and the desired forward activation disappears;
- keep the mixed-sign activation alive and the exact circuit remains highly
  heterochiral at the desired triad level and still leaks massively.

That is exactly the kind of bottleneck shape the favored route was hoping for.

## Interpretation

This does **not** prove the homochiral bottleneck route.

It does show that the route is no longer just a slogan:

- there is a concrete sign-sensitive squeeze already visible in exact helical
  ledger data;
- the squeeze is compatible with the external helical literature story;
- the missing step is now clearly a packet-level generalization, not a total
  absence of signal.

The result should be read carefully:

- it lives on a singleton support that is already known to be terminally dead as
  an exact Tao-circuit object;
- therefore it is only evidence for the *mechanism shape*, not for the final
  theorem object.

## Best Next Step

If this line continues, the next useful move is:

1. keep the exact-ledger viewpoint,
2. lift `SignDefect_mode` from singleton roles to packet families,
3. define it as a normalized minority-helicity participation mass in the exact
   packet ledger,
4. then test whether low packet leakage forces a positive lower bound on that
   packet sign-defect or yields a compact minimizing sequence.

## Bottom Line

The homochiral bottleneck now has one concrete local data point in its favor:
on the existing exact helical support audit, the least-leaky nontrivial sign
patterns are the most globally near-homochiral ones, but the desired activation
channel itself remains obligatorily heterochiral.

That makes the route worth continuing one level further at the packet stage.
