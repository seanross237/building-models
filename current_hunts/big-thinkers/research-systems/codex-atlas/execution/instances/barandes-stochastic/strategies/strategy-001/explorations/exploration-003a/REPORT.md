# Exploration 003a: Phase Freedom vs. Realm Selection — Computational Test

## Goal

For a qubit (N=2), explicitly construct and compare:
1. The space of all valid Theta matrices consistent with a given transition kernel Gamma (Barandes' phase freedom)
2. The space of all consistent history families for the same quantum system (CH's realm selection)

Then determine if these spaces have the same dimension and structure.

---

## Stage 1: Phase Freedom Space (Barandes Side)

### System Definition

**Hamiltonian:** H = (ω/2)σ_x with ω=1
**Evolution:** U(t) = cos(t)I − i sin(t)σ_x
**Time step:** t = π/4
**Unitary:** U = (1/√2)[[1, −i], [−i, 1]]
**Transition kernel:** Γ_ij = |U_ij|² = [[1/2, 1/2], [1/2, 1/2]] [COMPUTED]

### Construction of Phase Freedom Space

The general Theta with |Θ_ij|² = Γ_ij is:

```
Θ(α, β) = (1/√2) [[1, e^(iα)], [e^(iβ), e^(i(α+β−π))]]
```

where α, β ∈ [0, 2π) are free parameters (global phase already factored out). [VERIFIED]

**Unitarity constraint:** Θ†Θ = I requires e^(i(b−a)) + e^(i(d−c)) = 0, which gives d = α + β − π. This is ONE real constraint on 4 phases, leaving 3 free; modding out global phase gives **2 free parameters**. [VERIFIED]

**Key insight for N=2:** The complex unitarity equation e^(iX) + e^(iY) = 0 has Jacobian rank **1** (not 2) at a solution, because at X = Y + π the two gradient rows become proportional: J = [sin X; −cos X] ⊗ [1, −1, −1, 1]. This gives manifold dimension 4 − 1 = 3, minus 1 for global phase = **2**. [VERIFIED]

**Numerical verification:** 1000 random (α, β) pairs tested. All produce valid unitary Θ with |Θ_ij|² = Γ_ij. Maximum unitarity error: 5.6×10⁻¹⁶. Maximum Γ error: 5.0×10⁻¹⁶. [VERIFIED]

**Original U recovery:** U = Θ(−π/2, −π/2). [VERIFIED]

### Phase Freedom Space Properties

| Property | Value |
|----------|-------|
| **Real dimension** | 2 |
| **Topology** | T² (2-torus) |
| **Parameterization** | (α, β) ∈ [0, 2π)² |
| **CPTP constraint** | No additional constraints beyond unitarity |
| **Nature** | Each point = a distinct quantum channel with same Γ |

**Control check:** Γ = I (trivial) → only diagonal unitaries → dim = 1, topology T¹. [COMPUTED]

---

## Stage 2: Consistent History Families (CH Side)

### System Definition

Same Hamiltonian, initial state ρ₀ = |+⟩⟨+|, times t₀ = 0, t₁ = π/4, t₂ = π/2.

### Key Observation

Since H ∝ σ_x, the states |+⟩ and |−⟩ are energy eigenstates. Under evolution:
- ψ₁ = U(π/4)|+⟩ = e^(−iπ/4)|+⟩ (same direction, different phase)
- ψ₂ = U(π/2)|+⟩ = −i|+⟩ (same direction, different phase)

So {ψ₁, ψ₁⊥} = {ψ₂, ψ₂⊥} = {|+⟩, |−⟩} at all times. [COMPUTED]

### Single-Time Consistency (Trivial)

For projectors at only one time (t₁ or t₂), D(a,a') = δ_{a,a'} ⟨a|ρ|a⟩. **All bases are trivially consistent.** Dimension = 2 (S²). [VERIFIED]

### Three-Time Consistency (The Real Test)

For 3-time histories with rank-1 projective decompositions at both t₁ and t₂:

**Decoherence functional:** D((a₁,a₂), (a₁',a₂')) = Tr(C_{a₁,a₂} ρ₀ C†_{a₁',a₂'}) where C_{a₁,a₂} = P²_{a₂} U₁₂ P¹_{a₁} U₁.

**Critical finding:** For pure initial state, D = |α⟩⟨α| (rank 1) where α(a₁,a₂) = ⟨a₂|U₁₂|a₁⟩⟨a₁|U₁|ψ₀⟩. For D to be diagonal, α must have at most 1 nonzero entry. [VERIFIED]

### Analytic Proof: t₁ Must Be Eigenbasis of ψ₁

If any t₁ basis vector |a₁⟩ has ⟨a₁|ψ₁⟩ ≠ 0 (besides ψ₁ itself), the corresponding row of D couples with the ψ₁ row, making D non-diagonal. Therefore **t₁ = {ψ₁, ψ₁⊥} = {|+⟩, |−⟩}** is forced. [VERIFIED]

### Analytic Proof: t₂ Is Completely Free

When t₁ = {|+⟩, |−⟩}, the chain operators become rank-1:
- C_{+,b} = ⟨b|ψ₂⟩ · |b⟩⟨+|
- C_{−,b} = ⟨b|φ₂⟩ · |b⟩⟨−|

Every off-diagonal D element vanishes by one of two mechanisms:
1. **Same a₁, different a₂:** Tr involves ⟨b⊥|b⟩ = 0 (output orthogonality) [VERIFIED]
2. **Different a₁:** Tr involves ⟨+|−⟩ = 0 or ⟨−|+⟩ = 0 (input orthogonality via ρ₀ = |+⟩⟨+|) [VERIFIED]

**Numerical confirmation:** 1000 random t₂ bases tested with t₁ = {|+⟩, |−⟩}. Maximum |D_off| = 3.1×10⁻¹⁶. All consistent. [VERIFIED]

### Asymmetry: Reverse Does Not Work

With t₂ = {|+⟩, |−⟩} fixed and t₁ arbitrary: **0/1000 random t₁ bases were consistent** (max |D_off| = 0.25). The consistency structure is asymmetric. [COMPUTED]

### Consistent Family Space Properties

| Property | Value |
|----------|-------|
| **t₁ constraint** | Fixed: {ψ₁, ψ₁⊥} = {|+⟩, |−⟩} |
| **t₂ constraint** | None (any orthonormal basis works) |
| **Real dimension** | 2 (from t₂ choice on S²) |
| **Topology** | S² (2-sphere, Bloch sphere) |
| **Nature** | Each point = a decoherent history family with different t₂ measurement |

### The "Natural" Family

t₁ = t₂ = {|+⟩, |−⟩}: deterministic history P(+,+) = 1, all others = 0. This is the unique family where probability concentrates on a single history. [COMPUTED]

---

## Stage 3: Comparison

### Dimension Comparison at N=2

| | Phase Freedom (Barandes) | Realm Selection (CH) |
|---|---|---|
| **Dimension** | **2** | **2** |
| **Topology** | T² (2-torus) | S² (2-sphere) |
| **Parameterization** | Two phases (α, β) | Bloch sphere (θ₂, φ₂) |
| **Nature** | Gauge freedom (same Γ, different channel) | Measurement choice (same dynamics, different realm) |
| **Physical meaning** | Which quantum channel underlies the stochastic process | Which decoherent history family describes the system |

**The dimensions match at N=2 (both = 2), but the topologies are different (T² ≇ S²).** [VERIFIED]

### Scaling to General N (Uniform Gamma)

Phase freedom dimensions were computed via Jacobian rank at solution points (DFT-type unitaries). Realm selection dimensions are N²−N (flag manifold for free t₂ choice). [COMPUTED]

| N | Phase Freedom dim | Realm Selection dim | Equal? |
|---|---|---|---|
| 2 | 2 | 2 | **YES** |
| 3 | 4 | 6 | NO |
| 4 | 7 | 12 | NO |
| 5 | 8 | 20 | NO |
| 6 | 14 | 30 | NO |

**The dimension match at N=2 does not generalize.** For N > 2, realm selection always has more degrees of freedom than phase freedom. Both scale roughly quadratically in N but with different growth rates. [COMPUTED]

### Structural Assessment

The N=2 dimension match appears to be **coincidental**, arising from two independent facts:
1. Phase freedom gives dim = N² − rank(J) − 1 = 2 for N=2 (one real constraint on 4 phases)
2. Realm selection gives dim = N² − N = 2 for N=2 (S² for qubit)

Even at N=2 where the dimensions agree:
- **The spaces are topologically distinct:** T² (product of two circles) vs S² (sphere). T² has genus 1; S² has genus 0.
- **The parameterizations are independent:** Phase freedom varies the unitary channel; realm selection varies the measurement decomposition. These are different physical operations.
- **There is no natural map between them:** No construction sends a point in phase freedom space to a consistent history family, or vice versa.

### One Structural Parallel

Both spaces represent "hidden choices" that the stochastic/history frameworks must make but that standard QM fixes automatically:
- Barandes: standard QM fixes Θ = U (the actual unitary), eliminating phase freedom
- CH: standard QM has no preferred realm, creating the "realm problem"

The existence of these undetermined degrees of freedom is a shared structural feature of both frameworks, even though the specific spaces are different. [CONJECTURED]

---

## Summary of Verified Claims

| Claim | Status | Evidence |
|-------|--------|----------|
| Phase freedom space for N=2 uniform Γ has dim 2 | [VERIFIED] | Analytic proof + 1000 numerical samples |
| Phase freedom topology is T² | [VERIFIED] | Both parameters periodic, no constraints |
| CPTP adds no constraints beyond unitarity | [VERIFIED] | Analytic argument |
| 3-time CH requires t₁ = eigenbasis of ψ₁ | [VERIFIED] | Analytic proof + numerical scan |
| t₂ is completely free when t₁ = eigenbasis | [VERIFIED] | Analytic proof + 1000 numerical tests |
| Realm selection dim = 2 for N=2 | [VERIFIED] | S² for qubit |
| Dimensions match at N=2 | [VERIFIED] | 2 = 2 |
| Topologies differ (T² ≠ S²) | [VERIFIED] | Different Euler characteristic |
| Match does not generalize to N > 2 | [COMPUTED] | Jacobian analysis at N=3,4,5,6 |
| The match is coincidental | [CONJECTURED] | No structural map found |

---

## Code Artifacts

All code in `code/`:
- `stage1_phase_freedom.py` — Phase freedom construction, parameterization, verification
- `stage2_consistent_histories.py` — Brute-force grid search for consistent families (found 0 strict for 3-time)
- `stage2b_analytic_consistency.py` — Analytic analysis, optimization, proof of t₂ freedom
- `stage3_comparison.py` — Dimension comparison, general N scaling, topology analysis
- `dimension_fix.py` — Corrected Jacobian rank computation at solution points
