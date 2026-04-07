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
        H, W, N_OIL, NOISE = parts[:4]
    except EOFError:
        return

    oil_cells = []
    block_size = 4
    
    for r in range(0, H, block_size):
        for c in range(0, W, block_size):
            r_end = min(r + block_size, H)
            c_end = min(c + block_size, W)
            
            cells = []
            for i in range(r, r_end):
                for j in range(c, c_end):
                    cells.append((i, j))
            
            if not cells:
                continue
            
            query_parts = ["q", str(len(cells))]
            for cell_r, cell_c in cells:
                query_parts.append(str(cell_r))
                query_parts.append(str(cell_c))
            
            print(" ".join(query_parts))
            sys.stdout.flush()
            
            try:
                resp = sys.stdin.readline().split()
                if not resp:
                    break
                val = int(resp[0])
                if val > 0:
                    for cell_r, cell_c in cells:
                        print(f"q 1 {cell_r} {cell_c}")
                        sys.stdout.flush()
                        single_resp = sys.stdin.readline().split()
                        if single_resp and int(single_resp[0]) > 0:
                            oil_cells.append((cell_r, cell_c))
            except EOFError:
                break

    # Output found oil cells
    print(f"found {len(oil_cells)} cells")

solve()