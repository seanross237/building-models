# Exploration 004: Can Cost Function Constraints Select Ghost-Free Higher-Derivative Gravity?

## Goal

Investigate whether cost function constraints in the Pedraza et al. (2023) complexity-geometry framework can select ghost-free higher-derivative gravity — specifically QG+F (quadratic gravity with fakeon quantization). This is a technical investigation.

## Status: COMPLETE

---

## 1. The Pedraza et al. Construction — Deep Dive

### 1.1 Paper Identification and Context

The key paper is **"Gravitation from optimized computation: Einstein and beyond"** by Rafael Carrasco, Juan F. Pedraza, Andrew Svesko, and Zachary Weller-Davies (arXiv: 2306.08503, JHEP 09 (2023) 167).

This paper introduces the **"spacetime complexity" principle**: gravitational physics emerges from spacetime seeking to optimize the computational cost of its quantum dynamics. The key claim is that Einstein's equations are equivalent to requiring that the CV (Complexity=Volume) complexity responds consistently to state perturbations.

### 1.2 The CV Complexity Functional

The core functional is:

```
C_gen = (1/(G_N L)) ∫_Σ d^(D-1)σ √h F₁(g_μν, Φ, X^μ)
```

where:
- Σ is a codimension-one extremal hypersurface in the bulk
- h is the induced metric on Σ
- F₁ is a scalar function (the **cost function**) that depends on the bulk metric, dilaton, and embedding coordinates
- The surface Σ is determined by extremizing a (potentially different) functional F₂
- G_N is Newton's constant, L is the AdS length scale

**The standard CV proposal** has F₁ = F₂ = 1 (or F₁ = Φ in 2D JT gravity), so it just computes the volume of the maximal slice.

### 1.3 How Einstein Equations Emerge

The mechanism works via the **covariant phase space formalism**:

1. Define a bulk observable W[g_μν, Φ] = the complexity functional evaluated on the extremal slice
2. The symplectic form relates bulk and boundary variations: Ω_bulk(δ_W, δ) = δW = Ω_bdy(δ_W, δ)
3. Requiring this to hold for ALL variations δ **imposes the linearized Einstein equations** around pure AdS

The bidirectional coupling means:
- **Forward**: Given Einstein equations → complexity has the right first law
- **Reverse**: Assuming the CV proposal and requiring the first law → Einstein equations

This was first shown at linearized level by Pedraza, Russo, Svesko, and Weller-Davies in "Sewing spacetime with Lorentzian threads" (2021) and "Computing spacetime" (2022).

### 1.4 How Modified Cost Functions Yield Higher-Derivative Gravity

**This is the key mechanism for our question.** The paper modifies the cost function F₁ to include curvature-dependent terms:

```
F₁(r) = 1 + λ L⁴ × (curvature scalar)
```

where the curvature scalar can be:
- **Ricci scalar squared**: R_μν R^μν
- **Riemann tensor squared**: R_μνρσ R^μνρσ
- **Weyl tensor squared**: C_μνρσ C^μνρσ

The parameter λ is a coupling constant controlling the strength of the higher-derivative correction.

**The mapping**: different cost function modifications correspond to different higher-derivative gravitational theories:
- F₁ ∝ 1 + λ R_μν R^μν → gravity with R_μν R^μν correction
- F₁ ∝ 1 + λ C_μνρσ² → gravity with Weyl-squared correction
- F₁ ∝ 1 + λ R_μνρσ² → gravity with Gauss-Bonnet-type correction

**Important**: This is implemented via **corrections to the CV dictionary** — i.e., when the bulk gravitational theory includes higher-derivative terms, the complexity functional must be modified (from pure volume) to include curvature-dependent corrections to match the generalized gravitational equations.

### 1.5 The "Complexity = Anything" Generalization

A recent paper (arXiv: 2503.20943, March 2025) by the same group maps out "the landscape of complexity measures in 2D gravity." Key findings:

- There is an **infinite class of equally viable candidate observables** (the "complexity=anything" framework)
- Different bulk functionals correspond to different "elementary gate sets and cost functions" in the dual quantum circuit
- The cost function F₁ need not equal the extremizing functional F₂
- Complexity is inherently **scheme-dependent** — it depends on the choice of basis and gate costs

