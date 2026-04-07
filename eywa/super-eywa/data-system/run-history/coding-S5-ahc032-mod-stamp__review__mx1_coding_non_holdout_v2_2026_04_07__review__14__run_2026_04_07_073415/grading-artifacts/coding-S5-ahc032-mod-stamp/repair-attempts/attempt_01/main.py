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
            s_row = []
            for c in range(3):
                s_row.append(int(input_data[idx]))
                idx += 1
            stamp.append(s_row)
        stamps.append(stamp)

    placements = []
    
    # Greedy approach: find the best (stamp, i, j) to add
    # We can do this up to K times.
    # Since N is small (9), we can afford a bit of computation.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    # Calculate gain for placing stamp m at (i, j)
                    # Gain = sum_{r,c in 3x3} ( (board[i+r][j+c] + stamp[r][c]) % MOD - board[i+r][j+c] )
                    current_gain = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = board[i+r][j+c]
                            new_val = (old_val + stamps[m][r][c]) % MOD
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        # If the best gain is positive, apply it. 
        # If best_gain is negative, it means the modulo operation reduced the sum.
        if best_move is not None and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for r in range(3):
                for c in range(3):
                    board[i+r][j+c] = (board[i+r][j+c] + stamps[m][r][c]) % MOD
        else:
            # No more moves that increase the total sum
            break
            
    # Output the results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
