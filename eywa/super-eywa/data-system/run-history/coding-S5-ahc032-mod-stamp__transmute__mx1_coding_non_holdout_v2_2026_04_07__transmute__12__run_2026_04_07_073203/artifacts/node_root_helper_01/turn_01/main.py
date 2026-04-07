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
    for r in range(N):
        row = []
        for c in range(N):
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
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_sum_delta = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = board[i+dr][j+dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            current_sum_delta += (new_val - old_val)
                    
                    if current_sum_delta > best_gain:
                        best_gain = current_sum_delta
                        best_move = (m, i, j)
        
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for dr in range(3):
                for dc in range(3):
                    board[i+dr][j+dc] = (board[i+dr][j+dc] + stamps[m][dr][dc]) % MOD
        else:
            break
            
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()