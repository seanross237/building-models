import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    
    try:
        # Grid size H, W; Number of oil fields N; Noise parameter P; Number of shapes S
        # Format: H W N P S
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
            
    except EOFError:
        return

    # Strategy: Simple sampling. 
    # Since we don't know the exact placement, we probe a grid of points.
    # In a real competition, we would use the shapes to infer locations.
    # For a robust baseline, we probe single cells to find oil.
    
    oil_cells = []
    
    # To minimize cost, we don't probe everything.
    # We probe a sparse grid to find potential oil areas.
    step = max(1, int((H * W / (N * 10 + 1))**0.5))
    
    for r in range(0, H, step):
        for c in range(0, W, step):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            res = sys.stdin.readline().strip()
            if not res:
                break
            
            # Response is 1 if oil is present (with noise), 0 otherwise
            # Note: The problem says "noisy aggregate query", but q 1 is single cell.
            # We assume response is an integer.
            try:
                val = int(res)
                if val == 1:
                    # If we find oil, we might want to probe neighbors, 
                    # but for a simple baseline, we just record this cell.
                    oil_cells.append((r, c))
            except ValueError:
                continue

    # Final submission
    # The problem asks to recover the true oil configuration.
    # Since we only probed a sparse grid, we submit what we found.
    # In a real scenario, we'd use the shapes to expand these points.
    
    # For the sake of a valid submission that doesn't crash:
    # We'll try to find the actual shapes if we found a hit.
    # But without more complex logic, we just submit the hits.
    
    if not oil_cells:
        # If nothing found, submit empty or a single guess if N > 0
        print("a 0")
    else:
        # Deduplicate and format
        unique_cells = sorted(list(set(oil_cells)))
        output = [f"a {len(unique_cells)}"]
        for r, c in unique_cells:
            output.append(f"{r} {c}")
        
        # The command format is 'a k x1 y1 x2 y2 ...'
        # Let's re-format to match 'a k x1 y1 ... xk yk'
        cmd = ["a", str(len(unique_cells))]
        for r, c in unique_cells:
            cmd.append(str(r))
            cmd.append(str(c))
        print(" ".join(cmd))
    
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
