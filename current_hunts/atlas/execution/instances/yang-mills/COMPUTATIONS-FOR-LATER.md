# Computation Registry

Computations identified during explorations that would significantly advance the mission.
Maintained by the strategizer, read by the missionary and future strategizers.

## From Exploration 001 (Balaban RG Program)

### 1. Contraction analysis of 4D YM RG map
- **What:** Numerically study whether Balaban's RG transformation is contractive (in appropriate norms) for the marginally renormalizable 4D case
- **Why it matters:** Would inform Gap 2 (uniqueness of the continuum limit). If the RG map is contractive, uniqueness follows.
- **What it would resolve:** Whether the Tier 1 gap of proving uniqueness is within reach via Balaban's framework
- **Source:** Exploration 001
- **Difficulty:** Moderate — ~100-line numpy/scipy script once the map is formalized, but extracting the explicit RG map from Balaban's papers [11]-[12] is the hard part
- **Key references:** Balaban papers [11]-[12] on effective actions and β-functions in 4D

### 2. Wilson loop RG tracking
- **What:** Formalize how a Wilson loop observable transforms under one Balaban RG step, and estimate error bounds
- **Why it matters:** Would inform Gap 1 (extending UV stability to control gauge-invariant observables)
- **What it would resolve:** Whether Balaban's framework can be extended to track observables, not just the partition function
- **Source:** Exploration 001
- **Difficulty:** Conceptual — defining the right framework is the challenge; the computation itself would be moderate
- **Key references:** Balaban papers [6], [10], [11]

## From Exploration 002 (Constructive QFT 2D/3D vs 4D)

### 3. Numerical verification of Balaban's bounds on small lattices
- **What:** Implement block-spin RG for SU(2) lattice gauge theory on small lattices (e.g., 8⁴) and check whether Balaban's UV stability bounds are tight or have room for improvement
- **Why it matters:** Would reveal if there's unexploited room in the bounds that could simplify the Tier 1 gaps
- **What it would resolve:** Whether tighter bounds might make observable control (Gap 1) or uniqueness (Gap 2) more accessible
- **Source:** Exploration 002
- **Difficulty:** Moderate (100-200 lines of code for the RG step, but conceptual understanding of Balaban's setup needed)

### 4. Non-perturbative beta function comparison
- **What:** Compare perturbative beta function with Balaban-style block-spin beta function on the lattice
- **Why it matters:** Could illuminate how perturbative asymptotic freedom connects to non-perturbative UV stability
- **What it would resolve:** Whether the asymptotic freedom mechanism is fully captured by Balaban's framework
- **Source:** Exploration 002
- **Difficulty:** Moderate; would require lattice gauge theory simulation code
