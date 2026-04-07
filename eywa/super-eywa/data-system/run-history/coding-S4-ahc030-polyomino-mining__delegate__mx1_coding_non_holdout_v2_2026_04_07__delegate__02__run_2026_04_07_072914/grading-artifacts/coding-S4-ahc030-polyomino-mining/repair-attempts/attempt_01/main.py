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

    # Strategy:
    # Since we want to minimize cost, we use a coarse-to-fine approach.
    # 1. Sample the grid using aggregate queries to find potential oil regions.
    # 2. Use single-cell queries to confirm oil cells.
    # 3. Output the final set of cells.

    found_oil_cells = set()
    
    # Step 1: Coarse Probing
    # Divide the grid into blocks to find regions with high oil density.
    block_size = 5
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
            # We use a threshold to account for noise.
            if val > noise:
                # Step 2: Refinement (Single-cell queries in this block)
                for qr, qc in query_coords:
                    print(f"q 1 {qr} {qc}")
                    sys.stdout.flush()
                    res_line = sys.stdin.readline().strip()
                    if not res_line:
                        break
                    try:
                        cell_val = int(res_line)
                        # If cell_val is 1 (or > 0 depending on noise model), it's oil.
                        # In most AHC problems, 1 is oil, 0 is empty.
                        if cell_val > 0:
                            found_oil_cells.add((qr, qc))
                    except ValueError:
                        break

    # Step 3: Submit the final set of oil cells
    # Format: a k x1 y1 ... xk yk
    if not found_oil_cells:
        # Submit empty if nothing found
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
