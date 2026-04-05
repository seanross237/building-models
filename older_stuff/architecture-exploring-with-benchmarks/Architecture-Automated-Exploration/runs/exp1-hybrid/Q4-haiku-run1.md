# Q4: Polymer Force Law Under Thermal Isolation

## Problem Statement
A freely jointed polymer chain with n identical mass points connected by massless struts of fixed length ℓ is in thermal equilibrium. The polymer has a linear elastic force law at thermal equilibrium. When the polymer is thermally isolated (adiabatic), what is the force law between its ends?

## Solution Following Prescribed Plan

### Step 1: Entropy Decomposition
For a large polymer chain, decompose total entropy into two parts:

**Configurational entropy:**
$$S_{config} = \text{const} - \frac{3kx^2}{2nl^2}$$

This decreases quadratically with end-to-end extension x, reflecting fewer accessible configurations at larger extensions.

**Kinetic entropy:**
$$S_{kinetic} = \frac{nk}{2}\ln(T) + \text{const}$$

With approximately n degrees of freedom, the kinetic contribution is proportional to ln(T).

**Total entropy:**
$$S_{total} = \text{const} - \frac{3kx^2}{2nl^2} + \frac{nk}{2}\ln(T)$$

### Step 2: Adiabatic Constraint
For a thermally isolated system, entropy is conserved: dS = 0

$$dS = 0 = -\frac{3kx\,dx}{nl^2} + \frac{nk}{2}\frac{dT}{T}$$

Solving for the temperature-extension relationship:
$$\frac{nk}{2}\frac{dT}{T} = \frac{3kx\,dx}{nl^2}$$

$$\frac{dT}{T} = \frac{6x\,dx}{n^2l^2}$$

Integrating from x=0 (where T=T₀) to arbitrary x:
$$\ln\left(\frac{T(x)}{T_0}\right) = \frac{3x^2}{n^2l^2}$$

$$T(x) = T_0 \exp\left(\frac{3x^2}{n^2l^2}\right)$$

This is a key result: stretching an isolated polymer increases its temperature.

### Step 3: Energy and Force Calculation
The internal energy scales with temperature via equipartition:
$$E(x) = E(0) \exp\left(\frac{3x^2}{n^2l^2}\right)$$

The restoring force is:
$$F = -\frac{dE}{dx} = -E(0)\exp\left(\frac{3x^2}{n^2l^2}\right) \cdot \frac{6x}{n^2l^2}$$

### Step 4: Small-x Limit
For small extensions where $x \ll nl$, expand the exponential:
$$\exp\left(\frac{3x^2}{n^2l^2}\right) \approx 1 + \frac{3x^2}{n^2l^2} + O(x^4)$$

To leading order in small x:
$$F(x) \approx -E(0) \cdot \frac{6x}{n^2l^2}$$

## Answer

$$\boxed{F = -\frac{6E(0)x}{n^2l^2}}$$

The force law is **linear in x**, proportional to the stored energy E(0) and inversely proportional to n²l².

## Physical Interpretation

1. **Entropy constraint drives temperature increase**: When the isolated polymer is stretched, its configurational entropy decreases. To conserve total entropy, the kinetic entropy must increase, requiring higher temperature.

2. **Higher temperature increases internal energy**: The increased temperature raises the system's total energy, creating an entropic restoring force.

3. **Linear response at small x**: The force is linear in extension at small strains, similar to thermal equilibrium, but with the critical difference that the coefficient depends on E(0) rather than T.

4. **Comparison to thermal equilibrium**: At thermal equilibrium with a heat bath at temperature T, the force would be F = -3kTx/(nl²). Here, without heat exchange, the force is F = -6E(0)x/(n²l²), showing that the entropic mechanism is fundamentally different.

## Key Distinctions from Thermal Equilibrium

- **Thermal equilibrium**: F ∝ T (force proportional to reservoir temperature)
- **Adiabatic isolation**: F ∝ E(0)/(n²l²) (force determined by initial energy and structure)
- Both exhibit linear restoring forces, but the mechanism differs: one is temperature-driven, the other is entropy-driven through the thermal response of the isolated system.
