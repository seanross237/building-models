import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if not parts:
        return
    H, W, N, noise = parts

    # Read polyomino shapes
    shapes = []
    for _ in range(N):
        line = sys.stdin.readline()
        if not line:
            break
        shape_parts = list(map(int, line.split()))
        size = shape_parts[0]
        coords = []
        for i in range(size):
            coords.append((shape_parts[1 + 2*i], shape_parts[2 + 2*i]))
        shapes.append(coords)

    found_oil_cells = set()
    
    # Step 1: Probing
    # Use a step to balance cost and coverage.
    # A step of 2 or 3 is usually a safe heuristic for sparse oil.
    step = 2
    for r in range(0, H, step):
        for c in range(0, W, step):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            res = sys.stdin.readline()
            if not res:
                break
            try:
                val = int(res.strip())
                if val > 0:
                    found_oil_cells.add((r, c))
            except ValueError:
                break

    # Step 2: Expansion
    # If we find a cell, check its immediate neighbors to refine the set.
    final_oil_cells = set()
    for (r, c) in list(found_oil_cells):
        # Check the cell itself first (it might be noise, but we'll assume it's oil for now)
        # To be more robust, we check neighbors.
        is_oil = False
        # Check current cell and neighbors
        neighbors = [(r, c), (r+1, c), (r-1, c), (r, c+1), (r, c-1)]
        hits = 0
        for nr, nc in neighbors:
            if 0 <= nr < H and 0 <= nc < W:
                print(f"q 1 {nr} {nc}")
                sys.stdout.flush()
                res = sys.stdin.readline()
                if res:
                    try:
                        if int(res.strip()) > 0:
                            hits += 1
                            final_oil_cells.add((nr, nc))
                    except ValueError:
                        pass
        
        # If we found hits, the original (r,c) is likely part of an oil field
        if hits > 0:
            final_oil_cells.add((r, c))

    # Step 3: Final Submission
    # The problem asks for 'a k x1 y1 ... xk yk'
    unique_cells = sorted(list(final_oil_cells))
    if not unique_cells:
        print("a 0")
    else:
        # Format: a k x1 y1 x2 y2 ... xk yk
        # Note: The prompt says "a k x1 y1 ... xk yk", which implies 
        # k is the number of cells, followed by k pairs of coordinates.
        output_parts = [f"a {len(unique_cells)}"]
        for r, c in unique_cells:
            output_parts.append(f"{r} {c}")
        print(" ".join(output_parts))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
