# Exploration 001 Summary: Beta from Vasseur (2007)

## Goal
Extract the precise mathematical definition of the pressure exponent β from Vasseur's De Giorgi iteration framework for Navier-Stokes regularity.

## Outcome: SUCCESS — All 7 deliverables answered with equation-level precision.

## Key Takeaway

**β is NOT a pressure integrability exponent.** It is the nonlinear recurrence exponent in the De Giorgi level-set iteration. Specifically, Vasseur's Proposition 3 gives:

`U_k ≤ C_p^k (1 + ||P||_{Lp(L1)}) U_{k-1}^{β_p}`

where U_k measures energy on level sets v_k = [|u| - (1-2^{-k})]_+. If β > 3/2, ALL suitable weak solutions are regular (Conjecture 14 + Appendix proof). Current best: β < 4/3 (strictly), from a single term — the non-divergence part of the local pressure P_k^{21}. All other terms (transport, nonlocal pressure, local pressure in divergence form) exceed 3/2. The gap to close is > 1/6.

The bottleneck is: ∫|P_k^{21}| · |d_k| · 1_{v_k>0} dx dt, where P_k^{21} is bounded in all L^q by CZ theory independently of U_{k-1}. This "constant" bound (not depending on the level set energy) is what kills the exponent — the pressure doesn't get small even when the velocity is near its truncation level.

## DNS Computability: PARTIALLY computable
U_k, the pressure decomposition, and the bottleneck integral are all computable on periodic grids. The empirical β can be extracted by fitting the recurrence for k = 0,...,~12. Main adaptation: replace nested balls with periodic domain. Main limitation: single-flow non-universality.

## Unexpected Findings
The CZ slack measured earlier (7.6-17.5×) is on the FULL pressure, but the bottleneck involves P_k^{21} — a specific piece of the decomposed pressure involving u(1-v_k/|u|), which is bounded by 1. If CZ slack persists for this specific piece, the empirical β could significantly exceed 4/3.

## Computations Identified
1. **Empirical β measurement from DNS** — compute U_k for k=0,...,12 on Taylor-Green and anti-parallel tube flows, fit recurrence exponent. ~100 lines Python/spectral. Would reveal whether β > 4/3 or even > 3/2 empirically.
2. **CZ slack on P_k^{21} specifically** — decompose DNS pressure into the De Giorgi local/nonlocal pieces and measure CZ tightness on each piece separately. ~150 lines. Would identify whether the slack is in the bottleneck term or elsewhere.
