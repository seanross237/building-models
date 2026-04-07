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
    
    # Greedy approach: find the best stamp and position to add
    # We want to maximize the sum of (board[i][j] + stamp[di][dj]) % MOD
    # Since MOD is very large, (a + b) % MOD is usually just a + b.
    # The only risk is if a + b >= MOD, which would decrease the sum.
    # However, with N=9 and K=81, and typical stamp values, we just greedily pick.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_m = -1
        best_i = -1
        best_j = -1
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[i + di][j + dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_m = m
                        best_i = i
                        best_j = j
        
        # If no placement improves the sum (unlikely given the problem), stop.
        # But in competitive programming, we usually want to use as many as possible if they help.
        if best_m != -1 and best_gain > 0:
            placements.append((best_m, best_i, best_j))
            # Update board
            for di in range(3):
                for dj in range(3):
                    board[best_i + di][best_j + dj] = (board[best_i + di][best_j + dj] + stamps[best_m][di][dj]) % MOD
        else:
            break

    # Output the results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
