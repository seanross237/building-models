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
            row = []
            for c in range(3):
                row.append(int(input_data[idx]))
                idx += 1
            stamp.append(row)
        stamps.append(stamp)

    P = 998244353
    actions = []
    
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -float('inf')
        best_action = None
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            nr, nc = r + dr, c + dc
                            val_to_add = stamps[m][dr][dc]
                            if current_board[nr][nc] + val_to_add >= P:
                                gain -= 10**15
                            else:
                                gain += val_to_add
                                
                    if gain > best_gain:
                        best_gain = gain
                        best_action = (m, r, c)
        
        if best_action and best_gain > 0:
            m, r, c = best_action
            actions.append((m, r, c))
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % P

    print(sum(sum(row) for row in current_board) % P)