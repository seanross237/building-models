import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    K = int(input_data[2])
    P = float(input_data[3])
    
    idx = 4
    shapes = []
    for _ in range(K):
        size = int(input_data[idx])
        idx += 1
        shape = []
        for _ in range(size):
            shape.append((int(input_data[idx]), int(input_data[idx+1])))
            idx += 2
        shapes.append(shape)

    oil_cells = set()
    
    # Simple strategy: scan all cells with single-cell queries
    # In a real scenario, use aggregate queries and Bayesian updates
    for r in range(1, N + 1):
        for c in range(1, M + 1):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            res = sys.stdin.readline().strip()
            if not res:
                break
            if int(res) == 1:
                oil_cells.add((r, c))
        else:
            continue
        break

    # Output the identified cells
    cells_list = list(oil_cells)
    count = len(cells_list)
    output = [f"a {count}"]
    for r, c in cells_list:
        output.append(f"{r} {c}")
    
    print(" ".join(output))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()