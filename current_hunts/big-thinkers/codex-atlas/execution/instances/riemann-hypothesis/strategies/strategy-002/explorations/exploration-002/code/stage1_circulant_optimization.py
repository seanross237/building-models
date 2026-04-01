"""
Stage 1 & 3: Circulant Matrix Optimization for GUE Statistics

Key insight: A circulant Hermitian matrix of size N has eigenvalues = DFT of first row.
Since any real sequence can be expressed as a DFT, the unconstrained circulant
optimization reduces to: find N real numbers whose normalized spacings match GUE.
This is solvable (just arrange eigenvalues with GUE statistics directly).

The INTERESTING experiment is Stage 3: fix |c_k| = Λ(k)/k^α (von Mangoldt amplitudes)
and ONLY optimize the phases arg(c_k). Does arithmetic content constrain us to GUE?

We run:
  Experiment A: Unconstrained circulant — baseline, validates pipeline
  Experiment B: von Mangoldt amplitudes, optimize phases
  Experiment C: Direct eigenvalue optimization (trivial upper bound)
"""

import numpy as np
from scipy.optimize import minimize
from scipy.fft import fft, ifft
import warnings
warnings.filterwarnings('ignore')

# ─── Parameters ───────────────────────────────────────────────────────────────
N = 200
EXPLORATION_DIR = '/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-002'
np.random.seed(42)

# ─── Von Mangoldt function ─────────────────────────────────────────────────────

def von_mangoldt(n):
    """Λ(n) = log p if n = p^k, else 0."""
    if n < 2:
        return 0.0
    # Check if n is a prime power
    for p in range(2, int(n**0.5) + 2):
        if p > n:
            break
        if n % p == 0:
            # p divides n — check if n is a power of p
            m = n
            while m % p == 0:
                m //= p
            if m == 1:
                return np.log(p)
            else:
                return 0.0
    return np.log(n)  # n is prime

def von_mangoldt_array(N):
    """Compute Λ(k) for k = 0, 1, ..., N-1."""
    return np.array([von_mangoldt(k) for k in range(N)])

# ─── Matrix construction from circulant Fourier coefficients ──────────────────

def build_circulant_from_fourier(c_complex):
    """
    Given complex Fourier coefficients c (length N, Hermitian-symmetric),
    compute eigenvalues = FFT(c).
    For Hermitian circulant: c[N-k] = conj(c[k]) => eigenvalues are real.
    """
    eigenvalues = np.real(fft(c_complex))
    return eigenvalues

def params_to_unconstrained(params):
    """
    Unconstrained circulant: params = N real numbers.
    Pack into complex Fourier coefficients with Hermitian symmetry.
    params[0] = c[0] (real)
    params[2k-1], params[2k] = Re(c[k]), Im(c[k]) for k=1,...,N/2-1
    params[N-1] = c[N/2] (real)
    Returns eigenvalues.
    """
    N_half = N // 2
    c = np.zeros(N, dtype=complex)
    c[0] = params[0]
    for k in range(1, N_half):
        c[k] = params[2*k - 1] + 1j * params[2*k]
        c[N - k] = np.conj(c[k])
    c[N_half] = params[N - 1]
    return build_circulant_from_fourier(c)

def params_to_vm_phases(params, vm_amps):
    """
    Von Mangoldt constrained circulant:
    |c[k]| = vm_amps[k] (fixed von Mangoldt amplitudes)
    arg(c[k]) = params[k] (optimized phases)
    params has N/2 - 1 entries (phases for k=1,...,N/2-1).
    c[0] = vm_amps[0] (real), c[N/2] = vm_amps[N//2] (real)
    """
    N_half = N // 2
    c = np.zeros(N, dtype=complex)
    c[0] = vm_amps[0]  # real
    for k in range(1, N_half):
        phase = params[k - 1]
        c[k] = vm_amps[k] * np.exp(1j * phase)
        c[N - k] = np.conj(c[k])
    c[N_half] = vm_amps[N_half]  # real (sign can flip via phase 0 or pi)
    return build_circulant_from_fourier(c)

# ─── Eigenvalue unfolding ──────────────────────────────────────────────────────

