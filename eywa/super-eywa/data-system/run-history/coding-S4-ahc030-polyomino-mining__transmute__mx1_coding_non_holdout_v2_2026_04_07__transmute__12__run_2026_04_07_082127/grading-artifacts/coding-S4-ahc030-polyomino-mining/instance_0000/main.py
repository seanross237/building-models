import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    input_data = line.split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    K = int(input_data[2])
    P = int(input_data[3])
    
    # Consume the rest of the input for shapes
    # The shapes are provided in the input.
    remaining_input = sys.stdin.read().split()
    idx = 0
    shapes = []
    for _ in range(K):
        if idx >= len(remaining_input):
            break
        num_cells = int(remaining_input[idx])
        idx += 1
        shape = []
        for _ in range(num_cells):
            r = int(remaining_input[idx])
            c = int(remaining_input[idx+1])
            shape.append((r, c))
            idx += 2
        shapes.append(shape)

    found_cells = []

    # Strategy: Scan grid with single-cell queries.
    # Single-cell queries 'q 1 x y' return 1 if oil, 0 if not.
    # We iterate through the grid. To avoid TLE or excessive cost, 
    # we use a simple scan. In a real competition, one would use 
    # the polyomino shapes to skip cells, but a full scan is the most robust 
    # way to ensure correctness if the budget allows.
    
    for r in range(N):
        for c in range(M):
            print(f"q 1 {r} {c}", flush=True)
            res_line = sys.stdin.readline().strip()
            if not res_line:
                # If we hit EOF unexpectedly, stop
                break
            try:
                res = int(res_line)
                if res > 0:
                    found_cells.append((r, c))
            except ValueError:
                # If we get non-integer response, stop
                break
        else:
            continue
        break

    # Final submission
    # Format: a k x1 y1 x2 y2 ... xk yk
    if found_cells:
        # Construct the command string
        cmd = ["a", str(len(found_cells))]
        for r, c in found_cells:
            cmd.append(str(r))
            cmd.append(str(c))
        print(" ".join(cmd), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()
