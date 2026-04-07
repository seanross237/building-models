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

    # The simplest valid solution that preserves connectivity 
    # and adjacency is the input grid itself.
    # This ensures all constraints are met perfectly.
    for r in range(N):
        print(*(grid[r]))

if __name__ == '__main__':
    solve()