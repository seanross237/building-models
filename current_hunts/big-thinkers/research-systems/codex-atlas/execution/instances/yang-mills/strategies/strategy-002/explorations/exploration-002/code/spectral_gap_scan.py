"""
spectral_gap_scan.py
====================
Measure the MCMC spectral gap proxy (integrated autocorrelation time tau_int of the
average plaquette) for SU(2) lattice Yang-Mills on a 4^4 lattice.

Beta values: 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 3.0
Spectral gap proxy: gamma = 1 / (2 * tau_int)

Uses SU(2) code logic from exploration-003 (Kennedy-Pendleton heat bath)
and autocorr methods from exploration-008.

CORRECTNESS NOTE: Uses checkerboard decomposition for proper Gibbs updates.
"""

import numpy as np
import sys
import os
import json
import time

# ─────────────────────────────────────────────────────────
# SU(2) GROUP OPERATIONS
# ─────────────────────────────────────────────────────────

def su2_mul(q1, q2):
    """Vectorized quaternion multiply. q shape: (..., 4)"""
    a0, a1, a2, a3 = q1[...,0], q1[...,1], q1[...,2], q1[...,3]
    b0, b1, b2, b3 = q2[...,0], q2[...,1], q2[...,2], q2[...,3]
    out = np.empty_like(q1)
    out[...,0] = a0*b0 - a1*b1 - a2*b2 - a3*b3
    out[...,1] = a0*b1 + a1*b0 + a2*b3 - a3*b2
    out[...,2] = a0*b2 - a1*b3 + a2*b0 + a3*b1
    out[...,3] = a0*b3 + a1*b2 - a2*b1 + a3*b0
    return out

def su2_dag(q):
    """Hermitian conjugate: negate vector part."""
    r = q.copy()
    r[...,1:] *= -1
    return r

def su2_rand(shape):
    """Haar-random SU(2) elements. shape gives batch dims; output has extra last dim 4."""
    q = np.random.randn(*shape, 4)
    q /= np.linalg.norm(q, axis=-1, keepdims=True)
    return q


# ─────────────────────────────────────────────────────────
# AVERAGE PLAQUETTE (vectorized)
# ─────────────────────────────────────────────────────────

def avg_plaquette(links, L):
    """
    links shape: (L,L,L,L, 4, 4)  axes: x0,x1,x2,x3, mu, quat
    Returns average (1/2) Re Tr U_P over all plaquettes.
    """
    total = 0.0
    count = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            U1 = links[:,:,:,:, mu, :]
            U2 = np.roll(links[:,:,:,:, nu, :], -1, axis=mu)
            U3 = su2_dag(np.roll(links[:,:,:,:, mu, :], -1, axis=nu))
            U4 = su2_dag(links[:,:,:,:, nu, :])
            prod = su2_mul(su2_mul(su2_mul(U1, U2), U3), U4)
            total += np.sum(prod[...,0])
            count += L**4
    return total / count


# ─────────────────────────────────────────────────────────
# STAPLE SUM for a subset of sites (vectorized)
# ─────────────────────────────────────────────────────────

