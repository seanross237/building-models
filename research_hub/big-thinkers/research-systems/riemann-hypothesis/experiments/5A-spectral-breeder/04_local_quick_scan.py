#!/usr/bin/env python3
"""
Step 4: Quick local scan of known interesting CA rules.

Tests Class 3/4 boundary rules that are most likely to produce
complex particle dynamics (Rules 30, 45, 54, 60, 73, 86, 89, 90,
101, 102, 105, 110, 120, 122, 126, 135, 146, 149, 150, 153, 169, 182, 193, 225).
"""

import numpy as np
from scipy import stats
from scipy.integrate import quad
import json
import time
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# GUE reference
# ============================================================

def wigner_surmise_pdf(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_surmise_cdf(s):
    if np.isscalar(s):
        val, _ = quad(wigner_surmise_pdf, 0, max(s, 0))
        return val
    return np.array([quad(wigner_surmise_pdf, 0, max(si, 0))[0] for si in s])

def ks_test_gue(spacings):
    sorted_s = np.sort(spacings)
    n = len(sorted_s)
    ecdf = np.arange(1, n + 1) / n
    cdf_vals = wigner_surmise_cdf(sorted_s)
    ecdf_minus = np.arange(0, n) / n
    d_plus = np.max(ecdf - cdf_vals)
    d_minus = np.max(cdf_vals - ecdf_minus)
    ks_stat = max(d_plus, d_minus)
    p_value = stats.ksone.sf(ks_stat, n) * 2
    return ks_stat, min(p_value, 1.0)

def ks_test_poisson(spacings):
    result = stats.kstest(spacings, 'expon', args=(0, 1))
    return result.statistic, result.pvalue

# ============================================================
# CA engine (vectorized)
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
# Multiple spacing extraction methods
# ============================================================

def method_density_fluctuations(spacetime, stripe_width=10):
    """Density fluctuation peaks in vertical stripes."""
    steps, width = spacetime.shape
    n_stripes = width // stripe_width
    all_spacings = []
    for s in range(n_stripes):
        start_x = s * stripe_width
        stripe = spacetime[:, start_x:start_x + stripe_width]
        density = np.mean(stripe, axis=1)
        peaks = []
        mean_d = np.mean(density)
        std_d = np.std(density)
        if std_d < 0.001:
            continue
        for t in range(1, steps - 1):
            if density[t] > density[t-1] and density[t] > density[t+1]:
                if density[t] > mean_d + 0.5 * std_d:
                    peaks.append(t)
        if len(peaks) > 2:
            sp = np.diff(peaks).astype(np.float64)
            ms = np.mean(sp)
            if ms > 0:
                all_spacings.extend((sp / ms).tolist())
    return np.array(all_spacings) if all_spacings else np.array([])

def method_temporal_changes(spacetime, skip=50):
    """Peaks in the number of changed cells per timestep."""
    spacetime = spacetime[skip:]
    steps, width = spacetime.shape
    changes = np.array([np.sum(spacetime[t] != spacetime[t-1]) for t in range(1, steps)])
    if np.std(changes) < 0.5:
        return np.array([])
    peaks = []
    mean_c = np.mean(changes)
    std_c = np.std(changes)
    for t in range(1, len(changes) - 1):
        if changes[t] > changes[t-1] and changes[t] > changes[t+1]:
            if changes[t] > mean_c + 0.5 * std_c:
                peaks.append(t)
    if len(peaks) <= 5:
        return np.array([])
    sp = np.diff(peaks).astype(np.float64)
    sp = sp[sp > 0]
    if len(sp) <= 5:
        return np.array([])
    return sp / np.mean(sp)

def method_column_autocorrelation(spacetime, skip=50):
    """Peaks in column autocorrelation functions."""
    spacetime = spacetime[skip:]
    steps, width = spacetime.shape
    all_spacings = []
    for x in range(0, width, 2):  # Every other column for speed
        col = spacetime[:, x].astype(np.float64)
        col = col - np.mean(col)
        if np.std(col) < 0.01:
            continue
        autocorr = np.correlate(col, col, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        autocorr = autocorr / (autocorr[0] + 1e-10)
        peaks = []
        for t in range(1, min(len(autocorr) - 1, 300)):
            if autocorr[t] > autocorr[t-1] and autocorr[t] > autocorr[t+1]:
                if autocorr[t] > 0.1:
                    peaks.append(t)
        if len(peaks) > 3:
            sp = np.diff(peaks).astype(np.float64)
            ms = np.mean(sp)
            if ms > 0:
                all_spacings.extend((sp / ms).tolist())
    return np.array(all_spacings) if all_spacings else np.array([])

def method_row_entropy(spacetime, skip=100):
    """Row-level Shannon entropy peaks."""
    spacetime = spacetime[skip:]
    steps, width = spacetime.shape
    entropies = np.zeros(steps)
    for t in range(steps):
        p1 = np.mean(spacetime[t])
        p0 = 1 - p1
        if p0 > 0 and p1 > 0:
            entropies[t] = -p0 * np.log2(p0) - p1 * np.log2(p1)
    if np.std(entropies) < 0.001:
        return np.array([])
    peaks = []
    mean_e = np.mean(entropies)
    std_e = np.std(entropies)
    for t in range(1, steps - 1):
        if entropies[t] > entropies[t-1] and entropies[t] > entropies[t+1]:
            if entropies[t] > mean_e + 0.3 * std_e:
                peaks.append(t)
    if len(peaks) <= 5:
        return np.array([])
    sp = np.diff(peaks).astype(np.float64)
    sp = sp[sp > 0]
    if len(sp) <= 5:
        return np.array([])
    return sp / np.mean(sp)

def method_spatial_fourier_peaks(spacetime, skip=50):
    """
    Compute the dominant spatial frequency at each timestep.
    Look for peaks in the temporal variation of the dominant frequency.
    """
    spacetime = spacetime[skip:]
    steps, width = spacetime.shape
    dominant_freq = np.zeros(steps)
    for t in range(steps):
        fft = np.fft.rfft(spacetime[t].astype(np.float64))
        magnitudes = np.abs(fft[1:])  # Skip DC component
        if len(magnitudes) > 0:
            dominant_freq[t] = np.argmax(magnitudes) + 1

    if np.std(dominant_freq) < 0.1:
        return np.array([])

    # Find changes in dominant frequency
    change_times = []
    for t in range(1, steps):
        if dominant_freq[t] != dominant_freq[t-1]:
            change_times.append(t)

    if len(change_times) <= 5:
        return np.array([])

    sp = np.diff(change_times).astype(np.float64)
    sp = sp[sp > 0]
    if len(sp) <= 5:
        return np.array([])
    return sp / np.mean(sp)

def method_diagonal_density(spacetime, velocities=[-1, 0, 1], skip=50):
    """
    For each velocity v, look at density along diagonals (t, x+vt).
    Find peaks in the density signal. This directly detects
    particles/gliders at each velocity.
    """
    spacetime = spacetime[skip:]
    steps, width = spacetime.shape
    all_spacings = []

    for v in velocities:
        for start_x in range(0, width, 5):
            signal = np.zeros(steps)
            for t in range(steps):
                x = (start_x + v * t) % width
                signal[t] = spacetime[t, x]

            if np.std(signal) < 0.01:
                continue

            # Find transitions (0->1 or 1->0)
            transitions = []
            for t in range(1, steps):
                if signal[t] != signal[t-1]:
                    transitions.append(t)

            if len(transitions) > 10:
                sp = np.diff(transitions).astype(np.float64)
                sp = sp[sp > 0]
                if len(sp) > 5:
                    ms = np.mean(sp)
                    if ms > 0:
                        all_spacings.extend((sp / ms).tolist())

    return np.array(all_spacings) if all_spacings else np.array([])

# ============================================================
# Analyze a single rule with all methods
# ============================================================

def full_analysis(rule, width=500, steps=3000, n_trials=5):
    """Deep analysis of a single rule with multiple methods and trials."""
    all_methods_results = {}
    best_ks_gue = 1.0
    best_method = None

    methods = [
        ('density', method_density_fluctuations),
        ('temporal_changes', method_temporal_changes),
        ('column_autocorr', method_column_autocorrelation),
        ('row_entropy', method_row_entropy),
        ('fourier', method_spatial_fourier_peaks),
        ('diagonal', method_diagonal_density),
    ]

    for trial in range(n_trials):
        np.random.seed(rule * 10000 + trial * 7 + 137)
        ca = ElementaryCA(rule, width)
        spacetime = ca.run(steps)

        if np.std(spacetime[steps//2:].astype(float)) < 0.01:
            return {'rule': rule, 'trivial': True, 'best_ks_gue': 1.0}

        for method_name, method_func in methods:
            try:
                if method_name == 'diagonal':
                    spacings = method_func(spacetime, velocities=[-2, -1, 0, 1, 2])
                else:
                    spacings = method_func(spacetime)

                if len(spacings) >= 20:
                    ks_gue, p_gue = ks_test_gue(spacings)
                    ks_poi, p_poi = ks_test_poisson(spacings)

                    key = f'{method_name}_trial{trial}'
                    all_methods_results[key] = {
                        'n': int(len(spacings)),
                        'ks_gue': float(ks_gue),
                        'p_gue': float(p_gue),
                        'ks_poi': float(ks_poi),
                        'p_poi': float(p_poi),
                        'mean': float(np.mean(spacings)),
                        'std': float(np.std(spacings)),
                        'skew': float(stats.skew(spacings)),
                        'kurtosis': float(stats.kurtosis(spacings)),
                    }

                    if ks_gue < best_ks_gue:
                        best_ks_gue = ks_gue
                        best_method = key

                    # Save histogram for best methods
                    if ks_gue < 0.15:
                        bins = np.linspace(0, 4, 41)
                        hist, _ = np.histogram(spacings, bins=bins, density=True)
                        all_methods_results[key]['histogram'] = hist.tolist()
                        all_methods_results[key]['histogram_bins'] = ((bins[:-1] + bins[1:]) / 2).tolist()

            except Exception as e:
                pass  # Skip failed methods silently

    return {
        'rule': rule,
        'trivial': False,
        'best_ks_gue': float(best_ks_gue),
        'best_method': best_method,
        'methods': all_methods_results,
    }


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    # Known interesting rules: Class 3 (chaotic) and Class 4 (complex)
    # Class 3: 18, 22, 30, 45, 60, 73, 75, 86, 89, 90, 101, 102, 105,
    #          109, 120, 122, 126, 129, 135, 146, 149, 150, 153, 161, 169, 182, 193, 225
    # Class 4: 54, 106, 110
    interesting_rules = [
        18, 22, 30, 45, 54, 57, 60, 62, 73, 75, 86, 89, 90,
        101, 102, 105, 106, 109, 110, 120, 122, 126, 129,
        135, 146, 149, 150, 153, 161, 169, 182, 193, 225
    ]

    print(f"=== Deep Analysis of {len(interesting_rules)} Interesting Elementary CA Rules ===")
    print(f"Width=500, Steps=3000, Trials=5\n")

    all_results = []

    for rule in interesting_rules:
        t0 = time.time()
        result = full_analysis(rule, width=500, steps=3000, n_trials=5)
        elapsed = time.time() - t0

        all_results.append(result)

        if result.get('trivial'):
            print(f"Rule {rule:3d}: TRIVIAL ({elapsed:.1f}s)")
        else:
            print(f"Rule {rule:3d}: best_ks_gue = {result['best_ks_gue']:.4f} "
                  f"via {result.get('best_method', 'N/A')} ({elapsed:.1f}s)")

            # Show top 3 methods for this rule
            methods = result.get('methods', {})
            sorted_methods = sorted(methods.items(), key=lambda x: x[1]['ks_gue'])
            for m_name, m_data in sorted_methods[:3]:
                print(f"    {m_name}: KS(GUE)={m_data['ks_gue']:.4f} "
                      f"p={m_data['p_gue']:.4f}, "
                      f"KS(Poi)={m_data['ks_poi']:.4f}, "
                      f"n={m_data['n']}, "
                      f"std={m_data['std']:.3f}")

    # Sort and summarize
    all_results.sort(key=lambda r: r.get('best_ks_gue', 1.0))

    print(f"\n\n{'='*60}")
    print(f"=== FINAL RANKING (best GUE fit) ===")
    print(f"{'='*60}")
    for r in all_results[:15]:
        if r.get('trivial'):
            continue
        print(f"Rule {r['rule']:3d}: KS(GUE) = {r['best_ks_gue']:.4f} "
              f"[{r.get('best_method', 'N/A')}]")

    # Save results
    with open(os.path.join(OUTPUT_DIR, 'local_scan_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\nResults saved to local_scan_results.json")

    # Compare best CA result to zeta zero baseline
    baseline_file = os.path.join(OUTPUT_DIR, 'gue_baseline_results.json')
    if os.path.exists(baseline_file):
        with open(baseline_file) as f:
            baseline = json.load(f)
        zeta_ks = baseline['ks_gue_statistic']
        best_ca_ks = all_results[0]['best_ks_gue'] if all_results else 1.0
        print(f"\n=== COMPARISON ===")
        print(f"Zeta zeros KS(GUE): {zeta_ks:.4f}")
        print(f"Best CA KS(GUE):    {best_ca_ks:.4f}")
        if best_ca_ks < zeta_ks * 2:
            print("*** PROMISING: CA rule achieves comparable GUE fit! ***")
        else:
            print(f"CA fit is {best_ca_ks/zeta_ks:.1f}x worse than zeta zeros")
