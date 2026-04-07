import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
    MOD = 998244353
    
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[ptr]))
            ptr += 1
        board.append(row)
        
    stamps = []
    for m in range(M):
        stamp = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(int(input_data[ptr]))
                ptr += 1
            stamp.append(row)
        stamps.append(stamp)

    # Current state
    current_board = [row[:] for row in board]
    placements = [] # list of (m, r, c)

    # 1. Greedy Phase
    # We want to pick placements that increase the sum of the board.
    # Since we add modulo 998244353, we must be careful. 
    # However, the problem says 'added to the board modulo 998244353'. 
    # This usually means (cell + stamp_val) % MOD.
    
    # To maximize sum, we look for placements where the sum of stamp elements is high
    # and doesn't cause many cells to wrap around (though wrap around might actually help if it hits a high value, 
    # but usually we just want to add large positive numbers).
    
    # Precalculate stamp sums
    stamp_sums = []
    for m in range(M):
        s = 0
        for i in range(3):
            for j in range(3):
                s += stamps[m][i][j]
        stamp_sums.append(s)

    # Greedy: pick the best available placement that doesn't exceed K
    # We'll try to pick the best (m, r, c) repeatedly.
    
    for _ in range(K):
        best_delta = -1
        best_move = None
        
        # For simplicity in this baseline, we look for the stamp/pos that adds the most to the sum
        # without considering the modulo wrap-around complexity (which is hard to predict).
        # We just look for the highest sum of stamp elements.
        
        # Optimization: find the single best move among all possible