def staple_sum_for_mu_parity(links, L, mu, parity):
    """
    Compute the staple sum A[x, mu] for all sites x with
    parity = (x0+x1+x2+x3) % 2.

    Returns A[mask, 4] where mask picks out the sites with given parity.
    Also returns the site mask (shape L^4).

    The staple sum for link U_mu(x) is the sum over nu != mu of:
      Forward: U_nu(x+mu) * U_mu(x+nu)^dag * U_nu(x)^dag
      Backward: U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)

    For correct parallel updates: sites with the same (mu, parity) can be
    updated simultaneously because their staples depend only on links at
    OTHER (mu, parity) combinations (different direction or different parity).
    """
    # Build parity mask over full lattice
    x0, x1, x2, x3 = np.meshgrid(range(L), range(L), range(L), range(L), indexing='ij')
    par = (x0 + x1 + x2 + x3) % 2  # shape (L,L,L,L)
    mask = (par == parity)  # bool shape (L,L,L,L)

    A = np.zeros((L,L,L,L,4), dtype=np.float64)  # accumulate staple sum here

    for nu in range(4):
        if nu == mu:
            continue
        # Forward staple: U_nu(x+mu) * U_mu(x+nu)^dag * U_nu(x)^dag
        U_nu_xpmu = np.roll(links[:,:,:,:, nu, :], -1, axis=mu)
        U_mu_xpnu_dag = su2_dag(np.roll(links[:,:,:,:, mu, :], -1, axis=nu))
        U_nu_x_dag = su2_dag(links[:,:,:,:, nu, :])
        fwd = su2_mul(su2_mul(U_nu_xpmu, U_mu_xpnu_dag), U_nu_x_dag)

        # Backward staple: U_nu(x+mu-nu)^dag * U_mu(x-nu)^dag * U_nu(x-nu)
        U_nu_xpmu_mnu_dag = su2_dag(np.roll(np.roll(links[:,:,:,:, nu, :], -1, axis=mu), 1, axis=nu))
        U_mu_xmnu_dag = su2_dag(np.roll(links[:,:,:,:, mu, :], 1, axis=nu))
        U_nu_xmnu = np.roll(links[:,:,:,:, nu, :], 1, axis=nu)
        bwd = su2_mul(su2_mul(U_nu_xpmu_mnu_dag, U_mu_xmnu_dag), U_nu_xmnu)

        A += fwd + bwd

    # Extract only the masked sites
    return A[mask], mask  # shape (N_mask, 4) and (L,L,L,L)


# ─────────────────────────────────────────────────────────
# KENNEDY-PENDLETON SCALAR SAMPLER
# ─────────────────────────────────────────────────────────

def kp_sample_scalar(bk):
    """
    Sample a0 from P(a0) ~ exp(bk * a0) * sqrt(1 - a0^2) using KP algorithm.
    Single scalar version (correct reference implementation).
    """
    if bk < 0.01:
        return 2.0 * np.random.random() - 1.0
    while True:
        r1 = np.random.random()
        r2 = np.random.random()
        r3 = np.random.random()
        r1 = max(r1, 1e-300)
        r3 = max(r3, 1e-300)
        x = -(np.log(r1) + np.log(r3) * np.cos(np.pi * r2)**2) / bk
        if x > 2.0:
            continue
        r4 = np.random.random()
        if r4**2 <= 1.0 - x / 2.0:
            return 1.0 - x


def kp_sample_batch(bk_arr):
    """
    Sample a0 for a batch of bk values. Returns array same shape as bk_arr.
    Uses vectorized rejection sampling with automatic fallback for stragglers.
    """
    bk_flat = bk_arr.ravel().copy()
    n = len(bk_flat)
    a0_out = np.zeros(n)

    # Small bk: essentially uniform
    small = bk_flat < 0.01
    a0_out[small] = 2.0 * np.random.random(int(np.sum(small))) - 1.0

    needed = ~small
    if not np.any(needed):
        return a0_out.reshape(bk_arr.shape)

    idx_needed = np.where(needed)[0]

    # Vectorized rejection sampling — run in batches until all are filled
    MAX_ROUNDS = 500
    still_needed = np.ones(len(idx_needed), dtype=bool)

    for _ in range(MAX_ROUNDS):
        if not np.any(still_needed):
            break
        active = np.where(still_needed)[0]
        n_active = len(active)
        bk_a = bk_flat[idx_needed[active]]

        r1 = np.clip(np.random.random(n_active), 1e-300, 1.0)
        r2 = np.random.random(n_active)
        r3 = np.clip(np.random.random(n_active), 1e-300, 1.0)
        r4 = np.random.random(n_active)

        x = -(np.log(r1) + np.log(r3) * np.cos(np.pi * r2)**2) / bk_a
        accept = (x <= 2.0) & (r4**2 <= 1.0 - x / 2.0)

        accepted_positions = np.where(accept)[0]
        for pos in accepted_positions:
            global_idx = idx_needed[active[pos]]
            a0_out[global_idx] = 1.0 - x[pos]
            still_needed[active[pos]] = False

    # Fallback for any remaining (shouldn't happen in practice)
    for pos in np.where(still_needed)[0]:
        global_idx = idx_needed[pos]
        a0_out[global_idx] = kp_sample_scalar(bk_flat[global_idx])

    return a0_out.reshape(bk_arr.shape)


