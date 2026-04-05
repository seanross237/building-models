"""
curve_data.py — Extract elliptic curve arithmetic data using SageMath.

For each curve, we extract:
  - a_p (Frobenius traces) for primes up to a bound
  - Reduction type at each prime (good=0, split mult=+1, nonsplit mult=-1, additive=2)
  - Local Tamagawa numbers c_p
  - Global invariants: rank, conductor, |Sha|_an, regulator, real period, torsion order
  - The mod-ell Galois representation data (traces and determinants)

This module is designed to be run under sage -python.
"""

import json
import os
import sys

# Ensure we're running under SageMath
try:
    from sage.all import (
        EllipticCurve, primes, prime_range, ZZ, RR, matrix, GF,
        kronecker_symbol, next_prime
    )
except ImportError:
    print("ERROR: This module must be run under 'sage -python'", file=sys.stderr)
    sys.exit(1)


def reduction_type_code(E, p):
    """Return reduction type code: 0=good, 1=split mult, -1=nonsplit mult, 2=additive."""
    if not E.has_bad_reduction(p):
        return 0
    brt = E.local_data(p).bad_reduction_type()
    # brt: +1 = split multiplicative, -1 = nonsplit multiplicative, 0 = additive
    if brt == 0:
        return 2  # additive
    return int(brt)


