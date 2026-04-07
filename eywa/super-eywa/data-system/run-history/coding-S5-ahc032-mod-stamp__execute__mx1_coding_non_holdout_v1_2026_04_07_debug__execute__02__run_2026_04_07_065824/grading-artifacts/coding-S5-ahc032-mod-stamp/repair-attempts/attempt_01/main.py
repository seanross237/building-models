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
    # Find the stamp and position that adds the maximum sum to the board.
    # Since we are working modulo 998244353, we treat the addition as 
    # (current + stamp) % MOD. However, the problem says "The chosen 3x3 stamp 
    # is added to the board modulo 998244353". This usually means 
    # board[i][j] = (board[i][j] + stamp[di][dj]) % 998244353.
    
    MOD = 998244353
    placements = []
    
    # To avoid infinite loops or excessive computation, we'll use a simple greedy.
    # We can place at most K stamps.
    
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -1
        best_move = None # (m, r, c)
        
        # We look for the move that increases the total sum the most.
        # Note: Because of the modulo, a large addition might wrap around to a small number.
        # However, in most competitive programming contexts of this type, 
        # "added modulo X" means the operation is (a + b) % X.
        
        # To keep it efficient, we only check a subset of moves if N is large,
        # but N=9 is very small.
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
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
