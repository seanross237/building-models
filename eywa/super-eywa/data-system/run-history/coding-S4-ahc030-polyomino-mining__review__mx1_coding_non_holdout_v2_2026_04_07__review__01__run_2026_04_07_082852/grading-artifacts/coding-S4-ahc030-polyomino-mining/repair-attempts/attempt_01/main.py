import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if len(parts) < 4:
        return
    
    H, W, N_FIELDS, NOISE = parts[0:4]
    
    # The rest of the input contains polyomino shapes.
    # We need to consume the rest of the initial input to ensure we are ready for interaction.
    # However, the number of shapes isn't explicitly given in the first line, 
    # but the problem says "The rest of the input contains polyomino shapes".
    # In many AtCoder interactive problems, the shapes follow immediately.
    # Since we don't know how many, we'll assume the interaction starts after the first line 
    # or we read until we can't. But for a baseline, we just need to handle the first line.
    
    oil_cells = []

    # Strategy: Scan the grid using single-cell queries 'q 1 x y'
    # We use a simple scan. To avoid TLE or excessive cost in a real scenario, 
    # one would use aggregate queries, but for a valid baseline, we follow the protocol.
    
    # Note: In some environments, the shapes might be on subsequent lines.
    # We'll skip reading them for now and focus on the interaction loop.
    
    for y in range(1, H + 1):
        for x in range(1, W + 1):
            # Query single cell
            print(f"q 1 {x} {y}", flush=True)
            
            # Read response
            resp_line = sys.stdin.readline()
            if not resp_line:
                break
            
            try:
                # The response is a float representing the presence/noise
                resp_val = float(resp_line.strip())
                # Thresholding: if the value is significantly above 0, it's likely oil.
                # Given NOISE is provided, a simple threshold is a starting point.
                if resp_val > 0.5:
                    oil_cells.append((x, y))
            except ValueError:
                continue

    # Submit the final set of oil cells
    # Format: 'a k x1 y1 x2 y2 ... xk yk'
    if oil_cells:
        # Construct the command string
        cmd = [f"a {len(oil_cells)}"]
        for ox, oy in oil_cells:
            cmd.append(str(ox))
            cmd.append(str(oy))
        print(" ".join(cmd), flush=True)
    else:
        # Submit empty if nothing found
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()
