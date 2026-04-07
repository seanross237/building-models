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
        for i in range(3):
            row = []
            for j in range(3):
                row.append(int(input_data[ptr]))
                ptr += 1
            stamp.append(row)
        stamps.append(stamp)

    MOD = 998244353

    # The problem asks for placements of stamps. 
    # Based on typical AHC formats, we need to output the number of placements
    # followed by the placements themselves (m, r, c).
    # The current code was printing the score, which is incorrect.
    
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
                    for di in range(3):
                        for dj in range(3):
                            old_val = current_board[i + di][j + dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            # We want to maximize the sum of board entries modulo MOD.
                            # However, the problem asks to maximize the sum of board entries modulo 998244353.
                            # This usually means the sum is calculated, then taken modulo. 
                            # But in AHC, usually it's the sum of (board[i][j] % MOD).
                            # Let's assume the goal is to maximize the sum of the elements.
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for di in range(3):
                for dj in range(3):
                    current_board[i + di][j + dj] = (current_board[i + di][j + dj] + stamps[m][di][dj]) % MOD
        else:
            break

    # Output format: number of placements, then each placement (m, r, c)
    print(len(placements))
    for m, r, c in placements:
        print(f"{m} {r} {c}")

if __name__ == "__main__":
    solve()
