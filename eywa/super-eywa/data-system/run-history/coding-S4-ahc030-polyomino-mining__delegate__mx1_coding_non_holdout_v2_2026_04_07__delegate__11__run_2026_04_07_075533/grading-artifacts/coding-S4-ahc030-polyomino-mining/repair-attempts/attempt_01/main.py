import sys

def solve():
    # Read initial input
    # Format: H W N noise_param
    # N: number of polyominoes
    # Followed by N polyomino shapes
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
        # Assuming shape is given as a list of (dx, dy) relative to a root
        # The exact format of polyomino input isn't specified, 
        # but we must read it to advance the pointer.
        # For this template, we assume it's a list of integers representing coordinates.
        shape_data = list(map(int, shape_line.split()))
        # Example: k dx1 dy1 dx2 dy2 ...
        k = shape_data[0]
        coords = []
        for i in range(k):
            coords.append((shape_data[1 + 2*i], shape_data[2 + 2*i]))
        polyominoes.append(coords)

    # Strategy: 
    # Since we want to minimize cost, we use a grid-based sampling.
    # We'll use aggregate queries (q k ...) to find regions with oil.
    # Then we'll refine with single-cell queries (q 1 x y).
    
    discovered_oil = set()
    
    # Step 1: Coarse sampling using aggregate queries
    # We divide the grid into blocks to find potential oil locations.
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
                break
            count = int(resp.strip())
            
            # If count > 0, we probe the block more finely
            if count > 0:
                for cell in query_cells:
                    print(f"q 1 {cell[0]} {cell[1]}")
                    sys.stdout.flush()
                    res = sys.stdin.readline()
                    if not res:
                        break
                    if int(res.strip()) > 0:
                        discovered_oil.add(cell)

    # Step 2: Final Submission
    # Format: a k x1 y1 x2 y2 ...
    # We output the cells we believe are oil.
    # Note: In a real competition, we would use the polyomino shapes 
    # to infer the full shape from the single cells found.
    
    # For the sake of a valid submission structure, we output what we found.
    # In a real scenario, we'd perform pattern matching here.
    
    # To prevent empty submission if no oil found (though N >= 1)
    if not discovered_oil:
        # Try to find at least one cell if possible, or just submit empty
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
