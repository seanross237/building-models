import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx])
    M = int(input_data[idx+1])
    K = int(input_data[idx+2])
    idx += 3
    
    board = []
    for r in range(N):
        row = []
        for c in range(N):
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

    # Greedy approach:
    # Find the stamp and position that increases the sum of the board the most.
    # Since we are working modulo 998244353, we must be careful.
    # However, the problem asks to maximize the sum of final board entries.
    # The entries are (initial + sum of stamps) % 998244353.
    # This is a non-linear optimization problem due to the modulo.
    # A simple greedy strategy: pick the stamp/position that maximizes the sum 
    # of the 9 cells after the modulo operation.
    
    MOD = 998244353
    placements = []
    
    # To keep it efficient and avoid infinite loops or complexity, 
    # we'll try a simple greedy approach for a limited number of steps.
    # We'll only pick placements that actually increase the sum.
    
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -1
        best_move = None # (m, i, j)
        
        # To speed up, we don't check every single possibility every time if K is large,
        # but K=81 and N=9, M=20 is small enough.
        # Total possibilities: M * (N-2) * (N-2) = 20 * 7 * 7 = 980.
        # 81 * 980 is ~80,000, which is fine for Python.
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    # Calculate gain
                    current_sum = 0
                    new_sum = 0
                    for dr in range(3):
                        for dc in range(3):
                            val = current_board[i+dr][j+dc]
                            s_val = stamps[m][dr][dc]
                            current_sum += val
                            new_sum += (val + s_val) % MOD
                    
                    gain = new_sum - current_sum
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append(best_move)
            # Update board
            for dr in range(3):
                for dc in range(3):
                    current_board[i+dr][j+dc] = (current_board[i+dr][j+dc] + stamps[m][dr][dc]) % MOD
        else:
            break
            
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == '__main__':
    solve()
