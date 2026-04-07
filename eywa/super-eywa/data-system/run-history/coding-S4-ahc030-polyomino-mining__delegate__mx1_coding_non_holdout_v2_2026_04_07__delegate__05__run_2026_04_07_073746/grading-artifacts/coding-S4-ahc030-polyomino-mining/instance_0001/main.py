import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    
    try:
        # Grid size H, W; Number of oil fields N; Noise parameter P; Number of shapes S
        parts = list(map(int, line.split()))
        if len(parts) < 5:
            return
        H, W, N, P, S = parts
        
        # Read S shapes
        shapes = []
        for _ in range(S):
            shape_line = sys.stdin.readline().split()
            if not shape_line:
                break
            k = int(shape_line[0])
            coords = []
            for i in range(k):
                coords.append((int(shape_line[1 + 2*i]), int(shape_line[2 + 2*i])))
            shapes.append(coords)
            
    except (EOFError, ValueError):
        return

    # Strategy: Simple sampling. 
    # We probe a sparse grid to find potential oil.
    # To avoid excessive cost, we use a step size.
    oil_cells = []
    
    # Heuristic step size to find at least some oil without querying everything
    # N is the number of oil fields.
    step = max(1, int((H * W / (N * 5 + 1))**0.5))
    
    for r in range(0, H, step):
        for c in range(0, W, step):
            # Single-cell drill query
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            res = sys.stdin.readline().strip()
            if not res:
                break
            
            try:
                # Response is an integer (0 or 1)
                val = int(res)
                if val == 1:
                    # If we find oil, we add this cell.
                    # In a more advanced version, we would use the shapes to 
                    # deduce the full polyomino.
                    oil_cells.append((r, c))
            except ValueError:
                continue

    # Final submission
    # The command format is 'a k x1 y1 x2 y2 ... xk yk'
    if not oil_cells:
        print("a 0")
    else:
        # Deduplicate
        unique_cells = sorted(list(set(oil_cells)))
        cmd = ["a", str(len(unique_cells))]
        for r, c in unique_cells:
            cmd.append(str(r))
            cmd.append(str(c))
        print(" ".join(cmd))
    
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