def unfold_eigenvalues(evals):
    """Smooth unfolding using polynomial fit to the staircase."""
    evals_sorted = np.sort(evals)
    n = len(evals_sorted)
    # Normalize x to [-1, 1] for better polynomial conditioning
    x_min, x_max = evals_sorted[0], evals_sorted[-1]
    if x_max == x_min:
        return np.linspace(0, n, n)
    x_norm = 2 * (evals_sorted - x_min) / (x_max - x_min) - 1
    y = np.arange(n)
    # Fit degree-8 polynomial
    poly = np.polyfit(x_norm, y, 8)
    unfolded = np.polyval(poly, x_norm)
    return unfolded

# ─── Level repulsion fit ───────────────────────────────────────────────────────

def fit_level_repulsion(spacings, s_max=0.5):
    """Fit P(s) ~ s^beta for small spacings via log-linear regression."""
    s = spacings[(spacings > 1e-4) & (spacings < s_max)]
    if len(s) < 5:
        return 1.0
    try:
        hist, bins = np.histogram(s, bins=15, density=True)
        centers = (bins[:-1] + bins[1:]) / 2
        mask = hist > 0
        if mask.sum() < 3:
            return 1.0
        beta, _ = np.polyfit(np.log(centers[mask]), np.log(hist[mask]), 1)
        return float(np.clip(beta, 0, 5))
    except:
        return 1.0

# ─── Distribution benchmarks ──────────────────────────────────────────────────

