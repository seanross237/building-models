import sys

def solve():
    line = sys.stdin.readline()
    if not line:
        return
    parts = line.split()
    if not parts:
        return
    
    grid_size = int(parts[0])
    num_fields = int(parts[1])
    noise = float(parts[2])
    
    # Simplified strategy: probe cells to find oil
    # In a real scenario, we'd use the polyomino shapes
    # For this baseline, we probe cells and collect hits
    
    found_cells = []
    
    # This is a placeholder strategy for the interactive task
    # Real implementation would involve complex spatial reasoning
    for x in range(grid_size):
        for y in range(grid_size):
            print(f"q 1 {x} {y}", flush=True)
            res = sys.stdin.readline().split()
            if not res:
                break
            if res[1] == '1':
                found_cells.append((x, y))
        if found_cells and len(found_cells) >= num_fields * 4: # heuristic
            break

    # Submit found cells
    if found_cells:
        out = [f"a {len(found_cells)}"]
        for cx, cy in found_cells:
            out.append(f"{cx} {cy}")
        print(" ".join(out), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()