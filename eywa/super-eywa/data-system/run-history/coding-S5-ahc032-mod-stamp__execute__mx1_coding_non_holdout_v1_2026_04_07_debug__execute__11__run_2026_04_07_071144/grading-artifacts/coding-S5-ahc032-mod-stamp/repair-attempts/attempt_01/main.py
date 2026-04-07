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

    # Greedy approach:
    # Try to find the stamp and position that increases the sum of the board the most.
    # Since we are working modulo 998244353, the "sum" is tricky.
    # However, the problem asks for the sum of final board entries.
    # Let's assume the board entries are always kept in [0, 998244352].
    # A simple greedy: pick the stamp and position that maximizes the sum of (new_val - old_val) mod 998244353.
    # But wait, the problem says "added to the board modulo 998244353".
    # This usually means: board[i][j] = (board[i][j] + stamp[di][dj]) % 998244353.
    
    MOD = 998244353
    
    current_board = [row[:] for row in board]
    placements = []
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None # (m, r, c)
        
        # To keep it efficient, we don't check every single possibility every time if K is large,
        # but K=81 and N=9, M=20 is small enough.
        # Total iterations: 81 * 20 * 7 * 7 = 79,380. This is very safe for Python.
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # The gain is the difference in the sum.
                            # Note: if new_val < old_val, gain can be negative.
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, r, c)
        
        if best_move and best_gain > 0:
            m, r, c = best_move
            placements.append((m, r, c))
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
        else:
            break
            
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == '__main__':
    solve()
