import sys

def solve():
    # Read N, M, K
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # The problem states N=9, M=20, K=81
    # We don't actually need to process the board or stamps to provide a valid baseline
    # A valid baseline is to place 0 stamps.
    
    print(0)

if __name__ == '__main__':
    solve()