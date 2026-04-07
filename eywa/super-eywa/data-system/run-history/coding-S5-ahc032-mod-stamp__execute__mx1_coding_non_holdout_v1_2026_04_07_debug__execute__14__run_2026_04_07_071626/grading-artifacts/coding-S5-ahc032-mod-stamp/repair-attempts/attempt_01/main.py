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
    
    placements = []
    
    # Greedy approach: in each step, find the stamp and position that maximizes the sum increase.
    # Note: Since we are working modulo 998244353, the "gain" can be tricky.
    # However, the problem asks to maximize the sum of final entries.
    # The gain of adding a stamp is sum((board[i+r][j+c] + stamp[r][c]) % MOD - board[i+r][j+c]).
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = board[i+r][j+c]
                            new_val = (old_val + stamps[m][r][c]) % MOD
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        # If no move improves the sum (due to modulo wrap-around), we stop or pick the best available.
        # In many cases, even if gain is negative, it might be part of a strategy, 
        # but for a simple greedy, we stop if gain <= 0.
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            # Update board
            for r in range(3):
                for c in range(3):
                    board[i+r][j+c] = (board[i+r][j+c] + stamps[m][r][c]) % MOD
        else:
            break

    # Output the results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
