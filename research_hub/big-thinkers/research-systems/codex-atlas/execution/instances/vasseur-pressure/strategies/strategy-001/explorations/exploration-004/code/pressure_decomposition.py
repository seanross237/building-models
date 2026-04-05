"""
De Giorgi pressure decomposition for NS on T^3.

Decomposes the NS pressure p (solving -Delta p = d_i d_j (u_i u_j))
into Vasseur (2007) pieces based on velocity magnitude truncation.

For the periodic domain with phi_k = 1:
  u = u_below + u_above
  u_below = u * min(1, threshold / |u|)   (bounded by threshold)
  u_above = u - u_below                    (supported where |u| > threshold)

  P = P_k^{21} + P_k^{22} + P_k^{23}
  where:
    -Delta P_k^{21} = d_i d_j (u_below_i * u_below_j)
    -Delta P_k^{22} = d_i d_j (u_above_i * u_below_j + u_below_i * u_above_j)
    -Delta P_k^{23} = d_i d_j (u_above_i * u_above_j)

CZ tightness = ||P_k^{mn}||_Lq / (C_q * ||f^{mn}||_Lq)
where f^{mn} is the RHS tensor and C_q is the CZ constant.
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
import json
import sys
import os
import time

# Add the prior solver path
SOLVER_PATH = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/navier-stokes/strategies/strategy-001/explorations/exploration-002/code'
sys.path.insert(0, SOLVER_PATH)
from ns_solver import NavierStokesSolver, taylor_green_ic, random_gaussian_ic


def anti_parallel_tubes_ic(solver, Re):
    """Anti-parallel vortex tubes initial condition.

    Two counter-rotating vortex tubes aligned along z, separated in y.
    This produces strong vortex interaction and is a canonical setup
    for studying potential singularity formation.
    """
    X, Y, Z = solver.X, solver.Y, solver.Z

    # Two Gaussian vortex tubes centered at (pi, pi/2, z) and (pi, 3*pi/2, z)
    # with opposite circulation
    sigma = 0.5  # tube radius

    # Distance from tube centers
    r1_sq = (X - np.pi)**2 + (Y - np.pi/2)**2
    r2_sq = (X - np.pi)**2 + (Y - 3*np.pi/2)**2

    # Vorticity along z: omega_z for tube 1 (positive) and tube 2 (negative)
    omega_z = np.exp(-r1_sq / (2*sigma**2)) - np.exp(-r2_sq / (2*sigma**2))

    # Add some perturbation in z to trigger 3D dynamics
    omega_z *= (1 + 0.1 * np.cos(Z))

    # Recover velocity from vorticity via Biot-Savart in spectral space
    # omega = (0, 0, omega_z) => u = curl^{-1}(omega)
    # In spectral space: u_hat = i k x omega_hat / |k|^2
    omega_z_hat = fftn(omega_z)

    KX, KY, KZ = solver.KX, solver.KY, solver.KZ
    K2_safe = solver.K2_safe

    # From omega = curl(u) and div(u) = 0:
    # omega_z = du_y/dx - du_x/dy
    # In spectral: omega_z_hat = i*kx*uy_hat - i*ky*ux_hat
    # Combined with div=0: i*kx*ux_hat + i*ky*uy_hat + i*kz*uz_hat = 0
    # For omega = (0, 0, omega_z):
    # ux_hat = -i*ky * omega_z_hat / |k|^2 (for k != 0 component)
    # uy_hat =  i*kx * omega_z_hat / |k|^2
    # uz_hat = 0

    ux_hat = -1j * KY * omega_z_hat / K2_safe
    uy_hat =  1j * KX * omega_z_hat / K2_safe
    uz_hat = np.zeros_like(ux_hat)

    # Zero the k=0 mode
    ux_hat[0, 0, 0] = 0
    uy_hat[0, 0, 0] = 0

    # Project and dealias
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)

    # Normalize energy to match TGV scale
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    current_energy = 0.5 * np.mean(ux**2 + uy**2 + uz**2)
    target_energy = 0.5
    if current_energy > 1e-30:
        scale = np.sqrt(target_energy / current_energy)
        ux_hat *= scale
        uy_hat *= scale
        uz_hat *= scale

    return ux_hat, uy_hat, uz_hat


def evolve_to_developed(solver, ux_hat, uy_hat, uz_hat, t_target, max_steps=50000):
    """Evolve the flow to a target time to get developed turbulence."""
    t = 0.0
    step = 0
    while t < t_target and step < max_steps:
        dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)
        dt = min(dt, t_target - t)
        ux_hat, uy_hat, uz_hat = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)
        t += dt
        step += 1
    return ux_hat, uy_hat, uz_hat, t, step


def compute_full_pressure(solver, ux_hat, uy_hat, uz_hat):
    """Compute full NS pressure: -Delta p = d_i d_j (u_i u_j).

    Returns p in physical space and p_hat in spectral space.
    """
    # Get physical velocities (dealiased)
    ux = solver.to_physical(solver.dealias(ux_hat))
    uy = solver.to_physical(solver.dealias(uy_hat))
    uz = solver.to_physical(solver.dealias(uz_hat))

    u = [ux, uy, uz]
    K = [solver.KX, solver.KY, solver.KZ]

    # RHS tensor: f_{ij} = u_i * u_j
    # Pressure in spectral: p_hat = k_i k_j f_{ij,hat} / |k|^2
    # (sign: -Delta p = d_i d_j f_{ij} => -|k|^2 p_hat = -(k_i)(k_j) f_{ij,hat}
    #  => p_hat = k_i k_j f_{ij,hat} / |k|^2)

    p_hat = np.zeros((solver.N, solver.N, solver.N), dtype=complex)

    for i in range(3):
        for j in range(3):
            fij = u[i] * u[j]
            fij_hat = fftn(fij)
            p_hat += K[i] * K[j] * fij_hat / solver.K2_safe

    p_hat[0, 0, 0] = 0  # zero mean pressure

    p = ifftn(p_hat).real
    return p, p_hat


def decompose_velocity(solver, ux_hat, uy_hat, uz_hat, k_level):
    """Decompose velocity into below/above threshold parts.

    threshold = 1 - 2^{-k}
    u_below = u * min(1, threshold / |u|)
    u_above = u - u_below

    Returns (u_below_x, u_below_y, u_below_z), (u_above_x, u_above_y, u_above_z)
    in physical space.
    """
    ux = solver.to_physical(solver.dealias(ux_hat))
    uy = solver.to_physical(solver.dealias(uy_hat))
    uz = solver.to_physical(solver.dealias(uz_hat))

    threshold = 1.0 - 2.0**(-k_level)

    speed = np.sqrt(ux**2 + uy**2 + uz**2)
    speed_safe = np.maximum(speed, 1e-30)

    # Truncation factor: min(1, threshold / |u|)
    factor = np.minimum(1.0, threshold / speed_safe)
    # Where speed is essentially 0, factor should be 1 (u_below = u, u_above = 0)
    factor = np.where(speed < 1e-30, 1.0, factor)

    ub_x = ux * factor
    ub_y = uy * factor
    ub_z = uz * factor

    ua_x = ux - ub_x
    ua_y = uy - ub_y
    ua_z = uz - ub_z

    return (ub_x, ub_y, ub_z), (ua_x, ua_y, ua_z)


def compute_pressure_piece(solver, u1, u2):
    """Compute pressure piece: -Delta P = d_i d_j (u1_i * u2_j).

    u1, u2 are 3-tuples of physical-space fields.
    Returns P in physical space and P_hat in spectral space.
    """
    K = [solver.KX, solver.KY, solver.KZ]

    p_hat = np.zeros((solver.N, solver.N, solver.N), dtype=complex)

    for i in range(3):
        for j in range(3):
            fij = u1[i] * u2[j]
            fij_hat = fftn(fij)
            p_hat += K[i] * K[j] * fij_hat / solver.K2_safe

    p_hat[0, 0, 0] = 0
    p = ifftn(p_hat).real
    return p, p_hat


def compute_rhs_tensor_norm(solver, u1, u2, q):
    """Compute ||f||_{L^q} where f_{ij} = u1_i * u2_j.

    The L^q norm of the tensor f is:
    ||f||_q = (integral |f|^q dx)^{1/q}
    where |f| = sqrt(sum_{ij} f_{ij}^2) = Frobenius norm of the tensor at each point.
    """
    vol = (2 * np.pi)**3

    f_sq = 0.0
    for i in range(3):
        for j in range(3):
            f_sq += (u1[i] * u2[j])**2

    f_mag = np.sqrt(f_sq)

    if q == np.inf:
        return np.max(f_mag)

    norm_q = (np.mean(f_mag**q) * vol)**(1.0/q)
    return norm_q


def Lq_norm(field, q, vol=(2*np.pi)**3):
    """Compute L^q norm of a scalar field on T^3."""
    if q == np.inf:
        return np.max(np.abs(field))
    return (np.mean(np.abs(field)**q) * vol)**(1.0/q)


def cz_constant(q):
    """Best known CZ constant for second-order Riesz transforms R_iR_j on R^d.

    For the operator T = d_i d_j Delta^{-1}:
    ||Tf||_q <= C_q ||f||_q

    C_2 = 1 (exact, by Parseval/Plancherel)
    For q != 2: Iwaniec (1982) showed C_q <= max(q, q/(q-1)) - 1
    This is conjectured sharp (Iwaniec conjecture, proved for q=2).

    We use C_q = q* - 1 where q* = max(q, q/(q-1)).
    """
    if q == 2:
        return 1.0
    q_star = max(q, q / (q - 1))
    return q_star - 1.0


def measure_cz_tightness(solver, ux_hat, uy_hat, uz_hat, k_level, q_values):
    """Measure CZ tightness for each pressure piece at a given k level.

    Returns dict with tightness ratios for P21, P22, P23, and full pressure.
    """
    vol = (2 * np.pi)**3

    # Decompose velocity
    u_below, u_above = decompose_velocity(solver, ux_hat, uy_hat, uz_hat, k_level)

    # Compute full pressure
    ux = solver.to_physical(solver.dealias(ux_hat))
    uy = solver.to_physical(solver.dealias(uy_hat))
    uz = solver.to_physical(solver.dealias(uz_hat))
    u_full = (ux, uy, uz)

    p_full, p_full_hat = compute_pressure_piece(solver, u_full, u_full)

    # Compute pressure pieces
    p21, p21_hat = compute_pressure_piece(solver, u_below, u_below)

    # P22: cross terms (u_above_j * u_below_i + u_below_j * u_above_i)
    # We need to compute d_i d_j (u_above_j * u_below_i) + d_i d_j (u_below_j * u_above_i)
    # Since d_i d_j is symmetric in i,j, these give the same if f_{ij} is symmetrized
    # But the operator d_i d_j acts on f_{ij}, and we sum over both i and j
    # So P22 corresponds to f^{22}_{ij} = u_above_j * u_below_i + u_below_j * u_above_i
    # Let's compute it properly
    p22a, _ = compute_pressure_piece(solver, u_below, u_above)
    p22b, _ = compute_pressure_piece(solver, u_above, u_below)
    p22 = p22a + p22b

    p23, p23_hat = compute_pressure_piece(solver, u_above, u_above)

    # Verify decomposition: P21 + P22 + P23 should equal full pressure
    decomp_error = np.max(np.abs(p21 + p22 + p23 - p_full))
    decomp_rel = decomp_error / (np.max(np.abs(p_full)) + 1e-30)

    # Stats about the decomposition
    threshold = 1.0 - 2.0**(-k_level)
    speed = np.sqrt(ux**2 + uy**2 + uz**2)
    frac_above = np.mean(speed > threshold)
    max_speed = np.max(speed)

    results = {
        'k_level': k_level,
        'threshold': threshold,
        'frac_above_threshold': frac_above,
        'max_speed': max_speed,
        'decomp_error_abs': decomp_error,
        'decomp_error_rel': decomp_rel,
        'tightness': {}
    }

    # For each q, compute CZ tightness
    for q in q_values:
        Cq = cz_constant(q)

        # Full pressure
        p_full_Lq = Lq_norm(p_full, q)
        f_full_Lq = compute_rhs_tensor_norm(solver, u_full, u_full, q)
        tight_full = p_full_Lq / (Cq * f_full_Lq) if f_full_Lq > 1e-30 else 0.0

        # P21
        p21_Lq = Lq_norm(p21, q)
        f21_Lq = compute_rhs_tensor_norm(solver, u_below, u_below, q)
        tight_21 = p21_Lq / (Cq * f21_Lq) if f21_Lq > 1e-30 else 0.0

        # P22 (cross terms)
        p22_Lq = Lq_norm(p22, q)
        # For the cross term, f^{22}_{ij} = u_above_j * u_below_i + u_below_j * u_above_i
        # ||f22||_q is bounded by triangle inequality by 2 * ||u_above tensor u_below||_q
        # But for CZ tightness, we want the actual ratio
        f22_Lq = compute_rhs_tensor_norm_cross(solver, u_below, u_above, q)
        tight_22 = p22_Lq / (Cq * f22_Lq) if f22_Lq > 1e-30 else 0.0

        # P23
        p23_Lq = Lq_norm(p23, q)
        f23_Lq = compute_rhs_tensor_norm(solver, u_above, u_above, q)
        tight_23 = p23_Lq / (Cq * f23_Lq) if f23_Lq > 1e-30 else 0.0

        results['tightness'][q] = {
            'full': tight_full,
            'P21': tight_21,
            'P22': tight_22,
            'P23': tight_23,
            'p_full_Lq': p_full_Lq,
            'p21_Lq': p21_Lq,
            'p22_Lq': p22_Lq,
            'p23_Lq': p23_Lq,
            'f_full_Lq': f_full_Lq,
            'f21_Lq': f21_Lq,
            'f22_Lq': f22_Lq,
            'f23_Lq': f23_Lq,
            'Cq': Cq,
        }

    return results


def compute_rhs_tensor_norm_cross(solver, u1, u2, q):
    """Compute ||f||_{L^q} for the symmetrized cross tensor:
    f_{ij} = u1_i * u2_j + u2_i * u1_j
    """
    vol = (2 * np.pi)**3

    f_sq = 0.0
    for i in range(3):
        for j in range(3):
            fij = u1[i] * u2[j] + u2[i] * u1[j]
            f_sq += fij**2

    f_mag = np.sqrt(f_sq)

    if q == np.inf:
        return np.max(f_mag)

    return (np.mean(f_mag**q) * vol)**(1.0/q)


def run_single_case(ic_name, Re, N, q_values, k_values, t_evolve=None, progress_file=None):
    """Run the full analysis for a single IC/Re/N combination."""
    nu = 1.0 / Re
    solver = NavierStokesSolver(N, nu, cfl=0.5)

    # Initialize
    if ic_name == 'taylor_green':
        ux_hat, uy_hat, uz_hat = taylor_green_ic(solver, Re)
    elif ic_name == 'random_gaussian':
        ux_hat, uy_hat, uz_hat = random_gaussian_ic(solver, Re)
    elif ic_name == 'anti_parallel':
        ux_hat, uy_hat, uz_hat = anti_parallel_tubes_ic(solver, Re)
    else:
        raise ValueError(f"Unknown IC: {ic_name}")

    # Evolve to develop some turbulence
    if t_evolve is None:
        # Scale evolution time with Re
        t_evolve = min(2.0, 10.0 / Re)  # enough to develop nonlinearity, not too long

    if t_evolve > 0:
        msg = f"  Evolving {ic_name} Re={Re} N={N} to t={t_evolve:.3f}..."
        print(msg)
        if progress_file:
            with open(progress_file, 'a') as f:
                f.write(msg + '\n')

        ux_hat, uy_hat, uz_hat, t_actual, steps = evolve_to_developed(
            solver, ux_hat, uy_hat, uz_hat, t_evolve
        )
        print(f"    Evolved to t={t_actual:.4f} in {steps} steps")

    # Get physical velocities for stats
    ux = solver.to_physical(solver.dealias(ux_hat))
    uy = solver.to_physical(solver.dealias(uy_hat))
    uz = solver.to_physical(solver.dealias(uz_hat))
    speed = np.sqrt(ux**2 + uy**2 + uz**2)

    case_results = {
        'ic': ic_name,
        'Re': Re,
        'N': N,
        't_evolved': t_evolve,
        'max_speed': float(np.max(speed)),
        'mean_speed': float(np.mean(speed)),
        'energy': float(0.5 * np.mean(ux**2 + uy**2 + uz**2)),
        'k_results': []
    }

    # Normalize velocity so max speed ~ 2-4 (ensuring nontrivial decomposition)
    # The De Giorgi iteration uses threshold = 1 - 2^{-k}, approaching 1.
    # We want |u| to have a range crossing these thresholds.
    # Normalize so max|u| ~ 2 to ensure the decomposition is nontrivial for k=0..8
    current_max = np.max(speed)
    if current_max > 1e-10:
        target_max = 2.0  # max speed of 2 ensures k=0 (threshold=0) to k=8 have nontrivial support
        renorm = target_max / current_max
        ux_hat *= renorm
        uy_hat *= renorm
        uz_hat *= renorm
        case_results['renorm_factor'] = float(renorm)
        case_results['renormed_max_speed'] = float(target_max)

    # Measure CZ tightness for each k
    for k in k_values:
        msg = f"  k={k}..."
        print(msg, end='', flush=True)

        result = measure_cz_tightness(solver, ux_hat, uy_hat, uz_hat, k, q_values)
        case_results['k_results'].append(result)

        # Convert numpy types for JSON
        result['frac_above_threshold'] = float(result['frac_above_threshold'])
        result['max_speed'] = float(result['max_speed'])
        result['decomp_error_abs'] = float(result['decomp_error_abs'])
        result['decomp_error_rel'] = float(result['decomp_error_rel'])

        for q in q_values:
            for key in result['tightness'][q]:
                result['tightness'][q][key] = float(result['tightness'][q][key])

        frac = result['frac_above_threshold']
        t21 = result['tightness'][q_values[0]]['P21'] if q_values else 0
        print(f" frac_above={frac:.4f}, P21_tight(q={q_values[0]})={t21:.4f}")

    return case_results


def main():
    """Run the full De Giorgi pressure decomposition analysis."""

    OUTDIR = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-004'
    progress_file = os.path.join(OUTDIR, 'progress.txt')
    results_file = os.path.join(OUTDIR, 'code', 'results.json')

    with open(progress_file, 'w') as f:
        f.write(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    q_values = [2, 3, 4, 6, 8]
    k_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Primary runs: 3 ICs x 3 Re x N=64
    ics = ['taylor_green', 'anti_parallel', 'random_gaussian']
    Re_values = [100, 500, 1000]
    N_primary = 64

    all_results = {
        'q_values': q_values,
        'k_values': k_values,
        'cases': []
    }

    for ic in ics:
        for Re in Re_values:
            print(f"\n{'='*60}")
            print(f"IC={ic}, Re={Re}, N={N_primary}")
            print(f"{'='*60}")

            with open(progress_file, 'a') as f:
                f.write(f"\nRunning IC={ic}, Re={Re}, N={N_primary}\n")

            try:
                result = run_single_case(ic, Re, N_primary, q_values, k_values,
                                        progress_file=progress_file)
                all_results['cases'].append(result)

                # Save intermediate results
                with open(results_file, 'w') as f:
                    json.dump(all_results, f, indent=2)

            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()
                with open(progress_file, 'a') as f:
                    f.write(f"  ERROR: {e}\n")

    # Convergence check: one case at N=128
    print(f"\n{'='*60}")
    print(f"CONVERGENCE CHECK: IC=taylor_green, Re=500, N=128")
    print(f"{'='*60}")

    with open(progress_file, 'a') as f:
        f.write(f"\nConvergence check: IC=taylor_green, Re=500, N=128\n")

    try:
        conv_result = run_single_case('taylor_green', 500, 128, q_values, k_values,
                                     progress_file=progress_file)
        all_results['convergence_check'] = conv_result
    except Exception as e:
        print(f"  ERROR: {e}")
        all_results['convergence_check_error'] = str(e)

    # Save final results
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    with open(progress_file, 'a') as f:
        f.write(f"\nCompleted: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"\nResults saved to {results_file}")
    return all_results


if __name__ == '__main__':
    results = main()
