# Exploration 008: Transfer Matrix Spectral Gap and Adhikari-Cao Bound Analysis

## Goal

Two computational tasks:
- **Task A**: Compute spectral gap of transfer matrix / mass gap from autocorrelation and two-point functions for SU(2) lattice gauge theory on small lattices
- **Task B**: Compute spectral gap Δ_G of the group Laplacian on binary polyhedral subgroups 2T (24), 2O (48), 2I (120) of SU(2); plug into Adhikari-Cao bound β_min = (114 + 4 log|G|)/Δ_G; analyze how β_min scales with |G|

## Background

From prior explorations:
- Exploration 003: SU(2) lattice gauge theory confirms confinement, string tension σ > 0
- Exploration 005: Binary polyhedral subgroups 2T → 2O → 2I approach SU(2) to <0.5% accuracy; phase transition β_c ~ |G|^{0.6}
- Exploration 006: Adhikari-Cao (2025) proves mass gap for finite gauge groups via "swapping map"; bound degenerates as G → SU(2) in 4 structural layers; the spectral gap Δ_G → 0 is one layer

---

## Section 1: Spectral Gap of Group Laplacian (Task B)

### 1.1 Definition of Group Laplacian

For G ⊂ SU(2) with elements as unit quaternions, we use:

**Primary definition (nearest-neighbor Cayley graph)**:
S = {g ∈ G : d(g, e) is minimal non-trivial, i.e., smallest angle arccos(Re(g₀)) > 0}

L f(g) = |S| f(g) - Σ_{s∈S} f(gs)

The Laplacian matrix has L_{ii} = |S| and L_{ij} = -1 if g_j = g_i * s for some s ∈ S, else 0.

Spectral gap: Δ_G = λ₂(L) = smallest nonzero eigenvalue.

**Secondary definition (heat kernel random walk at β₀=1)**:
T_{gh} = exp(2 Re(<g,h>_quat)) / Z_g
Δ_G^{(heat)} = 1 - λ₂(T)

### 1.2 Results

(Populated after running code)

---

## Section 2: Adhikari-Cao Bound Analysis

### 2.1 The Bound

Adhikari-Cao (2025) Theorem 1.1: For finite gauge group G with spectral gap Δ_G,
at β ≥ β_min = (114 + 4 ln|G|) / Δ_G, correlations decay exponentially.

### 2.2 Scaling Analysis

(Populated after running code)

---

## Section 3: Transfer Matrix Analysis (Task A)

### 3.1 1D Transfer Matrix (0+1 dimensional toy model)

For a single spatial site with gauge group G, the "transfer matrix" is:
T_{g,h} = exp(β * 2 Re(<g,h>_quat))

This is exactly the heat kernel on G. The mass gap from this transfer matrix is:
m₀(β) = -ln(λ₂(T)/λ₁(T)) = ln(λ₁/λ₂)

**Note**: This is the mass gap of a 0+1D quantum mechanics on G, NOT the 4D Yang-Mills mass gap. It illustrates the β-dependence of the Fourier structure of the group.

### 3.2 Results for 2T, 2O, 2I

(Populated after running code)

---

## Section 4: Mass Gap from Autocorrelation Time (Task A)

### 4.1 Method

Run Monte Carlo for finite group gauge theory on 4⁴ lattice. Measure:
1. Plaquette autocorrelation function C(t) = ⟨P(0)P(t)⟩ - ⟨P⟩²
2. Integrated autocorrelation time τ_int = (1/2) + Σ_{t>0} C(t)/C(0)
3. Time-slice two-point function G(τ) = ⟨Tr(U_p(0)) Tr(U_p(τ))⟩_connected
4. Fit G(τ) ~ A exp(-m * τ) to get lattice mass gap m

### 4.2 Results

(Populated after running code)

---

## Section 5: Connection Between Tasks A and B

### 5.1 Expected Relationship

The spectral gap Δ_G of the group Laplacian should be related to:
- The gap of the transfer matrix T_{gh} = exp(β * 2<g,h>) at a given β
- The autocorrelation time of the Monte Carlo Markov chain
- The physical mass gap via m ≈ Δ_G * f(β) for some function f

### 5.2 Analysis

(Populated after running code)

---

## Summary of Results

(Populated last)
