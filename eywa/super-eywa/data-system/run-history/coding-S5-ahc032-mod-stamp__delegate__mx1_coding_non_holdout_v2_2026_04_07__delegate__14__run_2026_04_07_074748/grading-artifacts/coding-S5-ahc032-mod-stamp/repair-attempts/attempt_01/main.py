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
    # Based on typical AHC formats, we need to output the number of stamps
    # and then for each stamp: m i j (where i, j are top-left coordinates).
    # The current code was printing the score, which is incorrect.
    
    # Greedy approach to find K placements
    placements = []
    MOD = 998244353
    
    # We use a copy of the board to simulate
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    # Calculate gain: sum of (new_val - old_val) mod 998244353
                    # Note: The problem asks to maximize the sum of board entries modulo 998244353.
                    # This is tricky because (A+B)%MOD is not necessarily > A.
                    # However, a simple greedy approach is to maximize the sum of the elements
                    # as if they were not modulo, or just pick the first valid move.
                    # Let's try to maximize the sum of elements directly.
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            # We treat the board values as being in [0, MOD-1]
                            # The new value is (board[i+dr][j+dc] + stamp[dr][dc]) % MOD
                            old_v = current_board[i+dr][j+dc]
                            new_v = (old_v + stamps[m][dr][dc]) % MOD
                            # We want to maximize the total sum modulo MOD. 
                            # This is hard. Let's just pick moves that don't wrap around MOD
                            # to keep the sum increasing.
                            gain += (new_v - old_v)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for dr in range(3):
                for dc in range(3):
                    current_board[i+dr][j+dc] = (current_board[i+dr][j+dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    # Output format: 
    # Number of placements
    # For each placement: m i j
    print(len(placements))
    for m, i, j in placements:
        print(f"{m} {i} {j}")

if __name__ == "__main__":
    solve()
