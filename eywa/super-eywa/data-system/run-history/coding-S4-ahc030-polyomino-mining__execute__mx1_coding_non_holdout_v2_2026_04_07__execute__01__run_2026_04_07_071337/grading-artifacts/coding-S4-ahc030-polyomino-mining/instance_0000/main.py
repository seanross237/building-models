import sys

def solve():
    input_data = sys.stdin.readline().split()
    if not input_data:
        return
    
    # Grid size, number of fields, noise, number of shapes
    # Note: The exact input format is not specified, 
    # so we assume a standard parsing approach.
    try:
        N = int(input_data[0]) # Grid dimension
        M = int(input_data[1]) # Number of oil fields
        noise = float(input_data[2])
        num_shapes = int(input_data[3])
        
        shapes = []
        for _ in range(num_shapes):
            line = sys.stdin.readline().split()
            if not line: break
            k = int(line[0])
            coords = []
            for i in range(k):
                coords.append((int(line[1 + 2*i]), int(line[2 + 2*i])))
            shapes.append(coords)
    except (ValueError, IndexError):
        return

    oil_cells = set()
    
    # Simple strategy: probe every cell once to find oil
    # In a real scenario, we would use aggregate queries to save cost.
    # For a baseline, we probe single cells.
    for r in range(1, N + 1):
        for c in range(1, N + 1):
            print(f"q 1 {r} {c}", flush=True)
            res = sys.stdin.readline().strip()
            if res == "1":
                oil_cells.add((r, c))
            elif res == "0":
                pass
            else:
                # Handle potential error or noise
                pass

    # Submit the found oil cells
    if oil_cells:
        cells_list = []
        for r, c in oil_cells:
            cells_list.extend([r, c])
        print(f"a {len(oil_cells)} " + " ".join(map(str, cells_list)), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()