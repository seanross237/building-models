import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1
    
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

    for _ in range(K):
        best_gain = -1
        best_m = -1
        best_i = -1
        best_j = -1
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for di in range(3):
                        for dj in range(3):
                            current_gain += stamps[m][di][dj]
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_m = m
                        best_i = i
                        best_j = j
        
        if best_m != -1:
            for di in range(3):
                for dj in range(3):
                    board[best_i + di][best_j + dj] = (board[best_i + di][best_j + dj] + stamps[best_m][di][dj]) % MOD

    total_sum = 0
    for i in range(N):
        for j in range(N):
            total_sum = (total_sum + board[i][j]) % MOD
    print(total_sum)

solve()