### 1.6 Constraints on the Cost Function

From the landscape paper, valid complexity measures must satisfy:

1. **Linear growth at late times**: The effective potential U(r) = -a(r)²N(r) must have at least one local maximum interior to the event horizon
2. **Switchback effect**: Additive complexity for shockwave geometries
3. **Diffeomorphism invariance**: F must be a scalar under coordinate transformations
4. **Physical well-definedness**: a(r) = F evaluated on Σ must remain finite at the horizon (or diverge mildly)
5. **Positivity**: The effective potential cannot be globally negative

### 1.7 The 2D Dilaton Gravity Proof

The full proof of the spacetime complexity principle works in 2D dilaton gravity (including JT gravity), where:
- The problem of semi-classical backreaction can be solved exactly
- The functional W = ∫ dσ √h Φ (volume × dilaton) reproduces the correct equations
- Higher-derivative corrections are incorporated through F₁ depending on dilaton derivatives

---

## 2. QG+F: Quadratic Gravity with Fakeon Quantization

### 2.1 The Quadratic Gravity Lagrangian

The most general quadratic-curvature gravity action in 4D is:

```
S_QG = ∫d⁴x √(-g) [ M_P²/2 R - 1/(2f₂²) C_μνρσ C^μνρσ + 1/(3f₀²) R² ]
```

Equivalently, using the relation C² = R_μνρσ² - 2R_μν² + R²/3 (up to Gauss-Bonnet topological term):

```
S_QG = ∫d⁴x √(-g) [ M²/2 R + α R² + β R_μν R^μν ]
```

where M = M_P is the Planck mass and α, β are coupling constants. The Gauss-Bonnet combination G = R² - 4R_μν² + R_μνρσ² is topological in 4D and doesn't contribute to the equations of motion.

### 2.2 The Propagator Structure

The linearized graviton propagator in quadratic gravity decomposes into spin-2 and spin-0 sectors:

**Spin-2 sector:**
```
D^(2)(k) = P^(2) × [ 1/k² - 1/(k² - m₂²) ] / M²
```

**Spin-0 sector:**
```
D^(0)(k) = P^(0_s) × [ 1/k² + 1/(k² - m₀²) ] / (2M²)
```

where P^(2) and P^(0_s) are the spin-2 and spin-0 projection operators.

**Key mass relations:**
- **Spin-2 mass**: m₂² = f₂² M² (from the Weyl-squared term)
- **Spin-0 mass**: m₀² = f₀² M² (from the R² term)

### 2.3 The Ghost Problem

The spin-2 propagator has the form 1/k² - 1/(k² - m₂²). The second term has **negative residue** — it's a ghost. In Stelle's original theory, this ghost:
- Has a wrong-sign kinetic term
- Leads to an Ostrogradsky instability (Hamiltonian unbounded from below)
- Violates unitarity when treated as a physical particle

### 2.4 The Fakeon Prescription (Anselmi-Piva)

Anselmi and Piva's resolution (2017-2018): quantize the ghost pole using the **fakeon prescription** instead of the standard Feynman prescription.

**Standard Feynman prescription**: 1/(p² - m² + iε) → physical particle that can appear as asymptotic state

**Fakeon prescription**: alternative contour in complex plane → purely virtual particle that:
- Circulates in loops (preserving renormalizability)
- Cannot appear as external on-shell state at any energy
- Maintains S-matrix unitarity in the Fock subspace with fakeons removed

**The particle spectrum of QG+F:**
1. **Massless graviton** (spin-2): standard pole, Feynman prescription → physical
2. **Massive spin-2 fakeon** χ_μν: ghost pole, fakeon prescription → purely virtual
3. **Massive spin-0** φ: can be either physical (Feynman) or fakeon, depending on the model

**Key results:**
- The theory is **UV-complete and renormalizable** (power counting: propagators fall as 1/k⁴ at high energies)
- The theory is **unitary** (S-matrix cutting equations satisfied when ghost is quantized as fakeon)
- It is the **unique** perturbatively UV-complete quantum gravity within {Lorentz invariance, diffeomorphism invariance, renormalizability, unitarity}
- Microcausality is violated at energies above the fakeon mass, but this is a prediction, not a pathology

### 2.5 The Weyl-Squared vs R² Mapping

