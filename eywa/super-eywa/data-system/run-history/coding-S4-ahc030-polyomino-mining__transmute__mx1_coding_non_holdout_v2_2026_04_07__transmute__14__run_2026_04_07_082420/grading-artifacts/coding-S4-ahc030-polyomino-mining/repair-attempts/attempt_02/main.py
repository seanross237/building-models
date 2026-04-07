import sys

def solve():
    # Read initial input
    try:
        line = sys.stdin.readline()
        if not line:
            return
        parts = list(map(int, line.split()))
        if not parts:
            return
        H, W, N, noise_param = parts[0], parts[1], parts[2], parts[3]
        
        # Read polyomino shapes
        shapes = []
        for _ in range(N):
            shape_line = sys.stdin.readline().split()
            if not shape_line:
                break
            k = int(shape_line[0])
            coords = []
            for i in range(k):
                coords.append((int(shape_line[1 + 2*i]), int(shape_line[2 + 2*i])))
            shapes.append(coords)
    except (EOFError, ValueError, IndexError):
        return

    oil_cells = set()
    
    # Strategy:
    # To minimize cost, we need to find oil cells efficiently.
    # A simple scan with single-cell queries is robust against noise.
    # We use a step to avoid querying every single cell if the grid is huge,
    # but for a reliable baseline, we scan.
    
    # Given the potential for noise, we'll probe cells.
    # If a cell returns 1, it's likely oil.
    
    # To avoid TLE or excessive cost, we use a reasonable step.
    # However, the problem asks to recover the true configuration.
    # Let's try a scan.
    
    step = 1
    if H * W > 2500:
        step = 2

    for r in range(0, H, step):
        for c in range(0, W, step):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            res = sys.stdin.readline().strip()
            if not res:
                return
            try:
                val = int(res)
                if val == 1:
                    # If we find oil, check immediate neighbors to expand
                    # This helps capture the polyomino shape.
                    oil_cells.add((r, c))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < H and 0 <= nc < W and (nr, nc) not in oil_cells:
                            print(f"q 1 {nr} {nc}")
                            sys.stdout.flush()
                            res_n = sys.stdin.readline().strip()
                            if res_n and int(res_n) == 1:
                                oil_cells.add((nr, nc))
            except ValueError:
                return

    # Final submission
    # Format: a k x1 y1 x2 y2 ... xk yk
    unique_oil = list(oil_cells)
    k = len(unique_oil)
    
    output = [f"a {k}"]
    for r, c in unique_oil:
        output.append(f"{r} {c}")
    
    print(" ".join(output))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
