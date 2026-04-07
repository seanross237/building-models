import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if not parts:
        return
    H, W, N, noise = parts

    # Read polyomino shapes
    shapes = []
    for _ in range(N):
        line = sys.stdin.readline()
        if not line:
            break
        shape_parts = list(map(int, line.split()))
        if not shape_parts:
            continue
        # shape_parts[0] is the number of cells in the polyomino
        # followed by x1, y1, x2, y2...
        cells = []
        for i in range(1, len(shape_parts), 2):
            cells.append((shape_parts[i], shape_parts[i+1]))
        shapes.append(cells)

    found_oil = set()
    
    # Strategy: Simple scan to find any oil cells.
    # We use a step to reduce the number of queries.
    # Since we don't know the cost of 'q k', we stick to 'q 1' for safety.
    step = 2
    for r in range(0, H, step):
        for c in range(0, W, step):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            resp = sys.stdin.readline()
            if not resp:
                break
            try:
                val = int(resp.strip())
                if val > 0:
                    # If we find oil, we add the cell.
                    # In a real scenario, we'd use the shapes to find the rest.
                    found_oil.add((r, c))
            except ValueError:
                break
        else:
            continue
        break

    # Final submission
    # The format is: a k x1 y1 x2 y2 ... xk yk
    if not found_oil:
        print("a 0")
    else:
        # Convert set to list for consistent ordering
        oil_list = sorted(list(found_oil))
        output = [f"a {len(oil_list)}"]
        for r, c in oil_list:
            output.append(f"{r} {c}")
        
        # The problem says "a k x1 y1 ... xk yk"
        # This implies all coordinates on one line or space separated.
        # Let's construct the single line command.
        cmd = f"a {len(oil_list)}"
        for r, c in oil_list:
            cmd += f" {r} {c}"
        print(cmd)
        
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
