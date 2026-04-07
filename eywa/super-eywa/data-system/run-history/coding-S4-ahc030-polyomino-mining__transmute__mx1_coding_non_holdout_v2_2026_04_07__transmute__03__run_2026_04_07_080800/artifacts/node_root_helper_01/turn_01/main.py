import sys

def solve():
    line = sys.stdin.readline()
    if not line:
        return
    try:
        H, W, N, noise = map(float, line.split())
        H, W, N = int(H), int(W), int(N)
    except ValueError:
        return

    shapes = []
    for _ in range(N):
        shape_line = sys.stdin.readline().split()
        if not shape_line:
            break
        k = int(shape_line[0])
        coords = []
        for i in range(k):
            coords.append((int(shape_line[1 + 2*i]), int(shape_line[2 + 2*i])))
        shapes.append(coords)

    # Simple strategy: probe every cell to find oil
    # In a real scenario, we would use aggregate queries and pattern matching
    # For this baseline, we probe cells and collect results
    
    oil_cells = []
    
    # Since we don't know the noise model or exact query response format
    # for aggregate queries vs single, we use single-cell queries for simplicity.
    # Note: The problem description implies 'q 1 x y' returns occupancy.
    
    for y in range(H):
        for x in range(W):
            print(f"q 1 {x} {y}")
            sys.stdout.flush()
            
            res = sys.stdin.readline().strip()
            if not res:
                break
            
            # Assuming response is '1' for oil, '0' for empty
            if res == '1':
                oil_cells.append((x, y))
        if not oil_cells and y == H-1:
            pass # continue

    # Final submission
    if oil_cells:
        out = [f"a {len(oil_cells)}"]
        for cx, cy in oil_cells:
            out.append(f"{cx} {cy}")
        print(" ".join(out))
        sys.stdout.flush()
    else:
        print("a 0")
        sys.stdout.flush()

if __name__ == "__main__":
    solve()