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

    MOD = 998244353
    placements = []
    
    # Greedy approach: in each step, find the stamp and position that maximizes the sum increase.
    # Note: Since we are working modulo 998244353, the "gain" is (new_val - old_val).
    # However, if (old_val + stamp_val) >= MOD, the value wraps around, potentially decreasing the sum.
    # We must account for this wrap-around in our greedy calculation.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[i+di][j+dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            # The actual change in the sum is (new_val - old_val)
                            # This handles the modulo wrap-around correctly.
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        # If the best gain is non-positive, we might stop, but the problem says "at most K".
        # To maximize sum, we only place if gain > 0.
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for di in range(3):
                for dj in range(3):
                    board[i+di][j+dj] = (board[i+di][j+dj] + stamps[m][di][dj]) % MOD
        else:
            break

    # Output the number of placements
    print(len(placements))
    # Output each placement
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
