#!/usr/bin/env python3
"""
Step 2: Cellular Automata framework with particle/collision detection
and spacing statistics computation.

Implements:
  - Elementary CA (radius-1, 2-state, 256 rules)
  - Radius-2 CA (2-state, 2^32 rules)
  - Multi-state CA (3-state, radius-1)
  - Particle/domain-wall detection via multiple methods
  - Collision event extraction
  - Spacing statistics with KS comparison to GUE
"""

import numpy as np
from scipy import stats
from scipy.integrate import quad
from scipy.signal import correlate2d
import json
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# GUE reference (same as baseline script)
# ============================================================

def wigner_surmise_pdf(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_surmise_cdf(s):
    if np.isscalar(s):
        val, _ = quad(wigner_surmise_pdf, 0, s)
        return val
    return np.array([quad(wigner_surmise_pdf, 0, si)[0] for si in s])


# ============================================================
# Elementary CA Engine
# ============================================================

class ElementaryCA:
    """1D elementary cellular automaton (radius=1, 2 states)."""

    def __init__(self, rule_number, width=500):
        self.rule_number = rule_number
        self.width = width
        # Decode rule: neighborhood (left, center, right) -> new state
        self.rule_table = np.array([(rule_number >> i) & 1 for i in range(8)], dtype=np.uint8)

    def step(self, state):
        """Evolve one timestep."""
        # Periodic boundary conditions
        padded = np.concatenate([[state[-1]], state, [state[0]]])
        # Compute neighborhood indices
        neighborhood = (padded[:-2] << 2) | (padded[1:-1] << 1) | padded[2:]
        return self.rule_table[neighborhood]

    def run(self, steps, initial=None):
        """Run CA for given number of steps. Returns spacetime diagram."""
        if initial is None:
            # Random initial condition
            initial = np.random.randint(0, 2, self.width, dtype=np.uint8)

        spacetime = np.zeros((steps, self.width), dtype=np.uint8)
        spacetime[0] = initial
        for t in range(1, steps):
            spacetime[t] = self.step(spacetime[t-1])
        return spacetime


class Radius2CA:
    """1D CA with radius=2 (5-cell neighborhood), 2 states."""

    def __init__(self, rule_number, width=500):
        self.rule_number = rule_number
        self.width = width
        # 2^5 = 32 possible neighborhoods
        self.rule_table = np.array([(rule_number >> i) & 1 for i in range(32)], dtype=np.uint8)

    def step(self, state):
        n = len(state)
        padded = np.concatenate([state[-2:], state, state[:2]])
        neighborhood = (
            (padded[:-4] << 4) |
            (padded[1:-3] << 3) |
            (padded[2:-2] << 2) |
            (padded[3:-1] << 1) |
            padded[4:]
        )
        return self.rule_table[neighborhood]

    def run(self, steps, initial=None):
        if initial is None:
            initial = np.random.randint(0, 2, self.width, dtype=np.uint8)
        spacetime = np.zeros((steps, self.width), dtype=np.uint8)
        spacetime[0] = initial
        for t in range(1, steps):
            spacetime[t] = self.step(spacetime[t-1])
        return spacetime


class TotalisticCA3State:
    """1D totalistic CA with 3 states, radius 1.
    Neighborhood sum ranges 0..6 (3 cells, each 0-2), so 7 possible sums.
    Rule encodes sum -> new state (3^7 = 2187 possible rules).
    """

    def __init__(self, rule_number, width=500):
        self.rule_number = rule_number
        self.width = width
        self.n_states = 3
        # Decode rule in base 3
        self.rule_table = np.zeros(7, dtype=np.uint8)
        r = rule_number
        for i in range(7):
            self.rule_table[i] = r % 3
            r //= 3

    def step(self, state):
        n = len(state)
        padded = np.concatenate([[state[-1]], state, [state[0]]])
        total = padded[:-2].astype(int) + padded[1:-1].astype(int) + padded[2:].astype(int)
        return self.rule_table[total]

    def run(self, steps, initial=None):
        if initial is None:
            initial = np.random.randint(0, self.n_states, self.width, dtype=np.uint8)
        spacetime = np.zeros((steps, self.width), dtype=np.uint8)
        spacetime[0] = initial
        for t in range(1, steps):
            spacetime[t] = self.step(spacetime[t-1])
        return spacetime


# ============================================================
# Particle / Domain Wall Detection
# ============================================================

def detect_domain_walls(spacetime, window=3):
    """
    Detect domain walls by finding transitions between locally periodic regions.

    Method: For each cell, compute the local entropy in a small window.
    High-entropy cells are likely at domain boundaries.
    Returns a binary mask of domain wall positions.
    """
    steps, width = spacetime.shape
    walls = np.zeros_like(spacetime, dtype=np.float64)

    for t in range(window, steps - window):
        for x in range(width):
            # Compare patterns to the left and right
            left_start = (x - window) % width
            right_end = (x + window) % width

            # Get local patches
            left_patch = np.array([spacetime[t, (x - i) % width] for i in range(1, window + 1)])
            right_patch = np.array([spacetime[t, (x + i) % width] for i in range(1, window + 1)])

            # A domain wall exists where left and right neighborhoods differ significantly
            if not np.array_equal(left_patch, right_patch):
                walls[t, x] = 1.0

    return walls


def detect_domain_walls_fast(spacetime, block_size=4):
    """
    Fast domain wall detection using block pattern comparison.

    Identifies cells where the local pattern to the left differs
    from the local pattern to the right.
    """
    steps, width = spacetime.shape
    walls = np.zeros((steps, width), dtype=np.uint8)

    for t in range(steps):
        row = spacetime[t]
        for x in range(width):
            # Compare block_size cells to left vs right
            left_idx = [(x - i - 1) % width for i in range(block_size)]
            right_idx = [(x + i + 1) % width for i in range(block_size)]
            left_block = row[left_idx]
            right_block = row[right_idx]

            # XOR-based difference
            diff = np.sum(left_block != right_block)
            if diff > block_size // 2:
                walls[t, x] = 1

    return walls


def detect_activity(spacetime, background_period=1):
    """
    Simpler particle detection: identify cells that deviate from the
    expected background pattern.

    For period-1 backgrounds (uniform), this finds any non-background cell.
    For period-2 backgrounds (checkerboard etc.), finds deviations from the alternating pattern.
    """
    steps, width = spacetime.shape

    if background_period == 1:
        # Determine background state (most common)
        bg = int(np.round(np.mean(spacetime)))
        activity = (spacetime != bg).astype(np.uint8)
    elif background_period == 2:
        # Check both possible checkerboard phases
        checker1 = np.zeros_like(spacetime)
        checker2 = np.zeros_like(spacetime)
        for t in range(steps):
            for x in range(width):
                checker1[t, x] = (t + x) % 2
                checker2[t, x] = (t + x + 1) % 2
        diff1 = np.sum(spacetime != checker1)
        diff2 = np.sum(spacetime != checker2)
        if diff1 < diff2:
            activity = (spacetime != checker1).astype(np.uint8)
        else:
            activity = (spacetime != checker2).astype(np.uint8)
    else:
        # Fallback: use temporal difference
        activity = np.zeros_like(spacetime, dtype=np.uint8)
        for t in range(background_period, steps):
            activity[t] = (spacetime[t] != spacetime[t - background_period]).astype(np.uint8)

    return activity


def detect_collisions_from_activity(activity, min_cluster_size=3):
    """
    Detect collision events from an activity map.

    A collision is where multiple particle tracks converge:
    look for regions of high activity density that exceed a threshold.

    Returns list of (time, position) collision events.
    """
    steps, width = activity.shape
    collisions = []

    # Compute local activity density using a sliding window
    kernel_size = 5
    kernel = np.ones((kernel_size, kernel_size))

    # Use correlation to compute local density
    density = np.zeros_like(activity, dtype=np.float64)
    for t in range(steps):
        for x in range(width):
            count = 0
            for dt in range(-kernel_size//2, kernel_size//2 + 1):
                for dx in range(-kernel_size//2, kernel_size//2 + 1):
                    tt = t + dt
                    xx = (x + dx) % width
                    if 0 <= tt < steps:
                        count += activity[tt, xx]
            density[t, x] = count

    # Threshold for collision
    threshold = kernel_size * kernel_size * 0.6  # 60% of kernel area active

    # Find peaks in density
    for t in range(kernel_size, steps - kernel_size):
        for x in range(width):
            if density[t, x] >= threshold:
                # Check if this is a local maximum
                is_max = True
                for dt in range(-2, 3):
                    for dx in range(-2, 3):
                        if dt == 0 and dx == 0:
                            continue
                        tt = t + dt
                        xx = (x + dx) % width
                        if 0 <= tt < steps and density[tt, xx] > density[t, x]:
                            is_max = False
                            break
                    if not is_max:
                        break
                if is_max:
                    collisions.append((t, x))

    return collisions


def extract_collision_time_spacings(collisions, normalize=True):
    """
    Extract temporal spacings between collision events.
    Sort by time, compute nearest-neighbor spacings.
    """
    if len(collisions) < 3:
        return np.array([])

    times = sorted([c[0] for c in collisions])
    spacings = np.diff(times).astype(np.float64)

    # Remove zero spacings (simultaneous events)
    spacings = spacings[spacings > 0]

    if len(spacings) < 5:
        return np.array([])

    if normalize:
        mean_s = np.mean(spacings)
        if mean_s > 0:
            spacings = spacings / mean_s

    return spacings


# ============================================================
# Alternative: Difference-based particle detection (much faster)
# ============================================================

def detect_particles_difference(spacetime):
    """
    Fast particle detection using temporal XOR / difference.
    Particles are cells that change relative to a shifted copy.

    Returns activity count per timestep and inter-event spacings.
    """
    steps, width = spacetime.shape

    # Method 1: Temporal difference (cells that changed from t-1 to t)
    temporal_diff = np.zeros(steps, dtype=np.int32)
    for t in range(1, steps):
        temporal_diff[t] = np.sum(spacetime[t] != spacetime[t-1])

    # Method 2: Diagonal difference (detect gliders moving at speed 1)
    diag_events = []
    for t in range(1, steps):
        for x in range(width):
            # Check if cell differs from diagonal predecessor (left-moving glider)
            if spacetime[t, x] != spacetime[t-1, (x-1) % width]:
                diag_events.append(t)
                break  # One event per timestep is enough

    return temporal_diff, diag_events


def compute_density_fluctuation_spacings(spacetime, stripe_width=10):
    """
    Alternative approach: Divide the CA into vertical stripes.
    For each stripe, compute the density (fraction of 1s) at each timestep.
    Look at peaks in density fluctuation as "events."
    Extract spacing between peaks.
    """
    steps, width = spacetime.shape
    n_stripes = width // stripe_width

    all_spacings = []

    for s in range(n_stripes):
        start = s * stripe_width
        end = start + stripe_width
        stripe = spacetime[:, start:end]

        # Density per timestep
        density = np.mean(stripe, axis=1)

        # Find local maxima
        peaks = []
        for t in range(1, steps - 1):
            if density[t] > density[t-1] and density[t] > density[t+1]:
                if density[t] > np.mean(density) + 0.5 * np.std(density):
                    peaks.append(t)

        if len(peaks) > 2:
            spacings = np.diff(peaks).astype(np.float64)
            mean_s = np.mean(spacings)
            if mean_s > 0:
                spacings = spacings / mean_s
                all_spacings.extend(spacings.tolist())

    return np.array(all_spacings)


def compute_column_correlation_spacings(spacetime, skip_transient=50):
    """
    Another approach: compute the autocorrelation of each column.
    Find the spacing between correlation peaks.
    """
    spacetime = spacetime[skip_transient:]
    steps, width = spacetime.shape

    all_spacings = []

    for x in range(width):
        col = spacetime[:, x].astype(np.float64)
        col = col - np.mean(col)

        if np.std(col) < 0.01:
            continue  # Skip constant columns

        # Autocorrelation
        autocorr = np.correlate(col, col, mode='full')
        autocorr = autocorr[len(autocorr)//2:]  # Keep positive lags only
        autocorr = autocorr / autocorr[0]  # Normalize

        # Find peaks in autocorrelation
        peaks = []
        for t in range(1, min(len(autocorr) - 1, 500)):
            if autocorr[t] > autocorr[t-1] and autocorr[t] > autocorr[t+1]:
                if autocorr[t] > 0.1:  # Significant peak
                    peaks.append(t)

        if len(peaks) > 3:
            spacings = np.diff(peaks).astype(np.float64)
            mean_s = np.mean(spacings)
            if mean_s > 0:
                spacings = spacings / mean_s
                all_spacings.extend(spacings.tolist())

    return np.array(all_spacings)


# ============================================================
# Diagonal Particle Tracking (for gliders)
# ============================================================

def track_diagonal_particles(spacetime, velocity_range=(-3, 4)):
    """
    Track particles moving along diagonals in the spacetime diagram.

    For each velocity v in velocity_range, scan diagonal lines
    (t, x + v*t) and look for persistent structures.

    Returns collision events where multiple particle tracks intersect.
    """
    steps, width = spacetime.shape

    particle_tracks = []  # List of (velocity, start_x, start_t, end_t)

    for v in range(velocity_range[0], velocity_range[1]):
        # For each starting position
        for start_x in range(width):
            # Follow the diagonal
            track_active = False
            track_start = 0
            active_count = 0

            for t in range(steps):
                x = (start_x + v * t) % width
                cell_active = spacetime[t, x] == 1

                if cell_active:
                    if not track_active:
                        track_start = t
                        track_active = True
                    active_count += 1
                else:
                    if track_active and active_count >= 5:  # Minimum track length
                        particle_tracks.append((v, start_x, track_start, t))
                    track_active = False
                    active_count = 0

    # Find collision points: where tracks with different velocities intersect
    collisions = []
    for i in range(len(particle_tracks)):
        v1, x1, t1_start, t1_end = particle_tracks[i]
        for j in range(i + 1, len(particle_tracks)):
            v2, x2, t2_start, t2_end = particle_tracks[j]
            if v1 == v2:
                continue  # Parallel tracks don't collide

            # Solve for intersection: x1 + v1*t = x2 + v2*t (mod width)
            if v1 != v2:
                # t = (x2 - x1) / (v1 - v2)
                t_intersect = (x2 - x1) / (v1 - v2)
                if t_intersect > 0 and t1_start <= t_intersect <= t1_end and t2_start <= t_intersect <= t2_end:
                    x_intersect = int(x1 + v1 * t_intersect) % width
                    collisions.append((int(t_intersect), x_intersect))

    return collisions, particle_tracks


# ============================================================
# Master analysis function for a single CA rule
# ============================================================

def analyze_rule(rule_number, ca_type='elementary', width=500, steps=2000,
                 n_trials=3, seed=None):
    """
    Run a CA rule and analyze its spacing statistics.

    Returns dict with KS statistics against GUE and Poisson.
    Uses multiple detection methods and returns the best result.
    """
    results = {
        'rule': rule_number,
        'ca_type': ca_type,
        'width': width,
        'steps': steps,
        'methods': {},
    }

    best_ks_gue = 1.0

    for trial in range(n_trials):
        if seed is not None:
            np.random.seed(seed + trial)
        else:
            np.random.seed(rule_number * 1000 + trial)

        # Create and run CA
        if ca_type == 'elementary':
            ca = ElementaryCA(rule_number, width)
        elif ca_type == 'radius2':
            ca = Radius2CA(rule_number, width)
        elif ca_type == 'totalistic3':
            ca = TotalisticCA3State(rule_number, width)
        else:
            raise ValueError(f"Unknown CA type: {ca_type}")

        spacetime = ca.run(steps)

        # Skip trivial CAs (all same state after transient)
        if np.std(spacetime[steps//2:]) < 0.01:
            results['trivial'] = True
            return results

        # Method 1: Density fluctuation spacings
        spacings_density = compute_density_fluctuation_spacings(spacetime)
        if len(spacings_density) >= 20:
            ks_gue = ks_test_gue_fast(spacings_density)
            ks_poisson = ks_test_poisson_fast(spacings_density)
            key = f'density_trial{trial}'
            results['methods'][key] = {
                'n_spacings': len(spacings_density),
                'ks_gue': float(ks_gue),
                'ks_poisson': float(ks_poisson),
                'mean': float(np.mean(spacings_density)),
                'std': float(np.std(spacings_density)),
            }
            best_ks_gue = min(best_ks_gue, ks_gue)

        # Method 2: Column autocorrelation spacings
        spacings_corr = compute_column_correlation_spacings(spacetime)
        if len(spacings_corr) >= 20:
            ks_gue = ks_test_gue_fast(spacings_corr)
            ks_poisson = ks_test_poisson_fast(spacings_corr)
            key = f'correlation_trial{trial}'
            results['methods'][key] = {
                'n_spacings': len(spacings_corr),
                'ks_gue': float(ks_gue),
                'ks_poisson': float(ks_poisson),
                'mean': float(np.mean(spacings_corr)),
                'std': float(np.std(spacings_corr)),
            }
            best_ks_gue = min(best_ks_gue, ks_gue)

        # Method 3: Activity-based detection (for rules with clear background)
        for bg_period in [1, 2]:
            activity = detect_activity(spacetime, background_period=bg_period)
            activity_fraction = np.mean(activity)

            # Only meaningful if activity is neither too rare nor too common
            if 0.05 < activity_fraction < 0.8:
                # Count active cells per row as events
                row_activity = np.sum(activity, axis=1).astype(np.float64)

                # Find peaks in row activity
                peaks = []
                for t in range(1, steps - 1):
                    if row_activity[t] > row_activity[t-1] and row_activity[t] > row_activity[t+1]:
                        if row_activity[t] > np.mean(row_activity) + 0.3 * np.std(row_activity):
                            peaks.append(t)

                if len(peaks) > 10:
                    spacings = np.diff(peaks).astype(np.float64)
                    spacings = spacings[spacings > 0]
                    if len(spacings) > 10:
                        mean_s = np.mean(spacings)
                        if mean_s > 0:
                            spacings = spacings / mean_s
                            ks_gue = ks_test_gue_fast(spacings)
                            ks_poisson = ks_test_poisson_fast(spacings)
                            key = f'activity_bg{bg_period}_trial{trial}'
                            results['methods'][key] = {
                                'n_spacings': len(spacings),
                                'ks_gue': float(ks_gue),
                                'ks_poisson': float(ks_poisson),
                                'mean': float(np.mean(spacings)),
                                'std': float(np.std(spacings)),
                                'activity_fraction': float(activity_fraction),
                            }
                            best_ks_gue = min(best_ks_gue, ks_gue)

    results['best_ks_gue'] = float(best_ks_gue)
    results['trivial'] = False

    return results


def ks_test_gue_fast(spacings):
    """Fast KS statistic against GUE (no p-value computation)."""
    sorted_s = np.sort(spacings)
    n = len(sorted_s)
    ecdf = np.arange(1, n + 1) / n

    # Compute Wigner CDF at each point
    cdf_vals = wigner_surmise_cdf(sorted_s)

    ecdf_minus = np.arange(0, n) / n
    d_plus = np.max(ecdf - cdf_vals)
    d_minus = np.max(cdf_vals - ecdf_minus)
    return max(d_plus, d_minus)


def ks_test_poisson_fast(spacings):
    """Fast KS statistic against exponential distribution."""
    result = stats.kstest(spacings, 'expon', args=(0, 1))
    return result.statistic


# ============================================================
# Quick scan of all 256 elementary rules
# ============================================================

def scan_elementary_rules(width=300, steps=1500, verbose=True):
    """Scan all 256 elementary CA rules and rank by GUE fit."""
    results = []

    for rule in range(256):
        if verbose and rule % 32 == 0:
            print(f"  Scanning rules {rule}-{min(rule+31, 255)}...")

        try:
            result = analyze_rule(rule, ca_type='elementary', width=width,
                                steps=steps, n_trials=2)
            results.append(result)
        except Exception as e:
            print(f"  Rule {rule} failed: {e}")
            results.append({'rule': rule, 'best_ks_gue': 1.0, 'error': str(e)})

    # Sort by best KS distance to GUE
    results.sort(key=lambda r: r.get('best_ks_gue', 1.0))

    return results


if __name__ == '__main__':
    import time

    print("=== CA Framework Test ===")
    print("Testing a few well-known rules...")

    interesting_rules = [30, 54, 90, 110, 150, 184]

    for rule in interesting_rules:
        t0 = time.time()
        result = analyze_rule(rule, width=300, steps=1000, n_trials=2)
        elapsed = time.time() - t0

        print(f"\nRule {rule} ({elapsed:.1f}s):")
        print(f"  Trivial: {result.get('trivial', 'N/A')}")
        print(f"  Best KS(GUE): {result.get('best_ks_gue', 'N/A'):.4f}")
        for method_name, method_data in result.get('methods', {}).items():
            print(f"  {method_name}: KS(GUE)={method_data['ks_gue']:.4f}, "
                  f"KS(Poisson)={method_data['ks_poisson']:.4f}, "
                  f"n={method_data['n_spacings']}")
