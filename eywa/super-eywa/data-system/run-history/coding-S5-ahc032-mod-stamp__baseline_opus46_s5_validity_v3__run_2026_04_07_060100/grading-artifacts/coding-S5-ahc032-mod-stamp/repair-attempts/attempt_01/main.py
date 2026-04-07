import sys

def solve():
    MOD = 998244353
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); M = int(input_data[idx+1]); K = int(input_data[idx+2])
    idx += 3

    board = []
    for i in range(N):
        row = [int(input_data[idx+j]) for j in range(N)]
        idx += N
        board.append(row)

    stamps = []
    for m in range(M):
        stamp = []
        for i in range(3):
            row = [int(input_data[idx+j]) for j in range(3)]
            idx += 3
            stamp.append(row)
        stamps.append(stamp)

    placements = []

    for _ in range(K):
        best_gain = 0
        best_m = -1
        best_i = -1
        best_j = -1

        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[i+di][j+dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            gain += new_val - old_val
                    if gain > best_gain:
                        best_gain = gain
                        best_m = m
                        best_i = i
                        best_j = j

        if best_gain <= 0:
            break

        # Apply the best placement
        m = best_m
        i = best_i
        j = best_j
        for di in range(3):
            for dj in range(3):
                board[i+di][j+dj] = (board[i+di][j+dj] + stamps[m][di][dj]) % MOD
        placements.append((m, i, j))

    # Now try a second phase: see if we can get cells closer to MOD-1 by repeated application
    # For cells that are far from MOD-1, try to find stamp placements that help
    # Use a more targeted approach: for each cell, figure out how much we need to add
    
    # Phase 2: Try to push values higher by looking at deficit from MOD-1
    # We'll do additional greedy passes considering the "wrap-around" benefit
    remaining = K - len(placements)
    
    for _ in range(remaining):
        best_gain = 0
        best_m = -1
        best_i = -1
        best_j = -1

        for m in range(M):
            # Skip stamps that are all zeros
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[i+di][j+dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            gain += new_val - old_val
                    if gain > best_gain:
                        best_gain = gain
                        best_m = m
                        best_i = i
                        best_j = j

        if best_gain <= 0:
            break

        m = best_m
        i = best_i
        j = best_j
        for di in range(3):
            for dj in range(3):
                board[i+di][j+dj] = (board[i+di][j+dj] + stamps[m][di][dj]) % MOD
        placements.append((m, i, j))

    print(len(placements))
    for m, i, j in placements:
        print(m, i, j)

solve()
