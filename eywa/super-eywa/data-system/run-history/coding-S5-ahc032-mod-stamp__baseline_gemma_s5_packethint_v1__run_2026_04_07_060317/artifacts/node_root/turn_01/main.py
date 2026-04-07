import sys

def solve():
    # Read N, M, K
    line1 = sys.stdin.readline().split()
    if not line1: return
    n, m, k = map(int, line1)
    
    # Read the board
    board = []
    for _ in range(n):
        board.append(list(map(int, sys.stdin.readline().split())))
        
    # Read the M stamps
    stamps = []
    for _ in range(m):
        stamp = []
        for _ in range(3):
            stamp.append(list(map(int, sys.stdin.readline().split())))
        stamps.append(stamp)

    # A simple valid baseline is to output 0 placements.
    # This satisfies 0 <= L <= K and the output format.
    print(0)

if __name__ == '__main__':
    solve()