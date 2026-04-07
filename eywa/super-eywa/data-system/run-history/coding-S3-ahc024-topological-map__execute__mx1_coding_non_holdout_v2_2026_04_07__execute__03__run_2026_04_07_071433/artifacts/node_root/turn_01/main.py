import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = 50
    M = int(input_data[0])
    grid = []
    idx = 1
    for r in range(N):
        row = []
        for c in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        grid.append(row)

    # The simplest valid solution is to output the input grid itself.
    # The input grid is guaranteed to satisfy connectivity and adjacency constraints.
    # This ensures a valid (though not necessarily optimal) score.
    for r in range(N):
        print(*(grid[r]))

if __name__ == '__main__':
    solve()