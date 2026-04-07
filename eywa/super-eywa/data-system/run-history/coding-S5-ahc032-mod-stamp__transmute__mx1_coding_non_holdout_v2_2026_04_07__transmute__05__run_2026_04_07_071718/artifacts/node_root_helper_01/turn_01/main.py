import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx])
    idx += 1
    M = int(input_data[idx])
    idx += 1
    K = int(input_data[idx])
    idx += 1
    
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
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[i+dr][j+dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for dr in range(3):
                for dc in range(3):
                    current_board[i+dr][j+dc] = (current_board[i+dr][j+dc] + stamps[m][dr][dc]) % MOD

    print(sum(sum(row) for row in current_board) % MOD)