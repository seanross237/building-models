import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    K = int(input_data[2])
    
    idx = 3
    board = []
    for r in range(N):
        row = []
        for c in range(N):
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

    MOD = 998244353
    
    placements = []
    current_board = [row[:] for row in board]
    
    # Greedy approach to maximize the sum of board entries
    # Note: The score is the sum of final board entries.
    # Since we add modulo 998244353, we want to avoid the wrap-around 
    # that results in a small number. However, the problem asks for 
    # the sum of final entries.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = current_board[i+dr][j+dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # The gain is the difference in the sum
                            gain += (new_val - old_val)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, i, j)
        
        # If no move improves the sum (or if best_gain is negative), 
        # we might still want to place stamps if they are positive.
        # But in this problem, we can place up to K.
        if best_move is not None and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for dr in range(3):
                for dc in range(3):
                    current_board[i+dr][j+dc] = (current_board[i+dr][j+dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    # Output format:
    # L
    # m i j
    print(len(placements))
    for p in placements:
        # m is index, i and j are top-left positions
        # The problem says "m i j" where m is index and (i, j) is top-left.
        # The current code uses 0-based indexing for m, i, j.
        # The problem description doesn't specify 0 or 1 based, 
        # but standard competitive programming is 0-based for indices 
        # unless specified. However, the previous failed code used 1-based 
        # for i, j and m, which was wrong. Let's use 0-based.
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
