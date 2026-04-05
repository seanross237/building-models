#!/usr/bin/env python3
"""
Step 5: Evolutionary search over extended CA rule spaces.

Goes beyond elementary CAs to search:
  1. Radius-2 binary CAs (2^32 rules - sampled)
  2. 3-state totalistic CAs (2187 rules - exhaustive)
  3. Hybrid rules (elementary CA with probabilistic mutation)

Uses a genetic algorithm with KS(GUE) as the fitness function.
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

def ks_gue(spacings):
    sorted_s = np.sort(spacings)
    n = len(sorted_s)
    ecdf = np.arange(1, n + 1) / n
    cdf_vals = wigner_surmise_cdf(sorted_s)
    ecdf_minus = np.arange(0, n) / n
    d_plus = np.max(ecdf - cdf_vals)
    d_minus = np.max(cdf_vals - ecdf_minus)
    return max(d_plus, d_minus)

def ks_poisson(spacings):
    return stats.kstest(spacings, 'expon', args=(0, 1)).statistic

# ============================================================
# CA Engines
# ============================================================

class ElementaryCA:
    def __init__(self, rule_table, width=300):
        self.width = width
        if isinstance(rule_table, int):
            self.rule_table = np.array([(rule_table >> i) & 1 for i in range(8)], dtype=np.uint8)
        else:
            self.rule_table = np.array(rule_table, dtype=np.uint8)

    def run(self, steps, seed=None):
        if seed is not None:
            np.random.seed(seed)
        state = np.random.randint(0, 2, self.width, dtype=np.uint8)
        spacetime = np.zeros((steps, self.width), dtype=np.uint8)
        spacetime[0] = state
        for t in range(1, steps):
            padded = np.concatenate([[state[-1]], state, [state[0]]])
            neighborhood = (padded[:-2] << 2) | (padded[1:-1] << 1) | padded[2:]
            state = self.rule_table[neighborhood]
            spacetime[t] = state
        return spacetime


class Radius2CA:
    def __init__(self, rule_table, width=300):
        self.width = width
        if isinstance(rule_table, (int, np.integer)):
            self.rule_table = np.array([(int(rule_table) >> i) & 1 for i in range(32)], dtype=np.uint8)
        else:
            self.rule_table = np.array(rule_table, dtype=np.uint8)

    def run(self, steps, seed=None):
        if seed is not None:
            np.random.seed(seed)
        state = np.random.randint(0, 2, self.width, dtype=np.uint8)
        spacetime = np.zeros((steps, self.width), dtype=np.uint8)
        spacetime[0] = state
        for t in range(1, steps):
            padded = np.concatenate([state[-2:], state, state[:2]])
            neighborhood = (
                (padded[:-4] << 4) | (padded[1:-3] << 3) |
                (padded[2:-2] << 2) | (padded[3:-1] << 1) | padded[4:]
            )
            state = self.rule_table[neighborhood]
            spacetime[t] = state
        return spacetime


class TotalisticCA3:
    def __init__(self, rule_table, width=300):
        self.width = width
        if isinstance(rule_table, (int, np.integer)):
            r = int(rule_table)
            self.rule_table = np.zeros(7, dtype=np.uint8)
            for i in range(7):
                self.rule_table[i] = r % 3
                r //= 3
        else:
            self.rule_table = np.array(rule_table, dtype=np.uint8)

    def run(self, steps, seed=None):
        if seed is not None:
            np.random.seed(seed)
        state = np.random.randint(0, 3, self.width, dtype=np.uint8)
        spacetime = np.zeros((steps, self.width), dtype=np.uint8)
        spacetime[0] = state
        for t in range(1, steps):
            padded = np.concatenate([[state[-1]], state, [state[0]]])
            total = padded[:-2].astype(int) + padded[1:-1].astype(int) + padded[2:].astype(int)
            state = self.rule_table[total]
            spacetime[t] = state
        return spacetime


# ============================================================
# Unified spacing extraction
# ============================================================

def extract_spacings(spacetime, methods=('density', 'temporal', 'diagonal')):
    """
    Extract spacings using multiple methods, return the one with
    the most data points that has reasonable statistics.
    """
    steps, width = spacetime.shape
    results = {}

    if 'density' in methods:
        spacings = _density_spacings(spacetime)
        if len(spacings) >= 15:
            results['density'] = spacings

    if 'temporal' in methods:
        spacings = _temporal_spacings(spacetime)
        if len(spacings) >= 15:
            results['temporal'] = spacings

    if 'diagonal' in methods:
        spacings = _diagonal_spacings(spacetime)
        if len(spacings) >= 15:
            results['diagonal'] = spacings

    if 'entropy' in methods:
        spacings = _entropy_spacings(spacetime)
        if len(spacings) >= 15:
            results['entropy'] = spacings

    return results


def _density_spacings(spacetime, stripe_width=10):
    steps, width = spacetime.shape
    n_stripes = width // stripe_width
    all_sp = []
    for s in range(n_stripes):
        stripe = spacetime[:, s*stripe_width:(s+1)*stripe_width]
        density = np.mean(stripe.astype(float), axis=1)
        peaks = _find_peaks(density, threshold_sigma=0.5)
        if len(peaks) > 2:
            sp = np.diff(peaks).astype(float)
            ms = np.mean(sp)
            if ms > 0:
                all_sp.extend((sp / ms).tolist())
    return np.array(all_sp)


def _temporal_spacings(spacetime, skip=50):
    spacetime = spacetime[skip:]
    steps = spacetime.shape[0]
    changes = np.array([np.sum(spacetime[t] != spacetime[t-1]) for t in range(1, steps)])
    if np.std(changes) < 0.5:
        return np.array([])
    peaks = _find_peaks(changes, threshold_sigma=0.5)
    if len(peaks) <= 5:
        return np.array([])
    sp = np.diff(peaks).astype(float)
    sp = sp[sp > 0]
    if len(sp) <= 5:
        return np.array([])
    return sp / np.mean(sp)


def _diagonal_spacings(spacetime, velocities=[-2, -1, 0, 1, 2], skip=50):
    spacetime = spacetime[skip:]
    steps, width = spacetime.shape
    all_sp = []
    for v in velocities:
        for start_x in range(0, width, 5):
            signal = np.array([spacetime[t, (start_x + v * t) % width] for t in range(steps)])
            if np.std(signal.astype(float)) < 0.01:
                continue
            transitions = np.where(np.diff(signal) != 0)[0]
            if len(transitions) > 10:
                sp = np.diff(transitions).astype(float)
                sp = sp[sp > 0]
                if len(sp) > 5:
                    ms = np.mean(sp)
                    if ms > 0:
                        all_sp.extend((sp / ms).tolist())
    return np.array(all_sp)


def _entropy_spacings(spacetime, skip=100):
    spacetime = spacetime[skip:]
    steps = spacetime.shape[0]
    n_states = int(spacetime.max()) + 1
    entropies = np.zeros(steps)
    for t in range(steps):
        counts = np.bincount(spacetime[t], minlength=n_states)
        probs = counts / counts.sum()
        probs = probs[probs > 0]
        entropies[t] = -np.sum(probs * np.log2(probs))
    if np.std(entropies) < 0.001:
        return np.array([])
    peaks = _find_peaks(entropies, threshold_sigma=0.3)
    if len(peaks) <= 5:
        return np.array([])
    sp = np.diff(peaks).astype(float)
    sp = sp[sp > 0]
    if len(sp) <= 5:
        return np.array([])
    return sp / np.mean(sp)


def _find_peaks(signal, threshold_sigma=0.5):
    """Find local maxima above mean + threshold_sigma * std."""
    mean_s = np.mean(signal)
    std_s = np.std(signal)
    threshold = mean_s + threshold_sigma * std_s
    peaks = []
    for t in range(1, len(signal) - 1):
        if signal[t] > signal[t-1] and signal[t] > signal[t+1]:
            if signal[t] > threshold:
                peaks.append(t)
    return peaks


# ============================================================
# Fitness evaluation
# ============================================================

def evaluate_fitness(ca_class, rule_table, width=300, steps=1500, n_trials=3):
    """
    Evaluate a CA rule's fitness (lower = better GUE match).
    Returns (best_ks_gue, best_method, spacings_info).
    """
    best_ks = 1.0
    best_method = None
    best_n = 0

    for trial in range(n_trials):
        try:
            ca = ca_class(rule_table, width)
            spacetime = ca.run(steps, seed=hash((str(rule_table), trial)) % (2**31))

            # Check triviality
            if np.std(spacetime[steps//2:].astype(float)) < 0.01:
                return 1.0, None, 0

            results = extract_spacings(spacetime, methods=('density', 'temporal', 'diagonal', 'entropy'))

            for method_name, spacings in results.items():
                if len(spacings) >= 20:
                    ks = ks_gue(spacings)
                    if ks < best_ks:
                        best_ks = ks
                        best_method = f"{method_name}_t{trial}"
                        best_n = len(spacings)
        except Exception:
            pass

    return best_ks, best_method, best_n


# ============================================================
# Genetic Algorithm for Radius-2 Rules
# ============================================================

def ga_radius2(pop_size=50, n_generations=30, mutation_rate=0.1,
               width=300, steps=1500, verbose=True):
    """
    Genetic algorithm search over radius-2 CA rules.
    Genome: 32-bit rule table (each bit = output for one neighborhood).
    """
    print(f"\n{'='*60}")
    print(f"Genetic Algorithm: Radius-2 CAs")
    print(f"Pop={pop_size}, Generations={n_generations}, Mutation={mutation_rate}")
    print(f"{'='*60}")

    # Initialize population with random rules
    population = [np.random.randint(0, 2, 32, dtype=np.uint8) for _ in range(pop_size)]

    # Also seed with some known interesting elementary CA rules extended to radius-2
    for rule_num in [30, 54, 90, 110, 150]:
        elem_table = np.array([(rule_num >> i) & 1 for i in range(8)], dtype=np.uint8)
        # Extend to radius-2 by using the inner 3 bits of the 5-bit neighborhood
        r2_table = np.zeros(32, dtype=np.uint8)
        for i in range(32):
            inner = (i >> 1) & 7  # Middle 3 bits
            r2_table[i] = elem_table[inner]
        population.append(r2_table)

    best_ever = 1.0
    best_ever_rule = None
    history = []

    for gen in range(n_generations):
        t0 = time.time()

        # Evaluate fitness
        fitness = []
        for rule_table in population:
            ks, method, n = evaluate_fitness(Radius2CA, rule_table, width, steps, n_trials=2)
            fitness.append((ks, method, n))

        # Sort by fitness (lower KS = better)
        ranked = sorted(zip(fitness, population), key=lambda x: x[0][0])

        gen_best_ks = ranked[0][0][0]
        gen_best_method = ranked[0][0][1]

        if gen_best_ks < best_ever:
            best_ever = gen_best_ks
            best_ever_rule = ranked[0][1].copy()

        history.append({
            'gen': gen,
            'best_ks': float(gen_best_ks),
            'mean_ks': float(np.mean([f[0] for f, _ in ranked if f[0] < 1.0])),
            'best_method': gen_best_method,
        })

        elapsed = time.time() - t0
        if verbose:
            print(f"Gen {gen:3d}: best={gen_best_ks:.4f}, "
                  f"mean={history[-1]['mean_ks']:.4f}, "
                  f"best_ever={best_ever:.4f} ({elapsed:.1f}s)")

        # Selection: keep top 40%
        survivors = [rule for _, rule in ranked[:int(0.4 * len(ranked))]]

        # Crossover + mutation to fill population
        new_pop = list(survivors)
        while len(new_pop) < pop_size:
            # Pick two parents
            p1 = survivors[np.random.randint(len(survivors))]
            p2 = survivors[np.random.randint(len(survivors))]

            # Single-point crossover
            crossover_point = np.random.randint(1, 31)
            child = np.concatenate([p1[:crossover_point], p2[crossover_point:]])

            # Mutation
            for i in range(len(child)):
                if np.random.random() < mutation_rate:
                    child[i] = 1 - child[i]

            new_pop.append(child)

        population = new_pop[:pop_size]

    return best_ever, best_ever_rule, history


# ============================================================
# Exhaustive search: 3-state totalistic CAs
# ============================================================

def scan_totalistic3(width=300, steps=1500, verbose=True):
    """Exhaustively scan all 2187 3-state totalistic CA rules."""
    print(f"\n{'='*60}")
    print(f"Exhaustive Scan: 3-State Totalistic CAs (2187 rules)")
    print(f"Width={width}, Steps={steps}")
    print(f"{'='*60}")

    results = []
    t0 = time.time()

    for rule_num in range(2187):
        ks, method, n = evaluate_fitness(TotalisticCA3, rule_num, width, steps, n_trials=2)
        results.append({
            'rule': rule_num,
            'ks_gue': float(ks),
            'method': method,
            'n': n,
        })

        if verbose and rule_num % 200 == 0:
            elapsed = time.time() - t0
            print(f"  Rule {rule_num}/2187 ({elapsed:.0f}s)")

    results.sort(key=lambda r: r['ks_gue'])

    elapsed = time.time() - t0
    print(f"\nCompleted in {elapsed:.0f}s")
    print(f"\nTop 10 3-state totalistic rules:")
    for r in results[:10]:
        print(f"  Rule {r['rule']:4d}: KS(GUE) = {r['ks_gue']:.4f} "
              f"via {r['method']}, n={r['n']}")

    return results


# ============================================================
# Random search: Radius-2 CAs
# ============================================================

def random_search_radius2(n_samples=500, width=300, steps=1500, verbose=True):
    """Random search over radius-2 CA rules."""
    print(f"\n{'='*60}")
    print(f"Random Search: Radius-2 CAs ({n_samples} samples)")
    print(f"{'='*60}")

    results = []
    t0 = time.time()

    for i in range(n_samples):
        rule_table = np.random.randint(0, 2, 32, dtype=np.uint8)
        ks, method, n = evaluate_fitness(Radius2CA, rule_table, width, steps, n_trials=2)
        results.append({
            'rule_table': rule_table.tolist(),
            'ks_gue': float(ks),
            'method': method,
            'n': n,
        })

        if verbose and i % 100 == 0:
            elapsed = time.time() - t0
            best_so_far = min(r['ks_gue'] for r in results)
            print(f"  Sample {i}/{n_samples}: best_so_far={best_so_far:.4f} ({elapsed:.0f}s)")

    results.sort(key=lambda r: r['ks_gue'])

    elapsed = time.time() - t0
    print(f"\nCompleted in {elapsed:.0f}s")
    print(f"\nTop 10 radius-2 rules (random):")
    for r in results[:10]:
        print(f"  KS(GUE) = {r['ks_gue']:.4f} via {r['method']}, n={r['n']}")

    return results


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    all_results = {}

    # 1. Scan 3-state totalistic CAs (exhaustive, 2187 rules)
    tot3_results = scan_totalistic3(width=300, steps=1500)
    all_results['totalistic3'] = tot3_results[:50]  # Save top 50

    # 2. Random search over radius-2 CAs
    r2_random = random_search_radius2(n_samples=300, width=300, steps=1500)
    all_results['radius2_random'] = r2_random[:50]

    # 3. Genetic algorithm for radius-2 CAs
    ga_best_ks, ga_best_rule, ga_history = ga_radius2(
        pop_size=30, n_generations=20, mutation_rate=0.1,
        width=300, steps=1500
    )
    all_results['radius2_ga'] = {
        'best_ks': float(ga_best_ks),
        'best_rule': ga_best_rule.tolist() if ga_best_rule is not None else None,
        'history': ga_history,
    }

    # Summary
    print(f"\n\n{'='*60}")
    print(f"=== EVOLUTIONARY SEARCH SUMMARY ===")
    print(f"{'='*60}")

    # Collect all best results
    all_best = []
    if tot3_results:
        all_best.append(('3-state totalistic', tot3_results[0]['ks_gue'], tot3_results[0]))
    if r2_random:
        all_best.append(('Radius-2 random', r2_random[0]['ks_gue'], r2_random[0]))
    all_best.append(('Radius-2 GA', ga_best_ks, {'rule': ga_best_rule}))

    all_best.sort(key=lambda x: x[1])

    print(f"\nBest results across all searches:")
    for name, ks, info in all_best:
        print(f"  {name}: KS(GUE) = {ks:.4f}")

    # Compare to zeta zero baseline
    baseline_file = os.path.join(OUTPUT_DIR, 'gue_baseline_results.json')
    if os.path.exists(baseline_file):
        with open(baseline_file) as f:
            baseline = json.load(f)
        zeta_ks = baseline['ks_gue_statistic']
        best_ca_ks = all_best[0][1] if all_best else 1.0
        print(f"\n  Zeta zeros KS(GUE): {zeta_ks:.4f}")
        print(f"  Best CA KS(GUE):    {best_ca_ks:.4f}")
        print(f"  Ratio: {best_ca_ks/zeta_ks:.1f}x")

    # Save
    with open(os.path.join(OUTPUT_DIR, 'evolutionary_search_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\nResults saved to evolutionary_search_results.json")
