# Exploration 003 Summary: Tran-Yu on Galilean Invariance and Pressure

## Goal
Assess whether Tran-Yu's use of Galilean invariance for pressure improvement can improve Vasseur's De Giorgi recurrence exponent beta beyond 4/3.

## Outcome: SUCCESS — Grade (C): Not applicable to the De Giorgi bottleneck.

## What Was Tried
Identified and analyzed the full Tran-Yu research program (5 papers, 2015-2021). The referenced "2014 AIHP" paper doesn't exist; the actual program spans Nonlinearity (2015, 2016), AML (2016), JMP (2017), and JFM (2021). Galilean invariance appears explicitly only in the 2021 JFM paper on velocity-pressure correlation.

## Key Takeaway
**The Tran-Yu program operates in a fundamentally different framework (global L^q energy) than Vasseur's De Giorgi iteration (local level-set energy on nested balls).** The two frameworks have different pressure objects, different energy functionals, and different iteration structures. Most critically: **the pressure Poisson equation is Galilean-invariant for divergence-free flows** — a constant frame shift u -> u - u_0 does not change the CZ norm of the pressure at all, because the cross-terms vanish exactly when div u = 0. The Tran-Yu improvement comes from reducing the *velocity factor* in the L^q energy estimate (better constant), not from improving the pressure bound (which is impossible via Galilean boost). This improvement cannot be inserted into the De Giorgi framework where the bottleneck involves the specific decomposed piece P_k^{21}.

## Leads Worth Pursuing
The velocity-pressure anti-correlation (Bernoulli-type, from 2021 paper) might explain why empirical CZ bounds on P_k^{21} could be tighter than worst-case — relevant to the DNS computation identified in Exploration 001, but not to analytical improvement of beta.

## Unexpected Findings
The Choi-Vasseur (2014) paper introduces a **three-way pressure decomposition** P = P_1k + P_2k + P_3 that absorbs the "bad" non-divergence pressure term P_3 into the velocity equation. This is a different and potentially more relevant approach to the P_k^{21} bottleneck than anything in Tran-Yu. Worth investigating separately.

## Computations Identified
None directly from this exploration. The DNS computation of CZ slack on P_k^{21} (from Exploration 001) remains the most relevant empirical test.
