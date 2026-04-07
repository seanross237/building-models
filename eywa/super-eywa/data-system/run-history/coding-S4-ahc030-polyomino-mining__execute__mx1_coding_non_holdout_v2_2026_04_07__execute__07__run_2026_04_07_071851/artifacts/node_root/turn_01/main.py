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
        # The rest of the input contains polyomino shapes
        # For a baseline, we will probe cells to find oil
    except ValueError:
        return

    oil_cells = []
    
    # Simple strategy: probe every cell once to find oil
    # In a real contest, we'd use the polyomino shapes to optimize
    for r in range(1, H + 1):
        for c in range(1, W + 1):
            print(f"q 1 {r} {c}", flush=True)
            resp = sys.stdin.readline().strip()
            if not resp:
                break
            # Assuming response is '1' for oil, '0' for no oil
            if resp == '1':
                oil_cells.append((r, c))
        else:
            continue
        break

    # Submit final answer
    print(f"a {len(oil_cells)}", end="")
    for r, c in oil_cells:
        print(f" {r} {c}", end="")
    print("", flush=True)

if __name__ == "__main__":
    solve()