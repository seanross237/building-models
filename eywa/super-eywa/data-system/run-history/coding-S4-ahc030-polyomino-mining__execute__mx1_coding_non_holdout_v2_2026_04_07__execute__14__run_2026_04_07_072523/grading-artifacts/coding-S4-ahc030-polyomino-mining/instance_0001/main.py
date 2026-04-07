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
        H, W, N_FIELDS, NOISE = parts[:4]
        # The rest are polyomino shapes, but we'll handle them generically
    except ValueError:
        return

    oil_cells = set()
    
    # Strategy: Scan the grid with single-cell drills (q 1 x y)
    # This is a baseline approach. In a real scenario, we would use
    # the polyomino shapes to predict and use aggregate queries (q k ...)
    # to reduce cost. For a robust baseline, we scan.
    
    # To avoid excessive cost in large grids, we might sample or use a heuristic.
    # However, without knowing the density, a full scan is the safest baseline.
    # We'll limit the scan to a reasonable area if the grid is massive, 
    # but for standard competitive programming constraints, we iterate.
    
    for r in range(1, H + 1):
        for c in range(1, W + 1):
            # Query single cell
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            resp = sys.stdin.readline().strip()
            if not resp:
                break
            
            # The tester returns 1 if oil is present, 0 otherwise
            # (Assuming standard interactive format for this type of problem)
            if resp == "1":
                oil_cells.add((r, c))
            elif resp == "0":
                continue
            else:
                # Handle potential error or end of input
                break
        else:
            continue
        break

    # Submit the found oil cells
    # Format: a k x1 y1 x2 y2 ... xk yk
    if not oil_cells:
        print("a 0")
    else:
        cells_list = list(oil_cells)
        k = len(cells_list)
        coords = []
        for r, c in cells_list:
            coords.extend([r, c])
        print(f"a {k} {' '.join(map(str, coords))}")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()