#!/usr/bin/env python3
"""
Step 6: Transfer matrix analysis for promising CA rules.

For CAs that show GUE-like spacing statistics, construct the
transfer matrix and examine its eigenvalue spectrum.

The transfer matrix T encodes how a CA evolves one step:
if we think of the CA state as a vector in a 2^width dimensional space,
T maps state(t) -> state(t+1).

For practical analysis, we use:
1. The de Bruijn graph / overlap matrix representation
2. Eigenvalues of the spatial transfer matrix
3. Spectral analysis of the linearized dynamics
"""

import numpy as np
from scipy import linalg, stats
from scipy.integrate import quad
import json
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def wigner_surmise_pdf(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_surmise_cdf(s):
    if np.isscalar(s):
        val, _ = quad(wigner_surmise_pdf, 0, max(s, 0))
        return val
    return np.array([quad(wigner_surmise_pdf, 0, max(si, 0))[0] for si in s])


# ============================================================
# Transfer Matrix Construction
# ============================================================

def elementary_ca_transfer_matrix(rule_number, width):
    """
    Construct the full transfer matrix for an elementary CA
    with periodic boundary conditions.

    The state space has 2^width states. For width > ~12 this is
    impractical, so we use the de Bruijn graph representation instead.

    For small widths (8-14), we can compute the full matrix.
    """
    n_states = 2 ** width
    rule_table = np.array([(rule_number >> i) & 1 for i in range(8)], dtype=np.uint8)

    T = np.zeros((n_states, n_states), dtype=np.float64)

    for state_idx in range(n_states):
        # Decode state
        state = np.array([(state_idx >> i) & 1 for i in range(width)], dtype=np.uint8)

        # Apply rule
        padded = np.concatenate([[state[-1]], state, [state[0]]])
        neighborhood = (padded[:-2] << 2) | (padded[1:-1] << 1) | padded[2:]
        new_state = rule_table[neighborhood]

        # Encode new state
        new_idx = sum(int(new_state[i]) << i for i in range(width))
        T[new_idx, state_idx] = 1.0

    return T


def de_bruijn_transfer_matrix(rule_number, overlap=2):
    """
    Construct the de Bruijn graph transfer matrix for an elementary CA.

    The de Bruijn graph has 2^(2*radius) = 4 nodes for radius-1 CAs
    (representing overlapping pairs of cells), or more generally
    2^overlap nodes.

    Edge weights encode the rule: edge from (a,b) to (b,c) exists
    if the rule maps (a,b,c) to some output.
    """
    rule_table = np.array([(rule_number >> i) & 1 for i in range(8)], dtype=np.uint8)
    n_nodes = 2 ** overlap  # 4 for overlap=2

    T = np.zeros((n_nodes, n_nodes), dtype=np.float64)

    for left in range(2):
        for center in range(2):
            for right in range(2):
                # Neighborhood index
                nbr = (left << 2) | (center << 1) | right
                output = rule_table[nbr]

                # Node indices (using center, right as the overlap pair)
                from_node = (left << 1) | center
                to_node = (center << 1) | right

                # Weight by output
                T[to_node, from_node] += 1.0

    return T


def extended_de_bruijn_matrix(rule_number, overlap=4):
    """
    Larger de Bruijn graph with more overlap.
    For overlap=4, we have 16 nodes, which gives a richer spectrum.
    """
    rule_table = np.array([(rule_number >> i) & 1 for i in range(8)], dtype=np.uint8)
    n_nodes = 2 ** overlap

    T = np.zeros((n_nodes, n_nodes), dtype=np.complex128)

    # For overlap > 2, we need to track longer overlaps
    # This is the spatial transfer matrix: how a block of 'overlap' cells
    # constrains the next block

    for from_state in range(n_nodes):
        bits = [(from_state >> i) & 1 for i in range(overlap)]
        # Try extending by one bit on the right
        for new_bit in range(2):
            to_state = ((from_state << 1) | new_bit) & (n_nodes - 1)

            # Check if this extension is consistent with the rule
            # The rule applies to the first 3 bits of the 'from' state
            if overlap >= 3:
                nbr = (bits[-3] << 2) | (bits[-2] << 1) | bits[-1]
                output = rule_table[nbr]
                # Weight by output value (0 or 1) adds structure
                T[to_state, from_state] += 1.0 + 0.5j * output
            else:
                T[to_state, from_state] += 1.0

    return T


# ============================================================
# Spectral Analysis
# ============================================================

def analyze_spectrum(T, label=""):
    """Analyze the eigenvalue spectrum of a transfer matrix."""
    eigenvalues = linalg.eigvals(T)

    # Sort by magnitude
    mags = np.abs(eigenvalues)
    sorted_indices = np.argsort(-mags)
    eigenvalues = eigenvalues[sorted_indices]
    mags = mags[sorted_indices]

    # Compute spacing distribution of eigenvalue phases
    phases = np.angle(eigenvalues)
    # Only use eigenvalues with non-negligible magnitude
    significant = mags > 0.01 * mags[0]
    sig_phases = np.sort(phases[significant])

    # Compute spacings of sorted phases
    phase_spacings = np.diff(sig_phases)
    phase_spacings = phase_spacings[phase_spacings > 1e-10]  # Remove degenerate

    if len(phase_spacings) > 3:
        mean_s = np.mean(phase_spacings)
        if mean_s > 0:
            normalized_spacings = phase_spacings / mean_s
        else:
            normalized_spacings = np.array([])
    else:
        normalized_spacings = np.array([])

    # Compute spacing of eigenvalue magnitudes
    mag_spacings = np.diff(np.sort(mags[significant]))
    mag_spacings = mag_spacings[mag_spacings > 1e-10]
    if len(mag_spacings) > 3:
        mean_m = np.mean(mag_spacings)
        if mean_m > 0:
            normalized_mag_spacings = mag_spacings / mean_m
        else:
            normalized_mag_spacings = np.array([])
    else:
        normalized_mag_spacings = np.array([])

    result = {
        'label': label,
        'n_eigenvalues': len(eigenvalues),
        'n_significant': int(np.sum(significant)),
        'spectral_radius': float(mags[0]),
        'top_eigenvalues': [(float(np.real(e)), float(np.imag(e))) for e in eigenvalues[:10]],
        'eigenvalue_magnitudes': mags[:20].tolist(),
    }

    if len(normalized_spacings) >= 5:
        ks = ks_gue_fast(normalized_spacings)
        ks_p = ks_poisson_fast(normalized_spacings)
        result['phase_spacing_ks_gue'] = float(ks)
        result['phase_spacing_ks_poisson'] = float(ks_p)
        result['phase_spacing_n'] = len(normalized_spacings)

    if len(normalized_mag_spacings) >= 5:
        ks = ks_gue_fast(normalized_mag_spacings)
        ks_p = ks_poisson_fast(normalized_mag_spacings)
        result['mag_spacing_ks_gue'] = float(ks)
        result['mag_spacing_ks_poisson'] = float(ks_p)
        result['mag_spacing_n'] = len(normalized_mag_spacings)

    return result, eigenvalues


def ks_gue_fast(spacings):
    sorted_s = np.sort(spacings)
    n = len(sorted_s)
    ecdf = np.arange(1, n + 1) / n
    cdf_vals = wigner_surmise_cdf(sorted_s)
    ecdf_minus = np.arange(0, n) / n
    return max(np.max(ecdf - cdf_vals), np.max(cdf_vals - ecdf_minus))

def ks_poisson_fast(spacings):
    return stats.kstest(spacings, 'expon', args=(0, 1)).statistic


# ============================================================
# Full transfer matrix analysis for small CA widths
# ============================================================

def full_transfer_matrix_analysis(rule_number, widths=[8, 10, 12]):
    """
    Compute the full transfer matrix for small CA widths and
    analyze the eigenvalue spectrum.
    """
    results = {}

    for w in widths:
        n_states = 2 ** w
        if n_states > 16384:
            print(f"  Skipping width {w} (2^{w} = {n_states} states)")
            continue

        print(f"  Width {w}: constructing {n_states}x{n_states} transfer matrix...")
        T = elementary_ca_transfer_matrix(rule_number, w)

        print(f"  Width {w}: computing eigenvalues...")
        result, eigenvalues = analyze_spectrum(T, f"rule{rule_number}_w{w}")
        results[f'width_{w}'] = result

        print(f"  Width {w}: spectral radius = {result['spectral_radius']:.4f}, "
              f"{result['n_significant']} significant eigenvalues")

        if 'phase_spacing_ks_gue' in result:
            print(f"  Width {w}: Phase spacing KS(GUE) = {result['phase_spacing_ks_gue']:.4f}, "
                  f"KS(Poisson) = {result['phase_spacing_ks_poisson']:.4f}")

    return results


def de_bruijn_analysis(rule_number, overlaps=[2, 3, 4, 5, 6, 7, 8]):
    """Analyze the de Bruijn transfer matrices at various overlap sizes."""
    results = {}

    for overlap in overlaps:
        print(f"  Overlap {overlap}: constructing {2**overlap}x{2**overlap} matrix...")

        if overlap <= 4:
            T = extended_de_bruijn_matrix(rule_number, overlap)
        else:
            T = extended_de_bruijn_matrix(rule_number, overlap)

        result, eigenvalues = analyze_spectrum(T, f"rule{rule_number}_dB{overlap}")
        results[f'overlap_{overlap}'] = result

        print(f"  Overlap {overlap}: spectral radius = {result['spectral_radius']:.4f}, "
              f"{result['n_significant']} significant eigenvalues")

        if 'phase_spacing_ks_gue' in result:
            print(f"  Overlap {overlap}: Phase spacing KS(GUE) = {result['phase_spacing_ks_gue']:.4f}")

    return results


# ============================================================
# Random Matrix comparison
# ============================================================

def random_matrix_baseline(sizes=[16, 32, 64, 128]):
    """
    Compute eigenvalue spacing statistics for GUE random matrices
    as a baseline comparison.
    """
    results = {}

    for n in sizes:
        all_spacings = []

        for trial in range(100):
            # Generate GUE random matrix
            A = np.random.randn(n, n) + 1j * np.random.randn(n, n)
            H = (A + A.conj().T) / 2  # Hermitian
            eigenvalues = np.sort(np.real(linalg.eigvalsh(H)))

            # Unfolded spacings
            spacings = np.diff(eigenvalues)
            mean_s = np.mean(spacings)
            if mean_s > 0:
                all_spacings.extend((spacings / mean_s).tolist())

        spacings_arr = np.array(all_spacings)
        ks = ks_gue_fast(spacings_arr)
        ks_p = ks_poisson_fast(spacings_arr)

        results[f'GUE_{n}x{n}'] = {
            'n_spacings': len(spacings_arr),
            'ks_gue': float(ks),
            'ks_poisson': float(ks_p),
            'mean': float(np.mean(spacings_arr)),
            'std': float(np.std(spacings_arr)),
        }
        print(f"  GUE {n}x{n}: KS(GUE) = {ks:.4f}, KS(Poisson) = {ks_p:.4f}")

    return results


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    # Known promising rules (from quick scan or prior knowledge)
    promising_rules = [30, 45, 54, 73, 86, 89, 90, 105, 110, 150]

    all_results = {}

    # Random matrix baseline
    print("=== Random Matrix Baseline ===")
    rm_results = random_matrix_baseline([16, 32, 64])
    all_results['random_matrix_baseline'] = rm_results

    for rule in promising_rules:
        print(f"\n{'='*60}")
        print(f"=== Transfer Matrix Analysis: Rule {rule} ===")
        print(f"{'='*60}")

        # Full transfer matrix (small widths)
        print("\nFull transfer matrix:")
        full_results = full_transfer_matrix_analysis(rule, widths=[8, 10, 12])
        all_results[f'rule_{rule}_full'] = full_results

        # De Bruijn analysis
        print("\nDe Bruijn graph:")
        db_results = de_bruijn_analysis(rule, overlaps=[2, 3, 4, 5, 6, 7, 8])
        all_results[f'rule_{rule}_debruijn'] = db_results

    # Save results
    with open(os.path.join(OUTPUT_DIR, 'transfer_matrix_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\nResults saved to transfer_matrix_results.json")