# ─────────────────────────────────────────────────────────
# HEAT BATH SWEEP WITH CHECKERBOARD
# ─────────────────────────────────────────────────────────

def heat_bath_sweep(links, L, beta):
    """
    One full heat bath sweep using checkerboard decomposition.
    For each (mu, parity) pair: update all mu-links at sites of given parity
    simultaneously (they are independent given other links).

    Total: 4 directions × 2 parities = 8 sub-sweeps per full sweep.
    """
    for mu in range(4):
        for parity in range(2):
            A_masked, mask = staple_sum_for_mu_parity(links, L, mu, parity)
            # A_masked shape: (N, 4) where N = number of sites with given parity

            # k = ||A|| for each site
            k = np.sqrt(np.sum(A_masked**2, axis=-1))  # shape (N,)

            # V = A / k (normalized to SU(2)), handle k=0 case
            k_safe = np.where(k < 1e-10, 1.0, k)
            V = A_masked / k_safe[:, np.newaxis]  # shape (N, 4)

            # bk = beta * k
            bk = beta * k  # shape (N,)

            # Sample a0 from P(a0) ~ exp(bk*a0) * sqrt(1-a0^2)
            a0 = kp_sample_batch(bk)  # shape (N,)

            # Generate random (a1,a2,a3) on sphere of radius sqrt(1-a0^2)
            r = np.sqrt(np.clip(1.0 - a0**2, 0.0, 1.0))
            phi = 2.0 * np.pi * np.random.random(len(a0))
            cos_th = 2.0 * np.random.random(len(a0)) - 1.0
            sin_th = np.sqrt(np.clip(1.0 - cos_th**2, 0.0, 1.0))

            # W in the "staple frame"
            W = np.stack([a0, r*sin_th*np.cos(phi), r*sin_th*np.sin(phi), r*cos_th], axis=-1)
            # shape (N, 4)

            # U_new = W * V^dag
            V_dag = su2_dag(V)
            U_new = su2_mul(W, V_dag)  # shape (N, 4)

            # For degenerate cases (k ~ 0), use random SU(2)
            degenerate = k < 1e-10
            if np.any(degenerate):
                rand_links = su2_rand((int(np.sum(degenerate)),))
                U_new[degenerate] = rand_links

            # Put updated links back
            links[:,:,:,:, mu, :][mask] = U_new

    return links


# ─────────────────────────────────────────────────────────
# AUTOCORRELATION ANALYSIS
# ─────────────────────────────────────────────────────────

