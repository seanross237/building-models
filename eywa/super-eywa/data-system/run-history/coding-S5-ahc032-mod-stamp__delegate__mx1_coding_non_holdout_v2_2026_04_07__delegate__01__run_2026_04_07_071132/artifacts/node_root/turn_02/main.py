import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
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
        for i in range(3):
            row = []
            for j in range(3):
                row.append(int(input_data[ptr]))
                ptr += 1
            stamp.append(row)
        stamps.append(stamp)

    placements = []
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            gain += (new_val - (old_val % MOD))
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, r, c)
        
        if best_move:
            m, r, c = best_move
            placements.append((m, r, c))
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    print(len(placements))
    for m, r, c in placements:
        print(f"{m} {r} {c}")

solve()