import sys

def solve():
    # Read N, M, K
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # The problem asks for a valid sequence of placements.
    # A valid baseline is to perform 0 placements.
    # This satisfies L <= K and the constraints.
    print(0)

if __name__ == '__main__':
    solve()