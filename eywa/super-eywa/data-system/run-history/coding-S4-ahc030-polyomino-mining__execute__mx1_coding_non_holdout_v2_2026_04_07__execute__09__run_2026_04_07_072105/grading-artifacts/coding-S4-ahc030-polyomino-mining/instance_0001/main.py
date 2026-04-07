import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    
    try:
        parts = list(map(int, line.split()))
        if len(parts) < 3:
            return
        H, W, N_shapes = parts[0], parts[1], parts[2]
    except ValueError:
        return

    oil_cells = []

    # Simple baseline: query every cell individually
    # Note: In a real contest, we would use the polyomino shapes
    # and aggregate queries to minimize cost.
    for r in range(H):
        for c in range(W):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            resp = sys.stdin.readline().strip()
            if resp == "1":
                oil_cells.append((r, c))
            elif resp == "0":
                pass
            else:
                # Handle potential error or end of input
                break

    # Submit final answer
    if oil_cells:
        output = [f"a {len(oil_cells)}"]
        for r, c in oil_cells:
            output.append(f"{r} {c}")
        print(" ".join(output))
    else:
        print("a 0")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()