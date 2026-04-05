#!/usr/bin/env python3
"""
Step 3: Scan all 256 elementary CA rules on Modal cloud compute.

Sends the entire CA analysis framework as a self-contained script to Modal,
runs all 256 rules, and retrieves results ranked by GUE fit.
"""

import sys
import json
import os
import time

sys.path.insert(0, "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/modal")
from run_remote import remote_heavy

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# The entire analysis framework, self-contained for Modal
CA_SCAN_SCRIPT = '''
import numpy as np
from scipy import stats
from scipy.integrate import quad
import time
import json

# ============================================================
# GUE reference
# ============================================================

def wigner_surmise_pdf(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_surmise_cdf_single(s):
    val, _ = quad(wigner_surmise_pdf, 0, max(s, 0))
    return val

def wigner_surmise_cdf(s):
    if np.isscalar(s):
        return wigner_surmise_cdf_single(s)
    return np.array([wigner_surmise_cdf_single(si) for si in s])

def ks_test_gue_fast(spacings):
    sorted_s = np.sort(spacings)
    n = len(sorted_s)
    ecdf = np.arange(1, n + 1) / n
    cdf_vals = wigner_surmise_cdf(sorted_s)
    ecdf_minus = np.arange(0, n) / n
    d_plus = np.max(ecdf - cdf_vals)
    d_minus = np.max(cdf_vals - ecdf_minus)
    return max(d_plus, d_minus)

def ks_test_poisson_fast(spacings):
    result = stats.kstest(spacings, 'expon', args=(0, 1))
    return result.statistic

# ============================================================
# Elementary CA Engine
# ============================================================

class ElementaryCA:
    def __init__(self, rule_number, width=500):
        self.rule_number = rule_number
        self.width = width
        self.rule_table = np.array([(rule_number >> i) & 1 for i in range(8)], dtype=np.uint8)

    def step(self, state):
        padded = np.concatenate([[state[-1]], state, [state[0]]])
        neighborhood = (padded[:-2] << 2) | (padded[1:-1] << 1) | padded[2:]
        return self.rule_table[neighborhood]

    def run(self, steps, initial=None):
        if initial is None:
            initial = np.random.randint(0, 2, self.width, dtype=np.uint8)
        spacetime = np.zeros((steps, self.width), dtype=np.uint8)
        spacetime[0] = initial
        for t in range(1, steps):
            spacetime[t] = self.step(spacetime[t-1])
        return spacetime

# ============================================================
# Spacing extraction methods
# ============================================================

def compute_density_fluctuation_spacings(spacetime, stripe_width=10):
    steps, width = spacetime.shape
    n_stripes = width // stripe_width
    all_spacings = []
    for s in range(n_stripes):
        start = s * stripe_width
        end = start + stripe_width
        stripe = spacetime[:, start:end]
        density = np.mean(stripe, axis=1)
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
    spacetime = spacetime[skip_transient:]
    steps, width = spacetime.shape
    all_spacings = []
    for x in range(width):
        col = spacetime[:, x].astype(np.float64)
        col = col - np.mean(col)
        if np.std(col) < 0.01:
            continue
        autocorr = np.correlate(col, col, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        autocorr = autocorr / (autocorr[0] + 1e-10)
        peaks = []
        for t in range(1, min(len(autocorr) - 1, 500)):
            if autocorr[t] > autocorr[t-1] and autocorr[t] > autocorr[t+1]:
                if autocorr[t] > 0.1:
                    peaks.append(t)
        if len(peaks) > 3:
            spacings = np.diff(peaks).astype(np.float64)
            mean_s = np.mean(spacings)
            if mean_s > 0:
                spacings = spacings / mean_s
                all_spacings.extend(spacings.tolist())
    return np.array(all_spacings)

def compute_activity_spacings(spacetime, bg_period=1):
    steps, width = spacetime.shape
    if bg_period == 1:
        bg = int(np.round(np.mean(spacetime)))
        activity = (spacetime != bg).astype(np.uint8)
    elif bg_period == 2:
        checker1 = np.zeros_like(spacetime)
        for t in range(steps):
            for x in range(width):
                checker1[t, x] = (t + x) % 2
        diff1 = np.sum(spacetime != checker1)
        diff2 = np.sum(spacetime != (1 - checker1))
        if diff1 < diff2:
            activity = (spacetime != checker1).astype(np.uint8)
        else:
            activity = (spacetime != (1 - checker1)).astype(np.uint8)
    else:
        activity = np.zeros_like(spacetime, dtype=np.uint8)
        for t in range(bg_period, steps):
            activity[t] = (spacetime[t] != spacetime[t - bg_period]).astype(np.uint8)

    activity_fraction = np.mean(activity)
    if activity_fraction < 0.05 or activity_fraction > 0.8:
        return np.array([]), activity_fraction

    row_activity = np.sum(activity, axis=1).astype(np.float64)
    peaks = []
    mean_act = np.mean(row_activity)
    std_act = np.std(row_activity)
    if std_act < 0.01:
        return np.array([]), activity_fraction

    for t in range(1, steps - 1):
        if row_activity[t] > row_activity[t-1] and row_activity[t] > row_activity[t+1]:
            if row_activity[t] > mean_act + 0.3 * std_act:
                peaks.append(t)

    if len(peaks) <= 5:
        return np.array([]), activity_fraction

    spacings = np.diff(peaks).astype(np.float64)
    spacings = spacings[spacings > 0]
    if len(spacings) <= 5:
        return np.array([]), activity_fraction

    mean_s = np.mean(spacings)
    if mean_s > 0:
        spacings = spacings / mean_s

    return spacings, activity_fraction

def compute_row_entropy_spacings(spacetime, skip_transient=100):
    """Compute spacings from row-level Shannon entropy fluctuations."""
    spacetime = spacetime[skip_transient:]
    steps, width = spacetime.shape

    entropies = np.zeros(steps)
    for t in range(steps):
        p1 = np.mean(spacetime[t])
        p0 = 1 - p1
        if p0 > 0 and p1 > 0:
            entropies[t] = -p0 * np.log2(p0) - p1 * np.log2(p1)

    if np.std(entropies) < 0.001:
        return np.array([])

    # Find peaks
    peaks = []
    mean_e = np.mean(entropies)
    std_e = np.std(entropies)
    for t in range(1, steps - 1):
        if entropies[t] > entropies[t-1] and entropies[t] > entropies[t+1]:
            if entropies[t] > mean_e + 0.3 * std_e:
                peaks.append(t)

    if len(peaks) <= 5:
        return np.array([])

    spacings = np.diff(peaks).astype(np.float64)
    spacings = spacings[spacings > 0]
    if len(spacings) <= 5:
        return np.array([])

    mean_s = np.mean(spacings)
    if mean_s > 0:
        spacings = spacings / mean_s

    return spacings

def compute_difference_pattern_spacings(spacetime, skip_transient=50):
    """
    Compute spacings from the temporal difference pattern.
    Count number of changed cells per timestep. Peaks in this
    signal correspond to particle interaction events.
    """
    spacetime = spacetime[skip_transient:]
    steps, width = spacetime.shape

    changes = np.zeros(steps)
    for t in range(1, steps):
        changes[t] = np.sum(spacetime[t] != spacetime[t-1])

    if np.std(changes) < 0.5:
        return np.array([])

    # Find peaks
    peaks = []
    mean_c = np.mean(changes)
    std_c = np.std(changes)
    for t in range(2, steps - 1):
        if changes[t] > changes[t-1] and changes[t] > changes[t+1]:
            if changes[t] > mean_c + 0.5 * std_c:
                peaks.append(t)

    if len(peaks) <= 5:
        return np.array([])

    spacings = np.diff(peaks).astype(np.float64)
    spacings = spacings[spacings > 0]
    if len(spacings) <= 5:
        return np.array([])

    mean_s = np.mean(spacings)
    if mean_s > 0:
        spacings = spacings / mean_s

    return spacings


# ============================================================
# Main analysis for a single rule
# ============================================================

def analyze_rule(rule_number, width=500, steps=2000, n_trials=3):
    results = {
        'rule': rule_number,
        'width': width,
        'steps': steps,
        'methods': {},
    }
    best_ks_gue = 1.0

    for trial in range(n_trials):
        np.random.seed(rule_number * 1000 + trial + 42)

        ca = ElementaryCA(rule_number, width)
        spacetime = ca.run(steps)

        # Check triviality
        if np.std(spacetime[steps//2:].astype(float)) < 0.01:
            results['trivial'] = True
            return results

        # Method 1: Density fluctuation spacings
        spacings = compute_density_fluctuation_spacings(spacetime)
        if len(spacings) >= 20:
            ks_gue = ks_test_gue_fast(spacings)
            ks_poisson = ks_test_poisson_fast(spacings)
            key = f'density_t{trial}'
            results['methods'][key] = {
                'n': int(len(spacings)), 'ks_gue': float(ks_gue),
                'ks_poi': float(ks_poisson), 'mean': float(np.mean(spacings)),
                'std': float(np.std(spacings)),
            }
            best_ks_gue = min(best_ks_gue, ks_gue)

        # Method 2: Column autocorrelation
        spacings = compute_column_correlation_spacings(spacetime)
        if len(spacings) >= 20:
            ks_gue = ks_test_gue_fast(spacings)
            ks_poisson = ks_test_poisson_fast(spacings)
            key = f'corr_t{trial}'
            results['methods'][key] = {
                'n': int(len(spacings)), 'ks_gue': float(ks_gue),
                'ks_poi': float(ks_poisson), 'mean': float(np.mean(spacings)),
                'std': float(np.std(spacings)),
            }
            best_ks_gue = min(best_ks_gue, ks_gue)

        # Method 3: Activity-based (bg period 1 and 2)
        for bg in [1, 2]:
            spacings, act_frac = compute_activity_spacings(spacetime, bg_period=bg)
            if len(spacings) >= 15:
                ks_gue = ks_test_gue_fast(spacings)
                ks_poisson = ks_test_poisson_fast(spacings)
                key = f'act_bg{bg}_t{trial}'
                results['methods'][key] = {
                    'n': int(len(spacings)), 'ks_gue': float(ks_gue),
                    'ks_poi': float(ks_poisson), 'mean': float(np.mean(spacings)),
                    'std': float(np.std(spacings)), 'act_frac': float(act_frac),
                }
                best_ks_gue = min(best_ks_gue, ks_gue)

        # Method 4: Row entropy
        spacings = compute_row_entropy_spacings(spacetime)
        if len(spacings) >= 15:
            ks_gue = ks_test_gue_fast(spacings)
            ks_poisson = ks_test_poisson_fast(spacings)
            key = f'entropy_t{trial}'
            results['methods'][key] = {
                'n': int(len(spacings)), 'ks_gue': float(ks_gue),
                'ks_poi': float(ks_poisson), 'mean': float(np.mean(spacings)),
                'std': float(np.std(spacings)),
            }
            best_ks_gue = min(best_ks_gue, ks_gue)

        # Method 5: Difference pattern
        spacings = compute_difference_pattern_spacings(spacetime)
        if len(spacings) >= 15:
            ks_gue = ks_test_gue_fast(spacings)
            ks_poisson = ks_test_poisson_fast(spacings)
            key = f'diff_t{trial}'
            results['methods'][key] = {
                'n': int(len(spacings)), 'ks_gue': float(ks_gue),
                'ks_poi': float(ks_poisson), 'mean': float(np.mean(spacings)),
                'std': float(np.std(spacings)),
            }
            best_ks_gue = min(best_ks_gue, ks_gue)

    results['best_ks_gue'] = float(best_ks_gue)
    results['trivial'] = False
    return results


# ============================================================
# Scan all 256 rules
# ============================================================

WIDTH = ARGS.get("width", 500)
STEPS = ARGS.get("steps", 2000)
N_TRIALS = ARGS.get("n_trials", 3)
RULE_START = ARGS.get("rule_start", 0)
RULE_END = ARGS.get("rule_end", 256)

print(f"Scanning rules {RULE_START}-{RULE_END-1}, width={WIDTH}, steps={STEPS}, trials={N_TRIALS}")
t0 = time.time()

all_results = []
for rule in range(RULE_START, RULE_END):
    try:
        result = analyze_rule(rule, width=WIDTH, steps=STEPS, n_trials=N_TRIALS)
        all_results.append(result)
        if rule % 32 == 0:
            elapsed = time.time() - t0
            print(f"  Rule {rule}: best_ks_gue={result.get('best_ks_gue', 1.0):.4f} ({elapsed:.0f}s)")
    except Exception as e:
        print(f"  Rule {rule} FAILED: {e}")
        all_results.append({'rule': rule, 'best_ks_gue': 1.0, 'error': str(e), 'trivial': True})

# Sort by best KS distance to GUE
all_results.sort(key=lambda r: r.get('best_ks_gue', 1.0))

elapsed = time.time() - t0
print(f"\\nCompleted in {elapsed:.0f}s")

# Print top 20
print("\\n=== TOP 20 RULES (closest to GUE) ===")
for r in all_results[:20]:
    if r.get('trivial'):
        continue
    print(f"Rule {r['rule']:3d}: best_ks_gue = {r['best_ks_gue']:.4f}")
    for method_name, method_data in r.get('methods', {}).items():
        print(f"    {method_name}: KS(GUE)={method_data['ks_gue']:.4f}, "
              f"KS(Poi)={method_data['ks_poi']:.4f}, n={method_data['n']}")

# Categorize results
trivial_count = sum(1 for r in all_results if r.get('trivial'))
nontrivial = [r for r in all_results if not r.get('trivial')]
print(f"\\nTrivial rules: {trivial_count}")
print(f"Non-trivial rules: {len(nontrivial)}")

if nontrivial:
    ks_values = [r['best_ks_gue'] for r in nontrivial]
    print(f"KS(GUE) range: {min(ks_values):.4f} - {max(ks_values):.4f}")
    print(f"KS(GUE) median: {np.median(ks_values):.4f}")

RESULTS["all_results"] = all_results
RESULTS["top20"] = all_results[:20]
RESULTS["n_trivial"] = trivial_count
RESULTS["n_nontrivial"] = len(nontrivial)
RESULTS["elapsed_seconds"] = elapsed
'''

def main():
    print("Launching CA scan on Modal (remote_heavy)...")
    print("Scanning all 256 elementary CA rules, width=500, steps=2000, 3 trials each")
    print("This may take 10-30 minutes...")

    t0 = time.time()

    result = remote_heavy(CA_SCAN_SCRIPT, args={
        "width": 500,
        "steps": 2000,
        "n_trials": 3,
        "rule_start": 0,
        "rule_end": 256,
    })

    elapsed = time.time() - t0
    print(f"\nModal execution completed in {elapsed:.0f}s")

    if result.get("error"):
        print(f"ERROR: {result['error']}")
        return

    print("\n=== STDOUT ===")
    print(result.get("stdout", "(none)"))

    # Save results
    results_data = result.get("results", {})
    output_file = os.path.join(OUTPUT_DIR, 'elementary_scan_results.json')
    with open(output_file, 'w') as f:
        json.dump(results_data, f, indent=2)
    print(f"\nResults saved to {output_file}")

    return results_data


if __name__ == '__main__':
    main()
