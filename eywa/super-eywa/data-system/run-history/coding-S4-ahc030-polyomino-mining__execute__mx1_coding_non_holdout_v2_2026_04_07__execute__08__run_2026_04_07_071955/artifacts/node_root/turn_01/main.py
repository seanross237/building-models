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

    # Simple strategy: probe every cell once to find oil
    # In a real contest, we would use the polyomino shapes to optimize.
    # For a baseline, we probe all cells and collect those that are 1.
    
    oil_cells = []
    
    # To minimize cost, we could try to be smarter, but let's start simple.
    # We'll probe cells one by one. 
    # Note: In a real scenario, we'd use 'q k ...' to probe groups.
    
    for r in range(H):
        for c in range(W):
            print(f"q 1 {r} {c}", flush=True)
            resp = sys.stdin.readline().strip()
            if not resp:
                break
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