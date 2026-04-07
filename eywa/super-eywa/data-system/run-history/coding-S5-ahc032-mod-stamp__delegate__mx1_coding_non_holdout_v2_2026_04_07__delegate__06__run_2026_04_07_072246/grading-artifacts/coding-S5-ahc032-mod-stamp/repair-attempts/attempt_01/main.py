import sys

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1
    
    MOD = 998244353
    
    # Read initial board
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        board.append(row)
        
    # Read M stamps
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
    
    # Greedy approach:
    # In each step, find the (stamp, i, j) that maximizes the sum of the board after addition.
    # Since we want to maximize the sum of entries, and entries are modulo 998244353,
    # we look for the placement that results in the largest increase in the sum.
    # Note: The problem says 'added to the board modulo 998244353'. 
    # This usually means (board[i][j] + stamp[r][c]) % MOD.

    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = board[i + r][j + c]
                            new_val = (old_val + stamps[m][r][c]) % MOD
                            # The gain is the difference between new and old value
                            # Note: gain can be negative if the modulo wraps around
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        # If the best gain is non-positive, we might stop, 
        # but since we want to maximize sum, we only take if it helps.
        # However, in competitive programming, usually we take any move that doesn't hurt.
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for r in range(3):
                for c in range(3):
                    board[i + r][j + c] = (board[i + r][j + c] + stamps[m][r][c]) % MOD
        else:
            break

    # Output the results
    print(len(placements))
    for m, i, j in placements:
        print(f"{m} {i} {j}")

if __name__ == "__main__":
    solve()
