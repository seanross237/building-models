import sys

def solve():
    input_data = sys.stdin.readline().split()
    if not input_data: return
    N, M, K, P = map(int, input_data[:4])
    
    shapes = []
    idx = 4
    for _ in range(K):
        num_cells = int(input_data[idx])
        idx += 1
        shape = []
        for _ in range(num_cells):
            shape.append((int(input_data[idx]), int(input_data[idx+1])))
            idx += 2
        shapes.append(shape)

    found_cells = set()

    # Strategy: Scan grid with single-cell queries
    # In a real scenario, we would use aggregate queries to speed up
    # but single-cell is robust against noise P.
    for r in range(N):
        for c in range(M):
            print(f"q 1 {r} {c}", flush=True)
            res = sys.stdin.readline().strip()
            if not res: break
            if int(res) > 0:
                found_cells.add((r, c))
        if not res: break

    # Final submission
    if found_cells:
        cells_list = list(found_cells)
        output = [f"a {len(cells_list)}"]
        for r, c in cells_list:
            output.append(f"{r} {c}")
        print(" ".join(output), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()