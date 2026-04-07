import sys
import time

def solve():
    # Read N, M, K
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
    MOD = 998244353
    
    # Read Board
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[ptr]))
            ptr += 1
        board.append(row)
        
    # Read Stamps
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

    # Greedy Phase
    placements = []
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_inc = -1
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_sum_delta = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = current_board[i+r][j+c]
                            new_val = (old_val + stamps[m][r][c]) % MOD
                            current_sum_delta += (new_val - old_val)
                    
                    if current_sum_delta > best_inc:
                        best_inc = current_sum_delta
                        best_move = (m, i, j)
        
        if best_move:
            m, i, j = best_move
            placements.append((m, i, j))
            for r in range(3):
                for c in range(3):
                    current_board[i+r][j+c] = (current_board[i+r][j+c] + stamps[m][r][c]) % MOD

    # Output result
    total_sum = sum(sum(row) for row in current_board)
    print(total_sum)

solve()