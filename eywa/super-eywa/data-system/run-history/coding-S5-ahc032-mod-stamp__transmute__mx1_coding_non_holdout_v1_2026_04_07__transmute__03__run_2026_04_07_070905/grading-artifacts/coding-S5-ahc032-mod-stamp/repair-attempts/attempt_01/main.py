import sys

def solve():
    # Read N, M, K
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    K = int(input_data[2])
    
    idx = 3
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
    # Since we want to maximize the sum of the board, and the operation is (val + stamp) % MOD,
    # the "best" stamp placement is one that increases the sum the most.
    # However, because of the modulo, a large addition might wrap around to a small number.
    # A simple greedy strategy: try to find a placement that maximizes the sum of the 
    # resulting 3x3 area after the modulo operation.
    
    placements = []
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None # (m, r, c)
        
        # To keep it efficient, we don't check every single possibility if K is large,
        # but N=9, M=20, K=81 is small enough for a brute force search per step.
        # Total complexity: K * M * (N-2)^2 * 9
        # 81 * 20 * 49 * 9 approx 714,420 operations. This is well within 2 seconds.
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    # Calculate gain for this specific placement
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, r, c)
        
        # If no move improves the sum (gain <= 0), we might still want to place if 
        # we can't find anything better, but the problem says "at most K".
        # However, in modulo arithmetic, a "gain" can be negative.
        # If best_gain is negative, it means every single possible move reduces the sum.
        if best_move is not None and best_gain > 0:
            m, r, c = best_move
            placements.append((m, r, c))
            # Update board
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
