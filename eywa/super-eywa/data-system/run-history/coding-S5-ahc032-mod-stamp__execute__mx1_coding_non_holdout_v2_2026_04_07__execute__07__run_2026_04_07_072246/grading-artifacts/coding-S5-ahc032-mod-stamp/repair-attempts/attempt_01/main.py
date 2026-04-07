import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
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

    # The problem asks for placements of stamps. 
    # The current code prints the score, but the scorer expects the placements.
    # Output format for AHC style problems usually requires the number of placements 
    # followed by the placements themselves.
    # Based on the error 'Out of range', the contestant was printing the score instead of the moves.
    
    placements = []
    current_board = [row[:] for row in board]
    MOD = 998244353
    
    # Greedy approach to find placements
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    # Calculate the change in the sum of board entries modulo 998244353
                    # Note: The problem asks to maximize the sum modulo 998244353.
                    # This is tricky because (a+b)%MOD is not necessarily > a.
                    # However, a simple greedy approach is to pick moves that don't wrap around too much
                    # or just pick the first K moves to ensure valid output.
                    gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = current_board[i+di][j+dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            # We want to maximize the sum of (new_val % MOD)
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        if best_move:
            m, i, j = best_move
            placements.append((m, i, j))
            for di in range(3):
                for dj in range(3):
                    current_board[i+di][j+dj] = (current_board[i+di][j+dj] + stamps[m][di][dj]) % MOD
        else:
            break

    # Output format: 
    # Number of placements
    # For each placement: m i j
    print(len(placements))
    for m, i, j in placements:
        print(f"{m} {i} {j}")

if __name__ == '__main__':
    solve()
