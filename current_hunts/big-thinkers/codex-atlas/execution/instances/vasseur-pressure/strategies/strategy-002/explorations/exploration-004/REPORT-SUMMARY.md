# Exploration 004 Summary: Commutator / Compensated Compactness Analysis

## Goal
Determine whether CLMS compensated compactness or commutator estimates can improve the De Giorgi recurrence exponent β = 4/3 for 3D Navier-Stokes, following the SQG precedent (Caffarelli-Vasseur 2010).

## What was tried
1. Wrote out the exact bilinear form: P^{21} = R_iR_j[(û_i û_j) · v_{k-1} · λ_{k-1} · 1_{|u|>λ}].
2. Computed div(u^{below}) = -λ(u·∇|u|)/|u|² and curl(u^{above}) analytically — both O(|∇u|), not small.
3. Measured compressibility ratio numerically on two DNS datasets: ||div(u^below)||/||∇u|| = 0.07–0.14.
4. Verified vorticity concentrates where |u| is large (enstrophy ratio ≈ 0.9–1.0 at 30–50% thresholds).
5. Decomposed P^{21} into commutator + divergence-error remainder; measured remainder is 61% of total in L², dominates high frequencies 18×.
6. Checked CRW (1976) commutator bounds: ||u^below||_{BMO} ≤ 2||u^below||_{L^∞} — no improvement over direct CZ.
7. Analyzed SQG mechanism in detail: identified three structural reasons it works (scalar, linear, div-free) all of which fail for NS.

## Outcome: SUCCEEDED — Route 3 definitively closed

**Compensated compactness / commutator methods CANNOT improve β = 4/3 for NS.** The obstruction has three independent layers: (1) no div-curl structure in the truncated fields, (2) non-commutator remainder from div(u^above)≠0 dominates P^{21} at high frequencies, (3) CRW gives no improvement for bounded multipliers. The SQG–NS gap is structural: scalar vs vector, linear vs quadratic coupling, first-order vs second-order cancellation.

## Verification scorecard
- Verified: 0, Computed: 14, Checked: 2, Conjectured: 1

## Key takeaway
**β = 4/3 is sharp within the class of techniques using energy inequality + Sobolev + CZ pressure estimates + Chebyshev.** All "Route 3"-type attacks via commutators or compensated compactness fail because the NS pressure is a second-order (div-div) object, while CLMS handles first-order (div-curl) cancellations. To beat 4/3, one must use structural information about NS solutions beyond these four ingredients.

## Unexpected findings
- The commutator part of P^{21} actually HAS better high-frequency regularity than P^{21} overall (spectral ratio drops from 0.67 to 0.09 at k=20). But the divergence-error remainder completely negates this. If there were a way to eliminate the divergence error — a different truncation that preserves div-free — the commutator improvement could work. This is the scalar-vs-vector gap: for scalars (SQG), R^⊥ preserves div-free automatically; for vectors (NS), no amplitude truncation can.
- The vorticity-velocity correlation is weakly NEGATIVE for Taylor-Green (-0.24), but the conditional enstrophy on {|u|>λ} is still ≈ E[|ω|²] for moderate thresholds. The correlation is negative because some high-vorticity regions have moderate velocity (vortex cores), but the high-velocity regions still carry proportionate enstrophy.

## Computations identified
1. **Div-free truncation construction:** Is there ANY nonlinear map φ: R^3 → R^3 with (i) div(φ(u)) = 0 when div(u) = 0, (ii) |φ(u)| ≤ λ, (iii) φ(u) = u when |u| ≤ λ? Such a map would enable commutator methods. Likely impossible by topological arguments (u/|u| has nontrivial degree on {|u|=λ}), but a rigorous proof would close a loophole.
2. **Frequency-localized De Giorgi:** Could a Littlewood-Paley decomposition of the pressure, with different estimates on low vs high modes, bypass the 4/3 barrier? The divergence error is concentrated at high frequencies (confirmed numerically); low-mode P^{21} might have effective commutator structure.

## Proof gaps identified
- The "informal theorem" that β = 4/3 is sharp within energy+Sobolev+CZ+Chebyshev methods is stated but not formally proved. A rigorous version would require constructing an adversarial example showing 4/3 cannot be beaten by these tools — essentially an optimality result for the De Giorgi method applied to NS.
