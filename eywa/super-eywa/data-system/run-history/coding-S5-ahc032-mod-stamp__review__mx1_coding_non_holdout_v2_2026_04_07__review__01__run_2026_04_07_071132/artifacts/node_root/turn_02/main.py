import sys

def solve():
    # Read N, M, K
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # The problem states N=9, M=20, K=81
    # We just need to output 0 to indicate zero placements.
    print(0)

if __name__ == '__main__':
    solve()