def gue_wigner(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def goe_wigner(s):
    return (np.pi / 2.0) * s * np.exp(-np.pi * s**2 / 4.0)

def poisson_dist(s):
    return np.exp(-s)

# ─── Loss function factory ─────────────────────────────────────────────────────

def make_loss(eigenvalue_fn):
    """Create a loss function for a given eigenvalue computation function."""
    counter = [0]
    history = []

    def loss(params):
        counter[0] += 1

        eigenvalues = eigenvalue_fn(params)

        try:
            unfolded = unfold_eigenvalues(eigenvalues)
        except:
            return 1e6

        spacings = np.diff(np.sort(unfolded))
        mean_s = np.mean(spacings)
        if mean_s < 1e-10:
            return 1e6
        spacings = spacings / mean_s
        spacings = spacings[(spacings > 0) & (spacings < 8)]

        if len(spacings) < 50:
            return 1e6

        # Loss term 1: spacing histogram vs GUE
        bins = np.linspace(0, 4, 25)
        hist, _ = np.histogram(spacings, bins=bins, density=True)
        s_centers = (bins[:-1] + bins[1:]) / 2
        P_GUE = gue_wigner(s_centers)
        loss_spacing = np.mean((hist - P_GUE)**2)

        # Loss term 2: level repulsion beta
        beta = fit_level_repulsion(spacings)
        loss_beta = (beta - 2.0)**2

        total = loss_spacing + 0.5 * loss_beta

        history.append({'iter': counter[0], 'total': total,
                        'spacing': loss_spacing, 'beta': beta})

        if counter[0] % 200 == 0:
            print(f"    iter {counter[0]:5d}: loss={total:.5f}  spacing_mse={loss_spacing:.5f}  β={beta:.3f}")

        return total

    return loss, counter, history

# ─── Statistics evaluator ──────────────────────────────────────────────────────

def evaluate_full_statistics(eigenvalues, label=""):
    """Compute comprehensive statistics for an eigenvalue sequence."""
    evals_sorted = np.sort(eigenvalues)

    try:
        unfolded = unfold_eigenvalues(evals_sorted)
    except Exception as e:
        print(f"  [WARNING] Unfolding failed: {e}")
        return None

    spacings = np.diff(unfolded)
    mean_s = np.mean(spacings)
    if mean_s < 1e-10:
        return None
    spacings = spacings / mean_s
    spacings = spacings[(spacings > 0) & (spacings < 8)]

    beta = fit_level_repulsion(spacings)

    bins = np.linspace(0, 4, 25)
    hist, _ = np.histogram(spacings, bins=bins, density=True)
    s_centers = (bins[:-1] + bins[1:]) / 2

    mse_gue = np.mean((hist - gue_wigner(s_centers))**2)
    mse_goe = np.mean((hist - goe_wigner(s_centers))**2)
    mse_poi = np.mean((hist - poisson_dist(s_centers))**2)

    best = min([('GUE', mse_gue), ('GOE', mse_goe), ('Poisson', mse_poi)],
               key=lambda x: x[1])[0]

    print(f"\n  ┌─ Statistics: {label}")
    print(f"  │  β = {beta:.4f}  (GUE target: 2.0, GOE: 1.0, Poisson: 0.0)")
    print(f"  │  MSE vs GUE:     {mse_gue:.6f}")
    print(f"  │  MSE vs GOE:     {mse_goe:.6f}")
    print(f"  │  MSE vs Poisson: {mse_poi:.6f}")
    print(f"  │  Best match:     {best}")
    print(f"  └─ N eigenvalues: {len(eigenvalues)}, N spacings: {len(spacings)}")

    return {
        'label': label,
        'beta': beta,
        'mse_gue': mse_gue,
        'mse_goe': mse_goe,
        'mse_poi': mse_poi,
        'best_match': best,
        'spacings': spacings,
        'eigenvalues': evals_sorted,
        'unfolded': unfolded,
        'hist': hist,
        's_centers': s_centers,
    }

# ─── Experiment A: Unconstrained circulant ─────────────────────────────────────

def experiment_A():
    print("\n" + "="*70)
    print("EXPERIMENT A: Unconstrained Circulant (N=200)")
    print("="*70)
    print("Parameters: N Fourier coefficients with Hermitian symmetry")
    print("Optimization: L-BFGS-B, max 3000 iterations")

    all_stats = []

    for trial in range(3):
        np.random.seed(trial * 31 + 7)
        print(f"\n  Trial {trial+1}/3:")

        # Initialize with small random Fourier coefficients
        scale = 1.0 / np.sqrt(N)
        params = np.zeros(N)
        params[0] = 0.0
        for k in range(1, N // 2):
            params[2*k - 1] = np.random.randn() * scale
            params[2*k] = np.random.randn() * scale
        params[N - 1] = np.random.randn() * scale

        # Baseline statistics
        evals_init = params_to_unconstrained(params)
        stats_init = evaluate_full_statistics(evals_init, f"Trial {trial+1} (initial)")

        # Optimize
        loss_fn, counter, history = make_loss(params_to_unconstrained)
        result = minimize(loss_fn, params, method='L-BFGS-B',
                         options={'maxiter': 3000, 'disp': False})

        print(f"    Converged: {result.success}, iters: {result.nit}, "
              f"fun_evals: {result.nfev}, final_loss: {result.fun:.6f}")

        evals_opt = params_to_unconstrained(result.x)
        stats_opt = evaluate_full_statistics(evals_opt, f"Trial {trial+1} (optimized)")

        if stats_opt:
            all_stats.append(stats_opt)

        # Save
        np.save(f'{EXPLORATION_DIR}/code/expA_trial{trial+1}_params.npy', result.x)
        np.save(f'{EXPLORATION_DIR}/code/expA_trial{trial+1}_history.npy',
                np.array([(h['iter'], h['total'], h['beta']) for h in history]))

    return all_stats

# ─── Experiment B: Von Mangoldt constrained ────────────────────────────────────

def experiment_B():
    print("\n" + "="*70)
    print("EXPERIMENT B: Von Mangoldt Amplitudes, Optimize Phases (N=200)")
    print("="*70)
    print("Amplitudes: |c_k| = Λ(k) / (k+1)^α (von Mangoldt)")
    print("Parameters: phases arg(c_k) for k=1,...,N/2-1")

    # Compute von Mangoldt amplitudes
    vm = von_mangoldt_array(N)
    print(f"  Von Mangoldt nonzero entries: {np.sum(vm > 0)} of {N}")

    # Try several amplitude scalings
    results_by_alpha = {}

    for alpha in [0.5, 1.0, 1.5]:
        print(f"\n  ── α = {alpha} ──")

        # Amplitudes: Λ(k) / (k+1)^α
        amps = np.zeros(N)
        for k in range(N):
            amps[k] = vm[k] / (k + 1)**alpha if k > 0 else 1.0

        # Normalize so max amplitude = 1
        if amps.max() > 0:
            amps = amps / amps.max()

        # Show the amplitude structure
        print(f"  Max amplitude: {amps.max():.4f}, Mean: {amps.mean():.4f}")
        print(f"  Top-5 amplitudes at k =", np.argsort(amps)[-5:][::-1].tolist())

        trial_stats = []
        for trial in range(3):
            np.random.seed(trial * 53 + 13)
            print(f"\n    Trial {trial+1}/3 (α={alpha}):")

            # N/2 - 1 phase parameters
            n_phases = N // 2 - 1
            phases_init = np.random.uniform(-np.pi, np.pi, n_phases)

            # Wrap eigenvalue function
            fn = lambda p, a=amps: params_to_vm_phases(p, a)

            # Baseline
            evals_init = fn(phases_init)
            stats_init = evaluate_full_statistics(evals_init, f"B α={alpha} Trial {trial+1} init")

            # Optimize
            loss_fn, counter, history = make_loss(fn)
            result = minimize(loss_fn, phases_init, method='L-BFGS-B',
                             options={'maxiter': 3000, 'disp': False})

            print(f"    Converged: {result.success}, iters: {result.nit}, "
                  f"final_loss: {result.fun:.6f}")

            evals_opt = fn(result.x)
            stats_opt = evaluate_full_statistics(evals_opt,
                                                  f"B α={alpha} Trial {trial+1} opt")

            if stats_opt:
                trial_stats.append(stats_opt)

            np.save(f'{EXPLORATION_DIR}/code/expB_alpha{alpha}_trial{trial+1}_phases.npy',
                    result.x)

        if trial_stats:
            results_by_alpha[alpha] = trial_stats
            best_beta = max(s['beta'] for s in trial_stats)
            best_match = min(trial_stats, key=lambda s: s['mse_gue'])['best_match']
            print(f"\n  Summary α={alpha}: best β={best_beta:.4f}, "
                  f"best_match={best_match}")

    return results_by_alpha

# ─── Experiment C: Direct eigenvalue optimization (theoretical upper bound) ────

def experiment_C():
    """
    Direct optimization of eigenvalue sequence.
    This is the trivial upper bound: we directly optimize N eigenvalues
    to match GUE statistics. Shows what's achievable with no structural constraints.
    """
    print("\n" + "="*70)
    print("EXPERIMENT C: Direct Eigenvalue Optimization (upper bound)")
    print("="*70)
    print("Optimize N=200 real eigenvalues directly for GUE statistics")

    def fn(params):
        # Direct eigenvalues (sorted by the loss fn anyway)
        return params

    np.random.seed(42)
    # Initialize from semicircle distribution (GUE bulk)
    params_init = np.sort(np.random.randn(N) * np.sqrt(N) / 2)

    stats_init = evaluate_full_statistics(params_init, "Direct init (random Gaussian)")

    loss_fn, counter, history = make_loss(fn)
    result = minimize(loss_fn, params_init, method='L-BFGS-B',
                     options={'maxiter': 5000, 'disp': False})

    print(f"  Converged: {result.success}, iters: {result.nit}, "
          f"final_loss: {result.fun:.6f}")

    stats_opt = evaluate_full_statistics(result.x, "Direct opt (GUE target)")

    np.save(f'{EXPLORATION_DIR}/code/expC_direct_params.npy', result.x)

    return stats_opt

# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Riemann Hypothesis — Optimization-Based Operator Construction")
    print("N =", N)
    print()

    # Run experiments
    statsA = experiment_A()
    statsB = experiment_B()
    statsC = experiment_C()

    # ── Master summary ──
    print("\n\n" + "="*70)
    print("MASTER SUMMARY")
    print("="*70)

    print("\nExperiment A (unconstrained circulant):")
    for s in statsA:
        print(f"  {s['label']}: β={s['beta']:.4f}, MSE_GUE={s['mse_gue']:.5f}, "
              f"best={s['best_match']}")

    print("\nExperiment B (von Mangoldt amplitudes, optimize phases):")
    for alpha, stats_list in statsB.items():
        for s in stats_list:
            print(f"  α={alpha} {s['label']}: β={s['beta']:.4f}, "
                  f"MSE_GUE={s['mse_gue']:.5f}, best={s['best_match']}")

    print("\nExperiment C (direct eigenvalue optimization, upper bound):")
    if statsC:
        print(f"  {statsC['label']}: β={statsC['beta']:.4f}, "
              f"MSE_GUE={statsC['mse_gue']:.5f}, best={statsC['best_match']}")

    # Find overall best β
    all_results = statsA + [s for lst in statsB.values() for s in lst]
    if statsC:
        all_results.append(statsC)

    if all_results:
        best = max(all_results, key=lambda s: s['beta'])
        print(f"\nBest β overall: {best['beta']:.4f} ({best['label']})")
        print(f"GUE classification: {'SUCCESS (β > 1.5)' if best['beta'] > 1.5 else 'PARTIAL (β > 1.0)' if best['beta'] > 1.0 else 'FAIL'}")

    print("\nDone.")
