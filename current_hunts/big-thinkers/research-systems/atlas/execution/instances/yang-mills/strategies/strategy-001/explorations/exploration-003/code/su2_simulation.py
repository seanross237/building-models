"""
SU(2) Lattice Gauge Theory — Full Monte Carlo Simulation
=========================================================

Numba-optimized implementation for computing mass gap observables.
Uses heat bath algorithm (Kennedy-Pendleton) for SU(2).

Author: Math Explorer (Atlas system)
Date: 2026-03-27
"""

import numpy as np
from numba import njit, prange
from time import time
import json
import os
import sys

# ============================================================================
# SU(2) quaternion operations — Numba-compatible
# ============================================================================

@njit
def qmul(a, b):
    """Multiply two quaternions representing SU(2) elements."""
    c = np.empty(4)
    c[0] = a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3]
    c[1] = a[0]*b[1] + a[1]*b[0] + a[2]*b[3] - a[3]*b[2]
    c[2] = a[0]*b[2] - a[1]*b[3] + a[2]*b[0] + a[3]*b[1]
    c[3] = a[0]*b[3] + a[1]*b[2] - a[2]*b[1] + a[3]*b[0]
    return c

@njit
def qdag(a):
    """Hermitian conjugate of SU(2) quaternion."""
    c = np.empty(4)
    c[0] = a[0]
    c[1] = -a[1]
    c[2] = -a[2]
    c[3] = -a[3]
    return c

@njit
def qnorm(a):
    """Norm of quaternion."""
    return np.sqrt(a[0]**2 + a[1]**2 + a[2]**2 + a[3]**2)

@njit
def qnormalize(a):
    """Normalize quaternion to unit norm."""
    n = qnorm(a)
    if n > 0:
        return a / n
    else:
        r = np.array([1.0, 0.0, 0.0, 0.0])
        return r

# ============================================================================
# Kennedy-Pendleton heat bath for SU(2)
# ============================================================================

@njit
def kennedy_pendleton(bk):
    """
    Sample a0 from P(a0) ~ exp(bk * a0) * sqrt(1 - a0^2) on [-1, 1]
    using the Kennedy-Pendleton algorithm.
    """
    if bk < 0.01:
        # Essentially flat — just sample uniformly on S3
        # a0 is distributed as sqrt(1-a0^2) on [-1,1], CDF is known
        # Use rejection: P(a0) ~ sqrt(1-a0^2)
        while True:
            a0 = 2.0 * np.random.random() - 1.0
            if np.random.random() < np.sqrt(1.0 - a0**2):
                return a0

    while True:
        r1 = np.random.random()
        r2 = np.random.random()
        r3 = np.random.random()

        if r1 < 1e-300 or r3 < 1e-300:
            continue

        lam = -1.0 / bk * (np.log(r1) + np.log(r3) * (np.cos(2.0 * np.pi * r2))**2)

        if lam > 2.0:
            continue

        r4 = np.random.random()
        if r4 * r4 <= 1.0 - lam / 2.0:
            return 1.0 - lam