This decomposition is critical:
- **C_μνρσ C^μνρσ** (Weyl-squared) → controls the massive spin-2 sector (the ghost/fakeon)
- **R²** → controls the massive spin-0 sector
- The Gauss-Bonnet combination is topological → no dynamical content in 4D

So the question of which cost function modifications produce which gravitational corrections maps directly to the particle content:
- Cost function ~ C² → spin-2 fakeon physics
- Cost function ~ R² → spin-0 physics

---

## 3. The Key Question: Can Cost Function Constraints Select Ghost-Free Gravity?

### 3.1 The Logical Chain

The question has several sub-questions:

**Q1**: In the Pedraza framework, is the cost function freely choosable, or are there constraints?
**Q2**: If constrained, do the constraints distinguish between different higher-derivative gravity theories?
**Q3**: Specifically, can the constraints select ghost-free theories (QG+F) over ghost-full ones (Stelle gravity)?

### 3.2 Analysis of Q1: Cost Function Freedom

From the literature, the answer is: **the cost function is largely free**.

The "complexity = anything" framework (Belin et al. 2021, Jorstad et al. 2023, Pedraza et al. 2025) explicitly shows:
- There is an infinite class of equally valid complexity functionals
- Different choices correspond to different "gate sets" in the dual quantum circuit
- Complexity is inherently scheme-dependent

The constraints that DO exist are:
1. Diffeomorphism invariance (must be a scalar)
2. Late-time linear growth (effective potential must have interior maximum)
3. Switchback effect
4. Physical well-definedness (finite at horizons)

**These are IR/macroscopic constraints.** They constrain the qualitative behavior of complexity (growth rate, large-time asymptotics) but not the UV structure that would determine the particle content.

### 3.3 Analysis of Q2: Do Constraints Distinguish Theories?

The constraints in Section 3.2 do distinguish somewhat — for example, in Gauss-Bonnet gravity with D ≥ 5, there are restricted ranges of the coupling constant λ that allow valid complexity observables. But in 4D (which is what we care about for QG+F), the Gauss-Bonnet term is topological and the constraints are less restrictive.

**Critical observation**: The mapping between cost functions and gravitational theories goes in the WRONG DIRECTION for our purposes:

- **Pedraza's framework**: Given a bulk gravitational theory (with or without higher derivatives), what is the correct complexity functional?
- **Our question**: Given constraints on the complexity functional, can we DERIVE the bulk gravitational theory?

The framework is designed to answer the first question, not the second. The "reverse" direction (complexity → gravity) works for the Einstein equations because the CV proposal is a specific, fixed choice. But for higher-derivative gravity, the complexity functional must be MODIFIED to match the gravitational theory — meaning the cost function ENCODES the gravitational theory rather than SELECTING it.

### 3.4 Analysis of Q3: Ghost Freedom and Cost Functions

Now the critical question: even though the cost function is largely free, can some structural property of the cost function (e.g., positive-definiteness) automatically enforce ghost-freedom in the emergent gravitational theory?

#### 3.4.1 The Positive-Definiteness Argument

There IS a suggestive analogy. In the Nielsen complexity framework:

- The **penalty factor matrix** I_IJ defines the cost function: F² = Y^I I_IJ Y^J
- For the complexity to be well-defined, this matrix must be **symmetric positive-definite** (or at least have definite signature matching the group structure)
- When the penalty factors push the metric into an **indefinite** regime, the complexity measure becomes physically meaningless — this is the "swampland" of complexity (Flory et al. 2026, JHEP 02)
- Only penalty factors that yield a **positive-definite metric on the state space** give a viable complexity interpretation

This creates a **landscape/swampland** structure: only certain cost functions are physically viable.

**The tempting analogy**: The positive-definiteness requirement for the complexity metric might map, through the holographic dictionary, to positive spectral weight / ghost-freedom in the bulk gravitational theory. Ghosts (negative-residue poles) would correspond to indefinite complexity metrics.

#### 3.4.2 Why the Analogy Fails (or at Least is Incomplete)

However, there are several problems with this reasoning:

**Problem 1: Level mismatch.** The Nielsen complexity geometry lives on the boundary (the group of unitaries in the CFT), while the ghost/no-ghost question is about the bulk gravitational propagator. The holographic dictionary does not provide a direct mapping between the signature of the complexity metric on the boundary and the sign of propagator residues in the bulk.

