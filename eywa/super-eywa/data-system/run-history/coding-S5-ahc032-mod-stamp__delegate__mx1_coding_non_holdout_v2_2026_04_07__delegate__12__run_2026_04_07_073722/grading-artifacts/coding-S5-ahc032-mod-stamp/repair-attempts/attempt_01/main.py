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
    
    # Read Board
    board = []
    for r in range(N):
        row = []
        for c in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        board.append(row)
        
    # Read Stamps
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
        
    placements = []
    
    # Greedy approach:
    # In each step, find the placement (m, i, j) that maximizes the sum of the board
    # after applying the stamp modulo 998244353.
    # Since K is small (81) and N is small (9), we can afford a greedy search.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        # Try all possible stamps m and top-left positions (i, j)
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    # Calculate the change in sum for this specific placement
                    for dr in range(3):
                        for dc in range(3):
                            old_val = board[i + dr][j + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        # If no move improves the sum (or if gain is negative, though unlikely with positive stamps), stop.
        # However, in this problem, we want to maximize sum, and even if gain is negative, 
        # we might want to wrap around. But a simple greedy is a good baseline.
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            # Update board
            for dr in range(3):
                for dc in range(3):
                    board[i + dr][j + dc] = (board[i + dr][j + dc] + stamps[m][dr][dc]) % MOD
        else:
            break
            
    # Output results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
