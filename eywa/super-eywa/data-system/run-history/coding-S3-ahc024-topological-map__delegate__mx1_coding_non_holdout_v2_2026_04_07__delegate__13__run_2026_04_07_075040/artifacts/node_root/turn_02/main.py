import sys

def solve():
    # Read N, M
    try:
        line1 = sys.stdin.readline().split()
        if not line1: return
        n = int(line1[0])
        m = int(line1[1])
    except EOFError:
        return
    except ValueError:
        return

    # Read the 50x50 grid
    grid = []
    for _ in range(n):
        row = list(map(int, sys.stdin.readline().split()))
        if not row:
            break
        grid.append(row)

    # The objective is to maximize empty cells (0) while preserving
    # connectivity and adjacency. 
    # A simple valid baseline is to output the original grid.
    # This guarantees that connectivity and adjacency are preserved.
    
    for row in grid:
        print(*(row))

if __name__ == '__main__':
    solve()