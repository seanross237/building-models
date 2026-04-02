---
topic: asymptotic-safety
confidence: provisional
date: 2026-03-26
source: exploration-002-fixed-point-compatibility (quantum-gravity-2 strategy-003)
---

# AF–NGFP Fixed Point Connection: Same Point or Distinct?

Does the asymptotically free (AF) UV fixed point of quadratic gravity connect to the non-Gaussian fixed point (NGFP, Reuter) of asymptotic safety via RG flow — or are they the same fixed point seen at different approximation levels?

**Verdict: INCONCLUSIVE** — with strong hints of connection but no definitive proof.

## Two Competing Interpretations

### Interpretation A: Same Fixed Point, Different Approximations

Multiple results suggest the AF Gaussian FP and the NGFP may be the same point viewed at different levels of approximation:

- **Codello & Percacci (2006)**, PRL 97, 221301: Recalculated beta functions of higher-derivative gravity using a one-loop approximation to an *exact* (non-perturbative) RG equation. Found that "the theory appears to be asymptotically safe at a non-Gaussian fixed point rather than perturbatively renormalizable and asymptotically free." The implication: when non-perturbative effects are included, the perturbative AF Gaussian FP gets replaced by (or deformed into) an NGFP.

- **Niedermaier (2009/2010)**, PRL 103, 101303: Found asymptotically safe fixed points using *perturbative* methods in higher-derivative gravity. Strictly positive fixed points for g_N and lambda. "The renormalization flow is asymptotically safe with respect to this fixed point." Further blurs the AF/AS boundary.

- **Ohta & Percacci (2014)**, CQG 31, 015024: Derived one-loop beta functions for gravity with up to four derivatives. Nontrivial UV fixed points found in *all* dimensions studied (3, 4, near-4, 5, 6). Indication that a Weyl-invariant fixed point exists in 4D. Confirms higher-derivative gravity generically has non-Gaussian UV FPs.

- **QQG claim** (Salvio et al.): QQG "features a UV fixed point even in the presence of realistic matter sectors" and "can be regarded as a concrete realization of asymptotic safety."

If Interpretation A is correct, the question of a connecting trajectory is moot — they ARE the same point.

### Interpretation B: Distinct Fixed Points, Possible Connection

- **SWY (2022)**, JHEP 03 (2022) 130: Finds **two distinct fixed points** with different critical exponents and different numbers of relevant directions in the same fourth-order truncation. Explicitly states a "critical trajectory" between them "may exist" but uses hedged language. See `swy-two-fixed-points.md` for full details.

- **Falls, Kluth, Litim (2023)**, PRD 108, 026005: Study the NGFP ("Riemann fixed point") using polynomial Riemann tensor interactions. Find a **four-dimensional UV critical surface** — matching the number of couplings in quadratic gravity (f_2, f_0, G, Lambda). Treats NGFP and perturbative fixed points as distinct entities.

- **SWY (2023)**, JHEP 02 (2023) 054: Compute **scaling solutions** connecting the AF UV fixed point to Einstein gravity in the IR. Demonstrates AF has its own viable IR completion, independent of the NGFP. Does NOT address whether the AF trajectory passes through or near the NGFP.

If Interpretation B is correct, the connection question is open and important.

## Resolution of the Tension

The tension appears to be **truncation-dependent**:
- In the SWY truncation (gauge-invariant flow with all fourth-order terms): two FPs are clearly resolved
- In earlier truncations (Codello-Percacci, Einstein-Hilbert + R²): only one NGFP is found, which may be the AF FP shifted by non-perturbative effects

The SWY result is more refined and should be given more weight. But the Codello-Percacci result cannot be dismissed — it may indicate that the distinction is an artifact of perturbation theory.

## Known Flow Structure

In the full (f_2, f_0, G, Lambda) coupling space:
- **NGFP → GFP (Gaussian):** Standard AS trajectory. Well-established (Reuter 1998 onward).
- **AF → IR (Einstein gravity):** Scaling solutions exist (SWY 2023). Viable.
- **AF → NGFP:** "May exist" as critical trajectory (SWY 2022). Not computed.

## Specific Literature Gaps

1. **No paper has explicitly computed an RG trajectory from the AF fixed point to the NGFP.** This is the key missing calculation.
2. No systematic comparison of critical exponents between AF and NGFP across matching truncations.
3. No study of the separatrix structure in the full 4D coupling space that would definitively answer whether the two FPs are connected.
4. No universality class analysis determining whether they belong to the same or different universality classes.

## Implications

If the AF and NGFP are the same point (or connected): QG+F and AS are the same theory at different approximation levels (see `swy-two-fixed-points.md` for the "perturbative sector" hypothesis). If genuinely distinct: they are competing theories that could in principle be distinguished observationally (see `../cross-cutting/qgf-vs-as-cmb-discrimination.md`).

The 4D critical surface of the NGFP (Falls et al. 2023) matching quadratic gravity's 4-coupling count is suggestive but not conclusive — it could indicate shared UV physics or merely coincidence.
