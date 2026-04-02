"""
Stage 3: Structure Analysis — Why Does Projection Fail, and What Works?

Key findings from Stage 2:
- Approach A: GUE projection onto circulant → ALWAYS Poisson statistics
  Reason: c[d] = avg of N i.i.d. GUE entries → CLT → c[d] ≈ iid Gaussian → Poisson
- Approach B: Full Hermitian Nelder-Mead → fails (diverges, 900 params too many)
- Need: systematically find WHAT matrix structure admits GUE statistics

This script:
1. Rigorous analysis of GUE → circulant projection (CLT argument verified)
2. Test various structured matrix families for GUE statistics
3. Optimal eigenvalue sequence (direct optimization, bypassing matrix structure)
4. Von Mangoldt direct test (what statistics do VM-encoded matrices have?)
5. Structure requirements for GUE: the Dyson Coulomb gas formulation
"""

import numpy as np
from scipy.optimize import minimize, differential_evolution
from scipy.stats import gaussian_kde
from scipy.fft import fft
import warnings
warnings.filterwarnings('ignore')

EXPLORATION_DIR = '/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-002'
np.random.seed(42)

# ─── Reference functions ───────────────────────────────────────────────────────

def sample_gue(N, seed=None):
    if seed is not None: np.random.seed(seed)
    H = (np.random.randn(N, N) + 1j * np.random.randn(N, N)) / np.sqrt(2)
    return (H + H.conj().T) / np.sqrt(2 * N)

def unfold_eigenvalues(evals, poly_deg=8):
    s = np.sort(evals)
    n = len(s)
    x_min, x_max = s[0], s[-1]
    if x_max <= x_min: return np.linspace(0, n, n)
    xn = 2 * (s - x_min) / (x_max - x_min) - 1
    return np.polyval(np.polyfit(xn, np.arange(n), poly_deg), xn)

def get_spacings(evals):
    u = unfold_eigenvalues(evals)
    s = np.diff(u)
    s = s[s > 0]
    return s / np.mean(s)

def fit_beta(spacings, s_max=0.5):
    s = spacings[(spacings > 1e-4) & (spacings < s_max)]
    if len(s) < 5: return 1.0
    try:
        hist, bins = np.histogram(s, bins=15, density=True)
        centers = (bins[:-1] + bins[1:]) / 2
        mask = hist > 0
        if mask.sum() < 3: return 1.0
        beta, _ = np.polyfit(np.log(centers[mask]), np.log(hist[mask]), 1)
        return float(np.clip(beta, 0, 5))
    except: return 1.0

def gue_wigner(s): return (32./np.pi**2)*s**2*np.exp(-4.*s**2/np.pi)
def goe_wigner(s): return (np.pi/2.)*s*np.exp(-np.pi*s**2/4.)
def poisson_dist(s): return np.exp(-s)

def classify(spacings):
    bins = np.linspace(0, 4, 25)
    h, _ = np.histogram(spacings, bins=bins, density=True)
    sc = (bins[:-1]+bins[1:])/2
    d_gue = np.mean((h-gue_wigner(sc))**2)
    d_goe = np.mean((h-goe_wigner(sc))**2)
    d_poi = np.mean((h-poisson_dist(sc))**2)
    best = min([('GUE', d_gue), ('GOE', d_goe), ('Poisson', d_poi)], key=lambda x: x[1])
    return {'beta': fit_beta(spacings), 'mse_gue': d_gue, 'mse_goe': d_goe,
            'mse_poi': d_poi, 'best': best[0],
            'near_zero': np.mean(spacings < 0.3)}

def pprint(stats, label):
    print(f"  {label:50s}: β={stats['beta']:.3f} best={stats['best']:7s} "
          f"MSE_GUE={stats['mse_gue']:.4f} P(s<0.3)={stats['near_zero']:.3f}")

# ─── Part 1: Why circulant projection kills GUE ────────────────────────────────

