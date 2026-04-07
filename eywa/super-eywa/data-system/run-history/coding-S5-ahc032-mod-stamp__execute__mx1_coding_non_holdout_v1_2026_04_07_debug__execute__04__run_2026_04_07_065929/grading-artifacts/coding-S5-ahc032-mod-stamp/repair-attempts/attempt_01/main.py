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
    # Since the modulo is very large, we can treat the addition as regular addition
    # for a simple greedy heuristic, or just try to find the stamp and position
    # that adds the most value to the current board sum.
    
    MOD = 998244353
    placements = []
    
    # Current board state
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -1
        best_move = None # (m, i, j)
        
        # Try every possible stamp and position
        # Note: N is small (9), M is small (20), K is 81.
        # Total complexity per step: M * (N-2) * (N-2) = 20 * 7 * 7 = 980.
        # Total complexity: 81 * 980 = ~80,000. This is very safe for Python.
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    # Calculate gain if we place stamp m at (i, j)
                    # Gain = sum over 3x3 of ( (current[r][c] + stamp[dr][dc]) % MOD - current[r][c] )
                    # However, the problem says "The chosen 3x3 stamp is added to the board modulo 998244353"
                    # This usually means: board[r][c] = (board[r][c] + stamp[dr][dc]) % MOD
                    
                    current_gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[i + dr][j + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        # If no move improves the sum (or if best_gain is negative), stop.
        # In this specific problem, stamps are likely positive, so gain should be > 0.
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append(best_move)
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

if __name__ == '__main__':
    solve()
