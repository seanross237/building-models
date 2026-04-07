#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_lines = Path(args.input).read_text(encoding="utf-8").split()
    output_lines = Path(args.output).read_text(encoding="utf-8").split()
    payload = validate_case(input_lines, output_lines)
    print(json.dumps(payload))
    return 0


def validate_case(input_tokens: list[str], output_tokens: list[str]) -> dict[str, object]:
    try:
        t = int(input_tokens[0])
    except Exception:
        return {"ok": False, "notes": "Malformed input bundle."}
    if t != 1:
        return {"ok": False, "notes": "V1 checker expects one test case per public bundle."}

    cursor = 1
    n = int(input_tokens[cursor])
    cursor += 1
    init_parent: dict[int, int | None] = {}
    children = defaultdict(set)
    active = set(range(1, n + 1))
    for _ in range(n - 1):
        child = int(input_tokens[cursor])
        parent = int(input_tokens[cursor + 1])
        cursor += 2
        init_parent[child] = parent
        children[parent].add(child)
        children.setdefault(child, set())
    for node in active:
        init_parent.setdefault(node, None)
    m = int(input_tokens[cursor])
    cursor += 1
    final_parent: dict[int, int | None] = {}
    final_children = defaultdict(set)
    final_active = set()
    for _ in range(m - 1):
        child = int(input_tokens[cursor])
        parent = int(input_tokens[cursor + 1])
        cursor += 2
        final_parent[child] = parent
        final_children[parent].add(child)
        final_children.setdefault(child, set())
        final_active.add(child)
        final_active.add(parent)
    for node in active:
        children.setdefault(node, set())
    for node in final_active:
        final_children.setdefault(node, set())
        final_parent.setdefault(node, None)

    if not output_tokens:
        return {"ok": False, "notes": "Missing operation count."}
    try:
        k = int(output_tokens[0])
    except ValueError:
        return {"ok": False, "notes": "First output token must be the operation count."}
    if len(output_tokens) != 1 + 2 * k:
        return {"ok": False, "notes": "Output token count does not match the declared operation count."}

    out_cursor = 1
    for step in range(k):
        try:
            a = int(output_tokens[out_cursor])
            b = int(output_tokens[out_cursor + 1])
        except ValueError:
            return {"ok": False, "notes": f"Merge step {step + 1} is not two integers."}
        out_cursor += 2
        if a == b:
            return {"ok": False, "notes": f"Merge step {step + 1} uses the same node twice."}
        if a not in active or b not in active:
            return {"ok": False, "notes": f"Merge step {step + 1} references a missing node."}
        pa = init_parent.get(a)
        pb = init_parent.get(b)
        if pa is None or pb is None or pa != pb:
            return {"ok": False, "notes": f"Merge step {step + 1} does not merge siblings."}

        keep = max(a, b)
        remove = min(a, b)
        parent = pa
        if parent is not None:
            children[parent].discard(a)
            children[parent].discard(b)
            children[parent].add(keep)
        init_parent[keep] = parent

        merged_children = set(children.get(keep, set())) | set(children.get(remove, set()))
        merged_children.discard(keep)
        merged_children.discard(remove)
        children[keep] = merged_children
        for child in merged_children:
            init_parent[child] = keep

        children.pop(remove, None)
        init_parent.pop(remove, None)
        active.discard(remove)

    normalized_current = normalize_tree(active, init_parent)
    normalized_target = normalize_tree(final_active, final_parent)
    if normalized_current != normalized_target:
        return {"ok": False, "notes": "Merge sequence does not produce the target tree."}
    return {"ok": True, "notes": "Accepted by public checker."}


def normalize_tree(nodes: set[int], parent_map: dict[int, int | None]) -> list[tuple[int, int | None]]:
    return sorted((node, parent_map.get(node)) for node in nodes)


if __name__ == "__main__":
    raise SystemExit(main())
