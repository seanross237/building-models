import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1
    
    MOD = 998244353
    
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
        for r in range(3):
            s_row = []
            for c in range(3):
                s_row.append(int(input_data[idx]))
                idx += 1
            stamp.append(s_row)
        stamps.append(stamp)

    placements = []
    
    # Greedy approach to pick placements
    # Note: The problem asks to maximize sum modulo 998244353.
    # Since we can't easily optimize modulo, we just pick stamps that increase the sum.
    # We must ensure indices are within bounds: 1 <= r <= N-2, 1 <= c <= N-2
    # The current code uses 1-based indexing for output: (i+1, j+1, m+1)
    # For N=9, max i+r is 7+2=9. So i can go up to N-3 (index 6).
    # Wait, if N=9, and stamp is 3x3, top-left corner (i,j) can be 0 to 6.
    # 0+2=2, 6+2=8. So i in range(N-2) is correct.
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = board[i+r][j+c]
                            new_val = (old_val + stamps[m][r][c]) % MOD
                            # We want to maximize the sum. 
                            # In a simple greedy, we look at the change in sum.
                            # However, (a+b)%MOD - a can be negative if it wraps.
                            # But for a baseline, let's just try to avoid wrap-around or just pick any.
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((i + 1, j + 1, m + 1))
            for r in range(3):
                for c in range(3):
                    board[i+r][j+c] = (board[i+r][j+c] + stamps[m][r][c]) % MOD
        else:
            break

    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == '__main__':
    solve()