**Problem 2: The cost function is a different object than the gravitational Lagrangian.** In the Pedraza framework:
- The cost function F₁ appears in the complexity functional C_gen = ∫ √h F₁
- The gravitational Lagrangian appears in the bulk action S = ∫ √g L_grav
- These are related but NOT the same object. The cost function modifies the complexity observable; the Lagrangian determines the dynamics. The constraint "F₁ must produce a well-defined complexity" is NOT the same as "L_grav must be ghost-free."

**Problem 3: Complexity = anything allows too much freedom.** Even if we require positive-definiteness of the complexity metric, the "complexity = anything" framework shows there are infinitely many valid choices. Different choices of F₁ correspond to different gate sets, not different gravitational theories. The gravitational theory is determined by the BULK dynamics, not by the complexity observable.

**Problem 4: The Feynman vs. fakeon distinction is a quantization choice, not a Lagrangian choice.** The QG+F Lagrangian is IDENTICAL to Stelle's Lagrangian: L = R + αC² + βR². The difference is in how one quantizes the ghost pole. The cost function (which depends on the classical geometry) cannot distinguish between Stelle quantization and fakeon quantization, because the classical geometries are the same.

This is perhaps the most devastating observation: **the cost function is a classical geometric object, while the fakeon prescription is a quantum mechanical choice about how to handle propagator poles.** The cost function cannot "see" whether the ghost pole is quantized with Feynman or fakeon boundary conditions.

#### 3.4.3 What Boundary CFT Unitarity CAN Do

While the cost function itself can't select QG+F, there is a separate (and well-established) mechanism where **boundary CFT unitarity** constrains bulk higher-derivative gravity couplings:

1. **Conformal collider bounds** (Hofman-Maldacena 2008, Buchel et al. 2010): Positivity of energy flux in the CFT constrains the ratio of central charges a/c, which in turn bounds the Gauss-Bonnet and Weyl-squared coupling constants in the bulk.

2. **Causality constraints**: Requiring that the bulk respects causality (no superluminal propagation) also constrains higher-derivative couplings.

3. **Swampland conditions from CFT** (Caron-Huot et al. 2022): The conformal bootstrap imposes positivity, monotonicity, and log-convexity conditions on higher-derivative couplings.

These constraints provide **sign and magnitude bounds** on the couplings α and β in the higher-derivative Lagrangian. They can, for example, constrain:
- The sign of the Gauss-Bonnet coupling (in D ≥ 5)
- The allowed range of α/β ratios
- The magnitude of higher-derivative corrections (they must be parametrically small in the large-N expansion)

**However**, these constraints:
- Do NOT select a unique theory (they give ranges, not specific values)
- Do NOT distinguish between Feynman and fakeon quantization (they constrain the classical Lagrangian, not the quantization scheme)
- Apply only in the holographic (large-N) regime, where higher-derivative terms are treated perturbatively

---

## 4. Concrete Derivation Attempt

### 4.1 Setup

Can we derive the QG+F Lagrangian from cost function constraints? Let me attempt the most optimistic version of this.

**Starting point**: The generalized CV complexity functional:
```
C_gen = (1/(G_N L)) ∫_Σ d^(D-1)σ √h F₁(g_μν, X^μ)
```

**Assumption 1**: F₁ must be a diffeomorphism-invariant scalar built from the ambient metric and curvature evaluated on Σ. In 4D, the most general form to quadratic order in curvature:
```
F₁ = 1 + a₁ L² R + a₂ L⁴ R² + a₃ L⁴ R_μν R^μν + a₄ L⁴ C_μνρσ C^μνρσ + ...
```

**Assumption 2**: Apply the "spacetime complexity" principle in reverse — requiring δC_gen = δW (first law of complexity) for all perturbations imposes equations of motion on the bulk metric.

**What equations do we get?** At zeroth order in curvature corrections (a_i = 0), we get linearized Einstein equations. At first order, we would get Einstein + higher-derivative corrections. The specific corrections depend on the a_i coefficients.

### 4.2 The Problem

The mapping is: different values of (a₁, a₂, a₃, a₄) → different gravitational theories. But:

