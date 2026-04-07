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
        # shape_parts[0] is size, followed by x, y offsets
        size = shape_parts[0]
        coords = []
        for i in range(size):
            coords.append((shape_parts[1 + 2*i], shape_parts[2 + 2*i]))
        shapes.append(coords)

    # Strategy: 
    # 1. Sample the grid using single-cell queries to find potential oil cells.
    # 2. Since we want to minimize cost, we use a sparse sampling.
    # 3. Once an oil cell is found, we try to fit the known shapes.
    
    # For a simple robust solution in a competitive programming context:
    # We will probe cells in a grid pattern to find oil.
    # Then we will use the information to deduce the full shapes.
    
    found_oil_cells = set()
    
    # Step 1: Probing
    # We use a step to balance cost and coverage.
    step = 2
    for r in range(0, H, step):
        for c in range(0, W, step):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            res = sys.stdin.readline()
            if not res:
                break
            val = int(res.strip())
            if val > 0:
                # If we find a hit, we assume it's oil (ignoring noise for simplicity in this heuristic)
                # In a real scenario, we'd check noise probability.
                found_oil_cells.add((r, c))

    # Step 2: Expansion
    # If we found cells, try to see if they belong to any shape.
    # This is a simplified heuristic: if we find a cell, we check its neighbors.
    final_oil_cells = set()
    
    # To be safe and avoid over-querying, we'll just report what we found 
    # or try to expand locally if we have budget.
    # Given the constraints of a single-pass script, we'll refine the found cells.
    
    # For each found cell, try to see if it's part of a shape.
    # Since we don't know which shape or orientation, we'd ideally check all.
    # But to keep it simple and valid:
    for (r, c) in list(found_oil_cells):
        # Check immediate neighbors to see if they are also oil
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                print(f"q 1 {nr} {nc}")
                sys.stdout.flush()
                res = sys.stdin.readline()
                if res:
                    if int(res.strip()) > 0:
                        final_oil_cells.add((r, c))
                        final_oil_cells.add((nr, nc))
                    else:
                        final_oil_cells.add((r, c))
                else:
                    final_oil_cells.add((r, c))
            else:
                final_oil_cells.add((r, c))

    # If no cells found, final_oil_cells is empty.
    # If we found some, we output them.
    
    # Step 3: Final Submission
    # The problem asks for 'a k x1 y1 ... xk yk'
    # We need to ensure we don't output duplicates.
    unique_cells = list(final_oil_cells)
    if not unique_cells:
        # If nothing found, submit empty set to satisfy protocol
        print("a 0")
    else:
        out = [f"a {len(unique_cells)}"]
        for r, c in unique_cells:
            out.append(f"{r} {c}")
        print(" ".join(out))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
