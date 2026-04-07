import sys

def solve():
    line = sys.stdin.readline()
    if not line:
        return
    try:
        parts = list(map(int, line.split()))
        if len(parts) < 4: return
        N, M, K, sigma = parts
    except ValueError:
        return

    shapes = []
    for _ in range(K):
        shape_line = sys.stdin.readline().split()
        if not shape_line: break
        num_cells = int(shape_line[0])
        coords = []
        for i in range(num_cells):
            coords.append((int(shape_line[1+2*i]), int(shape_line[2+2*i])))
        shapes.append(coords)

    # Simple strategy: probe every cell once to build a map
    # In a real scenario, we'd use Bayesian updates and pattern matching
    grid_probs = [[0.0 for _ in range(M)] for _ in range(N)]
    
    # Phase 2: Probing
    # For simplicity in this template, we probe single cells
    # A more complex version would use q k queries
    for r in range(N):
        for c in range(M):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            res_line = sys.stdin.readline()
            if not res_line: break
            try:
                val = float(res_line.strip())
                grid_probs[r][c] = val
            except ValueError:
                grid_probs[r][c] = 0.0

    # Phase 3: Final Submission
    # Identify cells with high probability
    # Thresholding based on sigma or simple heuristic
    oil_cells = []
    threshold = 0.5
    for r in range(N):
        for c in range(M):
            if grid_probs[r][c] > threshold:
                oil_cells.append((r, c))

    if not oil_cells:
        # Fallback: if no cells found, try to find best fit for shapes
        # For this template, we just output nothing or a minimal set
        print("a 0")
    else:
        out = [f"a {len(oil_cells)}"]
        for r, c in oil_cells:
            out.append(f"{r} {c}")
        print(" ".join(out))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()