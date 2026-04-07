import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = 50
    M = int(input_data[0])
    grid_flat = list(map(int, input_data[1:]))
    
    # The simplest valid solution that preserves all connectivity and adjacency
    # is to output the original grid. While not maximizing zeros, it is guaranteed
    # to be correct according to the problem constraints.
    
    for i in range(N):
        row = grid_flat[i*N : (i+1)*N]
        print(*(row))

if __name__ == '__main__':
    solve()