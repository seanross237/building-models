import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if not parts:
        return
    
    # H: Height, W: Width, N_shapes: Number of shapes, noise_param: Noise
    H, W, N_shapes, noise_param = parts[:4]

    discovered_oil = []
    
    # Strategy: Use a coarse grid to find potential oil areas, 
    # then refine with single-cell queries.
    # We use a block size that balances query cost and granularity.
    BLOCK_SIZE = 3
    
    for r in range(0, H, BLOCK_SIZE):
        for c in range(0, W, BLOCK_SIZE):
            r_end = min(r + BLOCK_SIZE, H)
            c_end = min(c + BLOCK_SIZE, W)
            
            cells = []
            for br in range(r, r_end):
                for bc in range(c, c_end):
                    cells.append((br, bc))
            
            # Multi-cell noisy aggregate query
            # Format: q k x1 y1 ... xk yk
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
                
                # If the aggregate value is significant, probe individual cells
                # Threshold is set to account for noise
                if val > 0.1:
                    for cell in cells:
                        # Single-cell drill query
                        # Format: q 1 x y
                        print(f"q 1 {cell[0]} {cell[1]}")
                        sys.stdout.flush()
                        
                        try:
                            cell_resp = sys.stdin.readline().strip()
                            if not cell_resp:
                                break
                            if float(cell_resp) > 0.5:
                                discovered_oil.append(cell)
                        except EOFError:
                            break
                        except ValueError:
                            break
            except (EOFError, ValueError):
                break

    # Final submission
    # Format: a k x1 y1 ... xk yk
    if discovered_oil:
        submission = ["a", str(len(discovered_oil))]
        for cell in discovered_oil:
            submission.append(str(cell[0]))
            submission.append(str(cell[1]))
        print(" ".join(submission))
    else:
        # Submit empty if nothing found
        print("a 0")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
