import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    parts = line.split()
    if not parts:
        return
    
    grid_size = int(parts[0])
    num_fields = int(parts[1])
    noise = float(parts[2])
    
    # The problem mentions polyomino shapes follow in the input
    # We need to consume the rest of the input to be safe, 
    # though for a simple baseline we just need the grid info.
    # The shapes are likely provided as a list of relative coordinates.
    shapes = []
    # Since the exact format of shapes isn't fully detailed in the snippet,
    # we assume the rest of the lines describe the shapes.
    # However, for a robust baseline, we just proceed to queries.

    found_cells = []
    
    # Simple strategy: probe cells in a grid pattern.
    # To avoid TLE or excessive cost, we use a step.
    # But since we need to find polyominoes, we'll probe.
    # We'll stop after a reasonable number of probes or finding enough cells.
    
    # Heuristic: probe every 2nd cell to find a starting point, 
    # then probe neighbors. For this baseline, we probe a subset.
    step = max(1, grid_size // 10)
    
    stop_probing = False
    for x in range(0, grid_size, step):
        for y in range(0, grid_size, step):
            if stop_probing:
                break
            
            print(f"q 1 {x} {y}", flush=True)
            res_line = sys.stdin.readline()
            if not res_line:
                stop_probing = True
                break
            
            res = res_line.split()
            if not res:
                stop_probing = True
                break
            
            # The response format for 'q 1 x y' is expected to be '1' or '0' (or similar)
            # Based on the provided code, res[1] was used, implying 'q 1 x y' returns 'status value'
            # or similar. Let's check if res[0] is the value.
            # If the tester returns "1" for hit, res[0] is "1".
            if res[0] == '1':
                found_cells.append((x, y))
                # If we found a hit, let's probe immediate neighbors to find the shape
                for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid_size and 0 <= ny < grid_size:
                        print(f"q 1 {nx} {ny}", flush=True)
                        res_n = sys.stdin.readline().split()
                        if res_n and res_n[0] == '1':
                            found_cells.append((nx, ny))
                
                # Heuristic limit to prevent infinite/too long execution
                if len(found_cells) >= num_fields * 10:
                    stop_probing = True
        if stop_probing:
            break

    # Submit found cells
    # Format: a k x1 y1 x2 y2 ... xk yk
    if found_cells:
        # Remove duplicates
        unique_cells = list(set(found_cells))
        output = [f"a {len(unique_cells)}"]
        for cx, cy in unique_cells:
            output.append(f"{cx} {cy}")
        print(" ".join(output), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()
