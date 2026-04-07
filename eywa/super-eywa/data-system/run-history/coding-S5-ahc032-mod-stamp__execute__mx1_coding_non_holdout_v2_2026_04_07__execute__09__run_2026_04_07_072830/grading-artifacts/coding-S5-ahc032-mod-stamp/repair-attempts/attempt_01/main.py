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
    
    # The error 'Out of range' suggests the indices provided (i+1, j+1, m+1)
    # might be exceeding the allowed bounds for M or the board dimensions.
    # However, the problem states N=9, M is provided, and K=81.
    # Let's use a simple greedy approach but ensure we don't exceed M.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[i+di][j+dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            # We want to maximize the sum modulo 998244353.
                            # A simple greedy approach for sum modulo MOD is tricky.
                            # But the error 'Out of range' is the priority.
                            # Let's check if m+1 is the issue. The problem says M stamps.
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        if best_move is not None:
            m, i, j = best_move
            # Check if m+1 is within bounds [1, M]
            # The error 'Out of range: 7' in the log suggests m+1 might be 7 when M is smaller?
            # Or i+1/j+1 are out of bounds. Let's stick to 1-based indexing.
            placements.append((i + 1, j + 1, m + 1))
            for di in range(3):
                for dj in range(3):
                    board[i+di][j+dj] = (board[i+di][j+dj] + stamps[m][di][dj]) % MOD
        else:
            break

    # Limit placements to K
    placements = placements[:K]
    
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == '__main__':
    solve()
