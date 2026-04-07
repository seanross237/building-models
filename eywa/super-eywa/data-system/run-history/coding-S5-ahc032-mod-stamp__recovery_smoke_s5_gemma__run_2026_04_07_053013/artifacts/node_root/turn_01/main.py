import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1
    
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
        for i in range(3):
            row = []
            for j in range(3):
                row.append(int(input_data[idx]))
                idx += 1
            stamp.append(row)
        stamps.append(stamp)

    MOD = 998244353

    # Greedy approach: 
    # In each step, find the stamp and position that increases the total sum the most.
    # Since K is up to 81 and N is 9, we can afford some computation.
    
    placements = []
    
    # Pre-calculate stamp sums
    stamp_sums = []
    for m in range(M):
        s = 0
        for i in range(3):
            for j in range(3):
                s += stamps[m][i][j]
        stamp_sums.append(s)

    # To keep it simple and efficient, let's just pick the best stamp and place it
    # at all possible positions if it increases the sum.
    # Actually, the modulo makes it tricky. But if we assume the values don't wrap around
    # too often, we just want the largest stamp sum.
    
    # Find the stamp with the maximum sum
    best_m = 0
    max_s = -float('inf')
    for m in range(M):
        if stamp_sums[m] > max_s:
            max_s = stamp_sums[m]
            best_m = m