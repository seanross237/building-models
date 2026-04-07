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
    current_board = [row[:] for row in board]
    
    # Greedy approach: pick the stamp and position that maximizes the sum of the board
    # Note: The score is the sum of all final board entries.
    # Since we add modulo 998244353, the gain is not simply the sum of stamp elements.
    # However, for a greedy approach, we can look for the best immediate gain.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = current_board[i+r][j+c]
                            new_val = (old_val + stamps[m][r][c]) % MOD
                            # The change in the total sum is (new_val - old_val)
                            # But we must account for the fact that new_val might be smaller than old_val due to MOD
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        # If the best gain is negative, it might still be better to place it if we want to 
        # manipulate values for future stamps, but in a simple greedy, we stop if gain <= 0.
        # However, in this problem, adding a stamp always changes the board.
        # Let's only place if it improves the sum or if we have moves left and want to try.
        # Given the constraints and objective, we'll take any move that doesn't decrease the sum.
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for r in range(3):
                for c in range(3):
                    current_board[i+r][j+c] = (current_board[i+r][j+c] + stamps[m][r][c]) % MOD
        else:
            break

    # Output format:
    # L
    # m i j
    # ...
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
