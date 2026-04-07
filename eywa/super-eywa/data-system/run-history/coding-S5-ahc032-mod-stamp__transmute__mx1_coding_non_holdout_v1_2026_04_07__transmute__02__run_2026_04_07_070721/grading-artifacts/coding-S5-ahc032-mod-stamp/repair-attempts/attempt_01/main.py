import sys

def solve():
    # Read N, M, K
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx])
    M = int(input_data[idx+1])
    K = int(input_data[idx+2])
    idx += 3
    
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
            row = []
            for c in range(3):
                row.append(int(input_data[idx]))
                idx += 1
            stamp.append(row)
        stamps.append(stamp)

    # Greedy approach:
    # Since we want to maximize the sum of elements modulo 998244353,
    # and the operation is (current + stamp) % MOD, 
    # a simple greedy strategy is to pick the stamp and position that 
    # increases the total sum the most in one step.
    
    current_board = [row[:] for row in board]
    placements = []
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None # (m, i, j)
        
        # Try all possible stamps and positions
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[i + dr][j + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        # If no move improves the sum (or if gain is negative, though in this problem 
        # we can just stop), stop. However, since we want to maximize sum, 
        # we only take moves with gain > 0.
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            # Update board
            for dr in range(3):
                for dc in range(3):
                    current_board[i + dr][j + dc] = (current_board[i + dr][j + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    # Output results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
