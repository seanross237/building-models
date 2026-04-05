"""
Investigations 1, 2, 3: Fisher information, entropy production, and
monotone functionals along the de Bruijn-Newman heat flow.

Key idea: Under the heat flow H_t, the zeros of Xi move. For the truncated
system (first N zeros), we can track how statistical quantities change with t.

For zeros z_1(t), ..., z_N(t) of H_t (in the z-variable where Xi(1/2+iz) = H_0(z)),
define:

1. The empirical zero density:
   rho_t(x) = (1/N) * sum_k delta(x - z_k(t))

   Smoothed version with bandwidth h:
   rho_t(x; h) = (1/N) * sum_k K_h(x - z_k(t))
   where K_h is a Gaussian kernel with bandwidth h.

2. Fisher information of the smoothed density:
   I(t) = integral [rho_t'(x)]^2 / rho_t(x) dx

3. Differential entropy of the smoothed density:
   S(t) = -integral rho_t(x) log(rho_t(x)) dx

4. de Bruijn's identity: dS/dt = (1/2) I(t)
   (This holds for the actual heat equation; for the zero dynamics ODE it's
   an approximation. Let's check if it holds numerically.)

5. Perturbative Fisher information (from the findings):
   I_pert(t) = sum_n I_n(sigma_n(t), t_n(t))
   where sigma_n + i*t_n are the zero locations in the s-variable.

For t >= 0, all zeros of H_t are real (since Lambda <= 0.2), so the zeros
z_k(t) are all real, and in the s-variable, rho_k = 1/2 + i*z_k(t).
All sigma_n = 1/2.

For t < 0 (approaching Lambda from below), zeros could become complex,
meaning sigma_n != 1/2 in the s-variable.

Since we're interested in the region t in [0, 0.5], all zeros are real.
The Coulomb ODE governs their motion:
   dz_k/dt = -sum_{j!=k} 1/(z_k - z_j)

We compute the Fisher information and entropy as functions of t using
the zero positions from the ODE integration.
"""

import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.stats import gaussian_kde
import json
import time

# First 100 zeta zeros
zeta_zeros_100 = [
    14.134725141734693, 21.022039638771555, 25.010857580145688,
    30.424876125859513, 32.935061587739189, 37.586178158825671,
    40.918719012147495, 43.327073280914999, 48.005150881167159,
    49.773832477672302, 52.970321477714460, 56.446247697063394,
    59.347044002602353, 60.831778524609809, 65.112544048081606,
    67.079810529494173, 69.546401711173979, 72.067157674481907,
    75.704690699083933, 77.144840068874805, 79.337375020249367,
    82.910380854086030, 84.735492980517050, 87.425274613125229,
    88.809111207634465, 92.491899270558484, 94.651344040519838,
    95.870634228245309, 98.831194218193692, 101.31785100573139,
    103.72553804532511, 105.44662305232542, 107.16861118427640,
    111.02953554316967, 111.87465917699263, 114.32022091545271,
    116.22668032085755, 118.79078286597621, 121.37012500242066,
    122.94682929355258, 124.25681855434576, 127.51668387959649,
    129.57870419995605, 131.08768853093265, 133.49773720299758,
    134.75650975337387, 138.11604205453344, 139.73620895212138,
    141.12370740402112, 143.11184580762063,
    146.00098248680934, 147.42276534498665, 150.05352042636562,
    150.92525768847482, 153.02469384990923, 156.11290928490036,
    157.59759167856619, 158.84998811710850, 161.18896413903135,
    163.03070946525130, 165.53706943943252, 167.18443997739506,
    169.09451541574390, 169.91197641081440, 173.41153668294768,
    174.75419163964368, 176.44143424577452, 178.37740738764081,
    179.91648404073547, 182.20707848753218, 184.87446783013584,
    185.59878367812381, 187.22892258316085, 189.41615932005700,
    192.02665636459935, 193.07972660757127, 195.26539673621312,
    196.87648174589413, 198.01530924901260, 201.26475190038891,
    202.49359454070200, 204.18967180534640, 205.39469730826280,
    207.90625898184580, 209.57650934558480, 211.69086187332840,
    213.34791928716560, 214.54704714788440, 216.16953843752520,
    219.06759640637760, 220.71491899738440, 221.43070050570560,
    224.00700025253620, 224.98325168798100, 227.42130563018640,
    229.33741300710580, 231.25018849682240, 231.98716362040960,
    233.69340409690380, 236.52422966581200,
]

