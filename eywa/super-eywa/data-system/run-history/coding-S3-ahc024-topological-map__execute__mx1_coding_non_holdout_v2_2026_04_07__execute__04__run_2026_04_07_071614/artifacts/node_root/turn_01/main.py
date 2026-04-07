import sys

def solve():
    # Read N, M
    try:
        line1 = sys.stdin.readline().split()
        if not line1: return
        N = int(line1[0])
        M = int(line1[1])
    except EOFError:
        return

    # Read the 50x50 grid
    grid = []
    for _ in range(N):
        row = list(map(int, sys.stdin.readline().split()))
        grid.append(row)

    # The simplest valid solution that preserves connectivity 
    # and all color-adjacency relations is the input grid itself.
    # In the input grid, connectivity and adjacency are already satisfied.
    # This baseline ensures validity.
    
    for r in range(N):
        print(*(grid[r]))

if __name__ == '__main__':
    solve()