def frobenius_matrix_mod_ell(ap, p, ell):
    """
    Construct the Frobenius matrix in GL(2, F_ell) for prime p.

    The characteristic polynomial of Frob_p is x^2 - a_p*x + p (for good reduction).
    We pick a canonical representative: upper triangular if a_p^2 - 4p is a square mod ell,
    otherwise a matrix with the right trace and determinant.
    """
    F = GF(ell)
    a = F(ap)
    d = F(p)  # determinant = p (from Weil pairing)

    # discriminant of char poly
    disc = a**2 - 4 * d

    if disc == F(0):
        # Repeated eigenvalue
        lam = a / F(2) if F(2) != F(0) else F(0)
        return matrix(F, [[lam, 1], [0, lam]])

    # Check if disc is a square in F_ell
    if ell == 2:
        return matrix(F, [[a, d], [1, 0]])

    if disc**(int((ell - 1) // 2)) == F(1):
        # disc is a QR mod ell — split case, diagonalizable
        sqrt_disc = disc.sqrt()
        lam1 = (a + sqrt_disc) / F(2)
        lam2 = (a - sqrt_disc) / F(2)
        return matrix(F, [[lam1, 0], [0, lam2]])
    else:
        # Non-split case — use companion matrix form
        return matrix(F, [[0, -d], [1, a]])


def extract_curve_data(label, prime_bound=200, ell=3):
    """
    Extract full arithmetic data for curve with given LMFDB label.

    Args:
        label: LMFDB label like '37a1'
        prime_bound: compute a_p for primes up to this bound
        ell: prime for mod-ell Galois representation

    Returns:
        dict with all extracted data
    """
    E = EllipticCurve(label)
    N = int(E.conductor())

    good_primes = []
    bad_primes = []
    all_primes_data = []

    for p in prime_range(2, prime_bound + 1):
        ap = int(E.ap(p))
        rt = reduction_type_code(E, p)

        entry = {
            'p': int(p),
            'a_p': ap,
            'reduction_type': rt,
            'p_divides_N': (N % p == 0),
        }

        if rt == 0:  # good reduction
            # Normalized Frobenius angle: a_p / (2*sqrt(p))
            entry['frobenius_angle'] = float(ap / (2 * float(p)**0.5))
            # Frobenius matrix mod ell
            frob = frobenius_matrix_mod_ell(ap, p, ell)
            entry['frob_trace_mod_ell'] = int(frob.trace())
            entry['frob_det_mod_ell'] = int(frob.det())
            entry['frob_matrix_mod_ell'] = [[int(frob[i][j]) for j in range(2)] for i in range(2)]
            good_primes.append(entry)
        else:
            entry['tamagawa_number'] = int(E.local_data(p).tamagawa_number())
            bad_primes.append(entry)

        all_primes_data.append(entry)

    # Global invariants
    rank = int(E.rank())
    sha_an = float(E.sha().an_numerical())

    # Regulator (0 for rank 0)
    if rank > 0:
        reg = float(E.regulator())
    else:
        reg = 1.0

    omega = float(E.period_lattice().omega())
    torsion = int(E.torsion_order())
    tam_product = 1
    for bd in bad_primes:
        tam_product *= bd.get('tamagawa_number', 1)

    # BSD prediction for L^(r)(E,1)/r!
    bsd_leading = (sha_an * omega * reg * tam_product) / (torsion**2)

    data = {
        'label': label,
        'conductor': N,
        'rank': rank,
        'sha_analytic': sha_an,
        'regulator': reg,
        'real_period': omega,
        'torsion_order': torsion,
        'tamagawa_product': tam_product,
        'bsd_leading_coefficient': bsd_leading,
        'prime_bound': prime_bound,
        'mod_ell': ell,
        'good_primes': good_primes,
        'bad_primes': bad_primes,
        'all_primes': all_primes_data,
        'a_p_list': [(int(e['p']), e['a_p']) for e in all_primes_data],
    }

    return data


def extract_test_suite(prime_bound=200, ell=3):
    """
    Extract data for a curated test suite of elliptic curves spanning
    ranks 0, 1, 2, 3 with varying conductor sizes and Sha values.
    """
    # Curated test curves (label, description)
    test_curves = [
        # Rank 0
        ('11a1', 'smallest conductor, rank 0, torsion Z/5'),
        ('14a1', 'rank 0, conductor 14'),
        ('15a1', 'rank 0, conductor 15'),
        ('17a1', 'rank 0, conductor 17'),
        ('19a1', 'rank 0, conductor 19'),
        ('32a1', 'rank 0, Sha=1'),
        ('48a1', 'rank 0'),
        ('57a1', 'rank 0'),
        # Rank 0 with larger Sha
        ('571a1', 'rank 0, |Sha|=4 (if computed)'),
        ('681b1', 'rank 0'),

        # Rank 1
        ('37a1', 'smallest conductor rank 1'),
        ('43a1', 'rank 1, conductor 43'),
        ('53a1', 'rank 1'),
        ('58a1', 'rank 1'),
        ('61a1', 'rank 1'),
        ('77a1', 'rank 1'),
        ('79a1', 'rank 1'),
        ('83a1', 'rank 1'),
        ('89a1', 'rank 1'),
        ('91a1', 'rank 1'),

        # Rank 2
        ('389a1', 'smallest conductor rank 2'),
        ('433a1', 'rank 2'),
        ('446a1', 'rank 2 (maybe)'),
        ('563a1', 'rank 2'),
        ('571b1', 'rank 2'),

        # Rank 3
        ('5077a1', 'smallest conductor rank 3'),
    ]

    results = []
    for label, desc in test_curves:
        try:
            data = extract_curve_data(label, prime_bound=prime_bound, ell=ell)
            data['description'] = desc
            results.append(data)
            print(f"  Extracted {label}: rank={data['rank']}, N={data['conductor']}, "
                  f"|Sha|={data['sha_analytic']:.2f}")
        except Exception as e:
            print(f"  FAILED {label}: {e}", file=sys.stderr)

    return results


def save_test_suite(output_dir, prime_bound=200, ell=3):
    """Extract and save the full test suite to JSON files."""
    os.makedirs(output_dir, exist_ok=True)

    print(f"Extracting test suite with prime_bound={prime_bound}, mod-{ell} representation...")
    suite = extract_test_suite(prime_bound=prime_bound, ell=ell)

    # Save individual curves
    for data in suite:
        fname = os.path.join(output_dir, f"curve_{data['label']}.json")
        with open(fname, 'w') as f:
            json.dump(data, f, indent=2)

    # Save summary
    summary = {
        'prime_bound': prime_bound,
        'mod_ell': ell,
        'curves': [
            {
                'label': d['label'],
                'rank': d['rank'],
                'conductor': d['conductor'],
                'sha_analytic': d['sha_analytic'],
                'description': d.get('description', ''),
            }
            for d in suite
        ]
    }
    with open(os.path.join(output_dir, 'suite_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nSaved {len(suite)} curves to {output_dir}")
    return suite


if __name__ == '__main__':
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    save_test_suite(data_dir, prime_bound=200, ell=3)
