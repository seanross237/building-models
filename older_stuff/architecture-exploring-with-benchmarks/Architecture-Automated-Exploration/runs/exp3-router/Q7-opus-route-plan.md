ROUTE: COMPUTATION

PLAN:
1. Construct the single-site grand canonical partition function Z_site = sum over n=0..k of exp(beta * (n*mu - E(n) - mean-field interaction term)), where E(n) encodes the layer energies epsilon_1 and epsilon_l = (0.02)^l k_B T, and the mean-field interaction uses z_lateral=4 and z_inter=4 with self-consistent average occupation.
2. Compute beta = 1/(k_B * 318K), convert all energy parameters to dimensionless units (they are already given in units of k_B T), evaluate each Boltzmann weight numerically for n = 0, 1, 2, ... k.
3. Sum the weights to get Z_site; compute <k> = (1/Z_site) * sum over n of n * weight(n).
4. If mean-field self-consistency is required (occupation couples back through lateral/inter-layer interaction), iterate: guess <k>, compute effective field, recompute <k>, repeat until convergence.

END_PLAN
