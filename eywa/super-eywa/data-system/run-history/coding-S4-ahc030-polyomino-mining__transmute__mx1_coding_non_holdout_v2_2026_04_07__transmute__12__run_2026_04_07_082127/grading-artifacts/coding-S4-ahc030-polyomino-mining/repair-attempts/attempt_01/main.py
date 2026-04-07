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
    
    # The shapes are provided in the input but for a simple robust strategy 
    # we will just scan the grid.
    # Note: The input format for shapes might span multiple lines.
    # We need to consume the rest of the input correctly.
    
    # Since we don't know how many lines the shapes take, we read until we have K shapes.
    # However, the problem says "The initial input describes...". 
    # Let's assume the shapes are part of the initial block.
    
    # To be safe, we'll read all remaining input for the initial setup.
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
    # This is robust against noise P if P is a noise parameter for aggregate queries.
    # If P affects single queries, we'd need multiple samples, but usually 
    # in these problems, q 1 is deterministic or the noise is for 'q k'.
    
    for r in range(N):
        for c in range(M):
            print(f"q 1 {r} {c}", flush=True)
            res_line = sys.stdin.readline().strip()
            if not res_line:
                break
            try:
                res = int(res_line)
                if res > 0:
                    found_cells.append((r, c))
            except ValueError:
                break
        else:
            continue
        break

    # Final submission
    # Format: a k x1 y1 x2 y2 ... xk yk
    if found_cells:
        output = [f"a {len(found_cells)}"]
        for r, c in found_cells:
            output.append(f"{r} {c}")
        print(" ".join(output), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()
