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
                            old_val = board[i + dr][j + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            gain = (new_val - old_val)
                            if gain < 0:
                                gain -= MOD
                            current_gain += gain
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_m = m
                        best_i = i
                        best_j = j
        
        if best_gain <= 0:
            break