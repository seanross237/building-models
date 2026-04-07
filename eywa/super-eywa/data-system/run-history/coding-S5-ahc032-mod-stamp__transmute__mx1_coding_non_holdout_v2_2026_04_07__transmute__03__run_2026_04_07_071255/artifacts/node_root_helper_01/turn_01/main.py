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
        for r in range(3):
            row = []
            for c in range(3):
                row.append(int(input_data[ptr]))
                ptr += 1
            stamp.append(row)
        stamps.append(stamp)

    MOD = 998244353
    placements = []
    
    for _ in range(K):
        best_val = -1
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for r in range(3):
                        for c in range(3):
                            current_gain += stamps[m][r][c]
                    
                    if current_gain > best_val:
                        best_val = current_gain
                        best_move = (m, i, j)
        
        if best_move:
            m, i, j = best_move
            placements.append((m, i, j))
            for r in range(3):
                for c in range(3):
                    board[i+r][j+c] = (board[i+r][j+c] + stamps[m][r][c]) % MOD

    print(len(placements))
    for m, i, j in placements:
        print(f"{m} {i} {j}")

solve()