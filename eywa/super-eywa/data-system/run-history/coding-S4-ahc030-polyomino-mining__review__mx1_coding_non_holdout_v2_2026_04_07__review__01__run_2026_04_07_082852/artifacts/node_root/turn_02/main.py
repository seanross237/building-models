import sys

def solve():
    # Read initial input
    try:
        line = sys.stdin.readline()
        if not line:
            return
        parts = list(map(int, line.split()))
        if len(parts) < 4:
            return
        
        H, W, N_FIELDS, NOISE = parts[0:4]
        # The rest of the input contains polyomino shapes, but for a baseline 
        # we focus on the grid dimensions and the interaction.
    except EOFError:
        return

    oil_cells = []

    # Strategy: Scan the grid using single-cell queries 'q 1 x y'
    # This is a simple baseline. In a real competition, one would use 
    # aggregate queries 'q k ...' to find clusters more efficiently.
    
    for y in range(1, H + 1):
        for x in range(1, W + 1):
            # Query single cell
            print(f"q 1 {x} {y}", flush=True)
            
            # Read response
            resp_line = sys.stdin.readline()
            if not resp_line:
                break
            
            # Response format is typically a value indicating presence/noise
            # For this baseline, we assume a non-zero response means oil
            try:
                resp_val = float(resp_line.strip())
                if resp_val > 0.5:  # Thresholding based on noise
                    oil_cells.append((x, y))
            except ValueError:
                continue

    # Submit the final set of oil cells
    # Format: 'a k x1 y1 x2 y2 ... xk yk'
    if oil_cells:
        output = [f"a {len(oil_cells)}"]
        for ox, oy in oil_cells:
            output.append(f"{ox} {oy}")
        print(" ".join(output), flush=True)
    else:
        # Submit empty if nothing found
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()