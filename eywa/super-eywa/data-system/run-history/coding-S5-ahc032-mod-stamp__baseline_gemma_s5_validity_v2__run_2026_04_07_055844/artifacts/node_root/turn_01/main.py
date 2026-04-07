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
        for r in range(3):
            s_row = []
            for c in range(3):
                s_row.append(int(input_data[idx]))
                idx += 1
            stamp.append(s_row)
        stamps.append(stamp)

    placements = []
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = board[i+r][j+c]
                            new_val = (old_val + stamps[m][r][c]) % MOD
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for r in range(3):
                for c in range(3):
                    board[i+r][j+c] = (board[i+r][j+c] + stamps[m][r][c]) % MOD

    print(sum(sum(row) for row in board))

solve()