import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    K = int(input_data[2])
    
    idx = 3
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
    
    stamp_sums = []
    for m in range(M):
        s = 0
        for r in range(3):
            for c in range(3):
                s += stamps[m][r][c]
        stamp_sums.append(s)

    placements = []
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -1
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
        
        if best_move:
            m, i, j = best_move
            placements.append((i + 1, j + 1, m + 1))
            for dr in range(3):
                for dc in range(3):
                    current_board[i+dr][j+dc] = (current_board[i+dr][j+dc] + stamps[m][dr][dc]) % MOD

    print(sum(sum(row) for row in current_board) % MOD)
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

solve()