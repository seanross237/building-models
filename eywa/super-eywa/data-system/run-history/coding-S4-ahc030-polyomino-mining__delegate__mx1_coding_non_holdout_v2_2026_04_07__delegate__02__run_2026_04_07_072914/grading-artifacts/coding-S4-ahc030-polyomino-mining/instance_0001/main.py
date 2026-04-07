import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if len(parts) < 4:
        return
    H, W, N_shapes, noise = parts
    
    shapes = []
    for _ in range(N_shapes):
        shape_line = sys.stdin.readline().split()
        if not shape_line:
            break
        k = int(shape_line[0])
        coords = []
        for i in range(k):
            coords.append((int(shape_line[1 + 2*i]), int(shape_line[2 + 2*i])))
        shapes.append(coords)

    found_oil_cells = set()
    
    # Step 1: Coarse Probing
    # Divide the grid into blocks to find potential oil regions.
    # Using a larger block size to minimize cost.
    block_size = 8
    for r in range(0, H, block_size):
        for c in range(0, W, block_size):
            query_coords = []
            for dr in range(block_size):
                for dc in range(block_size):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < H and 0 <= nc < W:
                        query_coords.append((nr, nc))
            
            if not query_coords:
                continue
            
            # Construct aggregate query: q k x1 y1 ... xk yk
            cmd = ["q", str(len(query_coords))]
            for qr, qc in query_coords:
                cmd.append(str(qr))
                cmd.append(str(qc))
            
            print(" ".join(cmd))
            sys.stdout.flush()
            
            # Read response
            response = sys.stdin.readline().strip()
            if not response:
                return
            try:
                val = int(response)
            except ValueError:
                return

            # If val is significantly > 0, there's likely oil in this block.
            # The noise parameter is given. If val > noise, it's a signal.
            if val > noise:
                # Step 2: Refinement (Single-cell queries in this block)
                # To save cost, we only query cells if the aggregate value suggests oil.
                # We use single-cell queries to confirm.
                for qr, qc in query_coords:
                    print(f"q 1 {qr} {qc}")
                    sys.stdout.flush()
                    res_line = sys.stdin.readline().strip()
                    if not res_line:
                        break
                    try:
                        cell_val = int(res_line)
                        # In most AHC problems, 1 is oil, 0 is empty.
                        # Given noise, we check if cell_val is significantly positive.
                        if cell_val > 0:
                            found_oil_cells.add((qr, qc))
                    except ValueError:
                        break

    # Step 3: Submit the final set of oil cells
    # Format: a k x1 y1 ... xk yk
    if not found_oil_cells:
        print("a 0")
    else:
        cmd = ["a", str(len(found_oil_cells))]
        for (fr, fc) in found_oil_cells:
            cmd.append(str(fr))
            cmd.append(str(fc))
        print(" ".join(cmd))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
