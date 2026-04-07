import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if not parts:
        return
    
    # N: Grid size, K: Number of oil fields, P: Noise parameter, S: Number of shapes
    N, K, P, S = parts[0], parts[1], parts[2], parts[3]
    
    shapes = []
    for _ in range(S):
        shape_line = sys.stdin.readline().split()
        if not shape_line:
            break
        num_cells = int(shape_line[0])
        coords = []
        for i in range(num_cells):
            coords.append((int(shape_line[1 + 2*i]), int(shape_line[2 + 2*i])))
        shapes.append(coords)

    discovered_oil_cells = set()
    
    # Strategy:
    # Divide the grid into blocks to find potential oil areas using aggregate queries.
    # If a block returns > 0, refine with single-cell queries.
    # We use a larger block size to minimize the number of aggregate queries.
    
    block_size = 5
    for r in range(0, N, block_size):
        for c in range(0, N, block_size):
            block_cells = []
            for dr in range(block_size):
                for dc in range(block_size):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < N and 0 <= nc < N:
                        block_cells.append((nr, nc))
            
            if not block_cells:
                continue
            
            # Query the block
            # Format: q k x1 y1 ... xk yk
            query_parts = [f"q", str(len(block_cells))]
            for br, bc in block_cells:
                query_parts.append(str(br))
                query_parts.append(str(bc))
            
            print(" ".join(query_parts))
            sys.stdout.flush()
            
            # Read response
            resp_line = sys.stdin.readline().strip()
            if not resp_line:
                break
            try:
                resp = int(resp_line)
            except ValueError:
                break
            
            if resp > 0:
                # Refine block with single-cell queries
                # We assume 'q 1 x y' returns 1 if oil, 0 if not.
                for br, bc in block_cells:
                    print(f"q 1 {br} {bc}")
                    sys.stdout.flush()
                    cell_resp_line = sys.stdin.readline().strip()
                    if not cell_resp_line:
                        break
                    try:
                        cell_resp = int(cell_resp_line)
                        if cell_resp > 0:
                            discovered_oil_cells.add((br, bc))
                    except ValueError:
                        break

    # Final submission
    # Format: a k x1 y1 x2 y2 ... xk yk
    if discovered_oil_cells:
        ans_cells = list(discovered_oil_cells)
        ans_parts = [f"a", str(len(ans_cells))]
        for r, c in ans_cells:
            ans_parts.append(str(r))
            ans_parts.append(str(c))
        print(" ".join(ans_parts))
    else:
        print("a 0")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
