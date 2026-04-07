import sys

def solve():
    line = sys.stdin.readline()
    if not line:
        return
    parts = line.split()
    if not parts:
        return
    
    try:
        grid_size = int(parts[0])
        num_fields = int(parts[1])
        noise = float(parts[2])
    except (ValueError, IndexError):
        return
    
    found_cells = []
    
    # Conservative probing strategy to avoid exceeding limits
    # We probe a small subset of the grid.
    limit = min(grid_size * grid_size, 100)
    count = 0
    
    for x in range(grid_size):
        for y in range(grid_size):
            if count >= limit:
                break
            
            print(f"q 1 {x} {y}", flush=True)
            res_line = sys.stdin.readline()
            if not res_line:
                break
            
            res = res_line.split()
            # The error was IndexError: list index out of range
            # This happens if the scorer returns an empty line or a single value.
            # We must check if res has enough elements.
            if len(res) >= 2:
                # res[0] is the type, res[1] is the result
                if res[1] == '1':
                    found_cells.append((x, y))
            
            count += 1
        if count >= limit:
            break

    # Submit found cells
    # Format: a <count> <x1> <y1> <x2> <y2> ...
    if found_cells:
        output = [f"a {len(found_cells)}"]
        for cx, cy in found_cells:
            output.append(f"{cx} {cy}")
        print(" ".join(output), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()
