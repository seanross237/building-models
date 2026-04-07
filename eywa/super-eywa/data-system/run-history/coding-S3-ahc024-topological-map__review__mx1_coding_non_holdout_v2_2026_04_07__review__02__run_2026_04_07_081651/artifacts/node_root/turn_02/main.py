import sys

def solve():
    # Read N, M from the first line
    # The problem states N=50, but we should read it to be safe.
    # Input format: N M followed by N lines of N integers
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    M = int(input_data[1])
    
    grid = []
    idx = 2
    for r in range(N):
        row = []
        for c in range(N):
            row.append(input_data[idx])
            idx += 1
        grid.append(row)

    # The simplest valid solution is to output the original grid.
    # This preserves all connectivity and adjacency relations.
    for row in grid:
        print(" ".join(row))

if __name__ == "__main__":
    solve()