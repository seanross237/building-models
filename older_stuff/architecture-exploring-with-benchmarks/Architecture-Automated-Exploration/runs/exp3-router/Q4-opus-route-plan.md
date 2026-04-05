ROUTE: COMPUTATION
PLAN: Shortest path, 4 steps.
1. Model the freely jointed chain as a 3D random walk of n steps of length ℓ. The end-to-end vector distribution is Gaussian for large n: Ω(x) ∝ exp(−3x²/2nℓ²), giving configurational entropy S_config(x) = const − 3kx²/(2nℓ²).
2. Since the system is thermally isolated (microcanonical), the total energy E is fixed. The kinetic degrees of freedom (3n momenta) give the kinetic entropy S_kin(E_kin) = (3n/2)k ln(E_kin) + const, where E_kin = E − E(0) (potential energy is zero for massless struts, so E(0) is the ground-state/reference energy and E_kin = E − E(0)).
3. Compute the microcanonical temperature: 1/T = ∂S_total/∂E = (3n/2)k/(E − E(0)), so kT = 2(E − E(0))/(3n).
4. Compute force: F = −T(∂S_config/∂x) = −T·(−3kx/(nℓ²)) = 3kTx/(nℓ²). Substitute kT = 2(E − E(0))/(3n) to get F = 2(E − E(0))x/(n²ℓ²). This is a Hooke-law restoring force with spring constant depending on energy above ground state.
END_PLAN
