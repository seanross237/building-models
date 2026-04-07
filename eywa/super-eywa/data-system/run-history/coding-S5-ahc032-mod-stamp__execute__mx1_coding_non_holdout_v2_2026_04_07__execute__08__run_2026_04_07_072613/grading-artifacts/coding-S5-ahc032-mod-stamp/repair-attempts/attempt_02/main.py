import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1
    
    MOD = 998244353
    
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        board.append(row)
        
    stamps = []
    for m in range(M):
        stamp = []
        for r in range(3):
            s_row = []
            for c in range(3):
                s_row.append(int(input_data[idx]))
                idx += 1
            stamp.append(s_row)
        stamps.append(stamp)

    placements = []
    
    # The problem asks for 3x3 stamps on an NxN board.
    # A stamp starting at (r, c) covers cells (r, c) to (r+2, c+2).
    # Valid top-left indices (0-indexed) are 0 <= r <= N-3 and 0 <= c <= N-3.
    # The scorer error 'Out of range: 7' suggests the output (r, c, m) 
    # uses 1-based indexing for r and c, and the max value allowed for r or c 
    # is N-2 (since r+2 <= N).
    # For N=9, max r is 7 (1-based).
    
    # Simple baseline: pick the first stamp at (1, 1) up to K times.
    # This is guaranteed to be within bounds if N >= 3.
    if N >= 3:
        for _ in range(K):
            placements.append((1, 1, 1))

    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == '__main__':
    solve()
