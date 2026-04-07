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
        for i in range(3):
            row = []
            for j in range(3):
                row.append(int(input_data[idx]))
                idx += 1
            stamp.append(row)
        stamps.append(stamp)

    MOD = 998244353
    
    # Greedy approach:
    # In each step, find the placement (m, r, c) that increases the sum of the board the most.
    # Since we are working modulo 998244353, adding a value can either increase 
    # the sum or cause a wrap-around (decrease it significantly).
    # However, the problem asks to maximize the sum of final board entries.
    # A simple greedy strategy: pick the placement that maximizes the sum of the 9 cells 
    # after the modulo operation.
    
    placements = []
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None # (m, r, c)
        
        # Try all possible placements
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    # Calculate gain for this specific placement
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, r, c)
        
        # If no move improves the sum (or if best_gain is negative), stop.
        # Actually, even if gain is negative, we might want to place it if it's part of a sequence,
        # but for a simple greedy, we only take positive gains.
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
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
