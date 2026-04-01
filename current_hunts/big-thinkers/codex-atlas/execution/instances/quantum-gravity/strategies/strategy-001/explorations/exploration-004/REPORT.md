# Exploration 004: Asymptotic Safety ↔ Quadratic Gravity — Same Theory?

## Goal

Investigate whether asymptotic safety (AS) and quadratic gravity with fakeon quantization (QG+F) are the same theory viewed from different perspectives, complementary approaches, or fundamentally distinct programs.

## Table of Contents

1. [Background: Two Programs](#1-background)
2. [Propagator Comparison: 1/p⁴ in the UV](#2-propagator-comparison)
3. [Fixed Point Structure vs. Asymptotic Freedom](#3-fixed-point-structure)
4. [RG Flow: Exact RG for Quadratic Gravity](#4-rg-flow)
5. [Ghost/Fakeon Issue in Asymptotic Safety](#5-ghost-fakeon-issue)
6. [Recent Results (2024-2026)](#6-recent-results)
7. [Spectral Dimension as Bridge](#7-spectral-dimension-bridge)
8. [Synthesis and Conclusion](#8-synthesis)

---

## 1. Background

### Quadratic Gravity + Fakeon (QG+F)

The Stelle action (1977) adds R² and C_μνρσ C^μνρσ terms to the Einstein-Hilbert action:

S = ∫d⁴x √g [ (1/16πG) R - (1/2f₂²) C_μνρσ C^μνρσ + (1/6f₀²) R² ]

This theory is:
- **Renormalizable** (power-counting, the only 4D QG that is perturbatively renormalizable)
- **Asymptotically free** in f₂ (Weyl² coupling) — Fradkin-Tseytlin 1982
- Contains a **massive spin-2 ghost** (Stelle ghost) with mass m₂ ~ f₂ M_Pl
- The **fakeon prescription** (Anselmi-Piva 2017-2018) quantizes the ghost as a "fake particle" that doesn't appear in the physical spectrum, restoring unitarity

### Asymptotic Safety (AS)

The Weinberg conjecture (1979) posits that gravity is non-perturbatively renormalizable via a UV fixed point. Key developments:
- **Reuter (1998):** Used the functional RG (Wetterass equation) to find evidence of a non-trivial UV fixed point for gravity
- **Fixed point properties:** g* ≠ 0, λ* ≠ 0 (dimensionless Newton's constant and cosmological constant)
- At the fixed point, the anomalous dimension η_N = -2, making the effective graviton propagator go as 1/p⁴
- **Spectral dimension** flows from d_s = 4 in IR to d_s = 2 in UV

---

## 2. Propagator Comparison: 1/p⁴ in the UV

### In Quadratic Gravity

The graviton propagator in quadratic gravity has the structure (schematically, in the spin-2 sector):

G(p²) = 1/p² - 1/(p² + m₂²)

where m₂ is the ghost mass. This can be rewritten as:

G(p²) = m₂² / [p²(p² + m₂²)]

At **high energies** (p² >> m₂²), this approaches:

G(p²) → 1/p⁴

The 1/p⁴ UV behavior is **explicit** — it comes from the fourth-derivative terms (C²) in the action. This is the reason the theory is renormalizable: propagators fall fast enough to tame UV divergences.

The critical sign structure: the residues of the graviton pole (at p²=0) and ghost pole (at p²=-m₂²) have **opposite signs**. This opposite sign is required for the 1/p⁴ UV behavior but is also what creates the ghost problem.

### In Asymptotic Safety

At the Reuter fixed point, the anomalous dimension of Newton's constant is η_N = -2 (in d=4). This modifies the graviton propagator through the running of Newton's constant:

G_N(k) → g*/k² (dimensionless g* is constant at fixed point)

The effective propagator becomes:

G(p²) ~ Z_N(p)/p² ~ 1/p^(2-η_N) = 1/p⁴

This is the **same UV behavior** but arising from a completely different mechanism — not from explicit R² terms in the action, but from the non-perturbative running of Newton's constant.

### Analysis: Same Result, Different Mechanism?

The crucial question is whether these are truly different mechanisms or the same physics described differently:

1. **In QG:** The 1/p⁴ comes from the tree-level propagator structure with explicit higher-derivative terms
2. **In AS:** The 1/p⁴ comes from the anomalous dimension η_N = -2 at the non-perturbative fixed point

**Key insight from Knorr et al. (2021):** When the graviton propagator in asymptotic safety is reconstructed non-perturbatively, the full momentum dependence reveals form factors that are effectively equivalent to higher-curvature terms. Specifically, the form factors quadratic in curvature can be extracted from the non-perturbative propagator, and these correspond to the R² and C² terms of quadratic gravity.

This suggests the two approaches give the **same effective UV physics** but describe it at different levels:
- QG describes it perturbatively with explicit higher-derivative operators
- AS describes it non-perturbatively through the running of the full effective action

**Verdict on propagator:** The UV propagators are functionally identical (both go as 1/p⁴), and recent work reconstructing propagators in AS explicitly finds the quadratic-curvature form factors. This is strong evidence for a deep connection.

---

## 3. Fixed Point Structure vs. Asymptotic Freedom

This is where the relationship becomes most technically interesting.

### The Problem at First Glance

Asymptotic safety and quadratic gravity appear to be in tension:
- **AS** requires a non-trivial UV fixed point (g* ≠ 0)
- **QG** is asymptotically free (coupling → 0 in UV, i.e., the Gaussian fixed point)

These seem contradictory — one says couplings go to a non-zero value, the other says they go to zero.

### Resolution: Multiple Couplings, Multiple Fixed Points

The resolution, clarified by **Sen, Wetterich, and Yamada (2022)** (JHEP 03 (2022) 130), is that the theory space has **multiple couplings** and the fixed-point structure is richer than either program alone suggests.

In a fourth-order derivative expansion of gravity, there are (at minimum) four dimensionless couplings:
- g = G_N k² (dimensionless Newton's constant)
- λ (cosmological constant in Planck units)
- ω (coefficient of R² / Weyl² term — related to f₂)
- σ (coefficient of R² / Ricci scalar squared — related to f₀)

**Key finding: TWO fixed points exist:**

1. **Asymptotically Free Fixed Point (AF-FP):**
   - ω* = 0, σ* = 0 (fourth-derivative couplings → 0, i.e., Gaussian in these)
   - g* ≠ 0, λ* ≠ 0 (Newton's constant has a non-trivial fixed point!)
   - This corresponds to **quadratic gravity** where f₂ and f₀ are asymptotically free
   - But crucially, Newton's constant and Λ also need to reach fixed points for full UV completion

2. **Asymptotically Safe Fixed Point (AS-FP, Reuter):**
   - g* ≠ 0, λ* ≠ 0 (as in standard AS)
   - ω* ≠ 0, σ* ≠ 0 (fourth-derivative couplings are also non-zero!)
   - This extends the Reuter fixed point to include curvature-squared terms

### The Critical Trajectory

**Most importantly:** Sen, Wetterich, and Yamada find evidence for a **critical trajectory connecting the two fixed points**. Starting from asymptotic freedom in the extreme UV, the flow may pass through or near the Reuter fixed point on its way to the IR.

This means the relationship is:
- **UV (extreme high energy):** The theory is asymptotically free in the fourth-derivative couplings → looks like quadratic gravity
- **Intermediate UV:** The flow approaches the Reuter fixed point → looks like asymptotic safety
- **IR:** Both converge to Einstein gravity with small corrections

**This is a profound result:** Asymptotic freedom and asymptotic safety are not competing descriptions but **different aspects of the same RG flow**, visible at different scales.

### The Role of Matter

Salvio and Strumia ("Agravity up to infinite energy," 2018) showed that:
- The f₂ coupling is asymptotically free regardless of matter content
- The f₀ coupling is NOT asymptotically free — it grows in the UV
- For the theory to be valid to infinite energy, f₀ must reach a UV fixed point
- This requires specific matter content (beyond the Standard Model)
- At the fixed point, the gravitational sector flows toward **conformal gravity** (where only C² survives)

This bridges the two programs: the f₀ coupling needs to reach an interacting fixed point (asymptotic safety in f₀), even while f₂ is asymptotically free. **Both mechanisms operate simultaneously.**

---

## 4. RG Flow: Exact RG for Quadratic Gravity

### What Happens When You Compute the Exact RG for the Quadratic Gravity Action?

Several groups have computed the functional RG flow for truncations that include quadratic curvature terms:

**Codello and Percacci (2006):** "Fixed Points of Higher-Derivative Gravity"
- Used the functional RG (Wetterass equation) with the full quadratic-in-curvature truncation
- Found that in addition to the free fixed point (asymptotic freedom of f₂), there exist **non-trivial fixed points** for Newton's constant
- The non-trivial fixed point has the right sign structure to be free from tachyons (for one of two non-trivial FPs found)

**Benedetti et al. (2010):** Extended to R² polynomial truncations up to R⁸
- Found a fixed point with **three UV-attractive directions** → constrains couplings to a 3D subspace
- The fixed point persists as the truncation is enlarged → evidence for robustness

**Sen, Wetterich, Yamada (2022):** Non-perturbative flow equations at fourth-order derivative level
- Confirmed the two-fixed-point structure (AF + AS)
- Showed that Newton's constant and cosmological constant have non-trivial fixed points even in the asymptotically free scenario
- The IR limit reproduces Einstein gravity coupled to a scalar field with only unobservably small corrections

### The Perturbative vs. Non-Perturbative Story

A critical distinction:

1. **Perturbative RG** (one-loop, as used by Stelle, Fradkin-Tseytlin, Avramidi-Barvinsky, Salvio-Strumia):
   - Treats f₂ and f₀ as coupling constants
   - Finds asymptotic freedom in f₂
   - Does NOT address Newton's constant's RG running (it's not an independent coupling in the perturbative treatment — it gets renormalized but not in the same sense)

2. **Non-perturbative/functional RG** (Wetterass equation, as used by Reuter, Percacci, Wetterich):
   - Treats all couplings democratically (g, λ, ω, σ, and higher)
   - Finds the Reuter fixed point in g and λ
   - Recovers the asymptotic freedom of ω (f₂) as a feature of the Gaussian fixed point in that coupling
   - Additionally finds a non-trivial fixed point in ω

**Conclusion:** The exact RG **does** find the Reuter fixed point when applied to the quadratic gravity action. Moreover, it finds that the asymptotically free behavior of quadratic gravity and the Reuter fixed point coexist as two different fixed points in the same theory space. The perturbative treatment only sees the asymptotically free fixed point because it works near the Gaussian point by construction.

---

## 5. Ghost/Fakeon Issue in Asymptotic Safety

### The Central Tension

When the asymptotic safety effective action is expanded in curvature invariants, it generically produces terms like:

Γ_k = ∫d⁴x √g [ (Z_N/16πG) R + a(k) R² + b(k) C_μνρσC^μνρσ + ... ]

The C² term, when expanded around flat space, gives rise to a massive spin-2 mode with **wrong-sign kinetic term** — the Stelle ghost. This ghost appears in the spectrum regardless of whether the theory is viewed from the AS or QG perspective.

### Three Approaches to the Ghost Problem

The ghost/unitarity problem has been addressed by three distinct proposals, and their relationship illuminates the AS ↔ QG connection:

#### (A) Anselmi-Piva Fakeon Prescription
- The ghost pole is quantized using neither Feynman nor anti-Feynman prescription, but a new "fakeon" prescription
- The fake particle propagates inside loops but never appears as an external state
- The theory is proven unitary to all orders in perturbation theory
- The classical limit is Hermitian
- This is a **quantization choice** imposed on the theory
- The fakeon prescription modifies the analytic structure of amplitudes

#### (B) Donoghue-Menezes Unstable Ghost
- Quantum corrections give the ghost a large decay width (it decays to pairs of ordinary particles)
- The ghost becomes an unstable resonance that never appears in the asymptotic spectrum
- Unitarity is maintained because cuts only include stable particles
- Uses a Lee-Wick-type contour
- This is a **dynamical mechanism** — unitarity emerges from the quantum theory itself
- Criticism: Anselmi argues this leads to a non-Hermitian classical limit and issues with causality

#### (C) Non-perturbative Resolution (Asymptotic Safety perspective)
- At the non-perturbative Reuter fixed point, the effective action may not have a simple polynomial expansion
- The form factors (momentum-dependent coefficients of R², C²) may be **entire functions** without poles on the real axis
- In this case, there would be **no ghost pole at all** — the ghost is an artifact of the polynomial truncation
- Knorr et al. (2022) "Reconstructing the graviton" found that the non-perturbative propagator, when reconstructed from the Euclidean data:
  - Has complex conjugate poles (not on the real axis)
  - Does NOT have a simple ghost pole
  - The spectral function shows no negative-norm states

### Key Insight: The Ghost May Be a Perturbative Artifact

This is perhaps the most important finding for the AS ↔ QG relationship:

In **perturbative QG**, the ghost is explicit — it's a pole in the tree-level propagator. You need the fakeon prescription or the Lee-Wick mechanism to handle it.

In **non-perturbative AS**, the ghost may not exist as a real pole at all. The functional RG computation of the full propagator shows that what appears as a ghost in perturbation theory gets resolved into complex conjugate poles or a non-trivial spectral function without negative-norm states.

**If this is correct**, then the fakeon prescription is the **perturbative approximation** of what happens automatically at the non-perturbative level. The fakeon ensures unitarity in perturbation theory; non-perturbative AS achieves unitarity by not having a real ghost pole in the first place.

This is a major point of convergence: the fakeon prescription and asymptotic safety may be solving the same problem at different levels of approximation.

### Update (2025): All Three Approaches Converge on Complex Poles

The Buccio-Donoghue-Menezes-Percacci "ghost resonances" paper (JHEP 02, 2025) provides striking new evidence. When the ghost self-energy is resummed perturbatively (approach B), the ghost pole splits into **complex conjugate poles in the first Riemann sheet**. The Bonanno-Pawlowski non-perturbative reconstruction (approach C) also finds **complex conjugate poles**. Even the fakeon prescription (approach A) can be understood as projecting out modes corresponding to these complex poles.

**The convergence is now three-fold:**
- Perturbative resummation → complex conjugate poles (Donoghue et al.)
- Non-perturbative reconstruction → complex conjugate poles (Bonanno et al.)
- Fakeon prescription → effectively removes these modes from the spectrum

All three approaches agree: the Stelle ghost is NOT a physical particle with a real pole. Its pole structure is complex, and no negative-norm states appear in the physical spectrum.

---

## 6. Recent Results (2024-2026)

### 6.1. Platania & Wetterich: "Fictitious Ghosts" (2020, PLB)

**Key claim:** The ghost degrees of freedom appearing in truncations of the effective action at finite order in derivatives are **fictitious**. Their contributions to the fully-dressed propagator — specifically, the residues of the ghost-like poles — **vanish** once all operators compatible with the symmetry of the theory are included in the effective action.

**Implication:** The Stelle ghost is not a physical degree of freedom of the full theory; it is an artifact of truncating the effective action at quadratic order in curvature. In the full non-perturbative theory (asymptotic safety), the ghost disappears. This directly supports the hypothesis that asymptotic safety and quadratic gravity are the same theory, with the ghost being an intermediate perturbative artifact.

### 6.2. Bonanno, Denz, Pawlowski, Reichert: "Reconstructing the Graviton" (SciPost Phys. 12, 2022)

Reconstructed the Lorentzian graviton propagator in AS from Euclidean functional RG data.

**Key results:**
- The **background graviton** spectral function has negative parts (similar to the gluon in QCD — which is confined and not a physical asymptotic state)
- The **dynamical (fluctuation) graviton** spectral function is **positive**
- The positive spectral function of the physical graviton "may hint at the unitarity of asymptotically safe quantum gravity"
- Complex conjugate poles appear as a generic feature — NOT simple ghost poles on the real axis

**Significance:** The physical graviton propagator in AS does not have the pathological ghost structure of perturbative quadratic gravity. The ghost is resolved non-perturbatively.

### 6.3. Platania: "Causality, Unitarity, and Stability" (JHEP 09, 2022)

Established conditions for the momentum dependence of the dressed graviton propagator to be consistent with:
- **Unitarity** (positive spectral function for physical modes)
- **Causality** (appropriate analyticity properties)
- **Stability** (no tachyonic instabilities)

Showed that propagators satisfying all three conditions **exist** within asymptotic safety, while the naive quadratic gravity propagator fails causality unless supplemented with a prescription (fakeon or Lee-Wick).

### 6.4. Buccio, Donoghue, Menezes & Percacci: "Physical Running of Couplings" (PRL 133, 2024)

**Key discovery:** The well-known beta functions of quadratic gravity (computed by Fradkin-Tseytlin, Avramidi-Barvinsky, and others) do **not** correspond to the physical dependence of scattering amplitudes on external momenta. The authors derived the correct **physical beta functions** — i.e., the actual momentum-dependence governing how scattering amplitudes change with energy.

**Critical result:** Asymptotic freedom turns out to be **compatible with the absence of tachyons** when using the physical beta functions. This was previously unclear because the standard MS-bar beta functions could not disentangle physical running from scheme artifacts.

**Significance for AS ↔ QG:** This paper strengthens the QG side of the story by showing that quadratic gravity's asymptotic freedom is physically robust and not an artifact of the renormalization scheme. It also provides the correct comparison point for non-perturbative AS beta functions.

### 6.5. Buccio, Donoghue, Menezes & Percacci: "Remarks on Ghost Resonances" (JHEP 02, 2025)

**Key finding:** The dressed ghost propagator, after resummation of self-energy corrections, has a pair of **complex conjugate poles in the first Riemann sheet**. This is unlike ordinary unstable resonances, which have no pole in the first sheet but a complex conjugate pair in the second sheet.

**Technical detail:** For real masses above the multiparticle threshold, the ghost propagator structure is:
- Ghost pole at m²_ghost → splits into m²_ghost ± iΓ (complex conjugate pair)
- These poles are in the FIRST Riemann sheet (unusual!)
- No real-axis poles remain in the physical region

**Connection to AS ghost resolution:** This is remarkably consistent with the Bonanno-Pawlowski et al. finding (Section 6.2) that the non-perturbative graviton propagator in AS also has complex conjugate poles rather than real ghost poles. The perturbative (Donoghue) and non-perturbative (AS) approaches are converging on the **same pole structure**: complex conjugate pairs, not real ghost poles.

### 6.6. Knorr & Platania: "Positivity Bounds and Asymptotic Safety Landscapes" (JHEP 03, 2025)

At fourth order in derivatives, found **two gravitational fixed points** providing viable UV completions:
- The first corresponds to the standard Reuter fixed point
- The second yields a richer sub-landscape of effective theories
- Tested against positivity bounds and the weak gravity conjecture

**Key implication:** The theory space of asymptotic safety with curvature-squared terms is richer than previously understood, with the possibility that multiple UV completions exist.

### 6.7. Quadratic Gravity with Torsion and Asymptotic Freedom (JHEP 08, 2025)

A class of metric-affine gravitational theories with action quadratic in curvature and torsion tensors was studied. Using heat kernel techniques, the torsion contributions to one-loop counterterms were computed.

**Key result:** There exists a specific nonminimal kinetic term for the pure tensorial (hook-antisymmetric traceless) component of torsion that renders the gravitational couplings **asymptotically free in the absence of tachyons**. Vectorial and axial components preserve the qualitative RG flow of the metric sector.

**Significance:** This extends the QG program to metric-affine geometry, potentially connecting it to first-order formulations used in some AS calculations (Palatini-type). The asymptotic freedom result is robust under this extension.

### 6.8. Schiffer: "Asymptotically Safe QG: Functional and Lattice Perspectives" (2025)

A comprehensive review (arXiv: 2509.26352) synthesizing the status of asymptotic safety from both functional RG and lattice (CDT/EDT) perspectives. Confirms the robustness of the Reuter fixed point under various truncations and emphasizes the convergence between functional and lattice evidence for a UV fixed point.

### 6.9. Inverted Harmonic Oscillator Approach (March 2026)

A very recent paper (arxiv: 2603.07150) proposes a novel resolution to the ghost problem: instead of treating the extra spin-2 mode as a ghost, it should be understood as governed by an **inverted harmonic oscillator** Hamiltonian:

H_ghost = -ω/2 (p² + q²) → H_IHO = ω/2 (-p² + q²)

The IHO Hamiltonian is indefinite but Hermitian, and the mode remains off-shell and confined, never appearing in the asymptotic spectrum. This uses a **direct-sum Hilbert space** structure with sectors evolving forward and backward in time.

**Relation to other approaches:** This is presented as an alternative to both the fakeon prescription and the Lee-Wick mechanism, providing a "physical understanding" of why the ghost is harmless. It makes testable predictions: modified tensor-to-scalar ratios and parity asymmetry in the CMB.

### 6.10. Quanta Magazine Coverage (November 2025)

A Quanta Magazine article highlighted the "comeback" of quadratic gravity, noting:
- Donoghue and collaborators demonstrated asymptotic freedom in QG
- Multiple approaches (fakeon, unstable ghost, IHO) now claim to resolve unitarity
- Buoninfante: "Mathematically, they make sense now"
- Platania remains cautious: "It's still open as a question"

### 6.11. Buoninfante: "Strict Renormalizability as Paradigm" (JHEP 07, 2025)

Argues that strict renormalizability (i.e., the requirement that the theory is renormalizable without needing infinitely many counterterms) is a powerful selection criterion that uniquely picks out quadratic gravity as the quantum theory of the gravitational field.

### 6.12. Anselmi: "Asymptotically Local" QFTs

Anselmi has developed the concept of "asymptotically local" quantum field theories (AL-QFTs). Starting from nonlocal theories with form factors, he identifies a class of models whose local limits yield theories with **physical and purely virtual (fakeon) particles**. This provides a bridge: the non-local structure of the full effective action (as computed in AS) reduces in the local limit to precisely the fakeon theory. The fakeon prescription thus emerges as the **local limit** of a more fundamental non-local structure.

### 6.13. Basile, Knorr, Platania, Schiffer: "AS, QG, and the Swampland" (2025)

Examined the compatibility of asymptotic safety with swampland conjectures (conditions that string theory imposes on consistent EFTs). Key tensions:
- Strict AS may be incompatible with spacetime topology change
- Black hole thermodynamics may require non-standard interpretation
- This does NOT directly affect the AS ↔ QG relationship but constrains the broader program

---

## 7. Spectral Dimension as Bridge

### 7.1. The Universal d_s = 4 → 2 Flow

One of the most striking features of quantum gravity is the near-universal prediction that the spectral dimension flows from d_s = 4 at macroscopic scales to d_s ≈ 2 at microscopic scales. This has been observed in:

| Approach | UV Spectral Dimension | Mechanism |
|----------|----------------------|-----------|
| Asymptotic Safety | d_s → 2 | Anomalous dimension η_N = -2 |
| Quadratic Gravity | d_s → 2 | 1/p⁴ propagator (4th-derivative terms) |
| Causal Dynamical Triangulations | d_s → ~2 (actually ~3/2) | Monte Carlo simulations |
| Loop Quantum Gravity | d_s → 2 | Area gap / discrete geometry |
| Causal Set Theory | d_s → 2 | Causal structure / non-locality |
| Hořava-Lifshitz Gravity | d_s → 2 | Anisotropic scaling z = 3 |

### 7.2. Carlip's Universality Argument

**Carlip (2017, 2019)** argued that the universality of d_s → 2 has a deep explanation:

For a field with anomalous dimension η_N, the momentum-space propagator goes as:

G(p) ~ (p²)^(-1 + η_N/2)

For η_N = 2 - d (in d dimensions), this becomes G(p) ~ p^(-d), and the position-space propagator becomes **logarithmic** — exactly as for a free boson in 2 dimensions.

**The key insight:** Any quantum gravity theory that is asymptotically safe (in the generalized sense of having a fixed point with η_N = 2 - d) will automatically exhibit d_s → 2. This is true regardless of whether the fixed point is:
- The Reuter fixed point of AS
- The Gaussian fixed point of QG (where the 1/p⁴ propagator effectively gives η = -2)
- Any other fixed point

### 7.3. Why This Bridges AS and QG

The spectral dimension argument provides the conceptual bridge:

1. **Our prior exploration showed:** d_s = 4 → 2 implies a 1/p⁴ propagator, which uniquely selects quadratic gravity
2. **Asymptotic safety independently gives:** d_s = 4 → 2 via η_N = -2
3. **Both require the same propagator physics:** 1/p⁴ at high momenta

The spectral dimension is a **physical observable** (in principle measurable through diffusion processes on quantum spacetime). Both theories predict the same value. The reason is the same: the effective propagator must fall as 1/p⁴.

This is not a coincidence but a **necessary consequence**: any UV-complete quantum gravity theory with the spectral dimension flowing to 2 must have a 1/p⁴ propagator, which in 4D is equivalent to having curvature-squared terms (or equivalent form factors) in the effective action. Asymptotic safety and quadratic gravity are two descriptions of the same UV physics.

---

## 8. Synthesis and Conclusion

### 8.1. Summary of Evidence

| Question | Finding | Verdict |
|----------|---------|---------|
| Same UV propagator? | Both give 1/p⁴ | ✅ Identical |
| Same spectral dimension? | Both give d_s → 2 | ✅ Identical |
| Same fixed point? | Different but connected via critical trajectory | 🔶 Complementary |
| Same ghost resolution? | Fakeon (pert.) ↔ fictitious ghost (non-pert.) ↔ complex poles (both!) | ✅ Converging |
| Same RG flow? | AS contains QG as a perturbative limit | ✅ AS subsumes QG |
| Same predictions? | Both flow to Einstein gravity in IR | ✅ Identical IR physics |

### 8.2. The Emerging Picture

The evidence strongly supports the following synthesis:

**Quadratic gravity with fakeon quantization and asymptotic safety are NOT the same theory in a trivial sense, but they are deeply related — they are perturbative and non-perturbative descriptions of the same UV completion of gravity.**

The precise relationship is:

1. **Quadratic gravity** is the **perturbative truncation** of the asymptotic safety effective action. When you expand the AS effective action Γ_k in powers of curvature and keep terms up to quadratic order, you get the Stelle action. The perturbative RG (one-loop beta functions for f₂ and f₀) captures the behavior near the Gaussian fixed point in theory space.

2. **Asymptotic safety** is the **non-perturbative completion** of quadratic gravity. The functional RG reveals the full structure of theory space, including:
   - The Gaussian fixed point (where QG is asymptotically free)
   - The Reuter fixed point (non-perturbative)
   - A critical trajectory connecting them

3. **The fakeon prescription** is the **perturbative implementation** of what happens automatically at the non-perturbative level:
   - In perturbation theory, the ghost is a real pole → needs fakeon prescription for unitarity
   - Non-perturbatively, the ghost pole either vanishes (fictitious ghost, Platania-Wetterich) or splits into complex conjugate poles (Bonanno-Pawlowski et al.)
   - Even perturbative resummation of the ghost self-energy gives complex conjugate poles (Buccio-Donoghue-Menezes-Percacci 2025) — matching the non-perturbative result
   - The fakeon prescription "knows" about the non-perturbative resolution — it correctly removes the ghost from the physical spectrum

4. **The spectral dimension d_s = 2** is the **observable bridge** — it is predicted by both, and it constrains the UV propagator to be 1/p⁴, which is the defining feature of both approaches.

### 8.3. Where They Differ (and Why It Matters)

Despite the deep connections, important differences remain:

1. **Number of UV-attractive directions:** At the Reuter fixed point, there are typically 2-3 relevant directions. At the Gaussian (QG) fixed point, the number is different. This affects the number of free parameters in each approach.

2. **Non-perturbative effects:** The full AS effective action contains operators of all orders in curvature. Quadratic gravity truncates at second order. The higher-order terms could be physically significant (e.g., for black hole singularity resolution).

3. **The f₀ coupling:** In perturbative QG, f₀ is not asymptotically free — it runs to strong coupling. The AS perspective provides a UV fixed point for this coupling, completing the theory. This is where AS adds essential physics that perturbative QG cannot provide.

4. **Topology:** AS in its standard formulation does not accommodate spacetime topology change, while some non-perturbative aspects of quantum gravity may require it.

### 8.4. Final Conclusion

**Quadratic gravity + fakeon and asymptotic safety are two faces of the same theory.**

More precisely:
- **QG+F is the perturbative sector of AS.** It captures the correct UV behavior (1/p⁴ propagator, asymptotic freedom in f₂, renormalizability) and the correct unitarity prescription (fakeon → fictitious ghost).
- **AS is the non-perturbative completion of QG+F.** It provides the UV fixed point for f₀, resolves the ghost non-perturbatively, and reveals the full structure of theory space.
- **Neither is complete without the other.** QG+F needs AS for the f₀ fixed point and non-perturbative ghost resolution. AS needs QG+F for perturbative computability and the fakeon/unitarity mechanism.

This is analogous to the relationship between perturbative QCD (asymptotic freedom at high energy) and non-perturbative QCD (confinement at low energy) — they are the same theory (QCD) described at different scales and with different tools.

**For our quantum gravity program:** This means that the theory selected by the spectral dimension constraint (quadratic gravity + fakeon) is not just a perturbative approximation — it is the perturbative face of a non-perturbatively UV-complete theory (asymptotic safety). This greatly strengthens the case for this being THE correct theory of quantum gravity, as it passes tests at both the perturbative AND non-perturbative level.

### 8.5. Open Questions

1. **Exact mapping:** Can we explicitly construct the map between the fakeon prescription and the non-perturbative ghost resolution? This would cement the equivalence.

2. **Predictions:** Do AS and QG+F make the same predictions for scattering amplitudes, or do non-perturbative corrections matter? At what energy scale do the two descriptions diverge?

3. **Matter content:** Salvio-Strumia showed that the UV completion of f₀ requires specific matter beyond the SM. Does the AS approach also require this, or can it accommodate arbitrary matter?

4. **Black holes and cosmology:** The non-perturbative effects of AS may resolve singularities differently from perturbative QG. Can we distinguish these observationally?

5. **The third approach (IHO, 2026):** Does the direct-sum Hilbert space approach of the inverted harmonic oscillator provide yet another perspective on the same physics, or is it genuinely different?

6. **Physical vs. standard beta functions:** Buccio et al. (2024) showed that the physical beta functions differ from the standard MS-bar ones. How do the physical beta functions compare to the non-perturbative AS beta functions extracted from the functional RG? If they agree, this would be the most direct evidence yet for the equivalence.

7. **Torsion and metric-affine formulations:** The 2025 result showing asymptotic freedom with torsion opens the question: does the AS program in first-order (Palatini) formalism reproduce the same fixed-point structure? This could provide a formulation-independent proof of equivalence.

---

## Key References

1. Stelle, K.S. (1977). "Renormalization of higher-derivative quantum gravity." Phys. Rev. D 16, 953.
2. Fradkin, E.S. & Tseytlin, A.A. (1982). "Renormalizable asymptotically free quantum theory of gravity." Nuclear Physics B 201, 469.
3. Anselmi, D. & Piva, M. (2017-2018). Fakeon quantization series. JHEP.
4. Salvio, A. & Strumia, A. (2014). "Agravity." JHEP 06 (2014) 080.
5. Salvio, A. & Strumia, A. (2018). "Agravity up to infinite energy." Eur. Phys. J. C 78, 124.
6. Salvio, A. (2018). "Quadratic Gravity." Front. Phys. 6:77.
7. Sen, S., Wetterich, C. & Yamada, M. (2022). "Asymptotic freedom and safety in quantum gravity." JHEP 03 (2022) 130.
8. Codello, A. & Percacci, R. (2006). "Fixed Points of Higher-Derivative Gravity." Phys. Rev. Lett. 97, 221301.
9. Donoghue, J.F. & Menezes, G. (2021). "On Quadratic Gravity." arXiv:2112.01974.
10. Bonanno, A., Denz, T., Pawlowski, J.M. & Reichert, M. (2022). "Reconstructing the graviton." SciPost Phys. 12, 001.
11. Platania, A. (2022). "Causality, unitarity and stability in quantum gravity: a non-perturbative perspective." JHEP 09 (2022) 167.
12. Platania, A. & Wetterich, C. (2020). "Non-perturbative unitarity and fictitious ghosts in quantum gravity." PLB 811, 135911.
13. Carlip, S. (2019). "Dimension and Dimensional Reduction in Quantum Gravity." Universe 5, 83.
14. Knorr, B. & Schiffer, M. (2021). "Non-Perturbative Propagators in Quantum Gravity." Universe 7, 216.
15. Basile, I., Knorr, B., Platania, A. & Schiffer, M. (2025). "Asymptotic safety, quantum gravity, and the swampland." SciPost Phys. 20.2.027.
16. Buoninfante, L. (2025). "Strict renormalizability as a paradigm for fundamental physics." JHEP 07 (2025) 175.
17. Buccio, D., Donoghue, J.F., Menezes, G. & Percacci, R. (2024). "Physical running of couplings in quadratic gravity." Phys. Rev. Lett. 133, 021604.
18. Buccio, D., Donoghue, J.F., Menezes, G. & Percacci, R. (2025). "Remarks on ghost resonances." JHEP 02 (2025) 186.
19. Quadratic gravity with propagating torsion and asymptotic freedom (2025). JHEP 08 (2025) 130.
20. Schiffer, M. (2025). "Asymptotically safe quantum gravity: functional and lattice perspectives." arXiv:2509.26352.
21. Sravan Kumar, K. & Marto, J. (2026). "Quantum (quadratic) gravity: replacing the massive tensor ghost with an inverted harmonic oscillator-like instability." arXiv:2603.07150.
22. Sen, S., Wetterich, C. & Yamada, M. (2023). "Scaling solutions for asymptotically free quantum gravity." JHEP 02 (2023) 054.
