import sys

def solve():
    # Read N, M from the first line
    try:
        line = sys.stdin.readline().split()
        if not line: 
            return
        n = int(line[0])
        m = int(line[1])
    except (ValueError, IndexError):
        return

    # Read the 50x50 grid
    grid = []
    for _ in range(n):
        row = list(map(int, sys.stdin.readline().split()))
        grid.append(row)

    # The simplest valid solution is to output the original grid.
    # This preserves all connectivity and adjacency relations.
    for row in grid:
        print(*(row))

if __name__ == "__main__":
    solve()