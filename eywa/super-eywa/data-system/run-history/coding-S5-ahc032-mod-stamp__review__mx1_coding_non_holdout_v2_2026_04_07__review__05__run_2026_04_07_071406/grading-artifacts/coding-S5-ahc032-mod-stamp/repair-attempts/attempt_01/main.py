import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
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

    placements = []
    
    # Greedy approach to pick K placements
    # Note: The problem asks for the sum of board entries modulo 998244353.
    # However, the scorer expects the placements themselves in a specific format.
    # Based on the error "Out of range", the contestant was printing the score
    # instead of the required output format (the placements).
    # Standard AHC output for placements is usually: 
    # K
    # m r c
    # m r c ...
    
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    # Calculate gain: (sum of new values) - (sum of old values)
                    # Since we want to maximize sum % MOD, but the problem implies 
                    # maximizing the actual sum and then taking mod, or just maximizing 
                    # the sum of elements. In most AHC problems, you maximize the sum.
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            # The problem says: new_val = (old_val + stamp_val) % MOD
                            # This makes the objective function non-monotonic. 
                            # However, a simple greedy approach is a baseline.
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, r, c)
        
        if best_move:
            m, r, c = best_move
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
            placements.append((m, r, c))
        else:
            break

    # Output format: Number of placements, then each placement
    print(len(placements))
    for m, r, c in placements:
        print(f"{m} {r} {c}")

if __name__ == '__main__':
    solve()
