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
    for _ in range(N):
        row = []
        for _ in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        board.append(row)
        
    stamps = []
    for _ in range(M):
        stamp = []
        for _ in range(3):
            s_row = []
            for _ in range(3):
                s_row.append(int(input_data[idx]))
                idx += 1
            stamp.append(s_row)
        stamps.append(stamp)
    
    MOD = 998244353
    placements = []
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m_idx in range(M):
            stamp = stamps[m_idx]
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = board[i+r][j+c]
                            new_val = (old_val + stamp[r][c]) % MOD
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m_idx, i, j)
        
        if best_move is not None and best_gain > 0:
            m_idx, i, j = best_move
            placements.append(f"{m_idx} {i} {j}")
            for r in range(3):
                for c in range(3):
                    board[i+r][j+c] = (board[i+r][j+c] + stamps[m_idx][r][c]) % MOD

    print(len(placements))
    for p in placements:
        print(p)

solve()