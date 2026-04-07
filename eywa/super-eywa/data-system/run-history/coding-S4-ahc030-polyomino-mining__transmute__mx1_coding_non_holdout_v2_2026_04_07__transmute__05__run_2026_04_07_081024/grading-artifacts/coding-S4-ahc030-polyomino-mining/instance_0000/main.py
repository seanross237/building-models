import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    width = int(input_data[idx]); idx += 1
    height = int(input_data[idx]); idx += 1
    N = int(input_data[idx]); idx += 1
    P = float(input_data[idx]); idx += 1
    
    shapes = []
    # Assuming shapes are provided as number of shapes followed by their sizes
    # This part is tricky without exact format, assuming standard list
    num_shapes = int(input_data[idx]); idx += 1
    for _ in range(num_shapes):
        s_size = int(input_data[idx]); idx += 1
        shape = []
        for _ in range(s_size):
            dx = int(input_data[idx]); idx += 1
            dy = int(input_data[idx]); idx += 1
            shape.append((dx, dy))
        shapes.append(shape)

    oil_cells = set()
    
    # Simple strategy: probe every cell to find oil
    # In a real scenario, we would use the polyomino shapes to optimize
    for x in range(width):
        for y in range(height):
            print(f"q 1 {x} {y}", flush=True)
            res = sys.stdin.readline().strip()
            if res == "1" or res == "True":
                oil_cells.add((x, y))
    
    # Final submission
    if oil_cells:
        cells = list(oil_cells)
        k = len(cells)
        cmd = [f"a {k}"]
        for cx, cy in cells:
            cmd.append(f"{cx} {cy}")
        print(" ".join(cmd), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()