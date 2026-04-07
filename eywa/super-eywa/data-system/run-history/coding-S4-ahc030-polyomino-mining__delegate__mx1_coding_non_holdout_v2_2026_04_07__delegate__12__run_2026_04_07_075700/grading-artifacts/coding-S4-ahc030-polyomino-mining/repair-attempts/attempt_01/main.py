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
        H, W, N, noise = parts
    except EOFError:
        return

    # Read polyomino shapes
    shapes = []
    for _ in range(N):
        line = sys.stdin.readline()
        if not line:
            break
        shape_parts = list(map(int, line.split()))
        # shape_parts[0] is number of cells, then x, y pairs
        k = shape_parts[0]
        cells = []
        for i in range(k):
            cells.append((shape_parts[1 + 2*i], shape_parts[2 + 2*i]))
        shapes.append(cells)

    # Strategy:
    # 1. Sample the grid using single-cell queries to find potential oil cells.
    # 2. Since we want to minimize cost, we use a sparse grid sampling.
    # 3. Once a cell is found, we try to fit the known shapes.
    
    discovered_oil = set()
    
    # Step 1: Sparse sampling
    # We sample every few cells to find a starting point.
    # The cost of 'q 1' is 1. The cost of 'q k' is k.
    # For simplicity and robustness in this interactive environment, 
    # we will perform a scan.
    
    step = 2
    for r in range(0, H, step):
        for c in range(0, W, step):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            res_line = sys.stdin.readline()
            if not res_line:
                break
            res = int(res_line.strip())
            
            if res > 0:
                # Potential oil cell found. 
                # In a real scenario, we'd probe neighbors or use aggregate queries.
                # For this implementation, we'll probe a small window around it.
                for dr in range(-2, 3):
                    for dc in range(-2, 3):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < H and 0 <= nc < W:
                            print(f"q 1 {nr} {nc}")
                            sys.stdout.flush()
                            res_inner = sys.stdin.readline()
                            if not res_inner:
                                break
                            if int(res_inner.strip()) > 0:
                                discovered_oil.add((nr, nc))
        if not discovered_oil and r > H // 2: # Optimization: if nothing found in half grid, maybe stop
            pass 

    # Step 2: Refine (Heuristic: if we found cells, they are likely part of a shape)
    # In a competitive setting, we would use the shapes to 'expand' the discovered cells.
    # For this template, we submit what we found.
    
    # Final Submission
    # The problem asks to report the oil cells.
    # Format: a k x1 y1 x2 y2 ...
    
    # If we found nothing, we must still submit something valid.
    if not discovered_oil:
        print("a 0")
    else:
        # Convert set to list of coordinates
        coords = []
        for r, c in discovered_oil:
            coords.append(r)
            coords.append(c)
        print(f"a {len(discovered_oil)} {' '.join(map(str, coords))}")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
