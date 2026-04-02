"""
De Giorgi level-set iteration measurement on 3D Navier-Stokes DNS data.

Implements the De Giorgi recurrence from Vasseur (2007, NoDEA) Proposition 3:
  U_k <= C^k * (1 + ||P||) * U_{k-1}^{beta}

We measure U_k on DNS snapshots and extract beta_effective via regression.

Key formulas:
  - threshold_k = 1 - 2^{-k}
  - v_k = [|u_normalized| - threshold_k]_+
  - d_k^2 = (v_k/|u|)|grad|u||^2 + (threshold_k * 1_{|u|>=threshold_k}/|u|)|grad_u|^2
  - U_k = sup_t int v_k^2 dx + int_0^T int d_k^2 dx dt

The normalization ensures U_0 <= 1.

Usage: Called from run_all.py
"""

import numpy as np
from numpy.fft import fftn, ifftn


def compute_velocity_magnitude_and_gradients(solver, ux_hat, uy_hat, uz_hat):
    """
    Compute |u|, grad|u|, and |grad u|^2 from spectral velocity data.

    Returns:
        u_mag: |u| on physical grid (N^3)
        grad_umag_sq: |grad |u||^2 on physical grid
        grad_u_sq: |grad u|^2 = sum_{i,j} (du_i/dx_j)^2 on physical grid
        ux, uy, uz: physical velocities
    """
    # Physical velocities
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)

    # |u|
    u_mag = np.sqrt(ux**2 + uy**2 + uz**2)

    # All velocity gradients (9 components)
    dux_dx = solver.to_physical(1j * solver.KX * ux_hat)
    dux_dy = solver.to_physical(1j * solver.KY * ux_hat)
    dux_dz = solver.to_physical(1j * solver.KZ * ux_hat)
    duy_dx = solver.to_physical(1j * solver.KX * uy_hat)
    duy_dy = solver.to_physical(1j * solver.KY * uy_hat)
    duy_dz = solver.to_physical(1j * solver.KZ * uy_hat)
    duz_dx = solver.to_physical(1j * solver.KX * uz_hat)
    duz_dy = solver.to_physical(1j * solver.KY * uz_hat)
    duz_dz = solver.to_physical(1j * solver.KZ * uz_hat)

    # |grad u|^2 = sum_{i,j} (du_i/dx_j)^2
    grad_u_sq = (dux_dx**2 + dux_dy**2 + dux_dz**2 +
                 duy_dx**2 + duy_dy**2 + duy_dz**2 +
                 duz_dx**2 + duz_dy**2 + duz_dz**2)

    # grad|u| = (u . grad u) / |u| where (u . grad u)_j = sum_i u_i * du_i/dx_j
    # so grad|u|_j = (ux * dux/dxj + uy * duy/dxj + uz * duz/dxj) / |u|
    u_mag_safe = np.where(u_mag > 1e-14, u_mag, 1.0)

    grad_umag_x = (ux * dux_dx + uy * duy_dx + uz * duz_dx) / u_mag_safe
    grad_umag_y = (ux * dux_dy + uy * duy_dy + uz * duz_dy) / u_mag_safe
    grad_umag_z = (ux * dux_dz + uy * duy_dz + uz * duz_dz) / u_mag_safe

    # Zero out where |u| is negligible
    mask_zero = u_mag < 1e-14
    grad_umag_x[mask_zero] = 0.0
    grad_umag_y[mask_zero] = 0.0
    grad_umag_z[mask_zero] = 0.0

    grad_umag_sq = grad_umag_x**2 + grad_umag_y**2 + grad_umag_z**2

    return u_mag, grad_umag_sq, grad_u_sq, ux, uy, uz


