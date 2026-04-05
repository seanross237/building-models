---
topic: Prior art search — classicality budget novelty assessment
confidence: verified
date: 2026-03-27
source: "classicality-budget strategy-001 exploration-003"
---

## Verdict: PARTIALLY KNOWN (Novel Synthesis)

The structural form of the bound (redundancy <= total capacity / per-fact entropy) exists in the literature. The physical content (connecting this to the Bekenstein bound on a spatial region) does not.

## Closest Existing Result: Tank (2025)

Tank (2025) "Functional Information in Quantum Darwinism" (arXiv:2509.17775) derives:

> R_delta <= N * log_2(d_e) / ((1 - delta) * H_S)

where N = number of environment subenvironments, d_e = per-site Hilbert space dimension, H_S = pointer entropy, delta = information deficit threshold.

### Structural Comparison

| Feature | Tank (2025) | Classicality Budget |
|---------|-------------|---------------------|
| Numerator | N * log_2(d_e) = total environment entropy capacity | S_max = Bekenstein bound |
| Denominator | (1 - delta) * H_S = pointer entropy with deficit | S_T = pointer entropy |
| Physical scope | Quantum information theory (Hilbert space) | Gravitational/fundamental physics |
| What bounds the total? | Environment Hilbert space dimension | Spacetime geometry |

**Key insight:** The classicality budget is obtained from Tank's bound by replacing the abstract N * log_2(d_e) with the physical S_max (Bekenstein bound). The novelty is precisely this substitution — connecting abstract information-theoretic capacity to a concrete gravitational bound.

**Note:** Tank (2025) itself is very recent (September 2025). The structural form R ~ N/f was implicit in quantum Darwinism since Zurek (2009); Tank made it explicit as a capacity-limited bound; the classicality budget adds the physical grounding via Bekenstein.

## What Is Novel

1. The connection to the Bekenstein bound — identifying that N * log_2(d_e) is physically bounded above by S_max = A / (4 * G * hbar)
2. The conceptual interpretation as a "classicality budget" — the richness-objectivity trade-off constrained by spacetime geometry
3. All physical implications (Planck-scale breakdown, specific system computations, black hole physics connections)
4. The bridging of two previously unconnected research communities (see below)

## Two Disconnected Research Communities

After 29 distinct searches, 17 papers examined, and 8 author groups checked: **zero papers** cite both quantum Darwinism and Bekenstein/holographic entropy bounds in connection with this question.

- **QD community** (Zurek, Riedel, Zwolak, Brandao, Korbicz, Le, Olaya-Castro, Tank): Bound redundancy by abstract Hilbert space dimension of the environment. Never ask "what if the environment's capacity is itself bounded by spacetime geometry?"
- **Entropy bounds community** (Bekenstein, Bousso, Hayden, Wall, Maldacena): Study fundamental entropy limits from GR/QG. Never ask "what does this imply for quantum Darwinism redundancy?"

This is the hallmark of an interdisciplinary insight: obvious in retrospect, invisible from within either field.

## Key Conceptual Neighbors

- **Bousso (2017)** — Universal limit on communication (channel capacity ~ E * Delta_t / hbar). Bounds rate of information transfer, not total redundant information in a region. Related but distinct.
- **Hayden & Wang (2025)** — "What exactly does Bekenstein bound?" (Quantum 9, 1664). Rigorously shows Bekenstein constrains classical bits and qubits when encoder and decoder are spatially restricted. Does NOT connect to quantum Darwinism.
- **Zwolak et al. (2009)** — Environment "haziness" suppresses redundancy by factor (1 - h). Closest in spirit (connects environment entropy to redundancy), but operates per-qubit, not at the level of total regional entropy bounds.
- **QEC bounds** — Quantum Singleton/Hamming bounds structurally similar (more redundancy = less information), but not connected to Bekenstein-type entropy bounds.

## Comprehensive Negative Search: Key Authors

All major QD authors checked — **none** connect redundancy to external entropy bounds:
- Zurek (2003, 2009, 2022, 2025): R ~ N/f only, no Bekenstein mention
- Blume-Kohout & Zurek (2005, 2006): Numerical R values, no general bound
- Riedel, Zurek, Zwolak (2010, 2012, 2017): R conditions, no entropy bound
- Brandao, Piani, Horodecki (2015): Genericity proof, qualitative not quantitative
- Korbicz (2014, 2021): SBS framework, no entropy bound
- Bousso (2014, 2017): Channel capacity, different quantity
- Knott et al. (2018): Infinite-dim genericity, no entropy bound

## Search Audit

29 queries, 17 papers examined, 8 author groups checked. Full search log in exploration-003 report. Confidence: HIGH that the exact formula R_delta <= S_max / S_T - 1 has not been published. MEDIUM-HIGH that the structural form was implicit but only made explicit by Tank (2025).