@njit
def heat_bath_update(links, x0, x1, x2, x3, mu, beta, L):
    """
    Perform heat bath update for a single link at site (x0,x1,x2,x3) in direction mu.
    """
    # Compute staple sum
    A = np.zeros(4)

    for nu in range(4):
        if nu == mu:
            continue

        # Shifted indices with periodic BC
        # x + mu
        xm = np.array([x0, x1, x2, x3])
        xm[mu] = (xm[mu] + 1) % L

        # x + nu
        xn = np.array([x0, x1, x2, x3])
        xn[nu] = (xn[nu] + 1) % L

        # x + mu - nu
        xmn = np.array([x0, x1, x2, x3])
        xmn[mu] = (xmn[mu] + 1) % L
        xmn[nu] = (xmn[nu] - 1) % L

        # x - nu
        xneg = np.array([x0, x1, x2, x3])
        xneg[nu] = (xneg[nu] - 1) % L

        # Forward staple: U_nu(x+mu) * U_mu(x+nu)^dag * U_nu(x)^dag
        U1 = links[xm[0], xm[1], xm[2], xm[3], nu]
        U2 = qdag(links[xn[0], xn[1], xn[2], xn[3], mu])
        U3 = qdag(links[x0, x1, x2, x3, nu])
        fwd = qmul(qmul(U1, U2), U3)

        # Backward staple: U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)
        U4 = qdag(links[xmn[0], xmn[1], xmn[2], xmn[3], nu])
        U5 = qdag(links[xneg[0], xneg[1], xneg[2], xneg[3], mu])
        U6 = links[xneg[0], xneg[1], xneg[2], xneg[3], nu]
        bwd = qmul(qmul(U4, U5), U6)

        A[0] += fwd[0] + bwd[0]
        A[1] += fwd[1] + bwd[1]
        A[2] += fwd[2] + bwd[2]
        A[3] += fwd[3] + bwd[3]

    # Compute k = |A|
    k = qnorm(A)

    if k < 1e-10:
        # Random SU(2) element
        r = np.random.randn(4)
        links[x0, x1, x2, x3, mu] = r / np.sqrt(r[0]**2 + r[1]**2 + r[2]**2 + r[3]**2)
        return

    # V = A / k (normalized)
    V = A / k

    # Sample a0 from the heat bath distribution
    bk = beta * k
    a0 = kennedy_pendleton(bk)

    # Generate remaining components uniformly on sphere of radius sqrt(1-a0^2)
    r = np.sqrt(max(1.0 - a0**2, 0.0))
    phi = 2.0 * np.pi * np.random.random()
    cos_theta = 2.0 * np.random.random() - 1.0
    sin_theta = np.sqrt(max(1.0 - cos_theta**2, 0.0))

    U_new = np.empty(4)
    U_new[0] = a0
    U_new[1] = r * sin_theta * np.cos(phi)
    U_new[2] = r * sin_theta * np.sin(phi)
    U_new[3] = r * cos_theta

    # New link = U_new * V^dagger
    result = qmul(U_new, qdag(V))

    # Normalize for numerical stability
    links[x0, x1, x2, x3, mu] = qnormalize(result)


@njit
def heatbath_sweep(links, beta, L):
    """Perform one full heat bath sweep over all links."""
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    for mu in range(4):
                        heat_bath_update(links, x0, x1, x2, x3, mu, beta, L)


# ============================================================================
# Measurements
# ============================================================================

@njit
def measure_avg_plaquette(links, L):
    """Compute average plaquette (1/2) Re Tr U_P averaged over all plaquettes."""
    total = 0.0
    count = 0

    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    for mu in range(4):
                        for nu in range(mu+1, 4):
                            # Plaquette: U_mu(x) U_nu(x+mu) U_mu(x+nu)^dag U_nu(x)^dag
                            xm = np.array([x0, x1, x2, x3])
                            xm[mu] = (xm[mu] + 1) % L
                            xn = np.array([x0, x1, x2, x3])
                            xn[nu] = (xn[nu] + 1) % L

                            U1 = links[x0, x1, x2, x3, mu]
                            U2 = links[xm[0], xm[1], xm[2], xm[3], nu]
                            U3 = qdag(links[xn[0], xn[1], xn[2], xn[3], mu])
                            U4 = qdag(links[x0, x1, x2, x3, nu])

                            P = qmul(qmul(qmul(U1, U2), U3), U4)
                            total += P[0]  # (1/2) Re Tr
                            count += 1

    return total / count


@njit
def measure_wilson_loop(links, L, R, T):
    """
    Measure average Wilson loop W(R,T).
    R = spatial extent, T = temporal extent.
    Average over all positions and 3 spatial-temporal plane orientations.
    Returns <(1/2) Re Tr W(R,T)>.
    """
    total = 0.0
    count = 0
    temporal_dir = 0  # direction 0 is time

    for spatial_dir in range(1, 4):  # directions 1,2,3 are spatial
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        # Compute Wilson loop
                        site = np.array([x0, x1, x2, x3])
                        U = np.array([1.0, 0.0, 0.0, 0.0])  # identity

                        # Bottom: R steps in spatial direction
                        s = site.copy()
                        for _ in range(R):
                            U = qmul(U, links[s[0], s[1], s[2], s[3], spatial_dir])
                            s[spatial_dir] = (s[spatial_dir] + 1) % L

                        # Right: T steps in temporal direction
                        for _ in range(T):
                            U = qmul(U, links[s[0], s[1], s[2], s[3], temporal_dir])
                            s[temporal_dir] = (s[temporal_dir] + 1) % L

                        # Top: R steps backwards in spatial direction
                        for _ in range(R):
                            s[spatial_dir] = (s[spatial_dir] - 1) % L
                            U = qmul(U, qdag(links[s[0], s[1], s[2], s[3], spatial_dir]))

                        # Left: T steps backwards in temporal direction
                        for _ in range(T):
                            s[temporal_dir] = (s[temporal_dir] - 1) % L
                            U = qmul(U, qdag(links[s[0], s[1], s[2], s[3], temporal_dir]))

                        total += U[0]  # (1/2) Re Tr
                        count += 1

    return total / count