1. **The a_i are free parameters.** Nothing in the complexity framework fixes them to specific values. They represent the choice of complexity scheme (which gate set / cost function to use).

2. **The "reverse" direction doesn't uniquely determine the theory.** The Pedraza framework shows that, GIVEN a gravitational theory, there exists a compatible cost function. But many different cost functions can be compatible with many different gravitational theories.

3. **Even if we impose all known complexity constraints** (linear growth, switchback effect, positivity, diffeomorphism invariance), these constrain the qualitative behavior of C_gen but not the specific values of a_i.

### 4.3 The Spectral Weight / Positivity Argument (Strongest Available)

The best argument one could construct would be:

1. The Nielsen complexity geometry on the boundary requires a positive-definite penalty matrix I_IJ for the complexity to be well-defined.
2. Via AdS/CFT, the boundary complexity metric encodes information about the bulk geometry.
3. A bulk gravitational theory with ghosts would, through the holographic dictionary, induce negative eigenvalues in the boundary complexity metric.
4. Therefore, requiring positive-definite complexity → requiring ghost-free bulk gravity → QG+F.

**Assessment**: Step 3 is the weak link. There is currently **no proof** that bulk ghosts induce indefinite boundary complexity metrics. The known relationships between bulk and boundary are:
- The volume of the maximal slice ↔ state complexity (CV duality)
- The bulk equations of motion ↔ the first law of complexity
- The bulk central charges (a, c) ↔ boundary conformal anomaly coefficients

None of these provide a direct mapping from bulk propagator pole structure to boundary complexity metric signature.

### 4.4 What WOULD Be Needed

For cost function constraints to select QG+F, one would need to establish:

1. **A UV-sensitive complexity constraint**: Something that constrains not just the long-distance behavior of complexity (growth rate, etc.) but the short-distance/high-energy structure. This might come from requiring that complexity be well-defined for all states, including those at arbitrarily high energies.

2. **A holographic propagator-complexity dictionary**: A precise mapping between the residues of bulk propagator poles and properties of the boundary complexity metric. This dictionary does not currently exist.

3. **A quantization-scheme-sensitive observable**: Something on the boundary that distinguishes between Feynman and fakeon quantization in the bulk. This would be novel — most holographic observables are determined by the classical bulk geometry, which is the same for both quantization schemes.

---

## 5. Assessment and Conclusions

### 5.1 Main Finding: Cost Function Constraints Do NOT Select QG+F

The investigation reveals a clear negative result: **cost function constraints in the Pedraza et al. framework cannot, as currently formulated, select ghost-free higher-derivative gravity (QG+F) or any specific gravitational theory beyond Einstein gravity.**

The reasons are:

1. **Too much freedom**: The "complexity = anything" framework demonstrates an infinite class of valid complexity functionals. The constraints (linear growth, switchback, diffeomorphism invariance, positivity) are necessary but far from sufficient to select a unique theory.

2. **Wrong direction of inference**: The framework maps FROM bulk gravity TO complexity (given a gravitational theory, find the matching complexity functional). The reverse mapping is degenerate — many cost functions compatible with many theories.

3. **Classical vs. quantum distinction**: The cost function is a classical geometric object. The fakeon prescription (which is the key innovation of QG+F) is a quantum mechanical choice about propagator contours. No classical cost function can distinguish between Stelle gravity and QG+F, because their classical Lagrangians are identical.

4. **IR vs. UV constraints**: The known complexity constraints (linear growth, switchback) are infrared/macroscopic properties. Ghost-freedom is an ultraviolet/microscopic property. There is no established mapping between the two.

### 5.2 Partial Success: Identifying the Gap

The investigation does identify what WOULD be needed:

- **A UV-sensitive complexity constraint** that probes short-distance structure
- **A holographic propagator-complexity dictionary** mapping bulk pole residues to boundary complexity metric properties
- **A quantization-sensitive boundary observable** distinguishing Feynman from fakeon in the bulk
- **A positive-definiteness theorem** linking complexity metric definiteness to bulk ghost-freedom

The most promising lead is the **landscape/swampland structure** of CFT complexity penalty factors (Flory et al. 2026). The finding that only positive-definite penalty factors give viable complexity measures is structurally analogous to ghost-freedom. If a precise holographic dictionary could be established mapping penalty factor positive-definiteness to bulk propagator positive spectral weight, this could provide the link.

