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
        # The rest are polyomino shapes, but we'll use a simple strategy
    except ValueError:
        return

    oil_cells = []

    # Strategy: Probe every cell once to find oil.
    # In a real competition, we would use the polyomino shapes to optimize.
    # For a baseline, we probe single cells.
    
    # To keep cost low in a real scenario, we'd use aggregate queries.
    # Here we do a simple scan.
    
    for r in range(1, H + 1):
        for c in range(1, W + 1):
            print(f"q 1 {r} {c}", flush=True)
            resp = sys.stdin.readline().strip()
            if not resp:
                break
            
            # The tester returns 1 if oil is present, 0 otherwise (or similar)
            # Based on typical interactive problems
            if resp == "1":
                oil_cells.append((r, c))
        else:
            continue
        break

    # Submit the found oil cells
    if oil_cells:
        output = [f"a {len(oil_cells)}"]
        for r, c in oil_cells:
            output.append(f"{r} {c}")
        print(" ".join(output), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()