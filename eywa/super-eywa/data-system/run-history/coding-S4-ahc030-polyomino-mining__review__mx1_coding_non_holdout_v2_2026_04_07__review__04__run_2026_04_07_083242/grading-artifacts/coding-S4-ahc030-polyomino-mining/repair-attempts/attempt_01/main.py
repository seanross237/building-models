import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if not parts:
        return
    
    # H, W, N_OIL, NOISE, and then the polyomino shapes
    H = parts[0]
    W = parts[1]
    N_OIL = parts[2]
    NOISE = parts[3]
    
    # The problem states polyomino shapes are provided. 
    # However, for a simple valid submission, we focus on the interaction protocol.
    # The current logic uses a grid-based probing strategy.
    
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
            
            # Multi-cell noisy aggregate query: q k x1 y1 ... xk yk
            query_parts = ["q", str(len(cells))]
            for cell_r, cell_c in cells:
                query_parts.append(str(cell_r))
                query_parts.append(str(cell_c))
            
            print(" ".join(query_parts))
            sys.stdout.flush()
            
            try:
                resp_line = sys.stdin.readline()
                if not resp_line:
                    break
                resp = resp_line.split()
                if not resp:
                    break
                val = int(resp[0])
                
                # If the aggregate query returns a value > 0, 
                # we drill individual cells to confirm.
                if val > 0:
                    for cell_r, cell_c in cells:
                        print(f"q 1 {cell_r} {cell_c}")
                        sys.stdout.flush()
                        single_resp_line = sys.stdin.readline()
                        if not single_resp_line:
                            break
                        single_resp = single_resp_line.split()
                        if single_resp and int(single_resp[0]) > 0:
                            oil_cells.append((cell_r, cell_c))
            except (EOFError, ValueError, IndexError):
                break

    # Final submission: a k x1 y1 ... xk yk
    if oil_cells:
        submit_parts = ["a", str(len(oil_cells))]
        for cell_r, cell_c in oil_cells:
            submit_parts.append(str(cell_r))
            submit_parts.append(str(cell_c))
        print(" ".join(submit_parts))
        sys.stdout.flush()
    else:
        # Even if no oil found, must submit something valid
        print("a 0")
        sys.stdout.flush()

if __name__ == "__main__":
    solve()
