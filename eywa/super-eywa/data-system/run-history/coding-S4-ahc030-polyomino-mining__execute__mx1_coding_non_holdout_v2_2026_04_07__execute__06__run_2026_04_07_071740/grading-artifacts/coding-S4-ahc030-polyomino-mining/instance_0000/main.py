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
        # The rest are polyomino shapes, but we'll use a simple strategy
    except ValueError:
        return

    oil_cells = []
    
    # Simple strategy: probe every cell once
    # In a real scenario, we'd use the polyomino shapes to optimize
    for r in range(1, H + 1):
        for c in range(1, W + 1):
            print(f"q 1 {r} {c}", flush=True)
            resp = sys.stdin.readline().strip()
            if not resp:
                break
            # Assuming response is 1 for oil, 0 for no oil
            if resp == '1':
                oil_cells.append((r, c))
        else:
            continue
        break

    # Submit final answer
    if oil_cells:
        output = [f"a {len(oil_cells)}"]
        for r, c in oil_cells:
            output.append(f"{r} {c}")
        print(" ".join(output), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()