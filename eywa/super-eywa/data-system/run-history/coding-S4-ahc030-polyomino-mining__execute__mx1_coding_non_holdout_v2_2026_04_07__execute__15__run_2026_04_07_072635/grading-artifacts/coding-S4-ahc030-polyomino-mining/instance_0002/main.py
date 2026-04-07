import sys

def solve():
    # Read initial input
    # Format: H W N noise
    # Followed by N polyomino shapes
    line = sys.stdin.readline()
    if not line:
        return
    
    try:
        parts = list(map(int, line.split()))
        if len(parts) < 4:
            return
        H, W, N, noise = parts
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

    oil_cells = []

    # Strategy: Simple exhaustive single-cell drill
    # This is a baseline to ensure correctness and interaction protocol compliance.
    # In a real competition, one would use information gain or aggregate queries.
    
    for r in range(H):
        for c in range(W):
            # Command: q 1 x y
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            # Read response
            resp = sys.stdin.readline().strip()
            if not resp:
                break
            
            # Response is typically '1' for oil or '0' for no oil
            # Depending on the tester implementation, it might be '1' or '0'
            if resp == '1':
                oil_cells.append((r, c))

    # Final Answer
    # Command: a k x1 y1 ... xk yk
    if oil_cells:
        output = [f"a {len(oil_cells)}"]
        for r, c in oil_cells:
            output.append(f"{r} {c}")
        print(" ".join(output))
    else:
        print("a 0")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()