import sys

def solve():
    # Read all input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr])
    M = int(input_data[ptr+1])
    K = int(input_data[ptr+2])
    ptr += 3
    
    # Read initial board (N x N)
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[ptr]))
            ptr += 1
        board.append(row)
        
    # Read M stamps (3 x 3)
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

    # Greedy approach:
    # We want to maximize the sum of the board entries modulo 998244353.
    # Since the modulo is very large and the board is small, 
    # we can try to find the stamp and position that adds the most to the current sum.
    # However, a simple greedy might be too slow or suboptimal.
    # Let's try a simple greedy: pick the stamp and position that increases the sum the most.
    
    MOD = 998244353
    placements = []
    
    # Current board state
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -1
        best_move = None # (m, r, c)
        
        # Try all possible stamps and positions
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # The gain is the difference in the sum
                            # Note: because of modulo, gain can be negative if it wraps around
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, r, c)
        
        # If no move improves the sum (or if best_gain is negative), stop
        # But in this problem, we can just take any move that doesn't decrease the sum.
        # Actually, even if it decreases, we might want it if it allows better moves later.
        # But for a simple baseline, we only take positive gains.
        if best_move and best_gain > 0:
            m, r, c = best_move
            placements.append((m, r, c))
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    # Output results
    print(len(placements))
    for m, r, c in placements:
        print(f"{m} {r} {c}")

if __name__ == '__main__':
    solve()
