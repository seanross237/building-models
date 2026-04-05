# Q8: Mean-Field Adsorption in 2D Lattice Gas

## Problem Statement
Two-dimensional lattice gas adsorption system with N sites, multilayer adsorption allowed.

**Given:**
- ε = -(k_B T)/(2π)
- μ = 0.1 k_B T
- z_horizontal = 4
- z_vertical = 8
- T = 300 K

**Find:** ⟨n⟩ in grand canonical ensemble with mean-field approximation

---

## Solution

### Step 1: Total Coordination Number
z = z_h + z_v = 4 + 8 = **12**

### Step 2: Dimensionless Parameters
- β*ε = -1/(2π) = **-0.159154943**
- β*μ = **0.100000000**

### Step 3: Mean-Field Self-Consistency Equation
In the grand canonical ensemble with mean-field approximation:

```
⟨n⟩ = 1 / (1 + exp(z * β*ε * ⟨n⟩ - β*μ))
```

Substituting z = 12:

```
⟨n⟩ = 1 / (1 + exp(12 * (-0.159155) * ⟨n⟩ - 0.1))
⟨n⟩ = 1 / (1 + exp(-1.909858 * ⟨n⟩ - 0.1))
```

### Step 4: Iterative Solution
Fixed-point iteration starting from multiple initial guesses:

| Initial Guess | Converged Value | Iterations | Final Residual |
|---|---|---|---|
| 0.1 | 0.8480958211 | 20 | 1.76e-13 |
| 0.5 | 0.8480958211 | 19 | 2.37e-13 |
| 0.8 | 0.8480958211 | 18 | 1.02e-13 |
| 0.95 | 0.8480958211 | 18 | 1.89e-13 |

All initial guesses converge to a **unique fixed point**, confirming stability and self-consistency.

### Step 5: Verification
For n = 0.8480958211:
- Exponent: 12 × (-0.159155) × 0.848096 - 0.1 = -1.71901
- 1 / (1 + exp(-1.71901)) = 0.8480958211 ✓

**Self-consistency residual: 1.76 × 10⁻¹³ << tolerance**

---

## Result

⟨n⟩ = 0.8480958211

**Rounded to three decimal places: 0.848**

---

## Physical Interpretation
The mean occupancy of 0.848 indicates that approximately 84.8% of sites are occupied in the equilibrium state. The negative interaction energy (β*ε < 0) combined with the chemical potential (β*μ = 0.1 > 0) creates a stable adsorbed phase with high occupancy. The coordination number z = 12 reflects the contributions from both horizontal (nearest-neighbor) and vertical (interlayer) interactions.

