# Exploration 001: 4-Point Tree-Level MHV Amplitude — Three-Way Computation

## Goal

Implement the spinor-helicity formalism in Python and compute the 4-point tree-level MHV amplitude in N=4 SYM via three independent methods:

1. **Parke-Taylor formula** (analytic baseline)
2. **BCFW recursion** (on-shell recursion)
3. **Grassmannian / positive geometry** (amplituhedron approach)

Verify numerical agreement and characterize computational cost.

---

## 1. Spinor-Helicity Infrastructure

### 1.1 Mathematical Setup

**Conventions** (code: `spinor_helicity.py`):
- Metric signature: (+,-,-,-)
- σ^μ = (I, σ_x, σ_y, σ_z)
- Momentum matrix: p^{αα̇} = p_μ σ^μ = |i⟩[i| for massless particles
- Angle bracket: ⟨ij⟩ = λ_i^1 λ_j^2 - λ_i^2 λ_j^1
- Square bracket: [ij] = λ̃_i^1 λ̃_j^2 - λ̃_i^2 λ̃_j^1
- Mandelstam: s_{ij} = ⟨ij⟩[ij] (note: this differs from the (-,+,+,+) convention where s = ⟨ij⟩[ji])

**Spinor extraction**: Given lightlike p^μ, construct p^{αα̇} = p_μ σ^μ, which is rank-1. Factor as |p⟩[p| by selecting the dominant column for |p⟩ and dividing for [p|.

### 1.2 Implementation

The `spinor_helicity.py` module provides:
- `Particle` dataclass with spinors, momentum extraction, mass check
- `angle_bracket(p_i, p_j)`, `square_bracket(p_i, p_j)` — O(1) each
- `mandelstam_sij(p_i, p_j)` — via spinor brackets AND 4-vector cross-check
- `make_kinematics_com(E, θ)` — center-of-mass 2→2 scattering (all-outgoing convention)
- `validate_kinematics(particles)` — checks momentum conservation, masslessness, Schouten identity

### 1.3 Kinematics Validation [COMPUTED]

For COM kinematics with E=1, θ=π/3:
- Momentum conservation: |Σp| < 10⁻¹⁵ ✓
- Masslessness: |p_i²| < 10⁻¹⁵ for all i ✓
- Mandelstam (spinor vs 4-vector): agree to 10⁻¹⁵ ✓
- s + t + u = 0 to 10⁻¹⁵ ✓
- Schouten identity: |⟨12⟩⟨34⟩ + ⟨13⟩⟨42⟩ + ⟨14⟩⟨23⟩| = 0 to machine precision ✓

Verified across 8 distinct kinematic configurations (4 COM, 4 random).

---

## 2. Method 1: Parke-Taylor Formula

### 2.1 Formula

For A₄(1⁻, 2⁻, 3⁺, 4⁺):

```
A₄^MHV = ⟨12⟩⁴ / (⟨12⟩⟨23⟩⟨34⟩⟨41⟩) = ⟨12⟩³ / (⟨23⟩⟨34⟩⟨41⟩)
```

This is a single closed-form expression. Requires computing 4 angle brackets and forming a ratio.

### 2.2 Numerical Results [COMPUTED]

| Kinematics | s₁₂ | t₂₃ | u₁₃ | A_PT |
|---|---|---|---|---|
| COM E=1 θ=π/3 | 4.0 | -3.0 | -1.0 | 2.370370 |
| COM E=1 θ=π/4 | 4.0 | -3.414 | -0.586 | 1.608081 |
| COM E=1 θ=π/6 | 4.0 | -3.732 | -0.268 | 1.231225 |
| COM E=2 θ=2.1 | 16.0 | -3.961 | -12.039 | 7.134534 |
| Random (seed 42) | 7.557 | -1.551 | -6.007 | 7.714990 |

### 2.3 Cost Analysis

- **Operations**: 4 angle brackets (8 multiplications + 4 subtractions), 3 multiplications + 1 division = **~20 operations total**
- **Terms**: 1
- **n-point scaling**: O(n) — the denominator is a cyclic product of n brackets

---

## 3. Method 2: BCFW Recursion

### 3.1 Setup

The [1,2⟩ shift deforms the spinors:
- |1̂⟩ = |1⟩ + z|2⟩ (holomorphic spinor shifted)
- |2̂] = |2] - z|1] (anti-holomorphic spinor shifted)
- |1̂] = |1], |2̂⟩ = |2⟩ (unchanged)

