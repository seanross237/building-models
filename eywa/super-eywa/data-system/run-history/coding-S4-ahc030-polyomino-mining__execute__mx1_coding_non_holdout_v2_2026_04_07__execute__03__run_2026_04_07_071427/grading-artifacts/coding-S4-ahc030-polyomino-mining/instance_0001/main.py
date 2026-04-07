import sys

def solve():
    input_data = sys.stdin.readline().split()
    if not input_data: return
    
    # Grid size, number of fields, noise, number of shapes
    # Note: The problem description is slightly abstract about input format.
    # We assume a standard format: H W N S followed by S shapes.
    try:
        H = int(input_data[0])
        W = int(input_data[1])
        N = int(input_data[2])
        S = int(input_data[3])
    except (ValueError, IndexError):
        return

    shapes = []
    for _ in range(S):
        line = sys.stdin.readline().split()
        if not line: break
        k = int(line[0])
        coords = []
        for i in range(k):
            coords.append((int(line[1 + 2*i]), int(line[2 + 2*i])))
        shapes.append(coords)

    found_oil = set()
    
    # Simple strategy: probe cells randomly or in a grid to find oil
    # Since we want to minimize cost, we use single-cell queries 'q 1 x y'
    # and then try to reconstruct shapes.
    
    # For a baseline, we probe a subset of the grid.
    # In a real contest, we'd use more sophisticated heuristics.
    step = max(1, H // 5)
    for r in range(0, H, step):
        for c in range(0, W, step):
            print(f"q 1 {r} {c}", flush=True)
            res = sys.stdin.readline().split()
            if not res: break
            # Assume response is '1' for oil, '0' for no oil
            if res[0] == '1':
                found_oil.add((r, c))

    # After probing, we attempt to find the full polyominoes.
    # This is a placeholder for a more complex reconstruction logic.
    # For the baseline, we just report the cells we found.
    
    # Final submission: 'a k x1 y1 ... xk yk'
    oil_list = list(found_oil)
    k = len(oil_list)
    if k == 0:
        print("a 0", flush=True)
    else:
        cmd = ["a", str(k)]
        for r, c in oil_list:
            cmd.append(str(r))
            cmd.append(str(c))
        print(" ".join(cmd), flush=True)

if __name__ == "__main__":
    solve()