def compute_Uk_single_snapshot(solver, ux_hat, uy_hat, uz_hat, k, norm_factor):
    """
    Compute the spatial integrals for U_k at a single time snapshot.

    The fields are normalized: u_normalized = u / norm_factor

    Returns:
        int_vk_sq: integral of v_k^2 dx  (L2 energy on level set)
        int_dk_sq: integral of d_k^2 dx  (dissipation on level set)
    """
    N = solver.N
    vol = (2 * np.pi)**3
    dV = vol / N**3

    # Compute physical quantities (on the ORIGINAL, unnormalized field)
    u_mag, grad_umag_sq, grad_u_sq, ux, uy, uz = \
        compute_velocity_magnitude_and_gradients(solver, ux_hat, uy_hat, uz_hat)

    # Normalize
    u_mag_norm = u_mag / norm_factor
    # grad|u_norm| = grad|u| / norm_factor, so |grad|u_norm||^2 = |grad|u||^2 / norm_factor^2
    grad_umag_sq_norm = grad_umag_sq / norm_factor**2
    # |grad u_norm|^2 = |grad u|^2 / norm_factor^2
    grad_u_sq_norm = grad_u_sq / norm_factor**2

    # Level set threshold
    threshold_k = 1.0 - 2.0**(-k)

    # v_k = [|u_norm| - threshold_k]_+
    v_k = np.maximum(u_mag_norm - threshold_k, 0.0)

    # Indicator: where |u_norm| >= threshold_k (i.e., v_k > 0)
    active = u_mag_norm >= threshold_k  # boolean mask

    # d_k^2 has two terms:
    # Term 1: (v_k / |u_norm|) * |grad |u_norm||^2
    # Term 2: (threshold_k * 1_{active} / |u_norm|) * |grad u_norm|^2

    u_mag_norm_safe = np.where(u_mag_norm > 1e-14, u_mag_norm, 1.0)

    term1 = (v_k / u_mag_norm_safe) * grad_umag_sq_norm
    term1[u_mag_norm < 1e-14] = 0.0

    term2 = np.zeros_like(v_k)
    term2[active] = (threshold_k / u_mag_norm_safe[active]) * grad_u_sq_norm[active]

    dk_sq = term1 + term2

    # Spatial integrals
    int_vk_sq = np.sum(v_k**2) * dV
    int_dk_sq = np.sum(dk_sq) * dV

    return int_vk_sq, int_dk_sq


def compute_Uk_from_snapshots(solver, snapshots, k, norm_factor):
    """
    Compute U_k = sup_t int v_k^2 dx + int_0^T int d_k^2 dx dt

    snapshots: list of (t, ux_hat, uy_hat, uz_hat) tuples
    """
    sup_vk_sq = 0.0
    total_dk_sq_dt = 0.0

    for i, (t, ux_hat, uy_hat, uz_hat) in enumerate(snapshots):
        int_vk_sq, int_dk_sq = compute_Uk_single_snapshot(
            solver, ux_hat, uy_hat, uz_hat, k, norm_factor)

        # sup over time of the L2 integral
        if int_vk_sq > sup_vk_sq:
            sup_vk_sq = int_vk_sq

        # Time integral of dissipation (trapezoidal)
        if i > 0:
            dt_snap = t - snapshots[i-1][0]
            # Average of current and previous dissipation
            prev_dk_sq = compute_Uk_single_snapshot(
                solver, snapshots[i-1][1], snapshots[i-1][2], snapshots[i-1][3],
                k, norm_factor)[1]
            total_dk_sq_dt += 0.5 * (int_dk_sq + prev_dk_sq) * dt_snap

    # If only one snapshot, the time integral is just the instantaneous value times a nominal dt
    if len(snapshots) == 1:
        _, int_dk_sq = compute_Uk_single_snapshot(
            solver, snapshots[0][1], snapshots[0][2], snapshots[0][3], k, norm_factor)
        total_dk_sq_dt = int_dk_sq  # nominal: just use the value

    U_k = sup_vk_sq + total_dk_sq_dt
    return U_k


def compute_Uk_from_snapshots_fast(solver, snapshots, k, norm_factor):
    """
    Faster version: precompute per-snapshot dk_sq values to avoid recomputation.

    U_k = sup_t int v_k^2 dx + int_0^T int d_k^2 dx dt
    """
    n_snaps = len(snapshots)
    vk_sq_vals = np.zeros(n_snaps)
    dk_sq_vals = np.zeros(n_snaps)
    times = np.zeros(n_snaps)

    for i, (t, ux_hat, uy_hat, uz_hat) in enumerate(snapshots):
        int_vk_sq, int_dk_sq = compute_Uk_single_snapshot(
            solver, ux_hat, uy_hat, uz_hat, k, norm_factor)
        vk_sq_vals[i] = int_vk_sq
        dk_sq_vals[i] = int_dk_sq
        times[i] = t

    sup_vk_sq = np.max(vk_sq_vals)

    # Time integral via trapezoidal rule
    if n_snaps > 1:
        total_dk_sq_dt = np.trapezoid(dk_sq_vals, times)
    else:
        total_dk_sq_dt = dk_sq_vals[0]

    U_k = sup_vk_sq + total_dk_sq_dt
    return U_k, vk_sq_vals, dk_sq_vals