N = 50  # Use first 50 for speed
zeta_zeros = zeta_zeros_100[:N]

print(f"Using {N} zeta zeros for heat flow analysis")


def coulomb_rhs(t_param, x):
    """Vectorized Coulomb ODE RHS including mirror zeros at -x_k."""
    n = len(x)
    X = x.reshape(1, -1)

    diff = x.reshape(-1, 1) - X
    np.fill_diagonal(diff, np.inf)
    sum_pos = np.sum(-1.0 / diff, axis=1)

    sum_neg_mirrors = x.reshape(-1, 1) + X
    sum_neg = np.sum(-1.0 / sum_neg_mirrors, axis=1)

    return sum_pos + sum_neg


def compute_density_fisher_entropy(zeros, bandwidth=None, x_range=None, n_points=2000):
    """
    Compute the KDE-based density, Fisher information, and entropy
    for a set of zeros.
    """
    if bandwidth is None:
        # Use Silverman's rule
        bandwidth = 1.06 * np.std(zeros) * len(zeros)**(-0.2)

    if x_range is None:
        margin = 3 * bandwidth
        x_range = (zeros.min() - margin, zeros.max() + margin)

    x = np.linspace(x_range[0], x_range[1], n_points)
    dx = x[1] - x[0]

    # Compute KDE density
    rho = np.zeros_like(x)
    rho_prime = np.zeros_like(x)

    for z in zeros:
        gauss = np.exp(-0.5 * ((x - z) / bandwidth)**2) / (bandwidth * np.sqrt(2*np.pi))
        gauss_prime = gauss * (-(x - z) / bandwidth**2)
        rho += gauss
        rho_prime += gauss_prime

    rho /= len(zeros)
    rho_prime /= len(zeros)

    # Normalize
    norm = np.sum(rho) * dx
    rho /= norm
    rho_prime /= norm

    # Fisher information: I = integral (rho')^2 / rho dx
    mask = rho > 1e-30
    fisher = np.sum(rho_prime[mask]**2 / rho[mask]) * dx

    # Entropy: S = -integral rho log(rho) dx
    entropy = -np.sum(rho[mask] * np.log(rho[mask])) * dx

    return fisher, entropy, rho, x


def compute_perturbative_fisher(zeros, beta=2.0):
    """
    Compute the perturbative Fisher information from findings.md.
    For each zero pair at (1/2 + i*gamma_n, 1/2 - i*gamma_n),
    the perturbative Fisher info is:

    I_n(sigma; beta, t) = [t^2 + (sigma-1)^2]/(beta + 1 - 2*sigma)
                        + [t^2 + sigma^2]/(2*sigma + beta - 1)

    With sigma = 1/2 (all zeros on critical line):
    I_n(1/2; beta, t) = [t^2 + 1/4] / beta  +  [t^2 + 1/4] / beta
                       = 2[t^2 + 1/4] / beta
    """
    sigma = 0.5
    I_total = 0.0
    for gamma_n in zeros:
        t_n = gamma_n  # imaginary part
        term1 = (t_n**2 + (sigma - 1)**2) / (beta + 1 - 2*sigma)
        term2 = (t_n**2 + sigma**2) / (2*sigma + beta - 1)
        I_total += term1 + term2
    return I_total


def compute_gap_statistics(zeros):
    """Compute statistics of the zero gap distribution."""
    sorted_zeros = np.sort(zeros)
    gaps = np.diff(sorted_zeros)
    return {
        "mean_gap": float(np.mean(gaps)),
        "std_gap": float(np.std(gaps)),
        "min_gap": float(np.min(gaps)),
        "max_gap": float(np.max(gaps)),
        "gap_ratio_mean": float(np.mean(gaps[1:] / gaps[:-1])),
    }


# ================================================================
# Main computation: Integrate the ODE and compute statistics at each t
# ================================================================

print("\n=== Integrating Coulomb ODE forward: t in [0, 0.5] ===")

x0 = np.array(zeta_zeros)
t_values = np.linspace(0, 0.5, 101)

sol = solve_ivp(
    coulomb_rhs, (0, 0.5), x0,
    method='RK45', t_eval=t_values,
    rtol=1e-10, atol=1e-12,
    max_step=0.001
)

