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
            row = []
            for c in range(3):
                row.append(int(input_data[ptr]))
                ptr += 1
            stamp.append(row)
        stamps.append(stamp)

    MOD = 998244353
    
    placements = []
    current_board = [row[:] for row in board]
    
    # Greedy approach to find placements
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = current_board[i+r][j+c]
                            new_val = (old_val + stamps[m][r][c]) % MOD
                            # The gain is the change in the sum of the board
                            # Since we want to maximize sum % MOD, and the problem asks for sum of entries modulo MOD,
                            # we interpret this as maximizing the sum of (board[i][j] % MOD).
                            # However, the problem says 'maximize the sum of board entries modulo 998244353'.
                            # This usually means (Sum of entries) % MOD. 
                            # But in competitive programming, if the sum can be very large, 
                            # it usually means the sum of (entries % MOD) or the sum is taken modulo MOD.
                            # Given the context of AHC, it's likely maximizing the sum of entries, 
                            # and the score is that sum % MOD. 
                            # But if the sum is taken modulo MOD, the problem is non-monotonic.
                            # Let's assume we maximize the actual sum of entries.
                            gain += stamps[m][r][c]
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        if best_move:
            m, i, j = best_move
            placements.append((m, i, j))
            for r in range(3):
                for c in range(3):
                    current_board[i+r][j+c] = (current_board[i+r][j+c] + stamps[m][r][c]) % MOD
        else:
            break

    # Output format: K followed by K lines of 'm i j'
    print(len(placements))
    for m, i, j in placements:
        print(f"{m} {i} {j}")

if __name__ == '__main__':
    solve()
