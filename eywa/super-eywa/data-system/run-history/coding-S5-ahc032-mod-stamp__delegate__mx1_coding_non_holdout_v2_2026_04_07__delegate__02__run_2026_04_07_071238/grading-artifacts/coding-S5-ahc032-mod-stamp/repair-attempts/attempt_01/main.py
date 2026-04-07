import sys

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr])
    M = int(input_data[ptr+1])
    K = int(input_data[ptr+2])
    ptr += 3
    
    MOD = 998244353
    
    # Read initial board
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[ptr]))
            ptr += 1
        board.append(row)
        
    # Read M stamps
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

    placements = []
    
    # Greedy approach:
    # In each step, find the (m, i, j) that maximizes the increase in the sum of the board.
    # Since the board is updated modulo 998244353, we calculate the new sum.
    # Note: The problem asks for the sum of final board entries. 
    # Because the modulo is applied to each cell, the sum is sum(cell % MOD).
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        # Try all possible stamps and positions
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[i + di][j + dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        # If no move improves the sum (or if best_gain is negative/zero), we might stop.
        # However, in some cases, a negative gain now might lead to a huge gain later due to modulo.
        # But for a simple greedy, we take the best available if it's positive.
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            # Update the board
            for di in range(3):
                for dj in range(3):
                    board[i + di][j + dj] = (board[i + di][j + dj] + stamps[m][di][dj]) % MOD
        else:
            # If no positive gain is found, stop greedy
            break
            
    # Output the results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
