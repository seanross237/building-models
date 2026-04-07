import sys

def solve():
    # Read N, M, K
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    K = int(input_data[2])
    
    MOD = 998244353
    
    # Read initial board
    board = []
    idx = 3
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
        
    placements = []
    
    # Greedy approach:
    # In each step, find the (m, r, c) that maximizes the increase in total sum.
    # Since the modulo is very large, we assume the sum increases unless a cell wraps.
    # Because we want to maximize the sum, and the modulo is 998244353,
    # we should avoid wrapping around.
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        # Try all possible placements
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    current_gain = 0
                    possible = True
                    
                    # Calculate gain and check for modulo wrap-around
                    for dr in range(3):
                        for dc in range(3):
                            new_val = (board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
                            # If the modulo operation significantly reduces the value, 
                            # it's a bad move.
                            # A simple heuristic: if new_val < old_val, it wrapped.
                            # However, we want to maximize the sum.
                            # Let's calculate the actual change in sum.
                            old_val = board[r + dr][c + dc]
                            gain = new_val - old_val
                            current_gain += gain
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, r, c)
        
        # If no move improves the sum, stop
        if best_move is None or best_gain <= 0:
            break
            
        # Apply the best move
        m, r, c = best_move
        placements.append((m, r, c))
        for dr in range(3):
            for dc in range(3):
                board[r + dr][c + dc] = (board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
                
    # Output results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
