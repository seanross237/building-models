import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    try:
        parts = list(map(int, line.split()))
        if len(parts) < 4:
            return
        H, W, N, noise = parts[:4]
        # The rest are polyomino shapes, but we'll use a simple scan
    except ValueError:
        return

    oil_cells = []

    # Simple strategy: probe every cell once
    # In a real scenario, we would use the polyomino shapes to optimize
    for r in range(H):
        for c in range(W):
            print(f"q 1 {r} {c}", flush=True)
            resp = sys.stdin.readline().strip()
            if resp == "1":
                oil_cells.append((r, c))
            elif resp == "0":
                pass
            else:
                # Handle potential error or unexpected response
                pass

    # Submit the found oil cells
    print(f"a {len(oil_cells)}", end="")
    for r, c in oil_cells:
        print(f" {r} {c}", end="")
    print()
    sys.stdout.flush()

if __name__ == "__main__":
    solve()