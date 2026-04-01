# Exploration 002: Fixed Point Compatibility — Does the AF Fixed Point Connect to the Reuter NGFP?

## Goal
Determine what the published literature says about whether the asymptotically free (AF) fixed point of quadratic gravity connects to the non-Gaussian fixed point (NGFP, Reuter) via RG flow. Give a verdict: SUPPORTS / FALSIFIES / INCONCLUSIVE.

## Status: IN PROGRESS — final searches underway

---

## 1. The Central Paper: SWY (2022) — arXiv:2111.04696

Sen, Wetterich, and Yamada, "Asymptotic freedom and safety in quantum gravity," JHEP 03 (2022) 130.

### Key Findings:
- Compute non-perturbative flow equations for quantum gravity in fourth-order derivative expansion using gauge-invariant functional flow equations.
- **Two distinct fixed points found** in their truncation:
  1. **AF fixed point**: Corresponds to asymptotically free higher-derivative gravity (Stelle-type). The Weyl-squared coupling f_2 is asymptotically free.
  2. **NGFP**: Extension of the Reuter asymptotically safe fixed point from the Einstein-Hilbert truncation to include higher-derivative terms.
- Critical exponents computed for both — they differ, confirming these are genuinely different fixed points.
- **Critical sentence**: "There may exist a critical trajectory between the two fixed points, starting in the extreme ultraviolet from asymptotic freedom."
- The hedged language ("may exist") indicates the trajectory is plausible from their flow equations but **not definitively established**.
- They present AF as an **alternative** to AS, not as the same thing.

### Significance:
This is the most important paper for our question. It simultaneously finds BOTH fixed points in the same truncation and explicitly raises the question of a connecting trajectory. The answer is: **plausible but not proven**.

---

## 2. SWY Follow-up (2023) — arXiv:2211.05508

Sen, Wetterich, and Yamada, "Scaling solutions for asymptotically free quantum gravity," JHEP 02 (2023) 054.

### Key Findings:
- Compute **scaling solutions** connecting the AF UV fixed point to the non-perturbative IR region.
- These scaling solutions show that the AF fixed point can produce viable low-energy physics (Einstein gravity in the IR).
- "If the proposed scaling solution is confirmed beyond our approximations, asymptotic freedom is a viable alternative to asymptotic safety for quantum gravity."
- Focus: Can AF reach Einstein gravity in the IR? Answer: Yes, via scaling solutions.
- **Does NOT specifically address** whether the AF trajectory passes through or near the NGFP on its way to the IR.

### Significance:
Establishes that AF has its own viable IR completion. The AF → IR trajectory exists. But whether it goes *through* the NGFP remains unaddressed.

---

## 3. The Codello-Percacci Result (2006) — PRL 97, 221301

Codello and Percacci, "Fixed Points of Higher-Derivative Gravity."

### Key Finding:
- Recalculated beta functions of higher-derivative gravity using the one-loop approximation to an **exact** (non-perturbative) RG equation.
- **Crucial result**: "The theory appears to be **asymptotically safe at a non-Gaussian fixed point rather than perturbatively renormalizable and asymptotically free**."
- When non-perturbative effects are included via the functional RG, what was previously identified as the perturbative AF Gaussian fixed point gets replaced by (or deformed into) an NGFP.

### Significance for our question:
This is highly relevant. It suggests that the AF "Gaussian" fixed point of perturbative higher-derivative gravity and the NGFP of asymptotic safety may be **the same fixed point seen at different levels of approximation**:
- Perturbatively: looks like AF at a Gaussian FP (Stelle 1977)
- Non-perturbatively: looks like AS at an NGFP (Reuter 1998, Codello-Percacci 2006)

If true, the question of "connecting them via RG flow" is moot — they ARE the same point, just computed differently.

---

## 4. Niedermaier (2009, 2010) — PRL 103, 101303

Niedermaier, "Gravitational Fixed Points from Perturbation Theory."

### Key Finding:
- Found asymptotically safe fixed points using **perturbative** methods in higher-derivative gravity.
- Strictly positive fixed points for Newton's constant g_N and cosmological constant lambda.
- "The renormalization flow is asymptotically safe with respect to this fixed point."

### Significance:
Further evidence that perturbative analysis of higher-derivative gravity yields an asymptotically safe (not just asymptotically free) behavior, blurring the line between AF and AS interpretations.

---

## 5. Ohta-Percacci (2014) — CQG 31, 015024

Ohta and Percacci, "Higher Derivative Gravity and Asymptotic Safety in Diverse Dimensions."

### Key Finding:
- Derived one-loop beta functions for gravity with up to four derivatives.
- **Nontrivial UV fixed points found in all dimensions studied** (3, 4, near-4, 5, 6).
- Indication that a Weyl-invariant fixed point exists in four dimensions.

### Significance:
Confirms that higher-derivative gravity generically has nontrivial (non-Gaussian) UV fixed points, supporting the view that the perturbative AF fixed point is an approximation to a genuine NGFP.

---

## 6. Falls et al. (2023) — PRD 108, 026005

