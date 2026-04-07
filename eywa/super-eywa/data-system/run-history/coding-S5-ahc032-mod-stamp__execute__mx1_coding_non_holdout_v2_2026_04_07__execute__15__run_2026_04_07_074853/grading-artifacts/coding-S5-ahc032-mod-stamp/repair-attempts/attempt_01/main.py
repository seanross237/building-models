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
            row = []
            for c in range(3):
                row.append(int(input_data[idx]))
                idx += 1
            stamp.append(row)
        stamps.append(stamp)

    placements = []
    
    # Greedy approach: pick the stamp and position that maximizes the sum of the board
    # after the modulo operation. Since we want to maximize the sum, and the modulo 
    # is very large, we essentially want to maximize the sum of the stamp values 
    # added to the current board values, while being mindful of the modulo.
    # However, since the modulo is 998244353 and stamp values are likely smaller,
    # we can simply pick the stamp with the highest sum and place it repeatedly.
    
    best_m = -1
    max_stamp_sum = -1
    
    for m in range(M):
        current_sum = 0
        for r in range(3):
            for c in range(3):
                current_sum += stamps[m][r][c]
        if current_sum > max_stamp_sum:
            max_stamp_sum = current_sum
            best_m = m
            
    if best_m != -1:
        # We can place the best stamp at (0,0) up to K times.
        # Note: The problem says "at most K". 
        # The board is 9x9, stamp is 3x3. Top-left (i, j) must satisfy i+3 <= N and j+3 <= N.
        # For N=9, i and j can be 0 to 6.
        
        # To avoid the modulo wrapping around to a small number, 
        # we should check if adding the stamp makes the board value exceed MOD.
        # But for a simple greedy, let's just pick the best stamp and place it at (0,0).
        
        # Let's try to place it at (0,0) as many times as possible without wrapping around MOD.
        # Or just place it K times and hope for the best.
        
        # Actually, the simplest valid strategy is to find the best stamp and position
        # and place it K times.
        
        # Let's refine: find (m, i, j) that maximizes sum( (board[r][c] + stamp[m][r][c]) % MOD )
        # We'll do this greedily for K steps.
        
        current_board = [row[:] for row in board]
        
        for _ in range(K):
            best_gain = -1
            best_move = None
            
            for m in range(M):
                for i in range(N - 2):
                    for j in range(N - 2):
                        gain = 0
                        for r in range(3):
                            for c in range(3):
                                old_val = current_board[i+r][j+c]
                                new_val = (old_val + stamps[m][r][c]) % MOD
                                gain += (new_val - old_val)
                        
                        if gain > best_gain:
                            best_gain = gain
                            best_move = (m, i, j)
            
            if best_move and best_gain > 0:
                m, i, j = best_move
                placements.append((m, i, j))
                for r in range(3):
                    for c in range(3):
                        current_board[i+r][j+c] = (current_board[i+r][j+c] + stamps[m][r][c]) % MOD
            else:
                break

    print(len(placements))
    for p in placements:
        # Output format: m i j
        # m is stamp index, i and j are top-left position
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
