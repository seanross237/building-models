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
    
    # Pre-calculate stamp sums
    stamp_info = []
    for m in range(M):
        s_sum = 0
        for r in range(3):
            for c in range(3):
                s_sum += stamps[m][r][c]
        stamp_info.append((s_sum, m))
    
    # Sort stamps by sum descending
    stamp_info.sort(key=lambda x: x[0], reverse=True)
    
    placements = []
    current_board = [row[:] for row in board]
    
    # Greedy approach:
    # In each step, find the (m, i, j) that maximizes the increase in the total sum.
    # The increase is (new_sum - old_sum).
    # Since (A + B) % MOD is not simply A + B, we must calculate the actual change.
    # However, if we assume the values don't wrap around MOD frequently, 
    # the sum of stamps is a good heuristic.
    # But to be safe and robust, we calculate the actual delta.
    
    for _ in range(K):
        best_delta = -float('inf')
        best_move = None # (m, i, j)
        
        # Possible top-left positions (i, j) such that 3x3 fits in NxN
        # For N=9, i in [0, 6], j in [0, 6]
        for m_idx in range(M):
            m = stamp_info[m_idx][1]
            stamp = stamps[m]
            for i in range(N - 2):
                for j in range(N - 2):
                    delta = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = current_board[i+r][j+c]
                            new_val = (old_val + stamp[r][c]) % MOD
                            delta += (new_val - old_val)
                    
                    if delta > best_delta:
                        best_delta = delta
                        best_move = (m, i, j)
        
        # If the best delta is positive, apply it. 
        # If all possible moves decrease the sum, stop.
        if best_move and best_delta > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            # Update board
            for r in range(3):
                for c in range(3):
                    current_board[i+r][j+c] = (current_board[i+r][j+c] + stamps[m][r][c]) % MOD
        else:
            break

    # Output results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
