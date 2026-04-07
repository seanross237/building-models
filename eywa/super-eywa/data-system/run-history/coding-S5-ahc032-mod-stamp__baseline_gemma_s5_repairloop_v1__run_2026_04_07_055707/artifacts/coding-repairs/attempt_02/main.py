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
    
    # The problem asks to maximize (Sum of board entries) % 998244353.
    # The error "Out of range" in the previous code was because the user printed 
    # the total_sum as the first line. 
    # Looking at the AHC032 problem description (or standard AHC format):
    # The output should be the number of placements, then the placements themselves.
    # The score is calculated by the judge.
    # Wait, the problem says "maximize the sum of board entries modulo 998244353".
    # In AHC, you don't print the score. You print the solution.
    # The error "Out of range: 708792986" means the judge expected a count (number of placements)
    # but received a large number (the sum).
    
    # Greedy approach: pick the stamp and position that increases the sum the most.
    # We will keep the sum of the board elements.
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    current_gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            # We want to maximize the sum. 
                            # Since we apply modulo at each step, we must be careful.
                            # The problem says "maximize the sum of board entries modulo 998244353".
                            # This means Score = (Sum of all board[i][j]) % 998244353.
                            # To maximize this, we want the sum to be as large as possible 
                            # without wrapping around the MOD, or to wrap around to just below MOD.
                            # However, a simple greedy on the sum is a good heuristic.
                            old_val = board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # The change in the total sum modulo MOD is (new_val - old_val) % MOD
                            # But we want to maximize the actual sum modulo MOD.
                            # Let's just track the sum of the board.
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, r, c)
        
        if best_move is not None and best_gain > 0:
            m, r, c = best_move
            for dr in range(3):
                for dc in range(3):
                    board[r + dr][c + dc] = (board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
            placements.append((m, r, c))
        else:
            break

    # Output format:
    # Number of placements
    # m r c for each placement
    print(len(placements))
    for m, r, c in placements:
        print(f"{m} {r} {c}")

if __name__ == "__main__":
    solve()
