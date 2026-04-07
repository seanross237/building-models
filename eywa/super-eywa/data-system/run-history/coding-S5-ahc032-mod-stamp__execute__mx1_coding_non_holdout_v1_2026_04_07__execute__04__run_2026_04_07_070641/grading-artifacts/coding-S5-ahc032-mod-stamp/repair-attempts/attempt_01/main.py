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

    current_board = [row[:] for row in board]
    placements = []

    # Greedy approach: in each step, pick the stamp and position that maximizes the sum of the board
    # Since we are working modulo 998244353, the "gain" is (new_val - old_val)
    # Note: (a + b) % MOD - a can be negative if a + b >= MOD.
    # However, the problem asks to maximize the sum of final board entries.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_m = -1
        best_i = -1
        best_j = -1
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = current_board[i+di][j+dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            # The actual change in the sum of the board
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_m = m
                        best_i = i
                        best_j = j
        
        # If no placement improves the sum, we can stop or just pick the best one.
        # Given the modulo, it's possible all gains are negative.
        # But we are allowed up to K placements.
        if best_m != -1 and best_gain > -1e18: # Safety check
            # In some cases, adding a stamp might decrease the sum due to modulo.
            # But we must pick the best possible move.
            # If the best gain is extremely negative, we might want to stop.
            # However, the problem says "at most K", so we can stop if we want.
            # Let's only add if it's actually beneficial or if we want to be safe.
            # For this problem, let's only add if gain > 0 to be safe, 
            # but actually, the greedy choice is to pick the best available.
            if best_gain > 0:
                placements.append((best_m, best_i, best_j))
                for di in range(3):
                    for dj in range(3):
                        current_board[best_i+di][best_j+dj] = (current_board[best_i+di][best_j+dj] + stamps[best_m][di][dj]) % MOD
            else:
                break
        else:
            break

    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
