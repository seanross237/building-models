import sys

def solve():
    try:
        line = sys.stdin.readline()
        if not line:
            return
        parts = list(map(int, line.split()))
        if len(parts) < 4:
            return
        H, W, N_OIL, NOISE = parts[:4]
    except EOFError:
        return

    potential_oil = []
    BLOCK_SIZE = 4
    
    for r in range(0, H, BLOCK_SIZE):
        for c in range(0, W, BLOCK_SIZE):
            cells = []
            for dr in range(BLOCK_SIZE):
                for dc in range(BLOCK_SIZE):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < H and 0 <= nc < W:
                        cells.append((nr, nc))
            
            if not cells:
                continue
            
            query = ["q", str(len(cells))]
            for cr, cc in cells:
                query.append(str(cr))
                query.append(str(cc))
            
            print(" ".join(query))
            sys.stdout.flush()
            
            try:
                resp = sys.stdin.readline().strip()
                if not resp:
                    break
                signal = int(resp)
                
                if signal > 0:
                    for cr, cc in cells:
                        print(f"q 1 {cr} {cc}")
                        sys.stdout.flush()
                        
                        try:
                            cell_resp = sys.stdin.readline().strip()
                            if cell_resp and int(cell_resp) > 0:
                                potential_oil.append((cr, cc))
                        except:
                            break
            except:
                break

    if potential_oil:
        submission = ["a", str(len(potential_oil))]
        for pr, pc in potential_oil:
            submission.append(str(pr))
            submission.append(str(pc))
        print(" ".join(submission))
        sys.stdout.flush()

solve()