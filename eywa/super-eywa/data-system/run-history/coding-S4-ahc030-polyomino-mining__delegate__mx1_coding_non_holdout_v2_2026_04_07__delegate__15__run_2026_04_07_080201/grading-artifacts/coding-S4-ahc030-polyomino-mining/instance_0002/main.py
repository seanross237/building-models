import sys

def solve():
    # Read initial input
    # Format: H W N noise_param
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if not parts:
        return
    H, W, N, noise = parts

    shapes = []
    for _ in range(N):
        shape_line = sys.stdin.readline()
        if not shape_line:
            break
        shape_data = list(map(int, shape_line.split()))
        if not shape_data:
            continue
        k = shape_data[0]
        cells = []
        for i in range(k):
            cells.append((shape_data[1 + 2*i], shape_data[2 + 2*i]))
        shapes.append(cells)

    # Strategy:
    # The problem asks to minimize cost. A simple scan is a baseline.
    # We must ensure we don't crash if the input is slightly different.
    # We will probe every cell to be safe, as a baseline.
    
    found_oil_cells = []
    
    # To avoid TLE or excessive cost in a real scenario, we'd use a smarter approach.
    # But for a valid submission, we must follow the protocol.
    # We'll probe cells. We use a single-cell query 'q 1 x y'.
    
    for r in range(H):
        for c in range(W):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            res_line = sys.stdin.readline()
            if not res_line:
                break
            try:
                res = int(res_line.strip())
            except ValueError:
                break
            
            # In many AHC problems, res > 0 indicates presence of oil.
            # Given noise, we assume res > 0 means oil is present.
            if res > 0:
                found_oil_cells.append((r, c))
        else:
            continue
        break

    # Final submission
    # Format: a k x1 y1 x2 y2 ...
    # Note: The problem says "a k x1 y1 ... xk yk"
    # The current code was doing "a k \n x1 y1 ..." which is wrong.
    # It should be "a k x1 y1 x2 y2 ..." on one line or following the specific format.
    # Re-reading: "a k x1 y1 ... xk yk" implies a single line.
    
    k = len(found_oil_cells)
    output_parts = [f"a {k}"]
    for r, c in found_oil_cells:
        output_parts.append(f"{r} {c}")
    
    print(" ".join(output_parts))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
