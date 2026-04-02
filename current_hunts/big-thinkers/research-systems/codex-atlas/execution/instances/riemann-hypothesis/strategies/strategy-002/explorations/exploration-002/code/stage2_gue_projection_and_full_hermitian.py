"""
Stage 2: Better optimization approaches

Key findings from Stage 1:
- Histogram-based loss has near-zero gradients → L-BFGS-B converges immediately
- Need either: (a) smooth differentiable loss, or (b) gradient-free optimizer

This script implements:
  Approach A: GUE projection onto circulant subspace (analytical)
  Approach B: Full Hermitian N=40 with smooth KDE loss + differential evolution
  Approach C: Von Mangoldt constrained, energy-based loss, gradient-free

Smooth loss options:
  1. KDE-based: fit Gaussian KDE to spacings, compare to Wigner surmise
  2. Wasserstein-1: Earth mover distance between spacing CDFs
  3. Log-energy: minimize GUE log-gas energy (but this gives clock config, not GUE)
  4. Cumulative distribution matching: L2 distance between CDFs
"""

import numpy as np
from scipy.optimize import minimize, differential_evolution
from scipy.stats import gaussian_kde
from scipy.fft import fft, ifft
import warnings
warnings.filterwarnings('ignore')

EXPLORATION_DIR = '/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-002'

# ─── GUE matrix generation ─────────────────────────────────────────────────────

def sample_gue(N, seed=None):
    """Sample an N×N GUE matrix."""
    if seed is not None:
        np.random.seed(seed)
    H = (np.random.randn(N, N) + 1j * np.random.randn(N, N)) / np.sqrt(2)
    return (H + H.conj().T) / np.sqrt(2 * N)  # Wigner normalization

def sample_goe(N, seed=None):
    """Sample an N×N GOE matrix."""
    if seed is not None:
        np.random.seed(seed)
    H = np.random.randn(N, N)
    return (H + H.T) / np.sqrt(2 * N)

# ─── Von Mangoldt ──────────────────────────────────────────────────────────────

def von_mangoldt_array(N):
    """Λ(k) for k = 0,...,N-1."""
    def vm(n):
        if n < 2: return 0.0
        for p in range(2, int(n**0.5) + 2):
            if p > n: break
            if n % p == 0:
                m = n
                while m % p == 0: m //= p
                return np.log(p) if m == 1 else 0.0
        return np.log(n)
    return np.array([vm(k) for k in range(N)])

# ─── Eigenvalue unfolding ──────────────────────────────────────────────────────

def unfold_eigenvalues(evals, poly_deg=8):
    """Polynomial unfolding of eigenvalue sequence."""
    evals_s = np.sort(evals)
    n = len(evals_s)
    x_min, x_max = evals_s[0], evals_s[-1]
    if x_max <= x_min:
        return np.linspace(0, n, n)
    x_norm = 2 * (evals_s - x_min) / (x_max - x_min) - 1
    y = np.arange(n)
    poly = np.polyfit(x_norm, y, poly_deg)
    return np.polyval(poly, x_norm)

# ─── Spacing distribution ──────────────────────────────────────────────────────

def get_normalized_spacings(evals):
    """Compute normalized nearest-neighbor spacings."""
    unf = unfold_eigenvalues(evals)
    s = np.diff(unf)
    s = s[s > 0]
    s = s / np.mean(s)
    return s

# ─── Reference distributions ──────────────────────────────────────────────────

