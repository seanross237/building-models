import sys

def solve():
    # Read initial input
    # Format: H W N noise_param
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if not parts:
        return
    H, W, N, noise_param = parts
    
    polyominoes = []
    for _ in range(N):
        shape_line = sys.stdin.readline()
        if not shape_line:
            break
        shape_data = list(map(int, shape_line.split()))
        if not shape_data:
            continue
        k = shape_data[0]
        coords = []
        for i in range(k):
            coords.append((shape_data[1 + 2*i], shape_data[2 + 2*i]))
        polyominoes.append(coords)

    discovered_oil = set()
    
    # Strategy: 
    # Use aggregate queries to find regions with oil.
    # Then refine with single-cell queries.
    # To avoid excessive costs, we use a larger block size for initial scan.
    
    block_size = 5
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
            
            # Format: q k x1 y1 x2 y2 ...
            cmd = ["q", str(len(query_cells))]
            for cell in query_cells:
                cmd.append(str(cell[0]))
                cmd.append(str(cell[1]))
            print(" ".join(cmd))
            sys.stdout.flush()
            
            # Read response: number of oil cells in the query
            resp = sys.stdin.readline()
            if not resp:
                return
            try:
                count = int(resp.strip())
            except ValueError:
                return
            
            # If count > 0, probe the block more finely
            if count > 0:
                for cell in query_cells:
                    print(f"q 1 {cell[0]} {cell[1]}")
                    sys.stdout.flush()
                    res = sys.stdin.readline()
                    if not res:
                        return
                    try:
                        if int(res.strip()) > 0:
                            discovered_oil.add(cell)
                    except ValueError:
                        continue

    # Final Submission
    # Format: a k x1 y1 x2 y2 ...
    if not discovered_oil:
        print("a 0")
    else:
        cmd = ["a", str(len(discovered_oil))]
        for cell in discovered_oil:
            cmd.append(str(cell[0]))
            cmd.append(str(cell[1]))
        print(" ".join(cmd))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
