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

    # A simple baseline: print 0 placements.
    # This is always valid according to the problem description.
    print(0)

if __name__ == '__main__':
    solve()