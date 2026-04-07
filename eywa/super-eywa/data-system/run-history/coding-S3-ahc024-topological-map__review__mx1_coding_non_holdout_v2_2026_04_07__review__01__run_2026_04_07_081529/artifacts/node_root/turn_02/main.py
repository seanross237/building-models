import sys

def solve():
    # Read N, M from the first line
    # The problem states N=50, but we should read it to be safe.
    # Input format: N M
    # Then N lines of N integers
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    M = int(input_data[1])
    
    grid_elements = input_data[2:]
    
    # Reconstruct the grid
    grid = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(grid_elements[i * N + j])
        grid.append(row)

    # Output the grid exactly as it was read
    for row in grid:
        print(" ".join(row))

if __name__ == "__main__":
    solve()