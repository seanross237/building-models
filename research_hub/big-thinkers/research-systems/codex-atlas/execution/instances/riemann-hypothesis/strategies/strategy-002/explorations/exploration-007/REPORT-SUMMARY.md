# Exploration 007 — Report Summary

## Goal
Adversarial review of the claim: "C1 random-phase Von Mangoldt Hankel matrix satisfies Montgomery's pair correlation at 7.9% MRD."

## What Was Tried
Three adversarial tests on N=500 matrices:
1. Null matrix comparison: GUE control, flat-amplitude random phase, flat Toeplitz
2. C1 stability: 20 independent realizations, MRD computed per-realization
3. Severity assessment of all attack vectors

## Outcome: THREE SERIOUS ATTACKS ESTABLISHED

### Test 1 — Von Mangoldt Amplitude Unnecessary [COMPUTED]
- **GUE control MRD = 7.8%** — passes threshold, essentially same as C1's 7.9%
- **Flat-amplitude random phase MRD = 6.8%** — BETTER than C1
- **Flat Toeplitz (GOE class) MRD = 9.0%** — even a GOE-class matrix passes

**Finding: The Von Mangoldt amplitude structure is unnecessary. Any GUE-class (or even GOE-class) matrix achieves comparable pair correlation MRD when averaged over 5 realizations.**

### Test 2 — Individual Realization Instability [COMPUTED]
- **C1 individual MRD mean = 15.5% ± 1.9%** (20 realizations)
- **Pass rate: 0/20** — not a single realization achieves MRD ≤ 10%
- The 7.9% from E005 was for 5-realization AVERAGED R₂, which reduces noise by ~√5

**Finding: "MRD = 7.9%" is a 5-realization averaging artifact. Individual N=500 matrices have pair correlation noise of ~15.5%. The "PASS" verdict requires averaging over multiple realizations.**

### Test 3 — Severity Assessment

| Attack | Severity | Verdict |
|---|---|---|
| Von Mangoldt amplitude unnecessary | SERIOUS | ESTABLISHED |
| 7.9% MRD not stable per realization | SERIOUS | ESTABLISHED |
| Pair correlation insensitive to matrix class | SERIOUS | ESTABLISHED |
| GUE class ≠ Riemann-like (β=1.18 vs 2.0, Δ₃=0.285 vs 0.156) | MODERATE | ESTABLISHED |
| 3/10 PASS not strong evidence | MODERATE | ESTABLISHED |

## Restated Honest Claim
*"The C1 construction is in the GUE universality class. When pair correlation is averaged over 5+ realizations, it satisfies Montgomery's formula at ~8-10% level. This is generic to any GUE-class (or GOE-class) Hermitian matrix and does not require the Von Mangoldt amplitude structure. The random complex phase structure drives the GUE classification; the amplitude is irrelevant."*

**Status: SUPPORTED (not ESTABLISHED)** — The pair correlation result is real but not novel; it follows from GUE class membership.

## Unexpected Finding
Toeplitz GOE-class matrices (β=0.45) also pass the 9.0% MRD threshold. This shows that at N=500 with 5-realization averaging, pair correlation MRD is not capable of distinguishing GOE from GUE — it's insufficiently discriminating. A meaningful test requires larger N or more realizations.

## Key Takeaway
The adversarial review substantially weakens the pair correlation claim. The surviving strong result is not pair correlation but rather:
1. **C1 is in GUE universality class** (spacing distribution, form factor) — the random complex phases are sufficient
2. **C1 has anomalous intermediate rigidity** (Δ₃=0.285, between GUE=0.565 and zeta=0.156) — this IS specific to the Von Mangoldt Hankel structure and is not reproduced by flat amplitudes
3. **All arithmetic phase constructions (Gauss, Dirichlet) are GOE-confined** — an algebraically proved negative result

The most defensible novel claim shifts from pair correlation to the Δ₃ intermediate rigidity and the Dirichlet impossibility theorem.