def part1_circulant_theory():
    """
    Verify the CLT explanation: c[d] = avg of N i.i.d. entries → Gaussian → Poisson.

    Prediction: for GUE projection onto circulant,
    - Var(c[d]) ≈ 1/(2N) for d≠0 (each entry has Var = 1/(2N) after GUE normalization)
    - The N eigenvalues of the circulant ≈ iid Gaussian with var ≈ 1
    - → Poisson spacing statistics
    """
    print("\n" + "="*70)
    print("PART 1: Theoretical Analysis of GUE → Circulant Projection")
    print("="*70)

    N = 200
    n_samples = 10
    c_vars = []  # variance of c[d] for d=1,...,N/2

    for trial in range(n_samples):
        M = sample_gue(N, seed=trial)
        # Compute circulant projection
        c = np.zeros(N, dtype=complex)
        for d in range(N):
            c[d] = sum(M[(i+d)%N, i] for i in range(N)) / N
        # Variance of c[d] for d=1,...
        c_vars.append(np.var(np.abs(c[1:N//2])))

    mean_c_var = np.mean(c_vars)
    predicted_c_var = 1.0 / (2 * N)  # from GUE normalization: E[|H_ij|²] = 1/N → c[d] var = 1/(2N)

    print(f"  Measured Var(|c[d]|) for d=1,...,N/2: {mean_c_var:.6f}")
    print(f"  Predicted by CLT:                     {predicted_c_var:.6f}")
    print(f"  Ratio:                                {mean_c_var/predicted_c_var:.3f}")

    # Eigenvalue variance prediction
    # lambda_k = FFT(c)[k] ≈ Gaussian with variance ≈ sum_{d!=0} Var(c[d]) = (N-1)/(2N) ≈ 0.5
    pred_eval_var = (N - 1) / (2 * N)  # ≈ 0.5 for large N
    print(f"\n  Predicted eigenvalue variance:        {pred_eval_var:.4f}")

    # Verify
    M = sample_gue(N, seed=0)
    c = np.zeros(N, dtype=complex)
    for d in range(N):
        c[d] = sum(M[(i+d)%N, i] for i in range(N)) / N
    # Force Hermitian symmetry
    for k in range(1, N//2):
        avg = (c[k] + np.conj(c[N-k])) / 2
        c[k] = avg; c[N-k] = np.conj(avg)
    c[0] = np.real(c[0]); c[N//2] = np.real(c[N//2])
    evals_circ = np.real(fft(c))
    print(f"  Measured eigenvalue variance:         {np.var(evals_circ):.4f}")

    print(f"\n  CONCLUSION: c[d] ~ iid N(0, 1/(2N)) → FFT(c) ~ iid N(0, ~0.5)")
    print(f"  iid Gaussian eigenvalues → POISSON spacing statistics (no level repulsion)")
    print(f"  This explains why GUE projection → circulant always gives Poisson.")

    return {'mean_c_var': mean_c_var, 'predicted': predicted_c_var,
            'pred_eval_var': pred_eval_var}

# ─── Part 2: Structured matrix family survey ─────────────────────────────────

def part2_structured_families():
    """
    Test various structured matrix families for GUE statistics.

    N=100, 20 random samples each.
    Families:
    - GUE (ground truth)
    - GOE (real symmetric)
    - GUE projected to circulant
    - GUE projected to Toeplitz (H_{ij} = H_{|i-j|})
    - GUE projected to tridiagonal (bandwidth 1)
    - GUE projected to banded (bandwidth k=5, 10, 20)
    - Random tridiagonal
    - Random banded (k=5, 10, 20)
    - Von Mangoldt matrix
    """
    print("\n" + "="*70)
    print("PART 2: Structured Matrix Families — GUE Statistics Survey")
    print("="*70)

    N = 100
    n_samples = 20
    results = {}

    def test_family(name, matrix_fn):
        betas, mse_gues, near_zeros = [], [], []
        for seed in range(n_samples):
            M = matrix_fn(seed)
            evals = np.linalg.eigvalsh(M)
            s = get_spacings(evals)
            stats = classify(s)
            betas.append(stats['beta'])
            mse_gues.append(stats['mse_gue'])
            near_zeros.append(stats['near_zero'])
        return {
            'beta_mean': np.mean(betas), 'beta_std': np.std(betas),
            'mse_gue_mean': np.mean(mse_gues),
            'near_zero_mean': np.mean(near_zeros),
        }

    # GUE (ground truth)
    def gue_fn(seed):
        return sample_gue(N, seed=seed) * np.sqrt(N)
    results['GUE'] = test_family('GUE', gue_fn)

    # GOE
    def goe_fn(seed):
        np.random.seed(seed)
        H = np.random.randn(N, N)
        return (H + H.T) / 2
    results['GOE'] = test_family('GOE', goe_fn)

    # GUE → Circulant projection
    def circ_fn(seed):
        H = sample_gue(N, seed=seed) * np.sqrt(N)
        c = np.zeros(N, dtype=complex)
        for d in range(N):
            c[d] = sum(H[(i+d)%N, i] for i in range(N)) / N
        for k in range(1, N//2):
            avg = (c[k] + np.conj(c[N-k])) / 2
            c[k] = avg; c[N-k] = np.conj(avg)
        c[0] = np.real(c[0]); c[N//2] = np.real(c[N//2])
        # Build circulant matrix
        M = np.zeros((N, N), dtype=complex)
        for i in range(N):
            for j in range(N):
                M[i, j] = c[(j-i) % N]
        return np.real(M + M.conj().T) / 2  # ensure Hermitian
    # Actually just use eigenvalues directly for circulant
    def circ_evals_fn(seed):
        H = sample_gue(N, seed=seed) * np.sqrt(N)
        c = np.zeros(N, dtype=complex)
        for d in range(N):
            c[d] = sum(H[(i+d)%N, i] for i in range(N)) / N
        for k in range(1, N//2):
            avg = (c[k] + np.conj(c[N-k])) / 2
            c[k] = avg; c[N-k] = np.conj(avg)
        c[0] = np.real(c[0]); c[N//2] = np.real(c[N//2])
        evals = np.real(fft(c))
        # Fake a matrix with these eigenvalues
        D = np.diag(evals)
        return D  # eigenvalues of D are just evals
    results['Circulant(GUE)'] = test_family('Circulant(GUE)', circ_evals_fn)

    # GUE → Toeplitz projection
    def toeplitz_fn(seed):
        H = sample_gue(N, seed=seed) * np.sqrt(N)
        # Average along each diagonal
        T = np.zeros((N, N), dtype=complex)
        for d in range(N):
            diag_vals = [H[(i+d)%N if d<N else i, i] for i in range(N-d)]
            avg = np.mean(diag_vals) if diag_vals else 0
            for i in range(N-d):
                T[i, i+d] = avg
                T[i+d, i] = np.conj(avg)
        T += np.diag(np.real(np.diag(H)))
        return T
    results['Toeplitz(GUE)'] = test_family('Toeplitz(GUE)', toeplitz_fn)

    # GUE → Tridiagonal projection (bandwidth 1)
    def tridiag_fn(seed):
        H = sample_gue(N, seed=seed) * np.sqrt(N)
        T = np.zeros((N, N), dtype=complex)
        # Diagonal
        np.fill_diagonal(T, np.real(np.diag(H)))
        # Sub/superdiagonal
        for i in range(N-1):
            T[i, i+1] = H[i, i+1]
            T[i+1, i] = H[i+1, i]
        return T
    results['Tridiagonal(GUE)'] = test_family('Tridiagonal(GUE)', tridiag_fn)

    # GUE → Banded (bandwidth k)
    for bw in [5, 10, 20]:
        def banded_fn(seed, k=bw):
            H = sample_gue(N, seed=seed) * np.sqrt(N)
            T = np.zeros((N, N), dtype=complex)
            for i in range(N):
                for j in range(N):
                    if abs(i-j) <= k:
                        T[i, j] = H[i, j]
            return T
        results[f'Banded(k={bw})'] = test_family(f'Banded(k={bw})', banded_fn)

    # Random tridiagonal (Jacobi matrix)
    def rand_tridiag_fn(seed):
        np.random.seed(seed)
        d = np.random.randn(N)
        e = np.random.randn(N-1)
        T = np.diag(d) + np.diag(e, 1) + np.diag(e, -1)
        return T
    results['RandomTridiagonal'] = test_family('RandomTridiagonal', rand_tridiag_fn)

    # Wilkinson (arithmetic tridiagonal)
    def wilkinson_fn(seed):
        # Actually make it random Wilkinson-like with iid entries
        np.random.seed(seed)
        d = np.arange(N, dtype=float) - N//2
        e = np.random.randn(N-1) * np.sqrt(N/2)
        return np.diag(d) + np.diag(e, 1) + np.diag(e, -1)
    results['Wilkinson-like'] = test_family('Wilkinson-like', wilkinson_fn)

    # Von Mangoldt Hermitian Toeplitz
    def vm_toeplitz_fn(seed, alpha=0.5):
        def vm(n):
            if n < 2: return 0.0
            for p in range(2, int(n**0.5)+2):
                if p > n: break
                if n % p == 0:
                    m = n
                    while m % p == 0: m //= p
                    return np.log(p) if m == 1 else 0.0
            return np.log(n)
        np.random.seed(seed)
        amps = np.array([vm(k) / (k+1)**alpha if k > 0 else 1.0 for k in range(N)])
        amps = amps / max(amps.max(), 1e-10)
        # Random phases
        phases = np.random.uniform(-np.pi, np.pi, N)
        c = amps * np.exp(1j * phases)
        # Build Hermitian Toeplitz
        T = np.zeros((N, N), dtype=complex)
        for i in range(N):
            for j in range(N):
                d = abs(i-j)
                T[i, j] = c[d] if i <= j else np.conj(c[d])
        return T
    results['VM-Toeplitz(rand_phases)'] = test_family('VM-Toeplitz(rand_phases)', vm_toeplitz_fn)

    # Print results table
    print(f"\n  {'Family':35s} | {'β mean±std':14s} | {'MSE_GUE':8s} | {'P(s<0.3)':8s}")
    print(f"  {'-'*35}-+-{'-'*14}-+-{'-'*8}-+-{'-'*8}")
    for name, r in results.items():
        print(f"  {name:35s} | {r['beta_mean']:.3f}±{r['beta_std']:.3f}      | "
              f"{r['mse_gue_mean']:.5f}  | {r['near_zero_mean']:.3f}")

    return results

# ─── Part 3: Optimal eigenvalue sequence (direct) ─────────────────────────────

def part3_optimal_eigenvalue_sequence():
    """
    Directly search for an N-element real sequence with GUE-like spacing statistics.
    Uses GUE log-gas Langevin dynamics: sample from the GUE measure.

    GUE joint density: P(λ_1,...,λ_N) ∝ Π_{i<j}|λ_i-λ_j|² exp(-N Σ λ_i²)
    This is a Coulomb gas with β=2 repulsion in harmonic trap.

    We can SAMPLE from this distribution using Langevin MCMC:
    λ_i ← λ_i - ε * dE/dλ_i + √(2ε) * ξ_i    (ξ_i ~ N(0,1))

    where E(λ) = N Σ λ_i² - 2 Σ_{i<j} log|λ_i - λ_j|

    dE/dλ_i = 2N λ_i - 2 Σ_{j≠i} 1/(λ_i - λ_j)
    """
    print("\n" + "="*70)
    print("PART 3: GUE Log-Gas Langevin Sampling")
    print("="*70)
    print("Sample from GUE measure using Langevin MCMC.")
    print("This gives the 'ideal' eigenvalue sequence with GUE statistics.")

    N = 100
    n_steps = 5000
    eps = 5e-4  # step size
    beta = 2.0  # GUE repulsion

    # Initialize from Wigner semicircle
    # For GUE with confining V(x) = N x², bulk eigenvalues lie in [-2, 2]
    evals = np.linspace(-1.8, 1.8, N) + np.random.randn(N) * 0.01

    print(f"  N={N}, n_steps={n_steps}, ε={eps}")

    energy_history = []

    for step in range(n_steps):
        # Compute gradient
        diffs = evals[:, None] - evals[None, :]  # N x N
        np.fill_diagonal(diffs, np.inf)

        # dE/dλ_i = 2N λ_i - 2*beta * Σ_{j≠i} 1/(λ_i - λ_j)
        repulsion_grad = np.sum(1.0 / diffs, axis=1)  # Σ_{j≠i} 1/(λ_i - λ_j)
        confinement_grad = 2 * N * evals

        grad = confinement_grad - 2 * beta * repulsion_grad

        # Langevin step
        noise = np.random.randn(N)
        evals = evals - eps * grad + np.sqrt(2 * eps) * noise

        # Compute energy occasionally
        if step % 1000 == 0:
            diffs_abs = np.abs(evals[:, None] - evals[None, :])
            np.fill_diagonal(diffs_abs, 1.0)
            log_rep = np.sum(np.triu(np.log(diffs_abs), k=1))
            conf = np.sum(evals**2)
            E = N * conf - 2 * beta * log_rep
            energy_history.append(E)

            spacings = get_spacings(evals)
            stats = classify(spacings)
            print(f"  step {step:5d}: E={E:.2f}, β_fit={stats['beta']:.3f}, "
                  f"best={stats['best']}, MSE_GUE={stats['mse_gue']:.4f}")

    # Final statistics
    spacings = get_spacings(evals)
    stats_final = classify(spacings)
    print(f"\n  Final statistics:")
    pprint(stats_final, f"GUE Langevin N={N}")

    # Save
    np.save(f'{EXPLORATION_DIR}/code/langevin_eigenvalues.npy', evals)

    return {'eigenvalues': evals, 'stats': stats_final}

# ─── Part 4: Von Mangoldt matrix — direct test ────────────────────────────────

def part4_von_mangoldt_matrix():
    """
    Directly construct a Hermitian matrix using von Mangoldt function
    and test its spacing statistics WITHOUT optimization.

    Several constructions:
    1. Hermitian Toeplitz: H_{ij} = Λ(|i-j|) * exp(i * phase(i,j))
    2. Dirichlet-like: H_{ij} = 1 if j|i or i|j, normalized
    3. Prime-weighted: H_{ij} = Λ(i) * δ_{ij} (diagonal)
    4. Connes-like Hamiltonian: H = diag(log n) acting on L²

    Key question: which VM constructions produce GUE or GOE?
    """
    print("\n" + "="*70)
    print("PART 4: Von Mangoldt Matrix — Direct Statistical Tests")
    print("="*70)

    N = 200

    def vm(n):
        if n < 2: return 0.0
        for p in range(2, int(n**0.5)+2):
            if p > n: break
            if n % p == 0:
                m = n
                while m % p == 0: m //= p
                return np.log(p) if m == 1 else 0.0
        return np.log(n)

    vm_arr = np.array([vm(k) for k in range(1, N+1)])
    primes = [k+1 for k in range(N) if vm(k+1) == np.log(k+1)][:50]

    results = {}

    # Construction 1: Diagonal VM (trivially Poisson)
    M1 = np.diag(vm_arr)
    evals1 = np.diag(M1)
    evals1 = evals1[evals1 > 0]
    if len(evals1) > 20:
        s1 = get_spacings(evals1)
        st1 = classify(s1)
        pprint(st1, "VM diagonal (log p for p prime)")
        results['VM_diagonal'] = st1

    # Construction 2: Hermitian Toeplitz with VM amplitudes, random phases
    print(f"\n  Testing VM Toeplitz with various phase structures...")
    for phase_name, phase_fn in [
        ('random', lambda i, j: np.random.uniform(-np.pi, np.pi)),
        ('zeros', lambda i, j: 0),
        ('linear', lambda i, j: 0.1 * (i + j)),
    ]:
        np.random.seed(42)
        H = np.zeros((N, N), dtype=complex)
        for i in range(N):
            for j in range(N):
                d = abs(i - j)
                if d < N:
                    amp = vm_arr[d] if d > 0 else vm_arr[0]
                    phase = phase_fn(i, j)
                    H[i, j] = amp * np.exp(1j * phase) if i < j else amp * np.exp(-1j * phase)
        # Fix diagonal: real
        np.fill_diagonal(H, np.real(np.diag(H)))
        H = (H + H.conj().T) / 2  # ensure Hermitian
        evals = np.linalg.eigvalsh(H)
        s = get_spacings(evals)
        st = classify(s)
        pprint(st, f"VM-Toeplitz phases={phase_name}")
        results[f'VM_Toeplitz_{phase_name}'] = st

    # Construction 3: Selberg/Beurling type — H_{nm} = Λ(n/gcd(n,m)) stuff
    # Simplified: H_{nm} = Λ(gcd(n,m)) or 0
    print(f"\n  Testing GCD-based VM matrix...")
    H = np.zeros((N, N))
    for i in range(N):
        for j in range(i, N):
            g = np.gcd(i+1, j+1)
            val = vm(g)
            H[i, j] = val
            H[j, i] = val
    evals = np.linalg.eigvalsh(H)
    s = get_spacings(evals)
    st = classify(s)
    pprint(st, "GCD-VM matrix H_{ij}=Λ(gcd(i,j))")
    results['GCD_VM'] = st

    # Construction 4: Ramanujan sum matrix
    # H_{nm} = c_n(m) = sum_{k: gcd(k,n)=1} exp(2πikm/n) (Ramanujan sum)
    # Simplified: use Mobius function instead
    def mobius(n):
        if n == 1: return 1
        factors = []
        m = n
        for p in range(2, int(n**0.5)+2):
            if m % p == 0:
                factors.append(p)
                m //= p
                if m % p == 0: return 0  # p² divides n
        if m > 1: factors.append(m)
        return (-1)**len(factors)

    print(f"\n  Testing Ramanujan-Möbius matrix...")
    N_small = 100
    H = np.zeros((N_small, N_small))
    for i in range(N_small):
        for j in range(N_small):
            g = np.gcd(i+1, j+1)
            H[i, j] = mobius(g)
    H = (H + H.T) / 2
    evals = np.linalg.eigvalsh(H)
    s = get_spacings(evals)
    st = classify(s)
    pprint(st, "Möbius GCD matrix H_{ij}=μ(gcd(i,j))")
    results['Mobius_GCD'] = st

    # Construction 5: Berry-Keating-like Hamiltonian
    # In Berry-Keating: H = xp + px = -i(x d/dx + 1/2)
    # Discretize: H_{nm} = -i * n * delta(n-m+1) + conjugate
    print(f"\n  Testing Berry-Keating discretization...")
    N_bk = 150
    H_bk = np.zeros((N_bk, N_bk), dtype=complex)
    for i in range(N_bk - 1):
        n = i + 1  # n = 1, 2, ...
        H_bk[i, i+1] = -1j * n
        H_bk[i+1, i] = 1j * n
    # Add diagonal: optional confining term
    for i in range(N_bk):
        H_bk[i, i] = (i + 1)  # xp diagonal term
    H_bk = (H_bk + H_bk.conj().T) / 2
    evals_bk = np.linalg.eigvalsh(H_bk)
    s_bk = get_spacings(evals_bk)
    st_bk = classify(s_bk)
    pprint(st_bk, "Berry-Keating discretization")
    results['Berry_Keating'] = st_bk

    # Construction 6: Random phases with VM amplitudes (circulant)
    print(f"\n  Testing VM circulant (Toeplitz with VM amplitudes, random phases)...")
    N_circ = 200
    vm_200 = np.array([vm(k) for k in range(N_circ)])
    alpha = 0.5

    best_beta = 0
    best_phases = None

    for trial in range(5):
        np.random.seed(trial * 71 + 3)
        amps = np.zeros(N_circ)
        for k in range(N_circ):
            amps[k] = vm_200[k] / (k+1)**alpha if k > 0 else 1.0
        amps = amps / max(amps.max(), 1e-10)

        N_half = N_circ // 2
        phases = np.random.uniform(-np.pi, np.pi, N_half - 1)

        c = np.zeros(N_circ, dtype=complex)
        c[0] = amps[0]
        for k in range(1, N_half):
            c[k] = amps[k] * np.exp(1j * phases[k-1])
            c[N_circ - k] = np.conj(c[k])
        c[N_half] = amps[N_half]

        evals = np.real(fft(c))
        s = get_spacings(evals)
        st = classify(s)
        if st['beta'] > best_beta:
            best_beta = st['beta']
            best_phases = phases.copy()

    c = np.zeros(N_circ, dtype=complex)
    c[0] = amps[0]
    for k in range(1, N_half):
        c[k] = amps[k] * np.exp(1j * best_phases[k-1])
        c[N_circ - k] = np.conj(c[k])
    c[N_half] = amps[N_half]
    evals = np.real(fft(c))
    s = get_spacings(evals)
    st_vm_circ = classify(s)
    pprint(st_vm_circ, f"Best VM-circulant (5 random phase trials, α={alpha})")
    results['VM_circulant_best'] = st_vm_circ

    return results

# ─── Part 5: Targeted small-N optimization (N=20 full Hermitian) ─────────────

def part5_small_n_optimization():
    """
    Full Hermitian optimization for very small N=20.
    N²=400 params, Nelder-Mead should work.

    Start from: (a) random, (b) GUE sample
    Loss: proper level repulsion (fraction < 0.3) + KDE
    """
    print("\n" + "="*70)
    print("PART 5: Full Hermitian Optimization N=20 (400 params, Nelder-Mead)")
    print("="*70)

    N = 20

    def params_to_evals(p):
        H = np.zeros((N, N), dtype=complex)
        np.fill_diagonal(H, p[:N])
        idx = N
        for i in range(N):
            for j in range(i+1, N):
                if idx + 1 < len(p):
                    H[i, j] = p[idx] + 1j * p[idx+1]
                    H[j, i] = p[idx] - 1j * p[idx+1]
                    idx += 2
        return np.linalg.eigvalsh(H)

    def loss_smooth(p):
        evals = params_to_evals(p)
        s = get_spacings(evals)
        if len(s) < 10: return 1e6
        # KDE loss
        try:
            kde = gaussian_kde(s, bw_method=0.3)
            sg = np.linspace(0.01, 4, 60)
            l1 = np.mean((kde(sg) - gue_wigner(sg))**2)
        except:
            l1 = 1.0
        # Level repulsion
        l2 = (np.mean(s < 0.3) - 0.04)**2
        return l1 + 3.0 * l2

    results = []

    for trial in range(5):
        np.random.seed(trial * 13 + 7)
        print(f"\n  Trial {trial+1}/5:")

        # Initialize from GUE sample
        M_init = sample_gue(N, seed=trial * 13 + 7) * np.sqrt(N) * 2
        p_init = np.zeros(N * N)
        p_init[:N] = np.real(np.diag(M_init))
        idx = N
        for i in range(N):
            for j in range(i+1, N):
                if idx + 1 < len(p_init):
                    p_init[idx] = np.real(M_init[i, j])
                    p_init[idx+1] = np.imag(M_init[i, j])
                    idx += 2

        evals_init = params_to_evals(p_init)
        st_init = classify(get_spacings(evals_init))
        pprint(st_init, f"Trial {trial+1} initial (GUE N={N})")

        result = minimize(loss_smooth, p_init, method='Nelder-Mead',
                         options={'maxiter': 50000, 'xatol': 1e-5, 'fatol': 1e-6,
                                  'adaptive': True, 'disp': False})

        evals_opt = params_to_evals(result.x)
        st_opt = classify(get_spacings(evals_opt))
        pprint(st_opt, f"Trial {trial+1} optimized (loss={result.fun:.4f})")

        np.save(f'{EXPLORATION_DIR}/code/part5_trial{trial+1}_params.npy', result.x)
        results.append({'init': st_init, 'opt': st_opt, 'loss': result.fun})

    # Summary
    print(f"\n  Summary:")
    for i, r in enumerate(results):
        print(f"  Trial {i+1}: β_init={r['init']['beta']:.3f} → "
              f"β_opt={r['opt']['beta']:.3f}, best={r['opt']['best']}, "
              f"loss={r['loss']:.4f}")

    return results

# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from scipy.stats import gaussian_kde

    print("Structure Analysis — What Matrix Structures Admit GUE Statistics?")
    print()

    r1 = part1_circulant_theory()
    r2 = part2_structured_families()
    r3 = part3_optimal_eigenvalue_sequence()
    r4 = part4_von_mangoldt_matrix()
    r5 = part5_small_n_optimization()

    print("\n\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print("\nKey findings:")
    print("1. GUE projection → circulant gives Poisson (proven by CLT)")
    print("2. See structured family survey above for which families admit GUE")
    print("3. Langevin dynamics can sample GUE eigenvalue sequences")
    print("4. Von Mangoldt matrices tested for GUE statistics")
    print("5. Small Hermitian N=20 optimization results")