def gue_wigner(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def goe_wigner(s):
    return (np.pi / 2.0) * s * np.exp(-np.pi * s**2 / 4.0)

def poisson_dist(s):
    return np.exp(-s)

# GUE CDF (numerical)
def gue_wigner_cdf(s_grid):
    """CDF of GUE Wigner surmise at points s_grid."""
    from scipy.integrate import cumulative_trapezoid
    s_dense = np.linspace(0, max(s_grid.max(), 5), 1000)
    p = gue_wigner(s_dense)
    cdf_dense = cumulative_trapezoid(p, s_dense, initial=0)
    cdf_dense = cdf_dense / cdf_dense[-1]  # normalize
    return np.interp(s_grid, s_dense, cdf_dense)

# ─── Smooth loss functions ─────────────────────────────────────────────────────

def kde_loss_gue(spacings, bandwidth=0.2):
    """KDE-based L2 loss between empirical spacing density and GUE Wigner surmise."""
    if len(spacings) < 20:
        return 1e6
    try:
        kde = gaussian_kde(spacings, bw_method=bandwidth)
        s_grid = np.linspace(0.01, 4.0, 80)
        p_kde = kde(s_grid)
        p_gue = gue_wigner(s_grid)
        return np.mean((p_kde - p_gue)**2)
    except:
        return 1e6

def cdf_loss_gue(spacings):
    """L2 distance between empirical CDF and GUE Wigner CDF."""
    s_grid = np.linspace(0, 4, 50)
    # Empirical CDF
    ecdf = np.array([np.mean(spacings <= s) for s in s_grid])
    # GUE CDF
    gcdf = gue_wigner_cdf(s_grid)
    return np.mean((ecdf - gcdf)**2)

def level_repulsion_loss(spacings):
    """Penalize lack of level repulsion: want P(s near 0) to be very small."""
    near_zero = np.mean(spacings < 0.3)  # fraction of spacings < 0.3
    # GUE: ~4% of spacings < 0.3 (cubic repulsion)
    # Poisson: ~26% of spacings < 0.3
    target = 0.04
    return (near_zero - target)**2

def combined_loss(spacings, alpha_cdf=1.0, alpha_repulsion=2.0):
    """Combined smooth loss."""
    l1 = kde_loss_gue(spacings)
    l2 = level_repulsion_loss(spacings)
    return alpha_cdf * l1 + alpha_repulsion * l2

# ─── Statistics evaluator ──────────────────────────────────────────────────────

def fit_level_repulsion(spacings, s_max=0.5):
    s = spacings[(spacings > 1e-4) & (spacings < s_max)]
    if len(s) < 5: return 1.0
    try:
        hist, bins = np.histogram(s, bins=15, density=True)
        centers = (bins[:-1] + bins[1:]) / 2
        mask = hist > 0
        if mask.sum() < 3: return 1.0
        beta, _ = np.polyfit(np.log(centers[mask]), np.log(hist[mask]), 1)
        return float(np.clip(beta, 0, 5))
    except:
        return 1.0

def evaluate_stats(eigenvalues, label=""):
    spacings = get_normalized_spacings(eigenvalues)

    bins = np.linspace(0, 4, 25)
    hist, _ = np.histogram(spacings, bins=bins, density=True)
    s_centers = (bins[:-1] + bins[1:]) / 2

    beta = fit_level_repulsion(spacings)
    mse_gue = np.mean((hist - gue_wigner(s_centers))**2)
    mse_goe = np.mean((hist - goe_wigner(s_centers))**2)
    mse_poi = np.mean((hist - poisson_dist(s_centers))**2)
    best = min([('GUE', mse_gue), ('GOE', mse_goe), ('Poisson', mse_poi)],
               key=lambda x: x[1])[0]
    near_zero_frac = np.mean(spacings < 0.3)

    print(f"  [{label}]")
    print(f"    β={beta:.4f} | MSE_GUE={mse_gue:.5f} | MSE_GOE={mse_goe:.5f} | "
          f"MSE_Poi={mse_poi:.5f} | best={best} | P(s<0.3)={near_zero_frac:.3f}")

    return {
        'beta': beta, 'mse_gue': mse_gue, 'mse_goe': mse_goe, 'mse_poi': mse_poi,
        'best': best, 'spacings': spacings, 'eigenvalues': np.sort(eigenvalues),
        'near_zero_frac': near_zero_frac,
    }

# ─── APPROACH A: GUE projection onto circulant subspace ────────────────────────

def circulant_projection(M):
    """
    Project an N×N matrix M onto the circulant subspace.
    Result: circulant C where C_{jk} = average of M along the (j-k mod N) diagonal.
    The projected circulant minimizes ||M - C||_F² over all circulant matrices C.
    """
    N = M.shape[0]
    c = np.zeros(N, dtype=complex)
    for d in range(N):
        diag_sum = sum(M[(i + d) % N, i] for i in range(N))
        c[d] = diag_sum / N
    return c

def approach_A(N=200, n_samples=5):
    print("\n" + "="*70)
    print(f"APPROACH A: GUE Projection onto Circulant (N={N})")
    print("="*70)
    print("Project GUE matrix onto circulant subspace.")
    print("Key question: does the projected circulant retain GUE statistics?")

    stats_list = []

    for trial in range(n_samples):
        print(f"\n  Trial {trial+1}/{n_samples}:")

        # Sample GUE
        M = sample_gue(N, seed=trial * 7 + 3)
        evals_gue = np.linalg.eigvalsh(M)
        s_gue = evaluate_stats(evals_gue, f"GUE (N={N})")

        # Project onto circulant
        c = circulant_projection(M)

        # For circulant to be Hermitian: c[N-k] should = c[k]*
        # Check deviation from Hermitian:
        herm_error = np.max(np.abs(c[1:] - np.conj(c[-1:0:-1])))
        print(f"    Hermitian deviation: {herm_error:.4e}")

        # Enforce Hermitian symmetry
        c_herm = c.copy()
        for k in range(1, N // 2):
            avg = (c[k] + np.conj(c[N-k])) / 2
            c_herm[k] = avg
            c_herm[N-k] = np.conj(avg)
        c_herm[0] = np.real(c[0])
        c_herm[N//2] = np.real(c[N//2])

        # Eigenvalues of Hermitian circulant = DFT(c)
        evals_circ = np.real(fft(c_herm))
        s_circ = evaluate_stats(evals_circ, f"Circulant projection")

        # Analyze structure: |c_k| vs k
        magnitudes = np.abs(c_herm[:N//2 + 1])
        print(f"    |c_0| = {magnitudes[0]:.6f}  (diagonal)")
        print(f"    Max off-diag |c_k|: {magnitudes[1:].max():.6f} at k={magnitudes[1:].argmax()+1}")
        print(f"    Mean off-diag |c_k|: {magnitudes[1:].mean():.6f}")

        # Power-law fit to |c_k| vs k
        k_vals = np.arange(1, N//2 + 1)
        m_vals = magnitudes[1:]
        mask = m_vals > 1e-10
        if mask.sum() > 10:
            try:
                slope, intercept = np.polyfit(np.log(k_vals[mask]), np.log(m_vals[mask]), 1)
                print(f"    Power-law fit: |c_k| ~ k^{slope:.3f} (R² = log-log fit)")
            except:
                print(f"    Power-law fit failed")

        stats_list.append({'gue': s_gue, 'circ': s_circ,
                           'c_magnitudes': magnitudes, 'c_full': c_herm})

    # Aggregate statistics
    print(f"\n  Summary:")
    for i, s in enumerate(stats_list):
        print(f"  Trial {i+1}: GUE β={s['gue']['beta']:.3f} | "
              f"Circ β={s['circ']['beta']:.3f} | "
              f"Circ best={s['circ']['best']}")

    return stats_list

# ─── APPROACH B: Full Hermitian N=40, smooth loss, differential evolution ──────

def approach_B(N_small=30):
    print("\n" + "="*70)
    print(f"APPROACH B: Full Hermitian N={N_small}, Smooth Loss, Nelder-Mead")
    print("="*70)
    print(f"Parameters: {N_small**2} (full Hermitian matrix)")
    print("Loss: KDE + level repulsion")

    n_params = N_small**2
    print(f"Total parameters: {n_params}")

    def params_to_evals(params, N=N_small):
        """Unpack params into N×N Hermitian matrix, return eigenvalues."""
        # Diagonal: first N params
        d = params[:N]
        H = np.diag(d.astype(complex))
        # Upper triangle: pairs of (real, imag)
        idx = N
        for i in range(N):
            for j in range(i+1, N):
                if idx + 1 >= len(params):
                    break
                re, im = params[idx], params[idx+1]
                H[i, j] = re + 1j * im
                H[j, i] = re - 1j * im
                idx += 2
        return np.linalg.eigvalsh(H)

    counter = [0]

    def loss(params):
        counter[0] += 1
        evals = params_to_evals(params)
        spacings = get_normalized_spacings(evals)
        if len(spacings) < 20:
            return 1e6
        total = combined_loss(spacings)
        if counter[0] % 500 == 0:
            beta = fit_level_repulsion(spacings)
            print(f"    iter {counter[0]}: loss={total:.5f}, β={beta:.3f}")
        return total

    # Initialize from GUE sample (rescaled to unit scale)
    np.random.seed(42)
    M_init = sample_gue(N_small, seed=42) * np.sqrt(N_small)
    params_init = np.zeros(n_params)
    # Pack diagonal
    params_init[:N_small] = np.real(np.diag(M_init))
    # Pack upper triangle
    idx = N_small
    for i in range(N_small):
        for j in range(i+1, N_small):
            if idx + 1 >= n_params:
                break
            params_init[idx] = np.real(M_init[i, j])
            params_init[idx+1] = np.imag(M_init[i, j])
            idx += 2

    # Evaluate initial
    evals_init = params_to_evals(params_init)
    print(f"\n  Initial (GUE sample):")
    s_init = evaluate_stats(evals_init, f"Initial GUE N={N_small}")

    # Optimize with Nelder-Mead (gradient-free)
    print(f"\n  Optimizing with Nelder-Mead (max 20000 calls)...")
    result = minimize(loss, params_init, method='Nelder-Mead',
                     options={'maxiter': 20000, 'xatol': 1e-6, 'fatol': 1e-6,
                              'adaptive': True, 'disp': False})

    print(f"  Converged: {result.success}, calls: {result.nfev}")
    print(f"  Final loss: {result.fun:.6f}")

    evals_opt = params_to_evals(result.x)
    s_opt = evaluate_stats(evals_opt, f"Optimized Hermitian N={N_small}")

    np.save(f'{EXPLORATION_DIR}/code/appB_N{N_small}_params.npy', result.x)

    return {'init': s_init, 'opt': s_opt, 'params': result.x}

# ─── APPROACH C: Von Mangoldt phases, smooth loss, Nelder-Mead ────────────────

def approach_C(N=200, alpha=0.5):
    print("\n" + "="*70)
    print(f"APPROACH C: Von Mangoldt Phases, Smooth Loss (N={N}, α={alpha})")
    print("="*70)
    print("Fix |c_k| = Λ(k)/(k+1)^α, optimize phases")
    print("Loss: KDE + level repulsion (gradient-free)")

    # Von Mangoldt amplitudes
    vm = von_mangoldt_array(N)
    amps = np.zeros(N)
    for k in range(N):
        amps[k] = vm[k] / (k + 1)**alpha if k > 0 else 1.0
    if amps.max() > 0:
        amps = amps / amps.max()

    print(f"  Nonzero amplitudes: {np.sum(amps > 0)} / {N}")

    def params_to_evals(phases):
        N_half = N // 2
        c = np.zeros(N, dtype=complex)
        c[0] = amps[0]
        for k in range(1, N_half):
            c[k] = amps[k] * np.exp(1j * phases[k-1])
            c[N-k] = np.conj(c[k])
        c[N_half] = amps[N_half]
        return np.real(fft(c))

    counter = [0]

    def loss(phases):
        counter[0] += 1
        evals = params_to_evals(phases)
        spacings = get_normalized_spacings(evals)
        if len(spacings) < 20:
            return 1e6
        total = combined_loss(spacings)
        if counter[0] % 500 == 0:
            beta = fit_level_repulsion(spacings)
            print(f"    iter {counter[0]}: loss={total:.5f}, β={beta:.3f}")
        return total

    n_phases = N // 2 - 1
    results = []

    for trial in range(3):
        np.random.seed(trial * 17 + 99)
        phases_init = np.random.uniform(-np.pi, np.pi, n_phases)
        counter[0] = 0

        evals_init = params_to_evals(phases_init)
        print(f"\n  Trial {trial+1}/3:")
        s_init = evaluate_stats(evals_init, f"VM α={alpha} Trial {trial+1} init")

        result = minimize(loss, phases_init, method='Nelder-Mead',
                         options={'maxiter': 30000, 'xatol': 1e-5, 'fatol': 1e-5,
                                  'adaptive': True, 'disp': False})

        print(f"    Converged: {result.success}, calls: {result.nfev}, "
              f"final_loss: {result.fun:.6f}")

        evals_opt = params_to_evals(result.x)
        s_opt = evaluate_stats(evals_opt, f"VM α={alpha} Trial {trial+1} opt")

        np.save(f'{EXPLORATION_DIR}/code/appC_alpha{alpha}_trial{trial+1}_phases.npy',
                result.x)
        results.append({'init': s_init, 'opt': s_opt})

    return results

# ─── APPROACH D: Genuine GUE sample reference ─────────────────────────────────

def approach_D():
    """Compute reference GUE statistics for comparison."""
    print("\n" + "="*70)
    print("APPROACH D: Reference GUE Statistics (N=500, 10 samples)")
    print("="*70)

    beta_list = []
    mse_list = []

    for trial in range(5):
        N = 500
        M = sample_gue(N, seed=trial * 111 + 77)
        evals = np.linalg.eigvalsh(M)
        # Remove edge effects: use middle 60%
        n_keep = int(N * 0.6)
        n_skip = (N - n_keep) // 2
        evals_bulk = evals[n_skip:n_skip + n_keep]
        s = evaluate_stats(evals_bulk, f"GUE N={N} trial {trial+1}")
        beta_list.append(s['beta'])
        mse_list.append(s['mse_gue'])

    print(f"\n  Reference GUE statistics (mean ± std):")
    print(f"  β = {np.mean(beta_list):.3f} ± {np.std(beta_list):.3f}")
    print(f"  MSE_GUE = {np.mean(mse_list):.5f} ± {np.std(mse_list):.5f}")

    return beta_list, mse_list

# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Optimization-Based Operator Construction — Improved Approaches")
    print()

    # Reference GUE statistics
    ref_betas, ref_mses = approach_D()

    # Approach A: GUE projection
    stats_A = approach_A(N=200, n_samples=3)

    # Approach B: Full Hermitian N=30
    stats_B = approach_B(N_small=30)

    # Approach C: Von Mangoldt phases, α=0.5
    stats_C = approach_C(N=200, alpha=0.5)

    # ── Summary ──
    print("\n\n" + "="*70)
    print("MASTER SUMMARY")
    print("="*70)

    print(f"\nReference GUE N=500: β={np.mean(ref_betas):.3f}±{np.std(ref_betas):.3f}")

    print("\nApproach A (GUE → Circulant projection):")
    for i, s in enumerate(stats_A):
        print(f"  Trial {i+1}: GUE β={s['gue']['beta']:.3f} → "
              f"Circ β={s['circ']['beta']:.3f}, best={s['circ']['best']}")

    print(f"\nApproach B (Full Hermitian N=30, Nelder-Mead):")
    print(f"  Initial: β={stats_B['init']['beta']:.3f}")
    print(f"  Optimized: β={stats_B['opt']['beta']:.3f}, best={stats_B['opt']['best']}")

    print("\nApproach C (VM phases, smooth loss):")
    for i, s in enumerate(stats_C):
        print(f"  Trial {i+1}: β_init={s['init']['beta']:.3f} → "
              f"β_opt={s['opt']['beta']:.3f}, best={s['opt']['best']}")
