import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr])
    M = int(input_data[ptr+1])
    K = int(input_data[ptr+2])
    ptr += 3
    
    MOD = 998244353

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
            s_row = []
            for c in range(3):
                s_row.append(int(input_data[ptr]))
                ptr += 1
            stamp.append(s_row)
        stamps.append(stamp)

    for _ in range(K):
        best_gain = -float('inf')
        best_move = None

        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = board[i + dr][j + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        if best_move:
            m, i, j = best_move
            for dr in range(3):
                for dc in range(3):
                    board[i + dr][j + dc] = (board[i + dr][j + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    total_sum = sum(sum(row) for row in board) % MOD
    print(total_sum)

solve()