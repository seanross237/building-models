import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    grid_in = []
    idx = 2
    for r in range(N):
        grid_in.append([int(x) for x in input_data[idx:idx+N]])
        idx += N

    # The goal is to preserve connectivity and adjacency.
    # A trivial valid solution is to output the input grid itself.
    # The problem asks for a 50x50 grid of colors 0..M.
    # The input grid is already a 50x50 grid of colors 0..M.
    # It satisfies:
    # 1. Every nonzero color remains connected (it's the same grid).
    # 2. Two colors are adjacent if and only if they were adjacent in the input.
    # 3. The score is E + 1, where E is the number of 0 cells.
    # While not optimal for score, it is strictly valid.
    
    for r in range(N):
        print(*(grid_in[r]))

if __name__ == "__main__":
    solve()
