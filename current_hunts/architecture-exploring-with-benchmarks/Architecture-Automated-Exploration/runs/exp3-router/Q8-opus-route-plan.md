ROUTE: COMPUTATION

PLAN:
1. Write the mean-field self-consistency equation for the lattice gas grand canonical ensemble: ⟨n⟩ = 1 / (1 + exp[-(μ + zε⟨n⟩) / (k_B T)]), where z is the effective coordination number and ε is the interaction energy. Identify that z_horizontal and z_vertical represent coordination numbers for different layer directions — determine the effective z (likely z_total = z_horizontal + z_vertical = 12, or use them as specified by the multilayer geometry).
2. Substitute the given numerical parameters: ε = -(k_B T)/(2π), μ = 0.1 k_B T, z = 12 (or appropriate combination), T = 300 K. Express everything in units of k_B T to simplify: the self-consistency equation becomes ⟨n⟩ = 1 / (1 + exp[-(0.1 + 12 * (-1/(2π)) * ⟨n⟩)]) = 1 / (1 + exp[-(0.1 - (6/π)⟨n⟩)]).
3. Solve the self-consistency equation by iteration: start with ⟨n⟩_0 = 0.5, compute successive ⟨n⟩_{k+1} = 1 / (1 + exp[-(0.1 - (6/π)⟨n⟩_k)]) until convergence to 3 decimal places. (Note: since 6/pi ~ 1.91 > 1, there may be a first-order transition region — check for multiple solutions and select the thermodynamically stable one by comparing grand potentials if needed.)
4. Report ⟨n⟩ to 3 decimal places.

END_PLAN