This preserves on-shell conditions and momentum conservation.

### 3.2 Factorization

**Key insight**: The shifted amplitude A₄(z) = ⟨12⟩³ / (⟨23⟩⟨34⟩(⟨41⟩ + z⟨42⟩)) has exactly ONE pole in z, from ⟨41̂⟩ = 0 at z_A = -⟨14⟩/⟨24⟩. [VERIFIED analytically]

This corresponds to the color-ordered channel {4,1̂}|{2̂,3} with propagator P = p₁+p₄.

At z_A, the internal line K = p̂₁ + p₄ is on-shell (K² = 0), and the amplitude factorizes:

```
A₄ = A₃^{anti-MHV}(4⁺, 1̂⁻, (-P̂)⁺) × A₃^{MHV}(P̂⁻, 2̂⁻, 3⁺) / P²₁₄
```

The left vertex is anti-MHV (all |⟩ proportional since ⟨1̂ 4⟩ = 0), and the right vertex is MHV (all |] proportional, verified numerically).

### 3.3 Sign Convention Detail

A subtle but critical sign arises from the propagator structure: the Parke-Taylor denominator contains ⟨41⟩ + z⟨42⟩ while the propagator is P₁₄² = (⟨14⟩ + z⟨24⟩)[14]. Since ⟨41⟩ = -⟨14⟩, we have:

```
⟨41⟩ + z⟨42⟩ = -(⟨14⟩ + z⟨24⟩) = -P₁₄²/[14]
```

This introduces a relative **(-1)** between the naive sub-amplitude product and the BCFW result:

```
A₄ = -(A_L × A_R / s₁₄)
```

This minus sign is a consequence of the antisymmetry of angle brackets (⟨41⟩ = -⟨14⟩). I verified this analytically by computing the full Cauchy residue directly. [VERIFIED]

### 3.4 Cross-check: Direct Cauchy Method

As an independent verification, I implemented a "direct Cauchy" BCFW that evaluates A₄(z) = ⟨12⟩³/(⟨23⟩⟨34⟩(⟨41⟩+z⟨42⟩)) directly and extracts the residue. This avoids 3-point sub-amplitudes entirely. It agrees with both the sub-amplitude BCFW and Parke-Taylor to machine precision.

### 3.5 Numerical Results [COMPUTED]

(Full results in the comparison table below — all agree with Parke-Taylor to < 10⁻¹² relative error.)

### 3.6 Cost Analysis

- **Operations**: ~40 total — compute z, shifted spinors, K extraction, 3 brackets for A_L, 3 brackets for A_R, propagator, combine
- **Terms**: 1 diagram for n=4
- **n-point scaling**: O(n²) terms — each BCFW step adds at most 1 propagator, and the recursion has depth O(n). Total terms grow quadratically. However, each term involves only on-shell lower-point amplitudes (no virtual momenta).

---

## 4. Method 3: Grassmannian / Positive Geometry

### 4.1 Setup

The Grassmannian integral for G(k,n) = G(2,4):

```
L_{4,2} = ∫ d^{2×4}C / (vol(GL(2)) × M₁M₂M₃M₄) × δ⁴(C·λ̃) × δ⁴(C⊥·λ)
```

where M_i are consecutive 2×2 minors of C (the cyclic Plücker coordinates).

### 4.2 Implementation

