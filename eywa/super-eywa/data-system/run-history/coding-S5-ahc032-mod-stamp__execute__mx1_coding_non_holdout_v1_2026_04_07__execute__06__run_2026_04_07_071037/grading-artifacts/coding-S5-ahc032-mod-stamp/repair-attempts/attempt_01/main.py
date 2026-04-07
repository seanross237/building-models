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
    
    # Greedy approach: in each step, pick the stamp and position that maximizes the sum increase
    # Note: The increase is (new_val - old_val). Since we are working modulo 998244353,
    # the "gain" can be large if the addition wraps around.
    # However, the problem asks to maximize the sum of final board entries.
    # The sum of entries is sum(board[i][j]).
    # When we add a stamp, the new sum is sum((board[i][j] + stamp[i][j]) % MOD).
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # The change in the total sum is (new_val - old_val)
                            # This can be negative if it wraps around the MOD.
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, r, c)
        
        # If the best gain is negative, it might still be better to place it if we have K moves,
        # but usually, we want to maximize the sum. If best_gain <= 0, we stop or skip.
        # Given the objective is to maximize the sum, we only place if it helps.
        if best_move is not None and best_gain > 0:
            m, r, c = best_move
            placements.append((m, r, c))
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    print(len(placements))
    for m, r, c in placements:
        print(f"{m} {r} {c}")

if __name__ == "__main__":
    solve()
