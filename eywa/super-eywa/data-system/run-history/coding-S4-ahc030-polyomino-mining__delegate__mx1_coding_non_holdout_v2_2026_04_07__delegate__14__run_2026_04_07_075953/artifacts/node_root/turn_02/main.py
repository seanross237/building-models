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
        H, W, N_shapes, noise_param = parts[:4]
    except EOFError:
        return

    discovered_oil = []
    BLOCK_SIZE = 4
    
    for r in range(0, H, BLOCK_SIZE):
        for c in range(0, W, BLOCK_SIZE):
            r_end = min(r + BLOCK_SIZE, H)
            c_end = min(c + BLOCK_SIZE, W)
            
            cells = []
            for br in range(r, r_end):
                for bc in range(c, c_end):
                    cells.append((br, bc))
            
            query = ["q", str(len(cells))]
            for cell in cells:
                query.append(str(cell[0]))
                query.append(str(cell[1]))
            
            print(" ".join(query))
            sys.stdout.flush()
            
            try:
                resp = sys.stdin.readline().strip()
                if not resp:
                    break
                val = float(resp)
                
                if val > 0.1:
                    for cell in cells:
                        print(f"q 1 {cell[0]} {cell[1]}")
                        sys.stdout.flush()
                        
                        try:
                            cell_resp = sys.stdin.readline().strip()
                            if cell_resp and float(cell_resp) > 0.5:
                                discovered_oil.append(cell)
                        except:
                            break
            except:
                break

    # Final submission logic would go here

solve()