import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1
    
    board = []
    for r in range(N):
        row = []
        for c in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        board.append(row)
        
    stamps = []
    for m in range(M):
        stamp = []
        for r in range(3):
            s_row = []
            for c in range(3):
                s_row.append(int(input_data[idx]))
                idx += 1
            stamp.append(s_row)
        stamps.append(stamp)

    MOD = 998244353
    
    # Greedy approach to find placements
    # Note: The problem asks to maximize the sum modulo 998244353.
    # However, since the board values and stamp values are added, 
    # and the modulo is applied to the final board entries, 
    # a simple greedy approach on the sum of (new_val - old_val) % MOD 
    # is a reasonable baseline.
    
    current_board = [row[:] for row in board]
    placements = []
    
    for _ in range(K):
        best_gain = -1
        best_m = -1
        best_i = -1
        best_j = -1
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[i + dr][j + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            gain = (new_val - old_val)
                            if gain < 0: gain += MOD
                            current_gain += gain
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_m = m
                        best_i = i
                        best_j = j
        
        if best_m != -1 and best_gain > 0:
            placements.append((best_m, best_i, best_j))
            for dr in range(3):
                for dc in range(3):
                    current_board[best_i + dr][best_j + dc] = (current_board[best_i + dr][best_j + dc] + stamps[best_m][dr][dc]) % MOD
        else:
            break

    # Output format: 
    # Number of placements
    # For each placement: m i j
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == '__main__':
    solve()
