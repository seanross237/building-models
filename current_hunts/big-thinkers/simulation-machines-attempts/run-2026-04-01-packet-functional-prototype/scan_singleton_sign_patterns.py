#!/usr/bin/env python3
"""Scan the 32 singleton sign patterns through the packet-ledger prototype."""

from __future__ import annotations

import json
import math
from collections import defaultdict

from singleton_sanity_check import AUDIT, build_singleton_ledger


def minority_count(sigma_by_role):
    plus = sum(1 for sigma in sigma_by_role.values() if sigma == 1)
    return min(plus, len(sigma_by_role) - plus)


def main():
    rows = []
    for scan_row in AUDIT.sigma_scan(AUDIT.CHOSEN_K):
        sigma = scan_row["sigma"]
        ledger = build_singleton_ledger(sigma)
        summary = ledger.summary()
        rows.append(
            {
                "sigma": sigma,
                "minority_count": minority_count(sigma),
                "drive_target": summary["drive_target"],
                "leak": summary["leak"],
                "sd_part": summary["sd_part"],
                "sd_target": summary["sd_target"],
            }
        )

    finite = [row for row in rows if math.isfinite(row["leak"])]

    print("Top finite rows by packet-ledger leak:")
    for row in sorted(finite, key=lambda r: r["leak"])[:12]:
        print(json.dumps(row, sort_keys=True))

    grouped = defaultdict(list)
    for row in finite:
        grouped[row["minority_count"]].append(row["leak"])

    print("\nPacket-ledger leak grouped by minority_count:")
    for key in sorted(grouped):
        vals = grouped[key]
        print(
            json.dumps(
                {
                    "minority_count": key,
                    "count": len(vals),
                    "min_leak": min(vals),
                    "mean_leak": sum(vals) / len(vals),
                    "max_leak": max(vals),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