def compute_autocorr(ts, max_lag=None):
    """Normalized autocorrelation C(t) = <δP(0) δP(t)> / <δP(0)^2>"""
    n = len(ts)
    if max_lag is None:
        max_lag = min(n // 4, 300)

    mean = np.mean(ts)
    delta = ts - mean
    var = np.mean(delta**2)

    if var < 1e-15:
        return np.array([1.0])

    ac = np.zeros(max_lag + 1)
    ac[0] = 1.0
    for lag in range(1, max_lag + 1):
        ac[lag] = np.mean(delta[:-lag] * delta[lag:]) / var

    return ac


def compute_tau_int(ac):
    """
    tau_int = 0.5 + sum_{t>=1} C(t)
    Stop at first negative or t > 6*tau_int (auto-window method).
    """
    tau = 0.5
    for t in range(1, len(ac)):
        if ac[t] < 0:
            break
        tau += ac[t]
        if t > 6 * tau:
            break
    return tau


# ─────────────────────────────────────────────────────────
# MAIN SCAN
# ─────────────────────────────────────────────────────────

def run_beta(beta, L=4, n_therm=500, n_meas=2000, seed=None):
    """Run simulation at a single beta. Returns dict with results."""
    if seed is not None:
        np.random.seed(seed)

    # Hot start
    links = su2_rand((L, L, L, L, 4))

    t0 = time.time()

    # Thermalization
    for i in range(n_therm):
        links = heat_bath_sweep(links, L, beta)

    # Measurement
    plaquettes = np.zeros(n_meas)
    for i in range(n_meas):
        links = heat_bath_sweep(links, L, beta)
        plaquettes[i] = avg_plaquette(links, L)

    elapsed = time.time() - t0

    mean_P = float(np.mean(plaquettes))
    std_P = float(np.std(plaquettes))

    ac = compute_autocorr(plaquettes, max_lag=min(n_meas // 4, 300))
    tau = compute_tau_int(ac)
    gamma = 1.0 / (2.0 * tau)

    return {
        'beta': float(beta),
        'mean_P': mean_P,
        'std_P': std_P,
        'tau_int': float(tau),
        'gamma': float(gamma),
        'elapsed': float(elapsed),
        'ac_1': float(ac[1]) if len(ac) > 1 else 0.0,
        'ac_5': float(ac[min(5, len(ac)-1)]),
        'ac_10': float(ac[min(10, len(ac)-1)]),
        'ac_20': float(ac[min(20, len(ac)-1)]),
    }


def main():
    beta_values = [0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 3.0]
    L = 4
    n_therm = 500
    n_meas = 2000

    print("=" * 70)
    print("SU(2) SPECTRAL GAP SCAN — 4^4 LATTICE (checkerboard heat bath)")
    print("=" * 70)
    print(f"L={L}, n_therm={n_therm}, n_meas={n_meas}")
    print(f"Beta values: {beta_values}")
    print(f"SZZ bound: beta < 1/48 = {1/48:.4f}")
    print("=" * 70)
    print()

    results = []

    for i, beta in enumerate(beta_values):
        seed = 42 + i * 13
        print(f"Running beta = {beta:.4f} (seed={seed})...", flush=True)

        try:
            r = run_beta(beta, L=L, n_therm=n_therm, n_meas=n_meas, seed=seed)
            results.append(r)
            print(f"  beta = {beta:.4f}: <P> = {r['mean_P']:.5f}  "
                  f"tau_int = {r['tau_int']:.2f}  gamma = {r['gamma']:.5f}  "
                  f"C(1)={r['ac_1']:.4f}  [{r['elapsed']:.0f}s]",
                  flush=True)
        except Exception as e:
            import traceback
            traceback.print_exc()
            results.append({'beta': float(beta), 'error': str(e)})

    # Summary table
    print()
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"{'beta':>7}  {'<P>':>8}  {'tau_int':>10}  {'gamma':>10}  {'C(1)':>8}  note")
    print("-" * 70)
    for r in results:
        if 'error' in r:
            print(f"{r['beta']:>7.4f}  ERROR: {r['error']}")
            continue
        note = ""
        if r['beta'] <= 1/48:
            note = "<-- SZZ proved"
        elif r['beta'] >= 2.0:
            note = "<-- physical region"
        print(f"{r['beta']:>7.4f}  {r['mean_P']:>8.5f}  {r['tau_int']:>10.2f}  "
              f"{r['gamma']:>10.5f}  {r['ac_1']:>8.4f}  {note}")

    good = [r for r in results if 'error' not in r]
    if len(good) >= 2:
        r0 = good[0]
        rlast = good[-1]
        ratio = rlast['tau_int'] / r0['tau_int']
        print()
        print(f"tau_int(beta={rlast['beta']:.2f}) / tau_int(beta={r0['beta']:.4f}) = {ratio:.2f}")
        print(f"(Higher tau_int => slower mixing => smaller spectral gap)")

    # Save JSON
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {out_path}")

    return results


if __name__ == "__main__":
    main()