def compute_normalization_factor(solver, snapshots):
    """
    Compute norm_factor using L^inf normalization: divide u by max|u| over all snapshots.

    This ensures max|u_norm| = 1, so the De Giorgi level sets
    {|u_norm| > 1 - 2^{-k}} are nontrivial for all k.

    The L^inf normalization is the physically correct choice: the De Giorgi iteration
    measures energy concentration near the velocity maximum. U_0 then becomes a
    nontrivial quantity that characterizes the "spread" of velocity.

    Returns:
        norm_factor: max |u| over all snapshots and grid points
        Linf_max: same as norm_factor (the L^inf norm)
    """
    Linf_max = 0.0

    for t, ux_hat, uy_hat, uz_hat in snapshots:
        ux = solver.to_physical(ux_hat)
        uy = solver.to_physical(uy_hat)
        uz = solver.to_physical(uz_hat)
        u_mag = np.sqrt(ux**2 + uy**2 + uz**2)
        local_max = np.max(u_mag)
        if local_max > Linf_max:
            Linf_max = local_max

    norm_factor = max(Linf_max, 1e-30)
    return norm_factor, Linf_max


def measure_degiorgi_sequence(solver, snapshots, K_max=10):
    """
    Full De Giorgi measurement: compute U_k for k=0,...,K_max and fit beta.

    Returns dict with:
        - norm_factor: normalization used
        - U_0_unnorm: unnormalized U_0
        - U_k_values: array of U_k for k=0,...,K_max
        - beta_eff: fitted beta
        - beta_stderr: standard error on beta
        - a_coeff: fitted coefficient a in log(U_k) = a*k + beta*log(U_{k-1})
        - fit_residual: R^2 of the fit
    """
    # Normalization
    norm_factor, U_0_unnorm = compute_normalization_factor(solver, snapshots)

    # Compute U_k sequence
    U_k_values = np.zeros(K_max + 1)

    for k in range(K_max + 1):
        U_k, _, _ = compute_Uk_from_snapshots_fast(solver, snapshots, k, norm_factor)
        U_k_values[k] = U_k

        # Early termination if U_k becomes negligible
        if k > 0 and U_k < 1e-30:
            K_max_used = k
            U_k_values = U_k_values[:k+1]
            break
    else:
        K_max_used = K_max

    U_0_check = U_k_values[0]

    # Fit: log(U_k) = a*k + beta * log(U_{k-1}) for k >= 2
    beta_eff = np.nan
    beta_stderr = np.nan
    a_coeff = np.nan
    fit_r2 = np.nan

    # Filter: only use k where both U_k and U_{k-1} are positive
    valid_k = []
    log_Uk = []
    log_Ukm1 = []
    k_vals = []

    for k in range(2, len(U_k_values)):
        if U_k_values[k] > 1e-30 and U_k_values[k-1] > 1e-30:
            valid_k.append(k)
            log_Uk.append(np.log(U_k_values[k]))
            log_Ukm1.append(np.log(U_k_values[k-1]))
            k_vals.append(k)

    if len(valid_k) >= 3:
        # Regression: log(U_k) = a*k + beta*log(U_{k-1})
        A = np.column_stack([np.array(k_vals, dtype=float), np.array(log_Ukm1)])
        y = np.array(log_Uk)

        result = np.linalg.lstsq(A, y, rcond=None)
        coeffs = result[0]
        a_coeff = coeffs[0]
        beta_eff = coeffs[1]

        y_pred = A @ coeffs
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        fit_r2 = 1 - ss_res / max(ss_tot, 1e-30)

        n = len(y)
        p = 2
        if n > p:
            mse = ss_res / (n - p)
            try:
                cov = mse * np.linalg.inv(A.T @ A)
                beta_stderr = np.sqrt(max(cov[1, 1], 0))
            except np.linalg.LinAlgError:
                beta_stderr = np.nan

    # Also compute pointwise log-ratios: log(U_k)/log(U_{k-1})
    # This gives an alternative "effective beta" at each step
    log_ratios = []
    for k in range(1, len(U_k_values)):
        if U_k_values[k] > 1e-30 and U_k_values[k-1] > 1e-30:
            r = np.log(U_k_values[k]) / np.log(U_k_values[k-1])
            log_ratios.append((k, r))
        else:
            log_ratios.append((k, np.nan))

    # Consecutive ratio: log(U_k/U_{k-1})
    decay_rates = []
    for k in range(1, len(U_k_values)):
        if U_k_values[k] > 1e-30 and U_k_values[k-1] > 1e-30:
            decay_rates.append((k, np.log(U_k_values[k] / U_k_values[k-1])))
        else:
            decay_rates.append((k, np.nan))

    return {
        'norm_factor': norm_factor,
        'Linf': U_0_unnorm,
        'U_0_normalized': U_0_check,
        'U_k_values': U_k_values,
        'K_max_used': K_max_used,
        'beta_eff': beta_eff,
        'beta_stderr': beta_stderr,
        'a_coeff': a_coeff,
        'fit_r2': fit_r2,
        'monotone': all(U_k_values[i] >= U_k_values[i+1] for i in range(len(U_k_values)-1)),
        'log_ratios': log_ratios,
        'decay_rates': decay_rates,
    }


