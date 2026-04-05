"""
Step 5: Search for curves with non-trivial Sha (|Sha| > 1)
and test whether TDA persistence features detect it.

Sha(E) is the CORE arithmetic object in BSD. If persistent homology
detects Sha, that would be a genuine breakthrough connecting
computational topology to arithmetic geometry.
"""

import json
import os

OUTPUT_DIR = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/approach-3-tda/data"
NUM_PRIMES = 100
prime_list = primes_first_n(NUM_PRIMES)

class SageEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return int(obj)
        except (TypeError, ValueError):
            pass
        try:
            return float(obj)
        except (TypeError, ValueError):
            pass
        return super().default(obj)

def curve_data_full(E, label=None):
    """Extract full arithmetic data."""
    try:
        r = int(E.rank())
        N = int(E.conductor())
        if label is None:
            label = str(E.cremona_label())

        try:
            sha_an = float(E.sha().an_numerical(prec=53))
        except:
            sha_an = None

        torsion = int(E.torsion_order())
        ap_values = [int(E.ap(p)) for p in prime_list]

        red_types = []
        for p in prime_list:
            if N % int(p) != 0:
                red_types.append(0)
            else:
                try:
                    Ep = E.local_data(p)
                    rt = Ep.bad_reduction_type()
                    red_types.append(int(rt) if rt is not None else 0)
                except:
                    red_types.append(0)

        tamagawa = int(E.tamagawa_product())

        return {
            'label': str(label),
            'rank': r,
            'conductor': N,
            'sha_an': sha_an,
            'sha_an_rounded': int(round(sha_an)) if sha_an is not None else None,
            'torsion': torsion,
            'tamagawa': tamagawa,
            'ap': ap_values,
            'reduction_types': red_types,
        }
    except Exception as e:
        print(f"  FAILED: {e}")
        return None


# =====================================================================
# Strategy: find curves with |Sha| = 4, 9, 16, 25, etc.
# These exist but are rarer at low conductor.
# =====================================================================

print("=== Searching for curves with non-trivial Sha ===")

sha_curves = []
sha_counts = {}

# Known curves with non-trivial Sha:
known_sha_curves = [
    # Sha = 4
    ('571a1', 4),
    ('681b1', 4),
    ('960d1', 4),
    ('1058d1', 4),
    ('1070a1', 4),
    ('1246b1', 4),
    ('1913b1', 4),
    ('2006e1', 4),
    ('2429b1', 4),
    ('2534e1', 4),
    ('2541d1', 4),
    ('2674b1', 4),
    ('2710b1', 4),
    ('2768c1', 4),
    ('2849a1', 4),
    ('2932a1', 4),
    ('3054a1', 4),
    ('3306b1', 4),
    ('3536h1', 4),
    ('3712j1', 4),
    # Sha = 9
    ('5765a1', 9),
    ('7390a1', 9),
    ('8270a1', 9),
    ('11310a1', 9),
    # Sha = 16
    ('9834c1', 16),
    ('12846a1', 16),
    # Sha = 25
    ('67890a1', 25),
]

# Also search systematically
print("Checking known Sha > 1 curves...")
for label, expected_sha in known_sha_curves:
    try:
        E = EllipticCurve(label)
        data = curve_data_full(E, label)
        if data is not None and data['sha_an'] is not None:
            sha_round = int(round(data['sha_an']))
            if sha_round > 1:
                sha_curves.append(data)
                sha_counts[sha_round] = sha_counts.get(sha_round, 0) + 1
                if len(sha_curves) % 5 == 0:
                    print(f"  Found {len(sha_curves)} curves with Sha > 1")
    except Exception as e:
        pass

# Systematic search
print("\nSystematic search for Sha > 1 in Cremona database...")
for N in range(500, 15000):
    if len(sha_curves) >= 50:
        break
    try:
        for E in cremona_optimal_curves(N):
            try:
                r = int(E.rank())
                if r == 0:  # Sha is most interesting for rank 0
                    sha_val = float(E.sha().an_numerical(prec=53))
                    sha_round = int(round(sha_val))
                    if sha_round > 1:
                        data = curve_data_full(E)
                        if data is not None:
                            sha_curves.append(data)
                            sha_counts[sha_round] = sha_counts.get(sha_round, 0) + 1
                            print(f"  Found Sha={sha_round}: {data['label']} (conductor={N})")
            except:
                continue
    except:
        continue

print(f"\nTotal Sha > 1 curves: {len(sha_curves)}")
print(f"Sha distribution: {sha_counts}")

# Also get matching Sha=1 curves (same conductor range) as control
print("\nCollecting Sha=1 control curves...")
sha1_curves = []
sha_conductors = [c['conductor'] for c in sha_curves]
for N in range(min(sha_conductors) if sha_conductors else 500,
               max(sha_conductors) + 100 if sha_conductors else 5000):
    if len(sha1_curves) >= len(sha_curves):
        break
    try:
        for E in cremona_optimal_curves(N):
            try:
                r = int(E.rank())
                if r == 0:
                    sha_val = float(E.sha().an_numerical(prec=53))
                    if abs(sha_val - 1.0) < 0.1:
                        data = curve_data_full(E)
                        if data is not None:
                            sha1_curves.append(data)
                            if len(sha1_curves) % 10 == 0:
                                print(f"  {len(sha1_curves)} control curves")
                            if len(sha1_curves) >= max(60, len(sha_curves)):
                                break
            except:
                continue
    except:
        continue
    if len(sha1_curves) >= max(60, len(sha_curves)):
        break

print(f"Control (Sha=1) curves: {len(sha1_curves)}")

# Save
all_sha_data = {
    'sha_nontrivial': sha_curves,
    'sha_trivial': sha1_curves,
    'prime_list': [int(p) for p in prime_list],
    'num_primes': int(NUM_PRIMES),
}

outpath = os.path.join(OUTPUT_DIR, "sha_detection_data.json")
indent_val = int(Integer(2))
with open(outpath, 'w') as f:
    json.dump(all_sha_data, f, indent=indent_val, cls=SageEncoder)

print(f"\nSaved to {outpath}")