@njit
def measure_spatial_plaquette_timeslice(links, L, t):
    """
    Average spatial plaquette at time slice t.
    Only plaquettes in spatial planes (mu,nu both in {1,2,3}).
    """
    total = 0.0
    count = 0

    for x1 in range(L):
        for x2 in range(L):
            for x3 in range(L):
                for mu in range(1, 4):
                    for nu in range(mu+1, 4):
                        xm = np.array([t, x1, x2, x3])
                        xm[mu] = (xm[mu] + 1) % L
                        xn = np.array([t, x1, x2, x3])
                        xn[nu] = (xn[nu] + 1) % L

                        U1 = links[t, x1, x2, x3, mu]
                        U2 = links[xm[0], xm[1], xm[2], xm[3], nu]
                        U3 = qdag(links[xn[0], xn[1], xn[2], xn[3], mu])
                        U4 = qdag(links[t, x1, x2, x3, nu])

                        P = qmul(qmul(qmul(U1, U2), U3), U4)
                        total += P[0]
                        count += 1

    return total / count


@njit
def measure_plaquette_correlator(links, L):
    """
    Measure the plaquette-plaquette correlator C(dt) for all dt.
    C(dt) = <P(0)P(dt)> - <P>^2  (connected correlator)
    where P(t) is the spatially-averaged plaquette at time t.
    Returns array of C(dt) for dt = 0, 1, ..., L-1.
    """
    # Compute P(t) for each time slice
    plaq_t = np.empty(L)
    for t in range(L):
        plaq_t[t] = measure_spatial_plaquette_timeslice(links, L, t)

    mean_plaq = 0.0
    for t in range(L):
        mean_plaq += plaq_t[t]
    mean_plaq /= L

    # Connected correlator
    corr = np.zeros(L)
    for dt in range(L):
        for t in range(L):
            t2 = (t + dt) % L
            corr[dt] += (plaq_t[t] - mean_plaq) * (plaq_t[t2] - mean_plaq)
        corr[dt] /= L

    return corr


@njit
def measure_polyakov_loop(links, L):
    """Compute average Polyakov loop |<L>|."""
    total_re = 0.0
    total_im = 0.0  # We won't use imaginary part for (1/2)ReTr

    for x1 in range(L):
        for x2 in range(L):
            for x3 in range(L):
                U = np.array([1.0, 0.0, 0.0, 0.0])
                for t in range(L):
                    U = qmul(U, links[t, x1, x2, x3, 0])
                total_re += U[0]

    return total_re / (L**3)


# ============================================================================
# Main simulation
# ============================================================================

