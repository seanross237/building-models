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
    
    # Greedy approach: pick the best move that increases the total sum
    # The sum increases if (old + stamp) % MOD > old
    # Since MOD is very large, (old + stamp) % MOD is usually just old + stamp
    # unless old + stamp >= MOD.
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[i + di][j + dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            # The gain is the difference in the sum of board entries
                            # Note: new_val - old_val can be negative if modulo wraps around
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        if best_move is not None and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for di in range(3):
                for dj in range(3):
                    board[i + di][j + dj] = (board[i + di][j + dj] + stamps[m][di][dj]) % MOD
        else:
            break

    # Output format:
    # L
    # m i j (L lines)
    print(len(placements))
    for m, i, j in placements:
        print(f"{m} {i} {j}")

if __name__ == "__main__":
    solve()