### 5.3 Alternative Routes from Holography

While cost function constraints don't work, there ARE holographic mechanisms that constrain bulk higher-derivative gravity:

1. **CFT unitarity / conformal collider bounds**: Constrain the sign and magnitude of higher-derivative couplings (but give ranges, not unique values).

2. **Causality constraints**: Bulk causality ↔ boundary causality provides bounds on Gauss-Bonnet and Weyl-squared couplings.

3. **Conformal bootstrap / swampland conditions**: Positivity, monotonicity, log-convexity of couplings from bootstrap axioms.

These provide necessary conditions on the gravitational theory but do not uniquely select QG+F.

### 5.4 The Fundamental Obstacle

The deepest reason cost function constraints can't select QG+F is:

**The SCG framework (stochastic computational gravity) maps computational cost → spacetime geometry → gravitational dynamics. But the ghost problem and its resolution (the fakeon prescription) live at the level of the QUANTUM THEORY, not the classical geometry.** The cost function determines the classical geometry; the fakeon prescription determines how to quantize excitations around that geometry. These are distinct layers of structure, and the cost function can't reach the quantization layer.

To select QG+F from a computational/complexity framework, one would need to go beyond classical cost functions to something like a **quantum cost function** that directly constrains the propagator structure — i.e., a constraint on how quantum fluctuations around the optimal geometry are treated. This would be a significant extension of the current framework.

### 5.5 A Possible Way Forward

If one wanted to pursue this line further, the most promising approach would be:

1. **Start from the Nielsen complexity geometry** on the boundary CFT
2. **Require** that the complexity metric on the space of states be positive-definite (the "landscape" condition from Flory et al.)
3. **Show** that this positive-definiteness, through the holographic dictionary, constrains the bulk propagator to have positive spectral weight for all physical poles
4. **Show** that positive spectral weight for all physical poles, combined with renormalizability, uniquely selects QG+F

Steps 3 and 4 are both open problems. Step 4 is essentially the content of the Anselmi-Piva uniqueness theorem (which shows that QG+F is the unique theory satisfying these conditions). Step 3 would be genuinely new and would require establishing a new entry in the holographic dictionary.

---

## References

- Carrasco, Pedraza, Svesko, Weller-Davies, "Gravitation from optimized computation: Einstein and beyond," JHEP 09 (2023) 167. arXiv: 2306.08503.
- Pedraza, Russo, Svesko, Weller-Davies, "Computing spacetime," Int. J. Mod. Phys. D 31 (2022) 2242010. arXiv: 2205.05705.
- Pedraza, Russo, Svesko, Weller-Davies, "Sewing spacetime with Lorentzian threads," arXiv: 2106.12585.
- Jorstad, Myers, Ruan, "The landscape of complexity measures in 2D gravity," arXiv: 2503.20943 (2025).
- Jorstad, Myers, Ruan, "Generalized Volume Complexity in Gauss-Bonnet Gravity," Phys. Rev. D 108 (2023) 126018. arXiv: 2307.12530.
- Anselmi, "On the quantum field theory of the gravitational interactions," JHEP 06 (2017) 086. arXiv: 1704.07728.
- Anselmi, Piva, "The ultraviolet behavior of quantum gravity," JHEP 05 (2018) 027. arXiv: 1803.07777.
- Anselmi, Piva, "Quantum gravity, fakeons and microcausality," JHEP 11 (2018) 021. arXiv: 1806.03605.
- Salvio, "Quadratic gravity," Frontiers in Physics 6 (2018) 77. arXiv: 1804.09944.
- Stelle, "Renormalization of Higher Derivative Quantum Gravity," Phys. Rev. D 16 (1977) 953.
- Flory et al., "CFT complexity and penalty factors," JHEP 02 (2026) 247. arXiv: 2507.22118.
- Buchel, Myers, Sinha, "Beyond η/s = 1/4π," JHEP 03 (2009) 084. arXiv: 0812.2521.
- Buchel et al., "Causality constraints in AdS/CFT from conformal collider physics and Gauss-Bonnet gravity," JHEP 04 (2010) 007. arXiv: 0911.3160.
- Caron-Huot et al., "Swampland conditions for higher derivative couplings from CFT," JHEP 01 (2022) 176.
