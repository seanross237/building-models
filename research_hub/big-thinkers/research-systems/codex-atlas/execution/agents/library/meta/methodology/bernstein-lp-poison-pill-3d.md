---
topic: Bernstein inequality is the LP poison pill in 3D; k-dependent character change as structural insight
confidence: verified
date: 2026-03-30
source: "vasseur-pressure s2-meta-exploration-005"
---

## Lesson

The Bernstein inequality exchange rate 2^{3j/5} per LP block in 3D is fixed by dimensional analysis (Sobolev embedding L^2_{3/10} -> L^{10/3}) and destroys any frequency-localized improvement attempt for De Giorgi iterations. This is a general lesson for LP-based approaches to 3D PDE barriers where the target norm is L^{10/3} or similar: the conversion cost from regularity (Sobolev/Besov) to integrability (L^p) is exactly what CZ theory already accounts for. LP decomposition reveals the frequency structure that CZ handles implicitly, but cannot improve it.

## The k-Dependent Character Change

The paraproduct decomposition of P^{21} reveals that no single technique handles all De Giorgi levels optimally:

- **Low k (k=1,2):** resonance term R(u^{below}, u^{above}) dominates (same-frequency interaction)
- **High k (k >= 3):** paraproduct T_{u^below} u^{above} dominates (smooth x rough, exactly CZ exponents)

This transition means a technique that improves low-k estimates (e.g., commutator-based) becomes irrelevant at high k where the De Giorgi argument most needs to close. The character change may explain why the 4/3 barrier is so robust: the problem changes nature across De Giorgi levels, and any single analytical tool only addresses part of the range.

## When to Apply

When considering LP-based improvements for any 3D PDE barrier where:
1. The target norm is L^p with p > 2 (requiring Bernstein conversion from L^2)
2. The improvement would come from better frequency-by-frequency estimates
3. CZ theory is the current analytical tool

Check: is the Bernstein exchange rate 2^{dj(1/2 - 1/p)} comparable to the spectral decay? If yes, LP cannot help. The exchange rate is dimensional (d, p) and cannot be circumvented.

## Broader Pattern

When a barrier tool (here CZ) is optimal frequency-by-frequency, decomposing into frequencies and reassembling cannot beat the undecomposed estimate. Check whether the barrier tool already IS a frequency-by-frequency result before attempting LP decomposition.

## Distinct From

- **extract-precise-obstruction-from-failed-route** — that is about extracting information from failures; this is about recognizing a class of attempts as structurally doomed before running them
- **numerical-spectral-dns-diagnostic** — that is about using spectral DNS as a diagnostic; this is about interpreting the diagnostic (Bernstein cost)
- **distinguish-constant-from-scaling-slack** — that is about measurement interpretation; this is about analytical tool selection
