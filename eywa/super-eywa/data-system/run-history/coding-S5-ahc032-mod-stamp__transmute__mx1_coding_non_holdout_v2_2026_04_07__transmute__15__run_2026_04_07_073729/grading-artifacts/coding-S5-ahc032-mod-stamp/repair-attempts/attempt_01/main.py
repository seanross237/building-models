import sys

def solve():
    # Read N, M, K
    try:
        line1 = sys.stdin.readline().split()
        if not line1:
            return
        n, m, k = map(int, line1)
    except EOFError:
        return

    # Read initial board
    board = []
    for _ in range(n):
        board.append(list(map(int, sys.stdin.readline().split())))

    # Read M stamps
    stamps = []
    for _ in range(m):
        stamp = []
        for _ in range(3):
            stamp.append(list(map(int, sys.stdin.readline().split())))
        stamps.append(stamp)

    MOD = 998244353

    # Greedy approach:
    # Since we want to maximize the sum of the final board entries,
    # and the operation is (B[i][j] + S[dr][dc]) % MOD,
    # we want to pick stamps and positions that result in the largest possible values.
    # However, the modulo makes it non-linear.
    # A simple greedy strategy: 
    # Try to place stamps that increase the sum the most without causing a wrap-around 
    # that significantly decreases the value.
    
    # For a small N=9, M=20, K=81, we can try a simple greedy:
    # In each step, find the (stamp, r, c) that maximizes the sum of the board.
    
    current_board = [row[:] for row in board]
    placements = []

    for _ in range(k):
        best_gain = -float('inf')
        best_move = None
        
        # To speed up, we don't check every single possibility if K is large,
        # but here K=81 and N=9, M=20 is small enough.
        # Total possibilities: 20 * 7 * 7 = 980
        
        for s_idx in range(m):
            for r in range(n - 2):
                for c in range(n - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[s_idx][dr][dc]) % MOD
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (s_idx, r, c)
        
        # If no move improves the sum, stop.
        # Note: In some cases, a move might decrease the sum now but allow a huge increase later.
        # But for a simple greedy, we stop if gain <= 0.
        if best_move and best_gain > 0:
            s_idx, r, c = best_move
            placements.append(best_move)
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[s_idx][dr][dc]) % MOD
        else:
            break

    # Output results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
