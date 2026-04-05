"""
Fetch elliptic curve BSD invariant data from LMFDB API.
We'll get curves of rank 0, 1, 2, and 3 separately to ensure good coverage.
"""
import requests
import json
import time
import sys

BASE_URL = "https://www.lmfdb.org/api/ec/curves/"
FIELDS = "lmfdb_label,conductor,rank,torsion_order,tamagawa_product,real_period,regulator,analytic_sha,jinv,disc,ainvs,torsion_structure"

def fetch_curves(rank, limit=200, offset=0):
    """Fetch curves of a given rank from LMFDB."""
    params = {
        '_fields': FIELDS,
        '_limit': limit,
        '_offset': offset,
        'rank': rank,
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data.get('data', [])
    except Exception as e:
        print(f"Error fetching rank {rank}: {e}", file=sys.stderr)
        return []

all_curves = []
for r in [0, 1, 2, 3]:
    target = 500 if r <= 1 else 200
    print(f"Fetching rank {r} curves (target: {target})...")
    batch_size = 100
    fetched = 0
    for offset in range(0, target, batch_size):
        batch = fetch_curves(r, limit=batch_size, offset=offset)
        if not batch:
            break
        all_curves.extend(batch)
        fetched += len(batch)
        print(f"  rank {r}: got {len(batch)} curves (total so far: {fetched})")
        time.sleep(0.5)  # be polite to the API

print(f"\nTotal curves fetched: {len(all_curves)}")

# Save raw data
outpath = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/bsd-conjecture/approach-1-ml/data/lmfdb_curves_raw.json"
with open(outpath, 'w') as f:
    json.dump(all_curves, f, indent=2)
print(f"Saved to {outpath}")

# Print rank distribution
from collections import Counter
ranks = Counter(c.get('rank') for c in all_curves)
print(f"Rank distribution: {dict(sorted(ranks.items()))}")
