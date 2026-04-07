import sys

def solve():
    # Read N, M, K
    line1 = sys.stdin.readline().split()
    if not line1: return
    n, m, k = map(int, line1)
    
    # Skip the board
    for _ in range(n):
        sys.stdin.readline()
        
    # Skip the stamps
    for _ in range(m):
        for _ in range(3):
            sys.stdin.readline()
            
    # Output 0 placements as a valid baseline
    print(0)

if __name__ == '__main__':
    solve()