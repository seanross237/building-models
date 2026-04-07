import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = 50
    M = int(input_data[0])
    grid_flat = input_data[2:]
    
    # The input grid is N x N. 
    # We read the grid and print it as is.
    # The identity map is a valid baseline.
    
    grid = []
    idx = 0
    for r in range(N):
        row = []
        for c in range(N):
            row.append(grid_flat[idx])
            idx += 1
        grid.append(row)

    for row in grid:
        print(" ".join(row))

if __name__ == "__main__":
    solve()