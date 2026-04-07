import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    R = int(input_data[idx]); idx += 1
    C = int(input_data[idx]); idx += 1
    N_shapes = int(input_data[idx]); idx += 1
    noise = float(input_data[idx]); idx += 1
    
    shapes = []
    for _ in range(N_shapes):
        k = int(input_data[idx]); idx += 1
        shape = []
        for _ in range(k):
            sx = int(input_data[idx]); idx += 1
            sy = int(input_data[idx]); idx += 1
            shape.append((sx, sy))
        shapes.append(shape)

    belief = [[0.0 for _ in range(C)] for _ in range(R)]
    oil_cells = set()

    # Simple strategy: scan grid with single queries
    # In a real scenario, we'd use aggregate queries and shape matching
    for r in range(R):
        for c in range(C):
            print(f"q 1 {r} {c}", flush=True)
            res = float(sys.stdin.readline().strip())
            belief[r][c] = res
            if res > 0.5:
                oil_cells.add((r, c))

    # Final submission
    res_list = list(oil_cells)
    k = len(res_list)
    cmd = [f"a {k}"]
    for r, c in res_list:
        cmd.append(f"{r} {c}")
    print(" ".join(cmd), flush=True)

if __name__ == "__main__":
    solve()