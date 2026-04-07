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

    placements = []
    
    # Greedy approach: pick the stamp and position that increases the sum the most
    # Note: The problem asks to maximize (sum of board entries) % MOD.
    # However, in competitive programming, "maximize sum modulo X" usually implies 
    # the sum itself is calculated, then the modulo is applied for the score, 
    # OR the sum is kept within bounds. 
    # The error "Out of range" suggests the sum printed was >= MOD.
    # The problem asks to maximize the sum of board entries modulo 998244353.
    # This usually means: Score = (Sum of all board[i][j]) % 998244353.
    # The error "Out of range: 611935616" is actually < 998244353.
    # Wait, the error "Out of range" in AtCoder/AHC usually means the value 
    # provided is not in the range [0, MOD-1].
    # Let's ensure the total_sum is strictly within [0, MOD-1].
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    current_gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            # We want to maximize the sum. 
                            # Since we apply modulo at each step, we must be careful.
                            # But the problem says "maximize the sum of board entries modulo 998244353".
                            # This is ambiguous. Usually, it means (Sum % MOD).
                            # If we want to maximize (Sum % MOD), a greedy approach on the sum 
                            # is a heuristic.
                            old_val = board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # The change in the total sum modulo MOD is (new_val - old_val) % MOD
                            # But we want to maximize the actual sum modulo MOD.
                            # Let's just track the sum of the board.
                            current_gain += (new_val - old_val)
                    
                    # If current_gain is negative due to modulo wrap-around, 
                    # it's not necessarily bad for the modulo sum, but let's 
                    # try to keep the sum increasing to avoid complexity.
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, r, c)
        
        if best_move and best_gain > 0:
            m, r, c = best_move
            for dr in range(3):
                for dc in range(3):
                    board[r + dr][c + dc] = (board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
            placements.append((m, r, c))
        else:
            break

    total_sum = 0
    for i in range(N):
        for j in range(N):
            total_sum = (total_sum + board[i][j]) % MOD
            
    print(total_sum)
    print(len(placements))
    for m, r, c in placements:
        print(f"{m} {r} {c}")

if __name__ == "__main__":
    solve()
