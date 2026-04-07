import sys

def solve():
    # Read N, M from the first line
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
    except ValueError:
        return

    # Read the 50x50 grid
    grid = []
    for _ in range(n):
        row_str = sys.stdin.readline()
        if not row_str:
            break
        row = list(map(int, row_str.split()))
        grid.append(row)

    # The simplest valid solution that preserves all connectivity 
    # and adjacency relations is to output the input grid itself.
    for row in grid:
        print(*(row))

if __name__ == "__main__":
    solve()