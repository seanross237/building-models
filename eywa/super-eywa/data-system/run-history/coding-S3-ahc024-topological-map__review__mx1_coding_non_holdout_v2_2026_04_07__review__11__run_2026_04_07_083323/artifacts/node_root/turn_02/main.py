import sys

def solve():
    # Read N and M
    try:
        line = sys.stdin.readline()
        if not line:
            return
        parts = line.split()
        if not parts:
            return
        n = int(parts[0])
        m = int(parts[1])
    except EOFError:
        return

    # Read the 50x50 grid
    grid = []
    for _ in range(n):
        row = list(map(int, sys.stdin.readline().split()))
        grid.append(row)

    # The simplest valid solution is to output the input grid itself.
    # This preserves all connectivity and adjacency relations.
    for row in grid:
        print(*(row))

if __name__ == "__main__":
    solve()