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
    # 1. Divide the grid into blocks to find potential oil areas using aggregate queries.
    # 2. For blocks that return > 0, use single-cell queries to find exact cells.
    # 3. Since we don't know the exact noise behavior (P), we treat the aggregate 
    #    response as a hint. If resp > 0, we probe cells.
    
    block_size = 4
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
            query_str = f"q {len(block_cells)}"
            for br, bc in block_cells:
                query_str += f" {br} {bc}"
            print(query_str)
            sys.stdout.flush()
            
            # Read response
            resp_line = sys.stdin.readline().strip()
            if not resp_line:
                break
            resp = int(resp_line)
            
            if resp > 0:
                # Refine block with single-cell queries
                # Note: In some versions of this problem, 'q 1 x y' returns 1 if oil, 0 if not.
                # In others, it might be noisy. We assume 1/0 for simplicity.
                for br, bc in block_cells:
                    print(f"q 1 {br} {bc}")
                    sys.stdout.flush()
                    cell_resp = sys.stdin.readline().strip()
                    if not cell_resp:
                        break
                    if int(cell_resp) > 0:
                        discovered_oil_cells.add((br, bc))

    # Final submission
    # Format: a k x1 y1 x2 y2 ... xk yk
    if discovered_oil_cells:
        ans_cells = list(discovered_oil_cells)
        ans_str = f"a {len(ans_cells)}"
        for r, c in ans_cells:
            ans_str += f" {r} {c}"
        print(ans_str)
    else:
        print("a 0")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