Falls, Kluth, Litim, "Fixed Points of Quantum Gravity and the Dimensionality of the UV Critical Surface."

### Key Finding:
- Study quantum gravity with polynomial Riemann tensor interactions using functional RG.
- The main NGFP ("Riemann fixed point") has a **four-dimensional UV critical surface**.
- Quantum-induced shifts turn classically marginal and irrelevant operators into relevant ones.
- Higher-dimensional interactions remain irrelevant with near-Gaussian scaling.
- Treats the NGFP and perturbative fixed points as **distinct** entities.

### Significance:
The 4D critical surface is interesting — it matches the number of couplings in quadratic gravity (f_2, f_0, G, Lambda). This is consistent with the NGFP being a non-perturbative version of the same physics.

---

## 7. Wikipedia / QQG Claim

Wikipedia on asymptotic safety states about QQG:
> "QQG, besides being renormalizable, has also been shown to feature a UV fixed point (even in the presence of realistic matter sectors). It can, therefore, be regarded as a **concrete realisation of asymptotic safety**."

This claim (sourced from Salvio and collaborators) treats the UV fixed point of QQG as an asymptotically safe fixed point — effectively identifying AF quadratic gravity with AS.

---

## 8. Flow Topology: What We Know

The flow structure in the full (f_2, f_0, G, Lambda) space:

1. **AF fixed point**: f_2 = 0 (Gaussian in f_2), perturbatively accessible. This is the Stelle UV fixed point.
2. **NGFP (Reuter)**: Non-zero values for all couplings. Non-perturbative, found via functional RG.
3. **GFP (Gaussian)**: All couplings zero. Corresponds to free field theory / classical GR limit.

Known flow structure:
- NGFP → GFP: The standard asymptotic safety trajectory. Well-established (Reuter 1998, many subsequent works).
- AF → IR: Scaling solutions exist connecting AF to Einstein gravity (SWY 2023).
- AF → NGFP: "May exist" as a critical trajectory (SWY 2022). Not definitively computed.
- NGFP and AF may be the same fixed point at different approximation levels (Codello-Percacci 2006).

---

## 9. Analysis: Two Competing Interpretations

### Interpretation A: Same Fixed Point, Different Approximations
- Codello-Percacci (2006): Non-perturbative RG shows the AF fixed point IS an NGFP.
- Niedermaier (2009): Perturbative methods also find AS behavior.
- QQG claim: The UV fixed point of quadratic gravity IS a realization of AS.
- **If true**: No connecting trajectory needed — they're the same point.

### Interpretation B: Distinct Fixed Points, Possible Connection
- SWY (2022): Finds TWO separate fixed points in the same truncation.
- They have different critical exponents and different numbers of relevant directions.
- A "critical trajectory" between them "may exist" but isn't proven.
- Falls et al. (2023): Treats them as distinct.
- **If true**: The connection question is open and important.

### Resolution:
The tension between these interpretations appears to be **truncation-dependent**. In the SWY truncation (gauge-invariant flow with all fourth-order terms), two fixed points are clearly resolved. In earlier truncations (Codello-Percacci, Einstein-Hilbert + R^2), only one NGFP is found, which may be the AF fixed point shifted by non-perturbative effects. The SWY result is more refined and should be given more weight.

---

## 10. Verdict: INCONCLUSIVE — with strong hints of connection

### Evidence FOR connection (AF → NGFP trajectory exists):
1. SWY (2022) explicitly states a critical trajectory "may exist" between the two FPs.
2. Both FPs flow to Einstein gravity in the IR — they share the same IR physics.
3. QQG is described as "a concrete realisation of asymptotic safety" (Salvio et al.).
4. The 4D critical surface of the NGFP (Falls et al.) matches the coupling count of quadratic gravity.

### Evidence AGAINST connection (or making it moot):
1. SWY finds DIFFERENT critical exponents — different universality classes.
2. Codello-Percacci suggest they may be the SAME fixed point, making "connection" the wrong question.
3. No paper has explicitly computed a flow trajectory AF → NGFP.
4. The SWY language is hedged ("may exist") — not established.

### What's missing from the literature:
- **No paper has explicitly computed an RG trajectory from the AF fixed point to the NGFP.** This is a genuine gap.
- The question of same-vs-different fixed points depends on the truncation used.
- No universality class analysis comparing critical exponents systematically between the two.
- No study of the separatrix structure in the full 4D coupling space that would definitively answer whether the two FPs are connected.

### Final Verdict: **INCONCLUSIVE**

The literature does NOT contain a definitive answer. The SWY (2022) paper comes closest, finding both FPs in the same truncation and conjecturing a critical trajectory, but does not prove it. Codello-Percacci (2006) raises the possibility that the question itself may be ill-posed if the two FPs are the same point at different approximation levels. The gap between these interpretations has not been closed.

**For the conjecture that QG+F and AS are the same theory:** This remains open. The most favorable reading is that the AF fixed point is a perturbative approximation to the NGFP, and they are related by non-perturbative corrections. But this is NOT established — it is a plausible conjecture, not a proven result.
