import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx])
    M = int(input_data[idx+1])
    K = int(input_data[idx+2])
    idx += 3
    
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        board.append(row)
        
    stamps = []
    for m in range(M):
        stamp = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(int(input_data[idx]))
                idx += 1
            stamp.append(row)
        stamps.append(stamp)

    # Greedy approach:
    # We want to maximize the sum of board entries modulo 998244353.
    # Since the modulo is very large, we can treat the addition as regular addition
    # and try to pick stamps that have the largest sum of elements.
    # We can place stamps at any (i, j) such that 0 <= i <= N-3 and 0 <= j <= N-3.
    
    MOD = 998244353
    
    # Pre-calculate stamp sums
    stamp_sums = []
    for m in range(M):
        s = 0
        for r in range(3):
            for c in range(3):
                s += stamps[m][r][c]
        stamp_sums.append((s, m))
    
    # Sort stamps by sum descending
    stamp_sums.sort(key=lambda x: x[0], reverse=True)
    best_stamp_idx = stamp_sums[0][1]
    
    placements = []
    current_board = [row[:] for row in board]
    
    # Try to place the best stamp in all possible positions up to K times
    # To avoid over-complicating, we just pick the best stamp and place it 
    # in every possible position (i, j) until we hit K or run out of positions.
    # However, we must ensure we don't exceed K.
    
    count = 0
    for i in range(N - 2):
        for j in range(N - 2):
            if count < K:
                placements.append((best_stamp_idx, i, j))
                count += 1
                # Update board to simulate modulo (though for greedy sum we just add)
                for r in range(3):
                    for c in range(3):
                        current_board[i+r][j+c] = (current_board[i+r][j+c] + stamps[best_stamp_idx][r][c]) % MOD
            else:
                break
        if count >= K:
            break
            
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == '__main__':
    solve()
