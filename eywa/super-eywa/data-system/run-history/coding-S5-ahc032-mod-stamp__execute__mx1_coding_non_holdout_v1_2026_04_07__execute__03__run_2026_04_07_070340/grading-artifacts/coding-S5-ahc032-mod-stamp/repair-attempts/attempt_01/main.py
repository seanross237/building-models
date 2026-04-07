import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
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

    MOD = 998244353
    
    placements = []
    current_board = [row[:] for row in board]
    
    # Greedy approach: in each step, pick the stamp and position that maximizes the sum of the board
    # Note: The gain is (new_val - old_val). Since we are working modulo 998244353, 
    # the "gain" can be negative if the addition causes a wrap-around.
    # However, the problem asks to maximize the sum of final board entries.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = current_board[i+di][j+dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            # The change in the total sum is (new_val - old_val)
                            # But we must account for the fact that new_val is in [0, MOD-1]
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        # If the best gain is positive, apply it. 
        # In some cases, even a negative gain might be worth it if it sets up a huge gain later,
        # but for a simple greedy, we only take positive gains.
        if best_move is not None and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for di in range(3):
                for dj in range(3):
                    current_board[i+di][j+dj] = (current_board[i+di][j+dj] + stamps[m][di][dj]) % MOD
        else:
            break
            
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
