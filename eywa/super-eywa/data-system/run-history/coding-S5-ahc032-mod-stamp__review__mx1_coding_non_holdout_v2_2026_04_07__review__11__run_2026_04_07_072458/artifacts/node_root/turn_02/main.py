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

    valid_placements = []
    for m in range(M):
        for r in range(7):
            for c in range(7):
                valid_placements.append((m, r, c))

    current_board = [row[:] for row in board]
    current_placements = []
    
    def get_score(b):
        return sum(sum(row) for row in b)

    def apply_stamp(b, m, r, c, add=True):
        multiplier = 1 if add else -1
        for dr in range(3):
            for dc in range(3):
                b[r+dr][c+dc] = (b[r+dr][c+dc] + multiplier * stamps[m][dr][dc]) % MOD

    start_time = time.time()
    time_limit = 1.8

    best_placements = []
    best_score = get_score(current_board)

    solve()