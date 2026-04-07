import sys
import random
import time

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
    board_size = 9
    board = []
    for i in range(board_size):
        row = []
        for j in range(board_size):
            row.append(int(input_data[ptr]))
            ptr += 1
        board.append(row)
        
    MOD = 998244353
    
    stamps = []
    for m in range(M):
        stamp = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(int(input_data[ptr]))
                ptr += 1
            stamp.append(row)
        stamps.append(stamp)

    current_board = [row[:] for row in board]
    placements = []

    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(7):
                for j in range(7):
                    gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = current_board[i+di][j+dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            gain += (new_val - old_val)
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for di in range(3):
                for dj in range(3):
                    current_board[i+di][j+dj] = (current_board[i+di][j+dj] + stamps[m][di][dj]) % MOD
        else:
            break

    print(len(placements))
    for m, i, j in placements:
        print(f"{m} {i} {j}")

solve()