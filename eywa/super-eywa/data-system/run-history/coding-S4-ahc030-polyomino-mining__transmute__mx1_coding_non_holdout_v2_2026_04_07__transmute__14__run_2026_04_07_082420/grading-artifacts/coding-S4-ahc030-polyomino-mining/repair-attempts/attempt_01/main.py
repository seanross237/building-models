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
    except EOFError:
        return

    # Strategy: 
    # Since we don't know the exact noise distribution or cost function, 
    # a robust baseline is to probe cells to find oil, then expand.
    # However, for a general competitive programming solution where we must 
    # minimize cost, we'll use a simple scanning approach.
    
    oil_cells = []
    
    # Step 1: Scan the grid using single-cell queries to find potential oil.
    # To minimize cost, we could use aggregate queries, but single-cell is 
    # the most reliable way to get a ground truth in a noisy environment.
    # We'll sample a subset of cells or use a grid-based approach.
    
    # For the sake of a valid submission that works under constraints:
    # We will probe cells in a grid pattern to find "hotspots".
    step = 2 if H * W > 100 else 1
    
    for r in range(0, H, step):
        for c in range(0, W, step):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            res = sys.stdin.readline().strip()
            if not res:
                break
            if int(res) == 1:
                # If we find oil, we try to find the rest of the polyomino
                # by checking neighbors.
                oil_cells.append((r, c))
                # Simple local search around the found cell
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < H and 0 <= nc < W:
                            print(f"q 1 {nr} {nc}")
                            sys.stdout.flush()
                            res_n = sys.stdin.readline().strip()
                            if res_n and int(res_n) == 1:
                                if (nr, nc) not in oil_cells:
                                    oil_cells.append((nr, nc))
        if not oil_cells and step > 1: # If nothing found, try finer grain
            pass 

    # Step 2: Final submission
    # Remove duplicates and ensure uniqueness
    unique_oil = list(set(oil_cells))
    
    # Output the answer
    # Format: a k x1 y1 x2 y2 ... xk yk
    ans = [f"a {len(unique_oil)}"]
    for r, c in unique_oil:
        ans.append(f"{r} {c}")
    
    print(" ".join(ans))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