def compute_bottleneck_integral(solver, snapshots, k, norm_factor):
    """
    Compute the bottleneck integral I_k that limits beta.

    I_k = int_0^T int |P_k^{21}| * |d_k| * 1_{v_k > 0} dx dt

    where -Delta P_k^{21} = sum_{i,j} d_i d_j [u_j(1-v_k/|u|) * u_i(1-v_k/|u|)]

    On periodic domain, solve Poisson spectrally.
    """
    vol = (2 * np.pi)**3
    dV = vol / solver.N**3
    N = solver.N

    total_Ik = 0.0
    times = []

    for snap_idx, (t, ux_hat, uy_hat, uz_hat) in enumerate(snapshots):
        # Physical fields
        u_mag, grad_umag_sq, grad_u_sq, ux, uy, uz = \
            compute_velocity_magnitude_and_gradients(solver, ux_hat, uy_hat, uz_hat)

        # Normalized
        u_mag_norm = u_mag / norm_factor
        ux_norm = ux / norm_factor
        uy_norm = uy / norm_factor
        uz_norm = uz / norm_factor

        threshold_k = 1.0 - 2.0**(-k)
        v_k = np.maximum(u_mag_norm - threshold_k, 0.0)
        active = v_k > 0

        # Compute w_i = u_i * (1 - v_k/|u_norm|)  (the "low-pass" part)
        # Where v_k > 0: w_i = u_i_norm * threshold_k / |u_norm|
        # Where v_k = 0: w_i = u_i_norm
        u_mag_norm_safe = np.where(u_mag_norm > 1e-14, u_mag_norm, 1.0)

        ratio = np.where(active, threshold_k / u_mag_norm_safe, 1.0)
        ratio[u_mag_norm < 1e-14] = 0.0

        wx = ux_norm * ratio
        wy = uy_norm * ratio
        wz = uz_norm * ratio

        # Compute w_i * w_j for each (i,j), then take spectral d_i d_j
        # -Delta P_k^{21} = sum_{i,j} d_i d_j (w_j * w_i)
        # In spectral: K2 * P_hat = sum_{i,j} (-ki*kj) * FFT(wi * wj)
        # P_hat = -sum_{i,j} ki*kj * FFT(wi*wj) / K2

        w = [wx, wy, wz]
        K = [solver.KX, solver.KY, solver.KZ]

        P_hat = np.zeros((N, N, N), dtype=complex)
        for i in range(3):
            for j in range(3):
                wiwj_hat = fftn(w[i] * w[j])
                P_hat += (-K[i] * K[j]) * wiwj_hat

        P_hat = -P_hat / solver.K2_safe  # solve -Delta P = rhs => P_hat = rhs_hat / K2
        P_hat[0, 0, 0] = 0  # zero mean

        P_phys = ifftn(P_hat).real

        # Compute |d_k| from d_k^2
        grad_umag_sq_norm = grad_umag_sq / norm_factor**2
        grad_u_sq_norm = grad_u_sq / norm_factor**2

        term1 = np.where(u_mag_norm > 1e-14, (v_k / u_mag_norm_safe) * grad_umag_sq_norm, 0.0)
        term2 = np.zeros_like(v_k)
        term2[active] = (threshold_k / u_mag_norm_safe[active]) * grad_u_sq_norm[active]
        dk_sq = term1 + term2
        dk_abs = np.sqrt(np.maximum(dk_sq, 0.0))

        # I_k integrand: |P_k^21| * |d_k| * 1_{v_k > 0}
        integrand = np.abs(P_phys) * dk_abs * active.astype(float)
        I_k_snap = np.sum(integrand) * dV

        times.append(t)

        if snap_idx > 0:
            dt_snap = t - snapshots[snap_idx-1][0]
            total_Ik += I_k_snap * dt_snap  # simple rectangle rule
        elif len(snapshots) == 1:
            total_Ik = I_k_snap

    return total_Ik