print(f"ODE integration: success={sol.success}, reached t={sol.t[-1]:.4f}")

# Compute Fisher info, entropy at each time step
print("\n=== Computing Fisher information and entropy vs t ===\n")

# Fixed bandwidth and range for consistency
bw = 2.0  # bandwidth for KDE
x_range = (0, 160)

results = {
    "t": [],
    "fisher_kde": [],
    "entropy_kde": [],
    "fisher_pert": [],
    "mean_gap": [],
    "min_gap": [],
    "L2_distance": [],  # L2 distance from t=0 density
}

# Compute reference density at t=0
F0, S0, rho0, x_grid = compute_density_fisher_entropy(x0, bandwidth=bw, x_range=x_range)

step = max(1, len(sol.t) // 50)  # sample 50 time points
for idx in range(0, len(sol.t), step):
    t_val = sol.t[idx]
    zeros_at_t = sol.y[:, idx]

    # KDE-based Fisher and entropy
    F, S, rho_t, x_grid_t = compute_density_fisher_entropy(
        zeros_at_t, bandwidth=bw, x_range=x_range
    )

    # Perturbative Fisher (all sigma = 1/2 for t >= 0)
    F_pert = compute_perturbative_fisher(zeros_at_t, beta=2.0)

    # Gap statistics
    gaps = compute_gap_statistics(zeros_at_t)

    # L2 distance from t=0 density
    dx = x_grid[1] - x_grid[0]
    L2_dist = np.sqrt(np.sum((rho_t - rho0)**2) * dx)

    results["t"].append(float(t_val))
    results["fisher_kde"].append(float(F))
    results["entropy_kde"].append(float(S))
    results["fisher_pert"].append(float(F_pert))
    results["mean_gap"].append(gaps["mean_gap"])
    results["min_gap"].append(gaps["min_gap"])
    results["L2_distance"].append(float(L2_dist))

    if idx % (step * 5) == 0:
        print(f"t={t_val:.3f}: F_kde={F:.4f}, S={S:.6f}, F_pert={F_pert:.2f}, "
              f"min_gap={gaps['min_gap']:.6f}, L2={L2_dist:.8f}")


# ================================================================
# Investigation 2: dS/dt near t = 0 (de Bruijn's identity check)
# ================================================================

print("\n\n=== Investigation 2: Entropy production rate near t=0 ===")
print("de Bruijn's identity: dS/dt = (1/2) I(t)\n")

# Compute S(t) at very fine resolution near t=0
t_fine = np.linspace(0, 0.05, 51)
sol_fine = solve_ivp(
    coulomb_rhs, (0, 0.05), x0,
    method='RK45', t_eval=t_fine,
    rtol=1e-12, atol=1e-14,
    max_step=0.0001
)

S_fine = []
F_fine = []
for idx in range(len(sol_fine.t)):
    zeros_t = sol_fine.y[:, idx]
    F, S, _, _ = compute_density_fisher_entropy(zeros_t, bandwidth=bw, x_range=x_range)
    S_fine.append(S)
    F_fine.append(F)

S_fine = np.array(S_fine)
F_fine = np.array(F_fine)

# Numerical derivative of S
dt = t_fine[1] - t_fine[0]
dSdt = np.gradient(S_fine, dt)

print(f"{'t':>8s}  {'S(t)':>12s}  {'dS/dt':>12s}  {'I(t)/2':>12s}  {'ratio':>10s}")
for i in range(0, len(t_fine), 5):
    ratio = dSdt[i] / (0.5 * F_fine[i]) if abs(F_fine[i]) > 1e-10 else float('nan')
    print(f"{t_fine[i]:8.4f}  {S_fine[i]:12.8f}  {dSdt[i]:12.8f}  {0.5*F_fine[i]:12.8f}  {ratio:10.6f}")


# ================================================================
# Investigation 3: Monotone functionals
# ================================================================

print("\n\n=== Investigation 3: Monotone functionals ===")
print("Looking for Psi(t) monotone with Psi(0) = 0.\n")

t_arr = np.array(results["t"])
F_kde_arr = np.array(results["fisher_kde"])
S_arr = np.array(results["entropy_kde"])
F_pert_arr = np.array(results["fisher_pert"])
L2_arr = np.array(results["L2_distance"])

# Candidate 1: Psi_1(t) = F_kde(t) - F_kde(0)
Psi1 = F_kde_arr - F_kde_arr[0]
mono1 = all(Psi1[i] <= Psi1[i+1] for i in range(len(Psi1)-1))
print(f"Psi_1 = F_kde(t) - F_kde(0): monotone increasing? {mono1}")
print(f"  Values: {Psi1[0]:.6f}, {Psi1[len(Psi1)//4]:.6f}, {Psi1[len(Psi1)//2]:.6f}, {Psi1[-1]:.6f}")

# Candidate 2: Psi_2(t) = S(t) - S(0)
Psi2 = S_arr - S_arr[0]
mono2 = all(Psi2[i] <= Psi2[i+1] for i in range(len(Psi2)-1))
print(f"\nPsi_2 = S(t) - S(0): monotone increasing? {mono2}")
print(f"  Values: {Psi2[0]:.8f}, {Psi2[len(Psi2)//4]:.8f}, {Psi2[len(Psi2)//2]:.8f}, {Psi2[-1]:.8f}")

# Candidate 3: Psi_3(t) = L2 distance from t=0 density
mono3 = all(L2_arr[i] <= L2_arr[i+1] for i in range(len(L2_arr)-1))
print(f"\nPsi_3 = ||rho_t - rho_0||_2: monotone increasing? {mono3}")
print(f"  Values: {L2_arr[0]:.8f}, {L2_arr[len(L2_arr)//4]:.8f}, {L2_arr[len(L2_arr)//2]:.8f}, {L2_arr[-1]:.8f}")

# Candidate 4: Psi_4(t) = F_pert(t) - F_pert(0)
Psi4 = F_pert_arr - F_pert_arr[0]
mono4 = all(Psi4[i] <= Psi4[i+1] for i in range(len(Psi4)-1))
print(f"\nPsi_4 = F_pert(t) - F_pert(0): monotone increasing? {mono4}")
print(f"  Values: {Psi4[0]:.4f}, {Psi4[len(Psi4)//4]:.4f}, {Psi4[len(Psi4)//2]:.4f}, {Psi4[-1]:.4f}")

# Candidate 5: Psi_5(t) = -min_gap(t)  (should decrease as zeros spread)
min_gap_arr = np.array(results["min_gap"])
Psi5 = -(min_gap_arr - min_gap_arr[0])
mono5_inc = all(Psi5[i] <= Psi5[i+1] for i in range(len(Psi5)-1))
mono5_dec = all(min_gap_arr[i] >= min_gap_arr[i+1] for i in range(len(min_gap_arr)-1))
print(f"\nmin_gap(t): monotone decreasing? {mono5_dec}")
print(f"  Values: {min_gap_arr[0]:.6f}, {min_gap_arr[len(min_gap_arr)//4]:.6f}, "
      f"{min_gap_arr[len(min_gap_arr)//2]:.6f}, {min_gap_arr[-1]:.6f}")

# Candidate 6: Wasserstein distance
# W_1(rho_t, rho_0) = integral |F_t(x) - F_0(x)| dx (1-Wasserstein via CDFs)
print("\n\nDetailed table of functionals:")
print(f"{'t':>8s}  {'F_kde':>10s}  {'S':>12s}  {'F_pert':>12s}  {'L2':>12s}  {'min_gap':>10s}")
for i in range(len(results["t"])):
    print(f"{results['t'][i]:8.3f}  {results['fisher_kde'][i]:10.4f}  "
          f"{results['entropy_kde'][i]:12.8f}  {results['fisher_pert'][i]:12.2f}  "
          f"{results['L2_distance'][i]:12.8f}  {results['min_gap'][i]:10.6f}")


# Save all results
output = {
    "parameters": {
        "N_zeros": N,
        "bandwidth": bw,
        "x_range": list(x_range),
    },
    "time_series": results,
    "de_bruijn_identity_check": {
        "t_fine": t_fine.tolist(),
        "S_fine": S_fine.tolist(),
        "dSdt": dSdt.tolist(),
        "half_I": (0.5 * F_fine).tolist(),
    },
    "monotonicity": {
        "F_kde_monotone_increasing": bool(mono1),
        "S_monotone_increasing": bool(mono2),
        "L2_monotone_increasing": bool(mono3),
        "F_pert_monotone_increasing": bool(mono4),
    }
}

with open("/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/squeeze-lambda/fisher_entropy_results.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

print("\n\nResults saved to fisher_entropy_results.json")
