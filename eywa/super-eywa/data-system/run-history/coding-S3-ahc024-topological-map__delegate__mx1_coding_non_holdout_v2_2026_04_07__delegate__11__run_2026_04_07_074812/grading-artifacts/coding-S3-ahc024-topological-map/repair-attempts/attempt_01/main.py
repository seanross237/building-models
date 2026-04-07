import sys

def solve():
    # Read N, M
    try:
        line1 = sys.stdin.readline().split()
        if not line1:
            return
        N = int(line1[0])
        M = int(line1[1])
    except EOFError:
        return

    # Read the 50x50 grid
    grid = []
    for _ in range(N):
        grid.append(list(map(int, sys.stdin.readline().split())))

    # The problem asks to preserve connectivity and adjacency relations.
    # A simple valid solution is to output the original grid itself.
    # This guarantees that:
    # 1. Every nonzero color remains connected (as it was in the input).
    # 2. Two colors are adjacent if and only if they were adjacent in the input.
    # While this doesn't maximize the number of 0s (E), it is a strictly valid 
    # solution that satisfies all topological constraints.
    
    for row in grid:
        print(*(row))

if __name__ == "__main__":
    solve()