**Gauge fixing**: Set C = (I₂ | C') where C' is 2×2. This fixes GL(2) and leaves 4 free parameters.

**Delta function localization**: The constraint C·Λ̃ = 0 (where Λ̃ is the 4×2 matrix of λ̃ spinors) gives 4 equations for 4 unknowns. Solution via linear algebra:

```python
M = [λ̃₃ | λ̃₄]  # 2×2 system matrix
c_{a,3} , c_{a,4} = -M⁻¹ · λ̃_a  for a = 1, 2
```

**Complementary constraint**: C⊥·Λ = 0 is automatically satisfied by momentum conservation (verified numerically to < 10⁻¹⁵).

### 4.3 Key Finding: Algebraic Identity [COMPUTED]

The minors at the solution point, expressed in terms of square brackets, are:

```
M₁ = 1                    (gauge choice)
M₂ = (23) = [14]/[34]     (verified numerically)
M₃ = (34) = [12]/[34]     (verified numerically)
M₄ = (41) = -[23]/[34]    (verified numerically)
```

Their product: M₁M₂M₃M₄ = -[12][14][23]/[34]³

Therefore: **1/(M₁M₂M₃M₄) = -[34]³/([12][14][23])**

This is a "square bracket" representation of the amplitude. The **non-trivial algebraic identity**:

```
-[34]³ / ([12][14][23])  =  ⟨12⟩³ / (⟨23⟩⟨34⟩⟨41⟩)
```

holds for ANY 4-particle massless kinematics satisfying momentum conservation. [COMPUTED — verified across 10 kinematic points]

This identity follows from:
- s_{ij} = ⟨ij⟩[ij] (relating angle and square brackets via Mandelstam invariants)
- Schouten identity for both angle and square brackets
- Momentum conservation: s₁₂ = s₃₄, s₁₄ = s₂₃, s+t+u = 0

### 4.4 Momentum Twistor Data [COMPUTED]

Constructed momentum twistors Z_i = (λ_i, μ_i) where μ_i = x_i · λ_i via dual coordinates x_{i+1} = x_i - |i⟩[i|.

For COM E=1, θ=π/3:
- Z₁ = (2, 0, 0, 0)
- Z₂ = (0, 2, 0, 0)
- Z₃ = (-1.5, -0.866, 3.0, 1.732)
- Z₄ = (0.866, -1.5, -1.732, 3.0)
- ⟨1234⟩ = det(Z₁,Z₂,Z₃,Z₄) = 48.0

The four-bracket ⟨1234⟩ ≠ 0 confirms the momentum twistors are in general position, as required for the amplituhedron to be well-defined.

### 4.5 Cost Analysis

- **Operations**: ~30 — build Λ̃ matrix, solve 2×2 system, compute 4 minors, form product
- **Terms**: 1 residue (the integral fully localizes for k=2, n=4 tree level)
- **n-point scaling**: For general (n,k), the number of residues grows as the Eulerian number E(n-3, k-1). For MHV (k=2), there is always 1 residue, so the Grassmannian MHV computation is O(n) (same as Parke-Taylor). For NMHV (k=3), the number of terms grows, but each is an algebraic expression in the C-matrix data.

---

## 5. Comparison of Results

### Numerical Agreement Table [COMPUTED]

All three methods evaluated at the same kinematic point, compared to Parke-Taylor as baseline:

| Kinematics | A_PT | |BCFW/PT - 1| | |Grass/PT - 1| | Agree? |
|---|---|---|---|---|
| COM E=1 θ=π/3 | 2.37037037 | 4.4×10⁻¹⁶ | 0 | ✓ |
| COM E=1 θ=π/4 | 1.60808101 | 1.1×10⁻¹⁶ | 1.1×10⁻¹⁶ | ✓ |
| COM E=1 θ=π/6 | 1.23122473 | 4.4×10⁻¹⁶ | 0 | ✓ |
| COM E=1 θ=1.0 | 2.18913271 | 0 | 0 | ✓ |
| COM E=2 θ=2.1 | 7.13453397 | 1.1×10⁻¹⁶ | 7.8×10⁻¹⁶ | ✓ |
| COM E=5 θ=0.5 | 1.20862857 | 1.1×10⁻¹⁶ | 2.2×10⁻¹⁶ | ✓ |
| Random seed=42 | 7.71498985 | 4.4×10⁻¹⁶ | 0 | ✓ |
| Random seed=137 | 1.18809805 | 2.2×10⁻¹⁶ | 4.4×10⁻¹⁶ | ✓ |
| Random seed=999 | 4.47039754 | 3.3×10⁻¹⁶ | 3.3×10⁻¹⁶ | ✓ |
| Random seed=7 | 6.77603128 | 0 | 2.2×10⁻¹⁶ | ✓ |

**All 10 tests pass.** Maximum relative error across all methods and kinematics: < 10⁻¹⁵ (machine epsilon for float64).

### Timing Benchmark (5000 evaluations each, COM E=1 θ=π/3)

| Method | Time per eval | Ratio to PT |
|---|---|---|
| Parke-Taylor | 5.6 μs | 1.0× |
| BCFW | 231 μs | 41× |
| Grassmannian | 62 μs | 11× |

The BCFW is slowest due to spinor extraction for the internal on-shell momentum (requires building a 4-vector sum and factoring a 2×2 matrix). The Grassmannian requires a 2×2 linear solve. Parke-Taylor is fastest as it only evaluates angle brackets.

---

## 6. Computational Cost Analysis

### Summary

| Method | Operations (n=4) | Terms (n=4) | Scaling (general n) | Conceptual complexity |
|---|---|---|---|---|
| Parke-Taylor | ~20 | 1 | O(n) | Lowest — one formula |
| BCFW | ~40 | 1 | O(n²) terms | Medium — recursive factorization |
| Grassmannian | ~30 | 1 | O(n) for MHV, O(E(n-3,k-1)) general | Highest — linear algebra + geometry |

### Conceptual Advantages

**Parke-Taylor**: Simplest computation. But it's a RESULT, not a METHOD — it was conjectured from pattern-matching and proven by BCFW. Doesn't generalize beyond MHV without substantial extra structure.

**BCFW**: A genuine computational METHOD that works for any tree amplitude. The recursion reduces n-point to (n-1)-point, using only on-shell data. This is the "killer app" that launched the modern amplitudes program. Conceptual advantage: never introduces off-shell or gauge-dependent quantities.

**Grassmannian**: The most geometrically deep. Encodes the amplitude as a canonical form on the positive Grassmannian. For n=4, k=2, this is a quadrilateral in 2D, and the amplitude is its "volume." The Grassmannian makes manifest that the amplitude is a GEOMETRIC object, not just an algebraic formula. Key structural insight: the amplitude lives naturally in the Grassmannian/momentum-twistor space, and the usual spinor-bracket formulas are projections of this geometric data.

### Key Structural Observation

The Grassmannian result 1/(M₁M₂M₃M₄) gives the amplitude in terms of SQUARE brackets, while Parke-Taylor uses ANGLE brackets. These are related by the non-trivial identity in §4.3. From the amplituhedron perspective, this reflects the fact that the canonical form is independent of the specific coordinate system used to represent it — it's a geometric invariant.

---

## 7. Conclusions

### Results

1. **All three methods agree to machine precision** (~10⁻¹⁵ relative error) across all tested kinematic configurations. [COMPUTED]

2. The Grassmannian computation yields 1/(M₁M₂M₃M₄) = Parke-Taylor formula, establishing an algebraic identity between square-bracket and angle-bracket representations. [COMPUTED]

3. The BCFW recursion requires careful tracking of a sign from the antisymmetry of spinor brackets (⟨ij⟩ = -⟨ji⟩). This was verified both analytically and numerically. [VERIFIED]

4. For 4-point MHV, all three methods reduce to a single term, so the computational cost differences are modest. The real divergence appears at higher points.

### Assessment: Computational Tool vs. Deeper Structure?

Even at the 4-point tree level, the Grassmannian approach reveals structure NOT visible in the Parke-Taylor or BCFW formulations:

- The amplitude is the canonical form of a GEOMETRIC OBJECT (the amplituhedron), not just an algebraic expression.
- The momentum-twistor data (Z_i ∈ CP³) provides a natural home for the amplitude where locality and unitarity are emergent rather than manifest.
- The "square bracket representation" from the Grassmannian minors is dual to the "angle bracket representation" of Parke-Taylor, hinting at a deeper duality structure.

This suggests the amplituhedron is MORE than just a computational tool — it points to geometric structure underlying scattering amplitudes that is obscured by the conventional Lagrangian formulation.
