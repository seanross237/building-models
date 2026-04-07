import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = 50
    M = int(input_data[0])
    grid_flat = input_data[1:]
    
    # The problem asks to preserve connectivity and adjacency.
    # The simplest valid solution is to output the input grid itself.
    # This ensures all connectivity and adjacency relations are perfectly preserved.
    # While it doesn't maximize E (empty cells), it is a guaranteed valid baseline.
    
    grid = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(grid_flat[i * N + j])
        grid.append(row)

    for row in grid:
        print(" ".join(row))

if __name__ == "__main__":
    solve()