"""
Littlewood-Paley decomposition and paraproduct analysis of the De Giorgi pressure P^{21}.

Tasks:
1. Compute LP projections Delta_j P^{21} and measure ||Delta_j P^{21}||_{L^2} spectrum
2. Decompose the bilinear product u^below * u^above into paraproducts (Bony decomposition)
3. Compute bottleneck integral split I_k^{lo}(J) + I_k^{hi}(J)
4. Test whether I_k^{hi}(J(k)) / I_k decays with J or k
5. Bernstein inequality check

Uses the NS solver from strategy-001.
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
import sys, os

# Add strategy-001 code to path
s1_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
    '../../../../strategy-001/explorations/exploration-002/code'))
sys.path.insert(0, s1_path)

from ns_solver import NavierStokesSolver
from degiorgi_measure import (compute_velocity_magnitude_and_gradients,
                               compute_normalization_factor)

# =============================================================================
# LP PROJECTOR INFRASTRUCTURE
# =============================================================================

def lp_projector_mask(K_mag, j, N):
    """
    Littlewood-Paley projector Delta_j: dyadic frequency shell.

    j = -1: low frequencies |k| <= 1  (the "S_0" part)
    j >= 0: shell 2^j < |k| <= 2^{j+1}

    In practice we use sharp cutoffs (sufficient for L^2 analysis).
    """
    if j == -1:
        return (K_mag <= 1.0).astype(np.float64)
    else:
        lo = 2.0**j
        hi = 2.0**(j+1)
        return ((K_mag > lo) & (K_mag <= hi)).astype(np.float64)

def lp_low_pass_mask(K_mag, J):
    """S_J projector: all frequencies |k| <= 2^{J+1}."""
    return (K_mag <= 2.0**(J+1)).astype(np.float64)

def lp_high_pass_mask(K_mag, J):
    """(Id - S_J) projector: frequencies |k| > 2^{J+1}."""
    return (K_mag > 2.0**(J+1)).astype(np.float64)

def apply_lp_projector(f_hat, K_mag, j, N):
    """Apply Delta_j to f_hat (spectral)."""
    mask = lp_projector_mask(K_mag, j, N)
    return f_hat * mask

def apply_low_pass(f_hat, K_mag, J):
    """Apply S_J to f_hat."""
    return f_hat * lp_low_pass_mask(K_mag, J)

def apply_high_pass(f_hat, K_mag, J):
    """Apply (Id - S_J) to f_hat."""
    return f_hat * lp_high_pass_mask(K_mag, J)


# =============================================================================
# PARAPRODUCT DECOMPOSITION (Bony)
# =============================================================================

def bony_paraproduct(f_hat, g_hat, K_mag, N, j_max=None):
    """
    Compute Bony paraproduct decomposition of f*g:
      f*g = T_f g + T_g f + R(f,g)

    T_f g = sum_j S_{j-2}(f) * Delta_j(g)   [low-high: f smooth, g rough]
    T_g f = sum_j S_{j-2}(g) * Delta_j(f)   [high-low: g smooth, f rough]
    R(f,g) = sum_j Delta_j(f) * tilde{Delta}_j(g)  [resonance, |j-j'| <= 1]

    Returns T_f_g, T_g_f, R_fg in physical space.
    """
    if j_max is None:
        j_max = int(np.log2(N // 2)) + 1

    T_f_g = np.zeros((N, N, N), dtype=np.float64)
    T_g_f = np.zeros((N, N, N), dtype=np.float64)
    R_fg = np.zeros((N, N, N), dtype=np.float64)

    for j in range(0, j_max + 1):
        # Delta_j projections
        Dj_f_hat = apply_lp_projector(f_hat, K_mag, j, N)
        Dj_g_hat = apply_lp_projector(g_hat, K_mag, j, N)

        # S_{j-2} low-pass (frequencies <= 2^{j-1})
        if j >= 2:
            Sjm2_f_hat = apply_low_pass(f_hat, K_mag, j - 2)
            Sjm2_g_hat = apply_low_pass(g_hat, K_mag, j - 2)
        elif j == 1:
            Sjm2_f_hat = apply_lp_projector(f_hat, K_mag, -1, N)  # just the j=-1 part
            Sjm2_g_hat = apply_lp_projector(g_hat, K_mag, -1, N)
        else:
            Sjm2_f_hat = np.zeros_like(f_hat)
            Sjm2_g_hat = np.zeros_like(g_hat)

        Sjm2_f = ifftn(Sjm2_f_hat).real
        Sjm2_g = ifftn(Sjm2_g_hat).real
        Dj_f = ifftn(Dj_f_hat).real
        Dj_g = ifftn(Dj_g_hat).real

        # T_f g: S_{j-2}(f) * Delta_j(g)
        T_f_g += Sjm2_f * Dj_g

        # T_g f: S_{j-2}(g) * Delta_j(f)
        T_g_f += Sjm2_g * Dj_f

        # R(f,g): Delta_j(f) * tilde{Delta}_j(g) where tilde{Delta}_j = Delta_{j-1} + Delta_j + Delta_{j+1}
        tDj_g_hat = np.zeros_like(g_hat)
        for jj in [j-1, j, j+1]:
            if jj >= -1:
                tDj_g_hat += apply_lp_projector(g_hat, K_mag, jj, N)
        tDj_g = ifftn(tDj_g_hat).real
        R_fg += Dj_f * tDj_g

    return T_f_g, T_g_f, R_fg


# =============================================================================
# PRESSURE COMPUTATION
# =============================================================================

def compute_degiorgi_fields(solver, ux_hat, uy_hat, uz_hat, norm_factor, k):
    """Compute the De Giorgi truncated fields u^below and u^above at level k."""
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)

    u_mag = np.sqrt(ux**2 + uy**2 + uz**2)
    u_mag_norm = u_mag / norm_factor

    threshold_k = 1.0 - 2.0**(-k)
    v_k = np.maximum(u_mag_norm - threshold_k, 0.0)
    active = v_k > 0

    # u^below = u * min(1, threshold_k * norm_factor / |u|)
    # When |u_norm| <= threshold_k: u^below = u (full velocity)
    # When |u_norm| > threshold_k: u^below = u * threshold_k / |u_norm| (capped)
    u_mag_safe = np.where(u_mag > 1e-14, u_mag, 1.0)
    u_mag_norm_safe = np.where(u_mag_norm > 1e-14, u_mag_norm, 1.0)

    ratio_below = np.where(active, threshold_k / u_mag_norm_safe, 1.0)
    ratio_below[u_mag_norm < 1e-14] = 0.0

    # u^above = u - u^below = u * max(0, 1 - threshold_k/|u_norm|)
    # When |u_norm| > threshold_k: u^above = u * (1 - threshold_k/|u_norm|) = u * v_k/|u_norm|
    ratio_above = np.where(active, v_k / u_mag_norm_safe, 0.0)

    ux_below = ux / norm_factor * ratio_below
    uy_below = uy / norm_factor * ratio_below
    uz_below = uz / norm_factor * ratio_below

    ux_above = ux / norm_factor * ratio_above
    uy_above = uy / norm_factor * ratio_above
    uz_above = uz / norm_factor * ratio_above

    return (ux_below, uy_below, uz_below,
            ux_above, uy_above, uz_above,
            v_k, active, u_mag_norm)


def compute_P21_spectral(solver, ux_below, uy_below, uz_below,
                          ux_above, uy_above, uz_above):
    """
    Compute P^{21} = R_i R_j (u_i^below * u_j^above) spectrally.

    In Fourier: P^{21}_hat = -sum_{i,j} k_i k_j FFT(u_i^below * u_j^above) / |k|^2

    Returns P^{21} in both spectral and physical space.
    """
    N = solver.N
    w_below = [ux_below, uy_below, uz_below]
    w_above = [ux_above, uy_above, uz_above]
    K = [solver.KX, solver.KY, solver.KZ]

    rhs_hat = np.zeros((N, N, N), dtype=complex)
    for i in range(3):
        for j in range(3):
            prod_hat = fftn(w_below[i] * w_above[j])
            rhs_hat += K[i] * K[j] * prod_hat

    # P^{21}_hat = -rhs_hat / |k|^2 (solving -Δ P = div div (u^below ⊗ u^above))
    P21_hat = -rhs_hat / solver.K2_safe
    P21_hat[0, 0, 0] = 0

    P21_phys = ifftn(P21_hat).real

    return P21_hat, P21_phys


# =============================================================================
# TASK 1: LP SPECTRUM OF P^{21}
# =============================================================================

def measure_lp_spectrum(P21_hat, K_mag, N, j_max=None):
    """
    Compute ||Delta_j P^{21}||_{L^2} for each LP block j.

    Returns arrays of j values and corresponding L^2 norms.
    """
    if j_max is None:
        j_max = int(np.log2(N // 3))

    vol = (2 * np.pi)**3
    dV = vol / N**3

    j_vals = list(range(-1, j_max + 1))
    l2_norms = []

    for j in j_vals:
        Dj_P21_hat = apply_lp_projector(P21_hat, K_mag, j, N)
        Dj_P21_phys = ifftn(Dj_P21_hat).real
        l2 = np.sqrt(np.sum(Dj_P21_phys**2) * dV)
        l2_norms.append(l2)

    return np.array(j_vals), np.array(l2_norms)


# =============================================================================
# TASK 2: BOTTLENECK INTEGRAL SPLITTING
# =============================================================================

def compute_bottleneck_split(solver, ux_hat, uy_hat, uz_hat, norm_factor, k, J):
    """
    Compute the bottleneck integral I_k split into low-frequency and high-frequency parts:

    I_k^{lo}(J) = ∫ |S_J P^{21}| * |d_k| * 1_{v_k > 0} dx
    I_k^{hi}(J) = ∫ |(Id-S_J) P^{21}| * |d_k| * 1_{v_k > 0} dx
    I_k = I_k^{lo}(J) + ... (note: not exactly additive due to abs values)

    Also returns total I_k for comparison.
    """
    N = solver.N
    vol = (2 * np.pi)**3
    dV = vol / N**3

    # De Giorgi fields
    (ux_below, uy_below, uz_below,
     ux_above, uy_above, uz_above,
     v_k, active, u_mag_norm) = compute_degiorgi_fields(
         solver, ux_hat, uy_hat, uz_hat, norm_factor, k)

    # Pressure P^{21}
    P21_hat, P21_phys = compute_P21_spectral(
        solver, ux_below, uy_below, uz_below, ux_above, uy_above, uz_above)

    # LP split of pressure
    P21_lo_hat = apply_low_pass(P21_hat, solver.K_mag, J)
    P21_hi_hat = apply_high_pass(P21_hat, solver.K_mag, J)
    P21_lo = ifftn(P21_lo_hat).real
    P21_hi = ifftn(P21_hi_hat).real

    # Compute |d_k|
    u_mag, grad_umag_sq, grad_u_sq, _, _, _ = \
        compute_velocity_magnitude_and_gradients(solver, ux_hat, uy_hat, uz_hat)

    u_mag_norm_safe = np.where(u_mag_norm > 1e-14, u_mag_norm, 1.0)
    grad_umag_sq_norm = grad_umag_sq / norm_factor**2
    grad_u_sq_norm = grad_u_sq / norm_factor**2
    threshold_k = 1.0 - 2.0**(-k)

    term1 = np.where(u_mag_norm > 1e-14, (v_k / u_mag_norm_safe) * grad_umag_sq_norm, 0.0)
    term2 = np.zeros_like(v_k)
    term2[active] = (threshold_k / u_mag_norm_safe[active]) * grad_u_sq_norm[active]
    dk_abs = np.sqrt(np.maximum(term1 + term2, 0.0))

    # Bottleneck integrals
    active_f = active.astype(np.float64)

    I_k_total = np.sum(np.abs(P21_phys) * dk_abs * active_f) * dV
    I_k_lo = np.sum(np.abs(P21_lo) * dk_abs * active_f) * dV
    I_k_hi = np.sum(np.abs(P21_hi) * dk_abs * active_f) * dV

    # Also compute L^2 norms of the LP pieces
    P21_lo_l2 = np.sqrt(np.sum(P21_lo**2) * dV)
    P21_hi_l2 = np.sqrt(np.sum(P21_hi**2) * dV)
    P21_total_l2 = np.sqrt(np.sum(P21_phys**2) * dV)

    return {
        'I_k_total': I_k_total,
        'I_k_lo': I_k_lo,
        'I_k_hi': I_k_hi,
        'ratio_hi_total': I_k_hi / max(I_k_total, 1e-30),
        'P21_lo_l2': P21_lo_l2,
        'P21_hi_l2': P21_hi_l2,
        'P21_total_l2': P21_total_l2,
        'active_fraction': np.mean(active),
    }


# =============================================================================
# TASK 3: PARAPRODUCT DECOMPOSITION OF u^below ⊗ u^above
# =============================================================================

def analyze_paraproduct_pressure(solver, ux_below, uy_below, uz_below,
                                  ux_above, uy_above, uz_above):
    """
    Decompose u^below_i * u^above_j using Bony paraproduct and compute
    the pressure contribution from each piece.

    Returns L^2 norms of the three pressure contributions.
    """
    N = solver.N
    vol = (2 * np.pi)**3
    dV = vol / N**3
    K = [solver.KX, solver.KY, solver.KZ]

    w_below = [ux_below, uy_below, uz_below]
    w_above = [ux_above, uy_above, uz_above]

    # For each (i,j), decompose w_below_i * w_above_j into paraproducts
    # Then sum over (i,j) with k_i k_j / |k|^2 to get pressure
    P_Tfg_hat = np.zeros((N, N, N), dtype=complex)
    P_Tgf_hat = np.zeros((N, N, N), dtype=complex)
    P_R_hat = np.zeros((N, N, N), dtype=complex)

    for i in range(3):
        for j in range(3):
            f_hat = fftn(w_below[i])
            g_hat = fftn(w_above[j])

            T_fg, T_gf, R_fg = bony_paraproduct(f_hat, g_hat, solver.K_mag, N)

            T_fg_hat = fftn(T_fg)
            T_gf_hat = fftn(T_gf)
            R_fg_hat = fftn(R_fg)

            factor = -K[i] * K[j] / solver.K2_safe
            P_Tfg_hat += factor * T_fg_hat
            P_Tgf_hat += factor * T_gf_hat
            P_R_hat += factor * R_fg_hat

    P_Tfg_hat[0,0,0] = 0
    P_Tgf_hat[0,0,0] = 0
    P_R_hat[0,0,0] = 0

    P_Tfg = ifftn(P_Tfg_hat).real
    P_Tgf = ifftn(P_Tgf_hat).real
    P_R = ifftn(P_R_hat).real

    l2_Tfg = np.sqrt(np.sum(P_Tfg**2) * dV)
    l2_Tgf = np.sqrt(np.sum(P_Tgf**2) * dV)
    l2_R = np.sqrt(np.sum(P_R**2) * dV)
    l2_total = np.sqrt(np.sum((P_Tfg + P_Tgf + P_R)**2) * dV)

    return {
        'l2_T_below_above': l2_Tfg,   # T_{u^below} u^above (low-high)
        'l2_T_above_below': l2_Tgf,   # T_{u^above} u^below (high-low)
        'l2_R': l2_R,                   # Remainder/resonance
        'l2_total': l2_total,
        'fraction_T_below_above': l2_Tfg / max(l2_total, 1e-30),
        'fraction_T_above_below': l2_Tgf / max(l2_total, 1e-30),
        'fraction_R': l2_R / max(l2_total, 1e-30),
    }


# =============================================================================
# BERNSTEIN INEQUALITY CHECK
# =============================================================================

def bernstein_check(P21_hat, K_mag, N, j_max=None):
    """
    Bernstein inequality: ||Delta_j f||_{L^p} <= C * 2^{jn(1/q - 1/p)} * ||Delta_j f||_{L^q}

    For the De Giorgi pairing, we need L^{5/3} or L^{10/7} of pressure.
    Bernstein: ||Delta_j P||_{L^{5/3}} <= C * 2^{3j(3/5 - 2/5)} * ... wait, let's be precise.

    n=3: ||Delta_j f||_{L^p} <= C * 2^{3j(1/q - 1/p)} * ||Delta_j f||_{L^q} for p >= q.

    From L^2 to L^{5/3} (downward, p < q): Bernstein gives REVERSE:
    ||Delta_j f||_{L^{5/3}} <= C * 2^{3j(1/2 - 3/5)} ... no, 1/q - 1/p.

    Actually, Bernstein:
    ||Delta_j f||_{L^p} <= C 2^{jn(1/q - 1/p)} ||Delta_j f||_{L^q}, for 1 <= q <= p <= infty.

    So for L^2 to L^{10/3} (p=10/3 > q=2):
    ||Delta_j f||_{L^{10/3}} <= C 2^{3j(1/2 - 3/10)} ||Delta_j f||_{L^2} = C 2^{3j * 1/5} ||Delta_j f||_{L^2}
    = C 2^{3j/5} ||Delta_j f||_{L^2}

    This INFLATES. That's the concern: Bernstein inflates when going to higher L^p.

    For our purpose: the bottleneck uses Hölder with P in L^{10/3} paired with v_k in L^{10/7}
    and d_k in L^2 (from Vasseur's proof).

    Compute: for each j, ratio = 2^{3j/5} * ||Delta_j P||_{L^2} / ||P||_{L^{10/3}}
    to see if LP pieces individually are better or worse than the whole.
    """
    if j_max is None:
        j_max = int(np.log2(N // 3))

    vol = (2 * np.pi)**3
    dV = vol / N**3

    P21_phys = ifftn(P21_hat).real

    # Full L^{10/3} norm
    P_l103 = (np.sum(np.abs(P21_phys)**(10.0/3.0)) * dV)**(3.0/10.0)
    P_l2 = np.sqrt(np.sum(P21_phys**2) * dV)

    results = []
    for j in range(-1, j_max + 1):
        Dj_hat = apply_lp_projector(P21_hat, K_mag, j, N)
        Dj_phys = ifftn(Dj_hat).real

        Dj_l2 = np.sqrt(np.sum(Dj_phys**2) * dV)
        Dj_l103_actual = (np.sum(np.abs(Dj_phys)**(10.0/3.0)) * dV)**(3.0/10.0)

        # Bernstein upper bound from L^2
        # ||Delta_j||_{L^{10/3}} <= C 2^{3j(1/2 - 3/10)} ||Delta_j||_{L^2}
        # = C 2^{3j * 1/5} ||Delta_j||_{L^2} = C 2^{3j/5}||Delta_j||_{L^2}
        j_eff = max(j, 0)  # for j=-1, use j=0 scale
        bernstein_factor = 2.0**(3.0 * j_eff / 5.0)
        bernstein_bound = bernstein_factor * Dj_l2

        results.append({
            'j': j,
            'Dj_l2': Dj_l2,
            'Dj_l103_actual': Dj_l103_actual,
            'bernstein_bound': bernstein_bound,
            'bernstein_factor': bernstein_factor,
            'ratio_actual_to_bound': Dj_l103_actual / max(bernstein_bound, 1e-30),
        })

    return results, P_l103, P_l2


# =============================================================================
# MAIN: RUN ALL ANALYSES
# =============================================================================

def taylor_green_ic(solver):
    """Taylor-Green vortex initial condition."""
    ux = np.sin(solver.X) * np.cos(solver.Y) * np.cos(solver.Z)
    uy = -np.cos(solver.X) * np.sin(solver.Y) * np.cos(solver.Z)
    uz = np.zeros_like(solver.X)
    return solver.to_spectral(ux), solver.to_spectral(uy), solver.to_spectral(uz)


def kida_vortex_ic(solver):
    """Kida-Pelz high-symmetry initial condition — generates stronger nonlinearity."""
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = np.sin(X) * (np.cos(3*Y) * np.cos(Z) - np.cos(Y) * np.cos(3*Z))
    uy = np.sin(Y) * (np.cos(3*Z) * np.cos(X) - np.cos(Z) * np.cos(3*X))
    uz = np.sin(Z) * (np.cos(3*X) * np.cos(Y) - np.cos(X) * np.cos(3*Y))
    return solver.to_spectral(ux), solver.to_spectral(uy), solver.to_spectral(uz)


def run_full_analysis(N=64, Re=500, ic_type='taylor_green', T_run=0.5, n_snaps=10):
    """Run complete LP analysis pipeline."""
    nu = 1.0 / Re
    solver = NavierStokesSolver(N, nu)

    if ic_type == 'taylor_green':
        ux_hat, uy_hat, uz_hat = taylor_green_ic(solver)
    else:
        ux_hat, uy_hat, uz_hat = kida_vortex_ic(solver)

    print(f"=== Running NS solver: N={N}, Re={Re}, IC={ic_type}, T={T_run} ===")
    snap_interval = T_run / n_snaps
    ux_hat, uy_hat, uz_hat, snapshots = solver.run(
        ux_hat, uy_hat, uz_hat, T_run, snapshot_interval=snap_interval)
    print(f"  Collected {len(snapshots)} snapshots")

    # Use a snapshot near peak nonlinearity (around t = T_run/2 or later)
    snap_idx = len(snapshots) * 2 // 3
    t_snap, ux_s, uy_s, uz_s = snapshots[snap_idx]
    print(f"  Using snapshot at t = {t_snap:.4f}")

    # Normalization
    norm_factor, _ = compute_normalization_factor(solver, snapshots)
    print(f"  L^inf normalization: {norm_factor:.6f}")

    results = {}

    # =========================================================================
    # TASK 1: LP Spectrum of P^{21} at several De Giorgi levels
    # =========================================================================
    print("\n--- Task 1: LP Spectrum of P^{21} ---")

    j_max = int(np.log2(N // 3))

    for k in [1, 2, 3, 4, 5]:
        (ux_below, uy_below, uz_below,
         ux_above, uy_above, uz_above,
         v_k, active, u_mag_norm) = compute_degiorgi_fields(
             solver, ux_s, uy_s, uz_s, norm_factor, k)

        P21_hat, P21_phys = compute_P21_spectral(
            solver, ux_below, uy_below, uz_below, ux_above, uy_above, uz_above)

        j_vals, l2_norms = measure_lp_spectrum(P21_hat, solver.K_mag, N, j_max)

        total_l2 = np.sqrt(np.sum(P21_phys**2) * (2*np.pi)**3 / N**3)

        print(f"\n  k={k}: active fraction = {np.mean(active):.4f}, ||P^21||_L2 = {total_l2:.6e}")
        print(f"  LP spectrum ||Delta_j P^21||_L2:")
        for j_val, l2 in zip(j_vals, l2_norms):
            frac = l2 / max(total_l2, 1e-30)
            print(f"    j={j_val:3d}: ||Delta_j P||_L2 = {l2:.6e}  ({frac:.3f} of total)")

        results[f'lp_spectrum_k{k}'] = {
            'j_vals': j_vals,
            'l2_norms': l2_norms,
            'total_l2': total_l2,
            'active_fraction': np.mean(active)
        }

    # =========================================================================
    # TASK 2: Bottleneck Integral Splitting
    # =========================================================================
    print("\n--- Task 2: Bottleneck Integral Splitting ---")

    for k in [1, 2, 3, 4, 5, 6, 7, 8]:
        print(f"\n  De Giorgi level k={k}:")
        for J in range(0, j_max + 1):
            split = compute_bottleneck_split(solver, ux_s, uy_s, uz_s, norm_factor, k, J)
            ratio = split['ratio_hi_total']
            print(f"    J={J}: I_lo={split['I_k_lo']:.6e}, I_hi={split['I_k_hi']:.6e}, "
                  f"I_total={split['I_k_total']:.6e}, I_hi/I_total={ratio:.4f}")

            results[f'split_k{k}_J{J}'] = split

    # =========================================================================
    # TASK 3: Paraproduct Decomposition
    # =========================================================================
    print("\n--- Task 3: Paraproduct Decomposition ---")

    for k in [1, 2, 3, 5]:
        (ux_below, uy_below, uz_below,
         ux_above, uy_above, uz_above,
         v_k, active, u_mag_norm) = compute_degiorgi_fields(
             solver, ux_s, uy_s, uz_s, norm_factor, k)

        para = analyze_paraproduct_pressure(
            solver, ux_below, uy_below, uz_below, ux_above, uy_above, uz_above)

        print(f"\n  k={k}: Paraproduct decomposition of P^21")
        print(f"    T_{{u^below}} u^above (low-high):  L2 = {para['l2_T_below_above']:.6e}  "
              f"({para['fraction_T_below_above']:.3f})")
        print(f"    T_{{u^above}} u^below (high-low):  L2 = {para['l2_T_above_below']:.6e}  "
              f"({para['fraction_T_above_below']:.3f})")
        print(f"    R(u^below, u^above) (resonance):   L2 = {para['l2_R']:.6e}  "
              f"({para['fraction_R']:.3f})")
        print(f"    Total:                              L2 = {para['l2_total']:.6e}")

        results[f'paraproduct_k{k}'] = para

    # =========================================================================
    # BERNSTEIN INEQUALITY CHECK
    # =========================================================================
    print("\n--- Bernstein Inequality Check ---")

    k_test = 2
    (ux_below, uy_below, uz_below,
     ux_above, uy_above, uz_above,
     v_k, active, u_mag_norm) = compute_degiorgi_fields(
         solver, ux_s, uy_s, uz_s, norm_factor, k_test)

    P21_hat, _ = compute_P21_spectral(
        solver, ux_below, uy_below, uz_below, ux_above, uy_above, uz_above)

    bern_results, P_l103, P_l2 = bernstein_check(P21_hat, solver.K_mag, N, j_max)

    print(f"\n  k={k_test}: ||P^21||_L^2 = {P_l2:.6e}, ||P^21||_L^{{10/3}} = {P_l103:.6e}")
    print(f"  Bernstein analysis (L^2 → L^{{10/3}}):")
    print(f"  {'j':>4s}  {'||Dj||_L2':>12s}  {'||Dj||_L103':>12s}  {'Bern bound':>12s}  "
          f"{'Bern factor':>12s}  {'ratio':>8s}")

    sum_bernstein_bound = 0.0
    sum_actual_l103 = 0.0

    for r in bern_results:
        print(f"  {r['j']:4d}  {r['Dj_l2']:12.6e}  {r['Dj_l103_actual']:12.6e}  "
              f"{r['bernstein_bound']:12.6e}  {r['bernstein_factor']:12.4f}  "
              f"{r['ratio_actual_to_bound']:8.4f}")
        sum_bernstein_bound += r['bernstein_bound']
        sum_actual_l103 += r['Dj_l103_actual']

    print(f"\n  Sum of Bernstein bounds: {sum_bernstein_bound:.6e}")
    print(f"  Sum of actual L^{{10/3}}: {sum_actual_l103:.6e}")
    print(f"  Full ||P||_L^{{10/3}}: {P_l103:.6e}")
    print(f"  Inflation ratio (sum bounds / actual): {sum_bernstein_bound / max(P_l103, 1e-30):.4f}")

    results['bernstein'] = bern_results
    results['P_l103'] = P_l103
    results['P_l2'] = P_l2

    # =========================================================================
    # CUMULATIVE HI-FREQUENCY RATIO vs k
    # =========================================================================
    print("\n--- Hi-Frequency Ratio I_hi/I_total vs De Giorgi level k ---")
    print("  (Using J that gives best ratio at each k)")

    optimal_J = {}
    for k in range(1, 9):
        best_ratio = 1.0
        best_J = 0
        for J in range(0, j_max + 1):
            key = f'split_k{k}_J{J}'
            if key in results:
                r = results[key]['ratio_hi_total']
                if r < best_ratio:
                    best_ratio = r
                    best_J = J
        optimal_J[k] = (best_J, best_ratio)
        print(f"  k={k}: optimal J={best_J}, I_hi/I_total = {best_ratio:.4f}")

    results['optimal_J'] = optimal_J

    return results


if __name__ == '__main__':
    print("=" * 80)
    print("EXPLORATION 005: Frequency-Localized De Giorgi via LP Decomposition")
    print("=" * 80)

    # Run at N=64, Re=500 (Taylor-Green)
    print("\n\n### DATASET 1: Taylor-Green N=64, Re=500 ###")
    r1 = run_full_analysis(N=64, Re=500, ic_type='taylor_green', T_run=0.5, n_snaps=10)

    # Run at N=64, Re=1000 (Kida)
    print("\n\n### DATASET 2: Kida-Pelz N=64, Re=1000 ###")
    r2 = run_full_analysis(N=64, Re=1000, ic_type='kida', T_run=0.3, n_snaps=10)

    print("\n\nDONE.")
