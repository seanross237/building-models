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

    MOD = 998244353

    # Greedy approach:
    # Try to find the stamp and position that increases the total sum the most.
    # Since we want to maximize the sum of board entries modulo 998244353,
    # and the board entries are updated by (current + stamp) % MOD,
    # this is a non-linear optimization.
    # However, a simple greedy heuristic is to pick the stamp/position 
    # that results in the largest sum of the affected 3x3 area.
    
    current_board = [row[:] for row in board]
    placements = []
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None # (m, r, c)
        
        # To keep it efficient, we only check a subset or use a heuristic
        # if K and N were larger, but 9x9 is small.
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    # Calculate the sum of the 3x3 area after applying the stamp
                    current_area_sum = 0
                    new_area_sum = 0
                    for dr in range(3):
                        for dc in range(3):
                            val = current_board[r + dr][c + dc]
                            stamp_val = stamps[m][dr][dc]
                            current_area_sum += val
                            new_area_sum += (val + stamp_val) % MOD
                    
                    gain = new_area_sum - current_area_sum
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, r, c)
        
        # If no move improves the sum (or if gain is negative, though in this problem 
        # we just want to maximize), we stop. But since we want to maximize, 
        # we only take moves with gain > 0.
        if best_move and best_gain > 0:
            m, r, c = best_move
            placements.append((m, r, c))
            # Update board
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == '__main__':
    solve()
