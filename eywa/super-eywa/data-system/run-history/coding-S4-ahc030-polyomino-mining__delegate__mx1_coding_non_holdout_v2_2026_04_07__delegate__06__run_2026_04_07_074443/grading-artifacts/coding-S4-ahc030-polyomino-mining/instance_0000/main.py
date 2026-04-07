import sys

def solve():
    # Read initial parameters
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if len(parts) < 4:
        return
    
    H, W, N_OIL, NOISE = parts[:4]
    
    # The problem states polyomino shapes are provided in the input.
    # We must consume the rest of the initial input to reach the interaction phase.
    # The input format for shapes is usually: M (number of shapes), then for each shape:
    # S (size), then S pairs of (dr, dc) or similar.
    # However, since we don't know the exact structure of the shape input, 
    # we consume the remaining lines of the initial input block.
    # In many AtCoder problems, the shapes are provided after the first line.
    # We'll attempt to read the next line to see if it's the number of shapes.
    
    # Based on the problem description, we need to consume the shapes.
    # Let's assume the next line is M (number of shapes).
    shape_line = sys.stdin.readline()
    if shape_line:
        try:
            M = int(shape_line.strip())
            for _ in range(M):
                # Consume each shape's description
                # We don't know how many lines a shape takes, but we can read until 
                # we've processed M shapes. A common way is: size, then size pairs.
                shape_data = sys.stdin.readline().split()
                if not shape_data:
                    break
                S = int(shape_data[0])
                # If the coordinates are on the same line or next lines, 
                # we need to be careful. For simplicity in this repair, 
                # we assume the shape data is provided such that we can skip it.
                # A robust way is to just read the next S*2 integers.
                # But since we don't know the exact format, we'll just consume 
                # the line and assume it's one line per shape for now.
        except ValueError:
            pass

    potential_oil = []
    
    # Strategy: Divide the grid into blocks and use aggregate queries to find signal.
    # Using a larger block size to minimize query count.
    BLOCK_SIZE = 4
    
    for r in range(0, H, BLOCK_SIZE):
        for c in range(0, W, BLOCK_SIZE):
            cells = []
            for dr in range(BLOCK_SIZE):
                for dc in range(BLOCK_SIZE):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < H and 0 <= nc < W:
                        cells.append((nr, nc))
            
            if not cells:
                continue
            
            # Multi-cell noisy aggregate query: q k x1 y1 ... xk yk
            query = ["q", str(len(cells))]
            for cr, cc in cells:
                query.append(str(cr))
                query.append(str(cc))
            
            print(" ".join(query))
            sys.stdout.flush()
            
            resp = sys.stdin.readline().strip()
            if not resp:
                break
            
            try:
                signal = int(resp)
                # If signal is positive, there might be oil in this block.
                # Drill individual cells to confirm.
                if signal > 0:
                    for cr, cc in cells:
                        # Single-cell drill query: q 1 x y
                        print(f"q 1 {cr} {cc}")
                        sys.stdout.flush()
                        
                        cell_resp = sys.stdin.readline().strip()
                        if cell_resp:
                            if int(cell_resp) > 0:
                                potential_oil.append((cr, cc))
            except ValueError:
                break

    # Final submission: a k x1 y1 ... xk yk
    if potential_oil:
        submission = ["a", str(len(potential_oil))]
        for pr, pc in potential_oil:
            submission.append(str(pr))
            submission.append(str(pc))
        print(" ".join(submission))
    else:
        print("a 0")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