def run_simulation(L, beta, n_therm, n_meas, meas_interval=5, seed=42):
    """
    Run full Monte Carlo simulation and return measurements.

    Parameters:
        L: lattice size (L^4 lattice)
        beta: inverse coupling
        n_therm: number of thermalization sweeps
        n_meas: number of measurement sweeps
        meas_interval: measure every N sweeps
        seed: random seed
    """
    np.random.seed(seed)

    # Initialize lattice — hot start
    links = np.random.randn(L, L, L, L, 4, 4)
    # Normalize to SU(2)
    norms = np.sqrt(np.sum(links**2, axis=-1, keepdims=True))
    links = links / norms

    print(f"  L={L}, beta={beta:.2f}: Starting simulation...")
    print(f"  {n_therm} thermalization + {n_meas} measurement sweeps")

    # JIT warmup (first call compiles)
    t0 = time()
    heatbath_sweep(links, beta, L)
    t_compile = time() - t0
    print(f"  JIT compile + first sweep: {t_compile:.1f}s")

    # Thermalization
    t0 = time()
    for i in range(n_therm - 1):
        heatbath_sweep(links, beta, L)
        if (i+1) % max(1, n_therm//5) == 0:
            plaq = measure_avg_plaquette(links, L)
            print(f"  Therm sweep {i+2}/{n_therm}: <P> = {plaq:.6f}")
    t_therm = time() - t0
    print(f"  Thermalization done in {t_therm:.1f}s")

    # Measurements
    plaquettes = []
    polyakov_loops = []
    wilson_loops = {}  # (R,T) -> list of measurements
    plaq_correlators = []

    # Wilson loop sizes to measure
    max_R = min(L//2, 4)
    max_T = min(L//2, 4)
    for R in range(1, max_R + 1):
        for T in range(1, max_T + 1):
            wilson_loops[(R, T)] = []

    t0 = time()
    for i in range(n_meas):
        # Do meas_interval sweeps between measurements
        for _ in range(meas_interval):
            heatbath_sweep(links, beta, L)

        # Measure average plaquette
        plaq = measure_avg_plaquette(links, L)
        plaquettes.append(plaq)

        # Measure Polyakov loop
        poly = measure_polyakov_loop(links, L)
        polyakov_loops.append(poly)

        # Measure Wilson loops
        for R in range(1, max_R + 1):
            for T in range(1, max_T + 1):
                W = measure_wilson_loop(links, L, R, T)
                wilson_loops[(R, T)].append(W)

        # Measure plaquette correlator
        corr = measure_plaquette_correlator(links, L)
        plaq_correlators.append(corr)

        if (i+1) % max(1, n_meas//5) == 0:
            elapsed = time() - t0
            print(f"  Meas {i+1}/{n_meas}: <P>={plaq:.6f}, <L>={poly:.6f}, elapsed={elapsed:.1f}s")

    t_meas = time() - t0
    print(f"  Measurements done in {t_meas:.1f}s")

    # Compile results
    results = {
        'L': L,
        'beta': beta,
        'n_therm': n_therm,
        'n_meas': n_meas,
        'meas_interval': meas_interval,
        'seed': seed,
        'plaquette_mean': float(np.mean(plaquettes)),
        'plaquette_std': float(np.std(plaquettes)),
        'plaquette_err': float(np.std(plaquettes) / np.sqrt(len(plaquettes))),
        'polyakov_mean': float(np.mean(polyakov_loops)),
        'polyakov_std': float(np.std(polyakov_loops)),
        'wilson_loops': {},
        'plaq_correlator_mean': [float(x) for x in np.mean(plaq_correlators, axis=0)],
        'plaq_correlator_err': [float(x) for x in np.std(plaq_correlators, axis=0) / np.sqrt(len(plaq_correlators))],
    }

    for (R, T), vals in wilson_loops.items():
        key = f"{R},{T}"
        results['wilson_loops'][key] = {
            'mean': float(np.mean(vals)),
            'std': float(np.std(vals)),
            'err': float(np.std(vals) / np.sqrt(len(vals))),
        }

    return results


def compute_creutz_ratios(results):
    """
    Compute Creutz ratios from Wilson loop data:
    chi(R,T) = -ln(W(R,T) * W(R-1,T-1) / (W(R-1,T) * W(R,T-1)))

    The Creutz ratio approaches the string tension sigma in the confined phase.
    """
    wl = results['wilson_loops']
    creutz = {}

    for key in wl:
        R, T = map(int, key.split(','))
        if R >= 2 and T >= 2:
            k_RT = f"{R},{T}"
            k_R1T1 = f"{R-1},{T-1}"
            k_R1T = f"{R-1},{T}"
            k_RT1 = f"{R},{T-1}"

            if all(k in wl for k in [k_RT, k_R1T1, k_R1T, k_RT1]):
                W_RT = wl[k_RT]['mean']
                W_R1T1 = wl[k_R1T1]['mean']
                W_R1T = wl[k_R1T]['mean']
                W_RT1 = wl[k_RT1]['mean']

                # Creutz ratio
                ratio = (W_RT * W_R1T1) / (W_R1T * W_RT1)
                if ratio > 0:
                    chi = -np.log(ratio)
                    creutz[f"{R},{T}"] = float(chi)

                    # Error estimation via error propagation (simplified)
                    # delta_chi ~ sqrt(sum of (delta_W/W)^2) approximately
                    rel_errs = []
                    for k in [k_RT, k_R1T1, k_R1T, k_RT1]:
                        if abs(wl[k]['mean']) > 1e-10:
                            rel_errs.append(wl[k]['err'] / abs(wl[k]['mean']))
                    if rel_errs:
                        creutz[f"{R},{T}_err"] = float(np.sqrt(sum(e**2 for e in rel_errs)))

    return creutz


def extract_glueball_mass(correlator_mean, correlator_err, L):
    """
    Extract effective glueball mass from plaquette correlator.
    C(t) ~ A * (exp(-m*t) + exp(-m*(L-t))) for periodic BC.

    Effective mass: m_eff(t) = ln(C(t) / C(t+1))
    """
    masses = {}
    for t in range(1, L//2):
        c_t = correlator_mean[t]
        c_t1 = correlator_mean[t+1] if t+1 < L else correlator_mean[0]

        if c_t > 0 and c_t1 > 0:
            m_eff = np.log(c_t / c_t1)
            # Error from propagation
            if correlator_err[t] > 0 and correlator_err[t+1] > 0:
                err = np.sqrt((correlator_err[t]/c_t)**2 + (correlator_err[t+1]/c_t1)**2)
            else:
                err = 0.0
            masses[t] = {'mass': float(m_eff), 'err': float(err)}

    return masses


def main():
    """Run the full simulation suite."""
    output_dir = os.path.dirname(os.path.abspath(__file__))
    results_file = os.path.join(output_dir, 'results.json')

    all_results = {}

    # Simulation parameters
    # Small lattices first, then larger ones
    configs = [
        # (L, beta, n_therm, n_meas, meas_interval)
        # 4^4: ~10s each, total ~50s
        (4, 2.0, 200, 200, 5),
        (4, 2.2, 200, 200, 5),
        (4, 2.3, 200, 200, 5),
        (4, 2.5, 200, 200, 5),
        (4, 3.0, 200, 200, 5),
        # 6^4: ~50s each, total ~250s
        (6, 2.0, 150, 100, 5),
        (6, 2.2, 150, 100, 5),
        (6, 2.3, 150, 100, 5),
        (6, 2.5, 150, 100, 5),
        (6, 3.0, 150, 100, 5),
        # 8^4: ~3min each, total ~9min
        (8, 2.2, 100, 60, 5),
        (8, 2.3, 100, 60, 5),
        (8, 2.5, 100, 60, 5),
    ]

    print("=" * 70)
    print("SU(2) Lattice Gauge Theory — Mass Gap Observables")
    print("=" * 70)
    print()

    for i, (L, beta, n_therm, n_meas, meas_int) in enumerate(configs):
        print(f"\n{'='*60}")
        print(f"Configuration {i+1}/{len(configs)}: L={L}, beta={beta}")
        print(f"{'='*60}")

        t0 = time()
        results = run_simulation(L, beta, n_therm, n_meas, meas_int, seed=42+i)
        elapsed = time() - t0
        print(f"  Total time: {elapsed:.1f}s")

        # Compute derived quantities
        results['creutz_ratios'] = compute_creutz_ratios(results)
        results['effective_masses'] = extract_glueball_mass(
            results['plaq_correlator_mean'],
            results['plaq_correlator_err'],
            L
        )

        key = f"L{L}_beta{beta}"
        all_results[key] = results

        # Print summary
        print(f"\n  Results for L={L}, beta={beta}:")
        print(f"    <P> = {results['plaquette_mean']:.6f} ± {results['plaquette_err']:.6f}")
        print(f"    <L_Polyakov> = {results['polyakov_mean']:.6f}")

        # Wilson loops
        for wl_key, data in sorted(results['wilson_loops'].items()):
            print(f"    W({wl_key}) = {data['mean']:.6f} ± {data['err']:.6f}")

        # Creutz ratios
        for key_cr, val in sorted(results['creutz_ratios'].items()):
            if not key_cr.endswith('_err'):
                err_key = key_cr + '_err'
                err = results['creutz_ratios'].get(err_key, 0)
                print(f"    chi({key_cr}) = {val:.6f} ± {err:.6f}")

        # Glueball masses
        if results['effective_masses']:
            print(f"    Effective masses:")
            for t, data in sorted(results['effective_masses'].items()):
                print(f"      m_eff(t={t}) = {data['mass']:.4f} ± {data['err']:.4f}")

        # Save incremental results
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        print(f"  Results saved to {results_file}")

    print(f"\n{'='*60}")
    print("All simulations complete!")
    print(f"{'='*60}")

    return all_results


if __name__ == "__main__":
    results = main()
