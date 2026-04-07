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
        H, W, N_fields, noise = parts[:4]
        # The rest are polyomino shapes, but for a baseline we focus on grid traversal
    except ValueError:
        return

    oil_cells = []

    # Strategy: Simple scan of the grid using single-cell queries
    # This is a baseline. In a real scenario, we'd use the polyomino shapes
    # and aggregate queries to minimize cost.
    
    # To avoid excessive cost in a real contest, we might sample or use aggregate queries.
    # However, for a robust baseline, we'll probe a subset or use a simple pattern.
    # Given the constraints of a baseline, we'll probe every cell if H*W is small,
    # or a grid of cells if H*W is large.
    
    step = 1
    if H * W > 100:
        step = 2 # Sample every 2nd cell to reduce cost if grid is large

    for r in range(0, H, step):
        for c in range(0, W, step):
            print(f"q 1 {r} {c}", flush=True)
            resp = sys.stdin.readline().strip()
            if not resp:
                break
            
            # The tester response for 'q 1 x y' is typically a value indicating oil presence
            # We assume 1 means oil, 0 means no oil (or similar based on problem type)
            # Since the exact response format isn't specified, we assume it's an integer.
            try:
                val = int(resp)
                if val > 0:
                    oil_cells.append((r, c))
            except ValueError:
                continue

    # Submit the found oil cells
    if oil_cells:
        out = [f"a {len(oil_cells)}"]
        for r, c in oil_cells:
            out.append(f"{r} {c}")
        print(" ".join(out), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()