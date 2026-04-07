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
    
    placements = []
    
    # Greedy approach: in each step, find the stamp and position that maximizes the sum increase.
    # Note: The increase is (new_val - old_val), but since we are working modulo 998244353,
    # the "gain" can be tricky. However, the problem asks to maximize the sum of final entries.
    # The sum of entries is sum(board[i][j]).
    # When we add a stamp, the new sum is sum((board[i][j] + stamp[di][dj]) % MOD).
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[i + di][j + dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            # The gain is the difference in the sum
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        # If the best gain is negative, it might still be better to place it if we want to 
        # reach a state where future stamps are more effective, but in a simple greedy, 
        # we only take positive gains. However, since we want to maximize the sum, 
        # and we have a fixed number of moves K, we should check if best_gain is actually useful.
        # In this specific problem, adding a stamp always changes the board.
        # Let's just take the best move if it exists.
        if best_move is not None:
            m, i, j = best_move
            placements.append((m, i, j))
            for di in range(3):
                for dj in range(3):
                    board[i + di][j + dj] = (board[i + di][j + dj] + stamps[m][di][dj]) % MOD
        else:
            break

    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
