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
        k = shape_parts[0]
        cells = []
        for i in range(k):
            cells.append((shape_parts[1 + 2*i], shape_parts[2 + 2*i]))
        shapes.append(cells)

    discovered_oil = set()
    
    # Strategy:
    # To avoid TLE and handle the interactive nature, we use a simple scan.
    # We use a step to find potential oil cells.
    # Given the constraints and the nature of the problem, we'll probe 
    # cells to find any signal.
    
    step = 2
    for r in range(0, H, step):
        for c in range(0, W, step):
            # Single cell query
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            res_line = sys.stdin.readline()
            if not res_line:
                break
            try:
                res = int(res_line.strip())
            except ValueError:
                break
            
            if res > 0:
                # If we find a signal, check immediate neighbors to confirm
                # This is a simple way to find the boundaries of a shape
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < H and 0 <= nc < W:
                            # We don't re-query (r, c) to save cost
                            if dr == 0 and dc == 0:
                                discovered_oil.add((r, c))
                                continue
                                
                            print(f"q 1 {nr} {nc}")
                            sys.stdout.flush()
                            res_inner_line = sys.stdin.readline()
                            if not res_inner_line:
                                break
                            try:
                                res_inner = int(res_inner_line.strip())
                                if res_inner > 0:
                                    discovered_oil.add((nr, nc))
                            except ValueError:
                                break
        if len(discovered_oil) >= (N * 10): # Heuristic limit to prevent TLE
            break

    # Final Submission
    # Format: a k x1 y1 x2 y2 ...
    if not discovered_oil:
        print("a 0")
    else:
        coords = []
        for r, c in discovered_oil:
            coords.append(r)
            coords.append(c)
        print(f"a {len(discovered_oil)} {' '.join(map(str, coords))}")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
