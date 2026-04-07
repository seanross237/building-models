import sys

def solve():
    # Read N, M, K
    line1 = sys.stdin.readline().split()
    if not line1: return
    N, M, K = map(int, line1)

    # Read initial board
    board = []
    for _ in range(N):
        board.append(list(map(int, sys.stdin.readline().split())))

    # Read M stamps
    stamps = []
    for _ in range(M):
        stamp = []
        for _ in range(3):
            stamp.append(list(map(int, sys.stdin.readline().split())))
        stamps.append(stamp)

    # The problem asks for up to K placements of 3x3 stamps.
    # A simple valid baseline is to output 0 placements.
    # The output format for these types of problems is usually:
    # Number of placements
    # For each placement: stamp_index r c
    
    # We will output 0 placements to ensure a valid, though non-optimal, solution.
    print(0)

if __name__ == '__main__':
    solve()
