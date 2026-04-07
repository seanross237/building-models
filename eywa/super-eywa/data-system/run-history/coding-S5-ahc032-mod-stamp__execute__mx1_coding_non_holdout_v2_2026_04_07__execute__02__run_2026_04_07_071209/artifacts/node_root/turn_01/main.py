import sys

def solve():
    # Read N, M, K
    line1 = sys.stdin.readline().split()
    if not line1: return
    n, m, k = map(int, line1)
    
    # Read initial board
    board = []
    for _ in range(n):
        board.append(list(map(int, sys.stdin.readline().split())))
        
    # Read M stamps
    stamps = []
    for _ in range(m):
        stamp = []
        for _ in range(3):
            stamp.append(list(map(int, sys.stdin.readline().split())))
        stamps.append(stamp)

    # A valid baseline is to place 0 stamps.
    # This satisfies 0 <= L <= K.
    print(0)

if __name__ == '__main__':
    solve()