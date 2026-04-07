import sys

def solve():
    # Read initial input
    # Format: H W N noise (H, W: grid size, N: number of polyominoes, noise: noise parameter)
    # Followed by N polyomino shapes
    line = sys.stdin.readline()
    if not line:
        return
    try:
        parts = list(map(int, line.split()))
        if len(parts) < 4:
            return
        H, W, N, noise = parts
    except ValueError:
        return

    shapes = []
    for _ in range(N):
        shape_line = sys.stdin.readline()
        if not shape_line:
            break
        # Assuming shape is given as a list of (dx, dy) relative to a root
        # Or a list of cells. Let's assume it's a list of integers representing cells.
        # Since the exact format of shapes isn't specified in the prompt, 
        # we assume a standard format: k dx1 dy1 dx2 dy2 ... dxk dyk
        shape_data = list(map(int, shape_line.split()))
        k = shape_data[0]
        cells = []
        for i in range(k):
            cells.append((shape_data[1 + 2*i], shape_data[2 + 2*i]))
        shapes.append(cells)

    # Strategy:
    # 1. Sample the grid using aggregate queries to find regions with high signal.
    # 2. Use single-cell queries to refine the exact locations.
    # 3. Since we want to minimize cost, we use 'q k' (aggregate) heavily.
    
    # For this implementation, we'll perform a coarse-grained scan.
    # We'll query blocks of cells to find where oil might be.
    
    detected_oil = set()
    
    # Step 1: Coarse scan using aggregate queries
    # We divide the grid into blocks to find signals.
    block_size = 4
    for r in range(0, H, block_size):
        for c in range(0, W, block_size):
            query_cells = []
            for dr in range(block_size):
                for dc in range(block_size):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < H and 0 <= nc < W:
                        query_cells.append((nr, nc))
            
            if not query_cells:
                continue
            
            # Command: q k x1 y1 ... xk yk
            cmd = ["q", str(len(query_cells))]
            for qr, qc in query_cells:
                cmd.append(str(qr))
                cmd.append(str(qc))
            print(" ".join(cmd))
            sys.stdout.flush()
            
            # Read response: signal value
            res_line = sys.stdin.readline()
            if not res_line:
                break
            signal = float(res_line.strip())
            
            # If signal is significant, drill individual cells in this block
            if signal > noise * 0.5: # Heuristic threshold
                for qr, qc in query_cells:
                    print(f"q 1 {qr} {qc}")
                    sys.stdout.flush()
                    cell_res = sys.stdin.readline()
                    if not cell_res:
                        break
                    if float(cell_res.strip()) > 0.5:
                        detected_oil.add((qr, qc))

    # Step 2: Final submission
    # Command: a k x1 y1 ... xk yk
    if not detected_oil:
        # Submit nothing if nothing found
        print("a 0")
    else:
        oil_list = list(detected_oil)
        cmd = ["a", str(len(oil_list))]
        for r, c in oil_list:
            cmd.append(str(r))
            cmd.append(str(c))
        print(" ".join(cmd))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
