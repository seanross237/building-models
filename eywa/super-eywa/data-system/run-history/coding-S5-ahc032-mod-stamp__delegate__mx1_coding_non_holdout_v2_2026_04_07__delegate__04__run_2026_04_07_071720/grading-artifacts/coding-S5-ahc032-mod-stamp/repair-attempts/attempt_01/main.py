import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr])
    M = int(input_data[ptr+1])
    K = int(input_data[ptr+2])
    ptr += 3
    
    MOD = 998244353
    
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[ptr]))
            ptr += 1
        board.append(row)
        
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
    # Since the modulo is very large, the sum is maximized if we avoid the modulo wrap-around
    # or if we wrap around to a very large value.
    # However, a simple greedy strategy is to pick the placement that increases the sum the most.
    
    current_board = [row[:] for row in board]
    placements = []
    
    for _ in range(K):
        best_gain = -1
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
        
        # If no placement increases the sum, stop
        if best_move is None or best_gain <= 0:
            break
            
        # Apply the best move
        m, r, c = best_move
        placements.append((m, r, c))
        for dr in range(3):
            for dc in range(3):
                current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD

    # Output results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
