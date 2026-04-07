import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    W = int(input_data[idx]); idx += 1
    H = int(input_data[idx]); idx += 1
    N = int(input_data[idx]); idx += 1
    noise = float(input_data[idx]); idx += 1
    
    shapes = []
    for _ in range(N):
        num_cells = int(input_data[idx]); idx += 1
        shape = []
        for _ in range(num_cells):
            dx = int(input_data[idx]); idx += 1
            dy = int(input_data[idx]); idx += 1
            shape.append((dx, dy))
        shapes.append(shape)

    oil_cells = set()
    
    # Simple strategy: probe every cell using single-cell drill
    # In a real scenario, aggregate queries would be used to optimize cost
    for x in range(W):
        for y in range(H):
            print(f"q 1 {x} {y}", flush=True)
            res = sys.stdin.readline().strip()
            if res == '1':
                oil_cells.add((x, y))
            elif res == '0':
                pass
            else:
                # Handle potential error or noise if aggregate was used
                pass

    # Final submission
    cells_list = list(oil_cells)
    k = len(cells_list)
    cmd = [f"a", str(k)]
    for cx, cy in cells_list:
        cmd.append(str(cx))
        cmd.append(str(cy))
    
    print(" ".join(cmd), flush=True)

if __name__ == "__main__":
    solve()