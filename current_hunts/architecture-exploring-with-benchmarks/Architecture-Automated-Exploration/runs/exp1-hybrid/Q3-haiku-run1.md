# Q3: 2D Exciton Rydberg Energy for n=3

## Problem Statement
Consider a 2D semiconductor material with a band gap of 3eV and a simple screened Coulomb potential. The resonance peak for the 1s exciton is 1 eV. What is the Rydberg energy for n = 3?

## Solution

### Step 1: Extract R_y from the 1s Resonance Condition

For a 2D semiconductor with screened Coulomb potential, the binding energy formula is:
$$E_n = \frac{R_y}{(n - 1/2)^2}$$

For the 1s state (n=1):
$$E_1 = \frac{R_y}{(1 - 1/2)^2} = \frac{R_y}{1/4} = 4R_y$$

The resonance peak occurs at the optical transition energy, which is measured from the band gap:
$$E_{resonance} = E_{gap} - |E_1| = E_{gap} - 4R_y$$

Given:
- E_gap = 3 eV
- E_resonance = 1 eV

Therefore:
$$3 - 4R_y = 1$$
$$4R_y = 2$$
$$R_y = 0.5 \text{ eV}$$

### Step 2: Calculate E_3 Using the Formula

For n=3:
$$E_3 = \frac{R_y}{(3 - 1/2)^2} = \frac{0.5}{(2.5)^2} = \frac{0.5}{6.25} = 0.08 \text{ eV}$$

### Step 3: Verification and Physical Interpretation

**Key Clarification:** The "resonance peak" refers to the spectral position of the optical transition, not the binding energy itself.

- Binding energy for n=1: |E_1| = 4R_y = 2 eV
- Resonance peak for n=1: E_gap - |E_1| = 3 - 2 = 1 eV ✓ (matches given value)
- Binding energy for n=3: |E_3| = 0.08 eV
- Resonance peak for n=3: E_gap - |E_3| = 3 - 0.08 = 2.92 eV

This demonstrates the (n-1/2)² denominator characteristic of 2D exciton physics, which differs from the 3D case where E_n ∝ 1/n².

## Answer

**The Rydberg energy for n = 3 is 0.08 eV**

Equivalently:
- Binding energy: E_3 = 0.08 eV
- Spectral resonance position: 2.92 eV (measured from ground state)
