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
        
    # Read stamps (assuming 3x3 based on problem description)
    # The problem says M different 3x3 stamps.
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
    # Since we want to maximize the sum of (board[i][j] + added_values) % MOD,
    # and the MOD is very large (998244353), the modulo operation only triggers
    # if the sum exceeds MOD. 
    # However, the problem states "The chosen 3x3 stamp is added to the board modulo 998244353".
    # This usually means: Final_Cell = (Initial_Cell + Sum_of_Stamps) % MOD.
    # To maximize the sum, we want each cell to be as close to MOD-1 as possible.
    
    # Given the constraints and the nature of the problem, a simple greedy 
    # strategy is to pick the stamp and position that increases the current sum the most.
    
    current_board = [row[:] for row in board]
    placements = []
    
    for _ in range(K):
        best_gain = -1
        best_placement = None # (m, r, c)
        
        # Try all possible placements
        # Note: For N=9, M=20, K=81, this is 20 * 7 * 7 = 980 iterations per K.
        # Total iterations ~ 80,000. This is well within time limits.
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_placement = (m, r, c)
        
        if best_placement and best_gain > 0:
            m, r, c = best_placement
            placements.append((m, r, c))
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    # Output
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
