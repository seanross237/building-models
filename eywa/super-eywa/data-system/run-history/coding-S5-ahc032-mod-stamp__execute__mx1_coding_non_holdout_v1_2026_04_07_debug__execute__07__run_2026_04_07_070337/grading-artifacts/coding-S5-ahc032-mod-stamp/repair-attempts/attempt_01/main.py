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
        for r in range(3):
            row = []
            for c in range(3):
                row.append(int(input_data[idx]))
                idx += 1
            stamp.append(row)
        stamps.append(stamp)

    MOD = 998244353
    
    # Greedy approach: 
    # We want to maximize the sum of the board.
    # Since the operation is addition modulo 998244353, 
    # a simple greedy approach is to pick the stamp and position 
    # that increases the sum the most at each step.
    # However, because of the modulo, "increasing the sum" is tricky.
    # But the problem asks for the sum of final board entries.
    # If we assume the values don't wrap around too often or we just want 
    # to add large values, we can pick the stamp with the largest sum.
    
    current_board = [row[:] for row in board]
    placements = []
    
    # Pre-calculate stamp sums
    stamp_sums = []
    for m in range(M):
        s = 0
        for r in range(3):
            for c in range(3):
                s += stamps[m][r][c]
        stamp_sums.append(s)

    # Find the best stamp (highest sum)
    best_m = 0
    max_s = -1
    for m in range(M):
        if stamp_sums[m] > max_s:
            max_s = stamp_sums[m]
            best_m = m
            
    # To avoid modulo issues in a simple greedy, we just try to place 
    # the best stamp in all possible positions until K is reached.
    # We prioritize positions that don't cause a wrap-around if possible,
    # but since we don't know the future, we'll just fill greedily.
    
    # A slightly better greedy: 
    # In each step, find (m, i, j) that maximizes the sum of the board after placement.
    # Since N is small (9x9), we can afford some computation.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    # Calculate gain: sum(new_vals) - sum(old_vals)
                    # new_val = (old_val + stamp_val) % MOD
                    gain = 0
                    for r in range(3):
                        for c in range(3):
                            old_v = current_board[i+r][j+c]
                            new_v = (old_v + stamps[m][r][c]) % MOD
                            gain += (new_v - old_v)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            # Update board
            for r in range(3):
                for c in range(3):
                    current_board[i+r][j+c] = (current_board[i+r][j+c] + stamps[m][r][c]) % MOD
        else:
            break

    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
