"""
Step 1: Generate arithmetic data for elliptic curves using SageMath.

For each curve we collect:
  - Cremona label
  - Rank (algebraic)
  - Conductor
  - Analytic Sha (|Sha| from BSD formula)
  - Torsion order
  - a_p (Frobenius traces) at first N primes
  - Reduction type at each prime (0=good, 1=split mult, -1=nonsplit mult, 2=additive)

We target curves of rank 0, 1, 2, and 3 to test TDA rank discrimination.
"""

import json
import os

class SageEncoder(json.JSONEncoder):
    """Handle Sage integer/float types."""
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

OUTPUT_DIR = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/approach-3-tda/data"
NUM_PRIMES = 100  # First 100 primes (up to 541)

prime_list = primes_first_n(NUM_PRIMES)

def to_native(x):
    """Convert Sage types to native Python types for JSON serialization."""
    if x is None:
        return None
    try:
        if hasattr(x, 'pyobject'):
            return x.pyobject()
    except:
        pass
    try:
        return int(x)
    except:
        pass
    try:
        return float(x)
    except:
        pass
    return str(x)

def curve_data(label):
    """Extract full arithmetic data for a curve given its Cremona label."""
    try:
        E = EllipticCurve(label)
        r = E.rank()
        N = E.conductor()

        # Analytic Sha — can fail for high rank
        try:
            sha_an = float(E.sha().an_numerical(prec=53))
        except:
            sha_an = None

        torsion = int(E.torsion_order())

        # Frobenius traces
        ap_values = [int(E.ap(p)) for p in prime_list]

        # Reduction types
        red_types = []
        for p in prime_list:
            if int(N) % int(p) != 0:
                red_types.append(0)  # good reduction
            else:
                try:
                    Ep = E.local_data(p)
                    rt = Ep.bad_reduction_type()
                    if rt is None:
                        red_types.append(0)
                    else:
                        red_types.append(int(rt))
                except:
                    red_types.append(0)

        # Tamagawa numbers at bad primes
        tamagawa = int(E.tamagawa_product())

        # Real period
        try:
            omega = float(E.period_lattice().omega())
        except:
            omega = None

        # Regulator (height pairing det)
        try:
            reg = float(E.regulator())
        except:
            reg = None

        return {
            'label': str(label),
            'rank': int(r),
            'conductor': int(N),
            'sha_an': sha_an,
            'torsion': torsion,
            'tamagawa': tamagawa,
            'omega': omega,
            'regulator': reg,
            'ap': ap_values,
            'reduction_types': red_types,
        }
    except Exception as e:
        print(f"  FAILED {label}: {e}")
        return None


# ---------------------------------------------------------------
# Collect curves by rank
# ---------------------------------------------------------------
rank0_labels = []
rank1_labels = []
rank2_labels = []
rank3_labels = []

print("=== Gathering curves from Cremona database ===")

target = {0: 80, 1: 80, 2: 40, 3: 10}
counts = {0: 0, 1: 0, 2: 0, 3: 0}

for N in range(11, 500000):
    if all(counts[r] >= target[r] for r in target):
        break
    try:
        curves = cremona_optimal_curves(N)
    except:
        continue
    for E in curves:
        try:
            r = int(E.rank())
            if r in counts and counts[r] < target[r]:
                label = str(E.cremona_label())
                counts[r] += 1
                if r == 0: rank0_labels.append(label)
                elif r == 1: rank1_labels.append(label)
                elif r == 2: rank2_labels.append(label)
                elif r == 3: rank3_labels.append(label)
                if counts[r] % 10 == 0:
                    print(f"  Rank {r}: {counts[r]} curves collected")
        except:
            continue

print(f"\nFinal counts: {counts}")

# Add well-known curves for validation
known_curves = ['11a1', '37a1', '389a1', '5077a1']
all_labels = rank0_labels + rank1_labels + rank2_labels + rank3_labels
for lbl in known_curves:
    if lbl not in all_labels:
        all_labels.append(lbl)

print(f"Total curves to process: {len(all_labels)}")
print("Extracting arithmetic data...")

all_data = []
for i, label in enumerate(all_labels):
    if i % 20 == 0:
        print(f"  Processing {i}/{len(all_labels)}...")
    d = curve_data(label)
    if d is not None:
        all_data.append(d)

print(f"\nSuccessfully extracted data for {len(all_data)} curves")

# Save
outpath = os.path.join(OUTPUT_DIR, "curves_arithmetic_data.json")
indent_val = int(Integer(2))  # Force native Python int
with open(outpath, 'w') as f:
    json.dump({
        'num_primes': int(NUM_PRIMES),
        'prime_list': [int(p) for p in prime_list],
        'curves': all_data,
    }, f, indent=indent_val, cls=SageEncoder)

print(f"Saved to {outpath}")

# Print summary
for r in sorted(set(d['rank'] for d in all_data)):
    rc = [d for d in all_data if d['rank'] == r]
    sha_vals = [d['sha_an'] for d in rc if d['sha_an'] is not None]
    print(f"  Rank {r}: {len(rc)} curves, Sha values: {sorted(set(round(s,1) for s in sha_vals))[:10]}")
