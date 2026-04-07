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
        for i in range(3):
            row = []
            for j in range(3):
                row.append(int(input_data[idx]))
                idx += 1
            stamp.append(row)
        stamps.append(stamp)

    # Greedy approach:
    # In each step, find the (m, r, c) that maximizes the sum of the board
    # after applying the stamp. Since the modulo is very large, 
    # we can approximate the gain by the sum of the stamp elements.
    # However, we must account for the modulo.
    # Given the constraints and the nature of the problem, 
    # a simple greedy based on the sum of stamp elements is a good baseline.
    
    placements = []
    current_board = [row[:] for row in board]
    
    # Pre-calculate stamp sums
    stamp_sums = []
    for m in range(M):
        s = 0
        for r in range(3):
            for c in range(3):
                s += stamps[m][r][c]
        stamp_sums.append(s)

    # To handle the modulo correctly in a greedy way, we'd need to simulate.
    # But since we want to maximize the sum, and the modulo is huge,
    # we just want to add positive values.
    
    # Let's try to pick the best stamp and position greedily.
    # We can repeat this up to K times.
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        # We look for the move that increases the total sum the most.
        # Since we are adding, and the modulo is 998244353, 
        # the sum increases by (sum of stamp elements) unless a cell wraps around.
        # Because the modulo is so large, wrapping is rare.
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    # Calculate potential gain
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # The change in sum is (new_val - old_val)
                            # But we want to maximize the sum of all entries.
                            # The change in total sum is sum_{dr,dc} (new_val - old_val)
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, r, c)
        
        if best_move and best_gain > 0:
            m, r, c = best_move
            placements.append((m, r, c))
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
